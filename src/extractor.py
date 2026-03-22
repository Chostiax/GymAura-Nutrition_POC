import re

# This PoC only handles simple quantity patterns.
# More complex portion understanding is intentionally out of scope.

NUMBER_WORDS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "half": 0.5,
}

KNOWN_UNITS = {
    "g", "gram", "grams",
    "kg", "kilogram", "kilograms",
    "ml", "milliliter", "milliliters",
    "l", "liter", "liters",
    "cup", "cups",
    "bowl", "bowls",
    "slice", "slices",
    "piece", "pieces",
    "tbsp", "tablespoon", "tablespoons",
    "tsp", "teaspoon", "teaspoons",
    "glass", "glasses",
    "can", "cans",
    "bottle", "bottles",
    "bag", "bags",
    "scoop", "scoops",
    "plate", "plates",
}

NO_FOOD_PATTERNS = [
    r"\bi did(?:n t|nt) eat anything(?: yet)?(?: today)?\b",
    r"\bi have not eaten anything(?: yet)?(?: today)?\b",
    r"\bi haven t eaten anything(?: yet)?(?: today)?\b",
    r"\bi skipped breakfast(?: this morning)?\b(?!.*\bcoffee\b)",
]

LEADING_CONTEXT_PATTERNS = [
    r"^for (?:breakfast|lunch|dinner|dessert|a snack)\s*,?\s*",
    r"^this afternoon\s+",
    r"^last night\s+",
    r"^later\s+",
    r"^today\s+",
    r"^so far today\s+",
]

SEGMENT_PREFIX_PATTERNS = [
    r"^(?:i|we)\s+(?:had|ate|drank|got|grabbed|ordered|made|finished)\s+",
    r"^i\s+just\s+(?:had|ate|drank)\s+",
    r"^i\s+think\s+i\s+drank\s+",
    r"^my\s+breakfast\s+was\s+simple\s*,?\s*just\s+",
    r"^my\s+breakfast\s+was\s+simple\s+",
    r"^i\s+skipped\s+breakfast\s+this\s+morning\s*,?\s*just\s+had\s+",
    r"^we\s+ordered\s+takeout\s+and\s+i\s+got\s+",
    r"^we\s+went\s+to\s+an?\s+[a-z\s]+?restaurant\s+and\s+i\s+ordered\s+",
    r"^i\s+wasn\s*t\s+feeling\s+hungry\s*,?\s*so\s+i\s+just\s+ate\s+",
    r"^i\s+was\s+snacking\s+on\s+",
    r"^my\s+mom\s+made\s+us\s+",
    r"^my\s+girlfriend\s+baked\s+",
    r"^the\s+leftovers\s*[:\-]?\s*",
    "so i just ate",
    "so i ate",
    "so i just had",
    "my girlfriend baked",
    "my mom made us",
]

TRAILING_PATTERNS = [
    r"\s+for\s+(?:breakfast|lunch|dinner|dessert)\b.*$",
    r"\s+for\s+the\s+party\b.*$",
    r"\s+as\s+a\s+snack\b.*$",
    r"\s+after\s+my\s+workout\b.*$",
    r"\s+so\s+far\s+today\b.*$",
    r"\s+this\s+morning\b.*$",
    r"\s+while\s+watching\s+a\s+movie\b.*$",
    r"\s+while\s+waiting\s+for\s+dinner\b.*$",
    "for a snack",
    "while waiting",
    "while waiting for dinner",
]
# Words like "some", "just", or "a bit of" are useful in natural speech
# but usually do not help with dataset matching, so we strip them.

FILLER_PHRASES = [
    "some",
    "a bit of",
    "bit of",
    "a little",
    "a little bit of",
    "just",
    "only",
    "kind of",
    "maybe",
    "about",
]

NON_FOOD_WORDS = {
    "breakfast", "lunch", "dinner", "snack", "meal", "party", "restaurant",
    "was", "ate", "had", "drank", "just", "before", "after", "class", "as",
    "simple", "went", "ordered", "made", "baked", "mom", "girlfriend", "watching",
    "movie", "waiting", "today", "morning", "afternoon", "night", "leftovers","so",
    "while","feeling","hungry","skipped","breakfast",
}

CONTEXT_ONLY_PATTERNS = [
    r"^for\s+a$",
    r"^for\s+dessert$",
    r"^for\s+a\s+snack$",
    r"^my\s+simple$",
    r"^we\s+went\s+to\b",
    r"^i\s+wasn\s*t\s+feeling\s+hungry$",
    r"^i\s+skipped\s+breakfast$",
    r"^takeout$",
    r"^my$",
]


