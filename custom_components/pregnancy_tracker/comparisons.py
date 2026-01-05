"""Size comparison data for pregnancy tracker."""

# Week-by-week comparisons with emoji (weeks 1-42)
COMPARISONS = {
    1: {"veggie": "Poppy seed", "emoji": "🌾", "dad": "Dad's cologne sample"},
    2: {"veggie": "Sesame seed", "emoji": "🌾", "dad": "Dad's tie clip"},
    3: {"veggie": "Peppercorn", "emoji": "⚫", "dad": "Dad's collar stay"},
    4: {"veggie": "Lentil", "emoji": "⚫", "dad": "Dad's cufflink"},
    5: {"veggie": "Apple seed", "emoji": "🍎", "dad": "Dad's guitar pick"},
    6: {"veggie": "Sweet pea", "emoji": "🟢", "dad": "Dad's dice"},
    7: {"veggie": "Blueberry", "emoji": "🫐", "dad": "Dad's USB drive"},
    8: {"veggie": "Raspberry", "emoji": "🫐", "dad": "Dad's golf tee"},
    9: {"veggie": "Cherry", "emoji": "🍒", "dad": "Dad's bottle cap"},
    10: {"veggie": "Strawberry", "emoji": "🍓", "dad": "Dad's house key"},
    11: {"veggie": "Brussels sprout", "emoji": "🥬", "dad": "Dad's poker chip"},
    12: {"veggie": "Plum", "emoji": "🍑", "dad": "Dad's AirPods case"},
    13: {"veggie": "Lemon", "emoji": "🍋", "dad": "Dad's remote control"},
    14: {"veggie": "Peach", "emoji": "🍑", "dad": "Dad's coffee mug"},
    15: {"veggie": "Apple", "emoji": "🍎", "dad": "Dad's baseball"},
    16: {"veggie": "Avocado", "emoji": "🥑", "dad": "Dad's favorite beer"},
    17: {"veggie": "Turnip", "emoji": "🥬", "dad": "Dad's gaming controller"},
    18: {"veggie": "Bell pepper", "emoji": "🫑", "dad": "Dad's wallet"},
    19: {"veggie": "Mango", "emoji": "🥭", "dad": "Dad's running shoe"},
    20: {"veggie": "Banana", "emoji": "🍌", "dad": "Dad's laptop charger"},
    21: {"veggie": "Carrot", "emoji": "🥕", "dad": "Dad's tablet"},
    22: {"veggie": "Papaya", "emoji": "🧡", "dad": "Dad's sneaker"},
    23: {"veggie": "Grapefruit", "emoji": "🍊", "dad": "Dad's iPad"},
    24: {"veggie": "Cantaloupe", "emoji": "🍈", "dad": "Dad's laptop"},
    25: {"veggie": "Cauliflower", "emoji": "🥦", "dad": "Dad's toolbox"},
    26: {"veggie": "Lettuce head", "emoji": "🥬", "dad": "Dad's briefcase"},
    27: {"veggie": "Cabbage", "emoji": "🥬", "dad": "Dad's basketball"},
    28: {"veggie": "Eggplant", "emoji": "🍆", "dad": "Dad's bowling ball"},
    29: {"veggie": "Butternut squash", "emoji": "🎃", "dad": "Dad's backpack"},
    30: {"veggie": "Large cabbage", "emoji": "🥬", "dad": "Dad's monitor"},
    31: {"veggie": "Coconut", "emoji": "🥥", "dad": "Dad's guitar"},
    32: {"veggie": "Jicama", "emoji": "🥔", "dad": "Dad's golf bag"},
    33: {"veggie": "Pineapple", "emoji": "🍍", "dad": "Dad's grill cover"},
    34: {"veggie": "Honeydew melon", "emoji": "🍈", "dad": "Dad's cooler"},
    35: {"veggie": "Large honeydew melon", "emoji": "🍈", "dad": "Dad's tackle box"},
    36: {"veggie": "Romaine lettuce", "emoji": "🥬", "dad": "Dad's lawn mower"},
    37: {"veggie": "Swiss chard", "emoji": "🥬", "dad": "Dad's tool chest"},
    38: {"veggie": "Leek", "emoji": "🧅", "dad": "Dad's recliner"},
    39: {"veggie": "Mini watermelon", "emoji": "🍉", "dad": "Dad's TV"},
    40: {"veggie": "Small pumpkin", "emoji": "🎃", "dad": "Dad's grill"},
    41: {"veggie": "Pumpkin", "emoji": "🎃", "dad": "Dad's workbench"},
    42: {"veggie": "Watermelon", "emoji": "🍉", "dad": "Dad's car tire"},
}


def get_comparison(week: int, mode: str = "veggie") -> dict[str, str]:
    """Get size comparison data for a given week.
    
    Returns a dict with 'label', 'emoji' keys.
    """
    if week < 1 or week > 42:
        week = max(1, min(42, week))
    
    data = COMPARISONS.get(week, {})
    
    if mode == "dad":
        return {
            "label": data.get("dad", f"Week {week}"),
            "emoji": data.get("emoji", ""),
        }
    else:  # Default to veggie
        return {
            "label": data.get("veggie", f"Week {week}"),
            "emoji": data.get("emoji", ""),
        }


def get_all_comparisons(week: int) -> dict[str, dict[str, str]]:
    """Get all comparison modes for a given week with emojis."""
    if week < 1 or week > 42:
        week = max(1, min(42, week))
    
    data = COMPARISONS.get(week, {})
    
    return {
        "veggie": {
            "label": data.get("veggie", f"Week {week}"),
            "emoji": data.get("emoji", ""),
        },
        "dad": {
            "label": data.get("dad", f"Week {week}"),
            "emoji": data.get("emoji", ""),
        },
    }
