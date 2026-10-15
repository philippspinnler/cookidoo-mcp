import asyncio
from types import SimpleNamespace as NS

import server


class FakeRecipeApi:
    async def get_recipe_details(self, recipe_id):
        nutrition = NS(type="kcal", number=232, unittype="kcal")
        per = NS(quantity=1, unit_notation="Portion", nutritions=[nutrition])
        return NS(
            id=recipe_id,
            name="Kartoffelstock",
            total_time=3300,
            ingredients=[],
            nutrition_groups=[NS(name="", recipe_nutritions=[per])],
        )


def test_recipe_details_show_minutes_and_nutrition(monkeypatch):
    monkeypatch.setattr(server, "_cookidoo_api", FakeRecipeApi())

    result = asyncio.run(server.get_recipe_details("r794911"))

    assert "Total Time: 55 minutes" in result
    assert "Nutrition (per 1 Portion):\n  • kcal: 232 kcal" in result
