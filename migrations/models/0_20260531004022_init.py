from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "base_plates" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "impeller_range" VARCHAR(255) NOT NULL,
    "impeller_trim" VARCHAR(255) NOT NULL,
    "impeller_balance" VARCHAR(255) NOT NULL,
    "impeller_material" VARCHAR(255) NOT NULL,
    "impeller_wear_ring_material" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "options" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "base_plate_id" UUID NOT NULL REFERENCES "base_plates" ("id") ON DELETE CASCADE,
    "impeller_id" UUID NOT NULL REFERENCES "impellers" ("id") ON DELETE CASCADE,
    "options_id" UUID NOT NULL REFERENCES "options" ("id") ON DELETE CASCADE,
    "pump_info_id" UUID NOT NULL REFERENCES "pump_infos" ("id") ON DELETE CASCADE,
    "test_documentation_id" UUID NOT NULL REFERENCES "test_documentations" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "pump_configs" IS 'Aggregate model that links all pump component models together via';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "yP/jw7bLvNMoNDs6H2/oeXm/8AiuxcLA=="
)
