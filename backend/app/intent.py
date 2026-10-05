import re

from .schemas import Intent


_RULES: list[tuple[Intent, tuple[str, ...]]] = [
    ("scheme", ("scholarship", "scheme", "yojana", "pension", "subsidy", "छात्रवृत्ति", "योजना", "पेंशन")),
    ("farming", ("mandi", "wheat", "weather", "crop", "farmer", "गेहूं", "मंडी", "मौसम", "फसल", "किसान")),
    ("document", ("document", "notice", "certificate", "letter", "कागज", "नोटिस", "प्रमाण पत्र", "चिट्ठी")),
    ("task", ("remind", "reminder", "callback", "याद", "रिमाइंड", "बाद में")),
    ("human", ("human", "volunteer", "person", "इंसान", "व्यक्ति", "अधिकारी")),
]


def classify_intent(message: str) -> Intent:
    text = re.sub(r"\\s+", " ", message.lower()).strip()
    for intent, keywords in _RULES:
        if any(keyword in text for keyword in keywords):
            return intent
    return "general"
