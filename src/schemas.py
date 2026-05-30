from pydantic import BaseModel
from typing import Optional


class PumpInfo(BaseModel):
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

class Impeller(BaseModel):
    impeller_range: str
    impeller_trim: str
    impeller_balance: str
    impeller_material: str
    impeller_wear_ring_material: str
    
class BasePlate(BaseModel):
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


class Options(BaseModel):
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


class TestDocumentation(BaseModel):
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


# This brings together all pump class together to create a larger class
class PumpConfig(BaseModel):
    pump_info: PumpInfo
    impeller: Impeller
    base_plate: BasePlate
    options: Options
    test_documentation: TestDocumentation