from .ats_scorer import calculate_ats_score
from .matcher import compute_match
from .skills import extract_skills

def generate_feedback(resume_text, job_desc=""):
    """
    Generate complete AI feedback for a resume.
    Optionally compare with a job description.
    """
    # 1. ATS Score
    ats_result = calculate_ats_score(resume_text)

    # 2. Job match (if job_desc provided)
    match_result = None
    if job_desc.strip():
        match_result = compute_match(resume_text, job_desc)

    # 3. Skill extraction
    skills = extract_skills(resume_text)

    # Combine all suggestions
    suggestions = []

    # ATS feedback
    suggestions.extend(ats_result["feedback"])

    # Job match feedback
    if match_result:
        if match_result["match_percentage"] < 50:
            suggestions.append(
                f"Your resume matches the job description by only {match_result['match_percentage']}%. "
                "Tailor it to include more keywords from the JD."
            )
        if match_result["missing_keywords"]:
            missing = match_result["missing_keywords"]
            suggestions.append(
                f"Consider adding these missing keywords: {', '.join(missing[:8])}"
            )

    # Skill-based feedback
    if len(skills) < 8:
        suggestions.append(
            f"Only {len(skills)} skills detected. Try to list at least 8–10 relevant technical skills."
        )

    # General best‑practice tips
    suggestions.append("Use action verbs and quantify achievements (e.g., 'increased sales by 20%').")
    suggestions.append("Keep resume to 1–2 pages and use a clean, single‑column layout.")

    return {
        "ats_score": ats_result["ats_score"],
        "match_percentage": match_result["match_percentage"] if match_result else None,
        "skills": skills,
        "suggestions": list(set(suggestions))  # remove duplicates
    }