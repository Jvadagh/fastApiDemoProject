# demo_service.py
from sqlalchemy.orm import Session

from Demo.api.schema.demo_schema import DemoCreationCommand
from Demo.db.models.items_model import ItemModel
from Demo.db.repository.base import create_entity


class DemoService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_demo(self, command: DemoCreationCommand) -> ItemModel:
        return create_entity(self.session, ItemModel(
            name=command.name,
            phone_number=command.phone_number,
            company=command.company,
            email=command.email
        ))
