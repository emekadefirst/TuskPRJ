"""
Repository layer for all pump configuration Tortoise ORM models.

Each repository exposes four async methods:
    - fetch       : filtered list query (supports id + model-specific fields)
    - get_or_none : single record lookup, returns None when not found
    - update      : partial update by id, returns the refreshed instance or None
    - delete      : hard delete by id, returns True on success, False when not found

Usage example:
    pump = await PumpInfoRepository.get_or_none(id="<uuid>")
    results = await PumpInfoRepository.fetch(series="HV", size="4x6")
    updated = await PumpInfoRepository.update("<uuid>", hardware="Carbon Steel")
    deleted = await PumpInfoRepository.delete("<uuid>")
"""

from __future__ import annotations

import uuid
from typing import Any, List, Optionalfrom src.models import BasePlate, Impeller, Options, PumpConfig, PumpInfo, TestDocumentation


# ---------------------------------------------------------------------------
# PumpInfo Repository
# ---------------------------------------------------------------------------

class PumpInfoRepository:
    """CRUD repository for PumpInfo records."""

    @staticmethod
    async def create(**kwargs: Any) -> PumpInfo:
        """Create a new PumpInfo record from the supplied fields."""
        return await PumpInfo.create(**kwargs)

    @staticmethod
    async def fetch(
        id: Optional[uuid.UUID] = None,
        series: Optional[str] = None,
        size: Optional[str] = None,
        pump_material: Optional[str] = None,
        shaft_configuration: Optional[str] = None,
        casing_metal: Optional[str] = None,
        casing_drain: Optional[str] = None,
        casing_tap: Optional[str] = None,
        flange_configuration: Optional[str] = None,
        spot_facing: Optional[str] = None,
        casing_wear_ring: Optional[str] = None,
        tack_weld_wear_ring: Optional[str] = None,
        casing_mounting: Optional[str] = None,
        hardware: Optional[str] = None,
        seal_chamber_config: Optional[str] = None,
        shipping_gasket: Optional[str] = None,
        cradle_material: Optional[str] = None,
    ) -> List[PumpInfo]:
        """Return all PumpInfo rows matching the supplied (non-None) filters."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if series is not None:
            filters["series"] = series
        if size is not None:
            filters["size"] = size
        if pump_material is not None:
            filters["pump_material"] = pump_material
        if shaft_configuration is not None:
            filters["shaft_configuration"] = shaft_configuration
        if casing_metal is not None:
            filters["casing_metal"] = casing_metal
        if casing_drain is not None:
            filters["casing_drain"] = casing_drain
        if casing_tap is not None:
            filters["casing_tap"] = casing_tap
        if flange_configuration is not None:
            filters["flange_configuration"] = flange_configuration
        if spot_facing is not None:
            filters["spot_facing"] = spot_facing
        if casing_wear_ring is not None:
            filters["casing_wear_ring"] = casing_wear_ring
        if tack_weld_wear_ring is not None:
            filters["tack_weld_wear_ring"] = tack_weld_wear_ring
        if casing_mounting is not None:
            filters["casing_mounting"] = casing_mounting
        if hardware is not None:
            filters["hardware"] = hardware
        if seal_chamber_config is not None:
            filters["seal_chamber_config"] = seal_chamber_config
        if shipping_gasket is not None:
            filters["shipping_gasket"] = shipping_gasket
        if cradle_material is not None:
            filters["cradle_material"] = cradle_material
        return await PumpInfo.filter(**filters).all()

    @staticmethod
    async def get_or_none(
        id: Optional[uuid.UUID] = None,
        series: Optional[str] = None,
        size: Optional[str] = None,
        pump_material: Optional[str] = None,
    ) -> Optional[PumpInfo]:
        """Return the first PumpInfo matching the key fields, or None."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if series is not None:
            filters["series"] = series
        if size is not None:
            filters["size"] = size
        if pump_material is not None:
            filters["pump_material"] = pump_material
        return await PumpInfo.get_or_none(**filters)

    @staticmethod
    async def update(id: uuid.UUID, **kwargs: Any) -> Optional[PumpInfo]:
        """Update any field(s) on a PumpInfo record by id. Returns the updated record or None."""
        record = await PumpInfo.get_or_none(id=id)
        if record is None:
            return None
        for field, value in kwargs.items():
            setattr(record, field, value)
        await record.save()
        return record

    @staticmethod
    async def delete(id: uuid.UUID) -> bool:
        """Delete a PumpInfo record by id. Returns True if deleted, False if not found."""
        deleted_count = await PumpInfo.filter(id=id).delete()
        return deleted_count > 0


