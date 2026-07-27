import streamlit as st
import pandas as pd

st.set_page_config(page_title="Train", page_icon="🎯", layout="wide")

st.title("🎯 Personalized Training Plan")
st.markdown("Based on your Codeforces profile analysis, here are the problems you need to solve to rank up.")

handle_input = st.text_input("Enter Codeforces Handle", value=st.session_state.get("cf_handle", ""))

if st.button("Generate Training Plan", type="primary"):
    if handle_input:
        st.session_state.cf_handle = handle_input
        with st.spinner(f"Analyzing {handle_input}'s weaknesses and finding optimal problems..."):
            
            # Mock Data
            st.success("Training Plan Generated!")
            
            st.subheader("Your Target Weaknesses:")
            st.write("1. `dynamic programming` (Rating Gap: -300)")
            st.write("2. `graphs` (Solved: 2)")
            
            st.markdown("---")
            st.subheader("📚 Recommended Problem Set")
            
            problems = [
                {"Name": "Kefa and First Steps", "Tag": "dp", "Rating": 900, "Link": "https://codeforces.com/problemset/problem/580/A"},
                {"Name": "Cut Ribbon", "Tag": "dp", "Rating": 1300, "Link": "https://codeforces.com/problemset/problem/189/A"},
                {"Name": "Party", "Tag": "graphs", "Rating": 1100, "Link": "https://codeforces.com/problemset/problem/115/A"},
            ]
            
            for p in problems:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**[{p['Name']}]({p['Link']})**")
                    with col2:
                        st.write(f"Tag: `{p['Tag']}`")
                    with col3:
                        st.write(f"Rating: {p['Rating']}")
                    st.divider()
            
            st.info("💡 **Coach's Tip:** Focus on identifying the state transitions in the DP problems before writing any code. Draw it on paper first!")
