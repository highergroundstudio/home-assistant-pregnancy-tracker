"""Size comparison data for pregnancy tracker."""

# Week-by-week veggie comparisons (weeks 1-42)
VEGGIE_COMPARISONS = {
    1: "Poppy seed",
    2: "Sesame seed",
    3: "Peppercorn",
    4: "Lentil",
    5: "Apple seed",
    6: "Sweet pea",
    7: "Blueberry",
    8: "Raspberry",
    9: "Cherry",
    10: "Strawberry",
    11: "Brussels sprout",
    12: "Plum",
    13: "Lemon",
    14: "Peach",
    15: "Apple",
    16: "Avocado",
    17: "Turnip",
    18: "Bell pepper",
    19: "Mango",
    20: "Banana",
    21: "Carrot",
    22: "Papaya",
    23: "Grapefruit",
    24: "Cantaloupe",
    25: "Cauliflower",
    26: "Lettuce head",
    27: "Cabbage",
    28: "Eggplant",
    29: "Butternut squash",
    30: "Large cabbage",
    31: "Coconut",
    32: "Jicama",
    33: "Pineapple",
    34: "Honeydew melon",
    35: "Honeydew melon",
    36: "Romaine lettuce",
    37: "Swiss chard",
    38: "Leek",
    39: "Mini watermelon",
    40: "Small pumpkin",
    41: "Pumpkin",
    42: "Watermelon",
}

# Week-by-week dad comparisons (weeks 1-42)
DAD_COMPARISONS = {
    1: "Dad's cologne sample",
    2: "Dad's tie clip",
    3: "Dad's collar stay",
    4: "Dad's cufflink",
    5: "Dad's guitar pick",
    6: "Dad's dice",
    7: "Dad's USB drive",
    8: "Dad's golf tee",
    9: "Dad's bottle cap",
    10: "Dad's house key",
    11: "Dad's poker chip",
    12: "Dad's AirPods case",
    13: "Dad's remote control",
    14: "Dad's coffee mug",
    15: "Dad's baseball",
    16: "Dad's favorite beer",
    17: "Dad's gaming controller",
    18: "Dad's wallet",
    19: "Dad's running shoe",
    20: "Dad's laptop charger",
    21: "Dad's tablet",
    22: "Dad's sneaker",
    23: "Dad's iPad",
    24: "Dad's laptop",
    25: "Dad's toolbox",
    26: "Dad's briefcase",
    27: "Dad's basketball",
    28: "Dad's bowling ball",
    29: "Dad's backpack",
    30: "Dad's monitor",
    31: "Dad's guitar",
    32: "Dad's golf bag",
    33: "Dad's grill cover",
    34: "Dad's cooler",
    35: "Dad's tackle box",
    36: "Dad's lawn mower",
    37: "Dad's tool chest",
    38: "Dad's recliner",
    39: "Dad's TV",
    40: "Dad's grill",
    41: "Dad's workbench",
    42: "Dad's car tire",
}


def get_comparison(week: int, mode: str, custom_data: dict | None = None) -> str:
    """Get size comparison for a given week and mode."""
    if mode == "custom":
        if custom_data:
            return custom_data.get(str(week), f"Week {week}")
        # If custom mode selected but no data provided, fall back to veggie
        return VEGGIE_COMPARISONS.get(week, f"Week {week}")
    elif mode == "dad":
        return DAD_COMPARISONS.get(week, f"Week {week}")
    else:  # Default to veggie
        return VEGGIE_COMPARISONS.get(week, f"Week {week}")
