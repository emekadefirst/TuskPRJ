from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from decimal import Decimal


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class PumpInfoSchema(BaseModel):
    series: str
    size: str
    pump_material: str
    shaft_configuration: str
    casing_metal: str
    casing_drain: str
    casing_tap: str
    casing_gasket: Optional[str] = "Grafoil"
    flange_configuration: str
    spot_facing: Optional[str] = "Not required"
    casing_wear_ring: str
    tack_weld_wear_ring: Optional[str] = "Not required"
    casing_mounting: Optional[str] = "Not required"
    hardware: Optional[str] = None
    seal_chamber_config: Optional[str] = "Not required"
    shipping_gasket: Optional[str] = "Not required"
    cradle_material: Optional[str] = None


class PumpInfoUpdateSchema(BaseModel):
    series: Optional[str] = None
    size: Optional[str] = None
    pump_material: Optional[str] = None
    shaft_configuration: Optional[str] = None
    casing_metal: Optional[str] = None
    casing_drain: Optional[str] = None
    casing_tap: Optional[str] = None
    casing_gasket: Optional[str] = None
    flange_configuration: Optional[str] = None
    spot_facing: Optional[str] = None
    casing_wear_ring: Optional[str] = None
    tack_weld_wear_ring: Optional[str] = None
    casing_mounting: Optional[str] = None
    hardware: Optional[str] = None
    seal_chamber_config: Optional[str] = None
    shipping_gasket: Optional[str] = None
    cradle_material: Optional[str] = None


class SealSchema(BaseModel):
    seal_option: Optional[str] = "Included"
    seal_mfr: Optional[str] = None
    seal_configuration: str
    seal_type: str
    gland_type: Optional[str] = "NONE"
    gland_gasket: Optional[str] = "NONE"
    shaft_sleeve_material: Optional[str] = "NONE"
    inboard_rotating_face: str
    inboard_stationary_face: str
    inboard_elastomer: str
    outboard_rotating_face: Optional[str] = "N/A"
    outboard_stationary_face: Optional[str] = "N/A"
    outboard_elastomer: Optional[str] = "N/A"


class SealUpdateSchema(BaseModel):
    seal_option: Optional[str] = None
    seal_mfr: Optional[str] = None
    seal_configuration: Optional[str] = None
    seal_type: Optional[str] = None
    gland_type: Optional[str] = None
    gland_gasket: Optional[str] = None
    shaft_sleeve_material: Optional[str] = None
    inboard_rotating_face: Optional[str] = None
    inboard_stationary_face: Optional[str] = None
    inboard_elastomer: Optional[str] = None
    outboard_rotating_face: Optional[str] = None
    outboard_stationary_face: Optional[str] = None
    outboard_elastomer: Optional[str] = None


class MotorSchema(BaseModel):
    motor_control: Optional[str] = "N/A"
    power_hp: str
    speed: str
    voltage: str
    phase_hertz: Optional[str] = "3PH / 60Hz"
    frame: Optional[str] = None
    enclosure: Optional[str] = "TEFC"
    efficiency: Optional[str] = "Premium"
    c_face_adapter: Optional[str] = "N/A"
    manufacturer: Optional[str] = "N/A"


class MotorUpdateSchema(BaseModel):
    motor_control: Optional[str] = None
    power_hp: Optional[str] = None
    speed: Optional[str] = None
    voltage: Optional[str] = None
    phase_hertz: Optional[str] = None
    frame: Optional[str] = None
    enclosure: Optional[str] = None
    efficiency: Optional[str] = None
    c_face_adapter: Optional[str] = None
    manufacturer: Optional[str] = None

class ImpellerSchema(BaseModel):
    impeller_range: str
    impeller_trim: str
    impeller_balance: str
    impeller_material: str
    impeller_wear_ring_material: str

class ImpellerUpdateSchema(BaseModel):
    impeller_range: Optional[str]
    impeller_trim: Optional[str]
    impeller_balance: Optional[str]
    impeller_material: Optional[str]
    impeller_wear_ring_material: Optional[str]
    
class BasePlateSchema(BaseModel):
    baseplate_type: str
    baseplate_material: str
    drip_pan: str
    allignment_lugs: Optional[str] = "Not required"
    lifting_lugs: Optional[str] = "Not required"
    leveling_screws: Optional[str] = "Not required"
    grounding_lugs: Optional[str] = "Not required"
    grout_hole: Optional[str] = "Not required"
    isolation_pads: Optional[str] = "Not required"
    stilts: Optional[str] = "Not required"

class BasePlateUpdateSchema(BaseModel):
    baseplate_type: Optional[str]
    baseplate_material: Optional[str]
    drip_pan: Optional[str]
    allignment_lugs: Optional[str] = "Not required"
    lifting_lugs: Optional[str] = "Not required"
    leveling_screws: Optional[str] = "Not required"
    grounding_lugs: Optional[str] = "Not required"
    grout_hole: Optional[str] = "Not required"
    isolation_pads: Optional[str] = "Not required"
    stilts: Optional[str] = "Not required"


