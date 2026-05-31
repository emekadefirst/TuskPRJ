"""
FastAPI routers for all pump configuration repositories.

Each router maps one-to-one with a repository class and is tagged
with the repository class name so Swagger groups them cleanly.

Routes per resource:
    POST   /                -> create  (new record)
    GET    /                -> fetch   (query-param filtered list)
    GET    /{id}            -> fetch   (single record by id)
    PATCH  /{id}            -> update  (partial field update)
    DELETE /{id}            -> delete  (hard delete)

Mount all routers in main.py:
    from routes import (
        pump_info_router, impeller_router, base_plate_router,
        options_router, test_documentation_router, pump_config_router,
    )
    app.include_router(pump_info_router)
    app.include_router(impeller_router)
    app.include_router(base_plate_router)
    app.include_router(options_router)
    app.include_router(test_documentation_router)
    app.include_router(pump_config_router)
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from src.repo import (
    BasePlateRepo, ImpellerRepo, OptionsRepo,
    PumpConfigRepo, PumpInfoRepo, TestDocumentationRepo,
)
from src.schemas import (
    BasePlateSchema, BasePlateUpdateSchema,
    ImpellerSchema, ImpellerUpdateSchema,
    OptionSchema, OptionUpdateSchema,
    PumpConfigSchema, PumpConfigUpdateSchema,
    PumpInfoSchema, PumpInfoUpdateSchema,
    TestDocumentationSchema, TestDocumentationUpdateSchema,
)


# ---------------------------------------------------------------------------
# PumpInfo
# ---------------------------------------------------------------------------

pump_info_router = APIRouter(prefix="/pump-info", tags=["PumpInfo"])


@pump_info_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pump_info(dto: PumpInfoSchema):
    return await PumpInfoRepo.create(dto)


@pump_info_router.get("/")
async def fetch_pump_infos(search: Optional[str] = Query(default=None)):
    return await PumpInfoRepo.fetch(search=search)


@pump_info_router.get("/{id}")
async def fetch_pump_info(id: str):
    data = await PumpInfoRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Pump info not found")
    return data


@pump_info_router.patch("/{id}")
async def update_pump_info(id: str, dto: PumpInfoUpdateSchema):
    data = await PumpInfoRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Pump info not found")
    return data


@pump_info_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pump_info(id: str):
    return await PumpInfoRepo.delete(id=id)


# ---------------------------------------------------------------------------
# Impeller
# ---------------------------------------------------------------------------

impeller_router = APIRouter(prefix="/impeller", tags=["Impeller"])


@impeller_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_impeller(dto: ImpellerSchema):
    return await ImpellerRepo.create(dto)


@impeller_router.get("/")
async def fetch_impellers(search: Optional[str] = Query(default=None)):
    return await ImpellerRepo.fetch(search=search)


@impeller_router.get("/{id}")
async def fetch_impeller(id: str):
    data = await ImpellerRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Impeller not found")
    return data


@impeller_router.patch("/{id}")
async def update_impeller(id: str, dto: ImpellerUpdateSchema):
    data = await ImpellerRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Impeller not found")
    return data


@impeller_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_impeller(id: str):
    return await ImpellerRepo.delete(id=id)


# ---------------------------------------------------------------------------
# BasePlate
# ---------------------------------------------------------------------------

base_plate_router = APIRouter(prefix="/base-plate", tags=["BasePlate"])


@base_plate_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_base_plate(dto: BasePlateSchema):
    return await BasePlateRepo.create(dto)


@base_plate_router.get("/")
async def fetch_base_plates(search: Optional[str] = Query(default=None)):
    return await BasePlateRepo.fetch(search=search)


@base_plate_router.get("/{id}")
async def fetch_base_plate(id: str):
    data = await BasePlateRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Base plate not found")
    return data


@base_plate_router.patch("/{id}")
async def update_base_plate(id: str, dto: BasePlateUpdateSchema):
    data = await BasePlateRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Base plate not found")
    return data


@base_plate_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_base_plate(id: str):
    return await BasePlateRepo.delete(id=id)


# ---------------------------------------------------------------------------
# Options
# ---------------------------------------------------------------------------

options_router = APIRouter(prefix="/options", tags=["Options"])


@options_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_option(dto: OptionSchema):
    return await OptionsRepo.create(dto)


@options_router.get("/")
async def fetch_options(search: Optional[str] = Query(default=None)):
    return await OptionsRepo.fetch(search=search)


@options_router.get("/{id}")
async def fetch_option(id: str):
    data = await OptionsRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Option not found")
    return data


@options_router.patch("/{id}")
async def update_option(id: str, dto: OptionUpdateSchema):
    data = await OptionsRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Option not found")
    return data


@options_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_option(id: str):
    return await OptionsRepo.delete(id=id)


# ---------------------------------------------------------------------------
# TestDocumentation
# ---------------------------------------------------------------------------

test_documentation_router = APIRouter(prefix="/test-documentation", tags=["TestDocumentation"])


@test_documentation_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_test_documentation(dto: TestDocumentationSchema):
    return await TestDocumentationRepo.create(dto)


@test_documentation_router.get("/")
async def fetch_test_documentations(search: Optional[str] = Query(default=None)):
    return await TestDocumentationRepo.fetch(search=search)


@test_documentation_router.get("/{id}")
async def fetch_test_documentation(id: str):
    data = await TestDocumentationRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Test documentation not found")
    return data


@test_documentation_router.patch("/{id}")
async def update_test_documentation(id: str, dto: TestDocumentationUpdateSchema):
    data = await TestDocumentationRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Test documentation not found")
    return data


@test_documentation_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_documentation(id: str):
    return await TestDocumentationRepo.delete(id=id)


# ---------------------------------------------------------------------------
# PumpConfig
# ---------------------------------------------------------------------------

pump_config_router = APIRouter(prefix="/pump-config", tags=["PumpConfig"])


@pump_config_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pump_config(dto: PumpConfigSchema):
    return await PumpConfigRepo.create(dto)


@pump_config_router.get("/")
async def fetch_pump_configs():
    return await PumpConfigRepo.fetch()


@pump_config_router.get("/{id}")
async def fetch_pump_config(id: str):
    data = await PumpConfigRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Pump config not found")
    return data


@pump_config_router.patch("/{id}")
async def update_pump_config(id: str, dto: PumpConfigUpdateSchema):
    data = await PumpConfigRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Pump config not found")
    return data


@pump_config_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pump_config(id: str):
    return await PumpConfigRepo.delete(id=id)