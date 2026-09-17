# 🔬 MedLens — AI Medical Prescription & Lab Report Decoder

> **Hackathon Pitch Tagline**: *Bridging the gap between doctor handwriting and patient safety with multimodal vision AI, drug conflict detection, and multilingual voice assistance.*

---

## 🌟 Key Features

1. **📷 Vision Handwriting & Lab OCR**:
   - Transcribes illegible cursive doctor prescriptions and diagnostic lab panels.
   - Extracts Brand Name, Active Compound (Generic), Dosage, Frequency, and Food Instructions.

2. **🛡️ Drug-Drug Conflict Radar**:
   - Cross-references prescribed medicines against clinical contraindication rules (e.g. flagging deadly **Aspirin + Ibuprofen** or **Telmisartan + NSAID** interactions).
   - Shows intuitive severity badges: 🟢 Safe, 🟡 Caution, 🔴 Critical Risk.

3. **⏰ 24-Hour Patient Routine Timeline**:
   - Automatically segments medications into **Morning (Breakfast)**, **Afternoon (Lunch)**, and **Night (Dinner & Bedtime)** slots.

4. **🗣️ "Explain Like I'm 5" Voice Narration**:
   - Translates complex pharmacology into simple, comforting language.
   - Native audio playback in **English** and **Hindi (हिंदी)** for rural and elderly patients.

5. **📅 1-Click Calendar Sync (.ics)**:
   - Exports medication schedules with alarms directly into Google Calendar, Apple Calendar, or Outlook.

6. **⚡ Built-in Demo Presets**:
   - Pre-packaged clinical test cases (Antibiotics Rx, Cardiac Conflict Rx, Blood Lab Report) ensuring zero failure during live hackathon judging even without Wi-Fi.

---

## 🚀 How to Run Locally

### 1. Open Terminal and Navigate to Project
```powershell
cd "c:\Users\djbab\OneDrive\Documents\Tejas study\practice sheet\medlens"
```

### 2. Start the Server
```powershell
python server.py
```
*The app will be live at **http://127.0.0.1:8000**.*

---

## 🎬 2-Minute Hackathon Demo Script (How to Win the Judges)

1. **The Hook (0:00 - 0:30)**:
   > *"Every year, millions of patients suffer from medication errors simply because they can't read their doctor's handwriting or don't understand the dosage schedule. We built MedLens to eliminate this risk."*

2. **The Live Demo (0:30 - 1:15)**:
   > * Click on the **"Cardiology: High-Risk Conflict Demo"** preset.
   > * Point out the **Red Flashing Alert**:
   >   *"Notice what MedLens caught: The patient was taking Aspirin for their heart, but added Ibuprofen for knee pain. MedLens immediately flagged this critical conflict because Ibuprofen cancels Aspirin's antiplatelet protection and causes stomach ulcers."*

3. **Accessibility & Voice (1:15 - 1:40)**:
   > * Switch Language to **हिंदी (Hindi)**.
   > * Click the **Play (▶)** button.
   > * The AI voice explains the medicine instructions out loud.
   >   *"This empowers elderly or illiterate patients who cannot read medical labels."*

4. **1-Click Utility (1:40 - 2:00)**:
   > * Click **"📅 Add to Calendar (.ics)"**. Show the downloaded calendar file that schedules daily phone alarms for each dose.
   >   *"With MedLens, safe healthcare is just one photo away."*

---

## 🛠️ Project Structure
```
medlens/
├── server.py              # FastAPI server & static file host
├── analyzer.py            # Vision AI engine & clinical interaction checker
├── samples.py             # Pre-configured test cases & offline fallbacks
├── requirements.txt       # Dependencies
├── README.md              # Project documentation & pitch guide
└── static/
    ├── index.html         # Modern web interface
    ├── style.css          # Glassmorphism dark-slate design system
    ├── app.js             # Client logic (TTS, drag-drop, calendar export)
    └── images/            # SVG prescription illustrations
```
