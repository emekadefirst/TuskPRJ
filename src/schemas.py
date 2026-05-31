from pydantic import BaseModel
from typing import Optional


class PumpInfoSchema(BaseModel):
    series: str
    size: str
    pump_material: str
    shaft_configuration: str
    casing_metal: str
    casing_drain: str
    casing_tap: str
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
    series: Optional[str]
    size: Optional[str]
    pump_material: Optional[str]
    shaft_configuration: Optional[str]
    casing_metal: Optional[str]
    casing_drain: Optional[str]
    casing_tap: Optional[str]
    flange_configuration: Optional[str]
    spot_facing: Optional[str] = "Not required"
    casing_wear_ring: str
    tack_weld_wear_ring: Optional[str] = "Not required"
    casing_mounting: Optional[str] = "Not required"
    hardware: Optional[str] = None
    seal_chamber_config: Optional[str] = "Not required"
    shipping_gasket: Optional[str] = "Not required"
    cradle_material: Optional[str] = None

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
    impeller_id: str
    base_plate_id: str
    option_id: str
    test_documentation_id: str

class PumpConfigUpdateSchema(BaseModel):
    pump_info_id: Optional[str]
    impeller_id: Optional[str]
    base_plate_id: Optional[str]
    option_id: Optional[str]
    test_documentation_id: Optional[str]