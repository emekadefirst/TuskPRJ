# Developer Commands Reference

---

## Run Server

```bash
uvicorn main:app --reload
```

---

## Migrations with Aerich

Aerich is the official migration tool for Tortoise ORM.
It reads the `TORTOISE_ORM` config dict exported from `main.py`.

### 1. Initialise Aerich — run once per project

Creates `pyproject.toml` aerich config and a `migrations/` folder.

```bash
aerich init -t main.TORTOISE_ORM
```

> `-t` points aerich at the Tortoise config object: `<module>.<variable>`.

---

### 2. Create the initial migration — run once after init

Inspects all models and generates the first SQL schema file
inside `migrations/models/`.

```bash
aerich init-db
```

---

### 3. Generate a new migration — run after every model change

Diffs the current models against the last migration and writes
a new versioned SQL file.

```bash
aerich migrate --name <short_description>
```

**Examples:**

```bash
aerich migrate --name add_pump_series_index
aerich migrate --name add_impeller_balance_field
```

---

### 4. Apply pending migrations — run to push changes to the database

```bash
aerich upgrade
```

---

### 5. Roll back the last applied migration

```bash
aerich downgrade
```

---

### 6. Inspect migration history

```bash
aerich history
```

---

## Full First-Time Setup (in order)

```bash
# 1. Install dependencies
pip install fastapi uvicorn tortoise-orm aerich

# 2. Point aerich at the Tortoise config
aerich init -t main.TORTOISE_ORM

# 3. Generate the initial SQL schema from your models
aerich init-db

# 4. Start the server
uvicorn main:app --reload
```

---

## Typical Day-to-Day Workflow

```bash
# After changing a model
aerich migrate --name describe_your_change
aerich upgrade

# Then restart the server
uvicorn main:app --reload
```