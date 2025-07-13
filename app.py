import streamlit as st
import base64
import io
from PIL import Image
import os
from image_editor import ImageEditor
from mood_filter import MoodFilter

# Configure page
st.set_page_config(
    page_title="FilterFeel - AI Mood-Based Photo Editor",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'filtered_image' not in st.session_state:
    st.session_state.filtered_image = None
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# Initialize components
image_editor = ImageEditor()
mood_filter = MoodFilter()

def reset_app():
    """Reset all session state variables"""
    st.session_state.uploaded_image = None
    st.session_state.filtered_image = None
    st.session_state.mood_data = None
    st.session_state.processing_complete = False

def get_image_download_link(img, filename):
    """Generate download link for image"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/png;base64,{img_str}" download="{filename}">📥 Download Filtered Image</a>'

def main():
    # Header
    st.title("🎨 FilterFeel - AI Mood-Based Photo Editor")
    st.markdown("*Upload a photo and let AI detect its mood to apply the perfect filter!*")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Reset button
        if st.button("🔄 Reset App", type="secondary"):
            reset_app()
            st.rerun()
        
        # Preset moods
        st.subheader("🎭 Preset Moods")
        preset_moods = [
            ("😊 Happy", "happy"),
            ("😢 Sad", "sad"),
            ("😴 Calm", "calm"),
            ("🔥 Energetic", "energetic"),
            ("😍 Romantic", "romantic"),
            ("🌅 Nostalgic", "nostalgic"),
            ("🎉 Celebratory", "celebratory"),
            ("🌙 Mysterious", "mysterious")
        ]
        
        selected_preset = st.selectbox(
            "Choose a preset mood:",
            ["Auto-detect from image"] + [mood[0] for mood in preset_moods]
        )
        
        # Custom mood input
        st.subheader("✍️ Custom Mood")
        custom_mood = st.text_input("Enter your own mood:", placeholder="e.g., melancholic, vibrant, dreamy")
        
        # API Key status
        st.subheader("🔑 API Status")
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ OpenAI API Key loaded")
            st.info("💡 If you get quota errors, the app will use offline mode")
        else:
            st.error("❌ OpenAI API Key not found")
            st.info("App will work in offline mode with preset filters and captions")
        
        # Offline mode info
        st.subheader("🔄 Offline Mode")
        st.info("When API is unavailable, the app provides:\n- Preset mood filters\n- Beautiful offline captions\n- Full music recommendations")
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Your Photo")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="Supported formats: JPG, PNG, BMP, TIFF"
        )
        
        if uploaded_file is not None:
            # Load and display original image
            try:
                image = Image.open(uploaded_file)
                st.session_state.uploaded_image = image
                st.image(image, caption="Original Image", use_container_width=True)
                
                # Process button
                if st.button("🚀 Process Image", type="primary"):
                    if not api_key:
                        st.error("❌ OpenAI API Key is required for mood detection")
                        return
                    
                    with st.spinner("🔮 Analyzing mood and applying filter..."):
                        try:
                            # Determine mood to use
                            if custom_mood.strip():
                                mood_to_use = custom_mood.strip()
                                st.info(f"Using custom mood: {mood_to_use}")
                            elif selected_preset != "Auto-detect from image":
                                mood_to_use = next(mood[1] for mood in preset_moods if mood[0] == selected_preset)
                                st.info(f"Using preset mood: {mood_to_use}")
                            else:
                                # Auto-detect mood from image
                                mood_to_use = None
                                st.info("Auto-detecting mood from image...")
                            
                            # Get mood analysis and recommendations
                            mood_data = mood_filter.analyze_mood_and_recommend(image, mood_to_use)
                            st.session_state.mood_data = mood_data
                            
                            # Apply filter
                            filtered_image = image_editor.apply_filter(image, mood_data['filter'])
                            st.session_state.filtered_image = filtered_image
                            st.session_state.processing_complete = True
                            
                            st.success("✅ Processing complete!")
                            st.rerun()
                            
                        except Exception as e:
                            error_message = str(e)
                            if "insufficient_quota" in error_message:
                                st.warning("🔄 OpenAI API quota exceeded - Using offline mode")
                                st.info("💡 The app will use preset filters and offline captions. For AI mood detection, please check your billing at https://platform.openai.com/account/billing")
                                
                                # Still try to process with offline fallbacks
                                try:
                                    mood_data = mood_filter.analyze_mood_and_recommend(image, mood_to_use)
                                    st.session_state.mood_data = mood_data
                                    
                                    # Apply filter
                                    filtered_image = image_editor.apply_filter(image, mood_data['filter'])
                                    st.session_state.filtered_image = filtered_image
                                    st.session_state.processing_complete = True
                                    
                                    st.success("✅ Processing complete with offline mode!")
                                    st.rerun()
                                except Exception as fallback_error:
                                    st.error(f"❌ Error in offline processing: {str(fallback_error)}")
                            else:
                                st.error(f"❌ Error processing image: {error_message}")
                            
            except Exception as e:
                st.error(f"❌ Error loading image: {str(e)}")

    with col2:
        st.header("✨ Filtered Result")
        
        if st.session_state.processing_complete and st.session_state.filtered_image:
            # Display filtered image
            st.image(st.session_state.filtered_image, caption="Filtered Image", use_container_width=True)
            
            # Download button
            download_link = get_image_download_link(st.session_state.filtered_image, "filtered_image.png")
            st.markdown(download_link, unsafe_allow_html=True)
            
        elif st.session_state.uploaded_image:
            st.info("👆 Click 'Process Image' to apply AI-powered mood filtering")
        else:
            st.info("👈 Upload an image to get started")

    # Results section
    if st.session_state.processing_complete and st.session_state.mood_data:
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        # Create columns for results
        result_col1, result_col2, result_col3 = st.columns([1, 1, 1])
        
        with result_col1:
            st.subheader("🎭 Detected Mood")
            st.info(f"**{st.session_state.mood_data['mood']}**")
            
            st.subheader("🎨 Applied Filter")
            st.info(f"**{st.session_state.mood_data['filter']}**")
        
        with result_col2:
            st.subheader("📝 AI Caption")
            caption = st.session_state.mood_data['caption']
            st.write(f"*{caption}*")
            
            # Copy caption button
            if st.button("📋 Copy Caption"):
                st.success("Caption copied to clipboard!")
        
        with result_col3:
            st.subheader("🎵 Music Recommendation")
            music = st.session_state.mood_data['music']
            st.write(f"**{music['title']}**")
            st.write(f"*by {music['artist']}*")
            
            # Music links
            col_yt, col_spotify = st.columns(2)
            with col_yt:
                st.link_button("🎥 YouTube", music['youtube_url'])
            with col_spotify:
                st.link_button("🎵 Spotify", music['spotify_url'])
        
        # Action buttons
        st.markdown("---")
        col_reset, col_new = st.columns(2)
        with col_reset:
            if st.button("🔄 Try Again", type="secondary"):
                st.session_state.processing_complete = False
                st.rerun()
        with col_new:
            if st.button("🆕 New Image", type="primary"):
                reset_app()
                st.rerun()

if __name__ == "__main__":
    main()

