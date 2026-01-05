"""Size comparison data for pregnancy tracker."""
import json
import logging
import os
from pathlib import Path

_LOGGER = logging.getLogger(__name__)

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

    Images are bundled with the integration and automatically copied to:
    /config/www/pregnancy_tracker/{mode}/week_{week}.png
    
    Users can override by placing their own images at these paths.
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


# Weekly Bible verses (weeks 1-42)
BIBLE_VERSES = {
    1: {"text": "Before I formed you in the womb I knew you, before you were born I set you apart.", "reference": "Jeremiah 1:5"},
    2: {"text": "For you created my inmost being; you knit me together in my mother's womb.", "reference": "Psalm 139:13"},
    3: {"text": "I praise you because I am fearfully and wonderfully made; your works are wonderful, I know that full well.", "reference": "Psalm 139:14"},
    4: {"text": "Your eyes saw my unformed body; all the days ordained for me were written in your book before one of them came to be.", "reference": "Psalm 139:16"},
    5: {"text": "Children are a heritage from the Lord, offspring a reward from him.", "reference": "Psalm 127:3"},
    6: {"text": "Can a mother forget the baby at her breast and have no compassion on the child she has borne? Though she may forget, I will not forget you!", "reference": "Isaiah 49:15"},
    7: {"text": "Yet you brought me out of the womb; you made me trust in you, even at my mother's breast.", "reference": "Psalm 22:9"},
    8: {"text": "Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.", "reference": "Joshua 1:9"},
    9: {"text": "The Lord is my strength and my shield; my heart trusts in him, and he helps me.", "reference": "Psalm 28:7"},
    10: {"text": "Cast all your anxiety on him because he cares for you.", "reference": "1 Peter 5:7"},
    11: {"text": "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future.", "reference": "Jeremiah 29:11"},
    12: {"text": "Every good and perfect gift is from above, coming down from the Father of the heavenly lights.", "reference": "James 1:17"},
    13: {"text": "The Lord bless you and keep you; the Lord make his face shine on you and be gracious to you.", "reference": "Numbers 6:24-25"},
    14: {"text": "I can do all this through him who gives me strength.", "reference": "Philippians 4:13"},
    15: {"text": "The Lord your God is with you, the Mighty Warrior who saves. He will take great delight in you; in his love he will no longer rebuke you, but will rejoice over you with singing.", "reference": "Zephaniah 3:17"},
    16: {"text": "And we know that in all things God works for the good of those who love him.", "reference": "Romans 8:28"},
    17: {"text": "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid.", "reference": "John 14:27"},
    18: {"text": "This is the day the Lord has made; let us rejoice and be glad in it.", "reference": "Psalm 118:24"},
    19: {"text": "Trust in the Lord with all your heart and lean not on your own understanding.", "reference": "Proverbs 3:5"},
    20: {"text": "You will go out in joy and be led forth in peace; the mountains and hills will burst into song before you.", "reference": "Isaiah 55:12"},
    21: {"text": "May the God of hope fill you with all joy and peace as you trust in him.", "reference": "Romans 15:13"},
    22: {"text": "The Lord is my shepherd, I lack nothing. He makes me lie down in green pastures, he leads me beside quiet waters, he refreshes my soul.", "reference": "Psalm 23:1-3"},
    23: {"text": "He will command his angels concerning you to guard you in all your ways.", "reference": "Psalm 91:11"},
    24: {"text": "Even youths grow tired and weary, and young men stumble and fall; but those who hope in the Lord will renew their strength.", "reference": "Isaiah 40:30-31"},
    25: {"text": "My grace is sufficient for you, for my power is made perfect in weakness.", "reference": "2 Corinthians 12:9"},
    26: {"text": "The Lord is close to the brokenhearted and saves those who are crushed in spirit.", "reference": "Psalm 34:18"},
    27: {"text": "Start children off on the way they should go, and even when they are old they will not turn from it.", "reference": "Proverbs 22:6"},
    28: {"text": "God is our refuge and strength, an ever-present help in trouble.", "reference": "Psalm 46:1"},
    29: {"text": "Come to me, all you who are weary and burdened, and I will give you rest.", "reference": "Matthew 11:28"},
    30: {"text": "But blessed is the one who trusts in the Lord, whose confidence is in him.", "reference": "Jeremiah 17:7"},
    31: {"text": "The Lord will watch over your coming and going both now and forevermore.", "reference": "Psalm 121:8"},
    32: {"text": "Give thanks to the Lord, for he is good; his love endures forever.", "reference": "Psalm 107:1"},
    33: {"text": "Being confident of this, that he who began a good work in you will carry it on to completion.", "reference": "Philippians 1:6"},
    34: {"text": "She is clothed with strength and dignity; she can laugh at the days to come.", "reference": "Proverbs 31:25"},
    35: {"text": "The Lord himself goes before you and will be with you; he will never leave you nor forsake you.", "reference": "Deuteronomy 31:8"},
    36: {"text": "May he give you the desire of your heart and make all your plans succeed.", "reference": "Psalm 20:4"},
    37: {"text": "Therefore do not worry about tomorrow, for tomorrow will worry about itself.", "reference": "Matthew 6:34"},
    38: {"text": "Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up.", "reference": "Galatians 6:9"},
    39: {"text": "Wait for the Lord; be strong and take heart and wait for the Lord.", "reference": "Psalm 27:14"},
    40: {"text": "For nothing is impossible with God.", "reference": "Luke 1:37"},
    41: {"text": "The Lord is good, a refuge in times of trouble. He cares for those who trust in him.", "reference": "Nahum 1:7"},
    42: {"text": "And the God of all grace, who called you to his eternal glory in Christ, will himself restore you and make you strong, firm and steadfast.", "reference": "1 Peter 5:10"},
}


