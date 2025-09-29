import cv2


cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:

        face = frame[y:y+h, x:x+w]
        lab = cv2.cvtColor(face, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l_eq = clahe.apply(l)
        lab_eq = cv2.merge((l_eq, a, b))
        face_eq = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

        frame[y:y+h, x:x+w] = face_eq

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

  
    cv2.imshow('Video Call - CLAHE Enhanced Faces', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
