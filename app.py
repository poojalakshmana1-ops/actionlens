import streamlit as st

st.set_page_config(
    page_title="ActionLens",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 ActionLens")
st.subheader("See it. Understand it. Act on it.")

st.write(
    "Upload a screenshot, notice, poster, form, diagram, or any other image "
    "and ActionLens will help turn it into clear next steps."
)

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg", "webp"]
)

user_text = st.text_area(
    "What do you want to know about this image? (Optional)",
    placeholder="Example: What should I do next?"
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze with ActionLens"):
        st.info("AI analysis will be connected in the next step.")

st.divider()

st.caption("ActionLens • Multimodal AI Assistant")