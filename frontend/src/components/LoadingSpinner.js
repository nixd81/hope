import React from 'react';
import styled, { keyframes } from 'styled-components';

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const SpinnerContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
`;

const Spinner = styled.div`
  width: ${props => props.size || 24}px;
  height: ${props => props.size || 24}px;
  border: 3px solid rgba(66, 133, 244, 0.3);
  border-top: 3px solid #4285f4;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
`;

const LoadingText = styled.div`
  margin-left: 12px;
  color: #9aa0a6;
  font-size: 14px;
`;

const LoadingSpinner = ({ size, text, ...props }) => {
  return (
    <SpinnerContainer {...props}>
      <Spinner size={size} />
      {text && <LoadingText>{text}</LoadingText>}
    </SpinnerContainer>
  );
};

export default LoadingSpinner;
