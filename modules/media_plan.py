

import os
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import markdown
from dotenv import load_dotenv  
load_dotenv()  


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

################################################################

#                     Scraping and Brand Asset Extraction


################################################################


def is_valid_hex(color):
    return bool(re.match(r"^#[0-9A-Fa-f]{6}$", color))


def extract_brand_assets(soup, base_url):
    theme_color = None

    meta_theme = soup.find("meta", attrs={"name": "theme-color"})
    if meta_theme and meta_theme.get("content"):
        color = meta_theme.get("content").strip()
        if is_valid_hex(color):
            theme_color = color

    html_text = str(soup)
    hex_colors = re.findall(r"#[0-9A-Fa-f]{6}", html_text)

    ignored_colors = {
        "#ffffff", "#000000", "#f5f5f5", "#eeeeee", "#e5e5e5",
        "#cccccc", "#dddddd", "#f9f9f9", "#111111", "#222222"
    }

    filtered_colors = [
        c for c in hex_colors
        if c.lower() not in ignored_colors
    ]

    primary_color = theme_color or (filtered_colors[0] if filtered_colors else "#4f46e5")
    secondary_color = filtered_colors[1] if len(filtered_colors) > 1 else "#111827"

    logo_url = None
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        logo_url = og_image.get("content")

    if not logo_url:
        logo_img = soup.find("img", attrs={"alt": re.compile("logo|شعار", re.I)})
        if logo_img and logo_img.get("src"):
            logo_url = logo_img.get("src")

    if logo_url and logo_url.startswith("/"):
        logo_url = base_url.rstrip("/") + logo_url

    return {
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "logo_url": logo_url
    }



def fetch_store_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    brand_assets = extract_brand_assets(soup, url)

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""

    meta_description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_description = meta.get("content", "")

    headings = [
        h.get_text(" ", strip=True)
        for h in soup.find_all(["h1", "h2", "h3"])
        if h.get_text(strip=True)
    ]

    links_ctas = [
        a.get_text(" ", strip=True)
        for a in soup.find_all(["a", "button"])
        if a.get_text(strip=True)
    ]

    page_text = soup.get_text(" ", strip=True)

    return {
        "title": title,
        "meta_description": meta_description,
        "headings": headings[:50],
        "links_ctas": links_ctas[:80],
        "page_text": page_text[:12000],
        "brand_assets": brand_assets
    }


################################################################
#                     Extract Final Score from Report
################################################################

def extract_final_score(report_markdown):
    """
    Extract final score from Arabic or English reports.
    استخراج التقييم النهائي من التقرير.
    """

    match = re.search(
        r"(?:التقييم النهائي للمتجر هو:|Final Store Score:)\s*(\d+)",
        report_markdown,
        re.IGNORECASE
    )

    return match.group(1) if match else "7"



####################################################################
#                                             Function     
##################################################################


def generate_media_plan(
    store_name,
    store_url,
    niche,
    budget,
    country,
    main_goal="Full Media Strategy",
    business_problem="",
    report_language="Arabic",
    report_theme=None,
    **kwargs
):
    if report_theme is None:
        report_theme = {
            "agency_name": "Ameen",
            "bg_color": "#3B4757",
            "text_color": "#FFFFFF",
            "secondary_text_color": "#FEC000",
            "accent_color": "#FE5500",
        }

    store_data = fetch_store_page(store_url)



#############################################################

#                                  openAi Prompt   


