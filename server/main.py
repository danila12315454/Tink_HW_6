"""
hello_server.py
---------------

This module provides a basic HTTP server that responds to incoming requests
with a "Hello, World!" message.

"""
import logging.config
from typing import Any

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import app_settings
from db.users import UsersRepo
from .contracts import Message, User

app = FastAPI()

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": app_settings.log_level,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": app_settings.log_level,
    },
}

logging.config.dictConfig(logging_config)

engine = create_engine(app_settings.db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


@app.get("/")
async def root() -> Message:
    return Message(message="Hello that")


@app.get("/hello/{name}")
async def say_hello(name: str) -> Message:
    return Message(message=f"Hello {name}")


@app.get("/safe/users/{user_id}", response_model=User)
async def read_safe_user(user_id: str) -> Any:
    with SessionLocal() as session:
        user = UsersRepo(session).get_user(user_id)

    if user:
        return user

    raise HTTPException(status_code=404, detail="User not found")
