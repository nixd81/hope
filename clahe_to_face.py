import cv2

face = cv2.imread("khana.jpeg")

lab = cv2.cvtColor(face, cv2.COLOR_BGR2LAB)

l, a, b = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
l_eq = clahe.apply(l)

lab_eq = cv2.merge((l_eq, a, b))


face_eq = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)
s
cv2.imshow("Original Face", face)
cv2.imshow("CLAHE Enhanced Face", face_eq)
cv2.waitKey(0)
cv2.destroyAllWindows()

