"""
Backfill list_price on catalog PumpConfigs.

The workbook's Config Info tab carries no per-pump price, so catalog configs
were imported with list_price = NULL (and therefore showed no price and could
not be ordered). This computes a transparent, deterministic price from the
pump's motor HP, size and material:

    list_price = BASE + (HP * PER_HP) + MATERIAL_SURCHARGE

Admins can override any value later via the dashboard. Re-running only fills
configs whose price is still NULL (use --force to recompute all).
"""

from __future__ import annotations

import asyncio
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise import Tortoise  # noqa: E402
from src.database import TORTOISE_ORM  # noqa: E402
from src.models import PumpConfig  # noqa: E402

BASE = Decimal("1200")
PER_HP = Decimal("18")
MATERIAL_SURCHARGE = {
    "cast iron": Decimal("0"),
    "ductile iron": Decimal("450"),
    "(22) ductile iron": Decimal("600"),
}
_CENTS = Decimal("0.01")


def _hp(motor) -> Decimal:
    try:
        return Decimal(str(motor.power_hp).split()[0])
    except Exception:
        return Decimal("0")


def _material_surcharge(pump_info) -> Decimal:
    key = (pump_info.pump_material or "").strip().lower()
    return MATERIAL_SURCHARGE.get(key, Decimal("200"))


def _price(config) -> Decimal:
    total = BASE + _hp(config.motor) * PER_HP + _material_surcharge(config.pump_info)
    return total.quantize(_CENTS, rounding=ROUND_HALF_UP)


async def main(force: bool = False) -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    try:
        configs = await PumpConfig.filter(is_catalog=True).prefetch_related(
            "pump_info", "motor"
        )
        updated = skipped = 0
        for cfg in configs:
            if cfg.list_price is not None and not force:
                skipped += 1
                continue
            cfg.list_price = _price(cfg)
            await cfg.save()
            updated += 1
            print(f"  {cfg.name:50} -> ${cfg.list_price}")
        print(f"\nDone: {updated} priced, {skipped} left untouched (already had a price).")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main(force="--force" in sys.argv))
