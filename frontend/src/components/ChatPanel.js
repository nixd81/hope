import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { FiSend, FiMic, FiMicOff } from 'react-icons/fi';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #2d2d2d;
`;

const ChatHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #404040;
  background: #1a1a1a;
`;

const ChatTitle = styled.h3`
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #ffffff;
`;

const ChatSubtitle = styled.p`
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #9aa0a6;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const Message = styled.div`
  display: flex;
  flex-direction: column;
  align-items: ${props => props.isUser ? 'flex-end' : 'flex-start'};
`;

const MessageBubble = styled.div`
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  background: ${props => props.isUser ? '#4285f4' : '#404040'};
  color: white;
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
`;

const MessageTime = styled.div`
  font-size: 11px;
  color: #9aa0a6;
  margin-top: 4px;
  padding: 0 8px;
`;

const EmotionTag = styled.span`
  font-size: 11px;
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 8px;
`;

const InputContainer = styled.div`
  padding: 16px;
  border-top: 1px solid #404040;
  background: #1a1a1a;
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 8px;
  align-items: center;
`;

const TextInput = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #404040;
  border-radius: 24px;
  background: #2d2d2d;
  color: white;
  font-size: 14px;
  outline: none;
  
  &:focus {
    border-color: #4285f4;
  }
  
  &::placeholder {
    color: #9aa0a6;
  }
`;

const SendButton = styled.button`
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: #4285f4;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
  
  &:hover {
    background: #3367d6;
  }
  
  &:disabled {
    background: #404040;
    cursor: not-allowed;
  }
`;

const VoiceButton = styled.button`
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: ${props => props.isListening ? '#ea4335' : '#404040'};
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
  
  &:hover {
    background: ${props => props.isListening ? '#d33b2c' : '#555'};
  }
`;

const ProcessingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(66, 133, 244, 0.1);
  border-radius: 18px;
  color: #4285f4;
  font-size: 12px;
  margin: 8px 0;
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

const ChatPanel = ({ messages, onSendMessage, isProcessing }) => {
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (inputText.trim() && !isProcessing) {
      onSendMessage(inputText.trim());
      setInputText('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleVoiceInput = () => {
    if (isListening) {
      // Stop listening
      setIsListening(false);
      // Note: In a real implementation, you'd stop the speech recognition here
    } else {
      // Start listening
      setIsListening(true);
      // Note: In a real implementation, you'd start speech recognition here
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <ChatContainer>
      <ChatHeader>
        <ChatTitle>AI Therapist</ChatTitle>
        <ChatSubtitle>Your empathetic companion</ChatSubtitle>
      </ChatHeader>
      
      <MessagesContainer>
        {messages.length === 0 && (
          <div style={{ 
            textAlign: 'center', 
            color: '#9aa0a6', 
            padding: '40px 20px',
            fontSize: '14px'
          }}>
            Start a conversation with your AI therapist. 
            <br />Share how you're feeling today.
          </div>
        )}
        
        {messages.map((message) => (
          <Message key={message.id} isUser={message.type === 'user'}>
            <MessageBubble isUser={message.type === 'user'}>
              {message.text}
              {message.emotion && message.type === 'user' && (
                <EmotionTag>{message.emotion}</EmotionTag>
              )}
            </MessageBubble>
            <MessageTime>{formatTime(message.timestamp)}</MessageTime>
          </Message>
        ))}
        
        {isProcessing && (
          <ProcessingIndicator>
            <Spinner />
            AI is thinking...
          </ProcessingIndicator>
        )}
        
        <div ref={messagesEndRef} />
      </MessagesContainer>
      
      <InputContainer>
        <InputWrapper>
          <TextInput
            ref={inputRef}
            type="text"
            placeholder="Type your message..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isProcessing}
          />
          
          <VoiceButton
            isListening={isListening}
            onClick={handleVoiceInput}
            title={isListening ? 'Stop listening' : 'Start voice input'}
          >
            {isListening ? <FiMicOff /> : <FiMic />}
          </VoiceButton>
          
          <SendButton
            onClick={handleSend}
            disabled={!inputText.trim() || isProcessing}
            title="Send message"
          >
            <FiSend />
          </SendButton>
        </InputWrapper>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatPanel;
