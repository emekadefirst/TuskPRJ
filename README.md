# TUSK Pump Configurator — Technical Documentation

This document explains the entire backend system file by file: the data models,
the repositories (business logic), the API routes, the database/ORM setup,
authentication, the pricing engine, the data-import scripts, and the build/run
workflow. The two frontend files (`index.html` and `dashboard.html`) are
intentionally excluded as requested.

---

## 1. What the application does

The system is an API + thin web client for **ordering industrial pumps**. There
are two ways to obtain a pump configuration:

1. **Catalog** — ready-made, validated pump configurations imported from an
   Excel workbook (`pump_configurator_updated_with_prices.xlsx`). Each is
   orderable as-is.
2. **Custom build** — an admin/user assembles a configuration from individual
   validated components (pump body, seal, motor, and optionally impeller, base
   plate, options, test documentation).

A configuration (`PumpConfig`) ties those components together, carries a
`list_price`, and can be placed on an `Order`. Pricing is **always set by the
server** — clients can never set their own price. There is also a separate,
configurable **quote engine** (base price + options − discount + tax) that
mirrors the original spreadsheet's pricing math.

### Technology stack

| Concern            | Choice                                             |
|--------------------|----------------------------------------------------|
| Web framework      | FastAPI                                            |
| ORM                | Tortoise ORM                                       |
| Migrations         | Aerich                                             |
| Database           | SQLite (`tuskdb.sqlite3`)                           |
| Auth               | JWT in an httponly cookie, Argon2 password hashing |
| Validation         | Pydantic v2                                        |
| Excel import       | openpyxl                                           |
| Server             | Uvicorn                                            |
| Dependency manager | uv (`pyproject.toml` + `uv.lock`)                  |

---

## 2. Project layout

```
mustapha/
├── main.py                       # FastAPI app: routers, CORS, DB init, static HTML
├── pyproject.toml                # dependencies + aerich config
├── tuskdb.sqlite3                # SQLite database file
├── Command.md                    # developer command cheat-sheet (run/migrate)
├── index.html                    # user-facing catalog + order UI (not documented here)
├── dashboard.html                # admin CRUD dashboard (not documented here)
├── pump_configurator_updated_with_prices.xlsx   # source data workbook
├── migrations/
│   └── models/
│       └── 0_20260602153347_init.py   # Aerich initial schema migration
├── scripts/
│   ├── import_workbook.py        # one-shot: workbook -> DB (catalog + price lists)
│   └── backfill_prices.py        # one-shot: compute list_price for catalog configs
└── src/
    ├── database.py               # TORTOISE_ORM config dict
    ├── models.py                 # Tortoise ORM models (DB tables)
    ├── schemas.py                # Pydantic request/response schemas
    ├── repo.py                   # repositories = all business logic + serialization
    ├── api.py                    # FastAPI routers for the pump/order/pricing domain
    ├── auth.py                   # JWT service, password hashing, FastAPI deps
    ├── auth_router.py            # /auth and /users routes
    └── auth_schemas.py           # Pydantic schemas for auth
```

### Architecture in one line

`HTTP request → router (api.py / auth_router.py) → repository (repo.py) → model
(models.py) → SQLite`, with Pydantic schemas (`schemas.py` / `auth_schemas.py`)
validating input and the repositories shaping the JSON responses.

---

## 3. `main.py` — application entry point

This file builds the FastAPI application and wires everything together.

- **Creates the app**: `app = FastAPI(title="TUSK API")`.
- **Registers every router** (order matters only for Swagger grouping):
  `auth_router`, `users_router`, `pump_info_router`, `seal_router`,
  `motor_router`, `impeller_router`, `base_plate_router`, `options_router`,
  `test_documentation_router`, `pump_config_router`, `order_router`,
  `pricing_router`.
- **Initializes the database** via `register_tortoise(...)` with the
  `TORTOISE_ORM` config from `src/database.py`. Crucially:
  - `generate_schemas=False` — the app never creates tables at runtime; schema
    is owned by Aerich migrations.
  - `add_exception_handlers=True` — Tortoise's `DoesNotExist` / `IntegrityError`
    are turned into clean HTTP errors.
