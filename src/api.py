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
    SealRepo, MotorRepo,
)
from src.schemas import (
    BasePlateSchema, BasePlateUpdateSchema,
    ImpellerSchema, ImpellerUpdateSchema,
    OptionSchema, OptionUpdateSchema,
    PumpConfigSchema, PumpConfigUpdateSchema,
    PumpInfoSchema, PumpInfoUpdateSchema,
    TestDocumentationSchema, TestDocumentationUpdateSchema,
    SealSchema, SealUpdateSchema,
    MotorSchema, MotorUpdateSchema,
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
# Seal
# ---------------------------------------------------------------------------

seal_router = APIRouter(prefix="/seal", tags=["Seal"])


@seal_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_seal(dto: SealSchema):
    return await SealRepo.create(dto)


@seal_router.get("/")
async def fetch_seals(search: Optional[str] = Query(default=None)):
    return await SealRepo.fetch(search=search)


@seal_router.get("/{id}")
async def fetch_seal(id: str):
    data = await SealRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Seal not found")
    return data


@seal_router.patch("/{id}")
async def update_seal(id: str, dto: SealUpdateSchema):
    data = await SealRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Seal not found")
    return data


@seal_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seal(id: str):
    return await SealRepo.delete(id=id)


# ---------------------------------------------------------------------------
# Motor
# ---------------------------------------------------------------------------

motor_router = APIRouter(prefix="/motor", tags=["Motor"])


@motor_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_motor(dto: MotorSchema):
    return await MotorRepo.create(dto)


@motor_router.get("/")
async def fetch_motors(search: Optional[str] = Query(default=None)):
    return await MotorRepo.fetch(search=search)


@motor_router.get("/{id}")
async def fetch_motor(id: str):
    data = await MotorRepo.fetch(id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Motor not found")
    return data


@motor_router.patch("/{id}")
async def update_motor(id: str, dto: MotorUpdateSchema):
    data = await MotorRepo.update(id=id, data=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Motor not found")
    return data


@motor_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_motor(id: str):
    return await MotorRepo.delete(id=id)


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
async def fetch_pump_configs(
    catalog: Optional[bool] = Query(default=None, description="Filter by catalog configs (true) or custom (false)"),
    search: Optional[str] = Query(default=None),
):
    return await PumpConfigRepo.fetch(catalog=catalog, search=search)


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



# ---------------------------------------------------------------------------
# Orders (auth-protected; users only see their own orders)
# ---------------------------------------------------------------------------
from fastapi import Depends

from src.auth import get_current_user
from src.models import User
from src.repo import OrderRepo
from src.schemas import OrderSchema, OrderUpdateSchema


order_router = APIRouter(prefix="/orders", tags=["Order"])


@order_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    dto: OrderSchema,
    user: User = Depends(get_current_user),
):
    return await OrderRepo.create(user=user, dto=dto)


@order_router.get("/")
async def list_orders(
    user: User = Depends(get_current_user),
    search: Optional[str] = Query(default=None),
):
    return await OrderRepo.fetch(user=user, search=search)


@order_router.get("/{id}")
async def fetch_order(id: str, user: User = Depends(get_current_user)):
    data = await OrderRepo.fetch(user=user, id=id)
    if not data:
        raise HTTPException(status_code=404, detail="Order not found")
    return data


@order_router.patch("/{id}")
async def update_order(
    id: str,
    dto: OrderUpdateSchema,
    user: User = Depends(get_current_user),
):
    data = await OrderRepo.update(user=user, id=id, dto=dto)
    if not data:
        raise HTTPException(status_code=404, detail="Order not found")
    return data


@order_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: str, user: User = Depends(get_current_user)):
    return await OrderRepo.delete(user=user, id=id)


# ---------------------------------------------------------------------------
# Pricing / Quote
# ---------------------------------------------------------------------------
from src.repo import PricingRepo
from src.schemas import (
    PriceListSchema,
    OptionPriceSchema,
    QuoteRequestSchema,
    QuoteResponseSchema,
)


pricing_router = APIRouter(prefix="/pricing", tags=["Pricing"])


@pricing_router.get("/base-prices")
async def list_base_prices():
    return await PricingRepo.list_base_prices()


@pricing_router.post("/base-prices", status_code=status.HTTP_201_CREATED)
async def upsert_base_price(dto: PriceListSchema):
    return await PricingRepo.upsert_base_price(dto)


@pricing_router.get("/option-prices")
async def list_option_prices():
    return await PricingRepo.list_option_prices()


@pricing_router.post("/option-prices", status_code=status.HTTP_201_CREATED)
async def upsert_option_price(dto: OptionPriceSchema):
    return await PricingRepo.upsert_option_price(dto)


@pricing_router.post("/quote", response_model=QuoteResponseSchema)
async def calculate_quote(dto: QuoteRequestSchema):
    return await PricingRepo.quote(dto)
