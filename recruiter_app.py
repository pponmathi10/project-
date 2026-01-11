import streamlit as st
import PyPDF2

# ---------------- Page Config ----------------
st.set_page_config(page_title="Recruiter ATS", layout="wide")

st.title("🧑‍💼 Recruiter ATS Resume Screening")
st.caption("Secure Recruiter Evaluation Portal")

# ---------------- Role Skills ----------------
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "pandas", "numpy", "scikit-learn"]
    }
}

# ---------------- PDF Reader ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text.lower()

# ---------------- Resume Evaluation ----------------
def evaluate_resume(text, role):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = []
    for skill in skills:
        if skill in text:
            matched.append(skill)

    missing = []
    for skill in skills:
        if skill not in text:
            missing.append(skill)

    score = int((len(matched) / len(skills)) * 100)

    if (main_skill in text) or (len(matched) >= 2) or (score >= 50):
        decision = "SELECT"
    else:
        decision = "REJECT"

    return score, decision, matched, missing, skills

# ---------------- Login State ----------------
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- Login Page ----------------
if not st.session_state.login:
    st.subheader("🔐 Recruiter Login")

    name = st.text_input("Recruiter Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if name != "" and password != "":
            st.session_state.login = True
            st.success("Login Successful")
        else:
            st.error("Enter both name and password")

# ---------------- ATS Dashboard ----------------
else:
    st.subheader("📊 ATS Resume Screening")

    role = st.selectbox("Select Job Role", ROLE_SKILLS.keys())
    resume = st.file_uploader("Upload Resume", type=["pdf", "txt"])

    if st.button("Evaluate Resume"):
        if resume is None:
            st.warning("Please upload resume")
        else:
            if resume.type == "application/pdf":
                text = read_pdf(resume)
            else:
                text = resume.read().decode("utf-8").lower()

            score, decision, matched, missing, skills = evaluate_resume(text, role)

            st.markdown("## 🧠 Screening Result")
            st.metric("Skill Match %", score)
            st.progress(score / 100)

            if decision == "SELECT":
                st.success("🟢 Candidate Selected")
            else:
                st.error("🔴 Candidate Rejected")

            st.markdown("### Required Skills")
            st.write(", ".join(skills))

            st.markdown("### Matched Skills")
            st.write(", ".join(matched) if matched else "None")

            st.markdown("### Missing Skills")
            st.write(", ".join(missing) if missing else "None")

    if st.button("Logout"):
        st.session_state.login = False
