import uuid
from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    """Abstract base model with shared id, created_at, and updated_at fields."""

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True # prvents the compiler from treating the class as a but as a regualar python class 


class User(BaseModel):
    first_name = fields.CharField(max_length=255)
    last_name  = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)

    class Meta:
        table = "users"

class PumpInfo(BaseModel):
    series = fields.CharField(max_length=255)
    size = fields.CharField(max_length=255)
    pump_material = fields.CharField(max_length=255)
    shaft_configuration = fields.CharField(max_length=255)
    casing_metal = fields.CharField(max_length=255)
    casing_drain = fields.CharField(max_length=255)
    casing_tap = fields.CharField(max_length=255)
    casing_gasket = fields.CharField(max_length=255, default="Grafoil")
    flange_configuration = fields.CharField(max_length=255)
    spot_facing = fields.CharField(max_length=255, default="Not required")
    casing_wear_ring = fields.CharField(max_length=255)
    tack_weld_wear_ring = fields.CharField(max_length=255, default="Not required")
    casing_mounting = fields.CharField(max_length=255, default="Not required")
    hardware = fields.CharField(max_length=255, null=True)
    seal_chamber_config = fields.CharField(max_length=255, default="Not required")
    shipping_gasket = fields.CharField(max_length=255, default="Not required")
    cradle_material = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "pump_infos"


class Seal(BaseModel):
    """
    Mechanical seal selection. Mirrors the workbook's Mechanical Seals block
    (Data Sheet) and the Seal columns of the Config Info / Seal Descriptions tabs.
    """

    seal_option = fields.CharField(max_length=255, default="Included")
    seal_mfr = fields.CharField(max_length=255, null=True)
    seal_configuration = fields.CharField(max_length=255)
    seal_type = fields.CharField(max_length=255)
    gland_type = fields.CharField(max_length=255, default="NONE")
    gland_gasket = fields.CharField(max_length=255, default="NONE")
    shaft_sleeve_material = fields.CharField(max_length=255, default="NONE")
    inboard_rotating_face = fields.CharField(max_length=255)
    inboard_stationary_face = fields.CharField(max_length=255)
    inboard_elastomer = fields.CharField(max_length=255)
    outboard_rotating_face = fields.CharField(max_length=255, default="N/A")
    outboard_stationary_face = fields.CharField(max_length=255, default="N/A")
    outboard_elastomer = fields.CharField(max_length=255, default="N/A")

    class Meta:
        table = "seals"


class Motor(BaseModel):
    """
    Motor selection. Mirrors the Motor Options block of the Data Sheet plus the
    Recommended HP / Speed / Voltage columns of Config Info.
    """

    motor_control = fields.CharField(max_length=255, default="N/A")
    power_hp = fields.CharField(max_length=255)
    speed = fields.CharField(max_length=255)
    voltage = fields.CharField(max_length=255)
    phase_hertz = fields.CharField(max_length=255, default="3PH / 60Hz")
    frame = fields.CharField(max_length=255, null=True)
    enclosure = fields.CharField(max_length=255, default="TEFC")
    efficiency = fields.CharField(max_length=255, default="Premium")
    c_face_adapter = fields.CharField(max_length=255, default="N/A")
    manufacturer = fields.CharField(max_length=255, default="N/A")

    class Meta:
        table = "motors"


class Impeller(BaseModel):
    impeller_range = fields.CharField(max_length=255)
    impeller_trim = fields.CharField(max_length=255)
    impeller_balance = fields.CharField(max_length=255)
    impeller_material = fields.CharField(max_length=255)
    impeller_wear_ring_material = fields.CharField(max_length=255)

    class Meta:
        table = "impellers"


class BasePlate(BaseModel):
    baseplate_type = fields.CharField(max_length=255)
    baseplate_material = fields.CharField(max_length=255)
    drip_pan = fields.CharField(max_length=255)
    allignment_lugs = fields.CharField(max_length=255, default="Not required")
    lifting_lugs = fields.CharField(max_length=255, default="Not required")
    leveling_screws = fields.CharField(max_length=255, default="Not required")
    grounding_lugs = fields.CharField(max_length=255, default="Not required")
    grout_hole = fields.CharField(max_length=255, default="Not required")
    isolation_pads = fields.CharField(max_length=255, default="Not required")
    stilts = fields.CharField(max_length=255, default="Not required")

    class Meta:
        table = "base_plates"


class Options(BaseModel):
    coupling_type = fields.CharField(max_length=255)
    coupling_guard = fields.CharField(max_length=255)
    auxillary_nameplate = fields.CharField(max_length=255)
    crating = fields.CharField(max_length=255)
    oil_options = fields.CharField(max_length=255)
    bearing_frame_cooling = fields.CharField(max_length=255)
    lubrication_options = fields.CharField(max_length=255)
    oil_seat = fields.CharField(max_length=255)
    sight_gauge = fields.CharField(max_length=255)
    magnetic_drain = fields.CharField(max_length=255)
    expansion_chamber = fields.CharField(max_length=255)

    class Meta:
        table = "options"


