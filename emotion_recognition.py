import cv2
import numpy as np
from deepface import DeepFace

# Load OpenCV DNN face detector model files
prototxt_path = "deploy.prototxt"
model_path = "res10_300x300_ssd_iter_140000_fp16.caffemodel"

# Load the DNN face detector
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Initialize webcam
cap = cv2.VideoCapture(0)

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
                face_found = True
            except Exception as e:
                print("DeepFace error:", e)
                emotion = "Analysis error"
                face_found = True



            # Draw bounding box and emotion label on frame
            cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)

    if not face_found:
        cv2.putText(frame, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 2)

    cv2.imshow("Emotion Recognition", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
