import os
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, JSONResponse

from samples import SAMPLE_DATA
from analyzer import analyze_image_with_ai

app = FastAPI(
    title="MedLens API",
    description="AI Prescription & Medical Report Decoder with Interactive Schedules and Safety Warnings",
    version="1.0.0"
)

# Enable CORS for local testing & live demos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "MedLens", "version": "1.0.0"}

@app.get("/api/samples")
async def get_samples():
    """Return catalog of ready-to-test sample prescriptions."""
    catalog = []
    for key, val in SAMPLE_DATA.items():
        catalog.append({
            "id": val["id"],
            "title": val["title"],
            "doctor": val["doctor"],
            "diagnosis": val["diagnosis"],
            "medicines_count": len(val["medicines"]),
            "has_conflict": any(c["severity"] in ["warning", "danger"] for c in val.get("conflicts_and_warnings", []))
        })
    return {"samples": catalog}

@app.get("/api/sample/{sample_id}")
async def get_sample_detail(sample_id: str):
    """Fetch full decoded data for a specific sample preset."""
    if sample_id in SAMPLE_DATA:
        return SAMPLE_DATA[sample_id]
    raise HTTPException(status_code=404, detail="Sample not found")

@app.post("/api/analyze")
async def analyze_prescription(
    file: UploadFile = File(None),
    sample_id: str = Form(None),
    api_key: str = Form(None)
):
    """
    Decodes an uploaded prescription image or switches to selected sample.
    """
    # 1. Check if user picked a pre-loaded sample
    if sample_id and sample_id in SAMPLE_DATA:
        return JSONResponse(content=SAMPLE_DATA[sample_id])

    # 2. Process uploaded file
    if file and file.filename:
        content = await file.read()
        mime_type = file.content_type or "image/jpeg"
        result = analyze_image_with_ai(content, mime_type=mime_type, api_key=api_key)
        return JSONResponse(content=result)

    # 3. Fallback default case
    return JSONResponse(content=SAMPLE_DATA["sample_antibiotics"])

@app.post("/api/export-ics")
async def export_calendar(data: dict):
    """
    Generates an RFC 5545 standard .ics file so users can add
    all prescribed medicine dosage reminders directly to Google or Apple Calendar.
    """
    medicines = data.get("medicines", [])
    schedule = data.get("daily_schedule", {})
    patient = data.get("patient", "Patient")

    now = datetime.now()
    dtstamp = now.strftime("%Y%m%dT%H%M%SZ")

    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MedLens//AI Prescription Scheduler//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:MedLens Medication Schedule",
        "X-WR-TIMEZONE:UTC"
    ]

    event_id = 1
    # Generate daily recurring alarms for the next 7 days for each scheduled pill
    slot_times = {
        "morning": ("08:00", 8, 0),
        "afternoon": ("13:30", 13, 30),
        "evening": ("20:30", 20, 30)
    }

    for slot, items in schedule.items():
        if slot in slot_times:
            label, hour, minute = slot_times[slot]
            for item in items:
                med_name = item.get("medicine", "Medication")
                instruction = item.get("instruction", "")
                
                # Start tomorrow at this hour
                start_dt = (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0)
                end_dt = start_dt + timedelta(minutes=15)
                
                start_str = start_dt.strftime("%Y%m%dT%H%M%S")
                end_str = end_dt.strftime("%Y%m%dT%H%M%S")
                
                ics_lines.extend([
                    "BEGIN:VEVENT",
                    f"UID:medlens-{event_id}-{dtstamp}@medlens.ai",
                    f"DTSTAMP:{dtstamp}",
                    f"DTSTART:{start_str}",
                    f"DTEND:{end_str}",
                    "RRULE:FREQ=DAILY;COUNT=7",
                    f"SUMMARY:💊 MedLens Reminder: {med_name}",
                    f"DESCRIPTION:{instruction} | Patient: {patient}",
                    "STATUS:CONFIRMED",
                    "BEGIN:VALARM",
                    "TRIGGER:-PT5M",
                    "ACTION:DISPLAY",
                    f"DESCRIPTION:Time to take {med_name}",
                    "END:VALARM",
                    "END:VEVENT"
                ])
                event_id += 1

    ics_lines.append("END:VCALENDAR")
    ics_content = "\r\n".join(ics_lines)

    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=medlens_schedule.ics"}
    )

# Mount static files (HTML, CSS, JS, SVG assets)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "MedLens static frontend building in progress..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