- **CORS middleware**: allows `localhost`/`127.0.0.1` on any port (via
  `allow_origin_regex`) plus an explicit allow-list, and `"null"` so the UI
  works when opened from `file://` (browsers send `Origin: null`).
  `allow_credentials=True` is required so the auth cookie is sent on
  cross-origin requests.
- **`GET /health`**: returns `{"message": "Up and running"}` — a simple liveness
  probe the frontend uses to show the "connected" indicator.
- **Static HTML serving**:
  - `GET /` → returns `index.html`
  - `GET /dashboard` and `GET /dashboard.html` → returns `dashboard.html`
  - These are `include_in_schema=False`, so they don't clutter Swagger.

> Note: serving the HTML from the same origin as the API is deliberate — it
> means the auth cookie flows automatically with each API call without CORS
> complications.

---

## 4. `src/database.py` — ORM configuration

Defines the single `TORTOISE_ORM` dictionary consumed both by the running app
(`main.py`) and by Aerich (`pyproject.toml` points aerich at
`main.TORTOISE_ORM`).

```python
TORTOISE_ORM = {
    "connections": {"default": "sqlite://tuskdb.sqlite3"},
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Africa/Lagos",
}
```

Key points:
- **Connection**: a local SQLite file `tuskdb.sqlite3`.
- **Model discovery**: Tortoise loads models from `src.models` plus
  `aerich.models` (the latter is the `aerich` migration-history table).
- **`use_tz=True` + `timezone="Africa/Lagos"`**: datetimes are timezone-aware
  and rendered in West Africa Time.

---

## 5. `src/models.py` — database models

All tables use **Tortoise ORM**. Every model inherits from `BaseModel`.

### 5.1 `BaseModel` (abstract)

Shared columns for every table:
- `id` — `UUIDField` primary key, default `uuid.uuid4` (stored as `CHAR(36)`).
- `created_at` — `DatetimeField(auto_now_add=True)` (set once at insert).
- `updated_at` — `DatetimeField(auto_now=True)` (refreshed on every save).
- `class Meta: abstract = True` so no table is created for it directly.

### 5.2 `User` → table `users`
`first_name`, `last_name`, `email`, `password` — all `CharField(255)`. The
`password` column stores an **Argon2 hash**, never plaintext.

### 5.3 `PumpInfo` → table `pump_infos`
The pump body specification. Fields:
`series`, `size`, `pump_material`, `shaft_configuration`, `casing_metal`,
`casing_drain`, `casing_tap`, **`casing_gasket`** (default `"Grafoil"`),
`flange_configuration`, `spot_facing` (default `"Not required"`),
`casing_wear_ring`, `tack_weld_wear_ring`, `casing_mounting`, `hardware`
(nullable), `seal_chamber_config`, `shipping_gasket`, `cradle_material`
(nullable).

> `casing_gasket` was added specifically because the workbook's Config Info tab
> lists it as a core column.

### 5.4 `Seal` → table `seals`
Mechanical seal selection, mirroring the workbook's "Mechanical Seals" block and
"Seal Descriptions" tab. Fields:
`seal_option` (default `"Included"`), `seal_mfr` (nullable),
`seal_configuration`, `seal_type`, `gland_type`/`gland_gasket`/
`shaft_sleeve_material` (default `"NONE"`), the inboard face/elastomer trio
(`inboard_rotating_face`, `inboard_stationary_face`, `inboard_elastomer`), and
the outboard trio (`outboard_*`, default `"N/A"`).

### 5.5 `Motor` → table `motors`
Motor selection, from the workbook's "Motor Options" block plus Config Info's
HP/Speed/Voltage. Fields:
`motor_control` (default `"N/A"`), `power_hp`, `speed`, `voltage`,
`phase_hertz` (default `"3PH / 60Hz"`), `frame` (nullable), `enclosure`
(default `"TEFC"`), `efficiency` (default `"Premium"`), `c_face_adapter`
(default `"N/A"`), `manufacturer` (default `"N/A"`).

### 5.6 `Impeller` → table `impellers`
`impeller_range`, `impeller_trim`, `impeller_balance`, `impeller_material`,
`impeller_wear_ring_material`.

