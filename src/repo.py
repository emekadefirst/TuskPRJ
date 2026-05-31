from fastapi import HTTPException
from tortoise.expressions import Q
from typing import Optional

from src.models import BasePlate, Impeller, Options, PumpConfig, PumpInfo, TestDocumentation
from src.schemas import (
    ImpellerSchema, ImpellerUpdateSchema,
    BasePlateSchema, BasePlateUpdateSchema,
    OptionSchema, OptionUpdateSchema,
    PumpInfoSchema, PumpInfoUpdateSchema,
    TestDocumentationSchema, TestDocumentationUpdateSchema,
    PumpConfigSchema, PumpConfigUpdateSchema
)


class PumpInfoRepo:
    @classmethod
    async def create(cls, dto: PumpInfoSchema):
        return await PumpInfo.create(**dto.dict())              # fix: added **

    @classmethod
    async def delete(cls, id: str):
        data = await PumpInfo.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Pump info not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await PumpInfo.get_or_none(id=id)
        if search is not None:
            return await PumpInfo.filter(
                Q(series__icontains=search) |
                Q(size__icontains=search) |
                Q(pump_material__icontains=search) |
                Q(shaft_configuration__icontains=search) |
                Q(casing_metal__icontains=search) |
                Q(casing_drain__icontains=search) |
                Q(casing_tap__icontains=search) |
                Q(flange_configuration__icontains=search) |
                Q(spot_facing__icontains=search) |
                Q(casing_wear_ring__icontains=search) |
                Q(tack_weld_wear_ring__icontains=search) |
                Q(casing_mounting__icontains=search) |
                Q(hardware__icontains=search) |
                Q(seal_chamber_config__icontains=search) |
                Q(shipping_gasket__icontains=search) |
                Q(cradle_material__icontains=search)
            ).all()
        return await PumpInfo.all()

    @classmethod
    async def update(cls, id: str, data: PumpInfoUpdateSchema):
        pump = await PumpInfo.get_or_none(id=id)
        if pump is None:
            return None
        await pump.update_from_dict(data.model_dump(exclude_unset=True))
        await pump.save()
        return pump                                             # fix: return pump not save()


class ImpellerRepo:
    @classmethod
    async def create(cls, dto: ImpellerSchema):
        return await Impeller.create(**dto.dict())

    @classmethod
    async def delete(cls, id: str):
        data = await Impeller.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Impeller not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await Impeller.get_or_none(id=id)
        if search is not None:
            return await Impeller.filter(
                Q(impeller_range__icontains=search) |
                Q(impeller_trim__icontains=search) |
                Q(impeller_balance__icontains=search) |
                Q(impeller_material__icontains=search) |
                Q(impeller_wear_ring_material__icontains=search)
            ).all()
        return await Impeller.all()

    @classmethod
    async def update(cls, id: str, data: ImpellerUpdateSchema):
        impeller = await Impeller.get_or_none(id=id)
        if impeller is None:
            return None
        await impeller.update_from_dict(data.model_dump(exclude_unset=True))
        await impeller.save()
        return impeller


class BasePlateRepo:
    @classmethod
    async def create(cls, dto: BasePlateSchema):
        return await BasePlate.create(**dto.dict())

    @classmethod
    async def delete(cls, id: str):
        data = await BasePlate.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Base plate not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await BasePlate.get_or_none(id=id)
        if search is not None:
            return await BasePlate.filter(
                Q(baseplate_type__icontains=search) |
                Q(baseplate_material__icontains=search) |
                Q(drip_pan__icontains=search) |
                Q(allignment_lugs__icontains=search) |
                Q(lifting_lugs__icontains=search) |
                Q(leveling_screws__icontains=search) |
                Q(grounding_lugs__icontains=search) |
                Q(grout_hole__icontains=search) |
                Q(isolation_pads__icontains=search) |
                Q(stilts__icontains=search)
            ).all()
        return await BasePlate.all()

    @classmethod
    async def update(cls, id: str, data: BasePlateUpdateSchema):
        base_plate = await BasePlate.get_or_none(id=id)
        if base_plate is None:
            return None
        await base_plate.update_from_dict(data.model_dump(exclude_unset=True))
        await base_plate.save()
        return base_plate


