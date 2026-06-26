#########################################################################
#                                    Imports 101
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

/* ==============================
   1) App Background
   خلفية التطبيق بالكامل
   ============================== */
.stApp {
    background: radial-gradient(
                    circle at top left,
                    #15596A 0%,
                    #0F263C 35%,
                    #071729 100%
                            );
}


/* ==============================
   2) Main Titles
   العنوان الرئيسي والوصف تحت الهيدر
   ============================== */
.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color:#F1F3F4;
    margin-bottom: 6px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color:#2BB3BC;
    margin-bottom: 35px;
}

.section-title {
    font-size: 34px;
    font-weight: 800;
    color: #F1F3F4;
    margin: 20px 0 28px 0;
}

/* ==========================================================
   4) Main Form Labels
   أسماء الحقول داخل الصفحة الرئيسية
   ========================================================== */

main div[data-testid="stWidgetLabel"] p {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}


/* ==========================================================
   5) Main Form Inputs
   شكل جميع خانات الإدخال داخل الصفحة الرئيسية
   ========================================================== */

main .stTextInput input,
main .stNumberInput input,
main .stTextArea textarea,
main div[data-baseweb="select"] > div {

    background: #16364D !important;

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;

    border: 1px solid rgba(43,179,188,.20) !important;

    border-radius: 14px !important;

    transition: all .25s ease;

}


/* ==========================================================
   Placeholder Text
   لون النص الافتراضي داخل الخانات
   ========================================================== */

main .stTextInput input::placeholder,
main .stTextArea textarea::placeholder {

    color: #A8BCC9 !important;
    opacity: 1 !important;

}


/* ==========================================================
   Selectbox Text
   لون النص داخل الـ SelectBox
   ========================================================== */

main div[data-baseweb="select"] span,
main div[data-baseweb="select"] div {

    color: #FFFFFF !important;

}


/* ==========================================================
   Input Focus
   تأثير عند الضغط على الخانات
   ========================================================== */

main .stTextInput input:focus,
main .stNumberInput input:focus,
main .stTextArea textarea:focus,
main div[data-baseweb="select"] > div:focus-within {

    border-color: #2BB3BC !important;

    box-shadow: 0 0 0 3px rgba(43,179,188,.25);

}


/* ==========================================================
   Disabled Inputs
   شكل الخانات غير القابلة للتعديل
   ========================================================== */

main .stTextInput input:disabled,
main .stNumberInput input:disabled {

    background: #0F263C !important;

    color: #8FA2AD !important;
    -webkit-text-fill-color: #8FA2AD !important;

    opacity: 1 !important;

}


/* ==========================================================
   6) Main Buttons
   الأزرار الرئيسية (Generate Report)
   ========================================================== */

div.stButton > button {

    background: linear-gradient(
        90deg,
        #2BB3BC 0%,
        #38C6D4 100%
    ) !important;

    color: #071729 !important;

    border: none !important;

    border-radius: 16px !important;

    padding: 15px 24px !important;

    font-weight: 800 !important;

    transition: all .25s ease;

    box-shadow: 0 10px 24px rgba(43,179,188,.25);

}


/* ==========================================================
   Button Hover
   شكل الزر عند مرور الماوس
   ========================================================== */

div.stButton > button:hover {

    background: linear-gradient(
        90deg,
        #38C6D4 0%,
        #52DCE5 100%
    ) !important;

    transform: translateY(-2px);

    box-shadow: 0 14px 30px rgba(43,179,188,.35);

}




/* ==========================================================
   7) Hero Video
   إطار فيديو المقدمة الرئيسي
   ========================================================== */

.hero-video-wrap {

    width: min(100%, 1100px);

    margin: 30px auto;

    overflow: hidden;

    border-radius: 22px;

    background: #0F263C;

    border: 1px solid rgba(43,179,188,.15);

    box-shadow:
        0 12px 30px rgba(7,23,41,.35),
        0 0 30px rgba(43,179,188,.05);

}


/* ==========================================================
   Hero Video
   الفيديو نفسه
   ========================================================== */

.hero-video {

    width: 100%;

    height: 500px;

    object-fit: cover;

    object-position: center;

    display: block;

}

/* ==========================================================
   8) Tabs
   تبويبات عرض التقرير:
   Formatted Report / Raw Markdown / Download
   ========================================================== */