### 5.7 `BasePlate` → table `base_plates`
`baseplate_type`, `baseplate_material`, `drip_pan`, plus a set of options that
default to `"Not required"`: `allignment_lugs`, `lifting_lugs`,
`leveling_screws`, `grounding_lugs`, `grout_hole`, `isolation_pads`, `stilts`.

### 5.8 `Options` → table `options`
`coupling_type`, `coupling_guard`, `auxillary_nameplate`, `crating`,
`oil_options`, `bearing_frame_cooling`, `lubrication_options`, `oil_seat`,
`sight_gauge`, `magnetic_drain`, `expansion_chamber`.

### 5.9 `TestDocumentation` → table `test_documentations`
`performance_testing`, `hydro_testing`, `vibration`, `sound_level`,
`general_inspection`, and `documenttation_1` … `documenttation_6`.

### 5.10 `PumpConfig` → table `pump_configs` (the aggregate)
Ties the component models together into a single orderable configuration.

Own columns:
- `name` (nullable) — human label; for catalog rows this is the workbook's
  "Configuration ID" (e.g. `PH2110 | 4x6x8.5 | Single Component | Type 21`).
- `notes` (nullable `TextField`).
- `is_catalog` (`BooleanField`, default `False`) — distinguishes ready-made
  catalog entries from user-built configs.
- `list_price` (`DecimalField(12,2)`, **nullable**) — the price the server
  charges per unit when ordered.

Foreign keys:
- **Required**: `pump_info`, `seal`, `motor` — every config must have a body,
  seal and motor.
- **Optional (nullable)**: `impeller`, `base_plate`, `options`,
  `test_documentation` — a config can exist with just the core three. This is
  essential because the workbook only provides body/seal/motor data per row.

All FKs use `on_delete=CASCADE` and `related_name="pump_config"`.

> **Why some FKs are nullable**: the original schema required all five
> components. The workbook's Config Info only supplies pump body + seal + motor,
> so requiring impeller/baseplate/etc. would have made catalog import
> impossible. Making them nullable lets both catalog and partial custom configs
> exist.

### 5.11 `Order` → table `orders`
A purchase order placed by a user.
- `user` FK → `users` (`related_name="orders"`, `on_delete=CASCADE`).
- `status` — `CharField(32)`, default `"pending"`. Valid values declared in
  `STATUSES = ("pending", "confirmed", "shipped", "delivered", "cancelled")`.
- `notes`, `shipping_address` — nullable `TextField`s.
- `total` — `DecimalField(12,2)`, default `0`. The order total is **snapshotted**
  at creation so historical orders don't change if prices later move.

### 5.12 `OrderItem` → table `order_items`
A single line on an order.
- `order` FK → `orders` (`related_name="items"`, `on_delete=CASCADE`).
- `pump_config` FK → `pump_configs` (`related_name="order_items"`,
  `on_delete=RESTRICT`) — `RESTRICT` prevents deleting a config that an order
  still references.
- `quantity` — `IntField`, default `1`.
- `unit_price` — `DecimalField(12,2)`, default `0`. Set by the server from the
  config's `list_price` at order time.

### 5.13 `PriceList` → table `price_lists`
Base price per product family + size, sourced from the workbook's "Price Lists"
tab (left block).
- `product_family`, `size`, `base_price` (`DecimalField(12,2)`).
- `unique_together = (("product_family", "size"),)` — one base price per combo.

### 5.14 `OptionPrice` → table `option_prices`
Per-option add-on price, from the "Price Lists" tab (middle block).
- `field` (e.g. `"Material"`, `"Voltage"`), `option` (e.g. `"Steel"`, `"240V"`),
  `option_price` (`DecimalField(12,2)`).
- `unique_together = (("field", "option"),)`.

> `PriceList` and `OptionPrice` feed the **quote engine** (see PricingRepo).
> They are a separate, generic pricing system inherited from the workbook's "PX
> Configurator" demo and are independent of the pump catalog's `list_price`.

---

## 6. `src/schemas.py` — Pydantic schemas

