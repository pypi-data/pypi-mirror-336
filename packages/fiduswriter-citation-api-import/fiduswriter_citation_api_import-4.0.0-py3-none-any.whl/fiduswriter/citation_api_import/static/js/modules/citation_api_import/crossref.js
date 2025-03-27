import {searchApiResultCrossrefTemplate} from "./templates"

export class CrossrefSearcher {
    constructor(importer) {
        this.importer = importer
        this.id = "crossref"
        this.name = "Crossref"
    }

    bind() {
        document
            .querySelectorAll("#bibimport-search-result-crossref .api-import")
            .forEach(resultEl => {
                const doi = resultEl.dataset.doi
                resultEl.addEventListener("click", () => this.getBibtex(doi))
            })
    }

    lookup(searchTerm) {
        return fetch(
            `/api/citation_api_import/proxy/https://api.crossref.org/v1/works?query.bibliographic=${encodeURIComponent(escape(searchTerm))}&rows=5&select=DOI,ISBN,title,author,published,abstract`,
            {
                method: "GET"
            }
        )
            .then(response => response.json())
            .then(json => {
                const searchEl = document.getElementById(
                    "bibimport-search-result-crossref"
                )
                if (!searchEl) {
                    // window was closed before result was ready.
                    return
                }
                if (json.status !== "ok" || !json.message.items) {
                    searchEl.innerHTML = ""
                } else {
                    searchEl.innerHTML = searchApiResultCrossrefTemplate({
                        items: json.message.items
                    })
                }
                this.bind()
            })
    }

    getBibtex(doi) {
        this.importer.dialog.close()
        fetch(
            `/api/citation_api_import/proxy/https://api.crossref.org/v1/works/${encodeURIComponent(doi)}/transform`,
            {
                method: "GET",
                headers: {
                    Accept: "application/x-bibtex"
                }
            }
        )
            .then(response => response.text())
            .then(bibtex => this.importer.importBibtex(bibtex))
    }
}