class OptionsRepo:
    @classmethod
    async def create(cls, dto: OptionSchema):
        return await Options.create(**dto.dict())

    @classmethod
    async def delete(cls, id: str):
        data = await Options.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Option not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await Options.get_or_none(id=id)
        if search is not None:
            return await Options.filter(
                Q(coupling_type__icontains=search) |
                Q(coupling_guard__icontains=search) |
                Q(auxillary_nameplate__icontains=search) |
                Q(crating__icontains=search) |
                Q(oil_options__icontains=search) |
                Q(bearing_frame_cooling__icontains=search) |
                Q(lubrication_options__icontains=search) |
                Q(oil_seat__icontains=search) |
                Q(sight_gauge__icontains=search) |
                Q(magnetic_drain__icontains=search) |
                Q(expansion_chamber__icontains=search)
            ).all()
        return await Options.all()

    @classmethod
    async def update(cls, id: str, data: OptionUpdateSchema):
        option = await Options.get_or_none(id=id)
        if option is None:
            return None
        await option.update_from_dict(data.model_dump(exclude_unset=True))
        await option.save()
        return option


class TestDocumentationRepo:
    @classmethod
    async def create(cls, dto: TestDocumentationSchema):
        return await TestDocumentation.create(**dto.dict())

    @classmethod
    async def delete(cls, id: str):
        data = await TestDocumentation.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Test documentation not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await TestDocumentation.get_or_none(id=id)
        if search is not None:
            return await TestDocumentation.filter(
                Q(performance_testing__icontains=search) |
                Q(hydro_testing__icontains=search) |
                Q(vibration__icontains=search) |
                Q(sound_level__icontains=search) |
                Q(general_inspection__icontains=search) |
                Q(documenttation_1__icontains=search) |
                Q(documenttation_2__icontains=search) |
                Q(documenttation_3__icontains=search) |
                Q(documenttation_4__icontains=search) |
                Q(documenttation_5__icontains=search) |
                Q(documenttation_6__icontains=search)
            ).all()
        return await TestDocumentation.all()

    @classmethod
    async def update(cls, id: str, data: TestDocumentationUpdateSchema):
        test_doc = await TestDocumentation.get_or_none(id=id)
        if test_doc is None:
            return None
        await test_doc.update_from_dict(data.model_dump(exclude_unset=True))
        await test_doc.save()
        return test_doc


class PumpConfigRepo:
    # Helper: turn a Tortoise model row into a plain dict.
    @staticmethod
    def _model_to_dict(obj):
        if obj is None:
            return None
        # Use the auto-generated pydantic schema if available, otherwise __dict__.
        data = {}
        for field_name in obj._meta.db_fields:
            data[field_name] = getattr(obj, field_name, None)
        # Stringify UUIDs and datetimes so JSON serialization is uniform.
        out = {}
        for k, v in data.items():
            if hasattr(v, "isoformat"):
                out[k] = v.isoformat()
            elif v is not None and not isinstance(v, (str, int, float, bool, dict, list)):
                out[k] = str(v)
            else:
                out[k] = v
        return out

    @classmethod
    def _serialize(cls, config: "PumpConfig"):
        """Return a PumpConfig as a dict with nested component objects."""
        return {
            "id":         str(config.id),
            "created_at": config.created_at.isoformat() if config.created_at else None,
            "updated_at": config.updated_at.isoformat() if config.updated_at else None,
            "pump_info":          cls._model_to_dict(getattr(config, "pump_info", None)),
            "impeller":           cls._model_to_dict(getattr(config, "impeller", None)),
            "base_plate":         cls._model_to_dict(getattr(config, "base_plate", None)),
            "options":            cls._model_to_dict(getattr(config, "options", None)),
            "test_documentation": cls._model_to_dict(getattr(config, "test_documentation", None)),
        }

    @classmethod
    async def create(cls, dto: PumpConfigSchema):
        config = await PumpConfig.create(
            pump_info_id=dto.pump_info_id,
            impeller_id=dto.impeller_id,
            base_plate_id=dto.base_plate_id,
            options_id=dto.option_id,
            test_documentation_id=dto.test_documentation_id,
        )
        # Re-fetch with relations so the response includes full nested objects.
        await config.fetch_related(
            "pump_info", "impeller", "base_plate", "options", "test_documentation"
        )
        return cls._serialize(config)

    @classmethod
    async def delete(cls, id: str):
        data = await PumpConfig.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Pump config not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None):
        if id is not None:
            config = await PumpConfig.get_or_none(id=id).prefetch_related(
                "pump_info", "impeller", "base_plate", "options", "test_documentation"
            )
            return cls._serialize(config) if config else None

        configs = await PumpConfig.all().prefetch_related(
            "pump_info", "impeller", "base_plate", "options", "test_documentation"
        )
        return [cls._serialize(c) for c in configs]

    @classmethod
    async def update(cls, id: str, data: PumpConfigUpdateSchema):
        pump_config = await PumpConfig.get_or_none(id=id)
        if pump_config is None:
            return None
        await pump_config.update_from_dict(data.model_dump(exclude_unset=True))
        await pump_config.save()
        # Return the full nested representation after update too.
        await pump_config.fetch_related(
            "pump_info", "impeller", "base_plate", "options", "test_documentation"
        )
        return cls._serialize(pump_config)