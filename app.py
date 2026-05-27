import streamlit as st
import pdfplumber
import re

st.set_page_config(
    page_title="AI Resume ATS",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

h1 {
    color: #1f2937;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
}

.skill-box {
    background-color: #2563eb;
    color: white;
    padding: 6px 12px;
    border-radius: 8px;
    display: inline-block;
    margin: 4px;
    font-size: 14px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

st.title("🏆 AI Resume Screening System")
st.caption("Smart ATS + Job Matching Dashboard")

st.sidebar.header("⚙️ ATS Settings")

st.sidebar.info("""
This system:
✔ Extracts resume data
✔ Matches job description
✔ Scores candidates
✔ Ranks resumes automatically
""")

job_description = st.text_area(
    "📌 Paste Job Description",
    height=200
)

uploaded_files = st.file_uploader(
    "📂 Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

skill_weights = {
    "python": 20,
    "java": 15,
    "sql": 15,
    "html": 10,
    "css": 10,
    "javascript": 15,
    "machine learning": 25,
    "data science": 25,
    "django": 15,
    "flask": 15,
    "pandas": 10,
    "numpy": 10
}

if uploaded_files and job_description:

    jd_clean = clean_text(job_description)

    results = []

    for file in uploaded_files:

        text = extract_text(file)
        cleaned = clean_text(text)

        skill_score = 0
        skills_found = []

        for skill, weight in skill_weights.items():

            if skill in cleaned and skill in jd_clean:
                skills_found.append(skill)
                skill_score += weight

        skill_score = min(skill_score, 50)

        jd_words = set(jd_clean.split())
        resume_words = set(cleaned.split())

        match_score = len(jd_words.intersection(resume_words))
        match_score = min(match_score, 30)

        quality_score = min(len(cleaned.split()) // 50, 20)

        total_score = skill_score + match_score + quality_score

        results.append({
            "name": file.name,
            "score": total_score,
            "skills": list(set(skills_found))
        })

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    st.subheader("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Resumes", len(results))
    col2.metric("Top Score", results[0]["score"])
    col3.metric("Best Candidate", results[0]["name"])

    st.divider()

    st.subheader("🏆 Ranked Candidates")

    for i, r in enumerate(results):

        with st.container():

            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### Rank #{i+1}")
                st.write(f"📄 Resume: **{r['name']}**")

            with col2:
                st.metric("ATS Score", r["score"])

            st.progress(r["score"] / 100)

            st.write("### 🧠 Detected Skills")

            for skill in r["skills"]:
                st.markdown(
                    f'<span class="skill-box">{skill}</span>',
                    unsafe_allow_html=True
                )

            st.write("")

            st.info(
                "Score based on skill match, resume quality, and job relevance."
            )

            st.markdown('</div>', unsafe_allow_html=True)

    st.success(f"🥇 Best Match: {results[0]['name']}")

    st.subheader("📌 System Summary")

    st.info("""
This AI-powered ATS system:

✔ Extracts text from resumes  
✔ Cleans and processes data  
✔ Detects relevant technical skills  
✔ Matches resumes with job descriptions  
✔ Calculates ATS-style scores  
✔ Ranks candidates automatically  
""")