import logging

from fastapi import APIRouter, HTTPException

from ..db import schemas
from ..db.crud import CRUD

from ..utils.utils import log_formatter, stream_handler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

router = APIRouter()


@router.post("/users/register")
async def create_user(user: schemas.UserRegisterBody):
    try:
        logger.debug(f"Received request to create user {user.username}, {user.email}")

        # Check if user exists. if yes, return error message
        user_db = CRUD().get_user_by_email(user.email)
        logger.debug(f"User by email: {user_db}")
        if user_db:
            logger.error(f"Email {user.email} already registered")
            return HTTPException(
                status_code=409, detail=f"Email {user.email} already registered."
            )

        user_db = CRUD.get_user_by_username(user.username)
        logger.debug(f"User by username: {user_db}")
        if user_db:
            logger.error(f"Username {user.username} already registered")
            return HTTPException(
                status_code=409, detail=f"Username {user.username} already registered."
            )

        # create
        logger.debug("Creating user")
        new_user = schemas.UserCreate(
            username=user.username, email=user.email, password=user.password
        )
        create_user = CRUD.create_user(new_user)
        logger.debug(f"User created: {create_user}")
        if create_user:
            logger.debug(f"User created successfully: {create_user}")
            return HTTPException(status_code=201, detail="User created successfully.")
        logger.error("Failed to create user")
        return HTTPException(status_code=500, detail="Failed to create user")

    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}")
        return HTTPException(status_code=500, detail=str(e))
