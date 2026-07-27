import streamlit as st

st.set_page_config(
    page_title="AI CP Coach",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏅 AI Competitive Programming Coach")
st.markdown("""
### Welcome to your personal Grandmaster Coach! 🧠

This AI-powered assistant is designed to help you improve your Competitive Programming skills. 
It uses advanced LLMs and RAG to analyze problems, give you progressive hints, review your code, and track your Codeforces progress.

#### 👈 Select a mode from the sidebar to begin:

- **🧠 Analyze:** Paste a problem and get a deep algorithmic breakdown.
- **💡 Hints:** Stuck? Get progressive, Socratic hints without spoiling the solution.
- **✅ Review:** Submit your code for bug finding, TLE detection, and optimization.
- **📊 Profile:** Analyze your Codeforces handle for strengths and weaknesses.
- **🎯 Train:** Get personalized problem recommendations based on your weak topics.

---
*Built with LangChain, FAISS, and a Fine-tuned Qwen2.5-Coder model.*
""")

# Initialize session state for global variables if needed
if "cf_handle" not in st.session_state:
    st.session_state.cf_handle = ""

# Sidebar global settings
with st.sidebar:
    st.header("⚙️ Settings")
    handle = st.text_input("Codeforces Handle", value=st.session_state.cf_handle, placeholder="e.g. tourist")
    if handle:
        st.session_state.cf_handle = handle
    
    st.markdown("---")
    st.caption("AI CP Coach v1.0")
