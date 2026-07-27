import streamlit as st

st.set_page_config(page_title="Review Solution", page_icon="✅", layout="wide")
st.title("✅ Review Your Solution")
st.markdown("Submit your code and problem statement. The AI Coach will find bugs, check for TLE risks, and suggest optimizations.")

col1, col2 = st.columns(2)

with col1:
    problem_text = st.text_area("Problem Statement / Logic", height=200)
    language = st.selectbox("Language", ["C++", "Python", "Java"])

with col2:
    user_code = st.text_area("Your Code", height=200)

if st.button("Review Code", type="primary"):
    if not user_code.strip() or not problem_text.strip():
        st.warning("Please provide both the problem and your code.")
    else:
        with st.spinner("Reviewing your code line-by-line..."):
            from src.llm_wrapper import CPCoachLLM
            from src.chains.review_chain import SolutionReviewChain
            
            if "llm_instance" not in st.session_state:
                st.session_state.llm_instance = CPCoachLLM().get_llm()
                
            chain = SolutionReviewChain(st.session_state.llm_instance)
            result = chain.run(problem_text, user_code, language)
            if hasattr(result, "dict"): result = result.dict()
            
            st.success("Review Complete!")
            
            st.subheader(f"Verdict: `{result.get('verdict', 'UNKNOWN').upper()}`")
            
            issues = result.get('issues', [])
            opts = result.get('optimization_suggestions', [])
            
            if not issues and not opts:
                st.balloons()
                st.success("🎉 Perfect Code! No issues or optimizations found.")
            
            if issues:
                st.markdown("### 🐛 Issues Found")
                for issue in issues:
                    sev = issue.get('severity', 'warning').lower()
                    desc = issue.get('description', '')
                    fix = issue.get('fix', '')
                    line = issue.get('line_number', '')
                    line_str = f" (Line {line})" if line else ""
                    
                    msg = f"**{desc}**{line_str}\n\n💡 **Fix:** {fix}"
                    if sev == 'critical':
                        st.error(msg)
                    elif sev == 'warning':
                        st.warning(msg)
                    else:
                        st.info(msg)
            
            if opts:
                st.info("**[Style/Optimization] Suggestions**")
                for opt in opts:
                    st.write(f"- {opt}")
                
            st.write(f"**Your Time Complexity:** `{result.get('time_complexity_user', 'N/A')}`")
            st.write(f"**Optimal Time Complexity:** `{result.get('time_complexity_optimal', 'N/A')}`")
            st.write(f"**Score:** `{result.get('score', 'N/A')}/100`")
            
            if result.get('corrected_code'):
                with st.expander("Show Corrected Code"):
                    st.code(result.get('corrected_code'), language=language.lower())
