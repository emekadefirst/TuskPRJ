from src.env import (
    DB_HOST,
    DB_DATABASE,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
)
from tortoise import Tortoise
from urllib.parse import quote_plus




TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": DB_HOST,
                "port": DB_PORT,
                "user": DB_USER,
                "password": DB_PASSWORD,
                "database": DB_DATABASE,
                "timeout": 8, # time out for inactivity or time to drop connection
            },
        }
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"], # access db schemas defined by torstoise
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Africa/Lagos",        
    "minsize": 1, # minimum number of connections
    "maxsize": 5,  # maximum number of connections
    # "timeout": 10,         
    "max_queries": 500,  # maximum number of db query
}

