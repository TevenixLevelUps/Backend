from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import get_current_admin, get_current_user
from app.database import db_helper
from app.models.user import User

from . import service
from .shema import CreateService, ServiceRespon

router = APIRouter(tags=["service"])


@router.post(
    "/services/", response_model=ServiceRespon, status_code=status.HTTP_201_CREATED
)
async def create_service(
    name: str,
    description: str,
    price: float,
    execution_time: str,
    image: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    admin: User = Depends(get_current_admin),
):

    image_bytes = await image.read()

    service_data = CreateService(
        name=name,
        description=description,
        price=price,
        execution_time=execution_time,
        image=image_bytes,
    )

    return await service.create_service(session=session, service_data=service_data)


@router.get("/services/{service_id}", response_model=ServiceRespon)
async def get_service(
    service_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(get_current_user),
):
    return await service.get_service_by_id(session=session, service_id=service_id)


@router.get("/services/", response_model=list[ServiceRespon])
async def get_all_services(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(get_current_user),
):
    return await service.get_all_services(session=session)


@router.put("/services/{service_id}", response_model=ServiceRespon)
async def update_service(
    service_id: int,
    name: str,
    description: str,
    price: float,
    execution_time: str,
    image: UploadFile = File(None),  # Поле может быть пустым
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    admin: User = Depends(get_current_admin),
):

    image_bytes = await (image.read() if image else None)

    service_data = CreateService(
        name=name,
        description=description,
        price=price,
        execution_time=execution_time,
        image=image_bytes,
    )

    return await service.update_service(
        session=session, service_id=service_id, service_data=service_data
    )


@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    admin: User = Depends(get_current_admin),
):
    await service.delete_service(session=session, service_id=service_id)
