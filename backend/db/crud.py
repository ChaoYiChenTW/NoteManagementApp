import logging

from ..utils.utils import log_formatter, stream_handler
from . import models, schemas
from .database import SessionLocal

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


class CRUD:
    db = SessionLocal()

    @classmethod
    def create_user(cls, user: schemas.UserCreate):
        # Create a new user
        db_user = models.User(
            username=user.username, email=user.email, password_hash=user.password
        )
        cls.db.add(db_user)
        cls.db.commit()
        cls.db.refresh(db_user)

        # Assign the user the default role
        defalut_role = (
            cls.db.query(models.Role).filter_by(role_name="Regular User").all()
        )

        db_user.roles = defalut_role

        cls.db.commit()

        return db_user

    @classmethod
    def get_user_by_email(cls, email: str):
        return cls.db.query(models.User).filter_by(email=email).first()

    @classmethod
    def get_user_by_username(cls, username: str):
        return cls.db.query(models.User).filter_by(username=username).first()
