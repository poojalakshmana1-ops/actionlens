import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


load_dotenv()

st.set_page_config(
    page_title="ActionLens",
    page_icon="🔎",
    layout="wide"
)


st.title("🔎 ActionLens")
st.subheader("See it. Understand it. Act on it.")

st.write(
    "Upload a screenshot, notice, poster, form, diagram, or any other image "
    "and ActionLens will turn it into clear, actionable next steps."
)


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()


client = genai.Client(api_key=api_key)


uploaded_image = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg", "webp"]
)


user_text = st.text_area(
    "What do you want to know about this image? (Optional)",
    placeholder="Example: What should I do next?"
)


if uploaded_image:

    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Uploaded Image",
        width="stretch"
    )

    if st.button("🔎 Analyze with ActionLens", type="primary"):

        with st.spinner("ActionLens is analyzing the image..."):

            prompt = f"""
You are ActionLens, a multimodal AI assistant.

Your job is NOT simply to describe an image.

Your job is to help the user understand the image and decide what practical
actions they should take next.

Follow this structure:

SEE
- Identify the important information visible in the image.

UNDERSTAND
- Explain what the information means in simple language.

PRIORITIZE
- Identify deadlines, requirements, warnings, important dates, missing
  information, or urgent items.
- Clearly separate important information from less important information.

ACT
- Give the user a practical step-by-step action checklist.
- Use numbered steps.

VERIFY
- Mention anything the user should double-check before taking action.
- If information is unclear or unreadable, say so instead of inventing it.

USER'S QUESTION:
{user_text if user_text.strip() else "What should I understand and do next based on this image?"}

Return the answer using exactly these sections:

## SEE

## UNDERSTAND

## PRIORITIZE

## ACT

## VERIFY

Be concise, practical, and beginner-friendly.
"""

            try:

                response = client.models.generate_content(
                    model="gemma-4-31b-it",
                    contents=[
                        types.Part.from_bytes(
                            data=uploaded_image.getvalue(),
                            mime_type=uploaded_image.type
                        ),
                        prompt
                    ]
                )

                st.success("Analysis complete!")

                st.markdown(response.text)

            except Exception as e:

                st.error("Something went wrong while analyzing the image.")
                st.exception(e)


st.divider()

st.caption(
    "ActionLens • Multimodal AI Assistant • Powered by Gemma 4"
)