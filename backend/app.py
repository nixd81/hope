"""
Virtual Therapist Backend - Flask API
Main application file for the virtual therapist backend.
Handles video processing, emotion recognition, and AI responses.
"""

import cv2
import numpy as np
import base64
import io
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import requests
import json
from deepface import DeepFace
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import speech_recognition as sr
import pyttsx3
from image_preprocessing import ImagePreprocessor
from emotion_detector import EmotionDetector
from gemini_client import GeminiClient
from speech_processor import SpeechProcessor
from websocket_handler import WebSocketHandler
import threading
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
image_preprocessor = ImagePreprocessor()
emotion_detector = EmotionDetector()
gemini_client = GeminiClient()
speech_processor = SpeechProcessor()
websocket_handler = WebSocketHandler(socketio)

# Global state for conversation
conversation_history = []
current_emotions = {
    'face_emotion': 'neutral',
    'text_emotion': 'neutral'
}

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/process_frame', methods=['POST'])
def process_frame():
    """
    Process a video frame for emotion recognition
    Expected input: base64 encoded image
    Returns: detected emotions and confidence scores
    """
    try:
        data = request.get_json()
        if 'frame' not in data:
            return jsonify({'error': 'No frame data provided'}), 400
        
        # Decode base64 image
        frame_data = data['frame'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
        frame_bytes = base64.b64decode(frame_data)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Preprocess the frame
        processed_frame = image_preprocessor.preprocess(frame)
        
        # Detect emotions
        face_emotion = emotion_detector.detect_face_emotion(processed_frame)
        
        # Update global state
        current_emotions['face_emotion'] = face_emotion
        
        return jsonify({
            'face_emotion': face_emotion,
            'confidence': 0.85,  # Placeholder - implement confidence calculation
            'timestamp': time.time()
        })
        
    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({'error': 'Frame processing failed'}), 500

@app.route('/api/process_text', methods=['POST'])
def process_text():
    """
    Process text input for emotion detection and AI response
    Expected input: text message from user
    Returns: AI response and detected text emotion
    """
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        user_text = data['text']
        
        # Detect text emotion
        text_emotion = emotion_detector.detect_text_emotion(user_text)
        current_emotions['text_emotion'] = text_emotion
        
        # Get AI response from Gemini
        ai_response = gemini_client.get_response(
            face_emotion=current_emotions['face_emotion'],
            text_emotion=text_emotion,
            user_message=user_text
        )
        
        # Add to conversation history
        conversation_entry = {
            'user_message': user_text,
            'user_emotion': text_emotion,
            'ai_response': ai_response,
            'timestamp': time.time()
        }
        conversation_history.append(conversation_entry)
        
        return jsonify({
            'ai_response': ai_response,
            'text_emotion': text_emotion,
            'conversation_id': len(conversation_history) - 1
        })
        
    except Exception as e:
        print(f"Error processing text: {e}")
        return jsonify({'error': 'Text processing failed'}), 500

@app.route('/api/process_audio', methods=['POST'])
def process_audio():
    """
    Process audio input for speech-to-text and emotion detection
    Expected input: audio file or base64 encoded audio
    Returns: transcribed text, emotion, and AI response
    """
    try:
        # This would handle audio file upload and speech recognition
        # For now, return a placeholder response
        return jsonify({
            'transcribed_text': 'Audio processing not yet implemented',
            'text_emotion': 'neutral',
            'ai_response': 'I heard your voice, but audio processing is still being developed.'
        })
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({'error': 'Audio processing failed'}), 500

@app.route('/api/conversation', methods=['GET'])
def get_conversation():
    """Get conversation history"""
    return jsonify({
        'conversation': conversation_history,
        'current_emotions': current_emotions
    })

@app.route('/api/emotions', methods=['GET'])
def get_current_emotions():
    """Get current detected emotions"""
    return jsonify(current_emotions)

@app.route('/api/speak', methods=['POST'])
def speak_text():
    """Convert text to speech"""
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        # Use text-to-speech to speak the AI response
        # This would be implemented with pyttsx3 or similar
        return jsonify({'status': 'success', 'message': 'Text spoken'})
        
    except Exception as e:
        print(f"Error with text-to-speech: {e}")
        return jsonify({'error': 'Text-to-speech failed'}), 500

if __name__ == '__main__':
    print("Starting Virtual Therapist Backend...")
    print("Make sure to set your GEMINI_API_KEY in the environment variables")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
