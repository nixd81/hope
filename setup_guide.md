# Virtual Therapist Setup Guide

A comprehensive guide to set up and run the Virtual Therapist application.

## 🏗️ Architecture Overview

The Virtual Therapist is a full-stack web application with the following components:

### Backend (Python Flask)
- **Emotion Recognition**: Real-time facial emotion detection using DeepFace
- **Text Emotion Analysis**: Sentiment analysis using EmoRoBERTa transformer
- **Image Preprocessing**: Robust preprocessing with CLAHE, noise reduction, and contrast enhancement
- **AI Integration**: Gemini Flash API for empathetic responses
- **Speech Processing**: Speech-to-text and text-to-speech capabilities

### Frontend (React)
- **Google Meet-style UI**: Video call interface with controls
- **Real-time Video**: Webcam stream with emotion overlay
- **Chat Interface**: Text and voice input with AI responses
- **Responsive Design**: Modern, accessible interface

## 📋 Prerequisites

### System Requirements
- Python 3.8+ (recommended: Python 3.9 or 3.10)
- Node.js 16+ and npm
- Webcam and microphone
- 8GB+ RAM (for deep learning models)
- GPU recommended (optional, for faster processing)

### API Keys Required
- **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🚀 Installation Steps

### 1. Clone and Setup Backend

```bash
# Navigate to the project directory
cd virtual-therapist

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Download Required Models

The application requires several pre-trained models. Download them automatically:

```bash
# The models will be downloaded on first run, but you can pre-download them:
python -c "from deepface import DeepFace; DeepFace.build_model('Emotion')"
python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained('arpanghoshal/EmoRoBERTa')"
```

### 3. Setup Environment Variables

Create a `.env` file in the backend directory:

```bash
# Backend/.env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "REACT_APP_API_URL=http://localhost:5000" > .env
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/app.py` to customize:

```python
# Image preprocessing settings
image_preprocessor = ImagePreprocessor(
    target_size=(224, 224),
    preprocessing_method=PreprocessingMethod.COMBINED
)

# Emotion detection settings
emotion_detector = EmotionDetector()

# Gemini API settings
gemini_client = GeminiClient(api_key=os.getenv('GEMINI_API_KEY'))
```

### Frontend Configuration

Edit `frontend/src/App.js` to customize:

```javascript
// API endpoint configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Video constraints
const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: "user"
};
```

## 🏃‍♂️ Running the Application

### 1. Start the Backend

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Navigate to backend directory
cd backend

# Start Flask server
python app.py
```

The backend will be available at `http://localhost:5000`

### 2. Start the Frontend

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start React development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 3. Access the Application

Open your browser and go to `http://localhost:3000`

## 🔧 Troubleshooting

### Common Issues

#### 1. Camera Access Denied
- Ensure browser has camera permissions
- Try using HTTPS (required for some browsers)
- Check if another application is using the camera

#### 2. Model Download Issues
- Ensure stable internet connection
- Check available disk space (models are ~2GB total)
- Try downloading models manually

#### 3. API Key Issues
- Verify Gemini API key is correct
- Check API key has proper permissions
- Ensure environment variables are loaded

#### 4. Performance Issues
- Reduce video resolution in `VideoContainer.js`
- Increase processing interval in `App.js`
- Use GPU acceleration if available

### Debug Mode

Enable debug logging:

```python
# In backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Optimization

### Backend Optimizations

1. **Image Processing**:
   - Adjust preprocessing method in `ImagePreprocessor`
   - Reduce target image size for faster processing
   - Use GPU acceleration if available

2. **Model Loading**:
   - Pre-load models at startup
   - Use model caching
   - Consider model quantization

3. **API Rate Limiting**:
   - Implement request queuing
   - Add response caching
   - Use async processing

### Frontend Optimizations

1. **Video Processing**:
   - Reduce frame capture frequency
   - Implement frame skipping
   - Use Web Workers for processing

2. **Memory Management**:
   - Clear old messages periodically
   - Implement lazy loading
   - Optimize image handling

## 🔒 Security Considerations

### Production Deployment

1. **Environment Variables**:
   - Never commit API keys to version control
   - Use secure environment variable management
   - Implement proper secret rotation

2. **HTTPS**:
   - Enable HTTPS for production
   - Use secure WebSocket connections
   - Implement proper CORS policies

3. **Data Privacy**:
   - Implement data encryption
   - Add user consent mechanisms
   - Follow GDPR/privacy regulations

## 📈 Monitoring and Logging

### Backend Monitoring

```python
# Add logging configuration
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/virtual_therapist.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### Frontend Monitoring

```javascript
// Add error tracking
window.addEventListener('error', (event) => {
  console.error('Frontend error:', event.error);
  // Send to monitoring service
});
```

## 🚀 Production Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables for Production

```bash
# Production environment
FLASK_ENV=production
GEMINI_API_KEY=your_production_api_key
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url
```

## 📚 Additional Resources

- [DeepFace Documentation](https://github.com/serengil/deepface)
- [EmoRoBERTa Model](https://huggingface.co/arpanghoshal/EmoRoBERTa)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [React Webcam Documentation](https://github.com/mozmorris/react-webcam)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue on GitHub
4. Contact the development team

---

**Note**: This application is for educational and research purposes. For clinical use, ensure proper medical supervision and compliance with healthcare regulations.
