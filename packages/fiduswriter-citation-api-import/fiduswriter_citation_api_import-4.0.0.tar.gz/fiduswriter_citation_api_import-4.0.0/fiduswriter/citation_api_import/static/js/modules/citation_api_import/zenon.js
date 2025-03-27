import {get} from "../common"
import {searchApiResultZenonTemplate} from "./templates"

// Function to clean names
const cleanName = name => {
    // Remove dates (e.g., "1943-", "1856-1938")
    let cleanedName = name.replace(/,?\s*\d{4}(-\d{0,4})?/g, "")

    // Remove trailing commas and periods unless it's an abbreviation
    cleanedName = cleanedName.replace(/([^A-Za-z])[.,]+$/, "$1")

    return cleanedName.trim() // Trim any extra spaces
}

export class ZenonSearcher {
    constructor(importer) {
        this.importer = importer
        this.id = "zenon"
        this.name = "Zenon"
    }

    bind() {
        document
            .querySelectorAll("#bibimport-search-result-zenon .api-import")
            .forEach(resultEl => {
                const id = resultEl.dataset.id
                resultEl.addEventListener("click", () => this.getBibtex(id))
            })
    }

    lookup(searchTerm) {
        return get(
            "/api/citation_api_import/proxy/https://zenon.dainst.org/Search/Results",
            {lookfor: escape(searchTerm), type: "AllFields", submit: "Find"}
        )
            .then(response => response.text())
            .then(html => {
                const doc = new DOMParser().parseFromString(html, "text/html")
                const items = Array.from(doc.querySelectorAll("div.result"))
                    .map(el => {
                        if (el.textContent.length === 0) {
                            return false
                        }
                        const id = el.querySelector("input.hiddenId").value

                        const title = el.querySelector("a.title").textContent
                        const authors = Array.from(el.querySelectorAll("a"))
                            .filter(a => a.href.includes("/Author/"))
                            .map(a => a.textContent)
                            .map(name => cleanName(name))

                        const publicationInfo =
                            el.querySelector(".col-sm-8.middle").textContent
                        const yearMatch = publicationInfo.match(/\b\d{4}\b/)
                        let published = "Unknown"
                        if (yearMatch) {
                            published = yearMatch[0]
                        } else {
                        }
                        return {
                            id,
                            authors,
                            published,
                            title
                        }
                    })
                    .filter(item => item)
                const searchEl = document.getElementById(
                    "bibimport-search-result-zenon"
                )
                if (!searchEl) {
                    // window was closed before result was ready.
                    return
                }
                if (items.length) {
                    searchEl.innerHTML = searchApiResultZenonTemplate({items})
                } else {
                    searchEl.innerHTML = ""
                }
                this.bind()
            })
    }

    getBibtex(id) {
        this.importer.dialog.close()
        get(
            `/api/citation_api_import/proxy/https://zenon.dainst.org/Record/${id}/Export`,
            {
                style: "BibTeX"
            }
        )
            .then(response => response.text())
            .then(bibtex => this.importer.importBibtex(bibtex))
    }
}
