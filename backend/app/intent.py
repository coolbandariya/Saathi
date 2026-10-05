import re

from .schemas import Intent


_RULES: tuple[tuple[Intent, tuple[str, ...]], ...] = (
    ("human", ("human", "volunteer", "person", "इंसान", "व्यक्ति", "अधिकारी", "मानव")),
    ("scheme", ("scholarship", "scheme", "yojana", "pension", "subsidy", "छात्रवृत्ति", "योजना", "पेंशन")),
    ("farming", ("mandi", "wheat", "weather", "crop", "farmer", "गेहूं", "मंडी", "मौसम", "बारिश", "फसल", "किसान")),
    ("document", ("document", "notice", "certificate", "letter", "कागज", "नोटिस", "प्रमाण पत्र", "चिट्ठी")),
    ("task", ("remind", "reminder", "callback", "याद", "रिमाइंड", "बाद में")),
)

_HINDI_NEGATION = re.compile(r"(?:नहीं|मत|ना)")
_HUMAN_TERMS = r"(?:इंसान|व्यक्ति|अधिकारी|मानव|human|volunteer|person)"


def _contains_keyword(text: str, keyword: str) -> bool:
    pattern = re.escape(keyword).replace(r"\ ", r"\s+")
    return re.search(rf"(?<![\w]){pattern}(?![\w])", text, flags=re.UNICODE) is not None


def _human_request_is_negated(text: str) -> bool:
    for match in re.finditer(_HUMAN_TERMS, text):
        window = text[max(0, match.start() - 32):min(len(text), match.end() + 32)]
        if _HINDI_NEGATION.search(window):
            return True
    return False


def classify_intent(message: str) -> Intent:
    text = re.sub(r"\s+", " ", message.casefold()).strip()
    for intent, keywords in _RULES:
        if intent == "human" and _human_request_is_negated(text):
            continue
        if any(_contains_keyword(text, keyword) for keyword in keywords):
            return intent
    return "general"