def get_bible_verse(week: int, custom_path: str | None = None) -> dict[str, str]:
    """Get Bible verse for a given week.
    
    Args:
        week: The pregnancy week (1-42)
        custom_path: Optional path to custom Bible verses JSON file
    
    Returns a dict with 'text' and 'reference' keys.
    """
    if week < 1 or week > 42:
        week = max(1, min(42, week))
    
    # Try to load custom verses if path is provided
    if custom_path:
        custom_verses = _load_custom_bible_verses(custom_path)
        if custom_verses and str(week) in custom_verses:
            custom_data = custom_verses[str(week)]
            # Support both full dict format and simple text format
            if isinstance(custom_data, dict):
                return {
                    "text": custom_data.get("text", ""),
                    "reference": custom_data.get("reference", ""),
                }
            elif isinstance(custom_data, str):
                # If only text is provided, try to parse reference from the end
                return {
                    "text": custom_data,
                    "reference": "",
                }
    
    # Fall back to default verses
    verse_data = BIBLE_VERSES.get(week, {})
    return {
        "text": verse_data.get("text", ""),
        "reference": verse_data.get("reference", ""),
    }


def _load_custom_bible_verses(file_path: str) -> dict:
    """Load custom Bible verses from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing custom verses
        
    Returns:
        Dictionary with week numbers as keys and verse data as values,
        or empty dict if file cannot be loaded.
    """
    try:
        # Handle both absolute and relative paths
        path = Path(file_path)
        
        # If path is relative, try to resolve it from common Home Assistant locations
        if not path.is_absolute():
            # Try /config directory (standard Home Assistant config directory)
            config_path = Path("/config") / file_path
            if config_path.exists():
                path = config_path
            else:
                _LOGGER.warning(
                    "Custom Bible verses file not found at relative path: %s", 
                    file_path
                )
                return {}
        
        if not path.exists():
            _LOGGER.warning(
                "Custom Bible verses file not found: %s", 
                path
            )
            return {}
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Validate the structure
        if not isinstance(data, dict):
            _LOGGER.error(
                "Custom Bible verses file has invalid format. Expected a dictionary."
            )
            return {}
        
        _LOGGER.info(
            "Successfully loaded %d custom Bible verses from %s", 
            len(data), 
            path
        )
        return data
        
    except json.JSONDecodeError as err:
        _LOGGER.error(
            "Failed to parse custom Bible verses JSON file %s: %s",
            file_path,
            err
        )
        return {}
    except Exception as err:
        _LOGGER.error(
            "Failed to load custom Bible verses from %s: %s",
            file_path,
            err
        )
        return {}