/* Normal tabs / التابات العادية */
main button[data-baseweb="tab"],
main button[data-baseweb="tab"] *,
main div[data-baseweb="tab-list"] button,
main div[data-baseweb="tab-list"] button * {
    color: #A8BCC9 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
    transition: all .25s ease;
}

/* Active tab / التاب المختارة */
main button[data-baseweb="tab"][aria-selected="true"],
main button[data-baseweb="tab"][aria-selected="true"] *,
main div[data-baseweb="tab-list"] button[aria-selected="true"],
main div[data-baseweb="tab-list"] button[aria-selected="true"] * {
    color: #2BB3BC !important;
    font-weight: 800 !important;
}

/* Hover / عند الوقوف على التاب */
main button[data-baseweb="tab"]:hover,
main button[data-baseweb="tab"]:hover *,
main div[data-baseweb="tab-list"] button:hover,
main div[data-baseweb="tab-list"] button:hover * {
    color: #38C6D4 !important;
    opacity: 1 !important;
}

/* Tab underline / الخط تحت التاب المختارة */
main div[data-baseweb="tab-highlight"] {
    background-color: #2BB3BC !important;
    height: 3px !important;
    border-radius: 20px !important;
}


/* ==========================================================
   9) Markdown Preview
   تنسيق تبويب Raw Markdown
   ========================================================== */

/* الحاوية الرئيسية للـ Markdown */
.markdown-preview {

    background: #0F263C;

    border: 1px solid rgba(43,179,188,.15);

    border-radius: 18px;

    padding: 28px;

    box-shadow:
        0 10px 28px rgba(7,23,41,.25);

}


/* جميع النصوص */
.markdown-preview,
.markdown-preview * {

    color: #F8FAFC !important;

}


/* العناوين */
.markdown-preview h1,
.markdown-preview h2,
.markdown-preview h3 {

    color: #2BB3BC !important;

}


/* الفقرات والقوائم */
.markdown-preview p,
.markdown-preview li {

    color: #D6E3EA !important;

    line-height: 1.9;

}


/* الجداول */
.markdown-preview table {

    width: 100%;

    border-collapse: collapse;

    border-radius: 12px;

    overflow: hidden;

}


/* Header الجدول */
.markdown-preview th {

    background: #2BB3BC !important;

    color: #071729 !important;

    padding: 12px;

    font-weight: 700;

}


/* خلايا الجدول */
.markdown-preview td {

    background: rgba(255,255,255,.03);

    color: #F8FAFC !important;

    padding: 12px;

    border: 1px solid rgba(255,255,255,.08);

}


/* صفوف الجدول */
.markdown-preview tr:nth-child(even) td {

    background: rgba(255,255,255,.05);

}



/* ==========================================================
   10) Alerts
   رسائل Success / Warning / Error / Info
   ========================================================== */

div[data-testid="stAlert"]{

    border-radius:18px !important;

    border:1px solid rgba(43,179,188,.15) !important;

    box-shadow:
        0 8px 22px rgba(7,23,41,.12);

    padding:18px !important;

}


/* ==========================================================
   11) Sidebar Background
   خلفية القائمة الجانبية بالكامل
   ========================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0F263C 0%,
        #0A1D2E 45%,
        #071729 100%
    ) !important;

    border-right: 1px solid rgba(43,179,188,.15);
}


/* ==========================================================
   12) Sidebar Titles & Labels
   عناوين وأسماء الحقول داخل الـ Sidebar
   ========================================================== */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] div[role="radiogroup"] p {
    color: #D6E3EA !important;
    font-weight: 600 !important;
}


/* ==========================================================
   13) Sidebar Inputs
   خانات الإدخال داخل الـ Sidebar
   ========================================================== */

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #16364D !important;

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;

    border: 1px solid rgba(43,179,188,.22) !important;
    border-radius: 14px !important;

    transition: all .25s ease;
}


/* ==========================================================
   14) Sidebar Placeholder
   لون النص الافتراضي داخل الخانات
   ========================================================== */

section[data-testid="stSidebar"] input::placeholder,
section[data-testid="stSidebar"] textarea::placeholder {
    color: #A8BCC9 !important;
    opacity: 1 !important;
}


/* ==========================================================
   15) Sidebar Selectbox Text
   لون النص داخل الـ SelectBox
   ========================================================== */

section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] div {
    color: #FFFFFF !important;
}


/* ==========================================================
   16) Sidebar Focus Effect
   تأثير عند الضغط على الخانات
   ========================================================== */