These define the **shape of request bodies and some responses**. Pattern: each
resource has a `XSchema` (create — required fields) and an `XUpdateSchema`
(patch — all optional). Built on Pydantic v2.

- **`UserCreateSchema` / `UserUpdateSchema`** — `first_name`, `last_name`,
  `email` (`EmailStr`), `password`.
- **`PumpInfoSchema` / `PumpInfoUpdateSchema`** — all pump body fields;
  includes `casing_gasket` (default `"Grafoil"`). The update variant makes
  every field `Optional[...] = None` so partial PATCH works.
- **`SealSchema` / `SealUpdateSchema`** — seal fields; required ones are
  `seal_configuration`, `seal_type`, and the inboard face/elastomer trio. The
  rest carry workbook-style defaults (`"Included"`, `"NONE"`, `"N/A"`).
- **`MotorSchema` / `MotorUpdateSchema`** — required `power_hp`, `speed`,
  `voltage`; the rest default to spreadsheet values.
- **`ImpellerSchema`, `BasePlateSchema`, `OptionSchema`,
  `TestDocumentationSchema`** (+ their update variants) — straightforward field
  mirrors of the corresponding models.
- **`PumpConfigSchema`** (create):
  - Required: `pump_info_id`, `seal_id`, `motor_id`.
  - Optional: `impeller_id`, `base_plate_id`, **`option_id`** (note: singular,
    mapped to the model column `options_id` in the repo),
    `test_documentation_id`.
  - Plus `name`, `notes`, `is_catalog` (default `False`), `list_price`
    (`Optional[Decimal]`).
- **`PumpConfigUpdateSchema`** — all fields optional, same field names.
- **`PriceListSchema`** — `product_family`, `size`, `base_price`.
- **`OptionPriceSchema`** — `field`, `option`, `option_price`.
- **Quote engine schemas**:
  - `QuoteRequestSchema` — `product_family`, `size`, `options: dict[str,str]`
    (a `{field: option}` map), `quantity (ge=1)`, `discount_pct (0–100)`,
    `tax_rate (0–100)`.
  - `QuoteLineSchema` — one line of the breakdown (`field`, `option`, `price`).
  - `QuoteResponseSchema` — the full quote result (base, options, unit/extended
    list price, discount, subtotal, tax, total, `breakdown`, `warnings`). This
    is used as the `response_model` on the quote endpoint.
- **Order schemas**:
  - `OrderItemSchema` — `pump_config_id`, `quantity (ge=1)`. **`unit_price` is
    deliberately omitted** — the server prices each line so clients can't set
    their own price.
  - `OrderSchema` — `items: list[OrderItemSchema]` (`min_length=1`), optional
    `notes` and `shipping_address`.
  - `OrderUpdateSchema` — optional `status`, `notes`, `shipping_address`.

---

## 7. `src/repo.py` — repositories (business logic)

Repositories encapsulate all database access, validation, and JSON
serialization. Routers stay thin and just call these. Module-level setup:

- `ph = PasswordHasher()` — Argon2 hasher used by `UserRepo`.
- `SAFE_FIELDS` — the user columns safe to return (excludes `password`).

### 7.1 `UserRepo`
- `create(dto)` — rejects duplicate email (409), Argon2-hashes the password,
  inserts the user.
- `fetch(id|email|search)` — returns user(s) using only `SAFE_FIELDS` (password
  never leaks). `search` does a case-insensitive OR across id/email/names.
- `update(id, dto)` — `model_dump(exclude_unset=True)` so only provided fields
  change; re-hashes password if present; guards against email collisions; 404
  if missing.
- `delete(id)` — 404 if missing, else hard-delete.

### 7.2 Component repositories
`PumpInfoRepo`, `SealRepo`, `MotorRepo`, `ImpellerRepo`, `BasePlateRepo`,
`OptionsRepo`, `TestDocumentationRepo` all follow an identical CRUD pattern:

- `create(dto)` — `Model.create(**dto.dict())`.
- `delete(id)` — 404 if not found, else delete.
- `fetch(id|search)` — single by id, or an OR-filtered `__icontains` search
  across that model's text columns, or all rows.
