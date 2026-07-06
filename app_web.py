"""
AI Content Generator - Web UI (Groq Version)
=============================================
Groq FREE API use karta hai — koi credit card nahi chahiye!

Setup:
    pip install groq streamlit

Chalane ke liye:
    python -m streamlit run app_web.py
"""

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Generator",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI Content Generator")
st.caption("Blog posts aur social media captions AI se banao")

# ─── API Key — Streamlit Secrets se automatically aati hai ───────────────────
# Local chalane ke liye: set GROQ_API_KEY=your_key PowerShell mein
import os
api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("✍️ AI Content Generator")
    st.markdown("Apna topic likho, platform choose karo aur AI se content banao!")
    st.divider()
    st.markdown("**Kaise use karein:**")
    st.markdown("1. Topic likho\n2. Content type choose karo\n3. Tone select karo\n4. Language choose karo\n5. Generate dabao!")
    st.divider()
    st.markdown("**Supported Platforms:**")
    st.markdown("📝 Blog Post\n📸 Instagram\n🐦 Twitter/X\n💼 LinkedIn\n👥 Facebook\n📧 Email")
    st.divider()
    st.caption("⚡ Powered by Groq AI — Built by Khalid Khan")

# ─── Main Form ────────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        options=[
            "Blog Post",
            "Instagram Caption",
            "Twitter/X Post",
            "LinkedIn Post",
            "Facebook Post",
            "Email",
        ],
    )

with col2:
    tone = st.selectbox(
        "Tone",
        options=["Professional", "Friendly", "Funny", "Inspirational", "Educational"],
    )

topic = st.text_area(
    "Topic",
    placeholder="e.g. Pakistan mein freelancing ke fayde, AI tools beginners ke liye, ...",
    height=80,
)

language = st.radio(
    "Language",
    options=["English", "Urdu", "Hinglish"],
    horizontal=True,
)

generate_btn = st.button("⚡ Generate Content", type="primary", use_container_width=True)

# ─── Prompts ──────────────────────────────────────────────────────────────────

PROMPTS = {
    "Blog Post": """
Tum ek expert blog writer ho. Topic: {topic}. Tone: {tone}. Language: {language}.
Ek engaging blog post likho jisme:
- Ek catchy SEO-friendly title (# heading)
- Hook intro jo reader ko engage kare
- 3-4 main sections (## headings)
- Practical tips aur examples
- Strong conclusion with call-to-action
Format: Markdown. Length: 400-600 words.
""",
    "Instagram Caption": """
Tum ek viral Instagram content creator ho. Topic: {topic}. Tone: {tone}. Language: {language}.
Likho:
- Hook line (first line jo scroll rokay)
- 3-4 engaging lines
- Emotional connection
- Clear call-to-action (comment/save/share)
- 15-20 relevant hashtags
Length: 150-200 words (hashtags ke bina).
""",
    "Twitter/X Post": """
Topic: {topic}. Tone: {tone}. Language: {language}.
Ek viral tweet thread likho (3-5 tweets):
- Tweet 1: Strong hook (280 chars max)
- Tweet 2-4: Key points
- Last tweet: CTA + 2-3 hashtags
Har tweet ko 1/ 2/ 3/ se number karo.
""",
    "LinkedIn Post": """
Tum ek LinkedIn thought leader ho. Topic: {topic}. Tone: {tone}. Language: {language}.
Professional post likho:
- Attention-grabbing opening line
- Personal story ya insight
- 3-5 key takeaways (bullets)
- Lesson ya value
- Engaging question readers ke liye
- 3-5 professional hashtags
Length: 200-300 words.
""",
    "Facebook Post": """
Tum ek Facebook community manager ho. Topic: {topic}. Tone: {tone}. Language: {language}.
Engaging post likho:
- Warm, conversational opening
- Relatable story ya situation
- Value-packed middle
- Poll ya question for engagement
- 3-5 hashtags
Length: 150-250 words.
""",
    "Email": """
Tum ek professional email copywriter ho. Topic: {topic}. Tone: {tone}. Language: {language}.
Ek complete email likho jisme:

Subject Line: [Catchy subject line jo open karwaye]
Preview Text: [50 characters ka preview text]

Body:
- Personalized greeting
- Hook opening line
- Main message (2-3 short paragraphs)
- Clear call-to-action
- Professional sign-off

Length: 200-350 words. Simple aur clear language use karo.
""",
}

# ─── Generation ───────────────────────────────────────────────────────────────

if generate_btn:
    if not topic.strip():
        st.error("⚠️ Topic likho pehle!")
    elif not api_key:
        st.error("⚠️ API configuration error. Please contact the admin.")
    else:
        with st.spinner("⚡ AI content generate kar raha hai..."):
            try:
                client = Groq(api_key=api_key)

                prompt = PROMPTS[content_type].format(
                    topic=topic,
                    tone=tone,
                    language=language,
                )

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )

                result = response.choices[0].message.content

                st.success("✅ Content ready!")
                st.divider()

                if content_type == "Blog Post":
                    st.markdown(result)
                else:
                    st.text_area("Generated Content", value=result, height=300)

                st.download_button(
                    label="📥 Download (.txt)",
                    data=result,
                    file_name=f"{content_type.lower().replace(' ', '_')}_{topic[:20]}.txt",
                    mime="text/plain",
                )

            except Exception as e:
                err = str(e)
                if "invalid_api_key" in err or "401" in err:
                    st.error("❌ API configuration error. Please contact admin.")
                elif "rate_limit" in err:
                    st.error("⏳ Bohot zyada requests! Thodi der baad try karein.")
                else:
                    st.error(f"Error: {e}")
