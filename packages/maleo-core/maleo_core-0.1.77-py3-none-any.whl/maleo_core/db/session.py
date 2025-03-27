import warnings
from contextlib import contextmanager
from logging import Logger
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, Optional, Any

class SessionManager:
    _logger:Optional[Logger] = None
    _SessionLocal:Optional[sessionmaker[Session]] = None

    @classmethod
    def initialize(cls, logger:Logger, engine:Engine) -> None:
        """Initialize the sessionmaker if not already initialized."""
        if cls._SessionLocal is None:
            cls._logger = logger
            cls._SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
            cls._logger.info("SessionManager initialized successfully.")

    @classmethod
    def get(cls) -> Generator[Session, Any, None]:
        """Returns a generator that yields a SQLAlchemy session. This session should be used for all database interactions within the current request context."""
        if cls._logger is None:
            raise RuntimeError("Logger has not been initialized. Call initialize(engine, logger) first.")
        if cls._SessionLocal is None:
            raise RuntimeError("SessionLocal has not been initialized. Call initialize(engine, logger) first.")

        session = cls._SessionLocal()
        cls._logger.debug("New database session created.")
        try:
            yield session  #* Provide session
            session.commit()  #* Auto-commit on success
        except Exception as e:
            session.rollback()  #* Rollback on error
            cls._logger.error(f"Manual database transaction failed: {e}", exc_info=True)
        finally:
            session.close()
            cls._logger.debug("Database session closed.")

    @classmethod
    @contextmanager
    def create(cls) -> Generator[Session, None, None]:
        """
        Context manager for manual session handling.
        Automatically logs session creation, errors, and closing.
        Supports `with SessionManager.create() as session:`
        """
        if cls._logger is None:
            raise RuntimeError("Logger has not been initialized. Call initialize(engine, logger) first.")
        if cls._SessionLocal is None:
            raise RuntimeError("SessionLocal has not been initialized. Call initialize(engine, logger) first.")

        session = cls._SessionLocal()
        cls._logger.debug("New manual database session created.")
        try:
            yield session  #* Provide session
            session.commit()  #* Auto-commit on success
        except Exception as e:
            session.rollback()  #* Rollback on error
            cls._logger.error(f"Manual database transaction failed: {e}", exc_info=True)
        finally:
            session.close()  #* Ensure session closes
            cls._logger.debug("Database session closed.")

    @classmethod
    def dispose(cls) -> None:
        """Dispose of the sessionmaker and release any resources."""
        if cls._SessionLocal is not None:
            cls._SessionLocal.close_all()
            cls._SessionLocal = None
            if cls._logger is None:
                warnings.warn("Logger has not been initialized. SessionLocal will be disposed without being logged.", RuntimeWarning)
            else:
                cls._logger.info("SessionManager disposed successfully.")
        cls._logger = None