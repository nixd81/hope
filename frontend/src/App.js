import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import Webcam from 'react-webcam';
import { useSpeechRecognition } from 'react-speech-kit';
import axios from 'axios';
import io from 'socket.io-client';

// Components
import VideoContainer from './components/VideoContainer';
import ChatPanel from './components/ChatPanel';
import ControlPanel from './components/ControlPanel';
import EmotionDisplay from './components/EmotionDisplay';
import LoadingSpinner from './components/LoadingSpinner';

// Styles
const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  background: #1a1a1a;
  color: white;
  font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, sans-serif;
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
`;

const SidePanel = styled.div`
  width: 350px;
  background: #2d2d2d;
  border-left: 1px solid #404040;
  display: flex;
  flex-direction: column;
`;

const Header = styled.div`
  padding: 20px;
  background: #1a1a1a;
  border-bottom: 1px solid #404040;
  text-align: center;
`;

const Title = styled.h1`
  margin: 0;
  font-size: 24px;
  font-weight: 500;
  color: #ffffff;
`;

const Subtitle = styled.p`
  margin: 8px 0 0 0;
  font-size: 14px;
  color: #9aa0a6;
`;

function App() {
  // State management
  const [isVideoOn, setIsVideoOn] = useState(true);
  const [isMicOn, setIsMicOn] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState('neutral');
  const [isProcessing, setIsProcessing] = useState(false);
  const [messages, setMessages] = useState([]);
  const [socket, setSocket] = useState(null);
  
  // Refs
  const webcamRef = useRef(null);
  const processingIntervalRef = useRef(null);
  
  // Speech recognition
  const { listen, listening, stop } = useSpeechRecognition({
    onResult: (result) => {
      handleSpeechInput(result);
    },
    onEnd: () => {
      setIsSpeaking(false);
    }
  });

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);
    
    newSocket.on('connect', () => {
      console.log('Connected to backend');
    });
    
    newSocket.on('emotion_update', (data) => {
      setCurrentEmotion(data.emotion);
    });
    
    return () => newSocket.close();
  }, []);

  // Start emotion processing when video is on
  useEffect(() => {
    if (isVideoOn && !processingIntervalRef.current) {
      startEmotionProcessing();
    } else if (!isVideoOn && processingIntervalRef.current) {
      stopEmotionProcessing();
    }
    
    return () => {
      if (processingIntervalRef.current) {
        clearInterval(processingIntervalRef.current);
      }
    };
  }, [isVideoOn]);

  const startEmotionProcessing = () => {
    processingIntervalRef.current = setInterval(() => {
      if (webcamRef.current && isVideoOn) {
        captureAndProcessFrame();
      }
    }, 2000); // Process every 2 seconds
  };

  const stopEmotionProcessing = () => {
    if (processingIntervalRef.current) {
      clearInterval(processingIntervalRef.current);
      processingIntervalRef.current = null;
    }
  };

  const captureAndProcessFrame = async () => {
    if (!webcamRef.current) return;
    
    try {
      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) return;
      
      setIsProcessing(true);
      
      const response = await axios.post('/api/process_frame', {
        frame: imageSrc
      });
      
      if (response.data.face_emotion) {
        setCurrentEmotion(response.data.face_emotion);
        
        // Send emotion update via socket
        if (socket) {
          socket.emit('emotion_update', {
            emotion: response.data.face_emotion,
            confidence: response.data.confidence
          });
        }
      }
    } catch (error) {
      console.error('Error processing frame:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTextInput = async (text) => {
    if (!text.trim()) return;
    
    try {
      setIsProcessing(true);
      
      const response = await axios.post('/api/process_text', {
        text: text
      });
      
      // Add user message
      const userMessage = {
        id: Date.now(),
        type: 'user',
        text: text,
        emotion: response.data.text_emotion,
        timestamp: new Date()
      };
      
      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        text: response.data.ai_response,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, userMessage, aiMessage]);
      
    } catch (error) {
      console.error('Error processing text:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSpeechInput = async (text) => {
    if (!text.trim()) return;
    
    // Add visual feedback for speech input
    setIsSpeaking(true);
    
    // Process the speech input as text
    await handleTextInput(text);
  };

  const toggleVideo = () => {
    setIsVideoOn(!isVideoOn);
  };

  const toggleMic = () => {
    setIsMicOn(!isMicOn);
    if (isMicOn) {
      stop();
    } else {
      listen();
    }
  };

  const startListening = () => {
    if (!isMicOn) return;
    listen();
    setIsSpeaking(true);
  };

  const stopListening = () => {
    stop();
    setIsSpeaking(false);
  };

  return (
    <AppContainer>
      <MainContent>
        <Header>
          <Title>Virtual Therapist</Title>
          <Subtitle>Your AI companion for emotional support</Subtitle>
        </Header>
        
        <VideoContainer
          ref={webcamRef}
          isVideoOn={isVideoOn}
          currentEmotion={currentEmotion}
          isProcessing={isProcessing}
        />
        
        <ControlPanel
          isVideoOn={isVideoOn}
          isMicOn={isMicOn}
          isSpeaking={isSpeaking}
          isListening={listening}
          onToggleVideo={toggleVideo}
          onToggleMic={toggleMic}
          onStartListening={startListening}
          onStopListening={stopListening}
        />
        
        <EmotionDisplay
          emotion={currentEmotion}
          isProcessing={isProcessing}
        />
      </MainContent>
      
      <SidePanel>
        <ChatPanel
          messages={messages}
          onSendMessage={handleTextInput}
          isProcessing={isProcessing}
        />
      </SidePanel>
    </AppContainer>
  );
}

export default App;
