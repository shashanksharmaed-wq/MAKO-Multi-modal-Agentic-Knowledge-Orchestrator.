import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import sqlite3
import plotly.express as px
import time
from fpdf import FPDF
import base64
import re

# ==========================================
# 1. SYSTEM CONFIGURATION (ACADEMIC STANDARD)
# ==========================================
st.set_page_config(
    page_title="Asmentor Diagnostic System", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize Session State
for key in ["logged_in", "username", "role", "school_id", "grade", "active_test", "test_meta"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else None

# Professional CSS (No Gamification)
st.markdown("""<style>
    .main-header {font-size: 24px; font-weight: bold; color: #0F172A; border-bottom: 2px solid #0F172A; padding-bottom: 10px; margin-bottom: 20px;}
    .report-section {background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 4px; margin-bottom: 15px;}
    .metric-value {font-size: 28px; font-weight: bold; color: #1E40AF;}
    .metric-label {font-size: 14px; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;}
    div.stButton > button {background-color: #1E40AF; color: white; border-radius: 4px; border: none; padding: 10px 20px;}
    div.stButton > button:hover {background-color: #1E3A8A;}
    </style>""", unsafe_allow_html=True)

# API Client
client = None
try:
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except: pass

# ==========================================
# 2. DATABASE SCHEMA
# ==========================================
DB_NAME = 'asmentor_v11_academic.db'

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    
    # USERS
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY, password TEXT, role TEXT, 
                    school_id TEXT, grade_access TEXT, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # ASSESSMENTS
    c.execute('''CREATE TABLE IF NOT EXISTS assessments (
                    test_id TEXT PRIMARY KEY,
                    school_id TEXT, creator_id TEXT, grade TEXT, subject TEXT, 
                    topic TEXT, difficulty_level INTEGER, questions_json TEXT, 
                    status TEXT DEFAULT 'ACTIVE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # RESPONSES
    c.execute('''CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_id TEXT, test_id TEXT, student_id TEXT, 
                    question_text TEXT, selected_option TEXT, is_correct BOOLEAN, 
                    misconception_tag TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Master Admin Seed
    c.execute("SELECT count(*) FROM users WHERE username='master_admin'")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password, role, school_id, grade_access) VALUES (?, ?, ?, ?, ?)", 
                  ('master_admin', 'admin123', 'super_admin', 'HQ', 'ALL'))
    
    conn.commit()
    conn.close()

# --- CONTROLLERS ---
def authenticate(u, p):
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT role, school_id, grade_access FROM users WHERE username=? AND password=?", (u.strip(), p.strip())).fetchone()
    conn.close()
    return res

def create_user(u, p, r, s, g):
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute("INSERT INTO users (username, password, role, school_id, grade_access) VALUES (?, ?, ?, ?, ?)", (u.strip(), p.strip(), r, s.strip(), g))
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError: return False, "Username already exists."
    except Exception as e: return False, str(e)
    finally: conn.close()

def create_test(tid, sid, cid, g, s, t, d, q_json):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO assessments (test_id, school_id, creator_id, grade, subject, topic, difficulty_level, questions_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                 (tid, sid, cid, g, s, t, d, q_json))
    conn.commit()
    conn.close()

def get_school_tests(school_id):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT test_id, creator_id, grade, subject, topic, created_at FROM assessments WHERE school_id=? ORDER BY created_at DESC", conn, params=[school_id])
    conn.close()
    return df

def get_test_meta(tid):
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT * FROM assessments WHERE test_id=?", (tid,)).fetchone()
    conn.close()
    return res

def check_attempt(student, tid):
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT count(*) FROM responses WHERE student_id=? AND test_id=?", (student, tid)).fetchone()[0]
    conn.close()
    return res > 0

def save_attempt(data):
    conn = sqlite3.connect(DB_NAME)
    conn.executemany("INSERT INTO responses (school_id, test_id, student_id, question_text, selected_option, is_correct, misconception_tag) VALUES (?,?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()

def get_analytics(tid):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM responses WHERE test_id=?", conn, params=[tid])
    conn.close()
    return df

def reset_student_attempt(tid, student_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM responses WHERE test_id=? AND student_id=?", (tid, student_id))
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. ACADEMIC INTELLIGENCE ENGINE
# ==========================================
def clean_json(raw):
    try: return json.loads(raw)
    except:
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match: 
            try: return json.loads(match.group(0))
            except: pass
    return []

def generate_academic_questions(grade, subject, topic, difficulty):
    if not client: return []
    
    levels = {
        1: "Recall", 2: "Comprehension", 3: "Application", 
        4: "Analysis", 5: "Evaluation", 6: "Synthesis", 7: "High-Order Thinking (HOTS)"
    }
    
    prompt = f"""
    ROLE: Senior Academic Examiner (Board Level).
    TASK: Construct 5 Diagnostic Multiple-Choice Questions.
    
    PARAMETERS:
    - Grade: {grade}
    - Subject: {subject}
    - Topic: {topic}
    - Cognitive Level: {levels.get(difficulty, 'Application')}
    
    STRICT GUIDELINES:
    1. Tone must be formal, academic, and precise. NO emojis. NO casual language.
    2. Questions must be rigorously aligned to the topic '{topic}'.
    3. Distractors (wrong options) must test specific conceptual errors, not random guesses.
    
    OUTPUT FORMAT (JSON):
    [
      {{
        "question": "Formal question text...", 
        "options": ["A","B","C","D"], 
        "correct_index": 0, 
        "misconception_map": ["Correct", "Procedural Error", "Conceptual Gap", "Definition Error"]
      }}
    ]
    """
    try:
        res = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":prompt}], temperature=0.4)
        return clean_json(res.choices[0].message.content)
    except: return []

def generate_formal_report(report_type, context_data):
    if not client: return "Report Unavailable."
    
    if report_type == "student":
        prompt = f"""
        Generate a Formal Diagnostic Report for Student.
        Context: {context_data}.
        
        Sections Required:
        1. **Performance Analysis:** Objective summary of accuracy.
        2. **Conceptual Gap Identification:** Detailed explanation of the errors made.
        3. **Remedial Plan:** Specific academic concepts to review.
        """
    else: # Teacher
        prompt = f"""
        Generate a Pedagogical Intervention Plan.
        Topic: {context_data['topic']}.
        Identified Class Deficits: {context_data['errors']}.
        
        Sections Required:
        1. **Root Cause Analysis:** Why did the cohort fail these concepts?
        2. **Instructional Strategy:** A rigorous classroom activity to address these gaps.
        3. **Verification Mechanism:** A follow-up question to test understanding.
        """
    try:
        res = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":prompt}], temperature=0.7)
        return res.choices[0].message.content
    except: return "Analysis Failed."

# ==========================================
# 4. USER INTERFACE
# ==========================================

# --- LOGIN ---
if not st.session_state.logged_in:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown("<div class='main-header'>Asmentor Diagnostic System</div>", unsafe_allow_html=True)
        st.write("Enterprise Edition v11.0")
        st.write("Authorized Personnel Only.")
    
    with c2:
        with st.form("login_form"):
            st.write("### System Login")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Authenticate"):
                auth = authenticate(u, p)
                if auth:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.role = auth[0]
                    st.session_state.school_id = auth[1]
                    st.session_state.grade = auth[2]
                    st.rerun()
                else:
                    st.error("Authentication Failed.")

else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("Control Panel")
        st.write(f"User: **{st.session_state.username}**")
        st.write(f"Role: **{st.session_state.role.upper()}**")
        st.write(f"Node: **{st.session_state.school_id}**")
        st.divider()
        if st.button("Secure Logout"):
            st.session_state.clear()
            st.rerun()

    # --- ADMIN / TEACHER VIEW ---
    if st.session_state.role in ["super_admin", "admin", "teacher"]:
        st.markdown("<div class='main-header'>Academic Administration Dashboard</div>", unsafe_allow_html=True)
        
        tabs = st.tabs(["Assessment Creation", "Diagnostic Reports", "User Registry", "System Tools"])
        
        # 1. CREATE
        with tabs[0]:
            st.markdown("#### Configure New Assessment")
            c1, c2 = st.columns(2)
            # Full Range Class 1-12
            grade = c1.selectbox("Target Grade", [str(i) for i in range(1, 13)])
            subject = c2.selectbox("Subject Domain", ["Mathematics", "Science", "English", "Social Studies", "Physics", "Chemistry", "Biology"])
            topic = st.text_input("Specific Topic / Unit")
            diff = st.slider("Difficulty Index (1=Recall, 7=HOTS)", 1, 7, 4)
            
            if st.button("Initialize Assessment Generation"):
                if topic:
                    with st.spinner("Processing Curriculum Standards..."):
                        qs = generate_academic_questions(grade, subject, topic, diff)
                        if qs:
                            # ID Format: SUB-GR-TIME
                            tid = f"{subject[:3].upper()}{grade}-{int(time.time())}"[-8:]
                            create_test(tid, st.session_state.school_id, st.session_state.username, grade, subject, topic, diff, json.dumps(qs))
                            st.success(f"Assessment Created Successfully. ID: {tid}")
                            with st.expander("Review Generated Items"):
                                st.table(pd.DataFrame(qs)[['question']])
                        else: st.error("Generation Algorithm Failed.")
                else: st.warning("Topic field is mandatory.")

        # 2. REPORTS
        with tabs[1]:
            st.markdown("#### Performance Analytics")
            
            all_tests = get_school_tests(st.session_state.school_id)
            if not all_tests.empty:
                test_opts = all_tests['test_id'].tolist()
                sel_tid = st.selectbox("Select Assessment ID", test_opts)
                
                if sel_tid:
                    df = get_analytics(sel_tid)
                    if not df.empty:
                        meta = get_test_meta(sel_tid)
                        
                        # Metrics Row
                        m1, m2, m3 = st.columns(3)
                        m1.markdown(f"<div class='metric-label'>Cohort Size</div><div class='metric-value'>{len(df['student_id'].unique())}</div>", unsafe_allow_html=True)
                        avg_score = df['is_correct'].mean() * 100
                        m2.markdown(f"<div class='metric-label'>Mean Accuracy</div><div class='metric-value'>{avg_score:.1f}%</div>", unsafe_allow_html=True)
                        critical_errs = len(df[(df['is_correct']==0)])
                        m3.markdown(f"<div class='metric-label'>Total Errors</div><div class='metric-value'>{critical_errs}</div>", unsafe_allow_html=True)
                        
                        st.divider()
                        
                        # Charts
                        err_df = df[df['is_correct']==0]
                        if not err_df.empty:
                            st.markdown("##### Conceptual Deficit Analysis")
                            counts = err_df['misconception_tag'].value_counts().reset_index()
                            counts.columns = ['Identified Deficit', 'Frequency']
                            
                            fig = px.bar(counts, x='Frequency', y='Identified Deficit', orientation='h', 
                                         color_discrete_sequence=['#1E40AF'])
                            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            st.plotly_chart(fig, use_container_width=True)
                            
                            if st.button("Generate Pedagogical Intervention Plan"):
                                with st.spinner("Analyzing Cohort Data..."):
                                    plan = generate_formal_report("teacher", {"topic": meta[5], "errors": str(counts['Identified Deficit'].tolist())})
                                    st.markdown("<div class='report-section'>", unsafe_allow_html=True)
                                    st.markdown(plan)
                                    st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.info("No significant conceptual deficits detected in current data.")
                    else: st.info("Data pending. No student submissions recorded.")
            else: st.info("No assessment records found.")

        # 3. USERS
        with tabs[2]:
            st.markdown("#### User Registry")
            if st.session_state.role in ["super_admin", "admin"]:
                with st.form("add_user"):
                    c1, c2 = st.columns(2)
                    nu = c1.text_input("Username")
                    np = c2.text_input("Password")
                    nr = st.selectbox("Access Role", ["student", "teacher", "admin"])
                    ns = st.text_input("School ID", value=st.session_state.school_id, disabled=(st.session_state.role != "super_admin"))
                    ng = st.text_input("Grade Level (Students)", "All")
                    
                    if st.form_submit_button("Register User"):
                        success, msg = create_user(nu, np, nr, ns, ng)
                        if success: st.success(msg)
                        else: st.error(msg)
            else: st.warning("Administrative privileges required.")

        # 4. TOOLS
        with tabs[3]:
            st.markdown("#### System Maintenance")
            c1, c2 = st.columns(2)
            rtid = c1.text_input("Target Assessment ID")
            rsid = c2.text_input("Target Student ID")
            if st.button("Purge Student Submission"):
                reset_student_attempt(rtid, rsid)
                st.success(f"Submission record for {rsid} purged.")

    # --- STUDENT VIEW ---
    elif st.session_state.role == "student":
        st.markdown(f"<div class='main-header'>Student Portal | Grade {st.session_state.grade}</div>", unsafe_allow_html=True)
        
        if not st.session_state.active_test:
            with st.form("start_test"):
                tid = st.text_input("Enter Assessment ID")
                if st.form_submit_button("Begin Assessment"):
                    meta = get_test_meta(tid)
                    if meta:
                        if check_attempt(st.session_state.username, tid):
                            st.error("Submission Limit Reached: You have already completed this assessment.")
                        else:
                            st.session_state.active_test = json.loads(meta[7])
                            st.session_state.test_meta = meta
                            st.rerun()
                    else: st.error("Invalid Assessment ID.")
        
        else:
            meta = st.session_state.test_meta
            st.markdown(f"##### Assessment: {meta[5]}")
            st.markdown(f"**Subject:** {meta[4]} | **Rigor Level:** {meta[6]}/7")
            st.divider()
            
            with st.form("exam_paper"):
                qs = st.session_state.active_test
                answers = {}
                for i, q in enumerate(qs):
                    st.write(f"**{i+1}. {q['question']}**")
                    answers[i] = st.radio("Select Response", q['options'], key=i)
                    st.markdown("---")
                
                if st.form_submit_button("Submit Responses"):
                    score = 0
                    attempt_data = []
                    error_log = []
                    
                    for i, q in enumerate(qs):
                        try: idx = q['options'].index(answers[i])
                        except: idx = 0
                        
                        is_correct = (idx == q['correct_index'])
                        if is_correct: score += 1
                        
                        misc_tag = q['misconception_map'][idx]
                        if not is_correct:
                            error_log.append(f"Question: {q['question']} \nResponse: {answers[i]} \nAnalysis: {misc_tag}")
                        
                        attempt_data.append((st.session_state.school_id, meta[0], st.session_state.username, q['question'], answers[i], is_correct, misc_tag))
                    
                    save_attempt(attempt_data)
                    st.session_state.active_test = None
                    
                    st.success(f"Assessment Submitted. Score: {score}/{len(qs)}")
                    
                    if error_log:
                        st.markdown("#### Diagnostic Report")
                        with st.spinner("Generating Analysis..."):
                            rpt = generate_formal_report("student", f"Topic: {meta[5]}, Errors: {str(error_log)}")
                            st.markdown(rpt)
                            
                            # PDF
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_font("Arial", size=10)
                            pdf.multi_cell(0, 5, rpt.encode('latin-1', 'replace').decode('latin-1'))
                            b64 = base64.b64encode(pdf.output(dest='S').encode('latin-1')).decode()
                            st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="Diagnostic_Report.pdf">Download PDF Report</a>', unsafe_allow_html=True)
