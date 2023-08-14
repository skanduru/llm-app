from fastapi import FastAPI
from starlette.middleware.exceptions import ServerErrorMiddleware
from typing import Optional
from tortoise.contrib.fastapi import register_tortoise

from config import Settings  # Importing configuration settings
from core.logger import logger  # Importing application-wide logger
from db.session import init_db, close_db  # Importing database session functions
from ai.chat_agents import init_chat_agents  # Importing AI agents initialization function
from routers import recommendations, ratings, movies  # Importing routers
from middlewares import exception_handler_middleware  # Importing exception middleware

# This file will be responsible for setting up the FastAPI application, initializing database and AI agents, including routers, and adding middleware.


app = FastAPI()  # Initializing FastAPI application

app.middleware("http")(exception_handler_middleware)

@app.on_event("startup")
async def startup_event():
    """
    This function will be called when the application starts.
    It's responsible for setting up the database and AI chat agents and
    any other application settings
    """
    logger.info("Starting up...")
    await init_db()  # Initializing database
    await init_chat_agents()  # Initializing AI chat agents

@app.on_event("shutdown")
async def shutdown_event():
    """
    This function will be called when the application shuts down.
    It's responsible for closing the database session.
    """
    logger.info("Shutting down...")
    await close_db()  # Closing database session

# Adding middleware for centralized exception handling
app.add_middleware(ServerErrorMiddleware, handler=ExceptionMiddleware.http_exception_handler)

# Including routers
app.include_router(recommendations.router)
app.include_router(ratings.router)
app.include_router(movies.router)

# Registering Tortoise ORM models
register_tortoise(
    app,
    db_url=Settings.database_url,
    modules={"models": ["db.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
