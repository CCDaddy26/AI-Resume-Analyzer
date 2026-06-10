# test_ats.py
import sys
sys.path.append(".")

from app.backend.ats_scorer import calculate_ats_score
from app.backend.matcher import compute_match

# Sample resume (same as before)
sample_resume = """
John Doe
Email: john.doe@email.com | Phone: +1234567890

EDUCATION
Bachelor of Science in Computer Science, XYZ University

EXPERIENCE
Software Developer at ABC Corp (2020-Present)
- Developed REST APIs using Python and Django
- Managed a team of 3 junior developers
- Implemented CI/CD pipelines with Jenkins and Docker
- Improved application performance by 30%
- Led migration of legacy system to microservices

SKILLS
Python, Django, SQL, Docker, Kubernetes, AWS, Git, Agile, Scrum, Communication

PROJECTS
- Built a recommendation engine using TensorFlow
- Created a real‑time dashboard with React and Node.js
"""

# -- ATS Scoring --
ats_result = calculate_ats_score(sample_resume)
print("ATS Score:", ats_result["ats_score"])
print("\nATS Feedback:")
for tip in ats_result["feedback"]:
    print(f"  • {tip}")

# -- Job Matching --
job_description = """
We are looking for a Senior Python Developer with 5+ years of experience.
Must have strong skills in Django, FastAPI, Docker, Kubernetes, and AWS.
Experience with CI/CD, microservices, and Agile methodologies.
Good communication and leadership skills.
"""

match_result = compute_match(sample_resume, job_description)
print("\n--- Job Match ---")
print("Match Percentage:", match_result["match_percentage"], "%")
print("Missing Keywords:", match_result["missing_keywords"])
