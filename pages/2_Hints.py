import streamlit as st

st.set_page_config(page_title="Progressive Hints", page_icon="💡", layout="wide")
st.title("💡 Progressive Hints (Socratic Coach)")
st.markdown("Stuck? Ask for a hint. The coach will give you a small nudge first. You can reveal deeper hints if you are still stuck.")

problem_text = st.text_area("Problem Statement", height=200, placeholder="Paste the problem description here...")

if "hints_revealed" not in st.session_state:
    st.session_state.hints_revealed = 0

if st.button("Generate Hints", type="primary"):
    if problem_text:
        with st.spinner("Generating progressive hints..."):
            st.session_state.hints_revealed = 1
            from src.llm_wrapper import CPCoachLLM
            from src.chains.hint_chain import HintChain
            
            if "llm_instance" not in st.session_state:
                st.session_state.llm_instance = CPCoachLLM().get_llm()
            
            chain = HintChain(st.session_state.llm_instance)
            result = chain.run(problem_text)
            if hasattr(result, "dict"): result = result.dict()
            st.session_state.hints = result.get("hints", [])

if "hints" in st.session_state and st.session_state.hints:
    st.markdown("### Your Hints:")
    
    for i in range(st.session_state.hints_revealed):
        if i < len(st.session_state.hints):
            hint = st.session_state.hints[i]
            st.info(f"**[{hint.get('level', 'Hint').upper()}]** {hint.get('content', '')}")
            st.caption(f"Reveals: *{hint.get('reveals', '')}*")
        
    if st.session_state.hints_revealed < len(st.session_state.hints):
        if st.button("Give me another hint 💡"):
            st.session_state.hints_revealed += 1
            st.rerun()
    else:
        st.success("All hints revealed! You should be able to solve it now.")
