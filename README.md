# 🌈 FilterFeel – AI Mood-Based Photo Editor

FilterFeel is an AI-powered photo editor that automatically applies filters
based on the **mood detected in an image**.

You upload a photo → AI understands the mood → the app enhances it instantly.

🔗 **Live Demo**  
https://filterfeel-ai-edito-cajxjnwc4xcxmhfbwg5ksu.streamlit.app/

---

## ✨ What Can FilterFeel Do?
- Detect mood from images using AI
- Apply mood-based photo filters automatically
- Recommend music that matches the detected mood
- Works smoothly even when the OpenAI API is unavailable (offline mode)

---

## 🧠 How It Works
1. User uploads an image
2. Image is analyzed to detect mood
3. A suitable filter is selected automatically
4. Image is processed using OpenCV and PIL
5. Mood details, captions, and music recommendations are shown
6. User downloads the final image

---

## 🛠️ Tech Stack
- **Python**
- **Streamlit**
- **OpenAI GPT-4o**
- **OpenCV**
- **PIL (Pillow)**
- **NumPy**

---

## 🧩 Project Structure
filterfeel-ai-editor/
│── .devcontainer/ # Dev container configuration
│── pycache/ # Python cache files
│── Screenshot_UI/ # App UI screenshots
│── app.py # Main Streamlit application
│── image_editor.py # Image filters & processing logic
│── mood_filter.py # AI mood detection & recommendations
│── requirements.txt # Python dependencies
│── packages.txt # Additional packages (Streamlit Cloud)
│── pyproject.toml # Project configuration
│── .gitignore
│── README.md

---

## 🎨 Image Filters
FilterFeel supports **12 different filters**, including:
- Warm
- Cool
- Vintage
- Dramatic
- Soft
- Bright
- Cinematic  
and more.

Filters are applied automatically based on detected mood.

---

## 🔌 Offline Mode
If the OpenAI API is unavailable:
- Image filters continue to work
- Preset mood captions are used
- Music recommendations still function
- The app switches gracefully without breaking

This ensures reliability even without external AI access.

---

## ▶️ Run Locally

```bash
git clone https://github.com/ananayaarora/filterfeel-ai-editor.git
cd filterfeel-ai-editor
pip install -r requirements.txt
streamlit run app.py






