from httpx import AsyncClient
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.conf import settings

ALLOWED_DOMAINS = {
    "search.gesis.org": True,
    "api.datacite.org": True,
    "api.crossref.org": True,
    "zenon.dainst.org": True,
    "eutils.ncbi.nlm.nih.gov": True,
}

PUBMED_API_KEY = getattr(settings, "PUBMED_API_KEY", False)


@login_required
@require_GET
async def proxy(request, url):
    domain = url.split("/")[2]
    if domain not in ALLOWED_DOMAINS:
        return HttpResponseForbidden()
    query_string = request.META["QUERY_STRING"]
    if domain == "api.crossref.org":
        mailto = f"mailto={settings.CONTACT_EMAIL}"
        if len(query_string):
            query_string += "&" + mailto
        else:
            query_string = mailto
    elif domain == "eutils.ncbi.nlm.nih.gov" and PUBMED_API_KEY:
        if len(query_string):
            query_string += f"&api_key={PUBMED_API_KEY}"
        else:
            query_string = f"api_key={PUBMED_API_KEY}"
    if len(query_string):
        url = f"{url}?{query_string}"
    async with AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "User-Agent": request.META.get(
                    "HTTP_USER_AGENT", "Fidus Writer"
                ),
                "Referer": request.META.get("HTTP_REFERER", ""),
                "Accept": request.META.get("HTTP_ACCEPT", "application/json"),
            },
            timeout=88,  # Firefox times out after 90 seconds, so we need to return before that.
        )
    return HttpResponse(response.text, status=response.status_code)
