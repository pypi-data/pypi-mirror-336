import {escapeText} from "../../common"

const publicationOverviewTemplate = ({
    title,
    keywords,
    authors,
    updated,
    _added,
    abstract,
    id
}) =>
    `<a class="article"  href="/article/${id}/">
        <div class="keywords">${keywords
            .map(keyword => `<div class="keyword">${escapeText(keyword)}</div>`)
            .join("")}</div>
        <h1 class="article-title">${escapeText(title)}</h1>
        <h3 class="article-updated">${updated.slice(0, 10)}</h3>
        <div class="authors">${authors
            .map(
                author =>
                    `<div class="author">${escapeText(author.firstname)}${
                        author.lastname ? ` ${author.lastname}` : ""
                    }</div>`
            )
            .join("")}</div>
        <div class="abstract">${abstract
            .slice(0, 250)
            .split("\n")
            .map(part => `<p>${escapeText(part)}</p>`)
            .join("")}</div>
    </a>`

export const articleBodyTemplate = ({_user, publication, siteName}) => {
    const affiliations = {}
    let affCounter = 0
    let counter = 0
    const authorsOutputs = []
    publication.authors.forEach(author => {
        let output = ""
        if (author.firstname || author.lastname) {
            output += `<span id="authors-${counter++}" class="person">`
            const nameParts = []
            if (author.firstname) {
                nameParts.push(
                    `<span class="firstname">${escapeText(
                        author.firstname
                    )}</span>`
                )
            }
            if (author.lastname) {
                nameParts.push(
                    `<span class="lastname">${escapeText(
                        author.lastname
                    )}</span>`
                )
            }
            if (nameParts.length) {
                output += `<span class="name">${nameParts.join(" ")}</span>`
            }
            if (author.institution) {
                let affNumber
                if (affiliations[author.institution]) {
                    affNumber = affiliations[author.institution]
                } else {
                    affNumber = ++affCounter
                    affiliations[author.institution] = affNumber
                }
                output += `<a class="affiliation" href="#aff-${affNumber}">${affNumber}</a>`
            }
            output += "</span>"
        } else if (author.institution) {
            // There is an affiliation but no first/last name. We take this
            // as a group collaboration.
            output += `<span id="authors-${counter++}" class="group">`
            output += `<span class="name">${escapeText(
                author.institution
            )}</span>`
            output += "</span>"
        }
        authorsOutputs.push(output)
    })
    const authors = authorsOutputs.join(", ")
    return `<link rel="stylesheet" href="${staticUrl("css/website.css")}">
        <nav class="header">
            <a href="/">${escapeText(siteName)}</a>
            <span>${escapeText(publication.title)}</span>
            ${
                publication.can_edit
                    ? `<a href="/document/${publication.doc_id}/">${gettext(
                          "Edit"
                      )}</a>`
                    : ""
            }
        </nav>
        <div class="articles">
            <div class="keywords">${publication.keywords
                .map(
                    keyword =>
                        `<div class="keyword">${escapeText(keyword)}</div>`
                )
                .join("")}</div>
            <h3 class="article-updated">${publication.updated.slice(0, 10)}</h3>
            <h1 class="article-title">${escapeText(publication.title)}</h1>
            <div class="article-part article-contributors article-authors">${authors}</div>
            ${
                Object.keys(affiliations).length
                    ? `<div id="affiliations">${Object.entries(affiliations)
                          .map(
                              ([name, id]) =>
                                  `<aside class="affiliation" id="aff-${id}"><label>${id}</label> <div>${escapeText(
                                      name
                                  )}</div></aside>`
                          )
                          .join("")}</div>`
                    : ""
            }
            ${publication.content}
        </div>`
}

export const overviewContentTemplate = ({
    keywords,
    authors,
    publications,
    filters
}) =>
    `<div class="filters">
        <div class="filter">
            <h3 class="filter-title">${gettext("Keywords")}</h3>
            <div class="keywords">
                ${keywords
                    .map(
                        (keyword, index) =>
                            `<span class="keyword${
                                filters.keyword === keyword ? " selected" : ""
                            }" data-index="${index}">${escapeText(
                                keyword
                            )}</span>`
                    )
                    .join("")}
            </div>
        </div>
        <div class="filter">
            <h3 class="filter-title">${gettext("Authors")}</h3>
            <div class="authors">
                ${authors
                    .map(
                        (author, index) =>
                            `<span class="author${
                                filters.author === author ? " selected" : ""
                            }" data-index="${index}">${escapeText(
                                author
                            )}</span>`
                    )
                    .join("")}
            </div>
        </div>
    </div>
    <div class="articles">${publications
        .map(publication => publicationOverviewTemplate(publication))
        .join("")}</div>`

export const overviewBodyTemplate = ({
    user,
    siteName,
    publications,
    authors,
    keywords,
    filters
}) => `
    <link rel="stylesheet" href="${staticUrl("css/website.css")}">
    <div class="headers">
        ${
            user.is_authenticated
                ? `<nav class="header"><a href="/documents/">${gettext(
                      "Fidus Writer"
                  )}</a></nav>`
                : ""
        }
        <h1 class="site-name">${escapeText(siteName)}</h1>
    </div>
    <div class="content">
        ${overviewContentTemplate({keywords, authors, publications, filters})}
    </div>
    `
