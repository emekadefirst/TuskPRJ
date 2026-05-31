#import fastAPI Class
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

# import uvicorn

import uvicorn

# import the tortoise config
from src.database import TORTOISE_ORM

# add COR Middleware
from fastapi.middleware.cors import CORSMiddleware

# import tortose-fastapi config library
from tortoise.contrib.fastapi import register_tortoise

# Import Defined Routes
from src.api import pump_info_router, impeller_router, base_plate_router, base_plate_router, options_router, test_documentation_router, pump_config_router, order_router
from src.auth_router import auth_router, users_router

#make an instance of fastapi that will be used throughout the project
app = FastAPI(
    title="TUSK API"
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(pump_info_router)
app.include_router(impeller_router)
app.include_router(base_plate_router)
app.include_router(options_router)
app.include_router(test_documentation_router)
app.include_router(pump_config_router)
app.include_router(order_router)
# -------------------------------------------------
# DATABASE (TORTOISE ORM)
# -------------------------------------------------

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=False,   # IMPORTANT: no runtime schema creation
    add_exception_handlers=True,
)
app.add_middleware(
    CORSMiddleware,
    # Explicit origins (kept for clarity). Use "null" so the dashboard works
    # when opened directly from disk via file:// (browsers send Origin: null).
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5500",
        "null",
    ],
    # Match any localhost / 127.0.0.1 port so any static server works in dev.
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"message": "Up and running"}


# ---------------------------------------------------------------------------
# Serve the frontend HTML files from the project root
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent


@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(ROOT_DIR / "index.html")


@app.get("/dashboard", include_in_schema=False)
@app.get("/dashboard.html", include_in_schema=False)
async def serve_dashboard():
    return FileResponse(ROOT_DIR / "dashboard.html")
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