#############################################################
    # ==============================
    # Language Instructions / تعليمات اللغة
    # ==============================

    if report_language == "Arabic":
        language_instruction = """
        Write the entire report in professional Saudi Arabic.
        Use tables whenever possible.
        Use a business-friendly tone.
        """
    else:
        language_instruction = """
        Write the entire report in professional English.
        Use tables whenever possible.
        Use a business-friendly tone.
        """

    system_prompt = f"""
You are a world-class senior e-commerce growth consultant, media buyer,
conversion rate optimization (CRO) specialist and funnel strategist.

{language_instruction}

You are writing for business owners, not marketers.

Your mission is not just to create a media plan.

Your mission is to deeply understand the business problem and build a complete growth strategy around solving that problem.

Always prioritize the business problem provided by the client over generic recommendations.

Do not create generic reports.

First audit the website and understand:
- Customer journey
- Offers
- Product pages
- Trust elements
- Conversion opportunities
- Positioning
- Funnel stages

Then create a complete strategy.

Always explain the business impact on:

- Sales
- Conversion Rate
- Customer Trust
- ROAS
- Customer Retention

Use business-friendly language.

Avoid technical jargon.

Do not criticize the business.

Use a positive advisory tone.

Important:

Choose channels based on:
- Country
- Audience behavior
- Product type
- Funnel stage
- Budget
- Main business problem

Always mention the store name throughout the report.

Important wording rules:

Do not use:
- مشاكل
- قضايا

Use:
- ملاحظات
- فرص تحسين
- نقاط تحتاج تطوير

Use "أفضل أشكال الإعلانات" instead of "الإبداعات".

Use "فرص زيادة قيمة السلة" instead of "البيع الإضافي والبيع المتقاطع".

The report should contain:

# الملخص التنفيذي

# فهم المشكلة الأساسية للبيزنس

Explain:
- What the business problem means
- Possible causes
- Impact on growth

# تحليل تجربة المتجر

# فرص تحسين معدل التحويل

# الشرائح المستهدفة

# رحلة العميل

# القنوات الإعلانية المناسبة

# توزيع الميزانية

# هيكل الحملات الإعلانية

# خطة إعادة الاستهداف

# فرص زيادة قيمة السلة

# حملات واتساب

# خطة المحتوى حسب مراحل الفانل

# أفضل أشكال الإعلانات لكل منصة

# فرص تحسين الظهور في Google

# مؤشرات الأداء KPI

# إجراءات سريعة التنفيذ

# خطة نمو لمدة 90 يوم

# تقييم المتجر من 10

Give an overall score out of 10.

Also score:

- Customer Experience
- Offers
- Trust
- Product Pages
- Conversion Rate Opportunities
- Google Visibility
- Ads Readiness

For each score explain:

- Why this score was given.
- What improvements would increase the score.

End the evaluation section with exactly:

التقييم النهائي للمتجر هو: [number]

Output in Markdown.

Use tables whenever possible.

Think like a growth consultant, not just a media buyer.

The whole strategy should revolve around solving the client's main business problem.
"""
################################################################
    logo_url = store_data["brand_assets"]["logo_url"]
    user_prompt = f"""
Business Information

Store Name:
{store_name}

Store URL:
{store_url}

Business Niche:
{niche}

Monthly Budget:
{budget}

Target Country:
{country}

Main Goal:
{main_goal}

Main Business Problem:
{business_problem}

Important:

This business problem is the highest priority.

The whole report should revolve around solving this problem.

Do not create a generic media plan.

-------------------------------------------------

Website Audit Data

Page Title:
{store_data["title"]}

Meta Description:
{store_data["meta_description"]}

Headings:
{store_data["headings"]}

Buttons and CTAs:
{store_data["links_ctas"]}

Website Text:
{store_data["page_text"]}

-------------------------------------------------

Requirements

1. Understand the client's problem deeply.

2. Identify possible root causes.

3. Explain how this problem affects:
- Sales
- Conversion rate
- Customer trust
- ROAS

4. Audit the website.

5. Build a complete media strategy around solving this problem.

6. Recommend suitable channels.

7. Allocate the monthly budget.

8. Build campaign structure.

9. Build retargeting strategy.

10. Build content funnel.

11. Recommend creatives and offers.

12. Suggest KPIs.

13. Create a 90-day growth plan.

14. Provide a store score out of 10.

Use tables whenever possible.

Output in Markdown.
"""

##############################################################
        # Send request to OpenAI
    # إرسال الطلب إلى OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    # Extract the report markdown from OpenAI response
    # استخراج التقرير بصيغة Markdown من رد OpenAI
    report_markdown = response.choices[0].message.content

    # Convert Markdown tables and content to HTML
    # تحويل محتوى Markdown والجداول إلى HTML
    report_html_body = markdown.markdown(
        report_markdown,
        extensions=["tables"]
    )

   # Extract overall score from report
