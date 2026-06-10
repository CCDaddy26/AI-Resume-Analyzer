from sentence_transformers import SentenceTransformer, util
import re

# Load model once when the module is imported
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_match(resume_text: str, job_desc: str) -> dict:
    """
    Compare resume text with a job description.
    Returns:
        match_percentage: float 0-100
        missing_keywords: list of words in JD but not in resume
    """
    if not job_desc.strip():
        return {"match_percentage": 0.0, "missing_keywords": []}

    # Embed both texts and compute cosine similarity
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_job = model.encode(job_desc, convert_to_tensor=True)
    similarity = util.cos_sim(emb_resume, emb_job).item()

    # Simple missing keyword detection (single words for MVP)
    # Clean and tokenize
    resume_words = set(re.findall(r'\b[a-zA-Z]+\b', resume_text.lower()))
    job_words = set(re.findall(r'\b[a-zA-Z]+\b', job_desc.lower()))
    # Find words in JD not in resume (excluding common stopwords)
    stopwords = {'the','a','an','and','or','but','in','on','at','to','for','of','with','is','are','am','be','been','being','have','has','had','do','does','did','will','would','shall','should','may','might','must','can','could'}
    missing = [w for w in job_words if w not in resume_words and w not in stopwords]
    # Show top 10 by length (or just first 10)
    missing = sorted(missing, key=len, reverse=True)[:10]

    return {
        "match_percentage": round(similarity * 100, 1),
        "missing_keywords": missing
    }