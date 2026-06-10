import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ---------- Page config ----------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS (dark theme) ----------
st.markdown("""
<style>
    /* Background and main colours */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }
    /* Buttons */
    .stButton>button {
        background-color: #1F6FEB;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #388BFD;
    }
    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1rem;
    }
    /* File uploader */
    div[data-testid="stFileUploader"] {
        background-color: #161B22;
        border-radius: 12px;
        padding: 1rem;
    }
    /* Text area */
    textarea {
        background-color: #0D1117 !important;
        color: #C9D1D9 !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
    }
    /* Subheader */
    .subheader-style {
        font-size: 1.2rem;
        font-weight: 600;
        color: #58A6FF;
        margin-top: 1rem;
    }
    /* Suggestions list */
    .suggestion-box {
        background-color: #161B22;
        border-left: 4px solid #1F6FEB;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("📄 AI Resume Analyzer")
st.caption("Upload your resume and get an ATS score, skill analysis, and job‑match feedback in seconds.")

# ---------- Sidebar ----------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=80)
    st.header("📤 Upload & Analyse")
    uploaded_file = st.file_uploader(
        "Drag and drop your resume here",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )
    job_desc = st.text_area(
        "📋 Paste a job description (optional)",
        height=200,
        placeholder="Paste the job description to see how well your resume matches..."
    )
    analyze_btn = st.button("🔍 Analyse Resume", use_container_width=True)

# ---------- Main content ----------
if uploaded_file and analyze_btn:
    with st.spinner("🔬 Analysing your resume..."):
        # Call FastAPI backend
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        data = {"job_description": job_desc}
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                files=files,
                data=data
            )
            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    st.error(result["error"])
                else:
                    # ---- Score Cards ----
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("🎯 ATS Score", f"{result['ats_score']}/100")
                        # Progress bar
                        st.progress(result['ats_score'] / 100)
                    with col2:
                        match = result.get("match_percentage")
                        if match is not None:
                            st.metric("📊 Job Match", f"{match}%")
                            st.progress(match / 100)
                        else:
                            st.info("No job description provided for matching.")

                    st.markdown("---")

                    # ---- Skills section ----
                    skills = result.get("skills", [])
                    if skills:
                        st.subheader("🧠 Extracted Skills")
                        # Display as chips/tags
                        skill_html = " ".join(
                            [f'<span style="background:#1F6FEB; color:white; padding:0.25rem 0.75rem; border-radius:20px; margin:0.2rem; display:inline-block; font-size:0.85rem;">{skill}</span>' for skill in skills]
                        )
                        st.markdown(skill_html, unsafe_allow_html=True)
                    else:
                        st.warning("No skills detected. Your resume may not be ATS‑friendly.")

                    # ---- Skill chart (only if skills present) ----
                    if skills:
                        st.markdown("")
                        # Create a simple bar chart
                        skill_df = pd.DataFrame({"Skill": skills, "Count": [1] * len(skills)})
                        fig = px.bar(
                            skill_df,
                            x="Skill",
                            y="Count",
                            title="Skills Found in Resume",
                            color_discrete_sequence=["#1F6FEB"],
                            template="plotly_dark"
                        )
                        fig.update_layout(showlegend=False, height=300)
                        st.plotly_chart(fig, use_container_width=True)

                    # ---- Suggestions ----
                    suggestions = result.get("suggestions", [])
                    if suggestions:
                        st.subheader("💡 Improvement Suggestions")
                        for i, s in enumerate(suggestions, 1):
                            st.markdown(f"""
                            <div class="suggestion-box">
                                <strong>{i}.</strong> {s}
                            </div>
                            """, unsafe_allow_html=True)

            else:
                st.error("Backend error. Please make sure FastAPI is running on port 8000.")

        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to the backend. Is uvicorn running?")
else:
    # ---------- Default placeholder ----------
    st.markdown("""
    <div style="text-align:center; margin-top:3rem; opacity:0.6;">
        <img src="https://img.icons8.com/fluency/96/upload-to-cloud.png" width="80">
        <h3>Upload a resume to get started</h3>
        <p>PDF or DOCX, up to 2 MB</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("All analysis is done locally — your data never leaves your machine.")