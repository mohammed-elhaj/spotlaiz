import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

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
    </style>
    """, unsafe_allow_html=True)

st.title("Spotlaiz Marketing Content Generator")
st.write("Empower your brand with AI-driven marketing solutions")

# Sidebar for content type selection
content_type = st.sidebar.selectbox(
    "Choose Content Type",
    ("Social Media Post", "Marketing Campaign Strategy")
)

if content_type == "Social Media Post":
    st.header("Social Media Post Generator")
    
    platform = st.selectbox("Platform", ["Twitter", "Instagram", "Facebook", "LinkedIn"])
    brand_voice = st.selectbox("Brand Voice", ["Funny", "Informative", "Inspiring", "Professional"])
    product_description = st.text_area("Product/Service Description", max_chars=200)
    key_message = st.text_input("Key Message")

    if st.button("Generate Post"):
        prompt = f"""Create a {brand_voice} social media post for {platform} about the following product/service:
        {product_description}
        Key message: {key_message}
        Include relevant hashtags grouped by category (brand, industry, trending).
        Ensure the post adheres to the platform's character limits."""

        response = get_gemini_response(prompt)

        st.subheader("Generated Post:")
        st.write(response)

        # Spotlaiz Insights
        st.subheader("Spotlaiz Insights")
        insight_prompt = f"Analyze the following social media post and provide brief insights on its effectiveness, considering the platform ({platform}), brand voice ({brand_voice}), and key message:\n\n{response}"
        insights = get_gemini_response(insight_prompt)
        st.write(insights)

elif content_type == "Marketing Campaign Strategy":
    st.header("Marketing Campaign Strategy Outliner")
    
    target_audience = st.text_input("Target Audience", "Describe your ideal customer")
    campaign_goals = st.multiselect("Campaign Goals", ["Brand awareness", "Lead generation", "Sales", "Customer retention"])
    budget = st.slider("Budget", 1000, 100000, 10000)

    if st.button("Generate Strategy"):
        prompt = f"""Create a marketing campaign strategy outline for the following:
        Target Audience: {target_audience}
        Campaign Goals: {', '.join(campaign_goals)}
        Budget: ${budget}

        Include:
        1. Three campaign title ideas with varied styles
        2. Prioritized list of recommended channels with brief justifications
        3. 3-5 content pillars (overarching themes)
        4. Potential KPIs aligned with the chosen goals"""

        strategy = get_gemini_response(prompt)
        st.subheader("Generated Strategy:")
        st.write(strategy)

        # Spotlaiz Insights
        st.subheader("Spotlaiz Insights")
        insight_prompt = f"Analyze the following marketing campaign strategy and provide brief insights on its effectiveness, considering the target audience, goals, and budget:\n\n{strategy}"
        insights = get_gemini_response(insight_prompt)
        st.write(insights)

    # Download option
    if st.button("Download Strategy"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"spotlaiz_strategy_{timestamp}.txt"
        st.download_button(
            label="Click to Download",
            data=strategy,
            file_name=filename,
            mime="text/plain"
        )

st.sidebar.markdown("---")
st.sidebar.write("Powered by Spotlaiz - Your AI Marketing Partner")
