import streamlit as st
from PIL import Image
from image_editor import enhance_image, apply_filter
from mood_filter import get_filter_name

# Page config
st.set_page_config(page_title="FilterFeel", layout="centered")

# Title
st.title("🎨 FilterFeel - AI Mood-Based Photo Editor")
st.markdown("Upload a photo and share your mood — we’ll turn it into an expressive masterpiece.✨")

# Upload Image
uploaded_file = st.file_uploader("📤 Upload your image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Original Image", use_column_width=True)

    # Mood Input
    mood = st.text_input("💬 How are you feeling right now? (e.g., happy, calm, nostalgic)")

    if mood:
        if st.button("✨ Apply Mood Filter"):
            try:
                # Get filter name from mood
                filter_name = get_filter_name(mood)

                # Step 1: Enhance Image (brightness, contrast, sharpness)
                enhanced_img = enhance_image(image)

                # Step 2: Apply Filter (warm, cool, sepia, etc.)
                final_img = apply_filter(enhanced_img, filter_name)

                st.image(final_img, caption=f"🎨 Edited Image – Mood: {mood.capitalize()}", use_column_width=True)

                # Download Button
                st.download_button(
                    label="📥 Download Edited Image",
                    data=final_img.tobytes(),
                    file_name="filtered_image.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"❌ Error applying filter: {e}")

