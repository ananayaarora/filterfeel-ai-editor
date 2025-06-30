# mood_filter.py

def get_filter_name(mood): 
    #app.py me ye same name chahiye tha 
    """
    This function takes a user’s mood input (string)
    and returns the name of the filter that matches that mood.
    """
    
    mood = mood.lower().strip()  # Clean the input (convert to lowercase and remove spaces)
    
    # Dictionary mapping moods to filter styles
    mood_map = {
        "happy": "warm",
        "joyful": "warm",
        "excited": "warm",
        "calm": "cool",
        "peaceful": "cool",
        "sad": "grayscale",
        "angry": "high_contrast",
        "nostalgic": "sepia",
        "romantic": "rose",
        "tired": "dim",
        "neutral": "natural"
        #bored bhi add karna baaki hai abhi
    }

    # If the mood matches a key, return the corresponding filter
    if mood in mood_map:
        return mood_map[mood]
    
    # If not matched, return default
    return "natural"
