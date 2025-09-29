# 🤖 Virtual Therapist - AI-Powered Emotional Support

A full-stack web application that provides AI-powered emotional support through a Google Meet-style interface. Users can interact with an empathetic AI therapist using video, text, and voice input with real-time emotion recognition.

![Virtual Therapist Demo](https://img.shields.io/badge/Status-Ready%20for%20Demo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)

## ✨ Features

### 🎥 Real-time Video Processing
- **Live Webcam Feed**: Google Meet-style video interface
- **Facial Emotion Recognition**: Real-time emotion detection using DeepFace
- **Advanced Image Preprocessing**: CLAHE, noise reduction, brightness normalization
- **Visual Emotion Overlay**: Real-time emotion display with icons

### 💬 Intelligent Conversation
- **Text Input**: Type messages to the AI therapist
- **Voice Input**: Speech-to-text for natural conversation
- **Emotion-Aware Responses**: AI responses based on detected emotions
- **Empathetic AI**: Gemini Flash integration for therapeutic responses

### 🎛️ Interactive Controls
- **Camera Toggle**: Turn video on/off with visual feedback
- **Microphone Control**: Voice input with listening indicators
- **Real-time Chat**: Live conversation history
- **Emotion Display**: Current emotional state visualization

## 🏗️ Architecture

### Backend (Python Flask)
```
backend/
├── app.py                 # Main Flask application
├── image_preprocessing.py  # Advanced image preprocessing
├── emotion_detector.py    # Facial & text emotion detection
├── gemini_client.py       # AI response generation
├── speech_processor.py    # Speech-to-text & text-to-speech
├── websocket_handler.py   # Real-time communication
└── templates/             # HTML templates
```

### Frontend (React)
```
frontend/src/
├── App.js                 # Main React application
├── components/
│   ├── VideoContainer.js  # Video display & controls
│   ├── ChatPanel.js       # Chat interface
│   ├── ControlPanel.js    # Camera/mic controls
│   ├── EmotionDisplay.js  # Emotion visualization
│   └── LoadingSpinner.js  # Loading indicators
└── index.css             # Global styles
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Webcam and microphone
- Gemini API key

### 1. Clone Repository
```bash
git clone <repository-url>
cd virtual-therapist
```

### 2. Setup Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_api_key_here
```

### 3. Setup Frontend
```bash
cd frontend
npm install
```

### 4. Run Application
```bash
# Terminal 1: Start Backend
cd backend
python app.py

# Terminal 2: Start Frontend
cd frontend
npm start
```

### 5. Access Application
Open `http://localhost:3000` in your browser

## 🔧 Configuration

### Environment Variables
```bash
# Backend
GEMINI_API_KEY=your_gemini_api_key
FLASK_ENV=development
FLASK_DEBUG=True

# Frontend
REACT_APP_API_URL=http://localhost:5000
```

### Image Preprocessing Options
```python
# Available preprocessing methods
PreprocessingMethod.GRAYSCALE_EQUALIZATION
PreprocessingMethod.COLOR_EQUALIZATION
PreprocessingMethod.CLAHE
PreprocessingMethod.CLAHE_COLOR
PreprocessingMethod.COMBINED  # Recommended
```

## 📊 Technical Details

### Emotion Recognition Pipeline
1. **Video Capture**: Real-time webcam feed
2. **Face Detection**: OpenCV DNN face detection
3. **Image Preprocessing**: CLAHE, noise reduction, normalization
4. **Emotion Analysis**: DeepFace emotion classification
5. **Text Analysis**: EmoRoBERTa for text emotion detection
6. **AI Response**: Gemini Flash for empathetic responses

### Supported Emotions
- **Facial**: Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral
- **Text**: 28 emotions including Joy, Sadness, Anger, Fear, etc.

### AI Response System
- **Context-Aware**: Considers both facial and text emotions
- **Empathetic**: Tailored responses based on emotional state
- **Therapeutic**: Designed for emotional support and guidance

## 🛠️ Development

### Project Structure
```
virtual-therapist/
├── backend/               # Python Flask backend
├── frontend/              # React frontend
├── requirements.txt       # Python dependencies
├── setup_guide.md        # Detailed setup instructions
└── README.md             # This file
```

### Key Components

#### Backend Modules
- **ImagePreprocessor**: Advanced image preprocessing with multiple methods
- **EmotionDetector**: Facial and text emotion detection
- **GeminiClient**: AI response generation with empathetic prompts
- **SpeechProcessor**: Speech-to-text and text-to-speech
- **WebSocketHandler**: Real-time communication

#### Frontend Components
- **VideoContainer**: Webcam display with emotion overlay
- **ChatPanel**: Conversation interface with message history
- **ControlPanel**: Camera and microphone controls
- **EmotionDisplay**: Real-time emotion visualization

## 🔒 Security & Privacy

### Data Handling
- **Local Processing**: Video processing happens locally
- **No Storage**: No video or audio data is stored
- **Secure API**: Encrypted communication with AI services
- **Privacy First**: User data is not logged or tracked

### Production Considerations
- Use HTTPS for secure communication
- Implement proper CORS policies
- Add rate limiting for API endpoints
- Use environment variables for sensitive data

## 📈 Performance Optimization

### Backend Optimizations
- **Model Caching**: Pre-load deep learning models
- **Async Processing**: Non-blocking emotion analysis
- **Image Optimization**: Efficient preprocessing pipeline
- **Memory Management**: Proper cleanup of resources

### Frontend Optimizations
- **Frame Skipping**: Reduce processing frequency
- **Lazy Loading**: Load components on demand
- **Memory Management**: Clear old messages periodically
- **Responsive Design**: Optimized for different screen sizes

## 🧪 Testing

### Backend Testing
```bash
# Run backend tests
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
# Run frontend tests
cd frontend
npm test
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Production Environment
```bash
# Set production environment variables
FLASK_ENV=production
GEMINI_API_KEY=your_production_key
DATABASE_URL=your_database_url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues
- **Camera Access**: Ensure browser permissions are granted
- **Model Download**: Check internet connection for model downloads
- **API Errors**: Verify Gemini API key is correct
- **Performance**: Reduce video resolution for better performance

### Getting Help
- Check the [setup guide](setup_guide.md) for detailed instructions
- Review the troubleshooting section
- Create an issue on GitHub
- Contact the development team

## 🙏 Acknowledgments

- **OpenCV**: Computer vision and face detection
- **DeepFace**: Facial emotion recognition
- **Hugging Face**: EmoRoBERTa text emotion model
- **Google**: Gemini Flash API for AI responses
- **React**: Frontend framework
- **Flask**: Backend framework

## 📚 Resources

- [DeepFace Documentation](https://github.com/serengil/deepface)
- [EmoRoBERTa Model](https://huggingface.co/arpanghoshal/EmoRoBERTa)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [React Webcam](https://github.com/mozmorris/react-webcam)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)

---

**Note**: This application is for educational and research purposes. For clinical use, ensure proper medical supervision and compliance with healthcare regulations.

## 🎯 Roadmap

### Upcoming Features
- [ ] Multi-language support
- [ ] Advanced emotion analytics
- [ ] Session recording and playback
- [ ] Mobile app development
- [ ] Integration with healthcare systems
- [ ] Advanced AI personality customization

### Version History
- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Added WebSocket support for real-time communication
- **v1.2.0**: Enhanced image preprocessing pipeline
- **v1.3.0**: Improved AI response system

---

**Built with ❤️ for emotional well-being and AI research**
