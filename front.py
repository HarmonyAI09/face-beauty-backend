import dlib
import cv2

# Load the detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_81_face_landmarks.dat")

# Load an image using OpenCV
img = cv2.imread("front.jpg")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = detector(gray)

for face in faces:
    landmarks = predictor(gray, face)
    for n in range(0, 81):  # There are 68 landmark points
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(img, (x, y), 1, (255, 0, 0), -1)

# Display the image
cv2.imshow("Landmarks", img)
cv2.imwrite("land81_front.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
