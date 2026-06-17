# ==============================
# Imports / استدعاء المكتبات
# ==============================
import streamlit as st
import pandas as pd

from business_app import generate_media_plan
from openai import OpenAI
import base64
import os
# ==============================
# Page Config / إعدادات الصفحة
# ==============================
st.set_page_config(
    page_title="AI Business Growth Platform",
    layout="wide",
    page_icon="🚀"
)



# ==========================================
#             video Edit 
# =========================================
def autoplay_video(video_path):

    if os.path.exists(video_path):

        with open(video_path, "rb") as video_file:

            video_bytes = video_file.read()

            video_base64 = base64.b64encode(
                video_bytes
            ).decode()

        st.markdown(
            f"""
            <div class="hero-video-wrap">
                <video autoplay muted loop playsinline class="hero-video">
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("Hero video not found.")

# ==============================
# Custom CSS / تعديل شكل Streamlit
# ==============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 35%, #eef6ff 100%);
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #4b5563;
    margin-bottom: 35px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.07);
    border: 1px solid #e5e7eb;
}

div.stButton > button {
    background: linear-gradient(90deg, #ff2a00, #00a83b, #0066ff, #ffb000);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 22px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# Hero Video Function / دالة تشغيل فيديو المقدمة
# ==============================
def autoplay_video(video_path: str):
    """
    Show autoplay muted loop hero video.
    عرض فيديو المقدمة بشكل تلقائي وبدون صوت ومتكرر.
    """

    if os.path.exists(video_path):
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            video_base64 = base64.b64encode(video_bytes).decode()

        st.markdown(
            f"""
            <div class="hero-video-wrap">
                <video autoplay muted loop playsinline class="hero-video">
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Hero video not found. Please upload assets/hero.mp4")


# ==============================
# Header / مقدمة التطبيق
# ==============================
col1, col2, col3 = st.columns([1, 1.8, 1])

with col2:
    autoplay_video("assets/hero.mp4")

st.markdown(
    '<div class="main-title">AI Business Growth Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Generate SEO, Marketing, Media, Content, Financial, Prediction and Competitor Reports</div>',
    unsafe_allow_html=True
)

# ==============================
# Sidebar Settings / إعدادات جانبية عامة
# ==============================
st.sidebar.title("⚙️ Report Settings")

agency_name = st.sidebar.text_input(
    "Agency / Company Name",
    value="Your Agency"
)

report_primary_color = st.sidebar.color_picker(
    "Report Primary Color",
    "#0066FF"
)

report_language = st.sidebar.selectbox(
    "Report Language",
    ["Arabic - Saudi", "English"]
)


# ==============================
# Main Navigation / اختيار نوع الأداة
# ==============================
module = st.sidebar.radio(
    "Choose Module",
    [
        "Dashboard",
        "SEO Plan",
        "Marketing Plan",
        "Media Plan",
        "Content Plan",
        "Financial Plan",
        "Predictions",
        "Competitor Analysis",
        "Data Analysis"
    ]
)


# ==============================
# Dashboard / الصفحة الرئيسية
# ==============================
if module == "Dashboard":
    st.subheader("🚀 What can this platform do?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h3>🔎 SEO Plan</h3>
        <p>Analyze website SEO and suggest keyword, content and technical improvements.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <h3>🎯 Media Plan</h3>
        <p>Create paid media strategy, platform allocation, funnel and retargeting plan.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        <h3>📊 Data Analysis</h3>
        <p>Upload CSV or Excel files and get insights, sales funnel recommendations and growth actions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("Choose a module from the sidebar to start.")


# ==============================
# Website-Based Reports / تقارير مبنية على موقع المتجر
# ==============================
if module in [
    "SEO Plan",
    "Marketing Plan",
    "Media Plan",
    "Content Plan",
    "Financial Plan",
    "Predictions",
    "Competitor Analysis"
]:

    st.subheader(f"📌 {module}")

    col_a, col_b = st.columns(2)

    with col_a:
        store_name = st.text_input("Store / Business Name")
        store_url = st.text_input("Store URL")
        niche = st.text_input("Business Niche")

    with col_b:
        budget = st.text_input("Monthly Budget", value="10000 SAR")
        country = st.selectbox(
            "Target Country",
            ["Saudi Arabia", "UAE", "Qatar", "Kuwait", "Egypt", "Other"]
        )
        main_goal = st.selectbox(
            "Main Goal",
            [
                "Increase Sales",
                "Improve Conversion Rate",
                "Improve SEO",
                "Launch Paid Ads",
                "Content Growth",
                "Competitor Analysis",
                "Full Growth Strategy"
            ]
        )

    generate = st.button(f"Generate {module}", use_container_width=True)

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

            tab1, tab2, tab3 = st.tabs([
                "Formatted Report",
                "Raw Markdown",
                "Download"
            ])

            with tab1:
                st.components.v1.html(
                    html_report,
                    height=5000,
                    scrolling=True
                )

            with tab2:
                st.markdown(markdown_report)

            with tab3:
                st.download_button(
                    label="Download HTML Report",
                    data=html_report,
                    file_name=f"{store_name}_{module.replace(' ', '_')}.html",
                    mime="text/html"
                )


# ==============================
# Data Analysis Module / قسم تحليل البيانات
# ==============================
if module == "Data Analysis":

    st.subheader("📊 Data Analysis & Sales Funnel Recommendations")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv", "xlsx"]
    )

    data_goal = st.selectbox(
        "Analysis Goal",
        [
            "Sales Performance Analysis",
            "Customer Behavior Analysis",
            "Marketing Funnel Analysis",
            "Product Performance Analysis",
            "Revenue Forecast",
            "Full Business Insights"
        ]
    )

    if uploaded_file:

        # Read uploaded file / قراءة الملف المرفوع
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

        # Preview data / عرض عينة من البيانات
        st.write("Data Preview:")
        st.dataframe(df.head())

        st.write("Basic Summary:")
        st.write(df.describe(include="all"))

        analyze_data = st.button("Analyze Data with AI", use_container_width=True)

        if analyze_data:

            # Convert sample data to text / تحويل عينة من البيانات لنص
            data_sample = df.head(50).to_csv(index=False)

            prompt = f"""
            You are a senior business data analyst and growth consultant.

            Analyze the following business data.

            Goal:
            {data_goal}

            Data Sample:
            {data_sample}

            Provide:
            1. Key insights
            2. Sales funnel recommendations
            3. Marketing funnel recommendations
            4. Customer behavior opportunities
            5. Revenue improvement ideas
            6. Suggested KPIs
            7. Action plan for the next 30 days

            Write in professional Arabic.
            Use tables where possible.
            """

            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            with st.spinner("Analyzing data with AI..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )

            analysis_result = response.choices[0].message.content

            st.success("Analysis completed!")
            st.markdown(analysis_result)

            st.download_button(
                label="Download Data Analysis Report",
                data=analysis_result,
                file_name="data_analysis_report.md",
                mime="text/markdown"
            )