# ---------------------------------------------------------------------------
# Impeller Repository
# ---------------------------------------------------------------------------

class ImpellerRepository:
    """CRUD repository for Impeller records."""

    @staticmethod
    async def create(**kwargs: Any) -> Impeller:
        """Create a new Impeller record from the supplied fields."""
        return await Impeller.create(**kwargs)

    @staticmethod
    async def fetch(
        id: Optional[uuid.UUID] = None,
        impeller_range: Optional[str] = None,
        impeller_trim: Optional[str] = None,
        impeller_balance: Optional[str] = None,
        impeller_material: Optional[str] = None,
        impeller_wear_ring_material: Optional[str] = None,
    ) -> List[Impeller]:
        """Return all Impeller rows matching the supplied (non-None) filters."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if impeller_range is not None:
            filters["impeller_range"] = impeller_range
        if impeller_trim is not None:
            filters["impeller_trim"] = impeller_trim
        if impeller_balance is not None:
            filters["impeller_balance"] = impeller_balance
        if impeller_material is not None:
            filters["impeller_material"] = impeller_material
        if impeller_wear_ring_material is not None:
            filters["impeller_wear_ring_material"] = impeller_wear_ring_material
        return await Impeller.filter(**filters).all()

    @staticmethod
    async def get_or_none(
        id: Optional[uuid.UUID] = None,
        impeller_range: Optional[str] = None,
        impeller_material: Optional[str] = None,
    ) -> Optional[Impeller]:
        """Return the first Impeller matching the key fields, or None."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if impeller_range is not None:
            filters["impeller_range"] = impeller_range
        if impeller_material is not None:
            filters["impeller_material"] = impeller_material
        return await Impeller.get_or_none(**filters)

    @staticmethod
    async def update(id: uuid.UUID, **kwargs: Any) -> Optional[Impeller]:
        """Update any field(s) on an Impeller record by id. Returns the updated record or None."""
        record = await Impeller.get_or_none(id=id)
        if record is None:
            return None
        for field, value in kwargs.items():
            setattr(record, field, value)
        await record.save()
        return record

    @staticmethod
    async def delete(id: uuid.UUID) -> bool:
        """Delete an Impeller record by id. Returns True if deleted, False if not found."""
        deleted_count = await Impeller.filter(id=id).delete()
        return deleted_count > 0


# ---------------------------------------------------------------------------
# BasePlate Repository
# ---------------------------------------------------------------------------

