from fastapi import HTTPException
from tortoise.expressions import Q
from typing import Optional
from argon2 import PasswordHasher
from src.models import User, BasePlate, Impeller, Options, PumpConfig, PumpInfo, TestDocumentation, Seal, Motor
from src.schemas import (
    ImpellerSchema, ImpellerUpdateSchema,
    BasePlateSchema, BasePlateUpdateSchema,
    OptionSchema, OptionUpdateSchema,
    PumpInfoSchema, PumpInfoUpdateSchema,
    TestDocumentationSchema, TestDocumentationUpdateSchema,
    PumpConfigSchema, PumpConfigUpdateSchema,
    SealSchema, SealUpdateSchema,
    MotorSchema, MotorUpdateSchema,
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


class SealRepo:
    @classmethod
    async def create(cls, dto: SealSchema):
        return await Seal.create(**dto.dict())

    @classmethod
    async def delete(cls, id: str):
        data = await Seal.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Seal not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await Seal.get_or_none(id=id)
        if search is not None:
            return await Seal.filter(
                Q(seal_option__icontains=search) |
                Q(seal_mfr__icontains=search) |
                Q(seal_configuration__icontains=search) |
                Q(seal_type__icontains=search) |
                Q(gland_type__icontains=search) |
                Q(gland_gasket__icontains=search) |
                Q(shaft_sleeve_material__icontains=search) |
                Q(inboard_rotating_face__icontains=search) |
                Q(inboard_stationary_face__icontains=search) |
                Q(inboard_elastomer__icontains=search) |
                Q(outboard_rotating_face__icontains=search) |
                Q(outboard_stationary_face__icontains=search) |
                Q(outboard_elastomer__icontains=search)
            ).all()
        return await Seal.all()

    @classmethod
    async def update(cls, id: str, data: SealUpdateSchema):
        seal = await Seal.get_or_none(id=id)
        if seal is None:
            return None
        await seal.update_from_dict(data.model_dump(exclude_unset=True))
        await seal.save()
        return seal


class MotorRepo:
    @classmethod
    async def create(cls, dto: MotorSchema):
        return await Motor.create(**dto.dict())

    @classmethod
    async def delete(cls, id: str):
        data = await Motor.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Motor not found")
        return await data.delete()

    @classmethod
    async def fetch(cls, id: Optional[str] = None, search: Optional[str] = None):
        if id is not None:
            return await Motor.get_or_none(id=id)
        if search is not None:
            return await Motor.filter(
                Q(motor_control__icontains=search) |
                Q(power_hp__icontains=search) |
                Q(speed__icontains=search) |
                Q(voltage__icontains=search) |
                Q(phase_hertz__icontains=search) |
                Q(frame__icontains=search) |
                Q(enclosure__icontains=search) |
                Q(efficiency__icontains=search) |
                Q(c_face_adapter__icontains=search) |
                Q(manufacturer__icontains=search)
            ).all()
        return await Motor.all()

    @classmethod
    async def update(cls, id: str, data: MotorUpdateSchema):
        motor = await Motor.get_or_none(id=id)
        if motor is None:
            return None
        await motor.update_from_dict(data.model_dump(exclude_unset=True))
        await motor.save()
        return motor


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


# ---------------------------------------------------------------------------
# Pump config pricing
# ---------------------------------------------------------------------------
from decimal import Decimal as _Decimal, ROUND_HALF_UP as _ROUND_HALF_UP

# Transparent, deterministic list price for a pump config:
#   list_price = BASE + HP * PER_HP + material surcharge
# Kept in sync with scripts/backfill_prices.py.
_PRICE_BASE = _Decimal("1200")
_PRICE_PER_HP = _Decimal("18")
_MATERIAL_SURCHARGE = {
    "cast iron": _Decimal("0"),
    "ductile iron": _Decimal("450"),
    "(22) ductile iron": _Decimal("600"),
}


def compute_config_price(config: "PumpConfig") -> _Decimal:
    """Compute a list price from a config's motor HP and pump material."""
    motor = getattr(config, "motor", None)
    pump_info = getattr(config, "pump_info", None)

    hp = _Decimal("0")
    if motor is not None and motor.power_hp:
        try:
            hp = _Decimal(str(motor.power_hp).split()[0])
        except Exception:
            hp = _Decimal("0")

    material_key = ((getattr(pump_info, "pump_material", "") or "")).strip().lower()
    surcharge = _MATERIAL_SURCHARGE.get(material_key, _Decimal("200"))

    total = _PRICE_BASE + hp * _PRICE_PER_HP + surcharge
    return total.quantize(_Decimal("0.01"), rounding=_ROUND_HALF_UP)


def money_str(value) -> "str | None":
    """Format a stored decimal as a plain 2dp string (avoids 3.15E+3 output)."""
    if value is None:
        return None
    try:
        return str(_Decimal(str(value)).quantize(_Decimal("0.01"), rounding=_ROUND_HALF_UP))
    except Exception:
        return str(value)


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
            "name":       config.name,
            "notes":      config.notes,
            "is_catalog": config.is_catalog,
            "list_price": money_str(config.list_price),
            "created_at": config.created_at.isoformat() if config.created_at else None,
            "updated_at": config.updated_at.isoformat() if config.updated_at else None,
            "pump_info":          cls._model_to_dict(getattr(config, "pump_info", None)),
            "seal":               cls._model_to_dict(getattr(config, "seal", None)),
            "motor":              cls._model_to_dict(getattr(config, "motor", None)),
            "impeller":           cls._model_to_dict(getattr(config, "impeller", None)),
            "base_plate":         cls._model_to_dict(getattr(config, "base_plate", None)),
            "options":            cls._model_to_dict(getattr(config, "options", None)),
            "test_documentation": cls._model_to_dict(getattr(config, "test_documentation", None)),
        }

    @classmethod
    async def create(cls, dto: PumpConfigSchema):
        list_price = dto.list_price
        config = await PumpConfig.create(
            pump_info_id=dto.pump_info_id,
            seal_id=dto.seal_id,
            motor_id=dto.motor_id,
            impeller_id=dto.impeller_id,
            base_plate_id=dto.base_plate_id,
            options_id=dto.option_id,
            test_documentation_id=dto.test_documentation_id,
            name=dto.name,
            notes=dto.notes,
            is_catalog=dto.is_catalog,
            list_price=list_price,
        )
        # Re-fetch with relations so the response includes full nested objects.
        await config.fetch_related(
            "pump_info", "seal", "motor", "impeller",
            "base_plate", "options", "test_documentation",
        )
        # Auto-price a freshly built config when no explicit price was given,
        # so user-built configs are orderable just like catalog ones.
        if list_price is None:
            config.list_price = compute_config_price(config)
            await config.save()
        return cls._serialize(config)

    @classmethod
    async def delete(cls, id: str):
        data = await PumpConfig.get_or_none(id=id)
        if not data:
            raise HTTPException(status_code=404, detail="Pump config not found")
        return await data.delete()

    @classmethod
    async def fetch(
        cls,
        id: Optional[str] = None,
        catalog: Optional[bool] = None,
        search: Optional[str] = None,
    ):
        if id is not None:
            config = await PumpConfig.get_or_none(id=id).prefetch_related(
                "pump_info", "seal", "motor", "impeller",
                "base_plate", "options", "test_documentation",
            )
            return cls._serialize(config) if config else None

        qs = PumpConfig.all()
        if catalog is not None:
            qs = qs.filter(is_catalog=catalog)
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(notes__icontains=search)
                | Q(pump_info__series__icontains=search)
                | Q(pump_info__size__icontains=search)
            )

        configs = await qs.order_by("name").prefetch_related(
            "pump_info", "seal", "motor", "impeller",
            "base_plate", "options", "test_documentation",
        )
        return [cls._serialize(c) for c in configs]

    @classmethod
    async def update(cls, id: str, data: PumpConfigUpdateSchema):
        pump_config = await PumpConfig.get_or_none(id=id)
        if pump_config is None:
            return None
        payload = data.model_dump(exclude_unset=True)
        # Map the schema's "option_id" onto the model's "options_id" column.
        if "option_id" in payload:
            payload["options_id"] = payload.pop("option_id")
        await pump_config.update_from_dict(payload)
        await pump_config.save()
        # Return the full nested representation after update too.
        await pump_config.fetch_related(
            "pump_info", "seal", "motor", "impeller",
            "base_plate", "options", "test_documentation",
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
            "unit_price":     money_str(item.unit_price),
            "subtotal":       money_str(Decimal(item.unit_price) * item.quantity),
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
            "total":            money_str(order.total),
            "user_id":          str(order.user_id) if hasattr(order, "user_id") else None,
            "items":            [cls._serialize_item(i) for i in items],
            "created_at":       order.created_at.isoformat() if order.created_at else None,
            "updated_at":       order.updated_at.isoformat() if order.updated_at else None,
        }

    @classmethod
    async def create(cls, user: User, dto: OrderSchema) -> dict:
        # Validate every referenced pump config exists, and price each line from
        # the config's server-side list_price (clients never set prices).
        config_ids = [i.pump_config_id for i in dto.items]
        configs = await PumpConfig.filter(id__in=config_ids)
        price_by_id = {
            str(c.id): (Decimal(c.list_price) if c.list_price is not None else Decimal("0"))
            for c in configs
        }
        missing = [cid for cid in config_ids if cid not in price_by_id]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown pump_config_id(s): {', '.join(missing)}",
            )

        unpriced = [cid for cid in config_ids if price_by_id[cid] <= 0]
        if unpriced:
            raise HTTPException(
                status_code=409,
                detail="One or more selected configurations have no price set. "
                       "An administrator must set a list price before it can be ordered.",
            )

        total = sum(
            (price_by_id[i.pump_config_id] * i.quantity for i in dto.items),
            Decimal("0"),
        )

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
                    unit_price=price_by_id[it.pump_config_id],
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
                "items__pump_config__seal",
                "items__pump_config__motor",
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
            "items__pump_config__seal",
            "items__pump_config__motor",
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


