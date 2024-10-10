from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .shortcuts import aget_object_or_404
from SQL_db.database import get_db
from data.general_data import ErrorMessageSchema
from data.region_schemas import RegionSchema
from service.regions import get_region, get_regions

router = APIRouter(prefix='/regions')


@router.get('/', response_model=list[RegionSchema])
async def regions(db: AsyncSession = Depends(get_db)):
    return await get_regions(db)


@router.get('/{region_id}',
            response_model=RegionSchema,
            responses={status.HTTP_404_NOT_FOUND:
                       {'model': ErrorMessageSchema,
                        'description': 'Item not found'}})
async def region(region_id: int, db: AsyncSession = Depends(get_db)):
    return await aget_object_or_404(get_region, db, region_id)