class OptionSchema(BaseModel):
    coupling_type: str
    coupling_guard: str
    auxillary_nameplate: str
    crating: str
    oil_options: str
    bearing_frame_cooling: str
    lubrication_options: str
    oil_seat: str
    sight_gauge: str
    magnetic_drain: str
    expansion_chamber: str

class OptionUpdateSchema(BaseModel):
    coupling_type: Optional[str]
    coupling_guard: Optional[str]
    auxillary_nameplate: Optional[str]
    crating: Optional[str]
    oil_options: Optional[str]
    bearing_frame_cooling: Optional[str]
    lubrication_options: Optional[str]
    oil_seat: Optional[str]
    sight_gauge: Optional[str]
    magnetic_drain: Optional[str]
    expansion_chamber: Optional[str]


class TestDocumentationSchema(BaseModel):
    performance_testing: str
    hydro_testing: str
    vibration: str
    sound_level: str
    general_inspection: str
    documenttation_1 : str
    documenttation_2 : str
    documenttation_3 : str
    documenttation_4 : str
    documenttation_5 : str
    documenttation_6 : str

class TestDocumentationUpdateSchema(BaseModel):
    performance_testing: Optional[str]
    hydro_testing: Optional[str]
    vibration: Optional[str]
    sound_level: Optional[str]
    general_inspection: Optional[str]
    documenttation_1 : Optional[str]
    documenttation_2 : Optional[str]
    documenttation_3 : Optional[str]
    documenttation_4 : Optional[str]
    documenttation_5 : Optional[str]
    documenttation_6 : Optional[str]


# This brings together all pump class together to create a larger class
class PumpConfigSchema(BaseModel):
    pump_info_id: str
    seal_id: str
    motor_id: str
    impeller_id: Optional[str] = None
    base_plate_id: Optional[str] = None
    option_id: Optional[str] = None
    test_documentation_id: Optional[str] = None
    name: Optional[str] = None
    notes: Optional[str] = None
    is_catalog: bool = False
    list_price: Optional[Decimal] = None

class PumpConfigUpdateSchema(BaseModel):
    pump_info_id: Optional[str] = None
    seal_id: Optional[str] = None
    motor_id: Optional[str] = None
    impeller_id: Optional[str] = None
    base_plate_id: Optional[str] = None
    option_id: Optional[str] = None
    test_documentation_id: Optional[str] = None
    name: Optional[str] = None
    notes: Optional[str] = None
    is_catalog: Optional[bool] = None
    list_price: Optional[Decimal] = None


class PriceListSchema(BaseModel):
    product_family: str
    size: str
    base_price: Decimal = Decimal("0")


class OptionPriceSchema(BaseModel):
    field: str
    option: str
    option_price: Decimal = Decimal("0")


# ---------------------------------------------------------------------------
# Quote / pricing engine (mirrors the workbook's "PX Configurator" math)
# ---------------------------------------------------------------------------


class QuoteRequestSchema(BaseModel):
    product_family: str
    size: str
    # Selected options as {field: option}, e.g. {"Material": "Steel", "Voltage": "240V"}.
    options: dict[str, str] = Field(default_factory=dict)
    quantity: int = Field(default=1, ge=1)
    discount_pct: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    tax_rate: Decimal = Field(default=Decimal("0"), ge=0, le=100)


class QuoteLineSchema(BaseModel):
    field: str
    option: str
    price: Decimal


class QuoteResponseSchema(BaseModel):
    product_family: str
    size: str
    quantity: int
    base_price: Decimal
    option_price: Decimal
    unit_list_price: Decimal
    extended_list_price: Decimal
    discount_pct: Decimal
    discount_amount: Decimal
    subtotal: Decimal
    tax_rate: Decimal
    tax: Decimal
    total_quote: Decimal
    breakdown: list[QuoteLineSchema]
    warnings: list[str] = Field(default_factory=list)



# ---------------------------------------------------------------------------
# Order / OrderItem
# ---------------------------------------------------------------------------


class OrderItemSchema(BaseModel):
    pump_config_id: str
    quantity: int = Field(default=1, ge=1)
    # unit_price is intentionally omitted: the server prices each line from the
    # pump config's list_price so clients can't set their own prices.


class OrderSchema(BaseModel):
    items: list[OrderItemSchema] = Field(..., min_length=1)
    notes: Optional[str] = None
    shipping_address: Optional[str] = None


class OrderUpdateSchema(BaseModel):
    status: Optional[str] = None         # pending|confirmed|shipped|delivered|cancelled
    notes: Optional[str] = None
    shipping_address: Optional[str] = None