def clean_input_text(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("’", " ").replace("'", " ")
    text = text.replace("&", " and ").replace("+", " and ")
    text = text.replace(":", ", ").replace(";", ", ").replace(".", " ")
    text = re.sub(r"\s+", " ", text)

    for pattern in LEADING_CONTEXT_PATTERNS:
        text = re.sub(pattern, "", text).strip()

    return text


def split_into_segments(text: str) -> list[str]:
    parts = re.split(r",|\band\b|\bwith\b|\bthen\b|\bplus\b", text)
    return [part.strip() for part in parts if part.strip()]


def strip_leading_articles(text: str) -> str:
    return re.sub(r"^(?:a|an|the)\s+", "", text).strip()


def strip_leading_of(text: str) -> str:
    return re.sub(r"^of\s+", "", text).strip()


def strip_segment_prefixes(text: str) -> str:
    cleaned = text.strip()
    changed = True
    while changed:
        changed = False
        for pattern in SEGMENT_PREFIX_PATTERNS:
            new_cleaned = re.sub(pattern, "", cleaned).strip()
            if new_cleaned != cleaned:
                cleaned = new_cleaned
                changed = True
    return cleaned


def strip_trailing_phrases(text: str) -> str:
    cleaned = text.strip()
    for pattern in TRAILING_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned).strip()
    return cleaned


def remove_filler_phrases(text: str) -> str:
    cleaned = text
    for phrase in FILLER_PHRASES:
        cleaned = re.sub(rf"\b{re.escape(phrase)}\b", " ", cleaned)
    return " ".join(cleaned.split()).strip()


def extract_quantity_and_unit(segment: str) -> tuple[float | None, str | None, str]:
    segment = segment.strip()

    # numeric quantity: 2 cups of juice
    numeric_match = re.match(r"^(\d+(?:\.\d+)?)\s+([a-z]+)?\s*(.*)$", segment)
    if numeric_match:
        quantity = float(numeric_match.group(1))
        second_token = numeric_match.group(2)
        rest = numeric_match.group(3).strip()

        if second_token in KNOWN_UNITS:
            rest = strip_leading_of(rest)
            return quantity, second_token, rest

        return quantity, None, f"{second_token or ''} {rest}".strip()

    # word quantity: a can of coke / two cups of coffee
    for word, value in NUMBER_WORDS.items():
        pattern = rf"^{word}\s+([a-z]+)?\s*(.*)$"
        match = re.match(pattern, segment)
        if match:
            second_token = match.group(1)
            rest = match.group(2).strip()

            if second_token in KNOWN_UNITS:
                rest = strip_leading_of(rest)
                return float(value), second_token, rest

            return float(value), None, f"{second_token or ''} {rest}".strip()

    # half of ...
    half_match = re.match(r"^half\s+(?:a\s+|an\s+)?([a-z]+)\s+(.*)$", segment)
    if half_match:
        unit = half_match.group(1)
        rest = half_match.group(2).strip()
        if unit in KNOWN_UNITS:
            rest = strip_leading_of(rest)
            return 0.5, unit, rest

    return None, None, segment


def clean_food_text(food_text: str) -> str:
    food_text = strip_segment_prefixes(food_text)
    food_text = strip_trailing_phrases(food_text)
    food_text = remove_filler_phrases(food_text)
    food_text = strip_leading_articles(food_text)
    food_text = strip_leading_of(food_text)
    food_text = re.sub(r"[^a-z\s]", " ", food_text)
    tokens = [tok for tok in food_text.split() if tok not in NON_FOOD_WORDS]
    return " ".join(tokens).strip()


def is_context_only(text: str) -> bool:
    if not text:
        return True
    return any(re.match(pattern, text) for pattern in CONTEXT_ONLY_PATTERNS)


def extract_foods(text: str) -> list[dict]:
    normalized = clean_input_text(text)
# If the user explicitly says they did not eat anything,
# we short-circuit and return no items.
    if any(re.search(pattern, normalized) for pattern in NO_FOOD_PATTERNS):
        return []

    segments = split_into_segments(normalized)
    extracted = []

    for segment in segments:
        segment = strip_segment_prefixes(segment)
        segment = strip_trailing_phrases(segment)
        segment = remove_filler_phrases(segment)
        segment = " ".join(segment.split()).strip()

        if not segment or is_context_only(segment):
            continue

        quantity, unit, remaining = extract_quantity_and_unit(segment)
        food_text = clean_food_text(remaining)

        if not food_text or is_context_only(food_text):
            continue

        extracted.append({
            "raw_segment": segment,
            "food_text": food_text,
            "quantity": quantity,
            "unit": unit,
        })

    return extracted
