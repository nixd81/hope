"""
Emotion Detection Module
Handles both facial emotion detection using DeepFace and text emotion detection using EmoRoBERTa.
"""

import cv2
import numpy as np
import torch
from deepface import DeepFace
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

class EmotionDetector:
    """
    Comprehensive emotion detection for both facial expressions and text.
    """
    
    def __init__(self):
        """Initialize emotion detection models"""
        self.face_detector = None
        self.text_tokenizer = None
        self.text_model = None
        self.emotion_labels = None
        
        # Initialize face detection
        self._initialize_face_detection()
        
        # Initialize text emotion detection
        self._initialize_text_emotion_detection()
    
    def _initialize_face_detection(self):
        """Initialize face detection using OpenCV DNN"""
        try:
            # Load face detection model
            prototxt_path = "deploy.prototxt"
            model_path = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
            
            self.face_detector = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
            print("Face detection model loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load face detection model: {e}")
            self.face_detector = None
    
    def _initialize_text_emotion_detection(self):
        """Initialize text emotion detection using EmoRoBERTa"""
        try:
            model_name = "arpanghoshal/EmoRoBERTa"
            self.text_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.text_model = AutoModelForSequenceClassification.from_pretrained(model_name)
            
            # EmoRoBERTa emotion labels
            self.emotion_labels = [
                'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
                'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust',
                'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love',
                'nervousness', 'optimism', 'pride', 'realization', 'relief', 'remorse',
                'sadness', 'surprise', 'neutral'
            ]
            
            print("Text emotion detection model loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load text emotion model: {e}")
            self.text_tokenizer = None
            self.text_model = None
            self.emotion_labels = None
    
    def detect_faces(self, image, confidence_threshold=0.5):
        """
        Detect faces in an image using OpenCV DNN.
        
        Args:
            image (numpy.ndarray): Input image
            confidence_threshold (float): Minimum confidence for face detection
            
        Returns:
            list: List of face bounding boxes and confidence scores
        """
        if self.face_detector is None:
            return []
        
        try:
            h, w = image.shape[:2]
            
            # Prepare input blob
            blob = cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), 1.0,
                (300, 300), (104.0, 177.0, 123.0)
            )
            
            self.face_detector.setInput(blob)
            detections = self.face_detector.forward()
            
            faces = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                
                if confidence > confidence_threshold:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (x, y, x2, y2) = box.astype("int")
                    
                    # Boundary check
                    x = max(0, x)
                    y = max(0, y)
                    x2 = min(w, x2)
                    y2 = min(h, y2)
                    
                    faces.append({
                        'bbox': (x, y, x2, y2),
                        'confidence': confidence
                    })
            
            return faces
            
        except Exception as e:
            print(f"Error in face detection: {e}")
            return []
    
    def detect_face_emotion(self, image):
        """
        Detect emotion from facial expression in an image.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            str: Detected emotion or 'no_face' if no face detected
        """
        try:
            # Convert BGR to RGB for DeepFace
            if len(image.shape) == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Use DeepFace for emotion analysis
            result = DeepFace.analyze(
                image_rgb, 
                actions=['emotion'], 
                enforce_detection=False
            )
            
            # Handle different result formats
            if isinstance(result, list):
                emotion = result[0]['emotion']
            else:
                emotion = result['emotion']
            
            # Get dominant emotion
            dominant_emotion = max(emotion, key=emotion.get)
            
            return dominant_emotion
            
        except Exception as e:
            print(f"Error in face emotion detection: {e}")
            return 'neutral'
    
    def detect_text_emotion(self, text):
        """
        Detect emotion from text using EmoRoBERTa.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Detected emotion
        """
        if self.text_tokenizer is None or self.text_model is None:
            return 'neutral'
        
        try:
            # Tokenize input text
            inputs = self.text_tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512
            )
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.text_model(**inputs)
                logits = outputs.logits
                emotion_id = int(torch.argmax(logits))
            
            # Return corresponding emotion label
            if self.emotion_labels and 0 <= emotion_id < len(self.emotion_labels):
                return self.emotion_labels[emotion_id]
            else:
                return 'neutral'
                
        except Exception as e:
            print(f"Error in text emotion detection: {e}")
            return 'neutral'
    
    def get_emotion_confidence(self, text):
        """
        Get confidence scores for all emotions in text.
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Emotion confidence scores
        """
        if self.text_tokenizer is None or self.text_model is None:
            return {'neutral': 1.0}
        
        try:
            inputs = self.text_tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512
            )
            
            with torch.no_grad():
                outputs = self.text_model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=-1)
            
            # Create emotion confidence dictionary
            emotion_confidences = {}
            if self.emotion_labels:
                for i, emotion in enumerate(self.emotion_labels):
                    if i < len(probabilities[0]):
                        emotion_confidences[emotion] = float(probabilities[0][i])
            
            return emotion_confidences
            
        except Exception as e:
            print(f"Error getting emotion confidence: {e}")
            return {'neutral': 1.0}
    
    def detect_combined_emotion(self, image, text):
        """
        Combine facial and text emotion detection for comprehensive analysis.
        
        Args:
            image (numpy.ndarray): Input image
            text (str): Input text
            
        Returns:
            dict: Combined emotion analysis
        """
        face_emotion = self.detect_face_emotion(image)
        text_emotion = self.detect_text_emotion(text)
        
        # Simple combination logic - can be enhanced with more sophisticated methods
        combined_emotion = self._combine_emotions(face_emotion, text_emotion)
        
        return {
            'face_emotion': face_emotion,
            'text_emotion': text_emotion,
            'combined_emotion': combined_emotion,
            'confidence': {
                'face': 0.8,  # Placeholder - implement actual confidence calculation
                'text': 0.7   # Placeholder
            }
        }
    
    def _combine_emotions(self, face_emotion, text_emotion):
        """
        Combine facial and text emotions using simple rules.
        Can be enhanced with machine learning approaches.
        
        Args:
            face_emotion (str): Facial emotion
            text_emotion (str): Text emotion
            
        Returns:
            str: Combined emotion
        """
        # Simple combination rules
        if face_emotion == text_emotion:
            return face_emotion
        
        # Priority mapping for conflicting emotions
        emotion_priority = {
            'sadness': 3,
            'anger': 3,
            'fear': 3,
            'joy': 2,
            'surprise': 2,
            'disgust': 2,
            'neutral': 1
        }
        
        face_priority = emotion_priority.get(face_emotion, 1)
        text_priority = emotion_priority.get(text_emotion, 1)
        
        if face_priority > text_priority:
            return face_emotion
        elif text_priority > face_priority:
            return text_emotion
        else:
            return text_emotion  # Default to text emotion in case of tie

# Example usage and testing
if __name__ == "__main__":
    # Test emotion detection
    detector = EmotionDetector()
    
    # Test text emotion detection
    test_texts = [
        "I'm so happy today!",
        "This is really frustrating.",
        "I feel sad and lonely.",
        "What a wonderful surprise!"
    ]
    
    print("Testing text emotion detection:")
    for text in test_texts:
        emotion = detector.detect_text_emotion(text)
        print(f"Text: '{text}' -> Emotion: {emotion}")
    
    # Test confidence scores
    print("\nTesting emotion confidence:")
    confidence = detector.get_emotion_confidence("I'm feeling really excited about this!")
    print("Confidence scores:", confidence)
