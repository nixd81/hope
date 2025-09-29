"""
Speech Processing Module
Handles speech-to-text and text-to-speech functionality.
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
from typing import Optional, Callable

class SpeechProcessor:
    """
    Handles speech recognition and text-to-speech synthesis.
    """
    
    def __init__(self):
        """Initialize speech processing components"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.callback = None
        
        # Initialize TTS engine
        self._initialize_tts()
        
        # Adjust for ambient noise
        self._calibrate_microphone()
    
    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to use a female voice for more empathetic responses
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            
        except Exception as e:
            print(f"Warning: Could not initialize TTS engine: {e}")
            self.tts_engine = None
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone calibrated for ambient noise")
        except Exception as e:
            print(f"Warning: Could not calibrate microphone: {e}")
    
    def start_listening(self, callback: Optional[Callable] = None):
        """
        Start continuous speech recognition.
        
        Args:
            callback: Function to call when speech is recognized
        """
        if self.is_listening:
            return
        
        self.callback = callback
        self.is_listening = True
        
        # Start listening in a separate thread
        listen_thread = threading.Thread(target=self._listen_continuously)
        listen_thread.daemon = True
        listen_thread.start()
    
    def stop_listening(self):
        """Stop speech recognition"""
        self.is_listening = False
    
    def _listen_continuously(self):
        """Continuously listen for speech"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Recognize speech in a separate thread to avoid blocking
                recognition_thread = threading.Thread(
                    target=self._recognize_audio, 
                    args=(audio,)
                )
                recognition_thread.daemon = True
                recognition_thread.start()
                
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                continue
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                time.sleep(0.1)
    
    def _recognize_audio(self, audio):
        """Recognize speech from audio data"""
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            
            if text and self.callback:
                self.callback(text)
                
        except sr.UnknownValueError:
            # Speech was unintelligible
            pass
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
        except Exception as e:
            print(f"Error recognizing speech: {e}")
    
    def speak(self, text: str):
        """
        Convert text to speech.
        
        Args:
            text: Text to speak
        """
        if not self.tts_engine:
            print("TTS engine not available")
            return
        
        try:
            # Speak the text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
    
    def speak_async(self, text: str):
        """
        Convert text to speech asynchronously.
        
        Args:
            text: Text to speak
        """
        if not self.tts_engine:
            return
        
        # Speak in a separate thread
        speak_thread = threading.Thread(target=self.speak, args=(text,))
        speak_thread.daemon = True
        speak_thread.start()
    
    def get_available_voices(self):
        """Get list of available TTS voices"""
        if not self.tts_engine:
            return []
        
        voices = self.tts_engine.getProperty('voices')
        return [voice.name for voice in voices] if voices else []
    
    def set_voice(self, voice_name: str):
        """
        Set the TTS voice.
        
        Args:
            voice_name: Name of the voice to use
        """
        if not self.tts_engine:
            return False
        
        voices = self.tts_engine.getProperty('voices')
        if voices:
            for voice in voices:
                if voice_name.lower() in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    return True
        return False
    
    def set_speech_rate(self, rate: int):
        """
        Set the speech rate.
        
        Args:
            rate: Words per minute (100-300)
        """
        if self.tts_engine:
            self.tts_engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """
        Set the volume level.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.tts_engine:
            self.tts_engine.setProperty('volume', volume)

# Example usage and testing
if __name__ == "__main__":
    processor = SpeechProcessor()
    
    def on_speech_recognized(text):
        print(f"Recognized: {text}")
        # Respond with TTS
        processor.speak_async(f"I heard you say: {text}")
    
    print("Starting speech recognition...")
    print("Say something to test speech recognition")
    print("Press Ctrl+C to stop")
    
    try:
        processor.start_listening(on_speech_recognized)
        
        # Keep the program running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping speech recognition...")
        processor.stop_listening()
