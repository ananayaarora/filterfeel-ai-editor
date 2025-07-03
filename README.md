# 🎭 FilterFeel – AI Mood-Based Photo Editor

FilterFeel is a Streamlit-based web application that applies photo filters, generates captions, and recommends music based on the user's mood using both rule-based logic and GPT-powered intelligence.

## ✨ Features

- 🎨 Mood-based filter suggestions (Rule-Based & GPT-Based)
- 📝 Auto-generated captions for your mood
- 🎵 Music recommendations with YouTube and Spotify links
- 📸 Upload image and get instant, mood-enhanced preview
- ⬇️ Download the filtered image
- 🔁 Try Again & 🗑️ Clear Results buttons for quick reuse

## 🧠 Tech Stack

| Layer        | Technology                 |
|-------------|-----------------------------|
| Frontend     | Streamlit                  |
| Backend      | Python (OpenAI API, Pillow)|
| ML/NLP Logic | Rule-based + GPT-3.5 Turbo |
| Image Editor | Pillow (PIL)               |

---

## 📁 Folder Structure

- `app.py`: Streamlit UI
- `mood_filter.py`: Mood → filter logic
- `image_editor.py`: Enhancement + filter functions
- `.env`: Contains your OpenAI API key (not tracked)
- `requirements.txt`: Dependencies
- `README.md`: Project documentation