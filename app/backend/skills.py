import json
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def load_skill_database(path="data/skill_db.json"):
    with open(path, "r") as f:
        return json.load(f)

def extract_skills(text, skill_db=None):
    if skill_db is None:
        skill_db = load_skill_database()
    doc = nlp(text.lower())
    found_skills = set()
    # Direct keyword matching
    for skill in skill_db:
        if skill.lower() in text.lower():
            found_skills.add(skill)
    # spaCy named entities and noun chunks
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "SKILL"]:   # expand as needed
            found_skills.add(ent.text.title())
    # Additional regex based matching for compound skills
    compound = re.findall(r"(?:machine learning|deep learning|data science|power bi|project management|data analysis|big data|data engineering|ui/ux design|cloud computing)", text, re.IGNORECASE)
    for c in compound:
        found_skills.add(c.title())
    return list(found_skills)
