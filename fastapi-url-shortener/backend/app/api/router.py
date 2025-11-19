from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import RedirectResponse

from app.schemas import shortener as schema
from app.cruds import shortener as cruds


router = APIRouter()


@router.post("/shorten", response_model=schema.ShortenResponse)
def shorten_url(data: schema.ShortenRequest = Body(...)):
    if cruds.find_by_from_name(data.from_name):
        raise HTTPException(409, "from_name は既に使用されています")

    result = cruds.create_short_url(data.from_name, data.to_url)
    return result


@router.get("/u/{name}")
def redirect(name: str):
    url = cruds.increment_count_and_get_url(name)

    if url is None:
        raise HTTPException(404, "URL が見つかりません")

    return RedirectResponse(url=url)


# LINE_FRIEND_URL = "https://line.me/ti/p/pV1jTdnh2C"

# @router.get("/u/line")
# def redirect_to_line():
#     return RedirectResponse(url=LINE_FRIEND_URL, status_code=307)