- `update(id, data)` — `update_from_dict(model_dump(exclude_unset=True))` then
  `save()`; returns the row or `None` (the router converts `None` to 404).

### 7.3 Pump-config pricing helpers (module-level)
Defined just above `PumpConfigRepo`:

- `compute_config_price(config)` — deterministic list price for a configuration:
  ```
  list_price = BASE(1200) + HP * PER_HP(18) + material_surcharge
  ```
  - HP is parsed from `motor.power_hp` (e.g. `"75"` → `75`).
  - Material surcharge: `cast iron → 0`, `ductile iron → 450`,
    `(22) ductile iron → 600`, anything else → `200`.
  - Result is quantized to cents, `ROUND_HALF_UP`.
  - **Kept in sync with `scripts/backfill_prices.py`** (same constants).
- `money_str(value)` — formats a stored decimal as a plain 2-dp string
  (e.g. `"3150.00"`), avoiding SQLite's scientific-notation artifacts like
  `3.15E+3`. Used throughout serialization.

### 7.4 `PumpConfigRepo`
The most involved repository because it manages the aggregate + nested objects.

- `_model_to_dict(obj)` — turns any related Tortoise row into a plain dict over
  its `_meta.db_fields`, stringifying UUIDs/datetimes for uniform JSON.
- `_serialize(config)` — returns the full config dict: own fields (`id`, `name`,
  `notes`, `is_catalog`, `list_price` via `money_str`, timestamps) plus the
  seven nested component dicts (`pump_info`, `seal`, `motor`, `impeller`,
  `base_plate`, `options`, `test_documentation`).
- `create(dto)`:
  1. Inserts the config. Note the schema's `option_id` maps to the model's
     `options_id` column.
  2. `fetch_related(...)` to load all nested objects.
  3. **Auto-pricing**: if no `list_price` was supplied, computes one via
     `compute_config_price` and saves it — so user-built configs are orderable
     just like catalog ones.
  4. Returns the serialized config.
- `delete(id)` — 404 if missing, else delete.
- `fetch(id=None, catalog=None, search=None)`:
  - With `id`: returns one serialized config (with relations) or `None`.
  - Otherwise: lists configs, optionally filtered by `is_catalog` (the
    **catalog filter**) and/or a `search` across name/notes/series/size,
    ordered by `name`, each fully serialized.
- `update(id, data)` — partial update; remaps `option_id → options_id`; reloads
  relations; returns the serialized config (or `None` → 404).

### 7.5 `OrderRepo`
- `_serialize_item(item)` — line dict: `quantity`, `unit_price`, computed
  `subtotal` (both via `money_str`), and the nested `pump_config`.
- `_serialize(order)` — order dict: `status`, `notes`, `shipping_address`,
  `total` (via `money_str`), `user_id`, and the list of serialized items.
