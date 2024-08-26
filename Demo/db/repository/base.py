# base.py
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from Demo.db.models.items_model import Base


def create_entity(session: Session, entity: Base):
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity


def get_entity_by_id(session: Session, entity_id: int):
    pass


def get_entity_by_filter(session: Session, entity: Base, filters: list):
    query = session.query(entity)
    for filter_condition in filters:
        query = query.filter(filter_condition)  # Use filter() instead of where()

    entity = query.first()  # Fetch the first result

    if not entity:
        raise NoResultFound("No entity found matching the filters.")

    return entity
