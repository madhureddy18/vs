def detect_intent(locked_text: str, multi_text: str) -> str:
    """
    Detect intent using BOTH:
    - locked_text (native language, accurate)
    - multi_text (phonetic / mixed, fallback)
    """

    combined = f"{locked_text} {multi_text}".lower()

    # ---------- ENGLISH ----------
    en_vision = [
    # Presence / Direction
    "in front of me", "ahead of me", "near me", "around me",
    "beside me", "on the road",

    # Obstacles
    "obstacle", "block", "something ahead", "anything ahead",
    "is the path clear", "can i walk", "safe to walk",

    # People / Living
    "person", "people", "crowd", "someone in front",

    # Vehicles
    "car", "bike", "bus", "truck", "vehicle", "traffic",

    # Movement / Danger
    "coming towards me", "moving", "approaching",

    # Object queries
    "what is this object", "describe this object",
    "what am i holding", "what is this",

    # Visual attributes
    "what color", "how many", "how far", "distance",

    # Reading / Signs
    "read this", "what does this say"
]


    # ---------- HINDI (DEVANAGARI) ----------
    hi_vision = [
    # सामने / दिशा
    "मेरे सामने", "आगे क्या है", "मेरे आगे", "पास में",
    "आसपास क्या है", "सड़क पर",

    # बाधाएं
    "रास्ता साफ है", "कोई बाधा", "कुछ सामने है",
    "चलना सुरक्षित है",

    # लोग
    "कोई आदमी", "लोग सामने", "भीड़",

    # वाहन
    "गाड़ी", "कार", "बाइक", "बस", "ट्रक", "वाहन",

    # खतरा / गति
    "मेरी तरफ आ रहा", "चलती हुई",

    # वस्तु
    "यह क्या है", "इस वस्तु का विवरण",
    "मैं क्या पकड़े हुए हूँ",

    # रंग / संख्या
    "किस रंग का", "कितने", "कितनी दूरी",

    # पढ़ना
    "पढ़ो", "यह क्या लिखा है"
]


    # ---------- TELUGU (NATIVE SCRIPT) ----------
    te_vision = [
    # ముందు / దిశ
    "నా ముందు", "ముందు ఏముంది", "నా ముందే",
    "నా చుట్టూ", "సమీపంలో",

    # అడ్డంకులు
    "అడ్డంకి", "రహదారి సురక్షితమా",
    "ముందు ఏదైనా ఉందా",

    # వ్యక్తులు
    "వ్యక్తి", "ముందు ఎవరు", "జనం",

    # వాహనాలు
    "కారు", "బైక్", "బస్సు", "ట్రక్", "వాహనం",

    # ప్రమాదం / కదలిక
    "నా వైపు వస్తోంది", "కదులుతోంది",

    # వస్తువు
    "ఈ వస్తువు ఏమిటి", "ఈ వస్తువును వివరించు",
    "నేను ఏమి పట్టుకున్నాను",

    # రంగు / సంఖ్య / దూరం
    "ఏ రంగులో", "ఎన్ని", "ఎంత దూరంలో",

    # చదవడం
    "చదువు", "ఇది ఏమి వ్రాయబడింది"
]


    for kw in en_vision + hi_vision + te_vision:
        if kw in combined:
            return "VISION"

    return "KNOWLEDGE"