class BasePlateRepository:
    """CRUD repository for BasePlate records."""

    @staticmethod
    async def create(**kwargs: Any) -> BasePlate:
        """Create a new BasePlate record from the supplied fields."""
        return await BasePlate.create(**kwargs)

    @staticmethod
    async def fetch(
        id: Optional[uuid.UUID] = None,
        baseplate_type: Optional[str] = None,
        baseplate_material: Optional[str] = None,
        drip_pan: Optional[str] = None,
        allignment_lugs: Optional[str] = None,
        lifting_lugs: Optional[str] = None,
        leveling_screws: Optional[str] = None,
        grounding_lugs: Optional[str] = None,
        grout_hole: Optional[str] = None,
        isolation_pads: Optional[str] = None,
        stilts: Optional[str] = None,
    ) -> List[BasePlate]:
        """Return all BasePlate rows matching the supplied (non-None) filters."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if baseplate_type is not None:
            filters["baseplate_type"] = baseplate_type
        if baseplate_material is not None:
            filters["baseplate_material"] = baseplate_material
        if drip_pan is not None:
            filters["drip_pan"] = drip_pan
        if allignment_lugs is not None:
            filters["allignment_lugs"] = allignment_lugs
        if lifting_lugs is not None:
            filters["lifting_lugs"] = lifting_lugs
        if leveling_screws is not None:
            filters["leveling_screws"] = leveling_screws
        if grounding_lugs is not None:
            filters["grounding_lugs"] = grounding_lugs
        if grout_hole is not None:
            filters["grout_hole"] = grout_hole
        if isolation_pads is not None:
            filters["isolation_pads"] = isolation_pads
        if stilts is not None:
            filters["stilts"] = stilts
        return await BasePlate.filter(**filters).all()

    @staticmethod
    async def get_or_none(
        id: Optional[uuid.UUID] = None,
        baseplate_type: Optional[str] = None,
        baseplate_material: Optional[str] = None,
    ) -> Optional[BasePlate]:
        """Return the first BasePlate matching the key fields, or None."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if baseplate_type is not None:
            filters["baseplate_type"] = baseplate_type
        if baseplate_material is not None:
            filters["baseplate_material"] = baseplate_material
        return await BasePlate.get_or_none(**filters)

    @staticmethod
    async def update(id: uuid.UUID, **kwargs: Any) -> Optional[BasePlate]:
        """Update any field(s) on a BasePlate record by id. Returns the updated record or None."""
        record = await BasePlate.get_or_none(id=id)
        if record is None:
            return None
        for field, value in kwargs.items():
            setattr(record, field, value)
        await record.save()
        return record

    @staticmethod
    async def delete(id: uuid.UUID) -> bool:
        """Delete a BasePlate record by id. Returns True if deleted, False if not found."""
        deleted_count = await BasePlate.filter(id=id).delete()
        return deleted_count > 0


# ---------------------------------------------------------------------------
# Options Repository
# ---------------------------------------------------------------------------

class OptionsRepository:
    """CRUD repository for Options records."""

    @staticmethod
    async def create(**kwargs: Any) -> Options:
        """Create a new Options record from the supplied fields."""
        return await Options.create(**kwargs)

    @staticmethod
    async def fetch(
        id: Optional[uuid.UUID] = None,
        coupling_type: Optional[str] = None,
        coupling_guard: Optional[str] = None,
        auxillary_nameplate: Optional[str] = None,
        crating: Optional[str] = None,
        oil_options: Optional[str] = None,
        bearing_frame_cooling: Optional[str] = None,
        lubrication_options: Optional[str] = None,
        oil_seat: Optional[str] = None,
        sight_gauge: Optional[str] = None,
        magnetic_drain: Optional[str] = None,
        expansion_chamber: Optional[str] = None,
    ) -> List[Options]:
        """Return all Options rows matching the supplied (non-None) filters."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if coupling_type is not None:
            filters["coupling_type"] = coupling_type
        if coupling_guard is not None:
            filters["coupling_guard"] = coupling_guard
        if auxillary_nameplate is not None:
            filters["auxillary_nameplate"] = auxillary_nameplate
        if crating is not None:
            filters["crating"] = crating
        if oil_options is not None:
            filters["oil_options"] = oil_options
        if bearing_frame_cooling is not None:
            filters["bearing_frame_cooling"] = bearing_frame_cooling
        if lubrication_options is not None:
            filters["lubrication_options"] = lubrication_options
        if oil_seat is not None:
            filters["oil_seat"] = oil_seat
        if sight_gauge is not None:
            filters["sight_gauge"] = sight_gauge
        if magnetic_drain is not None:
            filters["magnetic_drain"] = magnetic_drain
        if expansion_chamber is not None:
            filters["expansion_chamber"] = expansion_chamber
        return await Options.filter(**filters).all()

    @staticmethod
    async def get_or_none(
        id: Optional[uuid.UUID] = None,
        coupling_type: Optional[str] = None,
        oil_options: Optional[str] = None,
        lubrication_options: Optional[str] = None,
    ) -> Optional[Options]:
        """Return the first Options record matching the key fields, or None."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if coupling_type is not None:
            filters["coupling_type"] = coupling_type
        if oil_options is not None:
            filters["oil_options"] = oil_options
        if lubrication_options is not None:
            filters["lubrication_options"] = lubrication_options
        return await Options.get_or_none(**filters)

    @staticmethod
    async def update(id: uuid.UUID, **kwargs: Any) -> Optional[Options]:
        """Update any field(s) on an Options record by id. Returns the updated record or None."""
        record = await Options.get_or_none(id=id)
        if record is None:
            return None
        for field, value in kwargs.items():
            setattr(record, field, value)
        await record.save()
        return record

    @staticmethod
    async def delete(id: uuid.UUID) -> bool:
        """Delete an Options record by id. Returns True if deleted, False if not found."""
        deleted_count = await Options.filter(id=id).delete()
        return deleted_count > 0


