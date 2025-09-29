import React from 'react';
import styled, { keyframes } from 'styled-components';

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const EmotionContainer = styled.div`
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.8);
  padding: 16px 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: ${fadeIn} 0.3s ease-out;
`;

const EmotionHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
`;

const EmotionIcon = styled.div`
  font-size: 24px;
  animation: ${props => props.isProcessing ? pulse : 'none'};
  animation-duration: 1s;
  animation-iteration-count: infinite;
`;

const EmotionLabel = styled.div`
  font-size: 16px;
  font-weight: 600;
  color: white;
  text-transform: capitalize;
`;

const EmotionDescription = styled.div`
  font-size: 12px;
  color: #9aa0a6;
  margin-top: 4px;
`;

const ProcessingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #4285f4;
  margin-top: 8px;
`;

const Spinner = styled.div`
  width: 12px;
  height: 12px;
  border: 2px solid #4285f440;
  border-top: 2px solid #4285f4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const getEmotionData = (emotion) => {
  const emotionData = {
    happy: {
      icon: '😊',
      description: 'You seem to be in a positive mood',
      color: '#34a853'
    },
    sad: {
      icon: '😢',
      description: 'I can sense you might be feeling down',
      color: '#4285f4'
    },
    angry: {
      icon: '😠',
      description: 'I notice you might be feeling frustrated',
      color: '#ea4335'
    },
    fear: {
      icon: '😨',
      description: 'You seem to be feeling anxious or worried',
      color: '#ff9800'
    },
    surprise: {
      icon: '😲',
      description: 'You appear to be surprised by something',
      color: '#9c27b0'
    },
    disgust: {
      icon: '🤢',
      description: 'I sense you might be feeling repulsed',
      color: '#795548'
    },
    neutral: {
      icon: '😐',
      description: 'Your expression appears calm and neutral',
      color: '#5f6368'
    }
  };
  
  return emotionData[emotion] || emotionData.neutral;
};

const EmotionDisplay = ({ emotion, isProcessing }) => {
  const emotionData = getEmotionData(emotion);
  
  return (
    <EmotionContainer>
      <EmotionHeader>
        <EmotionIcon isProcessing={isProcessing}>
          {emotionData.icon}
        </EmotionIcon>
        <EmotionLabel>{emotion}</EmotionLabel>
      </EmotionHeader>
      
      <EmotionDescription>
        {emotionData.description}
      </EmotionDescription>
      
      {isProcessing && (
        <ProcessingIndicator>
          <Spinner />
          Analyzing your emotions...
        </ProcessingIndicator>
      )}
    </EmotionContainer>
  );
};

export default EmotionDisplay;
