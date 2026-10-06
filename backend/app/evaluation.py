from dataclasses import dataclass

from .intent import classify_intent
from .schemas import Intent


@dataclass(frozen=True)
class IntentCase:
    text: str
    expected: Intent


# Synthetic benchmark: 20 utterances per intent x 6 intents = 120 cases.
# The set intentionally mixes Hindi, Hinglish and common code-mixed phrasing.
_CASES_BY_INTENT: dict[Intent, tuple[str, ...]] = {
    "farming": (
        "गेहूं का मंडी भाव क्या है?",
        "wheat ka rate batao",
        "किसान की फसल का भाव बताओ",
        "mandi me गेहूं ka bhav",
        "आज सरसों का रेट क्या है",
        "मेरी फसल का भाव बताइए",
        "tomato mandi rate batao",
        "धान का मंडी भाव चाहिए",
        "farmer ke liye mandi price",
        "कल बारिश होगी?",
        "बारिश का मौसम कैसा रहेगा",
        "weather batao",
        "mere khet ka weather batao",
        "मौसम और बारिश की जानकारी चाहिए",
        "crop ke liye mausam batao",
        "किसान के खेत में बारिश होगी?",
        "potato ka mandi bhav",
        "मंडी में आलू का भाव क्या है",
        "mustard ka rate bataiye",
        "फसल के लिए मौसम बताओ",
    ),
    "scheme": (
        "मुझे किसान योजना बताओ",
        "सरकारी योजना की जानकारी चाहिए",
        "yojana ke baare me batao",
        "मेरी पेंशन योजना कौन सी है",
        "scholarship kaise milegi",
        "छात्रवृत्ति की जानकारी चाहिए",
        "सरकार की subsidy के बारे में बताओ",
        "किसान subsidy कैसे मिलेगी",
        "pension ka form kaha hai",
        "सरकारी लाभ कैसे मिलेगा",
        "scheme eligibility batao",
        "योजना के लिए कौन पात्र है",
        "scholarship eligibility kya hai",
        "सरकारी मदद की योजना बताओ",
        "yojana ke documents kya hain",
        "पेंशन के कागज कौन से चाहिए",
        "किसान योजना का लाभ कैसे लें",
        "सरकारी subsidy मिलेगी क्या",
        "छात्रवृत्ति कैसे मिलेगी",
        "सरकारी योजना चाहिए",
    ),
    "document": (
        "इस नोटिस को समझाओ",
        "document ka matlab batao",
        "इस कागज को समझना है",
        "certificate के बारे में बताओ",
        "notice me kya likha hai",
        "यह पत्र पढ़कर समझाओ",
        "document explain karo",
        "प्रमाण पत्र में क्या लिखा है",
        "कागज़ का मतलब बताइए",
        "letter samjha do",
        "नोटिस का अगला कदम क्या है",
        "certificate ka matlab",
        "दस्तावेज़ समझने में मदद चाहिए",
        "इस चिट्ठी को समझाओ",
        "document ke important points batao",
        "कागज में क्या करना है",
        "notice explain karna hai",
        "प्रमाण पत्र समझाइए",
        "letter ka meaning batao",
        "दस्तावेज़ की जानकारी चाहिए",
    ),
    "task": (
        "मुझे कल याद दिलाना",
        "remind me tomorrow",
        "कल follow up याद रखना",
        "मुझे reminder चाहिए",
        "बाद में याद दिलाना",
        "reminder set karna hai",
        "अगले हफ्ते याद दिलाना",
        "callback याद रखना",
        "मुझे शाम को याद दिलाओ",
        "task बना दो",
        "इस काम का reminder चाहिए",
        "कल फिर याद दिलाना",
        "follow up के लिए task चाहिए",
        "बाद में call करने की याद दिलाओ",
        "remind me later",
        "मेरी pending बात याद रखना",
        "task ke liye reminder",
        "अगले महीने याद दिलाना",
        "callback का reminder लगाओ",
        "मुझे यह काम याद रखना है",
    ),
    "human": (
        "मुझे किसी इंसान से बात करनी है",
        "human se baat karni hai",
        "मुझे volunteer चाहिए",
        "किसी व्यक्ति से बात करवाओ",
        "अधिकारी से बात करनी है",
        "human support चाहिए",
        "इंसान से मदद चाहिए",
        "किसी आदमी से बात कराओ",
        "volunteer ko bulao",
        "मुझे किसी person से बात करनी है",
        "मानव सहायता चाहिए",
        "मुझे agent नहीं इंसान चाहिए",
        "किसी अधिकारी से संपर्क चाहिए",
        "someone से बात करनी है",
        "person help चाहिए",
        "मुझे इंसानी मदद चाहिए",
        "volunteer assistance चाहिए",
        "किसी व्यक्ति की सहायता चाहिए",
        "human support do",
        "अधिकारी से बात करवाइए",
    ),
    "general": (
        "नमस्ते",
        "hello saathi",
        "आप कौन हैं",
        "what can you do",
        "मुझे मदद चाहिए",
        "how are you",
        "साथी क्या कर सकता है",
        "tell me about yourself",
        "आपकी मदद चाहिए",
        "hi",
        "नमस्कार",
        "what is saathi",
        "मुझे जानकारी चाहिए",
        "can you help me",
        "आप कैसे काम करते हैं",
        "help me",
        "साथी के बारे में बताओ",
        "मुझे कुछ पूछना है",
        "hello",
        "नमस्ते साथी",
    ),
}

CASES = tuple(
    IntentCase(text=text, expected=intent)
    for intent, texts in _CASES_BY_INTENT.items()
    for text in texts
)


def run_intent_benchmark() -> dict[str, float | int]:
    correct = sum(classify_intent(case.text) == case.expected for case in CASES)
    return {
        "correct": correct,
        "total": len(CASES),
        "accuracy": correct / len(CASES),
    }