section[data-testid="stSidebar"] input:focus,
section[data-testid="stSidebar"] textarea:focus,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
    border-color: #2BB3BC !important;
    box-shadow: 0 0 0 3px rgba(43,179,188,.25) !important;
}


/* ==========================================================
   17) Sidebar Divider
   الخط الفاصل داخل الـ Sidebar
   ========================================================== */

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.08) !important;
}


/* ==========================================================
   18) Sidebar Radio Buttons
   أزرار اختيار الموديول
   ========================================================== */

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover p {
    color: #2BB3BC !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] input {
    accent-color: #2BB3BC !important;
}


/* ==========================================================
   19) Sidebar Color Pickers
   مربعات اختيار الألوان
   ========================================================== */

section[data-testid="stSidebar"] input[type="color"] {
    background: #16364D !important;
    border-radius: 12px !important;
    border: 1px solid rgba(43,179,188,.25) !important;
}


/* ==========================================================
   20) Sidebar Expander
   الـ Expander إذا استخدمته لاحقًا
   ========================================================== */

section[data-testid="stSidebar"] details {
    background: rgba(255,255,255,.03);
    border-radius: 12px;
}


/* ==========================================================
   21) Spinner
   Loading Indicator
   ========================================================== */

.stSpinner{

    padding:18px 24px;

    border-radius:16px;

    background:rgba(15,38,60,.65);

    backdrop-filter:blur(12px);

    border:1px solid rgba(43,179,188,.15);

}


/* ==========================================================
   13) Mobile Responsive
   تحسين عرض التطبيق على الشاشات الصغيرة
   ========================================================== */

@media (max-width: 768px) {

    /* Main page padding
       تقليل المسافات الجانبية داخل الصفحة الرئيسية */
    main {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }


    /* Sidebar mobile width
       ضبط عرض القائمة الجانبية على الموبايل */
    section[data-testid="stSidebar"] {
        width: 82vw !important;
        min-width: 82vw !important;
        max-width: 82vw !important;
        z-index: 999999 !important;
    }


    /* Sidebar inner container
       ضبط عرض المحتوى الداخلي للسايدبار */
    section[data-testid="stSidebar"] > div {
        width: 82vw !important;
    }


    /* Hero video wrapper
       ضبط صندوق فيديو الهيدر على الموبايل */
    .hero-video-wrap {
        width: 100% !important;
        border-radius: 18px !important;
        margin: 15px auto 20px auto !important;
    }


    /* Hero video
       تقليل ارتفاع الفيديو على الموبايل */
    .hero-video {
        height: 220px !important;
    }


    /* Main title
       تصغير العنوان الرئيسي */
    .main-title {
        font-size: 20px !important;
        line-height: 1.25 !important;
    }


    /* Subtitle
       تصغير النص أسفل العنوان */
    .sub-title {
        font-size: 14px !important;
        line-height: 1.6 !important;
        padding: 0 12px !important;
    }


    /* Section title
       تصغير عنوان كل موديول */
    .section-title {
        font-size: 28px !important;
        line-height: 1.3 !important;
    }


    /* Inputs and select boxes
       تكبير الخانات قليلًا لتناسب اللمس */
    main .stTextInput input,
    main .stNumberInput input,
    main .stTextArea textarea,
    main div[data-baseweb="select"] > div {
        min-height: 48px !important;
        font-size: 15px !important;
    }


    /* Buttons
       تحسين حجم الأزرار على الموبايل */
    div.stButton > button {
        min-height: 50px !important;
        font-size: 15px !important;
        border-radius: 14px !important;
    }


    /* Tabs
       جعل تبويبات التقرير أوضح على الموبايل */
    main button[data-baseweb="tab"],
    main button[data-baseweb="tab"] * {
        font-size: 14px !important;
        white-space: nowrap !important;
    }


    /* Markdown preview
       ضبط مساحة Raw Markdown على الموبايل */
    .markdown-preview {
        padding: 18px !important;
        border-radius: 14px !important;
        overflow-x: auto !important;
    }


    /* Tables
       منع الجداول من كسر عرض الشاشة */
    .markdown-preview table {
        display: block !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
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
    '<div class="section-title"> Media Plan Generator</div>',
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
            st.markdown(
            f"""
            <div class="markdown-preview">
            {markdown_report}
            </div>
            """,
            unsafe_allow_html=True
        )

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


