import {Dialog, addAlert, postJson} from "../common"
import {COMMENT_ONLY_ROLES, READ_ONLY_ROLES} from "../editor"

import {PublishDoc} from "./publish_doc"
import {submitDialogTemplate} from "./templates"
import {getTextContent} from "./tools"

import * as plugins from "../../plugins/website"

// Adds functions for Publishing to the editor
export class EditorWebsite {
    constructor(editor) {
        this.editor = editor
        this.publishUrl = "/api/website/publish_doc/"
        this.submission = {
            status: "unknown"
        }
    }

    init() {
        this.activateFidusPlugins()
        const docData = {
            doc_id: this.editor.docInfo.id
        }
        postJson("/api/website/get_doc_info/", docData)
            .then(({json}) => {
                this.submission = json["submission"]
                this.setupUI()
            })
            .catch(error => {
                addAlert("error", gettext("Could not obtain submission info."))
                throw error
            })
    }

    activateFidusPlugins() {
        // Add plugins.
        this.plugins = {}

        Object.keys(plugins).forEach(plugin => {
            if (typeof plugins[plugin] === "function") {
                this.plugins[plugin] = new plugins[plugin](this)
                this.plugins[plugin].init()
            }
        })
    }

    setupUI() {
        const websiteMenu = {
            title: gettext("Website"),
            id: "website",
            type: "menu",
            tooltip: gettext("Publish to website"),
            order: 10,
            disabled: editor => editor.docInfo.access_rights !== "write",
            content: [
                {
                    title:
                        this.submission.user_role === "editor"
                            ? gettext("Publish")
                            : gettext("Submit"),
                    type: "action",
                    tooltip:
                        this.submission.user_role === "editor"
                            ? gettext("Publish, reject or request changes")
                            : gettext("Submit for publishing to website"),
                    action: () => {
                        if (this.submission.user_role === "editor") {
                            this.publishDialog()
                        } else {
                            this.submitDialog()
                        }
                    },
                    disabled: editor => {
                        if (
                            READ_ONLY_ROLES.includes(
                                editor.docInfo.access_rights
                            ) ||
                            COMMENT_ONLY_ROLES.includes(
                                editor.docInfo.access_rights
                            )
                        ) {
                            return true
                        } else {
                            return false
                        }
                    }
                }
            ]
        }
        this.addArticleLinkUI(websiteMenu)
        this.editor.menu.headerbarModel.content.push(websiteMenu)
        if (this.editor.menu.headerView) {
            this.editor.menu.headerView.update()
        }
        return Promise.resolve()
    }

    addArticleLinkUI(websiteMenu) {
        if (
            this.submission.id &&
            ["resubmitted", "published"].includes(this.submission.status) &&
            websiteMenu.content.length < 2
        ) {
            websiteMenu.content.push({
                title: gettext("View on website"),
                type: "action",
                tooltip: gettext(
                    "Go to the last published version on the website."
                ),
                action: () => {
                    this.editor.app.goTo(`/article/${this.submission.id}/`)
                }
            })
        }
    }

    submitDialog() {
        const buttons = [
            {
                text: gettext("Submit"),
                classes: "fw-dark",
                click: () => {
                    const message = document
                        .getElementById("submission-message")
                        .value.trim()
                    this.submitDoc({message}).then(() => dialog.close())
                }
            },
            {
                type: "cancel"
            }
        ]

        const dialog = new Dialog({
            width: 750,
            id: "submission-dialog",
            buttons,
            title: gettext("Submit document to be published on website"),
            body: submitDialogTemplate({
                messages: this.submission.messages,
                status: this.submission.status
            })
        })
        dialog.open()
    }

    submitDoc({message}) {
        const docData = {
            doc_id: this.editor.docInfo.id,
            message
        }
        return postJson("/api/website/submit_doc/", docData).then(({json}) => {
            this.submission.status = json.status
            this.submission.messages.push(json.message)
            addAlert("info", gettext("Submitted document for publication."))
        })
    }

    // The dialog for a document reviewer.
    publishDialog() {
        const buttons = [
                {
                    text: gettext("Publish"),
                    click: () => {
                        const message = document
                            .getElementById("submission-message")
                            .value.trim()
                        this.publish(message).then(() => dialog.close())
                    },
                    classes: "fw-dark"
                },
                {
                    text: gettext("Ask for changes"),
                    click: () => {
                        const message = document
                            .getElementById("submission-message")
                            .value.trim()
                        this.review(message).then(() => dialog.close())
                    },
                    classes: "fw-dark"
                },
                {
                    text: gettext("Reject"),
                    click: () => {
                        const message = document
                            .getElementById("submission-message")
                            .value.trim()
                        this.reject(message).then(() => dialog.close())
                    },
                    classes: "fw-dark"
                },
                {
                    type: "cancel"
                }
            ],
            dialog = new Dialog({
                width: 750,
                id: "submission-dialog",
                title: gettext("Publish, reject or ask for changes"),
                body: submitDialogTemplate({
                    messages: this.submission.messages,
                    status: this.submission.status
                }),
                buttons
            })

        dialog.open()
    }

