"""Size comparison data for pregnancy tracker."""

# Week-by-week comparisons (weeks 1-42)
COMPARISONS = {
    1: {"veggie": "Poppy seed", "dad": "Dad's cologne sample"},
    2: {"veggie": "Sesame seed", "dad": "Dad's tie clip"},
    3: {"veggie": "Peppercorn", "dad": "Dad's collar stay"},
    4: {"veggie": "Lentil", "dad": "Dad's cufflink"},
    5: {"veggie": "Apple seed", "dad": "Dad's guitar pick"},
    6: {"veggie": "Sweet pea", "dad": "Dad's dice"},
    7: {"veggie": "Blueberry", "dad": "Dad's USB drive"},
    8: {"veggie": "Raspberry", "dad": "Dad's golf tee"},
    9: {"veggie": "Cherry", "dad": "Dad's bottle cap"},
    10: {"veggie": "Strawberry", "dad": "Dad's house key"},
    11: {"veggie": "Brussels sprout", "dad": "Dad's poker chip"},
    12: {"veggie": "Plum", "dad": "Dad's AirPods case"},
    13: {"veggie": "Lemon", "dad": "Dad's remote control"},
    14: {"veggie": "Peach", "dad": "Dad's coffee mug"},
    15: {"veggie": "Apple", "dad": "Dad's baseball"},
    16: {"veggie": "Avocado", "dad": "Dad's favorite beer"},
    17: {"veggie": "Turnip", "dad": "Dad's gaming controller"},
    18: {"veggie": "Bell pepper", "dad": "Dad's wallet"},
    19: {"veggie": "Mango", "dad": "Dad's running shoe"},
    20: {"veggie": "Banana", "dad": "Dad's laptop charger"},
    21: {"veggie": "Carrot", "dad": "Dad's tablet"},
    22: {"veggie": "Papaya", "dad": "Dad's sneaker"},
    23: {"veggie": "Grapefruit", "dad": "Dad's iPad"},
    24: {"veggie": "Cantaloupe", "dad": "Dad's laptop"},
    25: {"veggie": "Cauliflower", "dad": "Dad's toolbox"},
    26: {"veggie": "Lettuce head", "dad": "Dad's briefcase"},
    27: {"veggie": "Cabbage", "dad": "Dad's basketball"},
    28: {"veggie": "Eggplant", "dad": "Dad's bowling ball"},
    29: {"veggie": "Butternut squash", "dad": "Dad's backpack"},
    30: {"veggie": "Large cabbage", "dad": "Dad's monitor"},
    31: {"veggie": "Coconut", "dad": "Dad's guitar"},
    32: {"veggie": "Jicama", "dad": "Dad's golf bag"},
    33: {"veggie": "Pineapple", "dad": "Dad's grill cover"},
    34: {"veggie": "Honeydew melon", "dad": "Dad's cooler"},
    35: {"veggie": "Large honeydew melon", "dad": "Dad's tackle box"},
    36: {"veggie": "Romaine lettuce", "dad": "Dad's lawn mower"},
    37: {"veggie": "Swiss chard", "dad": "Dad's tool chest"},
    38: {"veggie": "Leek", "dad": "Dad's recliner"},
    39: {"veggie": "Mini watermelon", "dad": "Dad's TV"},
    40: {"veggie": "Small pumpkin", "dad": "Dad's grill"},
    41: {"veggie": "Pumpkin", "dad": "Dad's workbench"},
    42: {"veggie": "Watermelon", "dad": "Dad's car tire"},
}


def _image_path(mode: str, week: int) -> str:
    """Build an image path for a given mode/week.

    By default, we reference local www paths so users can drop their own assets at:
    /config/www/pregnancy_tracker/{mode}/week_{week}.png
    """
    return f"/local/pregnancy_tracker/{mode}/week_{week}.png"

