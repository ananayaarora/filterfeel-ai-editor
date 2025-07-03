from dotenv import load_dotenv
load_dotenv()
import os
import openai

# Prefer environment variable, fallback to hardcoded key
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-proj-...aapka-key...")

if not openai.api_key or openai.api_key.startswith("sk-") == False:
    raise ValueError("OpenAI API key not set. Please set it in code or as an environment variable.")

# Mood to filter mapping
MOOD_FILTERS = {
    "happy": "warm",
    "sad": "grayscale",
    "excited": "rose",
    "bored": "dim",
    "peaceful": "sepia",
    "energetic": "sharp",
    "nostalgic": "sepia",
    "hopeful": "bright",
    "angry": "cool",
    "relaxed": "sepia",
    "confused": "grayscale",
    "motivated": "sharp",
    "romantic": "rose",
    "lonely": "grayscale",
    "grateful": "warm",
    "anxious": "dim",
    "scared": "grayscale",
    "coward": "grayscale",
    "strong": "sharp"
}

# Mood to caption mapping
MOOD_CAPTIONS = {
    "happy": "Radiating joy and sunshine!",
    "sad": "Even rainy days help us grow.",
    "excited": "Can't wait for what's next!",
    "bored": "Looking for a spark in the ordinary.",
    "peaceful": "Calm mind, happy soul.",
    "energetic": "Full of life and ready to go!",
    "nostalgic": "Memories never fade.",
    "hopeful": "Eyes on the stars, feet on the ground.",
    "angry": "Turning fire into fuel.",
    "relaxed": "Just going with the flow.",
    "confused": "Lost in thought, finding my way.",
    "motivated": "Chasing dreams, one step at a time.",
    "romantic": "Love is in the air.",
    "lonely": "Sometimes, solitude is beautiful.",
    "grateful": "Thankful for every little thing.",
    "anxious": "Taking deep breaths and moving forward.",
    "scared": "Facing my fears, one step at a time.",
    "coward": "Gathering courage to move ahead.",
    "strong": "Unbreakable spirit, unstoppable mind!"
}

# Mood to music mapping
MOOD_MUSIC = {
    "happy": (
        "Happy - Pharrell Williams",
        "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
        "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH"
    ),
    "sad": (
        "Someone Like You - Adele",
        "https://www.youtube.com/watch?v=hLQl3WQQoQ0",
        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
    ),
    "excited": (
        "Can't Stop the Feeling! - Justin Timberlake",
        "https://www.youtube.com/watch?v=ru0K8uYEZWw",
        "https://open.spotify.com/track/6JV2JOEocMgcZxYSZelKcc"
    ),
    "bored": (
        "Bored - Billie Eilish",
        "https://www.youtube.com/watch?v=pbMwTqkKSps",
        "https://open.spotify.com/track/2dLLR6qlu5UJ5gk0dKz0h3"
    ),
    "peaceful": (
        "Weightless - Marconi Union",
        "https://www.youtube.com/watch?v=UfcAVejslrU",
        "https://open.spotify.com/track/7yCPwWs66K8Ba5lFuU2bcx"
    ),
    "energetic": (
        "Stronger - Kanye West",
        "https://www.youtube.com/watch?v=PsO6ZnUZI0g",
        "https://open.spotify.com/track/5CQ30WqJwcep0pYcV4AMNc"
    ),
    "nostalgic": (
        "See You Again - Wiz Khalifa ft. Charlie Puth",
        "https://www.youtube.com/watch?v=RgKAFK5djSk",
        "https://open.spotify.com/track/2b8fOow8UzyDFAE27YhOZM"
    ),
    "hopeful": (
        "Fight Song - Rachel Platten",
        "https://www.youtube.com/watch?v=xo1VInw-SKc",
        "https://open.spotify.com/track/2G7V7zsVDxg1yRsu7Ew9RJ"
    ),
    "angry": (
        "In The End - Linkin Park",
        "https://www.youtube.com/watch?v=eVTXPUF4Oz4",
        "https://open.spotify.com/track/60a0Rd6pjrkxjPbaKzXjfq"
    ),
    "relaxed": (
        "Better Together - Jack Johnson",
        "https://www.youtube.com/watch?v=u57d4_b_YgI",
        "https://open.spotify.com/track/3ebXMykcMXOcLeJ9xZ17XH"
    ),
    "confused": (
        "Lost - Frank Ocean",
        "https://www.youtube.com/watch?v=o_XQaIcIAfg",
        "https://open.spotify.com/track/1R0a2iXumgCiFb7HEZ7gUE"
    ),
    "motivated": (
        "Eye of the Tiger - Survivor",
        "https://www.youtube.com/watch?v=btPJPFnesV4",
        "https://open.spotify.com/track/2KH16WveTQWT6KOG9Rg6e2"
    ),
    "romantic": (
        "Perfect - Ed Sheeran",
        "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
        "https://open.spotify.com/track/0tgVpDi06FyKpA1z0VMD4v"
    ),
    "lonely": (
        "Lonely - Akon",
        "https://www.youtube.com/watch?v=6EEW-9NDM5k",
        "https://open.spotify.com/track/5y6nVaayzitvsI8ZJ0hL3j"
    ),
    "grateful": (
        "Grateful - Rita Ora",
        "https://www.youtube.com/watch?v=5oO5s3nbivA",
        "https://open.spotify.com/track/2QeKHdZQh1nvwK1d8WbD6V"
    ),
    "anxious": (
        "Breathe Me - Sia",
        "https://www.youtube.com/watch?v=wbP0cQkQvvE",
        "https://open.spotify.com/track/5kqIPrATaCc2LqxVWzQGbk"
    ),
    "scared": (
        "Scared to Be Lonely - Martin Garrix & Dua Lipa",
        "https://www.youtube.com/watch?v=e2vBLd5Egnk",
        "https://open.spotify.com/track/0nJW01T7XtvILxQgC5J7Wh"
    ),
    "coward": (
        "Brave - Sara Bareilles",
        "https://www.youtube.com/watch?v=QUQsqBqxoR4",
        "https://open.spotify.com/track/0puf9yIluy9W0vpMEUoAnN"
    ),
    "strong": (
        "Believer - Imagine Dragons",
        "https://www.youtube.com/watch?v=7wtfhZwyrcc",
        "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP"
    )
}

# Helper to get the best match for a mood
def get_best_match(mood, mapping, default):
    mood = mood.lower()
    for key in mapping:
        if key in mood:
            return mapping[key]
    return default

def get_filter_for_mood(mood):
    # Pehle dictionary mapping try karo
    filter_name = get_best_match(mood, MOOD_FILTERS, None)
    if filter_name:
        return filter_name
    # Agar nahi mila, toh GPT-based suggestion use karo
    return gpt_based_mood_filter(mood)

def generate_caption_for_mood(mood):
    return get_best_match(mood, MOOD_CAPTIONS, "Capturing the moment.")

def recommend_music_for_mood(mood):
    return get_best_match(
        mood,
        MOOD_MUSIC,
        (
            "Let It Be - The Beatles",
            "https://www.youtube.com/watch?v=QDYfEBY9NM4",
            "https://open.spotify.com/track/0aym2LBJBk9DAYuHHutrIl"
        )
    )

# ---------------------------
# Optional GPT-Based Logic
# ---------------------------

def gpt_based_mood_filter(mood):
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

User's mood: "{mood}"

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
