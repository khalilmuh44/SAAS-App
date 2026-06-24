#########################################################################
#                                    Imports
########################################################################


import streamlit as st
import pandas as pd

from modules.media_plan import generate_media_plan
from openai import OpenAI
import base64
import os



##################################################################
#                   Page Config
###############################################################

st.set_page_config(
    page_title="AI Business Growth Platform",
    layout="wide",
    page_icon="🚀"
)



########################################################################
#                                        video Edit 
#######################################################################

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



#########################################################################
#                               Custom CSS / تعديل شكل Streamlit
#########################################################################

# ==============================
# App Theme CSS / ثيم التطبيق الأساسي
# ==============================

st.markdown("""
<style>

/* ==============================
   App Background / خلفية التطبيق
   ============================== */

.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF6FF 55%, #FFFFFF 100%);
}

/* ==============================
   Sidebar / القائمة الجانبية
   ============================== */

section[data-testid="stSidebar"] {
    background: #1F2937 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}



/* Sidebar / القائمة الجانبية */
section[data-testid="stSidebar"] {
    background: #1F2937 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #374151 !important;
}

/* Sidebar radio text */
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #FFFFFF !important;
}

/* Sidebar divider */
section[data-testid="stSidebar"] hr {
    border-color: #374151 !important;
}

/* ==============================
   Main Titles / العناوين الرئيسية
   ============================== */

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #1565F5;
    margin-bottom: 6px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #4B5563;
    margin-bottom: 35px;
}

.section-title {
    font-size: 34px;
    font-weight: 800;
    color: #1565F5;
    margin: 20px 0 28px 0;
}

/* ==============================
   Cards / الكروت
   ============================== */

.card {
    background: #FFFFFF;
    padding: 26px;
    border-radius: 22px;
    box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08);
    border: 1px solid #E5E7EB;
}

.card h3 {
    color: #1565F5;
}

.card p {
    color: #4B5563;
}

/* ==============================
   Main Form Labels / أسماء خانات الفورم الرئيسي
   ============================== */

div[data-testid="stAppViewContainer"] div[data-testid="stWidgetLabel"] label,
div[data-testid="stAppViewContainer"] div[data-testid="stWidgetLabel"] p {
    color: #111827 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* ==============================
   Main Form Inputs / خانات الفورم الرئيسي
   ============================== */

div[data-testid="stAppViewContainer"] .stTextInput input,
div[data-testid="stAppViewContainer"] .stNumberInput input,
div[data-testid="stAppViewContainer"] .stTextArea textarea,
div[data-testid="stAppViewContainer"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 14px !important;
}

div[data-testid="stAppViewContainer"] .stTextInput input::placeholder,
div[data-testid="stAppViewContainer"] .stTextArea textarea::placeholder {
    color: #6B7280 !important;
    opacity: 1 !important;
}

div[data-testid="stAppViewContainer"] div[data-baseweb="select"] span,
div[data-testid="stAppViewContainer"] div[data-baseweb="select"] div {
    color: #111827 !important;
}

div[data-testid="stAppViewContainer"] .stTextInput input:disabled {
    background-color: #F3F4F6 !important;
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
    opacity: 1 !important;
}

div[data-testid="stAppViewContainer"] .stTextInput input:focus,
div[data-testid="stAppViewContainer"] .stNumberInput input:focus,
div[data-testid="stAppViewContainer"] .stTextArea textarea:focus,
div[data-testid="stAppViewContainer"] div[data-baseweb="select"] > div:focus-within {
    border-color: #1565F5 !important;
    box-shadow: 0 0 0 3px rgba(21, 101, 245, 0.15) !important;
}

/* Number input buttons */
div[data-testid="stAppViewContainer"] button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #E5E7EB !important;
}

/* ==============================
   Buttons / الأزرار
   ============================== */

div.stButton > button {
    background: linear-gradient(
        90deg,
        #FF3D1A 0%,
        #78C800 34%,
        #1565F5 68%,
        #FFC107 100%
    ) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 15px 24px !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 28px rgba(21, 101, 245, 0.18);
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 16px 34px rgba(21, 101, 245, 0.24);
}

/* ==============================
   Hero Video / فيديو المقدمة
   ============================== */

.hero-video-wrap {
    width: min(100%, 1100px);
    margin: 28px auto 26px auto;
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 24px 70px rgba(15, 23, 42, 0.16);
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
}

.hero-video {
    width: 100%;
    height: 430px;
    object-fit: cover;
    object-position: center;
    display: block;
}

/* ==============================
   Tabs / ألوان التابات
   ============================== */

div[data-testid="stAppViewContainer"] button[data-baseweb="tab"] p {
    color: #111827 !important;
    font-weight: 700 !important;
}

div[data-testid="stAppViewContainer"] button[data-baseweb="tab"][aria-selected="true"] p {
    color: #FF3D1A !important;
}

div[data-testid="stAppViewContainer"] div[data-baseweb="tab-highlight"] {
    background-color: #FF3D1A !important;
}

/* ==============================
   Markdown Preview فقط داخل الصفحة الرئيسية
   ============================== */

div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"],
div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] * {
    color: #111827 !important;
}

div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h3 {
    color: #1565F5 !important;
}

div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] table {
    background: #FFFFFF !important;
    color: #111827 !important;
}

div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] th {
    background: #1565F5 !important;
    color: #FFFFFF !important;
}

div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] td {
    color: #111827 !important;
}

/* ==============================
   Alerts / رسائل التنبيه
   ============================== */

div[data-testid="stAlert"] {
    border-radius: 16px;
}

/* ==============================
   Mobile Responsive / موبايل
   ============================== */

@media (max-width: 768px) {
    .hero-video-wrap {
        width: 100%;
        border-radius: 18px;
        margin: 15px auto 20px auto;
    }

    .hero-video {
        height: 220px;
        object-position: center;
    }

    .main-title {
        font-size: 30px !important;
    }

    .sub-title {
        font-size: 14px !important;
        padding: 0 12px;
    }
}

</style>
""", unsafe_allow_html=True)




