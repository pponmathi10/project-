import streamlit as st
import PyPDF2

st.set_page_config(page_title="Recruiter ATS Screening", layout="wide")

st.title("🧑‍💼 Recruiter ATS Resume Screening")
st.caption("Authenticated Recruiter Portal")

# ==================================================
# 🧠 Job Roles with MAIN SKILL + REQUIRED SKILLS
# ==================================================
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "spring boot", "hibernate", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "scikit-learn", "pandas", "numpy", "statistics"]
    },
    "Data Scientist": {
        "main": "python",
        "skills": ["python", "machine learning", "statistics", "pandas", "sql"]
    },
    "Web Developer": {
        "main": "javascript",
        "skills": ["html", "css", "javascript", "react", "bootstrap"]
    },
    "Full Stack Developer": {
        "main": "javascript",
        "skills": ["html", "css", "javascript", "react", "node", "express", "python", "sql"]
    }
}

# ==================================================
# 📄 PDF Reader
# ==================================================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==================================================
# 📊 ATS Evaluation Logic (WITH YOUR CONDITIONS)
# ==================================================
def evaluate_resume(text, role):
    role_data = ROLE_SKILLS[role]
    main_skill = role_data["main"]
    required = role_data["skills"]

    matched = [s for s in required if s in text]
    missing = [s for s in required if s not in text]

    score = int((len(matched) / len(required)) * 100)

    # ✅ CONDITIONS
    main_skill_present = main_skill in text
    two_skills_present = len(matched) >= 2
    percentage_pass = score >= 50

    if main_skill_present or two_skills_present or percentage_pass:
        decision = "SELECT"
    else:
        decision = "REJECT"

    return score, decision, matched, missing, required, main_skill_present

# ==================================================
# 🔐 Recruiter Authentication
# ==================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Recruiter Login")

    recruiter_name = st.text_input("Recruiter Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if recruiter_name and password:
            st.session_state.logged_in = True
            st.success(f"Welcome {recruiter_name}")
        else:
            st.error("Please enter valid credentials")

# ==================================================
# 📊 ATS DASHBOARD
# ==================================================
else:
    st.subheader("📊 ATS Resume Evaluation Dashboard")

    role = st.selectbox("Target Job Role", ROLE_SKILLS.keys())
    resume_file = st.file_uploader(
        "Upload Candidate Resume (Anonymous)",
        type=["pdf", "txt"]
    )

    if st.button("🔍 Run ATS Evaluation"):
        if not resume_file:
            st.warning("Please upload a resume")
            st.stop()

        resume_text = (
            read_pdf(resume_file)
            if resume_file.type == "application/pdf"
            else resume_file.read().decode("utf-8").lower()
        )

        score, decision, matched, missing, required, main_skill_present = evaluate_resume(resume_text, role)

        # ATS Badge
        if decision == "SELECT" and score >= 70:
            fit, badge = "HIGH FIT", "🟢 SHORTLIST"
        elif decision == "SELECT":
            fit, badge = "MODERATE FIT", "🟡 CONSIDER"
        else:
            fit, badge = "LOW FIT", "🔴 REJECT"

        st.markdown("## 🧠 ATS Screening Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Skill Match", f"{score}%")
        c2.metric("Matched Skills", len(matched))
        c3.metric("Role Fit", fit)

        st.progress(score / 100)

        st.markdown("### 📌 ATS Recommendation")
        st.success(badge)

        # Reasons (Recruiter-only insight)
        st.markdown("### 🧾 Selection Logic Applied")
        reasons = []
        if main_skill_present:
            reasons.append("Main skill detected")
        if len(matched) >= 2:
            reasons.append("At least 2 skills matched")
        if score >= 50:
            reasons.append("Skill match ≥ 50%")

        st.info(" | ".join(reasons) if reasons else "Criteria not satisfied")

        st.markdown("### 📋 Required Skills")
        st.write(", ".join(required))

        st.markdown("### ✅ Detected Skills")
        st.write(", ".join(matched) if matched else "None")

        st.markdown("### ⚠️ Missing Skills (Internal Use)")
        st.write(", ".join(missing) if missing else "None")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.success("Logged out successfully")
