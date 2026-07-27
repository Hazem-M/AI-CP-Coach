import streamlit as st

st.set_page_config(page_title="Analyze Problem", page_icon="🧠", layout="wide")
st.title("🧠 AI CP Coach - Analyze")
st.markdown("Paste a problem statement here and let the Grandmaster analyze it.")

problem_text = st.text_area("Problem Statement", height=250)

if st.button("Analyze", type="primary"):
    if not problem_text.strip():
        st.warning("Please enter a problem statement.")
    else:
        with st.spinner("Grandmaster is thinking... (This might take a minute)"):
            from src.llm_wrapper import CPCoachLLM
            from src.chains.analyze_chain import ProblemAnalysisChain
            
            if "llm_instance" not in st.session_state:
                st.session_state.llm_instance = CPCoachLLM().get_llm()
                
            chain = ProblemAnalysisChain(st.session_state.llm_instance)
            result = chain.run(problem_text)
            
            st.success("Analysis Complete!")
            
            if "</think>" in result:
                think_part, answer_part = result.split("</think>", 1)
                think_part = think_part.replace("<think>", "").strip()
                
                with st.expander("🤔 View AI Thinking Process", expanded=True):
                    st.write(think_part)
                
                st.markdown("### 💡 Final Solution")
                st.markdown(answer_part.strip())
            else:
                st.markdown(result)
