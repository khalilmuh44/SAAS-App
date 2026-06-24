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
            

.hero-video-wrap {
    width: min(100%, 1100px);
    margin: 28px auto 26px auto;
    border-radius: 28px;
    overflow: hidden;
    box-shadow: 0 24px 70px rgba(15, 23, 42, 0.16);
    background: #ffffff;
}

.hero-video {
    width: 100%;
    height: 430px;
    object-fit: cover;
    object-position: center;
    display: block;
}

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
    st.subheader("🎯 Media Plan Generator")

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


