import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly powered by Groq.")

# Sidebar API Key input
with st.sidebar:
    st.header("Settings")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")
    st.markdown("[Get a free Groq API Key](https://console.groq.com/keys)")

# User Selection Inputs
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        ["Social Media Post", "Blog Intro", "Product Announcement", "Educational Snippet", "Newsletter Intro"]
    )
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Threads"]
    )
    tone = st.selectbox(
        "Tone",
        ["Professional", "Casual & Friendly", "Energetic & Hype", "Informative", "Humorous", "Persuasive"]
    )

with col2:
    topic = st.text_input("Topic / Main Idea", placeholder="e.g., Remote work tips for developers")
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineers, Freelancers")

# Generate Content Logic
if st.button("Generate Content", type="primary"):
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill out both the Topic and Target Audience fields.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=groq_api_key)

            # Construct system prompt
            prompt = f"""
            You are an expert social media manager and content strategist. 
            Create a complete post based on the following requirements:
            
            - Content Type: {content_type}
            - Target Platform: {platform}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}

            Structure the response clearly as follows:
            1. **Main Post / Caption**: Tailored to the selected platform style and length constraints.
            2. **Call to Action (CTA)**: Encouraging engagement.
            3. **Hashtags**: A set of 5-10 relevant and trending hashtags.
            """

            with st.spinner("Generating content..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000,
                )

                generated_content = response.choices[0].message.content

                st.subheader("Generated Result")
                st.markdown(generated_content)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
