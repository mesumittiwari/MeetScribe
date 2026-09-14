# MeetScribe – AI Meeting Intelligence

![Project Banner](https://github.com/user-attachments/assets/e61ab72a-c820-4daa-b753-8be9d39ca3d2)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Transcription](https://img.shields.io/badge/Transcription-Groq%20Whisper-orange)](https://groq.com/)
[![LLM](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Email](https://img.shields.io/badge/Email-Resend-000000)](https://resend.com/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E0B4?logo=render&logoColor=white)](https://render.com/)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [AI Processing Flow](#ai-processing-flow)
- [Technologies Used](#technologies-used)
- [Supported File Formats](#supported-file-formats)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Security Considerations](#security-considerations)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Live Demo](#live-demo)
- [Demo](#demo)
- [Repository](#repository)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)
- [Author](#author)

---

## Overview

**MeetScribe** is a full-stack AI meeting intelligence application that transforms meeting recordings into structured, actionable insights.

Instead of manually reviewing an entire meeting recording, users can upload an audio or supported video file, generate a transcript using **Groq Whisper**, and send the transcript to **Google Gemini** for structured analysis.

MeetScribe extracts the most useful information from a meeting, including:

- 📄 **Meeting Summary**
- 🎯 **Client Pain Points**
- 🤔 **Objections & Resolutions**
- 🚀 **Next Steps**
- 🕒 **Discussion Timeline**

The generated results can then be downloaded as **JSON or CSV**, or delivered to a user-provided email address using **Resend**.

The application demonstrates a complete full-stack workflow involving a React frontend, FastAPI backend, third-party AI APIs, file validation, structured AI output, client-side exports, email delivery, and cloud deployment.

---

## Features

### 🎙️ Multi-Format Transcription

Upload supported audio and video files and generate a transcript using **Groq Whisper**.

Supported formats include:

- MP3
- WAV
- M4A
- MP4
- MPEG
- MPGA
- OGG
- FLAC
- WEBM

The application validates the file size before uploading it for transcription.

**Maximum file size: 25 MB**

---

### 🧠 AI-Powered Meeting Analysis

MeetScribe sends the generated transcript to **Google Gemini** and produces structured meeting intelligence rather than a plain text summary.

The analysis includes:

- Meeting Summary
- Client Pain Points
- Objections & Resolutions
- Next Steps
- Discussion Timeline

---

### 📤 Export Results

Meeting analysis can be exported directly from the frontend as:

- **JSON**
- **CSV**

This makes the generated information easy to store, process, or integrate with other workflows.

---

### 📧 Email Meeting Reports

Users can enter their own email address and send the generated meeting report directly from the application.

Email delivery is handled through the **Resend API** over HTTPS.

The recipient email address is entered by the user and is not hardcoded into the frontend.

---

### ⚡ Fast AI Transcription

MeetScribe uses **Groq Whisper** for transcription instead of running Whisper locally.

This keeps the backend lightweight while providing fast speech-to-text processing.

---

### 🛡️ File Validation

The application validates uploaded files on both the frontend and backend.

Validation includes:

- Supported file extension
- Maximum file size
- Empty file detection

The frontend provides an immediate error when a file exceeds the 25 MB limit, while the backend performs its own validation before sending the file to Groq.

---

### 🌐 Production Deployment

MeetScribe is deployed using **Render** and uses REST APIs for communication between the frontend and backend.

---

## How It Works

```text
                         ┌──────────────────────┐
                         │     User Uploads     │
                         │    Audio / Video     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Frontend Validation │
                         │      Max 25 MB       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Groq Whisper     │
                         │    Transcription     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Transcript      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Google Gemini     │
                         │  Meeting Intelligence│
                         └──────────┬───────────┘
                                    │
                                    ▼
                   ┌────────────────────────────────┐
                   │       Structured Results       │
                   │                                │
                   │  • Meeting Summary             │
                   │  • Client Pain Points          │
                   │  • Objections & Resolutions    │
                   │  • Next Steps                  │
                   │  • Discussion Timeline         │
                   └───────────────┬────────────────┘
                                   │
                     ┌─────────────┼─────────────┐
                     ▼             ▼             ▼
                ┌─────────┐   ┌─────────┐   ┌─────────┐
                │   JSON  │   │   CSV   │   │  Email  │
                │  Export │   │  Export │   │  Resend │
                └─────────┘   └─────────┘   └─────────┘
```

---

## AI Processing Flow

### 1. 🔊 Audio / Video Upload

The user selects an audio or supported video file through the React frontend.

Before uploading, the frontend checks the file size.

```text
Maximum file size: 25 MB
```

If the file exceeds the limit:

- The file is not uploaded.
- Transcription is not started.
- An upload error is displayed immediately.

Users can compress larger audio files or extract audio from larger video files before uploading.

---

### 2. 🛡️ Backend File Validation

The FastAPI backend receives the uploaded file and performs additional validation.

The backend checks:

- File extension
- File size
- Empty uploads

This provides a second layer of validation before the file is sent to the external transcription service.

---

### 3. 🎙️ Transcription via Groq Whisper

The validated file is sent to Groq using the Whisper transcription model:

```text
whisper-large-v3-turbo
```

Groq Whisper converts the meeting recording into a text transcript.

The generated transcript is returned to the FastAPI backend and then displayed in the React frontend.

---

### 4. 📝 Transcript Review

The generated transcript is displayed in the **Transcription Result** section.

The user can review the transcript and click:

```text
Copy to Analysis Input →
```

This copies the generated transcript into the analysis input field.

Users can also paste their own transcript directly into the analysis input.

---

### 5. 🧠 Meeting Analysis via Google Gemini

The transcript is sent to the FastAPI `/summarize` endpoint.

The backend sends the transcript to **Google Gemini** and requests structured JSON output.

Gemini analyzes the transcript and extracts:

```text
Meeting Summary
Client Pain Points
Objections & Resolutions
Next Steps
Discussion Timeline
```

---

### 6. 📊 Structured Results

The generated results are displayed in separate sections in the frontend.

This makes it easier to identify important information without manually searching through the complete transcript.

---

### 7. 📤 Export and Email

Once the analysis is complete, users can:

- Download the results as JSON
- Download the results as CSV
- Send the meeting report to an email address

Email delivery is handled through **Resend**.

---

## Technologies Used

### Frontend

- **React** – User interface and application state management
- **Vite** – Frontend development and production build tooling
- **Tailwind CSS** – Responsive styling
- **Axios** – HTTP communication with the backend
- **FileSaver.js** – Client-side JSON and CSV downloads

### Backend

- **Python** – Backend programming language
- **FastAPI** – REST API framework
- **Uvicorn** – ASGI server
- **python-dotenv** – Environment variable management
- **python-multipart** – Multipart file upload handling

### AI Services

- **Groq Whisper** – Speech-to-text transcription
- **Google Gemini** – AI-powered meeting analysis and structured insight generation

### Email

- **Resend** – Transactional email delivery through HTTPS

### Development & Deployment

- **Git** – Version control
- **GitHub** – Source code hosting
- **Render** – Cloud deployment
- **Vite** – Production frontend build

---

## Supported File Formats

| Format | Supported |
|---|---|
| MP3 | ✅ |
| WAV | ✅ |
| M4A | ✅ |
| MP4 | ✅ |
| MPEG | ✅ |
| MPGA | ✅ |
| OGG | ✅ |
| FLAC | ✅ |
| WEBM | ✅ |

### File Size Limit

```text
Maximum upload size: 25 MB
```

The 25 MB limit is enforced on both the frontend and backend.

If your recording exceeds the limit, you can:

- Compress the audio file
- Extract the audio track from the video
- Upload the resulting file if it is below 25 MB

---

## Getting Started

Follow the steps below to run MeetScribe locally.

### Prerequisites

Make sure the following are installed:

- Python 3.9+
- pip
- Node.js
- npm
- Git

You will also need API credentials for:

- Groq
- Google Gemini
- Resend

---

## Clone the Repository

```bash
git clone https://github.com/mesumittiwari/MeetScribe.git
cd MeetScribe
```

---

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
.\venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

---

## Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

---

## Environment Variables

The backend uses environment variables to store API credentials.

Create the following file:

```text
backend/.env
```

Add:

```dotenv
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_gemini_api_key
RESEND_API_KEY=your_resend_api_key
```

### Important

Never commit your `.env` file to GitHub.

Make sure `.env` is included in `.gitignore`.

---

## Running the Application

### Start the Backend

From the `backend` directory:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

---

### Start the Frontend

From the `frontend` directory:

```bash
npm run dev
```

Vite will provide a local development URL, typically:

```text
http://localhost:5173
```

The frontend uses the following environment variable to determine the backend URL:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If this variable is not configured, the application defaults to:

```text
http://127.0.0.1:8000
```

---

## Usage

### Step 1 — Upload a Meeting Recording

Click **Upload Audio** and select a supported audio or video file.

MeetScribe supports:

```text
MP3, WAV, M4A, MP4, MPEG, MPGA, OGG, FLAC, WEBM
```

The maximum supported file size is:

```text
25 MB
```

---

### Step 2 — Generate the Transcript

After a valid file is selected:

1. The frontend validates the file.
2. The file is sent to the FastAPI backend.
3. The backend validates the file again.
4. The file is sent to Groq Whisper.
5. Whisper generates the transcript.
6. The transcript is returned to the frontend.

---

### Step 3 — Review the Transcript

The generated transcript appears under **Transcription Result**.

Review the transcript and click:

```text
Copy to Analysis Input →
```

The transcript will then be placed in the analysis text area.

---

### Step 4 — Analyze the Meeting

Click:

```text
✨ Analyze Transcript
```

The transcript is sent to Google Gemini for structured meeting analysis.

---

### Step 5 — Review the Results

MeetScribe displays:

- 📄 Meeting Summary
- 🎯 Client Pain Points
- 🤔 Objections & Resolutions
- 🚀 Next Steps
- 🕒 Discussion Timeline

---

### Step 6 — Export Results

The analysis can be downloaded as:

```text
meeting_summary.json
meeting_summary.csv
```

Use:

```text
Export JSON
```

or:

```text
Export CSV
```

---

### Step 7 — Email the Report

Click:

```text
📧 Email Summary
```

Enter the recipient's email address and click:

```text
Send Report
```

The FastAPI backend sends the report through Resend.

---

## API Endpoints

### `POST /transcribe`

Uploads an audio/video file and generates a transcript using Groq Whisper.

#### Request

```text
Content-Type: multipart/form-data

file=<audio/video file>
```

#### Response

```json
{
  "transcript": "Generated meeting transcript..."
}
```

---

### `POST /summarize`

Analyzes a transcript using Google Gemini.

#### Request

```json
{
  "transcript": "Meeting transcript..."
}
```

#### Response

The endpoint returns structured meeting intelligence containing:

```text
summary
painPoints
objections
nextSteps
timeline
```

---

### `POST /email_summary`

Sends the generated meeting report to a user-provided email address through Resend.

#### Request

```json
{
  "summary": "Meeting summary...",
  "painPoints": [],
  "objections": [],
  "nextSteps": [],
  "timeline": [],
  "email": "recipient@example.com"
}
```

#### Response

```json
{
  "message": "Summary successfully sent to recipient@example.com"
}
```

---

## Project Structure

```text
MeetScribe/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── ...
│   ├── package.json
│   ├── package-lock.json
│   └── ...
│
├── .gitignore
└── README.md
```

> `.env` should remain local and must never be committed to the repository.

---

## Deployment

MeetScribe can be deployed using separate frontend and backend services.

### Backend Deployment

The FastAPI backend can be deployed on a cloud platform such as Render.

Configure the following environment variables in the deployment platform:

```text
GROQ_API_KEY
GOOGLE_API_KEY
RESEND_API_KEY
```

The backend should be started using:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

### Frontend Deployment

Build the React frontend using:

```bash
npm run build
```

Vite generates the production build.

Configure:

```text
VITE_API_BASE_URL
```

to point to the deployed FastAPI backend.

---

### CORS Configuration

The FastAPI backend uses CORS configuration to allow requests from the frontend.

When deploying the frontend to a different domain, the corresponding frontend URL should be added to the backend's allowed origins.

---

## Security Considerations

### API Keys

API credentials are stored using environment variables:

```text
GROQ_API_KEY
GOOGLE_API_KEY
RESEND_API_KEY
```

API keys should never be exposed in frontend source code.

---

### File Validation

Uploaded files are validated on both sides of the application.

The current validation includes:

```text
Supported extensions
Maximum file size: 25 MB
Empty file detection
```

---

### Email Validation

The frontend performs basic validation of the recipient's email address before sending the request to the backend.

---

### Environment Files

The backend `.env` file contains sensitive credentials and should never be committed to source control.

---

## Limitations

- Maximum upload size is currently **25 MB**.
- Transcription depends on the availability and limits of the Groq API.
- Meeting analysis depends on the availability and limits of the Google Gemini API.
- Email delivery depends on Resend configuration and service availability.
- AI-generated output may contain inaccuracies and should be reviewed before being used for important decisions.
- The current version does not provide speaker diarization.
- The current version does not provide persistent meeting history.
- The current version does not include user authentication.
- Large recordings may need to be compressed or have their audio extracted before upload.

---

## Future Improvements

Potential future improvements include:

- 🎤 Speaker identification and diarization
- 📁 Larger file support through server-side audio extraction/compression
- 👤 User authentication
- 🗂️ Persistent meeting history
- 🔎 Meeting search
- 📊 Meeting analytics dashboard
- 📅 Calendar integrations
- 🔔 Automatic action-item reminders
- 📑 Additional export formats
- 🎙️ Real-time transcription
- ⚙️ Background processing for long recordings
- 🔄 Automatic retry mechanisms
- 🧪 Expanded automated testing
- 🚀 More comprehensive CI/CD pipelines

---

## Live Demo

🚀 **Live Application:**

https://ai-meeting-summarizer-1-sfrq.onrender.com/

> Update this URL if the Render service is changed to a MeetScribe-branded URL.

---

## Demo

[![Watch the Demo](https://img.youtube.com/vi/ZccZPmXawIw/maxresdefault.jpg)](https://youtu.be/ZccZPmXawIw)

---

## Repository

💻 **GitHub Repository:**

https://github.com/mesumittiwari/MeetScribe

---

## Contact

**Sumit Tiwari**

📧 Email: [sumittiwari2414@gmail.com](mailto:sumittiwari2414@gmail.com)

🔗 GitHub: [mesumittiwari](https://github.com/mesumittiwari)

🔗 LinkedIn: [linkedin.com/in/mesumittiwari](https://www.linkedin.com/in/mesumittiwari/)

---

## Acknowledgments

MeetScribe is built using the following technologies and services:

- [React](https://react.dev/) – Frontend user interface
- [Vite](https://vite.dev/) – Frontend development and production build tooling
- [Tailwind CSS](https://tailwindcss.com/) – Responsive styling
- [FastAPI](https://fastapi.tiangolo.com/) – Backend REST API framework
- [Groq](https://groq.com/) – Fast AI inference and Whisper transcription
- [Google Gemini](https://ai.google.dev/) – AI-powered meeting analysis
- [Resend](https://resend.com/) – Email delivery
- [Render](https://render.com/) – Cloud deployment
- [GitHub](https://github.com/) – Source control and repository hosting

---

## Author

**MeetScribe – AI Meeting Intelligence**

Built by **Sumit Tiwari**.




































# AI-Meeting-Summarizer

![Project Banner](https://github.com/user-attachments/assets/e61ab72a-c820-4daa-b753-8be9d39ca3d2)


[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Backend-FastAPI%20/%20Flask-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![Language Model](https://img.shields.io/badge/LLM-Gemini%20/%20HuggingFace-orange?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/mesumittiwari/AI-Meeting-Summarizer)](https://github.com/mesumittiwari/AI-Meeting-Summarizer/commits/main)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E0B4?logo=render&logoColor=white)](https://render.com/) 

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Local Installation](#local-installation)
    * [Environment Variables](#environment-variables)
    * [Running the Backend](#running-the-backend)
    * [Running the Frontend](#running-the-frontend)
* [Usage](#usage)
* [Project Structure](#-project-structure)
* [Deployment](#-deployment)
* [Contact](#-contact)
* [Acknowledgments](#-acknowledgments)

---

## Overview

The **AI Meeting Summarizer** is a powerful web application designed to streamline your post-meeting workflows. It leverages state-of-the-art Artificial Intelligence to automatically transcribe spoken meeting audio and generate concise, actionable summaries. Say goodbye to manual note-taking and missed key points – focus on the discussion, and let the AI handle the rest!

This project aims to provide a robust solution for:
* Converting raw meeting audio into accurate text transcripts.
* Extracting the most important information, decisions, and action items.
* Saving valuable time for individuals and teams.

The output is categorized into:
- 📌 **Pain Points**
- 🛑 **Objections**
- ✅ **Next Steps**
- ⏳ **Timeline**

## Features

* **Audio Transcription:** Upload audio files (e.g., MP3, WAV) and get accurate text transcripts using advanced Speech-to-Text models.
* **AI-Powered Summarization:** Utilizes large language models to condense lengthy transcripts into clear, coherent, and concise summaries.
* **Key Information Extraction:** Automatically identifies and highlights critical decisions, action items, and discussion points.
* **User-Friendly Interface:** An intuitive web interface for easy audio upload, transcription, and summary viewing.
* **Scalable Backend:** Designed with a modular backend for easy integration of different AI models and future enhancements.
* **Secure API Key Handling:** Emphasizes best practices for managing sensitive API keys.

## Technologies Used

This project is built using a modern stack to ensure performance, scalability, and ease of development.

**Backend:**
* **Python:** The core programming language.
* **[FastAPI]:** FastAPI for high performance.
* **[Speech Recognition Library]:** WHISPER For converting audio to text.
* **[Large Language Model (LLM) API]:** Used 'gemini-1.5-flash-latest' for text summarization, Hugging Face API for fast trancription.
* **`python-dotenv`:** For managing environment variables.

**Frontend:**
* **[React]:** React + Tailwind CSS for dynamic user experience.

**Deployment & Hosting:**
* **GitHub:** Code hosting.
* **Render:** Cloud platform for deploying the web service.

## Getting Started

Follow these instructions to set up and run the AI Meeting Summarizer on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.9+** 
* **pip** (Python package installer)
* **Git**

### Local Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/mesumittiwari/AI-Meeting-Summarizer.git](https://github.com/mesumittiwari/AI-Meeting-Summarizer.git)
    cd AI-Meeting-Summarizer
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS / Linux
    source venv/bin/activate
    ```

3.  **Install backend dependencies:**
    Navigate into the `backend` directory and install the required Python packages.

    ```bash
    cd backend
    pip install -r requirements.txt
    cd .. # Go back to the project root
    ```
    *Make sure you have a `requirements.txt` file in your `backend` directory. If not, generate one from your current environment:*
    ```bash
    # In the backend directory
    pip freeze > requirements.txt
    ```

### Environment Variables

This project uses environment variables to manage sensitive API keys. You need to create a `.env` file in the `backend` directory.

1.  **Create a `.env` file:**
    In the `backend/` directory, create a new file named `.env` (note the leading dot).

2.  **Add your API keys:**
    Populate the `.env` file with your API keys. Replace the placeholder values with your actual keys.

    ```dotenv
    # backend/.env

    # Example for OpenAI API Key
    OPENAI_API_KEY=your_openai_api_key_here

    # Example for Hugging Face API Token (if used, e.g., for inference API)
    HF_ACCESS_TOKEN=your_huggingface_access_token_here

    # Add any other API keys or environment-specific variables your backend needs
    ```
    **IMPORTANT:** Never commit your `.env` file to version control. It is already included in `.gitignore` for your security.

### Running the Backend

Once the dependencies are installed and environment variables are set, you can start the backend server.

1.  **Navigate to the `backend` directory:**

    ```bash
    cd backend
    ```

2.  **Start the server:**
    (Choose the command based on your backend framework: FastAPI with Uvicorn, Flask with Gunicorn, etc.)

    **If using FastAPI with Uvicorn:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    *(`main:app` assumes your FastAPI app instance is named `app` in `main.py`)*

    **If using Flask with a simple Python script:**
    ```bash
    python app.py
    ```
    *(`app.py` would be your main Flask application file)*

    The backend server should now be running, typically accessible at `http://127.0.0.1:8000` (or the port you configured).

### Running the Frontend

1.  **Navigate to the `frontend` directory:**
    ```bash
    cd ../frontend # From the backend directory, or cd frontend from project root
    ```

2.  **Install frontend dependencies (e.g., for a React app):**
    ```bash
    npm install # or yarn install
    ```

3.  **Start the frontend development server:**
    ```bash
    npm start # or yarn start
    ```
    The frontend application should then open in your browser, usually at `http://localhost:3000`.

---

## Usage

1.  **Access the Application:** Open your web browser and navigate to the frontend URL (e.g., `http://localhost:3000`).
2.  **Upload Audio:** Use the provided interface to upload your meeting audio file (e.g., MP3, WAV).
3.  **Process:** It will automatically generate trancscription of uploaded auddio file. Click the "Copy to Analysis Input" button. The application will then:
    * Take transcription as text input.
    * Process the transcript with the AI model.
    * Display the generated summary and extracted key points.
4.  **View Summary:** Read the concise summary and review the extracted action items.
    * You can dowload the summarised text in CSV and JSON format.
    * You can e-mail it to a predefined receiver email from your email (see envrironment variables for more clarity).


## 📂 Project Structure
```plaintext
AI-Meeting-Summarizer/
│── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│── README.md
```

## 🎥 Live Demo

[![Watch the demo](https://img.youtube.com/vi/ZccZPmXawIw/maxresdefault.jpg)](https://youtu.be/ZccZPmXawIw)

## 🧠 AI Flow Explanation (Input → Transcription → LLM Summarization)

### 1. 🔊 Audio Input Upload
- User uploads a `.mp3`, `.wav`, or similar audio file via the frontend.
- The file is sent to the backend for processing.

### 2. 🎙️ Transcription via Whisper (Hugging Face)
- Backend converts audio to `.wav` if required using `ffmpeg`.
- Whisper (Hugging Face) processes the audio and generates the transcript (text).

### 3. 📝 Summarization via Gemini API
- The transcript is sent to **Google Gemini** (`gemini-1.5-flash-latest`).
- Gemini generates a structured summary categorized into:
  - **Pain Points**
  - **Objections**
  - **Next Steps**
  - **Timeline**

### 4. 📤 Output Delivery
- Results are displayed in the frontend UI.
- Users can optionally:
  - Download the output as **CSV** or **JSON**.
  - Email the summary.

---

## 🚀 Deployment

The AI Meeting Summarizer is deployed on **Render** for backend hosting and can be accessed live via the following link:

🔗 **Live App:** [AI Meeting Summarizer](https://ai-meeting-summarizer-1-sfrq.onrender.com/)

**Deployment Steps (if self-hosting):**
1. **Backend Deployment:**
   - Push the backend code to your GitHub repository.
   - Link your repository to a hosting platform such as **Render**, **Railway**, or **Heroku**.
   - Configure environment variables (API keys, etc.) in the platform’s settings.
   - Deploy and note the backend API URL.

2. **Frontend Deployment:**
   - Update API endpoints in the frontend code to point to the deployed backend.
   - Deploy the frontend using **Vercel**, **Netlify**, or **Render**.
   - Link your domain or use the default deployment URL provided by the hosting service.

3. **Testing:**
   - Test both frontend and backend integrations to ensure smooth performance.
   - Verify file uploads, summarization accuracy, and API connections.

---


## 📧 Contact  
**Sumit Tiwari**  
📩 Email: [sumittiwari2414@gmail.com](mailto:sumittiwari2414@gmail.com)  
🔗 GitHub: [mesumittiwari](https://github.com/mesumittiwari)


## 🙌 Acknowledgments

A huge thank you to all the amazing technologies, platforms, and people who made this project possible:

- **[Google Gemini API](https://deepmind.google/technologies/gemini/)** – for providing powerful summarization capabilities.
- **[Hugging Face](https://huggingface.co/)** – for robust transcription models like Whisper.
- **[FastAPI](https://fastapi.tiangolo.com/)** – for creating a high-performance backend.
- **[React](https://react.dev/)** and **[Tailwind CSS](https://tailwindcss.com/)** – for building a fast and responsive frontend.
- **[Render](https://render.com/)** – for reliable cloud deployment.
---
