import streamlit as st
from media_plan import generate_media_plan

st.set_page_config(
    page_title="Rabhan Growth",
    layout="wide"
)


col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:
    
    st.image("img.png", use_container_width=True)
st.title("📈 Rabhan Growth Agency")
st.subheader("AI Media Plan Generator")

store_name = st.text_input("Store Name")
store_url = st.text_input("Store URL")
niche = st.text_input("Business Niche")
budget = st.text_input("Monthly Budget", value="10000 SAR")

country = st.selectbox(
    "Target Country",
    ["Saudi Arabia", "UAE", "Qatar", "Kuwait"]
)

generate = st.button("Generate Media Plan")

if generate:
    if not store_name or not store_url or not niche or not budget:
        st.error("Please fill all fields.")
    else:
        with st.spinner("Analyzing store and generating report..."):
            html_report, markdown_report = generate_media_plan(
                store_name=store_name,
                store_url=store_url,
                niche=niche,
                budget=budget,
                country=country
            )

        st.success("Report generated successfully!")

        st.markdown(markdown_report)

        st.download_button(
            label="Download HTML Report",
            data=html_report,
            file_name="media_plan.html",
            mime="text/html"
        )