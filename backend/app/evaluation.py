from dataclasses import dataclass
from .intent import classify_intent
from .schemas import Intent

@dataclass(frozen=True)
class IntentCase:
    text: str
    expected: Intent

CASES = [IntentCase("गेहूं का मंडी भाव क्या है?", "farming"), IntentCase("कल बारिश होगी?", "farming"), IntentCase("मुझे किसान योजना बताओ", "scheme"), IntentCase("इस नोटिस को समझाओ", "document"), IntentCase("मुझे कल याद दिलाना", "task"), IntentCase("मुझे किसी इंसान से बात करनी है", "human")]

def run_intent_benchmark() -> dict[str, float | int]:
    correct = sum(classify_intent(c.text) == c.expected for c in CASES)
    return {"correct": correct, "total": len(CASES), "accuracy": correct / len(CASES)}
