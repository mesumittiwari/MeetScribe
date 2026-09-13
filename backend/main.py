# backend/main.py
import os
import json
import smtplib
import httpx

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from google import genai
from groq import Groq

load_dotenv()
# --- API Keys ---

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not configured.")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- API and App Initialization ---
app = FastAPI(title="AI Meeting Summarizer API")
try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        print("WARNING: GOOGLE_API_KEY is not configured.")
        gemini_client = None
    else:
        gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

except Exception as e:
    print(f"FATAL: Error configuring Google AI client: {e}")
    gemini_client = None



origins = ["http://localhost:5173", "http://127.0.0.1:5173", "https://ai-meeting-summarizer-1-sfrq.onrender.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "Backend is healthy!"}



# --- Helper Function for Email Formatting ---
def format_summary_as_html(data: dict) -> str:
    # This function remains the same as before...
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; }}
            h2 {{ color: #0d9488; border-bottom: 2px solid #ccfbf1; padding-bottom: 5px; }}
            ul {{ list-style-type: none; padding-left: 0; }}
            li {{ background-color: #f0fdfa; margin-bottom: 8px; padding: 10px; border-left: 4px solid #14b8a6; border-radius: 4px;}}
            p {{ margin-bottom: 10px; }}
            .section {{ background-color: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #e2e8f0; }}
        </style>
    </head>
    <body>
        <h1>Meeting Analysis Report</h1>
        <div class="section">
            <h2>📄 Meeting Summary</h2><p>{data.get('summary', 'N/A')}</p>
        </div>
        <div class="section">
            <h2>🎯 Client Pain Points</h2><ul>{''.join(f"<li>{item}</li>" for item in data.get('painPoints', []))}</ul>
        </div>
        <div class="section">
            <h2>🤔 Objections & Resolutions</h2><ul>{''.join(f"<li>{item}</li>" for item in data.get('objections', []))}</ul>
        </div>
        <div class="section">
            <h2>🚀 Next Steps</h2><ul>{''.join(f"<li>{item}</li>" for item in data.get('nextSteps', []))}</ul>
        </div>
        <div class="section">
            <h2>🕒 Timeline</h2><ul>{''.join(f"<li><b>{item.get('time', '')}:</b> {item.get('topic', '')}</li>" for item in data.get('timeline', []))}</ul>
        </div>
    </body>
    </html>
    """
    return html

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "AI Summarizer Backend is running."}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not groq_client:
        raise HTTPException(
            status_code=501,
            detail="Groq API key not configured. Transcription feature is disabled."
        )

    try:
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty."
            )

        print(
            f"Transcription started: {file.filename} "
            f"({len(file_content) / (1024 * 1024):.2f} MB)"
        )

        transcription = groq_client.audio.transcriptions.create(
            file=(file.filename, file_content),
            model="whisper-large-v3-turbo",
            response_format="json",
            temperature=0.0
        )

        transcript = transcription.text.strip()

        print(
            f"Transcription completed: {len(transcript)} characters"
        )

        return {
            "transcript": transcript
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"Transcription error: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to transcribe audio. Error: {str(e)}"
        )


@app.post("/summarize")
async def summarize_transcript(data: dict = Body(...)):
    if not gemini_client:
        raise HTTPException(status_code=501, detail="Gemini API key not configured. Summarization is disabled.")
    transcript = data.get("transcript")
    if not transcript or len(transcript.strip()) < 20:
        raise HTTPException(status_code=400, detail="Please provide a valid transcript.")

    prompt = f"""
    Analyze the following meeting transcript and generate a structured JSON output.
    Your entire response must be a single, valid JSON object.
    The JSON object must only contain these keys: "summary", "painPoints", "objections", "nextSteps", "timeline".
    - "summary": A concise paragraph summarizing the entire meeting.
    - "painPoints": An array of strings, with each string being a key problem or challenge the client mentioned.
    - "objections": An array of strings, with each string being an objection raised by the client and how it was addressed. If none, return an empty array.
    - "nextSteps": An array of strings, with each string being a concrete action item or follow-up.
    - "timeline": An array of objects, where each object has two keys: "time" (e.g., "Start", "Mid-point", "End") and "topic" (a string describing the main discussion point at that time).
    Transcript:
    ---
    {transcript}
    ---
    """
    try:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        print("Gemini response received successfully.")

        return json.loads(response.text)

    except Exception as e:
        print(f"Gemini summarization error: {repr(e)}")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process with Gemini. Error: {str(e)}"
        )

@app.post("/email_summary")
async def email_summary(data: dict = Body(...)):
    host, port_str, user, password, recipient = (os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PORT"), os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"), os.getenv("EMAIL_RECIPIENT"))
    if not all([host, port_str, user, password, recipient]):
        raise HTTPException(status_code=501, detail="Email service is not configured.")
    try:
        port = int(port_str)
        html_content = format_summary_as_html(data)
        message = MIMEMultipart("alternative")
        message["Subject"], message["From"], message["To"] = "Your AI Meeting Summary Report", user, recipient
        message.attach(MIMEText(html_content, "html"))
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(user, recipient, message.as_string())
        return {"message": f"Summary successfully sent to {recipient}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email. Error: {str(e)}")
