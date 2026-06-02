from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "base_plates" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "baseplate_type" VARCHAR(255) NOT NULL,
    "baseplate_material" VARCHAR(255) NOT NULL,
    "drip_pan" VARCHAR(255) NOT NULL,
    "allignment_lugs" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "lifting_lugs" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "leveling_screws" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "grounding_lugs" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "grout_hole" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "isolation_pads" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "stilts" VARCHAR(255) NOT NULL DEFAULT 'Not required'
);
CREATE TABLE IF NOT EXISTS "impellers" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "impeller_range" VARCHAR(255) NOT NULL,
    "impeller_trim" VARCHAR(255) NOT NULL,
    "impeller_balance" VARCHAR(255) NOT NULL,
    "impeller_material" VARCHAR(255) NOT NULL,
    "impeller_wear_ring_material" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "motors" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "motor_control" VARCHAR(255) NOT NULL DEFAULT 'N/A',
    "power_hp" VARCHAR(255) NOT NULL,
    "speed" VARCHAR(255) NOT NULL,
    "voltage" VARCHAR(255) NOT NULL,
    "phase_hertz" VARCHAR(255) NOT NULL DEFAULT '3PH / 60Hz',
    "frame" VARCHAR(255),
    "enclosure" VARCHAR(255) NOT NULL DEFAULT 'TEFC',
    "efficiency" VARCHAR(255) NOT NULL DEFAULT 'Premium',
    "c_face_adapter" VARCHAR(255) NOT NULL DEFAULT 'N/A',
    "manufacturer" VARCHAR(255) NOT NULL DEFAULT 'N/A'
) /* Motor selection. Mirrors the Motor Options block of the Data Sheet plus the */;
CREATE TABLE IF NOT EXISTS "option_prices" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "field" VARCHAR(255) NOT NULL,
    "option" VARCHAR(255) NOT NULL,
    "option_price" VARCHAR(40) NOT NULL DEFAULT 0,
    CONSTRAINT "uid_option_pric_field_04fc9e" UNIQUE ("field", "option")
) /* Per-option add-on price. */;
CREATE TABLE IF NOT EXISTS "options" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "coupling_type" VARCHAR(255) NOT NULL,
    "coupling_guard" VARCHAR(255) NOT NULL,
    "auxillary_nameplate" VARCHAR(255) NOT NULL,
    "crating" VARCHAR(255) NOT NULL,
    "oil_options" VARCHAR(255) NOT NULL,
    "bearing_frame_cooling" VARCHAR(255) NOT NULL,
    "lubrication_options" VARCHAR(255) NOT NULL,
    "oil_seat" VARCHAR(255) NOT NULL,
    "sight_gauge" VARCHAR(255) NOT NULL,
    "magnetic_drain" VARCHAR(255) NOT NULL,
    "expansion_chamber" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "price_lists" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "product_family" VARCHAR(255) NOT NULL,
    "size" VARCHAR(255) NOT NULL,
    "base_price" VARCHAR(40) NOT NULL DEFAULT 0,
    CONSTRAINT "uid_price_lists_product_12a779" UNIQUE ("product_family", "size")
) /* Base price for a product family + size combination. */;
CREATE TABLE IF NOT EXISTS "pump_infos" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "series" VARCHAR(255) NOT NULL,
    "size" VARCHAR(255) NOT NULL,
    "pump_material" VARCHAR(255) NOT NULL,
    "shaft_configuration" VARCHAR(255) NOT NULL,
    "casing_metal" VARCHAR(255) NOT NULL,
    "casing_drain" VARCHAR(255) NOT NULL,
    "casing_tap" VARCHAR(255) NOT NULL,
    "casing_gasket" VARCHAR(255) NOT NULL DEFAULT 'Grafoil',
    "flange_configuration" VARCHAR(255) NOT NULL,
    "spot_facing" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "casing_wear_ring" VARCHAR(255) NOT NULL,
    "tack_weld_wear_ring" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "casing_mounting" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "hardware" VARCHAR(255),
    "seal_chamber_config" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "shipping_gasket" VARCHAR(255) NOT NULL DEFAULT 'Not required',
    "cradle_material" VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS "seals" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "seal_option" VARCHAR(255) NOT NULL DEFAULT 'Included',
    "seal_mfr" VARCHAR(255),
    "seal_configuration" VARCHAR(255) NOT NULL,
    "seal_type" VARCHAR(255) NOT NULL,
    "gland_type" VARCHAR(255) NOT NULL DEFAULT 'NONE',
    "gland_gasket" VARCHAR(255) NOT NULL DEFAULT 'NONE',
    "shaft_sleeve_material" VARCHAR(255) NOT NULL DEFAULT 'NONE',
    "inboard_rotating_face" VARCHAR(255) NOT NULL,
    "inboard_stationary_face" VARCHAR(255) NOT NULL,
    "inboard_elastomer" VARCHAR(255) NOT NULL,
    "outboard_rotating_face" VARCHAR(255) NOT NULL DEFAULT 'N/A',
    "outboard_stationary_face" VARCHAR(255) NOT NULL DEFAULT 'N/A',
    "outboard_elastomer" VARCHAR(255) NOT NULL DEFAULT 'N/A'
) /* Mechanical seal selection. Mirrors the workbook's Mechanical Seals block */;
CREATE TABLE IF NOT EXISTS "test_documentations" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "performance_testing" VARCHAR(255) NOT NULL,
    "hydro_testing" VARCHAR(255) NOT NULL,
    "vibration" VARCHAR(255) NOT NULL,
    "sound_level" VARCHAR(255) NOT NULL,
    "general_inspection" VARCHAR(255) NOT NULL,
    "documenttation_1" VARCHAR(255) NOT NULL,
    "documenttation_2" VARCHAR(255) NOT NULL,
    "documenttation_3" VARCHAR(255) NOT NULL,
    "documenttation_4" VARCHAR(255) NOT NULL,
    "documenttation_5" VARCHAR(255) NOT NULL,
    "documenttation_6" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "pump_configs" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255),
    "notes" TEXT,
    "is_catalog" INT NOT NULL DEFAULT 0,
    "list_price" VARCHAR(40),
    "base_plate_id" CHAR(36) REFERENCES "base_plates" ("id") ON DELETE CASCADE,
    "impeller_id" CHAR(36) REFERENCES "impellers" ("id") ON DELETE CASCADE,
    "motor_id" CHAR(36) NOT NULL REFERENCES "motors" ("id") ON DELETE CASCADE,
    "options_id" CHAR(36) REFERENCES "options" ("id") ON DELETE CASCADE,
    "pump_info_id" CHAR(36) NOT NULL REFERENCES "pump_infos" ("id") ON DELETE CASCADE,
    "seal_id" CHAR(36) NOT NULL REFERENCES "seals" ("id") ON DELETE CASCADE,
    "test_documentation_id" CHAR(36) REFERENCES "test_documentations" ("id") ON DELETE CASCADE
) /* Aggregate model that links pump component models together. */;
CREATE TABLE IF NOT EXISTS "users" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "orders" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(32) NOT NULL DEFAULT 'pending',
    "notes" TEXT,
    "shipping_address" TEXT,
    "total" VARCHAR(40) NOT NULL DEFAULT 0,
    "user_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
) /* A purchase order placed by a user. The total is summed from the line items */;
CREATE TABLE IF NOT EXISTS "order_items" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "quantity" INT NOT NULL DEFAULT 1,
    "unit_price" VARCHAR(40) NOT NULL DEFAULT 0,
    "order_id" CHAR(36) NOT NULL REFERENCES "orders" ("id") ON DELETE CASCADE,
    "pump_config_id" CHAR(36) NOT NULL REFERENCES "pump_configs" ("id") ON DELETE RESTRICT
) /* A single line item on an order: one pump config, with quantity + price. */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
