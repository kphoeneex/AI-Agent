import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 BrandPulse – Live CX Dashboard")

uploaded_file = st.file_uploader("Upload classified_output.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Recent Messages")
    st.dataframe(df.tail(10), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Emotion Distribution**")
        st.bar_chart(df["emotion"].value_counts())
    with col2:
        st.markdown("**Urgency Levels**")
        st.bar_chart(df["urgency"].value_counts())
    with col3:
        st.markdown("**Type Breakdown**")
        st.bar_chart(df["type"].value_counts())
else:
    st.info("Run `main.py` first, then upload the generated CSV here.")
