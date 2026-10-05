from app.intent import classify_intent


EVAL_CASES = [
    ("गेहूं का भाव क्या है", "farming"),
    ("सोनीपत मंडी में आज गेहूं कितने का है", "farming"),
    ("कल बारिश होगी क्या", "farming"),
    ("मेरी फसल के लिए मौसम बताओ", "farming"),
    ("kisan yojana ke liye kaun eligible hai", "scheme"),
    ("मुझे सरकारी योजना चाहिए", "scheme"),
    ("scholarship ke documents kya hain", "scheme"),
    ("इस नोटिस में क्या लिखा है", "document"),
    ("मेरे कागज को समझा दो", "document"),
    ("मुझे बाद में याद दिलाना", "task"),
    ("इस काम का reminder लगा दो", "task"),
    ("मुझे किसी इंसान से बात करनी है", "human"),
    ("human volunteer se baat karao", "human"),
    ("नमस्ते साथी", "general"),
    ("what can you do", "general"),
    ("barish aur mandi dono batao", "farming"),
    ("मंडी नहीं पूछ रहा, मुझे योजना बताओ", "scheme"),
    ("मुझे इंसान नहीं चाहिए, योजना बताओ", "scheme"),
    ("बारिश नहीं, गेहूं का भाव बताओ", "farming"),
    ("document ka next step batao", "document"),
]


def test_core_hindi_eval_set():
    correct = sum(classify_intent(text) == expected for text, expected in EVAL_CASES)
    assert correct / len(EVAL_CASES) >= 0.90