    publish(message) {
        const doc = this.editor.getDoc({changes: "acceptAllNoInsertions"})
        doc.path = ""
        const article = doc.content
        // remove title
        article.content.shift()
        // Author field is only used on frontpage. We leave it in to be used on main article page.
        const authors = article.content
            .filter(
                part => part.attrs.metadata === "authors" && !part.attrs.hidden
            )
            .map(authorPart =>
                authorPart.content
                    ? authorPart.content
                          .filter(
                              author =>
                                  !author.marks ||
                                  !author.marks.find(
                                      mark => mark.type === "deletion"
                                  )
                          )
                          .map(author => author.attrs)
                    : []
            )
            .flat()
        if (authors.length) {
            // remove authors from document
            article.content = article.content.filter(
                part => part.attrs.metadata !== "authors"
            )
        } else {
            if (this.submission.submitter) {
                authors.push(this.submission.submitter)
            } else {
                const author = {
                    firstname:
                        this.editor.user.first_name || this.editor.user.name
                }
                if (this.editor.user.last_name.length) {
                    author.lastname = this.editor.user.last_name
                }
                const email = this.editor.user.emails.find(
                    email => email.primary
                )?.address
                if (email) {
                    author.email = email
                }
                authors.push(author)
            }
        }
        const keywords = article.content
            .filter(
                part => part.attrs.metadata === "keywords" && !part.attrs.hidden
            )
            .map(keywordPart =>
                keywordPart.content
                    ? keywordPart.content
                          .filter(
                              keyword =>
                                  !keyword.marks ||
                                  !keyword.marks.find(
                                      mark => mark.type === "deletion"
                                  )
                          )
                          .map(keyword => keyword.attrs.tag)
                    : []
            )
            .flat()

        // remove keywords
        article.content = article.content.filter(
            part => part.attrs.metadata !== "keywords"
        )

        // Abstract field is only used on front page. We leave it in to be used on the main article page.
        let abstract = article.content
            .filter(
                part => part.attrs.metadata === "abstract" && !part.attrs.hidden
            )
            .map(part => getTextContent(part))
            .join("")
            .replace(/(^\s*)|(\s*$)/gi, "")
            .replace(/[ ]{2,}/gi, " ")
            .replace(/\n /, "\n")
            .replace(/\n{2,}/gi, "\n")
            .trim()

        if (!abstract.length) {
            // There was no usable abstract text included. Use instead 500 chars
            // of other content, except for the title.
            abstract = article.content
                .slice(1)
                .map(part => getTextContent(part))
                .join("")
                .replace(/(^\s*)|(\s*$)/gi, "")
                .replace(/[ ]{2,}/gi, " ")
                .replace(/\n /, "\n")
                .replace(/\n{2,}/gi, "\n")
                .trim()
            abstract = abstract.slice(0, 500)
        }

        const publisher = new PublishDoc(
            this.publishUrl,
            this.editor.user,
            message,
            authors,
            keywords,
            abstract,
            doc,
            this.editor.mod.db.bibDB,
            this.editor.mod.db.imageDB,
            this.editor.app.csl,
            this.editor.docInfo.updated,
            this.editor.mod.documentTemplate.documentStyles
        )
        return publisher.init().then(({json}) => {
            this.submission.status = json.status
            this.submission.id = json.id
            this.submission.messages.push(json.message)
            addAlert("info", gettext("Published document."))
            const websiteMenu = this.editor.menu.headerbarModel.content.find(
                menu => menu.id === "website"
            )
            if (websiteMenu) {
                this.addArticleLinkUI(websiteMenu)
            }
        })
    }

    reject(message) {
        return postJson("/api/website/reject_doc/", {
            doc_id: this.editor.docInfo.id,
            message
        }).then(({json}) => {
            this.submission.status = json.status
            this.submission.messages.push(json.message)
            addAlert(
                "info",
                gettext("Publication of document has been rejected.")
            )
        })
    }

    review(message) {
        return postJson("/api/website/review_doc/", {
            doc_id: this.editor.docInfo.id,
            message
        }).then(({json}) => {
            this.submission.messages.push(json.message)
            addAlert(
                "info",
                gettext(
                    "Document has been reviewed. Request for changes has been sent."
                )
            )
        })
    }
}