# ---------------------------------------------------------------------------
# PricingRepo  (mirrors the workbook's "PX Configurator" calculation)
# ---------------------------------------------------------------------------
from src.models import PriceList, OptionPrice
from src.schemas import (
    PriceListSchema,
    OptionPriceSchema,
    QuoteRequestSchema,
)

# Money rounds to cents, half-up, like a spreadsheet currency cell.
from decimal import ROUND_HALF_UP

_CENTS = Decimal("0.01")


def _money(value: Decimal) -> Decimal:
    return Decimal(value).quantize(_CENTS, rounding=ROUND_HALF_UP)


class PricingRepo:
    """
    Pricing rules loaded from the workbook's Price Lists tab:
      * PriceList   -> base price per (product_family, size)
      * OptionPrice -> add-on price per (field, option)

    The quote math follows PX Configurator:
        unit_list      = base_price + sum(option_prices)
        extended       = unit_list * quantity
        discount_amount= extended * discount_pct/100
        subtotal       = extended - discount_amount
        tax            = subtotal * tax_rate/100
        total          = subtotal + tax
    """

    # ----- price list CRUD -------------------------------------------------
    @classmethod
    async def list_base_prices(cls):
        return await PriceList.all().order_by("product_family", "size")

    @classmethod
    async def list_option_prices(cls):
        return await OptionPrice.all().order_by("field", "option")

    @classmethod
    async def upsert_base_price(cls, dto: PriceListSchema):
        obj, _ = await PriceList.update_or_create(
            product_family=dto.product_family,
            size=dto.size,
            defaults={"base_price": dto.base_price},
        )
        return obj

    @classmethod
    async def upsert_option_price(cls, dto: OptionPriceSchema):
        obj, _ = await OptionPrice.update_or_create(
            field=dto.field,
            option=dto.option,
            defaults={"option_price": dto.option_price},
        )
        return obj

    # ----- the quote engine ------------------------------------------------
    @classmethod
    async def quote(cls, dto: QuoteRequestSchema) -> dict:
        warnings: list[str] = []

        base_row = await PriceList.get_or_none(
            product_family=dto.product_family, size=dto.size
        )
        if base_row is None:
            raise HTTPException(
                status_code=404,
                detail=f"No base price for '{dto.product_family} | {dto.size}'",
            )
        base_price = Decimal(base_row.base_price)

        breakdown = [
            {
                "field": "Base Family / Size",
                "option": f"{dto.product_family} / {dto.size}",
                "price": _money(base_price),
            }
        ]

        option_total = Decimal("0")
        for field, option in dto.options.items():
            row = await OptionPrice.get_or_none(field=field, option=option)
            if row is None:
                warnings.append(f"No price for {field} = '{option}'; treated as $0.00")
                price = Decimal("0")
            else:
                price = Decimal(row.option_price)
            option_total += price
            breakdown.append(
                {"field": field, "option": option, "price": _money(price)}
            )

        unit_list = base_price + option_total
        extended = unit_list * dto.quantity
        discount_amount = extended * (Decimal(dto.discount_pct) / Decimal("100"))
        subtotal = extended - discount_amount
        tax = subtotal * (Decimal(dto.tax_rate) / Decimal("100"))
        total = subtotal + tax

        return {
            "product_family": dto.product_family,
            "size": dto.size,
            "quantity": dto.quantity,
            "base_price": _money(base_price),
            "option_price": _money(option_total),
            "unit_list_price": _money(unit_list),
            "extended_list_price": _money(extended),
            "discount_pct": dto.discount_pct,
            "discount_amount": _money(discount_amount),
            "subtotal": _money(subtotal),
            "tax_rate": dto.tax_rate,
            "tax": _money(tax),
            "total_quote": _money(total),
            "breakdown": breakdown,
            "warnings": warnings,
        }