- `create(user, dto)` — **the price-authority step**:
  1. Loads all referenced configs and builds a `price_by_id` map from each
     config's `list_price` (or `0` if null).
  2. Rejects unknown config ids → **400**.
  3. Rejects any config with price `<= 0` → **409** ("an administrator must set
     a list price"). This guarantees no $0 orders slip through.
  4. Computes the order `total` from server prices × quantities.
  5. Inside an `in_transaction()`, creates the `Order` and each `OrderItem`,
     stamping `unit_price` from the server map (any client-sent price is
     ignored — the schema doesn't even accept it).
  6. Returns the freshly fetched, serialized order.
- `fetch(user=None, id=None, search=None)` — scoped to `user` when provided
  (users only see their own orders). Deeply `prefetch_related`s every nested
  component (including `seal` and `motor`) so serialization never lazy-loads.
  List results are ordered newest-first; `search` matches status/notes.
- `update(user, id, dto)` — validates `status` against `VALID_STATUSES`
  (400 otherwise); applies the partial update; returns the refreshed order.
- `delete(user, id)` — 404 if not owned/found, else delete.

### 7.6 `PricingRepo` (the quote engine)
Backed by `PriceList` + `OptionPrice`. Helpers `_money()` and `_CENTS` round to
cents half-up.

- `list_base_prices()` / `list_option_prices()` — ordered listings.
- `upsert_base_price(dto)` / `upsert_option_price(dto)` — `update_or_create`
  keyed on the natural unique key, so re-posting edits in place.
- `quote(dto)` — mirrors the workbook's "PX Configurator" math:
  1. Look up the base price for `(product_family, size)` → 404 if none.
  2. For each selected `{field: option}`, add its `OptionPrice`. Unknown options
     don't error — they're priced `0` and noted in `warnings`.
  3. Compute:
     ```
     unit_list       = base_price + Σ option_prices
     extended        = unit_list * quantity
     discount_amount = extended * discount_pct/100
     subtotal        = extended - discount_amount
     tax             = subtotal * tax_rate/100
     total           = subtotal + tax
     ```
  4. Returns every line of the calculation plus an itemized `breakdown` and any
     `warnings`. (Verified to reproduce the workbook's example total of
     **$919.93**.)

---

## 8. `src/api.py` — domain routers

Thin FastAPI routers that validate input via schemas and delegate to
repositories. Standard CRUD shape per resource:

```
POST   /<resource>/        -> create        (201)
GET    /<resource>/        -> list          (optional ?search=)
GET    /<resource>/{id}    -> single        (404 if missing)
PATCH  /<resource>/{id}    -> partial update (404 if missing)
DELETE /<resource>/{id}    -> delete        (204)
```

Routers and prefixes:
- `pump_info_router` → `/pump-info`
- `seal_router` → `/seal`
- `motor_router` → `/motor`
- `impeller_router` → `/impeller`
- `base_plate_router` → `/base-plate`
- `options_router` → `/options`
- `test_documentation_router` → `/test-documentation`
- `pump_config_router` → `/pump-config`
- `order_router` → `/orders` (auth-protected)
- `pricing_router` → `/pricing`

### Notable, non-generic endpoints

- **`GET /pump-config/`** accepts two query params:
  - `catalog` (`bool`) — `true` returns only catalog configs, `false` only
    custom; omitted returns all.
  - `search` (`str`) — name/notes/series/size match.
- **Orders** (`/orders`) — every endpoint depends on `get_current_user`, so a
  valid auth cookie is required, and all queries are **scoped to that user**.
  - `POST /orders/` — create from `OrderSchema` (server prices it).
  - `GET /orders/` — list the current user's orders (optional `?search=`).
  - `GET /orders/{id}`, `PATCH /orders/{id}`, `DELETE /orders/{id}`.
- **Pricing** (`/pricing`):
  - `GET /pricing/base-prices`, `POST /pricing/base-prices` (upsert).
  - `GET /pricing/option-prices`, `POST /pricing/option-prices` (upsert).
  - `POST /pricing/quote` — runs the quote engine; `response_model` is
    `QuoteResponseSchema`.
  - **Note**: these base/option-price routes are **not** mounted with a trailing
    `/{id}` and have no PATCH/DELETE — they are list + upsert only.

> **Security note**: the component CRUD routes (`/pump-info`, `/seal`, etc.) and
> the `/pricing` write routes are currently **unauthenticated**. Only `/orders`
> and `/users` require login. In a production deployment these admin-style write
> endpoints should be placed behind an auth/role check.

---

## 9. Authentication

### 9.1 `src/auth.py`
The auth toolkit. (Constants are hard-coded for the prototype — there's no
`.env`.)

- **Config constants**: `JWT_SECRET`, `JWT_ALGORITHM = "HS256"`,
  `ACCESS_TOKEN_TTL_MIN = 60*24` (24h), and cookie settings
  (`COOKIE_NAME = "access_token"`, `httponly=True`, `samesite="lax"`,
  `secure=False` for local dev).
- **Password hashing**: `hash_password()` / `verify_password()` wrap Argon2.
  `verify_password` returns `False` on mismatch rather than raising.
- **`JWTService`**:
  - `generate_token(subject, extra_claims)` — builds a JWT with `sub` (user id),
    `iat`, `exp`, plus extra claims (email, names).
  - `decode_token(token)` — decodes/validates; raises **401** on expired or
    invalid tokens.
  - `verify_token(token)` — boolean check, no raise.
  - `set_cookie` / `clear_cookie` — manage the httponly auth cookie.
  - `issue(response, user)` — convenience: generate token + set cookie.
- **FastAPI dependencies**:
  - `get_current_user` — reads the cookie, decodes it, loads the `User`; raises
    401 if missing/invalid/unknown. This is the guard used on `/orders` and
    `/users`.
  - `get_current_user_optional` — same but returns `None` instead of raising.
  - `CurrentUser = Annotated[User, Depends(get_current_user)]` — a reusable
    dependency alias.

### 9.2 `src/auth_router.py`
- **`auth_router`** (`/auth`):
  - `POST /auth/register` — 409 on duplicate email; creates user with a hashed
    password; issues a cookie; returns `AuthResponse`.
  - `POST /auth/login` — verifies credentials (401 on failure); issues a cookie.
  - `POST /auth/logout` — clears the cookie.
  - `GET /auth/me` — returns the current user (requires `CurrentUser`).
- **`users_router`** (`/users`) — admin-style user browsing; every route
  requires a logged-in user:
  - `GET /users/` — list users (optional `?search=` across names/email).
  - `GET /users/{id}` — single user (404 if missing).
  - `DELETE /users/{id}` — delete a user, but **400 if you try to delete your
    own account**.
  - `_user_to_dict` ensures the password is never serialized.

### 9.3 `src/auth_schemas.py`
- `RegisterSchema` — validated `first_name`/`last_name` (1–100 chars),
  `email` (`EmailStr`), `password` (6–255 chars).
- `LoginSchema` — `email`, `password`.
- `UserPublic` — safe public view (`id`, `first_name`, `last_name`, `email`)
  with a `from_user()` constructor.
- `AuthResponse` — `{ user: UserPublic, message: str }`.

---

## 10. Migrations — `migrations/models/`

Schema is managed by **Aerich** (configured in `pyproject.toml` under
`[tool.aerich]`, pointing at `main.TORTOISE_ORM`).

- The current schema lives in `0_20260602153347_init.py` — the initial
  migration generated after the models reached their final shape (it contains
  `users`, `pump_infos`, `seals`, `motors`, `impellers`, `base_plates`,
  `options`, `test_documentations`, `pump_configs`, `orders`, `order_items`,
  `price_lists`, `option_prices`, plus the `aerich` history table).

> **Why the schema was regenerated**: SQLite cannot `ALTER COLUMN` to change a
> `NOT NULL` constraint in place. When the `PumpConfig` FKs to
> impeller/baseplate/options/test_documentation were made nullable (and seal +
> motor added), Aerich's incremental `migrate` failed on SQLite. Because the
> database was empty at the time, the clean fix was to delete the empty DB and
> the stale init migration, then run `aerich init-db` to regenerate the full
> schema from the final models.

Day-to-day commands (also in `Command.md`):
```
aerich migrate --name <change>   # generate a migration after editing models
aerich upgrade                   # apply pending migrations
aerich downgrade                 # roll back the last migration
aerich history                   # view migration history
```

---

## 11. Data scripts — `scripts/`

These are one-shot maintenance scripts run with the project's Python
(`.venv/Scripts/python.exe scripts/<name>.py`). Both init Tortoise directly with
`TORTOISE_ORM` and close connections when done.

### 11.1 `scripts/import_workbook.py`
Loads `pump_configurator_updated_with_prices.xlsx` into the database using
**openpyxl**. It is **idempotent**.

- **`Config Info` sheet → catalog configs**: for each row it creates a
  `PumpInfo` (body columns incl. `casing_gasket`), a `Seal` (config/type +
  inboard faces/elastomer), and a `Motor` (HP/speed/voltage), then a catalog
  `PumpConfig` with `is_catalog=True`, `name` = the Configuration ID, `notes` =
  the Notes column, and `list_price=None` (the sheet has no per-config price).
  Existing configs (matched by `name` + `is_catalog`) are skipped, so re-running
  never duplicates.
- **`Price Lists` sheet → pricing tables**: the left block (`Product Family`,
  `Size`, `Base Price`) populates `PriceList`; the middle block (`Field`,
  `Option`, `Option Price`) populates `OptionPrice`. Both use
  `update_or_create` on their natural keys.
- Helpers `_s()` (trim/normalize cells to `str|None`) and `_dec()` (safe
  `Decimal`) guard against blank/None cells.
- Result of the import: **17 catalog configs, 9 price-list rows, 20
  option-price rows**.

### 11.2 `scripts/backfill_prices.py`
Because Config Info carries no per-pump price, catalog configs imported with
`list_price = NULL` and therefore couldn't be ordered or show a price. This
script computes a transparent, deterministic price:

```
list_price = BASE(1200) + HP * PER_HP(18) + MATERIAL_SURCHARGE
```

- Material surcharge map matches `repo.compute_config_price` exactly
  (`cast iron 0`, `ductile iron 450`, `(22) ductile iron 600`, default `200`).
- Only fills configs whose `list_price` is still `NULL`, unless run with
  `--force` to recompute all. Admins can override any value afterward via the
  dashboard.
- The resulting catalog prices range roughly **$1,920 – $4,350**.

> The pricing formula is intentionally duplicated in both `repo.py`
> (`compute_config_price`, used live when a custom config is created) and this
> script (used for bulk backfill). If you change one, change the other.

---

## 12. End-to-end flows

### 12.1 Browse & order a catalog pump
1. User signs in → `POST /auth/login` sets the auth cookie.
2. UI calls `GET /pump-config/?catalog=true` → list of priced catalog configs.
3. User picks one and `POST /orders/` with `{ items: [{ pump_config_id, quantity }] }`.
4. `OrderRepo.create` looks up the config's `list_price`, rejects unpriced ones
   (409), computes the total server-side, and stores the order + items inside a
   transaction. The client cannot influence price.

### 12.2 Build a custom config (admin/dashboard)
1. Create the required components (`POST /pump-info`, `/seal`, `/motor`) and any
   optional ones.
2. `POST /pump-config/` with the component ids and `is_catalog=false`.
3. `PumpConfigRepo.create` inserts it and, if no `list_price` was given,
   auto-computes one via `compute_config_price` so it's immediately orderable.

### 12.3 Get a configurable quote
`POST /pricing/quote` with a product family/size, an `{field: option}` map,
quantity, discount % and tax % → returns the full base/options/discount/tax/
total breakdown. Backed by the `PriceList` / `OptionPrice` tables that admins
maintain via `POST /pricing/base-prices` and `POST /pricing/option-prices`.

---

## 13. Running the project

```bash
# 1. Install dependencies (uv reads pyproject.toml / uv.lock)
uv sync

# 2. Apply the database schema
aerich upgrade            # or: aerich init-db on a fresh project

# 3. (first time) load the workbook data
.venv/Scripts/python.exe scripts/import_workbook.py
.venv/Scripts/python.exe scripts/backfill_prices.py

# 4. Run the server
uvicorn main:app --reload
```

- API docs (Swagger): `http://127.0.0.1:8000/docs`
- User catalog UI: `http://127.0.0.1:8000/`
- Admin dashboard: `http://127.0.0.1:8000/dashboard`

---

## 14. Design decisions & invariants (summary)

- **Server is the single source of truth for price.** `OrderItemSchema` has no
  `unit_price` field; `OrderRepo.create` always prices from the config's
  `list_price`. Unpriced configs cannot be ordered (409).
- **Money is always formatted to 2 dp** on output via `money_str` / `_money` to
  avoid SQLite scientific-notation artifacts.
- **Order totals are snapshotted** at creation so past orders are stable when
  prices change.
- **`PumpConfig` requires body/seal/motor; other components are optional** to
  match the data the workbook actually provides.
- **Two independent pricing systems coexist**: per-config `list_price` (what you
  pay for a pump) and the `PriceList`/`OptionPrice` quote engine (a configurable
  estimator carried over from the spreadsheet).
- **Schema is migration-owned** (`generate_schemas=False`); the app never
  mutates the schema at runtime.
- **Repositories own all logic**; routers are thin pass-throughs; schemas
  validate I/O.
```
 