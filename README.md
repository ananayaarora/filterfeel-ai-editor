# FilterFeel - AI Mood-Based Photo Editor

## Overview

FilterFeel is a Streamlit-based web application that combines computer vision, AI-powered mood detection, and image filtering to automatically apply appropriate photo filters based on the detected mood of uploaded images. The application uses OpenAI's GPT-4o model for mood analysis and provides music recommendations that match the detected mood.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular architecture with three main components:

1. **Frontend Layer**: Streamlit web interface for user interaction
2. **Processing Layer**: Image processing and mood detection services
3. **AI Integration Layer**: OpenAI API integration for mood analysis

The system is designed as a single-page application with session state management for maintaining user data across interactions.

## Key Components

### 1. Main Application (app.py)
- **Purpose**: Streamlit frontend and application orchestration
- **Key Features**:
  - File upload handling
  - Session state management
  - User interface components
  - Image download functionality
- **Architecture Decision**: Uses Streamlit for rapid prototyping and deployment, with session state for maintaining user context

### 2. Image Editor (image_editor.py)
- **Purpose**: Handles all image processing and filter applications
- **Key Features**:
  - 12 different image filters (warm, cool, vintage, dramatic, etc.)
  - PIL and OpenCV integration for image manipulation
  - Format conversion utilities
- **Architecture Decision**: Modular filter system allows easy addition of new filters and maintains separation of concerns

### 3. Mood Filter (mood_filter.py)
- **Purpose**: AI-powered mood detection and filter recommendation
- **Key Features**:
  - OpenAI GPT-4o integration for mood analysis
  - Mood-to-filter mapping system
  - Music recommendation engine
- Offline fallback system with preset captions
  - Keyword-based mood matching when API unavailable
- **Architecture Decision**: Uses OpenAI's latest multimodal model for accurate mood detection from images, with robust offline fallbacks


## Data Flow

1. **Image Upload**: User uploads image through Streamlit interface
2. **Mood Detection**: Image is encoded and sent to OpenAI API for mood analysis (with offline fallback)
3. **Filter Selection**: Detected mood is mapped to appropriate filter using predefined mapping
4. **Image Processing**: Selected filter is applied using PIL/OpenCV operations
5. **Caption Generation**: AI-generated or offline preset captions based on mood
6. **Result Display**: Filtered image is displayed with mood information and music recommendations
7. **Download**: User can download the processed image
## Offline Mode Features
When OpenAI API is unavailable or quota is exceeded:
- **Preset Mood Filters**: All 12 filters work independently of API
- **Offline Captions**: 22 beautifully crafted mood-specific captions
- **Keyword Matching**: Smart mood detection for custom inputs using keyword analysis
- **Full Music Recommendations**: Complete music database works offline
- **Graceful Degradation**: Seamless transition to offline mode with user notification

## External Dependencies

### AI Services
- **OpenAI API**: GPT-4o model for mood detection and analysis
- **API Key**: Required environment variable `OPENAI_API_KEY`

### Python Libraries
- **Streamlit**: Web framework for user interface
- **PIL (Pillow)**: Image processing and manipulation
- **OpenCV**: Advanced image processing operations
- **NumPy**: Numerical operations for image arrays
- **OpenAI Client**: API integration library

### Media Integration
- **YouTube**: Music recommendation links
- **Spotify**: Alternative music platform links

## Deployment Strategy

The application is designed for simple deployment with minimal configuration:

1. **Environment Setup**: Requires only OpenAI API key as environment variable
2. **Dependencies**: All dependencies are standard Python packages
3. **Deployment Options**: 
   - Local development via `streamlit run app.py`
   - Cloud deployment through Streamlit Cloud or similar platforms
   - Container deployment using Docker

### Key Architectural Decisions

1. **Streamlit Choice**: Selected for rapid development and built-in hosting capabilities, avoiding complex frontend/backend separation
2. **OpenAI Integration**: Uses latest GPT-4o model for superior multimodal capabilities over custom computer vision models
3. **Modular Design**: Separate classes for image processing and mood detection enable easy testing and feature extension
4. **Session State Management**: Maintains user context without requiring database storage
5. **Filter Mapping System**: Predefined mood-to-filter mapping provides consistent and predictable results
6. **Multiple Image Libraries**: Combines PIL and OpenCV to leverage strengths of both libraries for different processing tasks

The architecture prioritizes simplicity, modularity, and ease of deployment while providing robust AI-powered functionality.

