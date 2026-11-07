"""Sample data for the VelaiVaasal prototype (roles, skills, interview questions)."""

ROLES = {
    "data-analyst": {
        "title": {"en": "Junior Data Analyst", "ta": "ஜூனியர் டேட்டா அனலிஸ்ட்", "hi": "जूनियर डेटा एनालिस्ट"},
        "skills": [
            {"id": "excel", "weight": 3, "name": {"en": "Excel & spreadsheets", "ta": "எக்செல் & ஸ்ப்ரெட்ஷீட்", "hi": "एक्सेल और स्प्रेडशीट"},
             "lessons": [("Formulas: SUM, IF, VLOOKUP", 25), ("Pivot tables in 20 minutes", 20)], "task": "Clean a 100-row sales sheet and build one pivot table."},
            {"id": "sql", "weight": 3, "name": {"en": "SQL basics", "ta": "SQL அடிப்படைகள்", "hi": "SQL की बुनियादी बातें"},
             "lessons": [("SELECT, WHERE, ORDER BY", 30), ("GROUP BY and JOIN", 35)], "task": "Write 5 queries on a sample students table."},
            {"id": "stats", "weight": 2, "name": {"en": "Statistics basics", "ta": "புள்ளியியல் அடிப்படைகள்", "hi": "सांख्यिकी की बुनियादी बातें"},
             "lessons": [("Mean, median, spread", 20), ("Reading charts correctly", 15)], "task": "Summarise a small dataset in 3 sentences."},
            {"id": "viz", "weight": 2, "name": {"en": "Charts & dashboards", "ta": "வரைபடங்கள் & டாஷ்போர்டு", "hi": "चार्ट और डैशबोर्ड"},
             "lessons": [("Choosing the right chart", 15), ("Build a one-page dashboard", 40)], "task": "Make a one-page dashboard from your pivot table."},
            {"id": "comm", "weight": 1, "name": {"en": "Explaining insights", "ta": "கண்டுபிடிப்புகளை விளக்குதல்", "hi": "निष्कर्ष समझाना"},
             "lessons": [("Insight, evidence, action", 15)], "task": "Record a 1-minute explanation of your dashboard."},
        ],
    },
    "customer-support": {
        "title": {"en": "Customer Support Executive", "ta": "வாடிக்கையாளர் சேவை நிர்வாகி", "hi": "कस्टमर सपोर्ट एक्ज़ीक्यूटिव"},
        "skills": [
            {"id": "comm", "weight": 3, "name": {"en": "Clear spoken communication", "ta": "தெளிவான பேச்சுத் தொடர்பு", "hi": "स्पष्ट बोलचाल"},
             "lessons": [("Greeting and active listening", 20), ("Calming an upset customer", 25)], "task": "Role-play 3 complaint calls with a friend."},
            {"id": "typing", "weight": 2, "name": {"en": "Typing & email writing", "ta": "தட்டச்சு & மின்னஞ்சல்", "hi": "टाइपिंग और ईमेल"},
             "lessons": [("Writing a polite email", 20), ("Typing speed drills", 15)], "task": "Reply to 5 sample customer emails."},
            {"id": "tools", "weight": 2, "name": {"en": "CRM & ticket tools", "ta": "CRM & டிக்கெட் கருவிகள்", "hi": "CRM और टिकट टूल"},
             "lessons": [("What is a support ticket?", 15), ("Prioritising tickets", 20)], "task": "Sort 10 sample tickets by urgency."},
            {"id": "product", "weight": 1, "name": {"en": "Learning a product fast", "ta": "பொருளை விரைவாகக் கற்றல்", "hi": "प्रोडक्ट जल्दी सीखना"},
             "lessons": [("Reading product FAQs quickly", 15)], "task": "Summarise one product FAQ in 5 points."},
        ],
    },
    "accounts-assistant": {
        "title": {"en": "Accounts Assistant", "ta": "கணக்கு உதவியாளர்", "hi": "अकाउंट्स असिस्टेंट"},
        "skills": [
            {"id": "tally", "weight": 3, "name": {"en": "Accounting basics & Tally", "ta": "கணக்கியல் அடிப்படை & Tally", "hi": "अकाउंटिंग और टैली"},
             "lessons": [("Debit, credit and ledgers", 30), ("Voucher entry in Tally", 35)], "task": "Record 15 sample vouchers."},
            {"id": "gst", "weight": 2, "name": {"en": "GST basics", "ta": "GST அடிப்படைகள்", "hi": "GST की बुनियादी बातें"},
             "lessons": [("Reading a GST invoice", 20)], "task": "Check 5 sample invoices for GST errors."},
            {"id": "excel", "weight": 2, "name": {"en": "Excel & spreadsheets", "ta": "எக்செல் & ஸ்ப்ரெட்ஷீட்", "hi": "एक्सेल और स्प्रेडशीट"},
             "lessons": [("Formulas: SUM, IF, VLOOKUP", 25)], "task": "Build a monthly expense tracker."},
            {"id": "detail", "weight": 1, "name": {"en": "Accuracy & attention to detail", "ta": "துல்லியம்", "hi": "सटीकता"},
             "lessons": [("Checking your own work", 10)], "task": "Find 3 errors in a sample ledger."},
        ],
    },
}

