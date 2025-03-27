from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()  #* Correct way to define a declarative base

class DatabaseManager:
    class Base(Base):  #* Inheriting from declarative_base
        __abstract__ = True  #* Ensures this class is not treated as a table itself

        @declared_attr
        def __tablename__(cls) -> str:
            """Automatically generates table names based on class name."""
            return cls.__name__.lower()

    #* Explicitly define the type of metadata
    metadata:MetaData = Base.metadata

    @staticmethod
    def initialize(engine: Engine):
        """Creates the database tables if they do not exist."""
        DatabaseManager.metadata.create_all(engine)
