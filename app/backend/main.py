from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .parser import extract_text
from .feedback import generate_feedback

app = FastAPI(title="AI Resume Analyzer API")

# Allow requests from anywhere (frontend dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form("")
):
    """
    Analyze a resume file (PDF/DOCX) and return:
      - ats_score
      - match_percentage (if job_description provided)
      - skills found
      - improvement suggestions
    """
    # Read file content
    file_bytes = await file.read()
    file_type = file.content_type

    # Extract text from resume
    try:
        text = extract_text(file_bytes, file_type)
    except ValueError:
        return {"error": "Unsupported file format. Please upload a PDF or DOCX."}

    # Generate full feedback
    result = generate_feedback(text, job_description)
    return result

@app.get("/health")
def health():
    return {"status": "ok"}