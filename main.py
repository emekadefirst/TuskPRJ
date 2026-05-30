#import fastAPI Class
from fastapi import FastAPI

# import uvicorn

import uvicorn

# import the tortoise config
from src.database import TORTOISE_ORM

# import tortose-fastapi config library
from tortoise.contrib.fastapi import register_tortoise

# Import Defined Routes
from src.api import pump_info_router, impeller_router, base_plate_router, base_plate_router, options_router, test_documentation_router, pump_config_router

#make an instance of fastapi that will be used throughout the project
app = FastAPI(
    title="TUSK API"
)


app.include_router(pump_info_router)
app.include_router(impeller_router)
app.include_router(base_plate_router)
app.include_router(options_router)
app.include_router(test_documentation_router)
app.include_router(pump_config_router)
# -------------------------------------------------
# DATABASE (TORTOISE ORM)
# -------------------------------------------------

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=False,   # IMPORTANT: no runtime schema creation
    add_exception_handlers=True,
)


@app.get("/")
async def health():
    return {
        "message": "Up and running"
    }
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