# ---------------------------------------------------------------------------
# TestDocumentation Repository
# ---------------------------------------------------------------------------

class TestDocumentationRepository:
    """CRUD repository for TestDocumentation records."""

    @staticmethod
    async def create(**kwargs: Any) -> TestDocumentation:
        """Create a new TestDocumentation record from the supplied fields."""
        return await TestDocumentation.create(**kwargs)

    @staticmethod
    async def fetch(
        id: Optional[uuid.UUID] = None,
        performance_testing: Optional[str] = None,
        hydro_testing: Optional[str] = None,
        vibration: Optional[str] = None,
        sound_level: Optional[str] = None,
        general_inspection: Optional[str] = None,
        documenttation_1: Optional[str] = None,
        documenttation_2: Optional[str] = None,
        documenttation_3: Optional[str] = None,
        documenttation_4: Optional[str] = None,
        documenttation_5: Optional[str] = None,
        documenttation_6: Optional[str] = None,
    ) -> List[TestDocumentation]:
        """Return all TestDocumentation rows matching the supplied (non-None) filters."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if performance_testing is not None:
            filters["performance_testing"] = performance_testing
        if hydro_testing is not None:
            filters["hydro_testing"] = hydro_testing
        if vibration is not None:
            filters["vibration"] = vibration
        if sound_level is not None:
            filters["sound_level"] = sound_level
        if general_inspection is not None:
            filters["general_inspection"] = general_inspection
        if documenttation_1 is not None:
            filters["documenttation_1"] = documenttation_1
        if documenttation_2 is not None:
            filters["documenttation_2"] = documenttation_2
        if documenttation_3 is not None:
            filters["documenttation_3"] = documenttation_3
        if documenttation_4 is not None:
            filters["documenttation_4"] = documenttation_4
        if documenttation_5 is not None:
            filters["documenttation_5"] = documenttation_5
        if documenttation_6 is not None:
            filters["documenttation_6"] = documenttation_6
        return await TestDocumentation.filter(**filters).all()

    @staticmethod
    async def get_or_none(
        id: Optional[uuid.UUID] = None,
        performance_testing: Optional[str] = None,
        hydro_testing: Optional[str] = None,
        general_inspection: Optional[str] = None,
    ) -> Optional[TestDocumentation]:
        """Return the first TestDocumentation matching the key fields, or None."""
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if performance_testing is not None:
            filters["performance_testing"] = performance_testing
        if hydro_testing is not None:
            filters["hydro_testing"] = hydro_testing
        if general_inspection is not None:
            filters["general_inspection"] = general_inspection
        return await TestDocumentation.get_or_none(**filters)

    @staticmethod
    async def update(id: uuid.UUID, **kwargs: Any) -> Optional[TestDocumentation]:
        """Update any field(s) on a TestDocumentation record by id. Returns the updated record or None."""
        record = await TestDocumentation.get_or_none(id=id)
        if record is None:
            return None
        for field, value in kwargs.items():
            setattr(record, field, value)
        await record.save()
        return record

    @staticmethod
    async def delete(id: uuid.UUID) -> bool:
        """Delete a TestDocumentation record by id. Returns True if deleted, False if not found."""
        deleted_count = await TestDocumentation.filter(id=id).delete()
        return deleted_count > 0


# ---------------------------------------------------------------------------
# PumpConfig Repository
# ---------------------------------------------------------------------------

class PumpConfigRepository:
    """CRUD repository for PumpConfig records (aggregate root)."""

    # Prefetch all related sub-models in every query for convenience.
    _PREFETCH = (
        "pump_info",
        "impeller",
        "base_plate",
        "options",
        "test_documentation",
    )

    @staticmethod
    async def create(
        pump_info_id: uuid.UUID,
        impeller_id: uuid.UUID,
        base_plate_id: uuid.UUID,
        options_id: uuid.UUID,
        test_documentation_id: uuid.UUID,
    ) -> PumpConfig:
        """Create a new PumpConfig record. All FK ids are required."""
        record = await PumpConfig.create(
            pump_info_id=pump_info_id,
            impeller_id=impeller_id,
            base_plate_id=base_plate_id,
            options_id=options_id,
            test_documentation_id=test_documentation_id,
        )
        await record.fetch_related(*PumpConfigRepository._PREFETCH)
        return record

    @staticmethod
    async def fetch(
        id: Optional[uuid.UUID] = None,
        pump_info_id: Optional[uuid.UUID] = None,
        impeller_id: Optional[uuid.UUID] = None,
        base_plate_id: Optional[uuid.UUID] = None,
        options_id: Optional[uuid.UUID] = None,
        test_documentation_id: Optional[uuid.UUID] = None,
    ) -> List[PumpConfig]:
        """
        Return all PumpConfig rows matching the supplied (non-None) filters.
        Results are prefetched with all related sub-models.
        """
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if pump_info_id is not None:
            filters["pump_info_id"] = pump_info_id
        if impeller_id is not None:
            filters["impeller_id"] = impeller_id
        if base_plate_id is not None:
            filters["base_plate_id"] = base_plate_id
        if options_id is not None:
            filters["options_id"] = options_id
        if test_documentation_id is not None:
            filters["test_documentation_id"] = test_documentation_id
        return (
            await PumpConfig.filter(**filters)
            .prefetch_related(*PumpConfigRepository._PREFETCH)
            .all()
        )

    @staticmethod
    async def get_or_none(
        id: Optional[uuid.UUID] = None,
        pump_info_id: Optional[uuid.UUID] = None,
        impeller_id: Optional[uuid.UUID] = None,
    ) -> Optional[PumpConfig]:
        """
        Return a single PumpConfig matching the key fields (prefetched), or None.
        """
        filters: dict[str, Any] = {}
        if id is not None:
            filters["id"] = id
        if pump_info_id is not None:
            filters["pump_info_id"] = pump_info_id
        if impeller_id is not None:
            filters["impeller_id"] = impeller_id
        return (
            await PumpConfig.filter(**filters)
            .prefetch_related(*PumpConfigRepository._PREFETCH)
            .get_or_none()
        )

    @staticmethod
    async def update(id: uuid.UUID, **kwargs: Any) -> Optional[PumpConfig]:
        """
        Update any FK field(s) on a PumpConfig record by id.
        Accepted kwargs: pump_info_id, impeller_id, base_plate_id,
                         options_id, test_documentation_id.
        Returns the updated and prefetched record, or None if not found.
        """
        record = await PumpConfig.get_or_none(id=id)
        if record is None:
            return None
        for field, value in kwargs.items():
            setattr(record, field, value)
        await record.save()
        await record.fetch_related(*PumpConfigRepository._PREFETCH)
        return record

    @staticmethod
    async def delete(id: uuid.UUID) -> bool:
        """Delete a PumpConfig record by id. Returns True if deleted, False if not found."""
        deleted_count = await PumpConfig.filter(id=id).delete()
        return deleted_count > 0