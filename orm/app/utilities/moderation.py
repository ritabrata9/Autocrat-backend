from transformers import pipeline
from rapidfuzz import fuzz
import re

# load once (singleton) — force CPU
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    device=-1
)

TARGETS = ["ritabrata", "supreme leader", "leader"]


def normalize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)   # remove special chars
    text = re.sub(r'\s+', ' ', text).strip()   # normalize spaces
    return text


def mentions_target(text: str):
    for target in TARGETS:
        # direct match
        if target in text:
            return True

        # fuzzy match (handles typos like "leade", "ritabrta")
        if fuzz.partial_ratio(target, text) >= 80:
            return True

    return False


def violates_policy(text: str) -> bool:
    try:
        result = classifier(text)[0]

        label = result["label"].lower()
        score = result["score"]

        return ("toxic" in label) and score >= 0.5

    except Exception as e:
        # fail-safe: do not block if model crashes
        print("Moderation error:", e)
        return False


def is_disallowed(text: str) -> bool:
    # normalize once at entry
    text = normalize(text)

    # only check abuse if target is mentioned
    if not mentions_target(text):
        return False

    return violates_policy(text)