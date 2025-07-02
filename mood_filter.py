3# mood_filter.py

from dotenv import load_dotenv
load_dotenv()
import os
import openai

# Prefer environment variable, fallback to hardcoded key
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-proj-...aapka-key...")

if not openai.api_key or openai.api_key.startswith("sk-") == False:
    raise ValueError("OpenAI API key not set. Please set it in code or as an environment variable.")

def get_filter_for_mood(mood_input):
    """
    Expanded mood-to-filter logic.
    Handles aliases and basic free-text matching.
    """

    mood_input = mood_input.lower().strip()

    # Step 1: Define mood categories (with synonyms/aliases)
    mood_keywords = {
        "happy": ["happy", "joyful", "cheerful", "excited", "delighted"],
        "calm": ["calm", "relaxed", "serene", "chill", "cool"],
        "sad": ["sad", "down", "depressed", "unhappy", "lonely"],
        "romantic": ["romantic", "in love", "loving", "sweet"],
        "angry": ["angry", "mad", "furious", "annoyed", "frustrated"],
        "tired": ["tired", "exhausted", "sleepy", "drained"],
        "nostalgic": ["nostalgic", "memory", "past", "old"],
        "peaceful": ["peaceful", "zen", "still", "quiet"],
    }

    mood_to_filter = {
        "happy": "warm",
        "calm": "cool",
        "sad": "grayscale",
        "romantic": "sepia",
        "angry": "high_contrast",
        "tired": "low_saturation",
        "nostalgic": "sepia",
        "peaceful": "pastel"
    }

    # Step 2: Keyword matching
    for mood_category, keywords in mood_keywords.items():
        for keyword in keywords:
            if keyword in mood_input:
                return mood_to_filter[mood_category]

    # Step 3: Default fallback
    return "default"

# ---------------------------
# Optional GPT-Based Logic
# ---------------------------

def gpt_based_mood_filter(mood_input):
    """
    Uses GPT to map free-form emotional text to a photo filter.
    Returns one of: warm, cool, sepia, grayscale, high_contrast, low_saturation, pastel, default
    """
    prompt = f"""
You are a helpful assistant that chooses the best photo filter based on how a person is feeling.
Available filters are:
- warm
- cool
- sepia
- grayscale
- high_contrast
- low_saturation
- pastel

User's mood: "{mood_input}"

What is the best matching filter name from the list above? Just reply with the filter name only.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative photo mood assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=10
        )
        filter_name = response.choices[0].message['content'].strip().lower()
        return filter_name
    except Exception as e:
        print("Error using GPT:", e)
        return "default"

def rule_based_caption_for_mood(mood_input):
    """
    Returns a simple, friendly caption based on the detected mood using rules, with emojis.
    """
    mood_input = mood_input.lower().strip()
    mood_captions = {
        "happy": "Smiles all around! 😄✨",
        "calm": "Peace in every pixel. 🧘‍♂️🌿",
        "sad": "Finding beauty in the blues. 💧🦋",
        "romantic": "Love is in the air. 💖🌹",
        "angry": "Bold vibes, strong spirit. 😤🔥",
        "tired": "Taking a moment to rest. 😴☁️",
        "nostalgic": "Memories that linger. 📸🕰️",
        "peaceful": "Serenity captured. 🕊️🌸",
    }
    # Step 1: Keyword matching
    for mood, caption in mood_captions.items():
        if mood in mood_input:
            return caption
    # Step 2: Default fallback
    return "A moment worth sharing. 📷✨"

def generate_caption_for_mood(mood_input):
    """
    Returns a rule-based caption for a photo based on the user's mood.
    """
    return rule_based_caption_for_mood(mood_input)

def rule_based_music_for_mood(mood_input):
    """
    Returns a tuple: (song or playlist recommendation, YouTube link, Spotify link) based on the detected mood using rules.
    """
    mood_input = mood_input.lower().strip()
    mood_music = {
        "happy": ("'Happy' by Pharrell Williams", "https://www.youtube.com/watch?v=ZbZSe6N_BXs", "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH"),
        "calm": ("'Weightless' by Marconi Union", "https://www.youtube.com/watch?v=UfcAVejslrU", "https://open.spotify.com/track/7gZfnEnfia0P2ATo5bY5U3"),
        "sad": ("'Someone Like You' by Adele", "https://www.youtube.com/watch?v=hLQl3WQQoQ0", "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"),
        "romantic": ("'Perfect' by Ed Sheeran", "https://www.youtube.com/watch?v=2Vv-BfVoq4g", "https://open.spotify.com/track/0tgVpDi06FyKpA1z0VMD4v"),
        "angry": ("'Stronger' by Kanye West", "https://www.youtube.com/watch?v=PsO6ZnUZI0g", "https://open.spotify.com/track/3yfqSUWxFvZELEM4PmlwIR"),
        "tired": ("'Let Her Go' by Passenger", "https://www.youtube.com/watch?v=RBumgq5yVrA", "https://open.spotify.com/track/2jyjhRf6DVbMPU5zxagN2h"),
        "nostalgic": ("'Summer of '69' by Bryan Adams", "https://www.youtube.com/watch?v=eFjjO_lhf9c", "https://open.spotify.com/track/3B54sVLJ402zGa6Xm4YGNe"),
        "peaceful": ("'River Flows In You' by Yiruma", "https://www.youtube.com/watch?v=7maJOI3QMu0", "https://open.spotify.com/track/7yCPwWs66K8Ba5lFuU2bcx"),
    }
    # Step 1: Keyword matching
    for mood, song_tuple in mood_music.items():
        if mood in mood_input:
            return song_tuple
    # Step 2: Default fallback
    return ("'Viva La Vida' by Coldplay", "https://www.youtube.com/watch?v=dvgZkm1xWPE", "https://open.spotify.com/track/1mea3bSkSGXuIRvnydlB5b")

def recommend_music_for_mood(mood_input):
    """
    Returns a tuple: (song or playlist recommendation, YouTube link, Spotify link) for the user's mood.
    """
    return rule_based_music_for_mood(mood_input)

#test the code
if __name__ == "__main__":
    user_input = input("How are you feeling today? ")

    # Rule-based result
    rule_based = get_filter_for_mood(user_input)
    print(f"🎯 Rule-Based Filter: {rule_based}")

    # GPT-based result (optional)
    gpt_based = gpt_based_mood_filter(user_input)
    print(f"🤖 GPT-Based Filter: {gpt_based}")

    # Mood Caption
    caption = generate_caption_for_mood(user_input)
    print(f"📝 Caption: {caption}")

    # Music Recommendation
    music = recommend_music_for_mood(user_input)
    print(f"🎵 Music Recommendation: {music}")
