from tortoise import Tortoise
from .config import settings

# handles database connection setup and tear down with Tortoise ORM, along with session handling for transactions

async def get_db() -> Generator:
    """
    Creates a new database session for a connection and handles closing the connection.
    This function should be used as a dependency in FastAPI routes.
    """
    try:
        db = Tortoise.get_connection("default")
        yield db  # Provide the database session to the route handling the request
    finally:
        await Tortoise.close_connections()

async def init_db() -> None:
    """
    Initializes the database connection and creates tables based on Tortoise ORM models.
    This function should be called when the application starts up.
    """
    # url = "sqlite://db.sqlite3"
    await Tortoise.init(
        db_url=settings.database_url,
        modules={'models': ['app.db.models']}  # Link to Tortoise ORM models
    )
    await Tortoise.generate_schemas()

async def close_db() -> None:
    """
    Closes the database connection.
    This function should be called when the application shuts down.
    """
    await Tortoise.close_connections()

