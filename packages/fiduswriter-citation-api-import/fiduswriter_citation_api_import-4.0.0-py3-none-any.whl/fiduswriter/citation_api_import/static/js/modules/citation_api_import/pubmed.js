import {get} from "../common"
import {searchApiResultPubmedTemplate} from "./templates"

// Function to replace accented characters with non-accented equivalents
const stripAccents = str => {
    const accents = {
        À: "A",
        Á: "A",
        Â: "A",
        Ã: "A",
        Ä: "A",
        Å: "A",
        Ç: "C",
        È: "E",
        É: "E",
        Ê: "E",
        Ë: "E",
        Ì: "I",
        Í: "I",
        Î: "I",
        Ï: "I",
        Ñ: "N",
        Ò: "O",
        Ó: "O",
        Ô: "O",
        Õ: "O",
        Ö: "O",
        Ù: "U",
        Ú: "U",
        Û: "U",
        Ü: "U",
        à: "a",
        á: "a",
        â: "a",
        ã: "a",
        ä: "a",
        å: "a",
        ç: "c",
        è: "e",
        é: "e",
        ê: "e",
        ë: "e",
        ì: "i",
        í: "i",
        î: "i",
        ï: "i",
        ñ: "n",
        ò: "o",
        ó: "o",
        ô: "o",
        õ: "o",
        ö: "o",
        ß: "ss",
        ù: "u",
        ú: "u",
        û: "u",
        ü: "u",
        ý: "y"
    }
    return str.replace(/[^\x00-\x7F]/g, c => accents[c] || "")
}

export class PubmedSearcher {
    constructor(importer) {
        this.importer = importer
        this.id = "pubmed"
        this.name = "Pubmed"
    }

    bind() {
        document
            .querySelectorAll("#bibimport-search-result-pubmed .api-import")
            .forEach(resultEl => {
                const pmid = resultEl.dataset.pmid
                resultEl.addEventListener("click", () => this.getBibtex(pmid))
            })
    }

