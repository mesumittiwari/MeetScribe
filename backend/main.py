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
import google.generativeai as genai

load_dotenv()

# --- API and App Initialization ---
app = FastAPI(title="AI Meeting Summarizer API")
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"FATAL: Error configuring Google AI client: {e}")
    gemini_model = None

HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
WHISPER_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

origins = ["http://localhost:5173", "http://127.0.0.1:5173", "https://ai-meeting-summarizer-1-sfrq.onrender.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    if not HUGGING_FACE_API_KEY:
        raise HTTPException(status_code=501, detail="Hugging Face API key not found. Transcription feature is disabled.")

    
    file_content = await file.read()
    
# Determine the content type based on file extension or use a default audio mime type
    content_type = file.content_type
    if not content_type or content_type == "application/octet-stream":
        # Try to infer from filename if content_type is not specific
        filename = file.filename.lower()
        if filename.endswith('.mp3'):
            content_type = 'audio/mpeg'
        elif filename.endswith('.wav'):
            content_type = 'audio/wav'
        else:
            # Default to a common audio format if we can't determine
            content_type = 'audio/mpeg'

    # Add content_type to headers
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
        "Content-Type": content_type
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client: # Increased timeout for large files
            response = await client.post(WHISPER_API_URL, headers=headers, data=file_content)



        if response.status_code != 200:
            print(f"Hugging Face API Error: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"Transcription service failed: {response.json().get('error', 'Unknown error')}")

        result = response.json()
        return {"transcript": result.get("text", "No transcript found in response.")}

    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio. Error: {str(e)}")


@app.post("/summarize")
async def summarize_transcript(data: dict = Body(...)):
    if not gemini_model:
        raise HTTPException(status_code=500, detail="Gemini AI model not initialized.")
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
        generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
        response = await gemini_model.generate_content_async(prompt, generation_config=generation_config)
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process with Gemini. Error: {str(e)}")

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
