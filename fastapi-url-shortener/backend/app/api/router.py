from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.db import get_db
from app.cruds import shortener as cruds
from app.schemas import shortener as schemas

router = APIRouter()


@router.post("/shorten", response_model=schemas.ShortenResponse)
def shorten_url(
    data: schemas.ShortenRequest = Body(...),
    db: Session = Depends(get_db)
):

    if cruds.find_by_from_name(db, data.from_name):
        raise HTTPException(409, "from_name は既に使用されています")

    result = cruds.create_short_url(
        db=db,
        from_name=data.from_name,
        to_url=data.to_url
    )

    return result



@router.get("/u/{name}")
def redirect(name: str, db: Session = Depends(get_db)):

    to_url = cruds.increment_count_and_get_url(db, name)

    if to_url is None:
        raise HTTPException(404, "URL が見つかりません")

    return RedirectResponse(url=to_url)