import React from 'react';
import styled from 'styled-components';
import { 
  FiVideo, 
  FiVideoOff, 
  FiMic, 
  FiMicOff, 
  FiMic,
  FiSquare,
  FiPhone,
  FiPhoneOff
} from 'react-icons/fi';

const ControlContainer = styled.div`
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  background: rgba(0, 0, 0, 0.8);
  padding: 12px 20px;
  border-radius: 24px;
  backdrop-filter: blur(10px);
`;

const ControlButton = styled.button`
  width: 48px;
  height: 48px;
  border: none;
  border-radius: 50%;
  background: ${props => {
    if (props.isActive) return '#ea4335';
    if (props.isSecondary) return '#5f6368';
    return '#3c4043';
  }};
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 20px;
  
  &:hover {
    background: ${props => {
      if (props.isActive) return '#d33b2c';
      if (props.isSecondary) return '#6f7378';
      return '#4a4d52';
    }};
    transform: scale(1.05);
  }
  
  &:active {
    transform: scale(0.95);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const MicButton = styled(ControlButton)`
  background: ${props => {
    if (props.isListening) return '#34a853';
    if (props.isActive) return '#ea4335';
    return '#3c4043';
  }};
  
  &:hover {
    background: ${props => {
      if (props.isListening) return '#2d8f47';
      if (props.isActive) return '#d33b2c';
      return '#4a4d52';
    }};
  }
`;

const EndCallButton = styled(ControlButton)`
  background: #ea4335;
  width: 56px;
  height: 56px;
  font-size: 24px;
  
  &:hover {
    background: #d33b2c;
  }
`;

const StatusIndicator = styled.div`
  position: absolute;
  top: -8px;
  right: -8px;
  width: 16px;
  height: 16px;
  background: ${props => {
    if (props.isListening) return '#34a853';
    if (props.isActive) return '#ea4335';
    return '#5f6368';
  }};
  border: 2px solid #000;
  border-radius: 50%;
  animation: ${props => props.isListening ? 'pulse 1.5s infinite' : 'none'};
  
  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
  }
`;

const Tooltip = styled.div`
  position: absolute;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  
  ${ControlButton}:hover & {
    opacity: 1;
  }
`;

const ControlPanel = ({
  isVideoOn,
  isMicOn,
  isSpeaking,
  isListening,
  onToggleVideo,
  onToggleMic,
  onStartListening,
  onStopListening
}) => {
  const handleMicClick = () => {
    if (isListening) {
      onStopListening();
    } else if (isMicOn) {
      onStartListening();
    } else {
      onToggleMic();
    }
  };

  const handleEndCall = () => {
    // In a real application, this would end the session
    if (window.confirm('Are you sure you want to end this therapy session?')) {
      window.location.reload();
    }
  };

  return (
    <ControlContainer>
      <ControlButton
        isActive={!isVideoOn}
        onClick={onToggleVideo}
        title={isVideoOn ? 'Turn off camera' : 'Turn on camera'}
      >
        {isVideoOn ? <FiVideo /> : <FiVideoOff />}
      </ControlButton>
      
      <MicButton
        isActive={!isMicOn}
        isListening={isListening}
        onClick={handleMicClick}
        title={
          isListening ? 'Stop listening' : 
          isMicOn ? 'Start voice input' : 
          'Turn on microphone'
        }
      >
        {isMicOn ? <FiMic /> : <FiMicOff />}
        {isListening && <StatusIndicator isListening />}
      </MicButton>
      
      <EndCallButton
        onClick={handleEndCall}
        title="End session"
      >
        <FiPhoneOff />
      </EndCallButton>
    </ControlContainer>
  );
};

export default ControlPanel;