#                   ==============================
#                   Header / مقدمة التطبيق
#                   ==============================

col1, col2, col3 = st.columns([0.3, 3, 0.3])

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


#############################################################################
#                      Sidebar Settings / إعدادات التقرير الجانبية
###########################################################################


# Sidebar title / عنوان القائمة الجانبية
st.sidebar.title("⚙️ Report Settings")

# Agency name shown in report header and footer
# اسم الشركة الذي سيظهر في الهيدر والفوتر داخل التقرير
agency_name = st.sidebar.text_input(
    "Agency / Company Name",
    value="Ameen"
)

# Report language option
# اختيار لغة التقرير
report_language = st.sidebar.selectbox(
    "Report Language / لغة التقرير",
    [
        "Arabic",
        "English"
    ]
)

st.sidebar.divider()

# Report background color
# لون خلفية التقرير
report_bg_color = st.sidebar.color_picker(
    "Report Background Color / لون خلفية التقرير",
    "#3B4757"
)

# Main report text color
# لون النص الأساسي في التقرير
report_text_color = st.sidebar.color_picker(
    "Main Text Color / لون النص الأساسي",
    "#FFFFFF"
)

# Secondary text color for headings or highlighted text
# لون النص الثانوي للعناوين أو النصوص المميزة
report_secondary_text_color = st.sidebar.color_picker(
    "Secondary Text Color / لون النص الثانوي",
    "#FEC000"
)

# Accent color for icons, borders, buttons and visual highlights
# لون العناصر المميزة مثل الأيقونات والحدود والأزرار
report_accent_color = st.sidebar.color_picker(
    "Accent / Icons Color / لون الأيقونات والعناصر",
    "#FE5500"
)


##################################################################
#                              Main Navigation / اختيار نوع الأداة
####################################################                     
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




######################################################################
# Module Router / توجيه الموديولات
#########################################################################



# Active modules / الموديولات المفعلة حاليًا
active_modules = {
    "Media Plan": generate_media_plan
}

# Coming soon modules / الموديولات التي ما زالت قيد التطوير
coming_soon_modules = [
    "SEO Plan",
    "Marketing Plan",
    "Content Plan",
    "Financial Plan",
    "Predictions",
    "Competitor Analysis",
    "Data Analysis"
]


