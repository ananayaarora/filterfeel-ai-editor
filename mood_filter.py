# mood_filter.py

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