# استخراج التقييم النهائي من التقرير

    final_score = extract_final_score(report_markdown)


    # Get agency/report theme settings
    # جلب إعدادات هوية التقرير
    agency_name = report_theme.get("agency_name", "Ameen")
    bg_color = report_theme.get("bg_color", "#3B4757")
    text_color = report_theme.get("text_color", "#FFFFFF")
    secondary_text_color = report_theme.get("secondary_text_color", "#FEC000")
    accent_color = report_theme.get("accent_color", "#FE5500")

    # Store logo from website if available
    # لوجو المتجر من الموقع إن وجد
    logo_url = store_data["brand_assets"].get("logo_url")
    logo_html = (
        f'<img src="{logo_url}" class="logo" alt="Store Logo">'
        if logo_url
        else ""
    )

    html_dir = "rtl" if report_language == "Arabic" else "ltr"
    html_lang = "ar" if report_language == "Arabic" else "en"

    section_border_side = "right" if report_language == "Arabic" else "left"
    section_padding_side = "right" if report_language == "Arabic" else "left"

    # Report HTML Template
    # قالب التقرير النهائي
    html_template = f"""
<!DOCTYPE html>
<html lang="{html_lang}" dir="{html_dir}">
<head>
<meta charset="UTF-8">
<title>Media Plan - {store_name}</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --secondary-text: {secondary_text_color};
    --accent: {accent_color};
    --white: #FFFFFF;
    --border: rgba(255,255,255,0.18);
}}

html {{
    background: var(--bg);
}}

body {{
    font-family: 'IBM Plex Sans Arabic', Tahoma, Arial, sans-serif;
    direction: {html_dir};
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 0;
}}

.report {{
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    background: var(--bg);
    color: var(--text);
    overflow: hidden;
}}

.cover {{
    padding: 54px 50px 36px 50px;
    background: var(--bg);
    color: var(--text);
    border-bottom: 6px solid var(--accent);
}}

.logo {{
    max-height: 82px;
    max-width: 190px;
    background: var(--white);
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 26px;
}}

.cover h1 {{
    margin: 0;
    font-size: 38px;
    line-height: 1.55;
    color: var(--text);
    border: none;
    padding: 0;
}}

.cover p {{
    margin-top: 14px;
    font-size: 17px;
    color: var(--secondary-text);
}}

.content {{
    padding: 45px;
    background: var(--bg);
}}

.score-box {{
    background: var(--accent);
    color: #000000;
    padding: 28px;
    text-align: center;
    margin: 0 auto 42px auto;
    max-width: 440px;
    border: none;
}}

.score-number {{
    font-size: 58px;
    font-weight: 700;
    color: #000000;
    line-height: 1.1;
}}

.score-label {{
    font-size: 22px;
    color: #000000;
    margin-top: 8px;
    font-weight: 700;
}}

h1 {{
    color: var(--text);
    font-size: 34px;
    padding-bottom: 18px;
    border-bottom: 4px solid var(--accent);
}}

h2 {{
    color: var(--secondary-text);
    margin-top: 42px;
    font-size: 30px;
    border-{section_border_side}: 7px solid var(--accent);
    padding-{section_padding_side}: 14px;
}}

h3 {{
    color: var(--text);
    margin-top: 30px;
    font-size: 23px;
}}

p, li {{
    font-size: 18px;
    line-height: 2;
    color: var(--text);
}}

ul {{
    padding-right: 28px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 28px 0;
    font-size: 16px;
}}

th {{
    background: var(--accent);
    color: #000000;
    padding: 14px;
    border: 1px solid var(--accent);
    font-weight: 700;
}}

td {{
    padding: 14px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.06);
    color: var(--text);
}}

tr:nth-child(even) td {{
    background: rgba(255,255,255,0.10);
}}

strong {{
    color: var(--text);
    font-weight: 700;
}}

.footer {{
    margin-top: 55px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    text-align: center;
    color: var(--secondary-text);
    font-size: 14px;
}}

@page {{
    size: A4;
    margin: 0;
}}

@media print {{
    html, body {{
        width: 100%;
        margin: 0 !important;
        padding: 0 !important;
        background: var(--bg) !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}

    .report {{
        width: 100% !important;
        max-width: none !important;
        min-height: 100vh !important;
        margin: 0 !important;
        background: var(--bg) !important;
    }}

    .cover,
    .content,
    .score-box,
    th,
    td {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}
}}
</style>
</head>

<body>
<div class="report">
    <div class="cover">
        {logo_html}
        <h1>{agency_name} Growth Report</h1>
        <p>Media plan for {store_name}</p>
    </div>

    <div class="content">
        <div class="score-box">
            <div class="score-number">{final_score}/10</div>
            <div class="score-label">Overall Store Score</div>
        </div>

        {report_html_body}

        <div class="footer">
            Prepared by {agency_name}
        </div>
    </div>
</div>
</body>
</html>
"""

    # Save HTML locally
    # حفظ ملف HTML محليًا
    with open("media_plan.html", "w", encoding="utf-8") as file:
        file.write(html_template)

    return html_template, report_markdown