from sqlalchemy.orm import Session
from app.models.shortener import Url



def find_by_from_name(db: Session, from_name: str):
    return db.query(Url).filter(Url.from_name == from_name).first()



def create_short_url(db: Session, from_name: str, to_url: str):
    url = Url(
        from_name=from_name,
        to_url=to_url
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url



def increment_count_and_get_url(db: Session, from_name: str):
    url = db.query(Url).filter(Url.from_name == from_name).first()

    if not url:
        return None

    url.count += 1
    db.commit()

    return url.to_url