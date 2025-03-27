FidusWriter-Citation-API-import
=====

FidusWriter-Citation-API-import is a Fidus Writer plugin to allow for import of
citations from external sources via API.

Currently these citation sources are supported: Crossref, Datacite and GESIS Search.


Installation
-----------

1. Install Fidus Writer if you haven't done so already.

2. Within the virtual environment install Fidus Writer with the citation-api-import option::

    pip install fiduswriter[citation-api-import]

3. Add "citation-api-import" to your INSTALLED_APPS setting in the
   configuration.py file like this::

    INSTALLED_APPS += (
        ...
        'citation_api_import',
    )

4. Run `fiduswriter setup` to create the needed JavaScript files.

5. (Re)start your Fidus Writer server


API Keys
--------

In order to improve results and to avoid rate limiting, you can provide ab API key for Pubmed.

You can do this by adding the following lines to your configuration.py file::

```python
PUBMED_API_KEY = 'your_pubmed_api_key'
```

You can obtain an API key by registering for an NCBI account and generating a key from the [NCBI API Key Management](https://www.ncbi.nlm.nih.gov/account/settings/) page.

If no API key is provided, the plugin will still work but may be subject to stricter rate limits.

Credits
-----------

This plugin was originally developed by the `Opening Scholarly Communications in the Social Sciences (OSCOSS) <http://www.gesis.org/?id=10714>`_ project, financed by the German Research Foundation (DFG) and executed by the University of Bonn and GESIS - Leibniz Institute for the Social Sciences.

Original Developer: `Niloofar Azizi <https://github.com/NiloofarAzizi>`_
