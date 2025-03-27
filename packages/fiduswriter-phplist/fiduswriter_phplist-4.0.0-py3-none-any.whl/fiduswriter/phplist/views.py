import re
from httpx import AsyncClient, HTTPError
from urllib.parse import urlencode, urljoin

from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.conf import settings

from allauth.account.models import EmailAddress


@require_POST
async def subscribe_email(request):
    if (
        not hasattr(settings, "PHPLIST_BASE_URL")
        or not settings.PHPLIST_BASE_URL
    ):
        return HttpResponse()
    url = urljoin(settings.PHPLIST_BASE_URL, "/admin/")
    login_data = {
        "cmd": "login",
        "login": settings.PHPLIST_LOGIN,
        "password": settings.PHPLIST_PASSWORD,
    }
    if hasattr(settings, "PHPLIST_SECRET"):
        login_data["secret"] = settings.PHPLIST_SECRET
    try:
        async with AsyncClient() as client:
            response = await client.post(
                url,
                params={"page": "importsimple"},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                content=urlencode(login_data),
            )
            response.raise_for_status()
    except HTTPError:
        return HttpResponse(status=500)
    # <input type="hidden" name="formtoken" value="1f...114" />
    session_cookie = response.headers["Set-Cookie"]
    formtoken_match = re.search(
        r'<input.*?name=["\']formtoken["\'].*?value=["\'](.*?)["\']',
        response.content.decode("utf-8"),
    )
    if not formtoken_match:
        return HttpResponse(status=404)
    formtoken = formtoken_match.group(1)
    email = request.POST["email"]
    email_object = await EmailAddress.objects.filter(email=email).afirst()
    if not email_object:
        return HttpResponse(status=500)
    data = {
        "formtoken": formtoken,
        "importcontent": email,
        "importlists[unselect]": -1,
        f"importlists[{settings.PHPLIST_LIST_ID}]": settings.PHPLIST_LIST_ID,
        "confirm": 1,
        "checkvalidity": 1,
        "doimport": "Import subscribers",
    }
    if hasattr(settings, "PHPLIST_SECRET"):
        data["secret"] = settings.PHPLIST_SECRET
    async with AsyncClient() as client:
        response = await client.post(
            url,
            params={"page": "importsimple"},
            headers={
                "Cookie": session_cookie,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            content=urlencode(data),
        )
        response.raise_for_status()
    return HttpResponse(status=201)
