# demo_router.py
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from Demo.api.factory import demo_service_factory
from Demo.api.schema.demo_schema import DemoViewModel, DemoCreationCommand
from Demo.auth import get_current_user
from Demo.db.models.items_model import ItemModel
from Demo.db.services.demo_service import DemoService

demo_router = APIRouter()


@demo_router.post(
    "/counseling/",
    response_model=DemoViewModel,
    status_code=HTTPStatus.CREATED,
)
def create_demo(
        command: DemoCreationCommand,
        demo_service: Annotated[DemoService, Depends(demo_service_factory)],
        user: dict = Depends(get_current_user)
) -> ItemModel:
    try:
        return demo_service.create_demo(command)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Error")


