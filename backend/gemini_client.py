"""
Gemini AI Client
Handles communication with Google's Gemini API for empathetic therapy responses.
"""

import os
import requests
import json
from typing import Dict, Optional

class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    Generates empathetic responses based on user emotions and messages.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key (str, optional): Gemini API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY environment variable.")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def _create_therapy_prompt(self, face_emotion: str, text_emotion: str, user_message: str) -> str:
        """
        Create a therapeutic prompt for Gemini based on user's emotional state.
        
        Args:
            face_emotion (str): Detected facial emotion
            text_emotion (str): Detected text emotion
            user_message (str): User's message
            
        Returns:
            str: Formatted prompt for Gemini
        """
        # Create empathetic context based on emotions
        emotion_context = self._get_emotion_context(face_emotion, text_emotion)
        
        prompt = f"""You are an empathetic virtual therapist. Based on the user's emotional state and message, provide a supportive, understanding response.

User's facial emotion: {face_emotion}
User's text emotion: {text_emotion}
User's message: "{user_message}"

Context: {emotion_context}

Guidelines:
- Be warm, empathetic, and non-judgmental
- Acknowledge their emotional state
- Ask gentle, open-ended questions to understand their feelings better
- Provide supportive guidance without being prescriptive
- Keep responses concise (2-3 sentences) but meaningful
- Use "I" statements to show understanding
- Avoid clinical language - be conversational and human

Respond as a caring therapist would:"""

        return prompt
    
    def _get_emotion_context(self, face_emotion: str, text_emotion: str) -> str:
        """
        Generate contextual guidance based on detected emotions.
        
        Args:
            face_emotion (str): Facial emotion
            text_emotion (str): Text emotion
            
        Returns:
            str: Contextual guidance for the AI
        """
        # Map emotions to therapeutic approaches
        emotion_guidance = {
            'sad': "The user appears to be feeling sad. Show empathy, validate their feelings, and gently explore what's causing their sadness. Offer comfort and hope.",
            'angry': "The user seems angry or frustrated. Acknowledge their feelings, help them identify the source of their anger, and guide them toward calming techniques.",
            'fear': "The user appears anxious or fearful. Provide reassurance, help them feel safe, and gently explore what's causing their anxiety.",
            'happy': "The user seems to be in a positive mood. Celebrate with them, encourage them to share what's making them happy, and reinforce positive feelings.",
            'surprise': "The user seems surprised. Help them process whatever unexpected event or information they're dealing with.",
            'disgust': "The user appears to be feeling disgusted or repulsed. Validate their feelings and help them process what's causing this reaction.",
            'neutral': "The user's emotional state is neutral. Be warm and inviting, ask how they're feeling, and create a safe space for them to share."
        }
        
        # Use the more specific emotion (face or text) for guidance
        primary_emotion = face_emotion if face_emotion != 'neutral' else text_emotion
        return emotion_guidance.get(primary_emotion, emotion_guidance['neutral'])
    
    def get_response(self, face_emotion: str, text_emotion: str, user_message: str) -> str:
        """
        Get an empathetic response from Gemini based on user's emotional state.
        
        Args:
            face_emotion (str): Detected facial emotion
            text_emotion (str): Detected text emotion  
            user_message (str): User's message
            
        Returns:
            str: Gemini's empathetic response
        """
        try:
            prompt = self._create_therapy_prompt(face_emotion, text_emotion, user_message)
            
            # Prepare request data for Gemini API
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 200,
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH", 
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            }
            
            # Make API request
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract response text from Gemini API response
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        return candidate['content']['parts'][0]['text']
                
                return "I understand how you're feeling. Can you tell me more about what's on your mind?"
            else:
                print(f"Gemini API Error: {response.status_code} - {response.text}")
                return self._get_fallback_response(face_emotion, text_emotion)
                
        except requests.exceptions.Timeout:
            print("Gemini API request timed out")
            return self._get_fallback_response(face_emotion, text_emotion)
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._get_fallback_response(face_emotion, text_emotion)
    
    def _get_fallback_response(self, face_emotion: str, text_emotion: str) -> str:
        """
        Provide fallback responses when API is unavailable.
        
        Args:
            face_emotion (str): Detected facial emotion
            text_emotion (str): Detected text emotion
            
        Returns:
            str: Fallback empathetic response
        """
        fallback_responses = {
            'sad': "I can sense that you're going through a difficult time. I'm here to listen and support you. What's been weighing on your mind?",
            'angry': "I understand you're feeling frustrated or angry. That's completely valid. Can you help me understand what's causing these feelings?",
            'fear': "I can see you might be feeling anxious or worried. You're safe here, and I want to help you work through whatever is troubling you.",
            'happy': "It's wonderful to see you in good spirits! I'd love to hear more about what's bringing you joy right now.",
            'neutral': "Hello! I'm here to listen and support you. How are you feeling today? What would you like to talk about?"
        }
        
        primary_emotion = face_emotion if face_emotion != 'neutral' else text_emotion
        return fallback_responses.get(primary_emotion, fallback_responses['neutral'])
    
    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            test_prompt = "Hello, this is a test message."
            response = self.get_response('neutral', 'neutral', test_prompt)
            return len(response) > 0
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Test the Gemini client
    try:
        client = GeminiClient()
        
        # Test connection
        if client.test_connection():
            print("✅ Gemini API connection successful")
        else:
            print("❌ Gemini API connection failed")
        
        # Test empathetic response
        test_cases = [
            ("sad", "sadness", "I've been feeling really down lately"),
            ("angry", "anger", "I'm so frustrated with everything"),
            ("happy", "joy", "I just got great news!"),
            ("neutral", "neutral", "Hello, how are you?")
        ]
        
        print("\nTesting empathetic responses:")
        for face_emotion, text_emotion, message in test_cases:
            response = client.get_response(face_emotion, text_emotion, message)
            print(f"\nEmotions: {face_emotion}/{text_emotion}")
            print(f"Message: {message}")
            print(f"Response: {response}")
            
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your GEMINI_API_KEY environment variable")
