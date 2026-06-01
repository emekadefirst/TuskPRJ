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
    "base_plate_id" CHAR(36) NOT NULL REFERENCES "base_plates" ("id") ON DELETE CASCADE,
    "impeller_id" CHAR(36) NOT NULL REFERENCES "impellers" ("id") ON DELETE CASCADE,
    "options_id" CHAR(36) NOT NULL REFERENCES "options" ("id") ON DELETE CASCADE,
    "pump_info_id" CHAR(36) NOT NULL REFERENCES "pump_infos" ("id") ON DELETE CASCADE,
    "test_documentation_id" CHAR(36) NOT NULL REFERENCES "test_documentations" ("id") ON DELETE CASCADE
) /* Aggregate model that links all pump component models together via */;
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
