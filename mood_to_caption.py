import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if API key loaded
if not openai.api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")



# Fallback dictionary (offline mode)
fallback_captions = {
    "happy": "Happiness looks good on you 😊",
    "sad": "Even the clouds cry sometimes ☁️",
    "calm": "Breathe in peace, exhale the noise 🌿",
    "angry": "From fire comes change 🔥",
    "romantic": "Hearts speak in silence ❤️",
    "tired": "Exhaustion is just paused energy 😴",
    "nostalgic": "Let it fade, but never be forgotten 🕰️",
    "joyful": "Today is a celebration 🎉",
    "neutral": "Stillness has its own sound 🌫️"
}

def get_caption(mood):
    mood = mood.lower().strip()
    
    try:
        prompt = f"Generate a poetic one-line Instagram caption for a photo based on the mood: '{mood}'. Keep it expressive, concise, and elegant."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic and expressive caption writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=30,
        )

        return response.choices[0].message['content'].strip()

    except Exception as e:
        # If internet down or key invalid → fallback caption
        return fallback_captions.get(mood, "Let your photo say what words can’t ✨")

