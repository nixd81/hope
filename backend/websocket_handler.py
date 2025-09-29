"""
WebSocket Handler for Real-time Communication
Handles real-time communication between frontend and backend.
"""

from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import time
from typing import Dict, Any

class WebSocketHandler:
    """
    Handles WebSocket connections for real-time communication.
    """
    
    def __init__(self, socketio: SocketIO):
        """
        Initialize WebSocket handler.
        
        Args:
            socketio: Flask-SocketIO instance
        """
        self.socketio = socketio
        self.active_sessions = {}
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            print(f"Client connected: {request.sid}")
            emit('connected', {'status': 'success'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            print(f"Client disconnected: {request.sid}")
            if request.sid in self.active_sessions:
                del self.active_sessions[request.sid]
        
        @self.socketio.on('join_session')
        def handle_join_session(data):
            """Handle client joining a therapy session"""
            session_id = data.get('session_id', 'default')
            join_room(session_id)
            self.active_sessions[request.sid] = {
                'session_id': session_id,
                'connected_at': time.time(),
                'emotions': {'face': 'neutral', 'text': 'neutral'}
            }
            emit('session_joined', {'session_id': session_id})
        
        @self.socketio.on('emotion_update')
        def handle_emotion_update(data):
            """Handle emotion updates from client"""
            if request.sid in self.active_sessions:
                self.active_sessions[request.sid]['emotions'].update(data)
                # Broadcast to all clients in the session
                session_id = self.active_sessions[request.sid]['session_id']
                emit('emotion_broadcast', data, room=session_id)
        
        @self.socketio.on('message_sent')
        def handle_message_sent(data):
            """Handle message sent by client"""
            if request.sid in self.active_sessions:
                session_id = self.active_sessions[request.sid]['session_id']
                emit('message_received', data, room=session_id)
        
        @self.socketio.on('ai_response')
        def handle_ai_response(data):
            """Handle AI response to broadcast"""
            if request.sid in self.active_sessions:
                session_id = self.active_sessions[request.sid]['session_id']
                emit('ai_message', data, room=session_id)
        
        @self.socketio.on('video_status')
        def handle_video_status(data):
            """Handle video on/off status"""
            if request.sid in self.active_sessions:
                self.active_sessions[request.sid]['video_on'] = data.get('video_on', False)
                session_id = self.active_sessions[request.sid]['session_id']
                emit('video_status_update', data, room=session_id)
        
        @self.socketio.on('mic_status')
        def handle_mic_status(data):
            """Handle microphone on/off status"""
            if request.sid in self.active_sessions:
                self.active_sessions[request.sid]['mic_on'] = data.get('mic_on', False)
                session_id = self.active_sessions[request.sid]['session_id']
                emit('mic_status_update', data, room=session_id)
    
    def broadcast_emotion_update(self, session_id: str, emotion_data: Dict[str, Any]):
        """
        Broadcast emotion update to all clients in a session.
        
        Args:
            session_id: Session ID to broadcast to
            emotion_data: Emotion data to broadcast
        """
        self.socketio.emit('emotion_update', emotion_data, room=session_id)
    
    def broadcast_ai_response(self, session_id: str, response_data: Dict[str, Any]):
        """
        Broadcast AI response to all clients in a session.
        
        Args:
            session_id: Session ID to broadcast to
            response_data: AI response data
        """
        self.socketio.emit('ai_response', response_data, room=session_id)
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """
        Get information about a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session information
        """
        active_clients = [
            sid for sid, info in self.active_sessions.items()
            if info['session_id'] == session_id
        ]
        
        return {
            'session_id': session_id,
            'active_clients': len(active_clients),
            'clients': active_clients
        }
    
    def get_all_sessions(self) -> Dict[str, Any]:
        """
        Get information about all active sessions.
        
        Returns:
            Dictionary of all sessions
        """
        sessions = {}
        for sid, info in self.active_sessions.items():
            session_id = info['session_id']
            if session_id not in sessions:
                sessions[session_id] = {
                    'session_id': session_id,
                    'clients': [],
                    'created_at': info['connected_at']
                }
            sessions[session_id]['clients'].append(sid)
        
        return sessions

# Import required modules
from flask import request