# ==============================
# Dashboard / الصفحة الرئيسية
# ==============================
if module == "Dashboard":
    st.info("Choose a module from the sidebar to start.")


#######################################################################
# Media Plan Module / موديول الميديا بلان
#########################################################################


elif module == "Media Plan":

    # Page title / عنوان الصفحة
    st.markdown(
    '<div class="section-title">🎯 Media Plan Generator</div>',
    unsafe_allow_html=True
)

    # Split form into two columns / تقسيم الفورم إلى عمودين
    col_a, col_b = st.columns(2)

    with col_a:
        # Brand name / اسم العلامة التجارية
        brand_name = st.text_input(
            "Brand Name / اسم العلامة التجارية",
            placeholder="Example: Ameen Store"
        )

        # Brand website URL / رابط الموقع
        brand_url = st.text_input(
            "Brand Website URL / رابط موقع العلامة التجارية",
            placeholder="https://example.com"
        )

    with col_b:
        # Starting budget as number only / الميزانية رقم فقط
        starting_budget = st.number_input(
            "Starting Budget (SAR) / الميزانية المبدئية",
            min_value=100,
            value=10000,
            step=500
        )

        # Fixed target country / السوق المستهدف ثابت حاليًا
        country = "Saudi Arabia"

        st.text_input(
            "Target Country / السوق المستهدف",
            value=country,
            disabled=True
        )

    # Business problem / المشكلة الأساسية للبيزنس
    business_problem = st.text_area(
        "Business Problem / المشكلة الأساسية التي يعاني منها البيزنس",
        placeholder=(
            "مثال: المتجر يحصل على زيارات كثيرة لكن المبيعات ضعيفة، "
            "أو تكلفة الشراء عالية، أو العملاء يضيفون للسلة ولا يكملون الدفع..."
        ),
        height=180
    )

    # Media buying focus / تركيز الخطة الإعلانية
    main_goal = st.selectbox(
        "Media Buying Focus / تركيز الخطة الإعلانية",
        [
            "Increase Sales",
            "Improve Conversion Rate",
            "Reduce Cost Per Purchase",
            "Improve Retargeting",
            "Increase Average Order Value",
            "Launch Paid Ads From Scratch",
            "Full Media Strategy"
        ]
    )

    # Generate button / زر إنشاء التقرير
    generate = st.button(
        "Generate Media Plan",
        use_container_width=True
    )

    if generate:

        # Validate required fields / التأكد من البيانات المطلوبة
        if not brand_name or not brand_url or not business_problem:
            st.error(
                "Please fill Brand Name, Brand URL, and Business Problem."
            )

        else:
            # Build report theme from sidebar / بناء شكل التقرير من إعدادات السايدبار
            report_theme = {
                "agency_name": agency_name,
                "bg_color": report_bg_color,
                "text_color": report_text_color,
                "secondary_text_color": report_secondary_text_color,
                "accent_color": report_accent_color,
            }

            # Get active module function / جلب دالة الموديول المفعّل
            generator = active_modules[module]

            # Generate report / إنشاء التقرير
            with st.spinner("Analyzing brand problem and generating media plan..."):
                html_report, markdown_report = generator(
                    store_name=brand_name,
                    store_url=brand_url,
                    niche="Not specified",
                    budget=f"{starting_budget} SAR",
                    country=country,
                    main_goal=main_goal,
                    business_problem=business_problem,
                    report_language=report_language,
                    report_theme=report_theme
                )

            st.success("Media Plan generated successfully!")

            # Report preview tabs / تبويبات عرض التقرير
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
                    file_name=f"{brand_name}_Media_Plan.html",
                    mime="text/html"
                )


# ==============================
# Coming Soon Modules / موديولات قيد التطوير
# ==============================
elif module in coming_soon_modules:

    st.warning(
        f"🚧 {module} module is still under development."
    )

    st.info(
        "Currently, only the Media Plan module is active for testing."
    )


# ==============================
# Unknown Module / موديول غير معروف
# ==============================
else:
    st.error("Unknown module selected.")