class TestDocumentation(BaseModel):
    performance_testing = fields.CharField(max_length=255)
    hydro_testing = fields.CharField(max_length=255)
    vibration = fields.CharField(max_length=255)
    sound_level = fields.CharField(max_length=255)
    general_inspection = fields.CharField(max_length=255)
    documenttation_1 = fields.CharField(max_length=255)
    documenttation_2 = fields.CharField(max_length=255)
    documenttation_3 = fields.CharField(max_length=255)
    documenttation_4 = fields.CharField(max_length=255)
    documenttation_5 = fields.CharField(max_length=255)
    documenttation_6 = fields.CharField(max_length=255)

    class Meta:
        table = "test_documentations"


class PumpConfig(BaseModel):
    """
    Aggregate model that links pump component models together.

    A PumpConfig is either:
      * a catalog entry (is_catalog=True) imported from the workbook's
        Config Info tab and orderable as-is, or
      * a user-built "mix your own" configuration.

    pump_info, seal and motor are always required. impeller, base_plate,
    options and test_documentation are optional so a config can exist with
    just the core pump + seal + motor data (as the workbook provides).
    """

    name = fields.CharField(max_length=255, null=True)          # e.g. the workbook "Configuration ID"
    notes = fields.TextField(null=True)
    is_catalog = fields.BooleanField(default=False)
    list_price = fields.DecimalField(max_digits=12, decimal_places=2, null=True)

    pump_info = fields.ForeignKeyField(
        "models.PumpInfo",
        related_name="pump_config",
        on_delete=fields.CASCADE,
    )
    seal = fields.ForeignKeyField(
        "models.Seal",
        related_name="pump_config",
        on_delete=fields.CASCADE,
    )
    motor = fields.ForeignKeyField(
        "models.Motor",
        related_name="pump_config",
        on_delete=fields.CASCADE,
    )
    impeller = fields.ForeignKeyField(
        "models.Impeller",
        related_name="pump_config",
        on_delete=fields.CASCADE,
        null=True,
    )
    base_plate = fields.ForeignKeyField(
        "models.BasePlate",
        related_name="pump_config",
        on_delete=fields.CASCADE,
        null=True,
    )
    options = fields.ForeignKeyField(
        "models.Options",
        related_name="pump_config",
        on_delete=fields.CASCADE,
        null=True,
    )
    test_documentation = fields.ForeignKeyField(
        "models.TestDocumentation",
        related_name="pump_config",
        on_delete=fields.CASCADE,
        null=True,
    )

    class Meta:
        table = "pump_configs"


class Order(BaseModel):
    """
    A purchase order placed by a user. The total is summed from the line items
    and stored on the order so historical orders don't change if prices move.
    """

    STATUSES = ("pending", "confirmed", "shipped", "delivered", "cancelled")

    user = fields.ForeignKeyField(
        "models.User",
        related_name="orders",
        on_delete=fields.CASCADE,
    )
    status = fields.CharField(max_length=32, default="pending")
    notes = fields.TextField(null=True)
    shipping_address = fields.TextField(null=True)
    total = fields.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        table = "orders"


class OrderItem(BaseModel):
    """A single line item on an order: one pump config, with quantity + price."""

    order = fields.ForeignKeyField(
        "models.Order",
        related_name="items",
        on_delete=fields.CASCADE,
    )
    pump_config = fields.ForeignKeyField(
        "models.PumpConfig",
        related_name="order_items",
        on_delete=fields.RESTRICT,  # don't let a config disappear under an order
    )
    quantity = fields.IntField(default=1)
    unit_price = fields.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        table = "order_items"


# ---------------------------------------------------------------------------
# Pricing (from the workbook's "Price Lists" tab)
# ---------------------------------------------------------------------------


class PriceList(BaseModel):
    """
    Base price for a product family + size combination.
    Source: Price Lists tab (left block) -> key = "<product_family>|<size>".
    """

    product_family = fields.CharField(max_length=255)
    size = fields.CharField(max_length=255)
    base_price = fields.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        table = "price_lists"
        unique_together = (("product_family", "size"),)


class OptionPrice(BaseModel):
    """
    Per-option add-on price.
    Source: Price Lists tab (middle block) -> key = "<field>|<option>".
    """

    field = fields.CharField(max_length=255)      # e.g. "Material", "Voltage"
    option = fields.CharField(max_length=255)      # e.g. "Steel", "240V"
    option_price = fields.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        table = "option_prices"
        unique_together = (("field", "option"),)