# Weekly development summaries (weeks 1-42)
WEEKLY_SUMMARIES = {
    1: "Conception occurs. The fertilized egg begins its journey.",
    2: "The blastocyst implants into the uterine wall.",
    3: "Baby's heart and nervous system begin to form.",
    4: "The neural tube forms, which will become baby's brain and spinal cord.",
    5: "Baby's heart begins to beat! Major organs start developing.",
    6: "Facial features begin to form. Arm and leg buds appear.",
    7: "Baby's brain is growing rapidly. Eyelids and nose are forming.",
    8: "Webbed fingers and toes are developing. Baby starts to move!",
    9: "Baby's heartbeat can be heard on ultrasound. Organs continue developing.",
    10: "Baby's vital organs are formed and starting to function.",
    11: "Baby's bones are beginning to harden. Fingernails are forming.",
    12: "Baby's reflexes are developing. They can open and close their fists.",
    13: "Baby's vocal cords are forming. Fingerprints are developing.",
    14: "Baby can make facial expressions and may even squint and frown.",
    15: "Baby's skeleton continues to develop. They're very active now!",
    16: "Baby's eyes can move. You might start feeling those first kicks!",
    17: "Baby can hear sounds from the outside world now.",
    18: "Baby's ears are properly positioned. They can yawn and hiccup!",
    19: "Vernix caseosa (protective coating) covers baby's skin.",
    20: "Halfway there! Baby can hear your voice and may respond to sounds.",
    21: "Baby's movements become more coordinated and noticeable.",
    22: "Baby's eyebrows and eyelashes are visible. Senses are developing.",
    23: "Baby's lungs are preparing for breathing, though not yet functional.",
    24: "Viability milestone! Baby has a chance of survival if born now.",
    25: "Baby responds to your voice and touch. Hair may be growing.",
    26: "Baby's eyes are beginning to open. They can see light.",
    27: "Third trimester begins! Baby's brain is developing rapidly.",
    28: "Baby can dream! REM sleep has begun.",
    29: "Baby's muscles and lungs are maturing rapidly.",
    30: "Baby's brain is developing billions of neurons.",
    31: "Baby's five senses are fully developed and functional.",
    32: "Baby practices breathing by inhaling amniotic fluid.",
    33: "Baby's bones are hardening, but the skull remains soft.",
    34: "Baby's central nervous system is maturing.",
    35: "Baby's kidneys are fully developed. Liver is processing waste.",
    36: "Baby is shedding vernix and lanugo. Almost ready!",
    37: "Full term! Baby could arrive any day now.",
    38: "Baby has a firm grasp and is perfecting reflexes.",
    39: "Baby's brain and lungs continue maturing.",
    40: "Due date! Baby is fully developed and ready to meet you.",
    41: "Still waiting! Baby continues to gain weight.",
    42: "Past due. Doctor may recommend induction.",
}


def get_comparison(week: int, mode: str = "veggie") -> dict[str, str]:
    """Get size comparison data for a given week.

    Returns a dict with 'label' and 'image' keys (no emoji).
    """
    if week < 1 or week > 42:
        week = max(1, min(42, week))

    data = COMPARISONS.get(week, {})

    if mode == "dad":
        return {
            "label": data.get("dad", f"Week {week}"),
            "image": _image_path("dad", week),
        }
    else:  # Default to veggie
        return {
            "label": data.get("veggie", f"Week {week}"),
            "image": _image_path("veggie", week),
        }


def get_all_comparisons(week: int) -> dict[str, dict[str, str]]:
    """Get all comparison modes for a given week with images."""
    if week < 1 or week > 42:
        week = max(1, min(42, week))

    data = COMPARISONS.get(week, {})

    return {
        "veggie": {
            "label": data.get("veggie", f"Week {week}"),
            "image": _image_path("veggie", week),
        },
        "dad": {
            "label": data.get("dad", f"Week {week}"),
            "image": _image_path("dad", week),
        },
    }


def get_weekly_summary(week: int) -> str:
    """Get developmental summary for a given week."""
    if week < 1 or week > 42:
        week = max(1, min(42, week))
    
    return WEEKLY_SUMMARIES.get(week, f"Week {week} of pregnancy.")
