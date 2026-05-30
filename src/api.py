"""
FastAPI routers for all pump configuration repositories.

Each router maps one-to-one with a repository class and is tagged
with the repository class name so Swagger groups them cleanly.

Routes per resource:
    GET    /                -> fetch   (query-param filtered list)
    GET    /lookup          -> get_or_none (key-field single lookup)
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

import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from src.repository import (
    BasePlateRepository,
    ImpellerRepository,
    OptionsRepository,
    PumpConfigRepository,
    PumpInfoRepository,
    TestDocumentationRepository,
)


# ===========================================================================
# Shared helpers
# ===========================================================================

def _not_found(resource: str, id: uuid.UUID) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id '{id}' was not found.",
    )


def _record_to_dict(record: Any) -> Dict[str, Any]:
    """Serialize a Tortoise model instance to a plain dict."""
    return {
        col: getattr(record, col)
        for col in record._meta.fields_map
        if not record._meta.fields_map[col].generated  # exclude reverse relations
        and hasattr(record, col)
    }


# ===========================================================================
# ── PumpInfo ──────────────────────────────────────────────────────────────
# ===========================================================================

class PumpInfoUpdate(BaseModel):
    series: Optional[str] = None
    size: Optional[str] = None
    pump_material: Optional[str] = None
    shaft_configuration: Optional[str] = None
    casing_metal: Optional[str] = None
    casing_drain: Optional[str] = None
    casing_tap: Optional[str] = None
    flange_configuration: Optional[str] = None
    spot_facing: Optional[str] = None
    casing_wear_ring: Optional[str] = None
    tack_weld_wear_ring: Optional[str] = None
    casing_mounting: Optional[str] = None
    hardware: Optional[str] = None
    seal_chamber_config: Optional[str] = None
    shipping_gasket: Optional[str] = None
    cradle_material: Optional[str] = None


pump_info_router = APIRouter(
    prefix="/pump-info",
    tags=["PumpInfoRepository"],
)


@pump_info_router.get("/", summary="Fetch pump info records")
async def fetch_pump_info(
    id: Optional[uuid.UUID] = Query(None),
    series: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    pump_material: Optional[str] = Query(None),
    shaft_configuration: Optional[str] = Query(None),
    casing_metal: Optional[str] = Query(None),
    casing_drain: Optional[str] = Query(None),
    casing_tap: Optional[str] = Query(None),
    flange_configuration: Optional[str] = Query(None),
    spot_facing: Optional[str] = Query(None),
    casing_wear_ring: Optional[str] = Query(None),
    tack_weld_wear_ring: Optional[str] = Query(None),
    casing_mounting: Optional[str] = Query(None),
    hardware: Optional[str] = Query(None),
    seal_chamber_config: Optional[str] = Query(None),
    shipping_gasket: Optional[str] = Query(None),
    cradle_material: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    records = await PumpInfoRepository.fetch(
        id=id,
        series=series,
        size=size,
        pump_material=pump_material,
        shaft_configuration=shaft_configuration,
        casing_metal=casing_metal,
        casing_drain=casing_drain,
        casing_tap=casing_tap,
        flange_configuration=flange_configuration,
        spot_facing=spot_facing,
        casing_wear_ring=casing_wear_ring,
        tack_weld_wear_ring=tack_weld_wear_ring,
        casing_mounting=casing_mounting,
        hardware=hardware,
        seal_chamber_config=seal_chamber_config,
        shipping_gasket=shipping_gasket,
        cradle_material=cradle_material,
    )
    return [_record_to_dict(r) for r in records]


@pump_info_router.get("/lookup", summary="Look up a single pump info record")
async def get_or_none_pump_info(
    id: Optional[uuid.UUID] = Query(None),
    series: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    pump_material: Optional[str] = Query(None),
) -> Optional[Dict[str, Any]]:
    record = await PumpInfoRepository.get_or_none(
        id=id, series=series, size=size, pump_material=pump_material
    )
    return _record_to_dict(record) if record else None


@pump_info_router.patch("/{id}", summary="Update a pump info record")
async def update_pump_info(id: uuid.UUID, body: PumpInfoUpdate) -> Dict[str, Any]:
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    record = await PumpInfoRepository.update(id, **payload)
    if record is None:
        raise _not_found("PumpInfo", id)
    return _record_to_dict(record)


@pump_info_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a pump info record")
async def delete_pump_info(id: uuid.UUID) -> None:
    deleted = await PumpInfoRepository.delete(id)
    if not deleted:
        raise _not_found("PumpInfo", id)


# ===========================================================================
# ── Impeller ──────────────────────────────────────────────────────────────
# ===========================================================================

class ImpellerUpdate(BaseModel):
    impeller_range: Optional[str] = None
    impeller_trim: Optional[str] = None
    impeller_balance: Optional[str] = None
    impeller_material: Optional[str] = None
    impeller_wear_ring_material: Optional[str] = None


impeller_router = APIRouter(
    prefix="/impellers",
    tags=["ImpellerRepository"],
)


@impeller_router.get("/", summary="Fetch impeller records")
async def fetch_impellers(
    id: Optional[uuid.UUID] = Query(None),
    impeller_range: Optional[str] = Query(None),
    impeller_trim: Optional[str] = Query(None),
    impeller_balance: Optional[str] = Query(None),
    impeller_material: Optional[str] = Query(None),
    impeller_wear_ring_material: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    records = await ImpellerRepository.fetch(
        id=id,
        impeller_range=impeller_range,
        impeller_trim=impeller_trim,
        impeller_balance=impeller_balance,
        impeller_material=impeller_material,
        impeller_wear_ring_material=impeller_wear_ring_material,
    )
    return [_record_to_dict(r) for r in records]


@impeller_router.get("/lookup", summary="Look up a single impeller record")
async def get_or_none_impeller(
    id: Optional[uuid.UUID] = Query(None),
    impeller_range: Optional[str] = Query(None),
    impeller_material: Optional[str] = Query(None),
) -> Optional[Dict[str, Any]]:
    record = await ImpellerRepository.get_or_none(
        id=id, impeller_range=impeller_range, impeller_material=impeller_material
    )
    return _record_to_dict(record) if record else None


@impeller_router.patch("/{id}", summary="Update an impeller record")
async def update_impeller(id: uuid.UUID, body: ImpellerUpdate) -> Dict[str, Any]:
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    record = await ImpellerRepository.update(id, **payload)
    if record is None:
        raise _not_found("Impeller", id)
    return _record_to_dict(record)


@impeller_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an impeller record")
async def delete_impeller(id: uuid.UUID) -> None:
    deleted = await ImpellerRepository.delete(id)
    if not deleted:
        raise _not_found("Impeller", id)


# ===========================================================================
# ── BasePlate ─────────────────────────────────────────────────────────────
# ===========================================================================

class BasePlateUpdate(BaseModel):
    baseplate_type: Optional[str] = None
    baseplate_material: Optional[str] = None
    drip_pan: Optional[str] = None
    allignment_lugs: Optional[str] = None
    lifting_lugs: Optional[str] = None
    leveling_screws: Optional[str] = None
    grounding_lugs: Optional[str] = None
    grout_hole: Optional[str] = None
    isolation_pads: Optional[str] = None
    stilts: Optional[str] = None


base_plate_router = APIRouter(
    prefix="/base-plates",
    tags=["BasePlateRepository"],
)


@base_plate_router.get("/", summary="Fetch base plate records")
async def fetch_base_plates(
    id: Optional[uuid.UUID] = Query(None),
    baseplate_type: Optional[str] = Query(None),
    baseplate_material: Optional[str] = Query(None),
    drip_pan: Optional[str] = Query(None),
    allignment_lugs: Optional[str] = Query(None),
    lifting_lugs: Optional[str] = Query(None),
    leveling_screws: Optional[str] = Query(None),
    grounding_lugs: Optional[str] = Query(None),
    grout_hole: Optional[str] = Query(None),
    isolation_pads: Optional[str] = Query(None),
    stilts: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    records = await BasePlateRepository.fetch(
        id=id,
        baseplate_type=baseplate_type,
        baseplate_material=baseplate_material,
        drip_pan=drip_pan,
        allignment_lugs=allignment_lugs,
        lifting_lugs=lifting_lugs,
        leveling_screws=leveling_screws,
        grounding_lugs=grounding_lugs,
        grout_hole=grout_hole,
        isolation_pads=isolation_pads,
        stilts=stilts,
    )
    return [_record_to_dict(r) for r in records]


@base_plate_router.get("/lookup", summary="Look up a single base plate record")
async def get_or_none_base_plate(
    id: Optional[uuid.UUID] = Query(None),
    baseplate_type: Optional[str] = Query(None),
    baseplate_material: Optional[str] = Query(None),
) -> Optional[Dict[str, Any]]:
    record = await BasePlateRepository.get_or_none(
        id=id, baseplate_type=baseplate_type, baseplate_material=baseplate_material
    )
    return _record_to_dict(record) if record else None


@base_plate_router.patch("/{id}", summary="Update a base plate record")
async def update_base_plate(id: uuid.UUID, body: BasePlateUpdate) -> Dict[str, Any]:
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    record = await BasePlateRepository.update(id, **payload)
    if record is None:
        raise _not_found("BasePlate", id)
    return _record_to_dict(record)


@base_plate_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a base plate record")
async def delete_base_plate(id: uuid.UUID) -> None:
    deleted = await BasePlateRepository.delete(id)
    if not deleted:
        raise _not_found("BasePlate", id)


# ===========================================================================
# ── Options ───────────────────────────────────────────────────────────────
# ===========================================================================

class OptionsUpdate(BaseModel):
    coupling_type: Optional[str] = None
    coupling_guard: Optional[str] = None
    auxillary_nameplate: Optional[str] = None
    crating: Optional[str] = None
    oil_options: Optional[str] = None
    bearing_frame_cooling: Optional[str] = None
    lubrication_options: Optional[str] = None
    oil_seat: Optional[str] = None
    sight_gauge: Optional[str] = None
    magnetic_drain: Optional[str] = None
    expansion_chamber: Optional[str] = None


options_router = APIRouter(
    prefix="/options",
    tags=["OptionsRepository"],
)


@options_router.get("/", summary="Fetch options records")
async def fetch_options(
    id: Optional[uuid.UUID] = Query(None),
    coupling_type: Optional[str] = Query(None),
    coupling_guard: Optional[str] = Query(None),
    auxillary_nameplate: Optional[str] = Query(None),
    crating: Optional[str] = Query(None),
    oil_options: Optional[str] = Query(None),
    bearing_frame_cooling: Optional[str] = Query(None),
    lubrication_options: Optional[str] = Query(None),
    oil_seat: Optional[str] = Query(None),
    sight_gauge: Optional[str] = Query(None),
    magnetic_drain: Optional[str] = Query(None),
    expansion_chamber: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    records = await OptionsRepository.fetch(
        id=id,
        coupling_type=coupling_type,
        coupling_guard=coupling_guard,
        auxillary_nameplate=auxillary_nameplate,
        crating=crating,
        oil_options=oil_options,
        bearing_frame_cooling=bearing_frame_cooling,
        lubrication_options=lubrication_options,
        oil_seat=oil_seat,
        sight_gauge=sight_gauge,
        magnetic_drain=magnetic_drain,
        expansion_chamber=expansion_chamber,
    )
    return [_record_to_dict(r) for r in records]


@options_router.get("/lookup", summary="Look up a single options record")
async def get_or_none_options(
    id: Optional[uuid.UUID] = Query(None),
    coupling_type: Optional[str] = Query(None),
    oil_options: Optional[str] = Query(None),
    lubrication_options: Optional[str] = Query(None),
) -> Optional[Dict[str, Any]]:
    record = await OptionsRepository.get_or_none(
        id=id,
        coupling_type=coupling_type,
        oil_options=oil_options,
        lubrication_options=lubrication_options,
    )
    return _record_to_dict(record) if record else None


@options_router.patch("/{id}", summary="Update an options record")
async def update_options(id: uuid.UUID, body: OptionsUpdate) -> Dict[str, Any]:
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    record = await OptionsRepository.update(id, **payload)
    if record is None:
        raise _not_found("Options", id)
    return _record_to_dict(record)


@options_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an options record")
async def delete_options(id: uuid.UUID) -> None:
    deleted = await OptionsRepository.delete(id)
    if not deleted:
        raise _not_found("Options", id)


# ===========================================================================
# ── TestDocumentation ─────────────────────────────────────────────────────
# ===========================================================================

class TestDocumentationUpdate(BaseModel):
    performance_testing: Optional[str] = None
    hydro_testing: Optional[str] = None
    vibration: Optional[str] = None
    sound_level: Optional[str] = None
    general_inspection: Optional[str] = None
    documenttation_1: Optional[str] = None
    documenttation_2: Optional[str] = None
    documenttation_3: Optional[str] = None
    documenttation_4: Optional[str] = None
    documenttation_5: Optional[str] = None
    documenttation_6: Optional[str] = None


test_documentation_router = APIRouter(
    prefix="/test-documentation",
    tags=["TestDocumentationRepository"],
)


@test_documentation_router.get("/", summary="Fetch test documentation records")
async def fetch_test_documentation(
    id: Optional[uuid.UUID] = Query(None),
    performance_testing: Optional[str] = Query(None),
    hydro_testing: Optional[str] = Query(None),
    vibration: Optional[str] = Query(None),
    sound_level: Optional[str] = Query(None),
    general_inspection: Optional[str] = Query(None),
    documenttation_1: Optional[str] = Query(None),
    documenttation_2: Optional[str] = Query(None),
    documenttation_3: Optional[str] = Query(None),
    documenttation_4: Optional[str] = Query(None),
    documenttation_5: Optional[str] = Query(None),
    documenttation_6: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    records = await TestDocumentationRepository.fetch(
        id=id,
        performance_testing=performance_testing,
        hydro_testing=hydro_testing,
        vibration=vibration,
        sound_level=sound_level,
        general_inspection=general_inspection,
        documenttation_1=documenttation_1,
        documenttation_2=documenttation_2,
        documenttation_3=documenttation_3,
        documenttation_4=documenttation_4,
        documenttation_5=documenttation_5,
        documenttation_6=documenttation_6,
    )
    return [_record_to_dict(r) for r in records]


@test_documentation_router.get("/lookup", summary="Look up a single test documentation record")
async def get_or_none_test_documentation(
    id: Optional[uuid.UUID] = Query(None),
    performance_testing: Optional[str] = Query(None),
    hydro_testing: Optional[str] = Query(None),
    general_inspection: Optional[str] = Query(None),
) -> Optional[Dict[str, Any]]:
    record = await TestDocumentationRepository.get_or_none(
        id=id,
        performance_testing=performance_testing,
        hydro_testing=hydro_testing,
        general_inspection=general_inspection,
    )
    return _record_to_dict(record) if record else None


@test_documentation_router.patch("/{id}", summary="Update a test documentation record")
async def update_test_documentation(id: uuid.UUID, body: TestDocumentationUpdate) -> Dict[str, Any]:
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    record = await TestDocumentationRepository.update(id, **payload)
    if record is None:
        raise _not_found("TestDocumentation", id)
    return _record_to_dict(record)


@test_documentation_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a test documentation record")
async def delete_test_documentation(id: uuid.UUID) -> None:
    deleted = await TestDocumentationRepository.delete(id)
    if not deleted:
        raise _not_found("TestDocumentation", id)


# ===========================================================================
# ── PumpConfig ────────────────────────────────────────────────────────────
# ===========================================================================

class PumpConfigUpdate(BaseModel):
    pump_info_id: Optional[uuid.UUID] = None
    impeller_id: Optional[uuid.UUID] = None
    base_plate_id: Optional[uuid.UUID] = None
    options_id: Optional[uuid.UUID] = None
    test_documentation_id: Optional[uuid.UUID] = None


pump_config_router = APIRouter(
    prefix="/pump-configs",
    tags=["PumpConfigRepository"],
)


@pump_config_router.get("/", summary="Fetch pump config records")
async def fetch_pump_configs(
    id: Optional[uuid.UUID] = Query(None),
    pump_info_id: Optional[uuid.UUID] = Query(None),
    impeller_id: Optional[uuid.UUID] = Query(None),
    base_plate_id: Optional[uuid.UUID] = Query(None),
    options_id: Optional[uuid.UUID] = Query(None),
    test_documentation_id: Optional[uuid.UUID] = Query(None),
) -> List[Dict[str, Any]]:
    records = await PumpConfigRepository.fetch(
        id=id,
        pump_info_id=pump_info_id,
        impeller_id=impeller_id,
        base_plate_id=base_plate_id,
        options_id=options_id,
        test_documentation_id=test_documentation_id,
    )
    return [_record_to_dict(r) for r in records]


@pump_config_router.get("/lookup", summary="Look up a single pump config record")
async def get_or_none_pump_config(
    id: Optional[uuid.UUID] = Query(None),
    pump_info_id: Optional[uuid.UUID] = Query(None),
    impeller_id: Optional[uuid.UUID] = Query(None),
) -> Optional[Dict[str, Any]]:
    record = await PumpConfigRepository.get_or_none(
        id=id, pump_info_id=pump_info_id, impeller_id=impeller_id
    )
    return _record_to_dict(record) if record else None


@pump_config_router.patch("/{id}", summary="Update a pump config record")
async def update_pump_config(id: uuid.UUID, body: PumpConfigUpdate) -> Dict[str, Any]:
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    record = await PumpConfigRepository.update(id, **payload)
    if record is None:
        raise _not_found("PumpConfig", id)
    return _record_to_dict(record)


@pump_config_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a pump config record")
async def delete_pump_config(id: uuid.UUID) -> None:
    deleted = await PumpConfigRepository.delete(id)
    if not deleted:
        raise _not_found("PumpConfig", id)