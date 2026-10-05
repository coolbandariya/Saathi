from app.intent import classify_intent

SEEDS = {
    "farming": [
        "गेहूं का मंडी भाव क्या है",
        "सोनीपत मंडी में गेहूं कितने का है",
        "कल बारिश होगी क्या",
        "मेरी फसल के लिए मौसम बताओ",
        "kisan ke liye mandi price batao",
    ],
    "scheme": [
        "किसान योजना के लिए कौन eligible है",
        "मुझे सरकारी योजना चाहिए",
        "scholarship ke documents kya hain",
        "मेरी पेंशन योजना कौन सी है",
        "subsidy ke liye kya chahiye",
    ],
    "document": [
        "इस नोटिस में क्या लिखा है",
        "मेरे कागज को समझा दो",
        "document ka next step batao",
        "यह certificate किसलिए है",
        "इस letter का जवाब कैसे दें",
    ],
    "task": [
        "मुझे बाद में याद दिलाना",
        "इस काम का reminder लगा दो",
        "कल callback करना",
        "याद रखो कि प्रमाण पत्र लेना है",
        "remind me tomorrow",
    ],
    "human": [
        "मुझे किसी इंसान से बात करनी है",
        "human volunteer se baat karao",
        "किसी व्यक्ति की मदद चाहिए",
        "अधिकारी से बात करनी है",
        "मुझे volunteer चाहिए",
    ],
    "general": [
        "नमस्ते साथी",
        "what can you do",
        "आप कैसे मदद करते हैं",
        "hello saathi",
        "साथी क्या है",
    ],
}

PREFIXES = ["", "कृपया ", "मुझे बताइए ", "जरा "]

CASES = [
    (prefix + seed + suffix, intent)
    for intent, seeds in SEEDS.items()
    for seed in seeds
    for prefix in PREFIXES
]

def test_synthetic_intent_benchmark():
    correct = sum(classify_intent(text) == expected for text, expected in CASES)
    assert len(CASES) == 120
    assert correct / len(CASES) >= 0.90
