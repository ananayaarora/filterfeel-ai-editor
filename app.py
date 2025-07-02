import streamlit as st
from mood_filter import get_filter_for_mood, gpt_based_mood_filter, generate_caption_for_mood, recommend_music_for_mood
from image_editor import apply_filter
from PIL import Image
import os
import io

st.set_page_config(page_title="FilterFeel", page_icon="🎭")
st.title("🎭 FilterFeel - AI Mood-Bases Photo Editor")
st.write("Upload your photo and enter your mood to get a matching filter, creative caption, and music suggestion.")

openai_key = os.getenv("OPENAI_API_KEY", "")
if not openai_key or openai_key.startswith("sk-") == False:
    st.error("OpenAI API key not set. Please set it in your environment variables.")
else:
    # Sidebar input panel
    with st.sidebar:
        st.title("💭 Mood and Photo Input")
        with st.form("mood_form"):
            user_mood = st.text_input("How are you feeling today?", "")
            uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            submitted = st.form_submit_button("✨ Get Mood Filter")

    # Session state to store results
    if "results" not in st.session_state:
        st.session_state["results"] = None

    # Handle form submission
    if submitted:
        if not user_mood.strip():
            st.warning("Please enter your mood!")
        elif not uploaded_file:
            st.warning("Please upload an image!")
        else:
            with st.spinner("Analyzing your mood and processing your image..."):
                rule_based = get_filter_for_mood(user_mood)
                gpt_based = gpt_based_mood_filter(user_mood)
                caption = generate_caption_for_mood(user_mood)
                music_title, music_youtube, music_spotify = recommend_music_for_mood(user_mood)
                image = Image.open(uploaded_file)
                filtered_image = apply_filter(image, rule_based)
            # Store results in session state
            st.session_state["results"] = {
                "rule_based": rule_based,
                "gpt_based": gpt_based,
                "caption": caption,
                "music_title": music_title,
                "music_youtube": music_youtube,
                "music_spotify": music_spotify,
                "image": image,
                "filtered_image": filtered_image
            }

    # Main area: show results
    results = st.session_state.get("results")
    if results:
        st.success("Here are your mood-based enhancements!")
        st.balloons()
        st.markdown(f"**Rule-Based Filter:** `{results['rule_based']}`")
        st.markdown(f"**GPT-Based Filter:** `{results['gpt_based']}`")
        st.markdown(f"**Caption:** _{results['caption']}_")
        st.markdown(f"**Music Recommendation:** _{results['music_title']}_  ")
        st.markdown(f"[▶️ Listen on YouTube]({results['music_youtube']}) | [🎵 Listen on Spotify]({results['music_spotify']})")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📤 Original Image")
            st.image(results["image"], use_column_width=True)
        with col2:
            st.subheader(f"🎨 Filtered Image ({results['rule_based']})")
            st.image(results["filtered_image"], use_column_width=True)
            # Add download button for filtered image
            buf = io.BytesIO()
            results["filtered_image"].save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Filtered Image",
                data=byte_im,
                file_name="filtered_image.png",
                mime="image/png"
            )
    else:
        st.info("Fill the input panel and submit to see results here.")
