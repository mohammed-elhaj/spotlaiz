import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(prompt, language):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Please respond in {language}:\n{prompt}")
    return response.text

# Function to translate UI elements
def translate_ui(key, language):
    translations = {
        "en": {
            "app_title": "Spotlaiz Marketing Content Generator",
            "app_subtitle": "Empower your brand with AI-driven marketing solutions",
            "content_type_label": "Choose Content Type",
            "social_media_post": "Social Media Post",
            "marketing_campaign": "Marketing Campaign Strategy",
            "generate_button": "Generate",
            "download_button": "Download",
            "language_selector": "Select Language",
            "analysis_title": "Spotlaiz Insights",
            "target_audience": "Target Audience",
            "campaign_goals": "Campaign Goals",
            "budget": "Budget",
            "platform": "Platform",
            "brand_personality": "Brand Personality",
            "industry": "Industry",
            "key_message": "Key Message",
            "target_emotion": "Target Emotion",
            "campaign_duration": "Campaign Duration (weeks)",
            "unique_selling_point": "Unique Selling Point",
        },
        "ar": {
            "app_title": "مولد محتوى التسويق Spotlaiz",
            "app_subtitle": "عزز علامتك التجارية بحلول تسويقية مدعومة بالذكاء الاصطناعي",
            "content_type_label": "اختر نوع المحتوى",
            "social_media_post": "منشور وسائل التواصل الاجتماعي",
            "marketing_campaign": "استراتيجية الحملة التسويقية",
            "generate_button": "إنشاء",
            "download_button": "تحميل",
            "language_selector": "اختر اللغة",
            "analysis_title": "رؤى Spotlaiz",
            "target_audience": "الجمهور المستهدف",
            "campaign_goals": "أهداف الحملة",
            "budget": "الميزانية",
            "platform": "المنصة",
            "brand_personality": "شخصية العلامة التجارية",
            "industry": "الصناعة",
            "key_message": "الرسالة الرئيسية",
            "target_emotion": "العاطفة المستهدفة",
            "campaign_duration": "مدة الحملة (بالأسابيع)",
            "unique_selling_point": "نقطة البيع الفريدة",
        }
    }
    return translations[language][key]

