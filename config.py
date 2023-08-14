from pydantic_settings import BaseSettings

"""
# This file will use the Pydantic's BaseSettings class for environment variables handling
# We'll set up the basic configuration settings here which can be easily expanded in the future
"""

class Settings(BaseSettings):
    """
    Configuration settings from environment variables.
    """

    # FastAPI settings
    project_name: str = "AutoRecAI"
    debug: bool = True

    # Database settings
    database_url: str = "sqlite://:memory:"  # In-memory SQLite for simplicity
    database_url: str = "sqlite://autorec_db.db"  # 

    # Chat agent settings
    lang_model: str = "gpt-3-turbo"
    chat_model: str = "davinci-codex"
    
    # Logging options
    LOG_LEVEL: str = logging.INFO
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Other necessary configurations can be added here later.

    class Config:
        """
        Pydantic configuration.
        """
        env_file = ".env"  # Name of the file to read environment variables from
        env_file_encoding = "utf-8"  # Encoding to use when reading the .env file
        case_sensitive = True  # If False, all keys read from environment will be converted to lowercase


settings = Settings()  # Creating an instance of settings

