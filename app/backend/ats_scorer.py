import re
from .skills  import load_skill_database, extract_skills

def calculate_ats_score(text):
    """
    Analyse the resume text and return a dictionary with:
      - ats_score: a number 0-100
      - feedback: list of improvement suggestions
    """
    score = 0
    feedback = []

    # ---------- 1. Keyword / Skill coverage (max 30 points) ----------
    skill_db = load_skill_database()
    found_skills = extract_skills(text, skill_db)
    # What % of the skill database appears in the resume?
    coverage = len(found_skills) / max(len(skill_db), 1)
    skill_points = coverage * 30
    score += min(skill_points, 30)

    if len(found_skills) < 8:
        feedback.append("Add more technical skills relevant to your target job (aim for at least 8-10).")

    # ---------- 2. Section detection (max 30 points) ----------
    sections = {
        "education": bool(re.search(r"(?i)\beducation\b", text)),
        "experience": bool(re.search(r"(?i)\b(experience|work history|employment)\b", text)),
        "skills": bool(re.search(r"(?i)\bskills?\b", text)),
        "projects": bool(re.search(r"(?i)\b(projects?|portfolio)\b", text)),
    }
    section_score = sum(sections.values()) * 7.5   # each section = 7.5 pts
    score += section_score

    if not sections["education"]:
        feedback.append("Include an Education section.")
    if not sections["experience"]:
        feedback.append("Add a Work Experience section with detailed bullet points.")
    if not sections["projects"]:
        feedback.append("Consider adding a Projects section to showcase practical work.")

    # ---------- 3. Contact info (10 points) ----------
    has_email = bool(re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
    has_phone = bool(re.search(r"\+?\d[\d\-\(\) ]{6,}\d", text))
    if has_email and has_phone:
        score += 10
    else:
        feedback.append("Add a professional email and phone number for ATS compatibility.")

    # ---------- 4. Readability – sentence length (10 points) ----------
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 3]
    if sentences:
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
        if 15 <= avg_len <= 25:
            score += 10
        else:
            feedback.append("Improve sentence length (aim for 15–25 words per sentence).")
    else:
        feedback.append("Resume appears too short; add more detailed descriptions.")

    # ---------- 5. Bullet points (10 points) ----------
    bullet_count = len(re.findall(r"•|●||\*|-", text))
    if bullet_count >= 5:
        score += 10
    else:
        feedback.append("Use bullet points to list achievements and responsibilities.")

    # ---------- 6. Action verbs (10 points) ----------
    action_verbs = r"\b(developed|managed|led|created|designed|implemented|improved|increased|reduced|launched|delivered|automated|optimised|optimized|spearheaded|orchestrated)\b"
    action_count = len(re.findall(action_verbs, text, re.IGNORECASE))
    if action_count >= 3:
        score += 10
    else:
        feedback.append("Start bullet points with strong action verbs (e.g. 'developed', 'managed', 'launched').")

    # Final score capped at 100
    final_score = min(score, 100)
    return {
        "ats_score": round(final_score, 1),
        "feedback": list(set(feedback))   # remove any duplicate tips
    }
