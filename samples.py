"""
Pre-configured realistic medical samples for MedLens.
Ensures bulletproof, instant hackathon demonstrations even with offline/spotty connections.
"""

SAMPLE_DATA = {
    "sample_antibiotics": {
        "id": "sample_antibiotics",
        "title": "General Practice: Acute Respiratory Infection",
        "doctor": "Dr. S. K. Sharma, MD (Internal Medicine)",
        "patient": "Rahul Verma, 29 M",
        "diagnosis": "Acute Bacterial Bronchitis & Pharyngitis",
        "image_url": "/static/images/sample_rx1.svg",
        "medicines": [
            {
                "name": "Augmentin (Amoxicillin + Clavulanate)",
                "generic": "Amoxicillin 500mg + Clavulanic Acid 125mg",
                "dosage": "625 mg",
                "frequency": "Twice daily (1 - 0 - 1)",
                "duration": "5 days",
                "timing": "After meals",
                "purpose": "Broad-spectrum antibiotic to eliminate bacterial throat & chest infection",
                "food_instruction": "Take with or right after food to prevent stomach upset",
                "badge": "Antibiotic",
                "color": "blue"
            },
            {
                "name": "Pan-D (Pantoprazole + Domperidone)",
                "generic": "Pantoprazole 40mg + Domperidone 30mg",
                "dosage": "1 Capsule",
                "frequency": "Once daily (1 - 0 - 0)",
                "duration": "5 days",
                "timing": "Morning, 30 mins before breakfast",
                "purpose": "Reduces stomach acid and prevents antibiotic-induced nausea or gastritis",
                "food_instruction": "Strictly on an empty stomach with a full glass of water",
                "badge": "Antacid",
                "color": "emerald"
            },
            {
                "name": "Dolo 650 (Paracetamol)",
                "generic": "Acetaminophen / Paracetamol 650mg",
                "dosage": "650 mg",
                "frequency": "Thrice daily as needed (SOS)",
                "duration": "3 days",
                "timing": "Every 6-8 hours if body temperature > 100°F",
                "purpose": "Relieves body aches, fever, and sore throat pain",
                "food_instruction": "After light food",
                "badge": "Analgesic",
                "color": "amber"
            },
            {
                "name": "Levocet-M",
                "generic": "Levocetirizine 5mg + Montelukast 10mg",
                "dosage": "1 Tablet",
                "frequency": "Once daily at night (0 - 0 - 1)",
                "duration": "5 days",
                "timing": "Before sleeping",
                "purpose": "Anti-allergic to reduce nasal drip, coughing fits, and chest tightness",
                "food_instruction": "May cause slight drowsiness; avoid driving after taking",
                "badge": "Anti-Allergy",
                "color": "purple"
            }
        ],
        "conflicts_and_warnings": [
            {
                "severity": "safe",
                "title": "Course Completion Alert",
                "description": "Ensure completion of the full 5-day Augmentin course even if fever subsides early, to prevent antibiotic resistance."
            },
            {
                "severity": "caution",
                "title": "Sedation Warning (Levocet-M)",
                "description": "Antihistamine components cause mild drowsiness. Do not drive or operate machinery after your nighttime dose."
            }
        ],
        "daily_schedule": {
            "morning": [
                {"time": "07:30 AM", "medicine": "Pan-D 40mg", "instruction": "Empty stomach (30 mins before breakfast)", "icon": "🌅"},
                {"time": "08:30 AM", "medicine": "Augmentin 625mg", "instruction": "Immediately after breakfast with plenty of water", "icon": "💊"}
            ],
            "afternoon": [
                {"time": "02:00 PM", "medicine": "Dolo 650mg", "instruction": "Optional: Only if fever or body ache is present", "icon": "☀️"}
            ],
            "evening": [
                {"time": "08:30 PM", "medicine": "Augmentin 625mg", "instruction": "After dinner", "icon": "🌙"},
                {"time": "10:00 PM", "medicine": "Levocet-M", "instruction": "Right before bed to assist restful sleep without coughing", "icon": "🛌"}
            ]
        },
        "plain_english_summary": "You have been diagnosed with an acute bacterial respiratory infection. The doctor has prescribed Augmentin to fight off the bacteria, Pan-D to protect your stomach lining from acidity, Dolo for fever relief, and Levocet-M at night to calm your throat and reduce nasal congestion. Remember to drink plenty of fluids and never stop your antibiotic course midway.",
        "hindi_summary": "आपको सांस की नली में बैक्टीरियल इन्फेक्शन हुआ है। डॉक्टर ने इन्फेक्शन खत्म करने के लिए ऑगमेंटिन (एंटीबायोटिक), पेट में गैस से बचाव के लिए पैन-डी खाली पेट, और बुखार व बदन दर्द के लिए डोलो 650 दी है। रात को सोने से पहले एलर्जी की गोली लें। एंटीबायोटिक का पूरा 5 दिन का कोर्स जरूर पूरा करें।"
    },
    "sample_cardiac_conflict": {
        "id": "sample_cardiac_conflict",
        "title": "Cardiology & Diabetes: High-Risk Conflict Check",
        "doctor": "Dr. Ananya Roy, DNB (Cardiology)",
        "patient": "Kishan Lal, 62 M",
        "diagnosis": "Type 2 Diabetes Mellitus + Hypertension + Mild Ischemic Heart Disease",
        "image_url": "/static/images/sample_rx2.svg",
        "medicines": [
            {
                "name": "Telmisartan",
                "generic": "Telmisartan 40mg",
                "dosage": "40 mg",
                "frequency": "Once daily morning (1 - 0 - 0)",
                "duration": "Continuous / 30 days",
                "timing": "Morning after breakfast",
                "purpose": "Angiotensin receptor blocker to control hypertension and protect kidneys",
                "food_instruction": "Consistent timing every morning",
                "badge": "BP / Cardiac",
                "color": "blue"
            },
            {
                "name": "Metformin Extended Release",
                "generic": "Metformin ER 500mg",
                "dosage": "500 mg",
                "frequency": "Twice daily (1 - 0 - 1)",
                "duration": "Continuous / 30 days",
                "timing": "With breakfast and dinner",
                "purpose": "Controls blood sugar and enhances insulin sensitivity",
                "food_instruction": "Always take with food to minimize GI distress",
                "badge": "Antidiabetic",
                "color": "emerald"
            },
            {
                "name": "Ecosprin (Aspirin)",
                "generic": "Low-dose Enteric Coated Aspirin 75mg",
                "dosage": "75 mg",
                "frequency": "Once daily (0 - 1 - 0)",
                "duration": "Continuous",
                "timing": "Post lunch",
                "purpose": "Antiplatelet blood thinner preventing arterial clots and stroke",
                "food_instruction": "Take after a meal with water",
                "badge": "Blood Thinner",
                "color": "amber"
            },
            {
                "name": "Ibuprofen (Added OTC for Knee Pain)",
                "generic": "Ibuprofen 400mg NSAID",
                "dosage": "400 mg",
                "frequency": "Twice daily",
                "duration": "Self-medicated",
                "timing": "With food",
                "purpose": "Pain relief for joint arthritis",
                "food_instruction": "Take with meals",
                "badge": "NSAID",
                "color": "rose"
            }
        ],
        "conflicts_and_warnings": [
            {
                "severity": "danger",
                "title": "CRITICAL DRUG-DRUG INTERACTION: Ibuprofen + Aspirin",
                "description": "NSAIDs like Ibuprofen competitively block Aspirin's antiplatelet binding, eliminating its cardioprotective effect. Furthermore, combining both significantly increases the risk of severe stomach bleeding and ulcers."
            },
            {
                "severity": "warning",
                "title": "Renal Caution: Ibuprofen + Telmisartan",
                "description": "Concurrent use of NSAIDs and ARBs (Telmisartan) may impair renal blood flow and precipitate acute kidney injury in elderly diabetic patients."
            }
        ],
        "daily_schedule": {
            "morning": [
                {"time": "08:00 AM", "medicine": "Telmisartan 40mg", "instruction": "Take with breakfast for blood pressure control", "icon": "🌅"},
                {"time": "08:15 AM", "medicine": "Metformin ER 500mg", "instruction": "Take midway through your morning meal", "icon": "💊"}
            ],
            "afternoon": [
                {"time": "01:30 PM", "medicine": "Ecosprin 75mg", "instruction": "Take after lunch with water", "icon": "☀️"}
            ],
            "evening": [
                {"time": "08:30 PM", "medicine": "Metformin ER 500mg", "instruction": "Take during dinner", "icon": "🌙"},
                {"time": "ACTION REQUIRED", "medicine": "STOP Ibuprofen 400mg", "instruction": "Replace with Paracetamol after consulting your physician", "icon": "⚠️"}
            ]
        },
        "plain_english_summary": "URGENT SAFETY ALERT: You are prescribed Aspirin to protect your heart and Telmisartan for blood pressure. Taking Ibuprofen alongside Aspirin is dangerous: it cancels out the heart-protecting benefit of Aspirin and raises the risk of severe stomach bleeding and kidney stress. Stop Ibuprofen immediately and speak with your doctor for safer pain options like topical gels or Paracetamol.",
        "hindi_summary": "महत्वपूर्ण चेतावनी: दिल की सुरक्षा के लिए आपको एस्पिरिन और बीपी के लिए टेलमिसार्टन दी गई है। इसके साथ आइबुप्रोफेन (पेनकिलर) लेना खतरनाक हो सकता है क्योंकि यह एस्पिरिन के असर को खत्म करता है और पेट में ब्लीडिंग तथा किडनी पर दबाव बढ़ाता है। आइबुप्रोफेन तुरंत बंद करें और डॉक्टर की सलाह लें।"
    },
    "sample_lab_report": {
        "id": "sample_lab_report",
        "title": "Diagnostic Lab: Metabolic Panel & Lipid Screen",
        "doctor": "Metropolis Diagnostics - Dr. P. Mehta, Pathologist",
        "patient": "Sneha Gupta, 45 F",
        "diagnosis": "Comprehensive Metabolic & Lipid Health Checkup",
        "image_url": "/static/images/sample_lab1.svg",
        "medicines": [
            {
                "name": "Atorvastatin (Recommended)",
                "generic": "Atorvastatin Calcium 10mg",
                "dosage": "10 mg",
                "frequency": "Once daily at night (0 - 0 - 1)",
                "duration": "Doctor consultation required",
                "timing": "After dinner",
                "purpose": "HMG-CoA reductase inhibitor to reduce LDL cholesterol and cardiovascular risk",
                "food_instruction": "Evening dose before bedtime",
                "badge": "Lipid Lowering",
                "color": "blue"
            },
            {
                "name": "Vitamin D3 (Cholecalciferol)",
                "generic": "Cholecalciferol 60,000 IU",
                "dosage": "60,000 IU",
                "frequency": "Once weekly for 8 weeks",
                "duration": "8 weeks",
                "timing": "Sunday morning after milk/breakfast",
                "purpose": "Corrects severe Vitamin D deficiency for bone density and immune function",
                "food_instruction": "Must be taken with fat-containing meal/milk for absorption",
                "badge": "Vitamin",
                "color": "amber"
            }
        ],
        "conflicts_and_warnings": [
            {
                "severity": "warning",
                "title": "High Total Cholesterol (248 mg/dL) & High LDL (158 mg/dL)",
                "description": "Your bad cholesterol (LDL) is elevated above the 100 mg/dL target. Lifestyle modification and physician-guided statin therapy are advised."
            },
            {
                "severity": "caution",
                "title": "Vitamin D3 Deficiency (14.2 ng/mL)",
                "description": "Values under 20 ng/mL indicate deficiency. Can cause bone aches, fatigue, and muscle weakness."
            }
        ],
        "daily_schedule": {
            "morning": [
                {"time": "09:00 AM (Sundays)", "medicine": "Vitamin D3 60K IU", "instruction": "Take once a week with a glass of milk", "icon": "🥛"}
            ],
            "afternoon": [
                {"time": "Daily Routine", "medicine": "30 mins brisk walking", "instruction": "Recommended to assist cholesterol reduction", "icon": "👟"}
            ],
            "evening": [
                {"time": "09:30 PM", "medicine": "Atorvastatin 10mg", "instruction": "Nightly after dinner (if approved by physician)", "icon": "🌙"}
            ]
        },
        "plain_english_summary": "Your lab results indicate elevated LDL (bad cholesterol) and low Vitamin D3 levels. Your blood sugar is currently within normal limits. A weekly Vitamin D3 supplement is strongly recommended along with heart-healthy dietary changes (reduced saturated fats) and a doctor visit to evaluate if daily cholesterol-lowering medication is needed.",
        "hindi_summary": "आपकी लैब रिपोर्ट के अनुसार आपका एलडीएल (खराब कोलेस्ट्रॉल) बढ़ा हुआ है और विटामिन डी3 काफी कम है। हड्डियों की मजबूती और थकान दूर करने के लिए हफ्ते में एक बार विटामिन डी3 सप्लीमेंट दूध के साथ लें। कोलेस्ट्रॉल नियंत्रित करने के लिए तैलीय भोजन कम करें और चिकित्सक से परामर्श लें।"
    }
}
