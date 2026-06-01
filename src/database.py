from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://tuskdb.sqlite3"
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],  # access db schemas defined by tortoise
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Africa/Lagos"
}