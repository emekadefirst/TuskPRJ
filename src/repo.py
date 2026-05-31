from fastapi import HTTPException
from tortoise.expressions import Q
from typing import Optional
from argon2 import PasswordHasher
from src.models import User, BasePlate, Impeller, Options, PumpConfig, PumpInfo, TestDocumentation
from src.schemas import (
    ImpellerSchema, ImpellerUpdateSchema,
    BasePlateSchema, BasePlateUpdateSchema,
    OptionSchema, OptionUpdateSchema,
    PumpInfoSchema, PumpInfoUpdateSchema,
    TestDocumentationSchema, TestDocumentationUpdateSchema,
    PumpConfigSchema, PumpConfigUpdateSchema,
    UserCreateSchema, UserUpdateSchema,
)

ph = PasswordHasher()

SAFE_FIELDS = ["id", "first_name", "last_name", "email", "created_at", "updated_at"]


class UserRepo:

    @classmethod
    async def create(cls, dto: UserCreateSchema):
        existing = await User.get_or_none(email=dto.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        hashed = ph.hash(dto.password)
        return await User.create(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            password=hashed
        )

    @classmethod
    async def fetch(cls, id: Optional[str] = None, email: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await User.filter(id=id).values(*SAFE_FIELDS).first()

        if email is not None:
            return await User.filter(email=email).values(*SAFE_FIELDS).first()

        if search is not None:
            return await User.filter(
                Q(id__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            ).values(*SAFE_FIELDS)

        return await User.all().values(*SAFE_FIELDS)

    @classmethod
    async def update(cls, id: str, dto: UserUpdateSchema):
        user = await User.get_or_none(id=id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = dto.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = ph.hash(update_data["password"])

        if "email" in update_data and update_data["email"] != user.email:
            existing = await User.get_or_none(email=update_data["email"])
            if existing:
                raise HTTPException(status_code=409, detail="Email already in use")

        await user.update_from_dict(update_data)
        await user.save()

        return await User.filter(id=id).values(*SAFE_FIELDS).first()

    @classmethod
    async def delete(cls, id: str):
        user = await User.get_or_none(id=id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await user.delete()

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



# ---------------------------------------------------------------------------
# OrderRepo
# ---------------------------------------------------------------------------
from decimal import Decimal
from tortoise.transactions import in_transaction

from src.models import Order, OrderItem, User
from src.schemas import OrderSchema, OrderUpdateSchema


class OrderRepo:

    VALID_STATUSES = {"pending", "confirmed", "shipped", "delivered", "cancelled"}

    @staticmethod
    def _serialize_item(item: OrderItem) -> dict:
        pc = getattr(item, "pump_config", None)
        return {
            "id":             str(item.id),
            "quantity":       item.quantity,
            "unit_price":     str(item.unit_price),
            "subtotal":       str(Decimal(item.unit_price) * item.quantity),
            "pump_config":    PumpConfigRepo._serialize(pc) if pc else None,
            "pump_config_id": str(pc.id) if pc else None,
            "created_at":     item.created_at.isoformat() if item.created_at else None,
            "updated_at":     item.updated_at.isoformat() if item.updated_at else None,
        }

    @classmethod
    def _serialize(cls, order: Order) -> dict:
        items = list(getattr(order, "items", []) or [])
        return {
            "id":               str(order.id),
            "status":           order.status,
            "notes":            order.notes,
            "shipping_address": order.shipping_address,
            "total":            str(order.total),
            "user_id":          str(order.user_id) if hasattr(order, "user_id") else None,
            "items":            [cls._serialize_item(i) for i in items],
            "created_at":       order.created_at.isoformat() if order.created_at else None,
            "updated_at":       order.updated_at.isoformat() if order.updated_at else None,
        }

    @classmethod
    async def create(cls, user: User, dto: OrderSchema) -> dict:
        # Validate every referenced pump config exists before we create anything.
        config_ids = [i.pump_config_id for i in dto.items]
        existing = await PumpConfig.filter(id__in=config_ids).values_list("id", flat=True)
        existing_set = {str(x) for x in existing}
        missing = [cid for cid in config_ids if cid not in existing_set]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown pump_config_id(s): {', '.join(missing)}",
            )

        total = sum((Decimal(i.unit_price) * i.quantity for i in dto.items), Decimal("0"))

        async with in_transaction():
            order = await Order.create(
                user_id=user.id,
                status="pending",
                notes=dto.notes,
                shipping_address=dto.shipping_address,
                total=total,
            )
            for it in dto.items:
                await OrderItem.create(
                    order_id=order.id,
                    pump_config_id=it.pump_config_id,
                    quantity=it.quantity,
                    unit_price=it.unit_price,
                )

        return await cls.fetch(id=str(order.id), user=user)

    @classmethod
    async def fetch(
        cls,
        user: Optional[User] = None,
        id: Optional[str] = None,
        search: Optional[str] = None,
    ):
        """
        - If `id` is given, return one order (scoped to user when provided).
        - Otherwise return a list, scoped to user when provided.
        - `search` matches order id prefix, status, or notes.
        """
        # Build base queryset
        if id is not None:
            qs = Order.filter(id=id)
            if user is not None:
                qs = qs.filter(user_id=user.id)
            order = await qs.prefetch_related(
                "items__pump_config__pump_info",
                "items__pump_config__impeller",
                "items__pump_config__base_plate",
                "items__pump_config__options",
                "items__pump_config__test_documentation",
            ).first()
            return cls._serialize(order) if order else None

        qs = Order.all()
        if user is not None:
            qs = qs.filter(user_id=user.id)
        if search:
            qs = qs.filter(
                Q(status__icontains=search)
                | Q(notes__icontains=search)
            )

        orders = await qs.order_by("-created_at").prefetch_related(
            "items__pump_config__pump_info",
            "items__pump_config__impeller",
            "items__pump_config__base_plate",
            "items__pump_config__options",
            "items__pump_config__test_documentation",
        )
        return [cls._serialize(o) for o in orders]

    @classmethod
    async def update(cls, user: User, id: str, dto: OrderUpdateSchema):
        order = await Order.get_or_none(id=id, user_id=user.id)
        if order is None:
            return None
        data = dto.model_dump(exclude_unset=True)
        if "status" in data and data["status"] not in cls.VALID_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {sorted(cls.VALID_STATUSES)}",
            )
        await order.update_from_dict(data)
        await order.save()
        return await cls.fetch(id=str(order.id), user=user)

    @classmethod
    async def delete(cls, user: User, id: str):
        order = await Order.get_or_none(id=id, user_id=user.id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        await order.delete()
        return None
