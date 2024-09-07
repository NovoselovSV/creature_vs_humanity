from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .shortcuts import get_object_or_404
from SQL_db.database import get_db
from data.general_data import ErrorMessageSchema
from data.region import RegionSchema
from service.regions import get_region, get_regions

router = APIRouter(prefix='/regions')


@router.get('/', response_model=list[RegionSchema])
def regions(db: Session = Depends(get_db)):
    return get_regions(db)


@router.get('/{region_id}',
            response_model=RegionSchema,
            responses={status.HTTP_404_NOT_FOUND:
                       {'model': ErrorMessageSchema,
                        'description': 'Item not found'}})
def region(region_id: int, db: Session = Depends(get_db)):
    return get_object_or_404(get_region, db, region_id)