# Custom CSS for Spotlaiz branding
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton>button {
        background-color: #4682b4;
        color: white;
    }
    .stSelectbox>div>div>div {
        background-color: #4682b4;
        color: white;
    }
    .arabic {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# Language selection
language = st.sidebar.selectbox(
    "Select Language / اختر اللغة",
    ("English", "العربية")
)

lang_code = "en" if language == "English" else "ar"

# App title and subtitle
st.title(translate_ui("app_title", lang_code))
st.write(translate_ui("app_subtitle", lang_code))

# Content type selection
content_type = st.sidebar.selectbox(
    translate_ui("content_type_label", lang_code),
    (translate_ui("social_media_post", lang_code), translate_ui("marketing_campaign", lang_code))
)

# Output language selection
output_language = st.sidebar.multiselect(
    "Output Language / لغة الإخراج",
    ["English", "العربية"],
    default=["English"] if lang_code == "en" else ["العربية"]
)

if translate_ui("social_media_post", lang_code) in content_type:
    st.header(translate_ui("social_media_post", lang_code))
    
    platform = st.selectbox(translate_ui("platform", lang_code), ["Instagram", "Facebook", "LinkedIn"])
    brand_personality = st.select_slider(
        translate_ui("brand_personality", lang_code),
        options=["Professional", "Casual", "Playful", "Inspirational", "Educational"]
    )
    industry = st.selectbox(translate_ui("industry", lang_code), ["Technology", "Fashion", "Food & Beverage", "Health & Wellness", "Finance"])
    key_message = st.text_area(translate_ui("key_message", lang_code), max_chars=200)
    target_emotion = st.select_slider(
        translate_ui("target_emotion", lang_code),
        options=["Excitement", "Trust", "Joy", "Anticipation", "Curiosity"]
    )

    if st.button(translate_ui("generate_button", lang_code)):
        prompt = f"""Create a social media post for {platform} with the following details:
        Industry: {industry}
        Brand Personality: {brand_personality}
        Key Message: {key_message}
        Target Emotion: {target_emotion}

        The post should include:
        1. Attention-grabbing headline
        2. Main body (respecting platform character limits)
        3. Call-to-action
        4. 3-5 relevant hashtags

        Ensure the tone matches the brand personality and aims to evoke the target emotion."""

        for lang in output_language:
            output_lang_code = "en" if lang == "English" else "ar"
            response = get_gemini_response(prompt, lang)
            
            st.subheader(f"Generated Post ({lang}):")
            if output_lang_code == "ar":
                st.markdown(f'<div class="arabic">{response}</div>', unsafe_allow_html=True)
            else:
                st.write(response)

        # Spotlaiz Insights
        st.subheader(translate_ui("analysis_title", lang_code))
        insight_prompt = f"""Analyze the social media post and provide concise insights:
        1. Engagement Potential (Score 1-10)
        2. Brand Alignment (Score 1-10)
        3. Key Strengths (Bullet points)
        4. Improvement Suggestions (Bullet points)
        
        Present the analysis as a JSON object with these keys: engagement_score, brand_alignment_score, strengths, improvements"""

        insights_raw = get_gemini_response(insight_prompt, "English")
        try:
            insights = json.loads(insights_raw)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Engagement Potential", f"{insights['engagement_score']}/10")
            with col2:
                st.metric("Brand Alignment", f"{insights['brand_alignment_score']}/10")
            st.subheader("Key Strengths")
            for strength in insights['strengths']:
                st.markdown(f"- {strength}")
            st.subheader("Improvement Suggestions")
            for improvement in insights['improvements']:
                st.markdown(f"- {improvement}")
        except json.JSONDecodeError:
            st.write("Unable to parse insights. Here's the raw output:")
            st.write(insights_raw)

elif translate_ui("marketing_campaign", lang_code) in content_type:
    st.header(translate_ui("marketing_campaign", lang_code))
    
    target_audience = st.text_area(translate_ui("target_audience", lang_code), "Describe your ideal customer persona")
    campaign_goals = st.multiselect(translate_ui("campaign_goals", lang_code), ["Brand Awareness", "Lead Generation", "Sales Conversion", "Customer Retention", "Product Launch"])
    budget = st.number_input(translate_ui("budget", lang_code), min_value=1000, max_value=1000000, value=10000, step=1000)
    campaign_duration = st.slider(translate_ui("campaign_duration", lang_code), 1, 52, 4)
    unique_selling_point = st.text_input(translate_ui("unique_selling_point", lang_code), "What sets your product/service apart?")


    if st.button(translate_ui("generate_button", lang_code)):
        prompt = f"""Create a marketing campaign strategy outline with the following details:
        Target Audience: {target_audience}
        Campaign Goals: {', '.join(campaign_goals)}
        Budget: ${budget}
        Campaign Duration: {campaign_duration} weeks
        Unique Selling Point: {unique_selling_point}

        Include:
        1. Campaign Concept: A creative theme that ties the campaign together
        2. Channel Strategy: Prioritized list of marketing channels with budget allocation
        3. Content Calendar: High-level overview of content types and posting frequency
        4. Key Performance Indicators (KPIs): Specific metrics to measure success
        5. Risk Assessment: Potential challenges and mitigation strategies"""

        for lang in output_language:
            output_lang_code = "en" if lang == "English" else "ar"
            strategy = get_gemini_response(prompt, lang)
            
            st.subheader(f"Generated Strategy ({lang}):")
            if output_lang_code == "ar":
                st.markdown(f'<div class="arabic">{strategy}</div>', unsafe_allow_html=True)
            else:
                st.write(strategy)

        # Spotlaiz Insights
        st.subheader(translate_ui("analysis_title", lang_code))
        insight_prompt = f"""Analyze the marketing campaign strategy and provide concise insights:
        1. Strategy Effectiveness (Score 1-10)
        2. Budget Optimization (Score 1-10)
        3. Key Strengths (Bullet points)
        4. Potential Risks (Bullet points)
        
        Present the analysis as a JSON object with these keys: effectiveness_score, budget_score, strengths, risks"""

        insights_raw = get_gemini_response(insight_prompt, "English")
        try:
            insights = json.loads(insights_raw)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Strategy Effectiveness", f"{insights['effectiveness_score']}/10")
            with col2:
                st.metric("Budget Optimization", f"{insights['budget_score']}/10")
            st.subheader("Key Strengths")
            for strength in insights['strengths']:
                st.markdown(f"- {strength}")
            st.subheader("Potential Risks")
            for risk in insights['risks']:
                st.markdown(f"- {risk}")
        except json.JSONDecodeError:
            st.write("Unable to parse insights. Here's the raw output:")
            st.write(insights_raw)

    # Download option
    if st.button(translate_ui("download_button", lang_code)):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"spotlaiz_strategy_{timestamp}.txt"
        st.download_button(
            label=translate_ui("download_button", lang_code),
            data=strategy,
            file_name=filename,
            mime="text/plain"
        )

st.sidebar.markdown("---")
st.sidebar.write("Powered by Spotlaiz - Your AI Marketing Partner")
