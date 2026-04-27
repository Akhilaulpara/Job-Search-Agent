import streamlit as st
import asyncio
import os
import logging
import nest_asyncio
import base64
from dotenv import load_dotenv
from job_agents import run_analysis

nest_asyncio.apply()
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Job Search",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK_CSS = """
<style>
/* ── Global dark base ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0f1117 !important;
    color: #e2e8f0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #161b27 !important;
    border-right: 1px solid #2d3748 !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ── Header branding ── */
.brand-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 0 4px 0;
    border-bottom: 1px solid #2d3748;
    margin-bottom: 20px;
}
.brand-header h1 {
    font-size: 1.9rem;
    font-weight: 700;
    color: #7dd3fc !important;
    margin: 0;
    letter-spacing: -0.5px;
}
.brand-subtitle {
    font-size: 0.88rem;
    color: #94a3b8;
    margin-top: 2px;
}

/* ── Sidebar section label ── */
.sidebar-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background-color: #1e2433 !important;
    border: 1px dashed #334155 !important;
    border-radius: 10px !important;
    padding: 8px !important;
}
[data-testid="stFileUploader"] * {
    color: #94a3b8 !important;
}

/* ── Text inputs ── */
[data-testid="stTextInput"] input {
    background-color: #1e2433 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    padding: 10px 12px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
}
[data-testid="stTextInput"] label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
}

/* ── Primary button ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 20px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(59,130,246,0.35) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.5) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button[disabled] {
    opacity: 0.45 !important;
    cursor: not-allowed !important;
    transform: none !important;
}

/* ── Error / info boxes ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: 1px solid #ef4444 !important;
    background-color: #1f1215 !important;
    color: #fca5a5 !important;
}

/* ── Results section heading ── */
.results-heading {
    font-size: 1.3rem;
    font-weight: 700;
    color: #7dd3fc;
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e293b;
}

/* ── Markdown content area ── */
.results-body {
    background-color: #141921;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 28px 32px;
    line-height: 1.75;
}
.results-body h2 {
    color: #7dd3fc !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    margin-top: 28px !important;
    padding-bottom: 6px !important;
    border-bottom: 1px solid #1e293b !important;
}
.results-body h3 {
    color: #93c5fd !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-top: 20px !important;
}
.results-body h4 {
    color: #bfdbfe !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    margin-top: 16px !important;
}
.results-body hr {
    border-color: #1e293b !important;
    margin: 20px 0 !important;
}
.results-body a {
    color: #60a5fa !important;
    text-decoration: none !important;
    font-weight: 500 !important;
}
.results-body a:hover {
    color: #93c5fd !important;
    text-decoration: underline !important;
}
.results-body code {
    background-color: #1e293b !important;
    color: #7dd3fc !important;
    padding: 2px 8px !important;
    border-radius: 4px !important;
    font-size: 0.87rem !important;
}
.results-body blockquote {
    border-left: 3px solid #3b82f6 !important;
    background-color: #192033 !important;
    padding: 10px 16px !important;
    border-radius: 0 6px 6px 0 !important;
    color: #94a3b8 !important;
    font-style: normal !important;
    margin: 12px 0 !important;
}
.results-body table {
    width: 100% !important;
    border-collapse: collapse !important;
}
.results-body th {
    background-color: #1e293b !important;
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    padding: 10px 14px !important;
}
.results-body td {
    padding: 9px 14px !important;
    border-bottom: 1px solid #1e293b !important;
    color: #cbd5e1 !important;
    font-size: 0.88rem !important;
}
.results-body tr:hover td {
    background-color: #192033 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #3b82f6 !important;
}
[data-testid="stSpinner"] * {
    color: #60a5fa !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

/* ── Remove default Streamlit top padding ── */
.block-container { padding-top: 1.5rem !important; }

/* ── Divider ── */
hr { border-color: #1e293b !important; }
</style>
"""

st.markdown(DARK_CSS, unsafe_allow_html=True)

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'is_analyzing' not in st.session_state:
    st.session_state.is_analyzing = False


async def analyze_resume(uploaded_file):
    try:
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        result = await run_analysis(file_path)
        st.session_state.analysis_result = result
        os.remove(file_path)

    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        st.error(f"Error analyzing resume: {str(e)}")

    finally:
        st.session_state.is_analyzing = False


def main():
    # ── Header ──
    try:
        with open("./assets/Nebius.png", "rb") as file:
            logo_b64 = base64.b64encode(file.read()).decode()
        st.markdown(f"""
        <div class="brand-header">
            <img src="data:image/png;base64,{logo_b64}" style="height:48px;" />
            <div>
                <h1>Job Search Agent</h1>
                <div class="brand-subtitle">AI-powered job matching </div> 
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.markdown("""
        <div class="brand-header">
            <div>
                <h1>Job Search Agent</h1>
                <div class="brand-subtitle">AI-powered job matching — upload your resume to get started</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Sidebar ──
    with st.sidebar:
        st.markdown('<div class="sidebar-label">Upload Your Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "PDF or DOCX supported",
            type=["pdf", "docx"],
            label_visibility="collapsed",
        )

        st.markdown('<div class="sidebar-label" style="margin-top:18px;">Nebius API Key</div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Enter your Nebius API key…",
            label_visibility="collapsed",
        )

        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

        analyze_clicked = st.button(
            "🔍 Analyze Resume",
            type="primary",
            disabled=st.session_state.is_analyzing,
            use_container_width=True,
        )

        if analyze_clicked:
            if not uploaded_file:
                st.error("Please upload a resume first.")
                return
            if not api_key:
                st.error("Please enter your Nebius API key.")
                return

            os.environ["NEBIUS_API_KEY"] = api_key
            st.session_state.is_analyzing = True
            st.session_state.analysis_result = ""

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(analyze_resume(uploaded_file))
            finally:
                loop.close()

        st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.78rem; color:#475569; line-height:1.6;">
            <b style="color:#64748b;">How it works</b><br>
            1. Upload your resume (PDF/DOCX)<br>
            2. Enter your Nebius API key<br>
            3. Click <em>Analyze Resume</em><br>
            4. Get AI-matched job listings
        </div>
        """, unsafe_allow_html=True)

    # ── Loading ──
    if st.session_state.is_analyzing:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        with st.spinner("Analyzing your resume and fetching job matches… this may take a moment."):
            st.empty()

    # ── Results ──
    if st.session_state.analysis_result:
        st.markdown('<div class="results-heading">📊 Analysis Results</div>', unsafe_allow_html=True)
        st.markdown(st.session_state.analysis_result)


if __name__ == "__main__":
    main()
