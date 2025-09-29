import React, { forwardRef } from 'react';
import styled from 'styled-components';
import Webcam from 'react-webcam';

const VideoWrapper = styled.div`
  flex: 1;
  position: relative;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
`;

const VideoElement = styled(Webcam)`
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1); /* Mirror the video */
`;

const VideoPlaceholder = styled.div`
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: white;
`;

const PlaceholderIcon = styled.div`
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.7;
`;

const PlaceholderText = styled.div`
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 8px;
`;

const PlaceholderSubtext = styled.div`
  font-size: 14px;
  opacity: 0.8;
`;

const ProcessingOverlay = styled.div`
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.8);
  padding: 12px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
`;

const Spinner = styled.div`
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff40;
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const EmotionOverlay = styled.div`
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  padding: 12px 16px;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const EmotionIcon = styled.span`
  font-size: 18px;
`;

const getEmotionIcon = (emotion) => {
  const emotionIcons = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    fear: '😨',
    surprise: '😲',
    disgust: '🤢',
    neutral: '😐'
  };
  return emotionIcons[emotion] || '😐';
};

const VideoContainer = forwardRef(({ isVideoOn, currentEmotion, isProcessing }, ref) => {
  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  return (
    <VideoWrapper>
      {isVideoOn ? (
        <VideoElement
          ref={ref}
          audio={false}
          videoConstraints={videoConstraints}
          screenshotFormat="image/jpeg"
          mirrored={true}
        />
      ) : (
        <VideoPlaceholder>
          <PlaceholderIcon>📹</PlaceholderIcon>
          <PlaceholderText>Camera is off</PlaceholderText>
          <PlaceholderSubtext>Turn on your camera to start the session</PlaceholderSubtext>
        </VideoPlaceholder>
      )}
      
      {isProcessing && (
        <ProcessingOverlay>
          <Spinner />
          Analyzing emotions...
        </ProcessingOverlay>
      )}
      
      <EmotionOverlay>
        <EmotionIcon>{getEmotionIcon(currentEmotion)}</EmotionIcon>
        <span>{currentEmotion.charAt(0).toUpperCase() + currentEmotion.slice(1)}</span>
      </EmotionOverlay>
    </VideoWrapper>
  );
});

VideoContainer.displayName = 'VideoContainer';

export default VideoContainer;
