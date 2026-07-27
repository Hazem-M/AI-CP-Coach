import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add parent directory to path to import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.codeforces_api import CodeforcesAPI

st.set_page_config(page_title="CF Profile Analysis", page_icon="📊", layout="wide")

st.title("📊 Codeforces Profile Analysis")
st.markdown("Analyze your strengths and weaknesses based on your Codeforces submission history.")

# Get handle from session state or input
handle_input = st.text_input("Enter Codeforces Handle", value=st.session_state.get("cf_handle", ""))

if st.button("Analyze Profile", type="primary"):
    if not handle_input.strip():
        st.warning("Please enter a valid handle.")
    else:
        st.session_state.cf_handle = handle_input
        
        with st.spinner(f"Fetching data for {handle_input} from Codeforces API..."):
            api = CodeforcesAPI()
            analysis = api.analyze_weaknesses(handle_input)
            
            if "error" in analysis:
                st.error(analysis["error"])
            else:
                st.success(f"Analysis complete for {handle_input}!")
                
                # Metrics Row
                col1, col2, col3 = st.columns(3)
                col1.metric("Current Rating", analysis["current_rating"])
                col2.metric("Max Rating", analysis["max_rating"])
                col3.metric("Unique Solved", analysis["total_solved_unique"])
                
                st.markdown("---")
                
                # Strengths vs Weaknesses
                col_s, col_w = st.columns(2)
                
                with col_s:
                    st.subheader("💪 Your Strengths")
                    strengths = analysis.get("strengths", [])
                    if strengths:
                        df_s = pd.DataFrame(strengths).head(10)
                        # Rename for display
                        df_s = df_s.rename(columns={"tag": "Tag", "solved": "Solved", "avg_rating": "Avg Rating"})
                        st.dataframe(df_s, use_container_width=True, hide_index=True)
                    else:
                        st.info("Keep solving problems to build your strengths!")
                        
                with col_w:
                    st.subheader("⚠️ Your Weaknesses")
                    weaknesses = analysis.get("weaknesses", [])
                    if weaknesses:
                        df_w = pd.DataFrame(weaknesses).head(10)
                        df_w = df_w.rename(columns={"tag": "Tag", "solved": "Solved", "avg_rating": "Avg Rating"})
                        st.dataframe(df_w, use_container_width=True, hide_index=True)
                    else:
                        st.success("No obvious weaknesses detected at your current level!")
                        
                # Visualization
                if strengths or weaknesses:
                    st.subheader("Radar Chart (Top Tags)")
                    all_tags = (strengths[:5] + weaknesses[:5])
                    df_radar = pd.DataFrame(all_tags)
                    if not df_radar.empty:
                        fig = px.line_polar(df_radar, r='solved', theta='tag', line_close=True,
                                            title="Problems Solved per Tag")
                        fig.update_traces(fill='toself')
                        st.plotly_chart(fig, use_container_width=True)