    lookup(searchTerm) {
        const esearchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${encodeURIComponent(searchTerm)}&retmode=json&retmax=5`
        return get(`/api/citation_api_import/proxy/${esearchUrl}`)
            .then(response => response.json())
            .then(esearchData => {
                const pmids = esearchData.esearchresult?.idlist || []
                if (!pmids.length) {
                    const searchEl = document.getElementById(
                        "bibimport-search-result-pubmed"
                    )
                    if (searchEl) {
                        searchEl.innerHTML = ""
                    }
                    return
                }
                const efetchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${pmids.join(",")}&retmode=xml`
                return get(`/api/citation_api_import/proxy/${efetchUrl}`)
            })
            .then(response => response?.text())
            .then(xml => {
                if (!xml) {
                    return
                }
                const parser = new DOMParser()
                const doc = parser.parseFromString(xml, "text/xml")
                const articles = Array.from(
                    doc.querySelectorAll("PubmedArticle")
                )
                const items = articles
                    .map(article => {
                        const pmidEl = article.querySelector("PMID")
                        const pmid = pmidEl?.textContent || ""
                        const authors = Array.from(
                            article.querySelectorAll("Author")
                        )
                            .map(author => {
                                const lastName =
                                    author.querySelector("LastName")
                                        ?.textContent || ""
                                const initials =
                                    author.querySelector("Initials")
                                        ?.textContent || ""
                                const collectiveName =
                                    author.querySelector("CollectiveName")
                                        ?.textContent || ""
                                if (collectiveName) {
                                    return stripAccents(collectiveName)
                                }
                                if (lastName && initials) {
                                    return stripAccents(
                                        `${lastName} ${initials}`
                                    )
                                }
                                return ""
                            })
                            .filter(name => name)
                        const authorText = authors.join(", ")
                        const titleEl = article.querySelector("ArticleTitle")
                        const title = titleEl
                            ? stripAccents(
                                  titleEl.textContent.replace(/\.$/, "")
                              )
                            : ""
                        const journalEl = article.querySelector("Journal")
                        const isoAbbrev =
                            journalEl?.querySelector("ISOAbbreviation")
                                ?.textContent || ""
                        const journalTitle =
                            isoAbbrev ||
                            journalEl?.querySelector("Title")?.textContent ||
                            ""
                        const pubDateEl = journalEl?.querySelector("PubDate")
                        const yearEl = pubDateEl?.querySelector("Year")
                        const year =
                            yearEl?.textContent ||
                            pubDateEl?.textContent?.match(/\d{4}/)?.[0] ||
                            ""
                        return {
                            pmid,
                            authors: authorText,
                            published: year,
                            title,
                            journalTitle
                        }
                    })
                    .filter(item => item.pmid)
                const searchEl = document.getElementById(
                    "bibimport-search-result-pubmed"
                )
                if (!searchEl) {
                    return
                }
                searchEl.innerHTML = items.length
                    ? searchApiResultPubmedTemplate({items})
                    : ""
                this.bind()
            })
            .catch(error => {
                console.error("PubMed search error:", error)
                const searchEl = document.getElementById(
                    "bibimport-search-result-pubmed"
                )
                if (searchEl) {
                    searchEl.innerHTML = ""
                }
            })
    }

    getBibtex(pmid) {
        this.importer.dialog.close()
        const efetchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${pmid}&retmode=xml`
        get(`/api/citation_api_import/proxy/${efetchUrl}`)
            .then(response => response.text())
            .then(xml => {
                const parser = new DOMParser()
                const doc = parser.parseFromString(xml, "text/xml")
                const article = doc.querySelector("PubmedArticle")
                if (!article) {
                    throw new Error("No article found")
                }

                const pmidEl = article.querySelector("PMID")
                const pmid = pmidEl?.textContent || ""
                const authors = Array.from(article.querySelectorAll("Author"))
                    .map(author => {
                        const lastName =
                            author.querySelector("LastName")?.textContent || ""
                        const initials =
                            author.querySelector("Initials")?.textContent || ""
                        const collectiveName =
                            author.querySelector("CollectiveName")
                                ?.textContent || ""
                        if (collectiveName) {
                            return stripAccents(collectiveName)
                        }
                        if (lastName && initials) {
                            return `${stripAccents(lastName)}, ${stripAccents(initials)}`
                        }
                        return null
                    })
                    .filter(author => author)
                const authorStr = authors.join(" and ")
                const titleEl = article.querySelector("ArticleTitle")
                const title = titleEl
                    ? stripAccents(titleEl.textContent.replace(/\.$/, ""))
                    : ""
                const journalEl = article.querySelector("Journal")
                const isoAbbrev =
                    journalEl?.querySelector("ISOAbbreviation")?.textContent ||
                    ""
                const journalTitle =
                    isoAbbrev ||
                    journalEl?.querySelector("Title")?.textContent ||
                    ""
                const pubDateEl = journalEl?.querySelector("PubDate")
                const year =
                    pubDateEl?.querySelector("Year")?.textContent ||
                    pubDateEl?.textContent?.match(/\d{4}/)?.[0] ||
                    ""
                const volume =
                    article.querySelector("Volume")?.textContent || ""
                const issue = article.querySelector("Issue")?.textContent || ""
                const pages =
                    article.querySelector("MedlinePgn")?.textContent || ""

                let formattedPages = pages
                if (pages.includes("-")) {
                    const [start, end] = pages.split("-")
                    if (end.length < start.length) {
                        const commonPart = start.slice(
                            0,
                            start.length - end.length
                        )
                        formattedPages = `${start}--${commonPart}${end}`
                    } else {
                        formattedPages = `${start}--${end}`
                    }
                }

                let bibtex = `@article{pmid${pmid},\n`
                bibtex += `  author = {${authorStr}},\n`
                bibtex += `  title = {${title}},\n`
                bibtex += `  journal = {${stripAccents(journalTitle)}},\n`
                bibtex += `  year = {${year}}`
                if (volume) {
                    bibtex += `,\n  volume = {${volume}}`
                }
                if (issue) {
                    bibtex += `,\n  number = {${issue}}`
                }
                if (formattedPages) {
                    bibtex += `,\n  pages = {${formattedPages}}`
                }
                bibtex += "\n}"

                return this.importer.importBibtex(bibtex)
            })
            .catch(error => console.error("Error fetching BibTeX:", error))
    }
}
