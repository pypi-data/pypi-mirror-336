from sqlalchemy import Engine
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy.orm.decl_api import DeclarativeMeta
from typing import Type

class DatabaseManager:
    @as_declarative()
    class Base(metaclass=DeclarativeMeta): #* Explicitly define the metaclass
        id:int
        __name__:str

        #* Automatically generate table names if not provided
        @declared_attr
        def __tablename__(cls) -> str:
            """Automatically generates table names based on class name."""
            return cls.__name__.lower()

    #* Explicitly define the type of metadata
    metadata: Type[Base] = Base.metadata

    @staticmethod
    def initialize(engine:Engine):
        """Creates the database tables if they do not exist."""
        DatabaseManager.Base.metadata.create_all(engine)