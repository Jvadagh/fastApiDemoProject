# factory.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from Demo.db.db import get_db
from Demo.db.services.demo_service import DemoService


def demo_service_factory(session: Annotated[Session, Depends(get_db)]) -> DemoService:
    return DemoService(session)
