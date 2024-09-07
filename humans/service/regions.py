from random import sample

from sqlalchemy.orm import Session

from data.region import Region


def get_regions(db: Session) -> list[Region]:
    return db.query(Region).all()


def get_region(db: Session, region_id: int) -> Region:
    return db.query(Region).filter(Region.id == region_id).first()


def get_random_region(db: Session) -> Region:
    return sample(get_regions(db))