# Interview questions. kw = expected keywords (any language), used by the demo scorer.
QUESTIONS = {
    "hr": [
        {"id": "hr1", "kw": ["student", "project", "college", "learn", "skill", "interest", "மாணவர்", "கற்று", "छात्र", "सीख"],
         "q": {"en": "Tell me about yourself.", "ta": "உங்களைப் பற்றிச் சொல்லுங்கள்.", "hi": "अपने बारे में बताइए।"},
         "tip": {"en": "Name, studies, one project, one goal.", "ta": "பெயர், படிப்பு, ஒரு திட்டம், ஒரு இலக்கு.", "hi": "नाम, पढ़ाई, एक प्रोजेक्ट, एक लक्ष्य।"}},
        {"id": "hr2", "kw": ["team", "learn", "reliable", "hardworking", "communication", "problem", "குழு", "கடின", "टीम", "मेहनत"],
         "q": {"en": "What is your biggest strength?", "ta": "உங்கள் மிகப்பெரிய பலம் என்ன?", "hi": "आपकी सबसे बड़ी ताकत क्या है?"},
         "tip": {"en": "Pick one strength and give a real example.", "ta": "ஒரு பலத்தைத் தேர்ந்து உண்மையான உதாரணம் கொடுங்கள்.", "hi": "एक ताकत चुनें और असली उदाहरण दें।"}},
        {"id": "hr3", "kw": ["because", "example", "situation", "result", "did", "solved", "learned", "முடிவு", "நான்", "परिणाम", "मैंने"],
         "q": {"en": "Describe a time you solved a difficult problem.", "ta": "நீங்கள் ஒரு கடினமான பிரச்சனையைத் தீர்த்த அனுபவத்தைச் சொல்லுங்கள்.", "hi": "कोई कठिन समस्या हल करने का अनुभव बताइए।"},
         "tip": {"en": "Use Situation, Action, Result.", "ta": "சூழல், செயல், முடிவு என்ற வரிசையில் சொல்லுங்கள்.", "hi": "स्थिति, कार्य, परिणाम के क्रम में बताएं।"}},
    ],
    "data-analyst": [
        {"id": "da1", "kw": ["join", "tables", "key", "combine", "inner", "left", "rows", "இணை", "जोड़"],
         "q": {"en": "What does a SQL JOIN do?", "ta": "SQL JOIN என்ன செய்கிறது?", "hi": "SQL JOIN क्या करता है?"},
         "tip": {"en": "Mention tables, a common key, and one join type.", "ta": "அட்டவணைகள், பொது விசை, ஒரு வகை.", "hi": "टेबल, कॉमन की और एक जॉइन प्रकार बताएं।"}},
        {"id": "da2", "kw": ["average", "mean", "median", "outlier", "skew", "middle", "சராசரி", "औसत", "माध्यिका"],
         "q": {"en": "When would you use median instead of average?", "ta": "சராசரிக்குப் பதிலாக எப்போது இடைநிலை (median) பயன்படுத்துவீர்கள்?", "hi": "औसत की जगह माध्यिका कब इस्तेमाल करेंगे?"},
         "tip": {"en": "Think about outliers like very high salaries.", "ta": "மிக அதிக சம்பளம் போன்ற விலகல்களை நினையுங்கள்.", "hi": "बहुत ज्यादा वेतन जैसे आउटलायर सोचें।"}},
    ],
    "customer-support": [
        {"id": "cs1", "kw": ["listen", "apologize", "apologise", "sorry", "understand", "solution", "calm", "follow", "empathy", "கேட்டு", "மன்னிப்பு", "सुन", "माफ"],
         "q": {"en": "How would you handle an angry customer?", "ta": "கோபமான வாடிக்கையாளரை எப்படிக் கையாள்வீர்கள்?", "hi": "गुस्से वाले ग्राहक को कैसे संभालेंगे?"},
         "tip": {"en": "Listen, apologise, solve, follow up.", "ta": "கேளுங்கள், மன்னிப்பு, தீர்வு, பின்தொடர்தல்.", "hi": "सुनें, माफी, समाधान, फॉलो-अप।"}},
        {"id": "cs2", "kw": ["priority", "urgent", "impact", "deadline", "first", "queue", "முன்னுரிமை", "प्राथमिकता", "जरूरी"],
         "q": {"en": "You have 10 tickets. How do you decide which to do first?", "ta": "10 டிக்கெட்டுகள் உள்ளன. எதை முதலில் செய்வீர்கள்?", "hi": "10 टिकट हैं। पहले कौन सा करेंगे?"},
         "tip": {"en": "Urgency, customer impact, deadline.", "ta": "அவசரம், பாதிப்பு, காலக்கெடு.", "hi": "तात्कालिकता, असर, डेडलाइन।"}},
    ],
    "accounts-assistant": [
        {"id": "ac1", "kw": ["debit", "credit", "ledger", "balance", "entry", "double", "வரவு", "செலவு", "डेबिट", "क्रेडिट"],
         "q": {"en": "Explain debit and credit in simple words.", "ta": "டெபிட், கிரெடிட் என்பதை எளிமையாக விளக்குங்கள்.", "hi": "डेबिट और क्रेडिट आसान शब्दों में समझाइए।"},
         "tip": {"en": "Every entry has two sides that balance.", "ta": "ஒவ்வொரு பதிவுக்கும் இரு பக்கங்கள் சமமாக இருக்கும்.", "hi": "हर एंट्री के दो पक्ष बराबर होते हैं।"}},
        {"id": "ac2", "kw": ["gst", "invoice", "tax", "rate", "input", "gstin", "வரி", "कर"],
         "q": {"en": "What details must a GST invoice contain?", "ta": "GST விலைப்பட்டியலில் என்னென்ன விவரங்கள் இருக்க வேண்டும்?", "hi": "GST इनवॉइस में कौन सी जानकारी जरूरी है?"},
         "tip": {"en": "GSTIN, date, rate, tax amount.", "ta": "GSTIN, தேதி, வரி விகிதம், தொகை.", "hi": "GSTIN, तारीख, दर, कर राशि।"}},
    ],
}
FILLERS = ["um", "uh", "like", "you know", "actually", "basically", "maybe", "sort of", "kind of", "i think"]
LEVELS = {0: "Never tried", 1: "Beginner", 2: "Comfortable", 3: "Strong"}
