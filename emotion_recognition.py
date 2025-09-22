import cv2
import numpy as np
from deepface import DeepFace
import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from gemini_integration import get_gemini_response


# Load OpenCV DNN face detector model files
prototxt_path = "deploy.prototxt"
model_path = "res10_300x300_ssd_iter_140000_fp16.caffemodel"

# Load the DNN face detector
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize speech recognizer and microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()

def get_speech_text():
    print("Speak now...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except Exception as e:
        print("Speech recognition error:", e)
        return ""

# Load EmoRoBERTa model/tokenizer for text emotion detection
tokenizer = AutoTokenizer.from_pretrained("arpanghoshal/EmoRoBERTa")
model = AutoModelForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion_labels = [
    'admiration','amusement','anger','annoyance','approval','caring',
    'confusion','curiosity','desire','disappointment','disapproval','disgust',
    'embarrassment','excitement','fear','gratitude','grief','joy','love',
    'nervousness','optimism','pride','realization','relief','remorse',
    'sadness','surprise','neutral'
]

def get_text_emotion(text):
    inputs = tokenizer(text, return_tensors="pt")
    logits = model(**inputs).logits
    emotion_id = int(torch.argmax(logits))
    return emotion_labels[emotion_id]

latest_face_emotion = "No face detected"
spoken_text = ""
latest_text_emotion = ""

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    h, w = frame.shape[:2]

    # Prepare input blob for the detector
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    face_found = False
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x2, y2) = box.astype("int")

            # Boundary check
            x = max(0, x)
            y = max(0, y)
            x2 = min(w, x2)
            y2 = min(h, y2)

            face = frame[y:y2, x:x2]

            try:
                face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                if face.shape[0] < 50 or face.shape[1] < 50:
                    continue

                result = DeepFace.analyze(face_rgb, actions=['emotion'], enforce_detection=False)
                if isinstance(result, list):
                    emotion = result[0]['dominant_emotion']
                else:
                    emotion = result['dominant_emotion']
                latest_face_emotion = emotion  # Store latest emotion
                face_found = True
            except Exception as e:
                print("DeepFace error:", e)
                latest_face_emotion = "Analysis error"
                face_found = True

            # Draw bounding box and face emotion label on frame
            cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, latest_face_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)

    if not face_found:
        latest_face_emotion = "No face detected"
        cv2.putText(frame, latest_face_emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

    # Display recognized speech text and text emotion on the frame
    if spoken_text:
        cv2.putText(frame, f"Speech: {spoken_text}", (10, h - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    if latest_text_emotion:
        cv2.putText(frame, f"Text Emotion: {latest_text_emotion}", (10, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Emotion Recognition", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    # Press 'r' to start speech recognition
    if key == ord('r'):
        spoken_text = get_speech_text()
        if spoken_text:
            latest_text_emotion = get_text_emotion(spoken_text)
            response = get_gemini_response(latest_face_emotion, latest_text_emotion, spoken_text)
            print("Gemini response:", response)

cap.release()
cv2.destroyAllWindows()
