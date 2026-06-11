# 📄 AI Resume Analyzer

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B.svg)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688.svg)](https://fastapi.tiangolo.com)
[![spaCy](https://img.shields.io/badge/spaCy-3.8-green.svg)](https://spacy.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent **ATS Resume Analyzer** that extracts skills, calculates ATS compatibility scores, matches resumes to job descriptions, and provides AI‑powered improvement suggestions — all through a modern dark‑theme dashboard.

---

## 🚀 Features

- ✅ **PDF/DOCX Parsing** – Upload any resume file and extract text automatically
- 🧠 **Skill Extraction** – Detects 200+ technical, soft, and business skills using spaCy NLP
- 🎯 **ATS Score** – Calculates a 0‑100 compatibility score based on keywords, sections, formatting, action verbs
- 📊 **Job Description Matching** – Semantic similarity via Sentence Transformers, plus missing keyword detection
- 💬 **AI Feedback** – Actionable suggestions like *“Add measurable achievements”* or *“Improve bullet‑point usage”*
- 🖥️ **Modern Dashboard** – Dark‑themed Streamlit UI with interactive charts and metric cards
- 🔌 **REST API** – FastAPI backend ready to serve any client

---

## 🖼️ Demo

![App Screenshot]("D:\Daniel\AI-Resume-Analyzer\screen recording\Screenshot 2026-06-11 161556.png") <!-- add a screenshot if you have one -->

> **Live Demo** – *Coming soon (currently run locally)*  
> **Local Setup** – See instructions below to run on your machine in under 5 minutes.

---

## 🧰 Tech Stack

| Layer       | Technology                                      |
|-------------|-------------------------------------------------|
| **Frontend**| Streamlit (custom CSS dark theme)               |
| **Backend** | FastAPI (REST API)                              |
| **NLP**     | spaCy, Sentence Transformers, scikit‑learn      |
| **Parsing** | pdfplumber, python‑docx                         |
| **Charts**  | Plotly                                          |
| **Deployment** | Render (backend), Streamlit Cloud (frontend) |

---

## 📁 Project Structure
AI-Resume-Analyzer/
├── app/
│ ├── backend/
│ │ ├── main.py # FastAPI server
│ │ ├── parser.py # PDF/DOCX extraction
│ │ ├── skills.py # Skill detection
│ │ ├── ats_scorer.py # ATS scoring logic
│ │ ├── matcher.py # Job description matching
│ │ └── feedback.py # Combined AI feedback
│ ├── frontend/
│ │ └── streamlit_app.py # Modern dashboard UI
│ └── utils/
│ └── helpers.py # Utility functions
├── data/
│ └── skill_db.json # 200+ skill database
├── notebooks/ # Experimental notebooks
├── requirements.txt
├── Procfile # For Render deployment
└── README.md
