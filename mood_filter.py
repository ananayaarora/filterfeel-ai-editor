import os
import json
import base64
import io
import openai
import requests
from urllib.parse import quote

class MoodFilter:
    """Handles mood detection, filter mapping, and content generation"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Mood to filter mapping
        self.mood_filters = {
            'happy': 'warm',
            'joyful': 'vibrant',
            'sad': 'cool',
            'melancholy': 'monochrome',
            'calm': 'soft',
            'peaceful': 'ethereal',
            'energetic': 'vibrant',
            'excited': 'dramatic',
            'romantic': 'warm',
            'nostalgic': 'vintage',
            'mysterious': 'moody',
            'dreamy': 'dreamy',
            'serene': 'soft',
            'celebratory': 'golden',
            'contemplative': 'cool',
            'uplifting': 'bright',
            'cozy': 'warm',
            'dramatic': 'dramatic',
            'ethereal': 'ethereal',
            'vibrant': 'vibrant',
            'moody': 'moody',
            'bright': 'bright'
        }
        
        # Offline fallback captions by mood
        self.offline_captions = {
            'happy': 'Sunshine and smiles light up this beautiful moment.',
            'joyful': 'Pure joy radiates from this wonderful scene.',
            'sad': 'Sometimes the heart speaks through quiet moments.',
            'melancholy': 'Beauty found in the depths of contemplation.',
            'calm': 'Serenity captured in perfect stillness.',
            'peaceful': 'Tranquil moments that soothe the soul.',
            'energetic': 'Dynamic energy bursts from every frame.',
            'excited': 'Electric excitement fills the air.',
            'romantic': 'Love stories written in light and shadow.',
            'nostalgic': 'Memories dance in golden hues.',
            'mysterious': 'Secrets whispered in shadows and light.',
            'dreamy': 'Where reality meets imagination.',
            'serene': 'Perfect harmony in peaceful silence.',
            'celebratory': 'Moments of triumph and celebration.',
            'contemplative': 'Deep thoughts reflected in quiet beauty.',
            'uplifting': 'Hope rises like the morning sun.',
            'cozy': 'Warmth and comfort in every detail.',
            'dramatic': 'Intensity captured in striking contrast.',
            'ethereal': 'Otherworldly beauty beyond words.',
            'vibrant': 'Life bursts forth in brilliant colors.',
            'moody': 'Atmospheric depth tells its story.',
            'bright': 'Radiant light illuminates everything.'
        }
        # Music recommendations by mood
        self.music_recommendations = {
            'happy': {
                'title': 'Happy',
                'artist': 'Pharrell Williams',
                'youtube_url': 'https://www.youtube.com/results?search_query=happy+pharrell+williams',
                'spotify_url': 'https://open.spotify.com/search/happy%20pharrell%20williams'
            },
            'joyful': {
                'title': 'Good as Hell',
                'artist': 'Lizzo',
                'youtube_url': 'https://www.youtube.com/results?search_query=good+as+hell+lizzo',
                'spotify_url': 'https://open.spotify.com/search/good%20as%20hell%20lizzo'
            },
            'sad': {
                'title': 'Mad World',
                'artist': 'Gary Jules',
                'youtube_url': 'https://www.youtube.com/results?search_query=mad+world+gary+jules',
                'spotify_url': 'https://open.spotify.com/search/mad%20world%20gary%20jules'
            },
            'melancholy': {
                'title': 'The Night We Met',
                'artist': 'Lord Huron',
                'youtube_url': 'https://www.youtube.com/results?search_query=the+night+we+met+lord+huron',
                'spotify_url': 'https://open.spotify.com/search/the%20night%20we%20met%20lord%20huron'
            },
            'calm': {
                'title': 'Weightless',
                'artist': 'Marconi Union',
                'youtube_url': 'https://www.youtube.com/results?search_query=weightless+marconi+union',
                'spotify_url': 'https://open.spotify.com/search/weightless%20marconi%20union'
            },
            'peaceful': {
                'title': 'Clair de Lune',
                'artist': 'Claude Debussy',
                'youtube_url': 'https://www.youtube.com/results?search_query=clair+de+lune+debussy',
                'spotify_url': 'https://open.spotify.com/search/clair%20de%20lune%20debussy'
            },
            'energetic': {
                'title': 'Uptown Funk',
                'artist': 'Mark Ronson ft. Bruno Mars',
                'youtube_url': 'https://www.youtube.com/results?search_query=uptown+funk+mark+ronson+bruno+mars',
                'spotify_url': 'https://open.spotify.com/search/uptown%20funk%20mark%20ronson'
            },
            'excited': {
                'title': 'Can\'t Stop the Feeling!',
                'artist': 'Justin Timberlake',
                'youtube_url': 'https://www.youtube.com/results?search_query=cant+stop+the+feeling+justin+timberlake',
                'spotify_url': 'https://open.spotify.com/search/can\'t%20stop%20the%20feeling%20justin%20timberlake'
            },
            'romantic': {
                'title': 'Perfect',
                'artist': 'Ed Sheeran',
                'youtube_url': 'https://www.youtube.com/results?search_query=perfect+ed+sheeran',
                'spotify_url': 'https://open.spotify.com/search/perfect%20ed%20sheeran'
            },
            'nostalgic': {
                'title': 'The Way You Look Tonight',
                'artist': 'Frank Sinatra',
                'youtube_url': 'https://www.youtube.com/results?search_query=the+way+you+look+tonight+frank+sinatra',
                'spotify_url': 'https://open.spotify.com/search/the%20way%20you%20look%20tonight%20frank%20sinatra'
            },
            'mysterious': {
                'title': 'Mysterious Ways',
                'artist': 'U2',
                'youtube_url': 'https://www.youtube.com/results?search_query=mysterious+ways+u2',
                'spotify_url': 'https://open.spotify.com/search/mysterious%20ways%20u2'
            },
            'dreamy': {
                'title': 'Dream a Little Dream of Me',
                'artist': 'Ella Fitzgerald',
                'youtube_url': 'https://www.youtube.com/results?search_query=dream+a+little+dream+ella+fitzgerald',
                'spotify_url': 'https://open.spotify.com/search/dream%20a%20little%20dream%20ella%20fitzgerald'
            },
            'serene': {
                'title': 'River',
                'artist': 'Joni Mitchell',
                'youtube_url': 'https://www.youtube.com/results?search_query=river+joni+mitchell',
                'spotify_url': 'https://open.spotify.com/search/river%20joni%20mitchell'
            },
            'celebratory': {
                'title': 'Celebration',
                'artist': 'Kool & The Gang',
                'youtube_url': 'https://www.youtube.com/results?search_query=celebration+kool+and+the+gang',
                'spotify_url': 'https://open.spotify.com/search/celebration%20kool%20the%20gang'
            },
            'contemplative': {
                'title': 'The Sound of Silence',
                'artist': 'Simon & Garfunkel',
                'youtube_url': 'https://www.youtube.com/results?search_query=sound+of+silence+simon+garfunkel',
                'spotify_url': 'https://open.spotify.com/search/sound%20of%20silence%20simon%20garfunkel'
            },
            'uplifting': {
                'title': 'Here Comes the Sun',
                'artist': 'The Beatles',
                'youtube_url': 'https://www.youtube.com/results?search_query=here+comes+the+sun+beatles',
                'spotify_url': 'https://open.spotify.com/search/here%20comes%20the%20sun%20beatles'
            },
            'cozy': {
                'title': 'Autumn Leaves',
                'artist': 'Eva Cassidy',
                'youtube_url': 'https://www.youtube.com/results?search_query=autumn+leaves+eva+cassidy',
                'spotify_url': 'https://open.spotify.com/search/autumn%20leaves%20eva%20cassidy'
            }
        }
    
    def _image_to_base64(self, image):
        """Convert PIL image to base64 string"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def detect_mood_from_image(self, image):
        """Detect mood from image using OpenAI vision API"""
        try:
            base64_image = self._image_to_base64(image)
            
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing the emotional mood and atmosphere of images. "
                                 "Analyze the image and determine the primary mood it conveys. "
                                 "Consider colors, lighting, subjects, composition, and overall atmosphere. "
                                 "Respond with a JSON object containing the mood (single word) and confidence (0-1). "
                                 "Available moods: happy, joyful, sad, melancholy, calm, peaceful, energetic, excited, "
                                 "romantic, nostalgic, mysterious, dreamy, serene, celebratory, contemplative, uplifting, cozy, dramatic, ethereal, vibrant, moody, bright"
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What mood does this image convey? Please analyze the emotional atmosphere."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content)
            mood = result.get('mood', 'calm').lower()
            confidence = result.get('confidence', 0.5)
            
            # Ensure mood is in our supported list
            if mood not in self.mood_filters:
                mood = 'calm'  # Default fallback
            
            return mood, confidence
            
        except Exception as e:
            error_message = str(e)
            if "insufficient_quota" in error_message:
                print(f"OpenAI API quota exceeded: {e}")
                raise e  # Re-raise to be handled by the calling function
            else:
                print(f"Error detecting mood from image: {e}")
                return 'calm', 0.5  # Default fallback
    
    def match_custom_mood(self, custom_mood):
        """Match custom mood to supported mood using GPT"""
        try:
            response = openai.ChatCompletions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at matching emotional descriptions to specific mood categories. "
                                 "Match the given mood to the most appropriate category from the available options. "
                                 "Available moods: happy, joyful, sad, melancholy, calm, peaceful, energetic, excited, "
                                 "romantic, nostalgic, mysterious, dreamy, serene, celebratory, contemplative, uplifting, cozy, dramatic, ethereal, vibrant, moody, bright. "
                                 "Respond with a JSON object containing the matched mood and confidence (0-1)."
                    },
                    {
                        "role": "user",
                        "content": f"Match this mood description to the most appropriate category: '{custom_mood}'"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
            mood = result.get('mood', 'calm').lower()
            confidence = result.get('confidence', 0.5)
            
            # Ensure mood is in our supported list
            if mood not in self.mood_filters:
                mood = 'calm'  # Default fallback
            
            return mood, confidence
            
        except Exception as e:
            error_message = str(e)
            if "insufficient_quota" in error_message:
                print(f"OpenAI API quota exceeded: {e}")
                raise e  # Re-raise to be handled by the calling function
            else:
                print(f"Error matching custom mood: {e}")
                return 'calm', 0.5  # Default fallback
    
    def generate_caption(self, mood, image):
        """Generate a mood-appropriate caption for the image"""
        try:
            base64_image = self._image_to_base64(image)
            
            response = openai.ChatCompletions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a creative caption writer. Generate a single, poetic one-line caption "
                                 f"that captures the {mood} mood of the image. The caption should be inspirational, "
                                 f"artistic, and emotionally resonant. Keep it under 15 words."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Generate a {mood} caption for this image:"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=150
            )
            
            caption = response.choices[0].message.content.strip()
            # Remove quotes if present
            if caption.startswith('"') and caption.endswith('"'):
                caption = caption[1:-1]
            
            return caption
            
        except Exception as e:
            error_message = str(e)
            if "insufficient_quota" in error_message:
                print(f"OpenAI API quota exceeded, using offline caption: {e}")
                return self.offline_captions.get(mood.lower(), f"Capturing the {mood} essence of this moment.")
            else:
                print(f"Error generating caption, using offline caption: {e}")
                return self.offline_captions.get(mood.lower(), f"Capturing the {mood} essence of this moment.")
    def get_filter_for_mood(self, mood):
        """Get the appropriate filter for a given mood"""
        return self.mood_filters.get(mood.lower(), 'soft')
    
    def get_music_for_mood(self, mood):
        """Get music recommendation for a given mood"""
        return self.music_recommendations.get(mood.lower(), {
            'title': 'Imagine',
            'artist': 'John Lennon',
            'youtube_url': 'https://www.youtube.com/results?search_query=imagine+john+lennon',
            'spotify_url': 'https://open.spotify.com/search/imagine%20john%20lennon'
        })
    
    def analyze_mood_and_recommend(self, image, custom_mood=None):
        """Complete mood analysis and recommendation pipeline"""
        try:
            # Determine mood
            if custom_mood:
                if custom_mood.lower() in self.mood_filters:
                    mood = custom_mood.lower()
                    confidence = 1.0
                else:
                    try:
                        mood, confidence = self.match_custom_mood(custom_mood)
                    except Exception as e:
                        if "insufficient_quota" in str(e):
                            # Fallback to basic mood matching without API
                            mood = self._fallback_mood_matching(custom_mood)
                            confidence = 0.8
                        else:
                            raise e
            else:
                mood, confidence = self.detect_mood_from_image(image)
            
            # Get filter
            filter_name = self.get_filter_for_mood(mood)
            
            # Generate caption (with offline fallback built-in)
            caption = self.generate_caption(mood, image)
            
            # Get music recommendation
            music = self.get_music_for_mood(mood)
            
            return {
                'mood': mood.title(),
                'confidence': confidence,
                'filter': filter_name,
                'caption': caption,
                'music': music
            }
            
        except Exception as e:
            error_message = str(e)
            if "insufficient_quota" in error_message:
                # Use offline fallbacks when API is unavailable
                default_mood = 'calm'
                return {
                    'mood': default_mood.title(),
                    'confidence': 0.5,
                    'filter': self.get_filter_for_mood(default_mood),
                    'caption': self.offline_captions.get(default_mood, 'A moment captured in time.'),
                    'music': self.get_music_for_mood(default_mood)
                }
            else:
                print(f"Error in mood analysis pipeline: {e}")
                # Return default values for other errors
                return {
                    'mood': 'Calm',
                    'confidence': 0.5,
                    'filter': 'soft',
                    'caption': 'A moment captured in time.',
                    'music': {
                        'title': 'Imagine',
                        'artist': 'John Lennon',
                        'youtube_url': 'https://www.youtube.com/results?search_query=imagine+john+lennon',
                        'spotify_url': 'https://open.spotify.com/search/imagine%20john%20lennon'
                    }
                }
    def _fallback_mood_matching(self, custom_mood):
        """Simple keyword-based mood matching when API is unavailable"""
        custom_mood_lower = custom_mood.lower()
        
        # Simple keyword matching for common mood descriptions
        mood_keywords = {
            'happy': ['happy', 'joyful', 'cheerful', 'glad', 'pleased', 'delighted'],
            'sad': ['sad', 'melancholy', 'depressed', 'gloomy', 'sorrowful', 'blue'],
            'calm': ['calm', 'peaceful', 'serene', 'tranquil', 'relaxed', 'zen'],
            'energetic': ['energetic', 'dynamic', 'lively', 'vibrant', 'active', 'spirited'],
            'romantic': ['romantic', 'loving', 'tender', 'affectionate', 'passionate'],
            'nostalgic': ['nostalgic', 'vintage', 'retro', 'old', 'classic', 'timeless'],
            'mysterious': ['mysterious', 'enigmatic', 'secretive', 'dark', 'shadowy'],
            'dreamy': ['dreamy', 'ethereal', 'whimsical', 'fantastical', 'magical'],
            'dramatic': ['dramatic', 'intense', 'powerful', 'striking', 'bold'],
            'bright': ['bright', 'radiant', 'luminous', 'brilliant', 'glowing']
        }
        
        # Check for keyword matches
        for mood, keywords in mood_keywords.items():
            if any(keyword in custom_mood_lower for keyword in keywords):
                return mood
        
        # Default fallback
        return 'calm'
            
