#!/usr/bin/env python3
"""
Virtual Therapist Backend Startup Script
Automatically sets up and runs the backend server.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'flask_cors', 'opencv-python', 'numpy', 
        'deepface', 'transformers', 'torch', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_api_key():
    """Check if Gemini API key is set"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("Please set your Gemini API key:")
        print("export GEMINI_API_KEY=your_api_key_here")
        return False
    
    print("✅ Gemini API key is set")
    return True

def download_models():
    """Download required model files if they don't exist"""
    backend_dir = Path(__file__).parent / 'backend'
    prototxt_path = backend_dir / 'deploy.prototxt'
    model_path = backend_dir / 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
    
    if not prototxt_path.exists() or not model_path.exists():
        print("📥 Downloading required model files...")
        try:
            # Download prototxt file
            if not prototxt_path.exists():
                import urllib.request
                urllib.request.urlretrieve(
                    'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/opencv_face_detector.pbtxt',
                    prototxt_path
                )
                print("✅ Downloaded prototxt file")
            
            # Download model file
            if not model_path.exists():
                import urllib.request
                urllib.request.urlretrieve(
                    'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/opencv_face_detector.caffemodel',
                    model_path
                )
                print("✅ Downloaded model file")
                
        except Exception as e:
            print(f"⚠️  Could not download model files: {e}")
            print("The application will attempt to download them at runtime")
    
    return True

def start_backend():
    """Start the backend server"""
    backend_dir = Path(__file__).parent / 'backend'
    os.chdir(backend_dir)
    
    print("🚀 Starting Virtual Therapist Backend...")
    print("📍 Backend will be available at: http://localhost:5000")
    print("📍 Frontend should be running at: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the Flask application
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🤖 Virtual Therapist Backend Startup")
    print("=" * 40)
    
    # Check requirements
    if not check_python_version():
        return False
    
    if not check_dependencies():
        return False
    
    if not check_api_key():
        return False
    
    # Download models if needed
    download_models()
    
    # Start the backend
    return start_backend()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Startup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Backend stopped successfully")
