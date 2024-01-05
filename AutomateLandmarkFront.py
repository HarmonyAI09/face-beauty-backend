import os
from datetime import datetime
import hashlib
from fastapi import UploadFile
from PIL import Image
import numpy as np
import cv2
import dlib
import mediapipe as mp

UPLOAD_DIR = "UPLOADS"
DEFAULT_LENGTH = 800
DELTA = 0.005

def getVectorParameters(x1, y1, x2, y2):
    A = (y1 - y2) / (x1 - x2)
    B = y1 - x1 * A
    return A, B
def getCrossPoint(x1, y1, x2, y2, x3, y3, x4, y4):
    A1, B1 = getVectorParameters(x1, y1, x2, y2)
    A2, B2 = getVectorParameters(x3, y3, x4, y4)
    X = (B2 - B1) / (A1 - A2)
    Y = A1 * X + B1
    return X, Y

def storeImage(image:UploadFile):
    # Create a folder if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded image to the folder
    currentTime = datetime.now()
    imageID = hashlib.md5(str(currentTime).encode()).hexdigest()
    imageFileName = imageID + ".jpg"
    imageStorePath = os.path.join(UPLOAD_DIR, imageFileName)
    imageSrc = Image.open(image.file)
    imageSrc = imageSrc.convert('RGB')
    if imageSrc.width > imageSrc.height:
        width = DEFAULT_LENGTH
        height = int(imageSrc.height*DEFAULT_LENGTH/imageSrc.width)
    else:
        height = DEFAULT_LENGTH
        width = int(imageSrc.width*DEFAULT_LENGTH/imageSrc.height)
    imageResize = imageSrc.resize((width, height))
    imageResize.save(imageStorePath, format="JPEG")
    return imageStorePath

def getLandmarksUsing68(imgPath, IndexList, Landmarks):
    imgGray = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    p = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)
    faces = detector(imgGray, 0)
    for i, face in enumerate(faces):
        shape = predictor(imgGray, face)
        shape = np.array([[l.x, l.y] for l in shape.parts()])
        Landmarks[12, 0, 0] = (shape[38][0] + shape[41][0]) / 2
        Landmarks[12, 0, 1] = (shape[38][1] + shape[41][1]) / 2
        Landmarks[12, 1, 0] = (shape[44][0] + shape[47][0]) / 2
        Landmarks[12, 1, 1] = (shape[44][1] + shape[47][1]) / 2
    return Landmarks
def getLandmarksUsing81(imgPath, IndexList, Landmarks):
    imgGray = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    p = "shape_predictor_81_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)
    faces = detector(imgGray, 0)
    for i, face in enumerate(faces):
        shape = predictor(imgGray, face)
        shape = np.array([[l.x, l.y] for l in shape.parts()])
        for index in range(len(IndexList)):
            Landmarks[IndexList[index][1], IndexList[index][2], 0] = shape[IndexList[index][0]-1][0]
            Landmarks[IndexList[index][1], IndexList[index][2], 1] = shape[IndexList[index][0]-1][1]
    return Landmarks
def getLandmarksUsingMP(imgPath, IndexList, Landmarks):
    imgBGR = cv2.imread(imgPath)
    imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
    height, width, _ = imgRGB.shape
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.9) as face_mesh:
        faces = face_mesh.process(imgRGB)
        for face in faces.multi_face_landmarks:
            for index in range(len(IndexList)):
                Landmarks[IndexList[index][1], IndexList[index][2], 0] = int(face.landmark[IndexList[index][0]].x*width)
                Landmarks[IndexList[index][1], IndexList[index][2], 1] = int(face.landmark[IndexList[index][0]].y*height)
            Landmarks[3, 0, 0] = int(face.landmark[105].x*width)
            Landmarks[3, 0, 1] = int((face.landmark[105].y - DELTA)*height)
            Landmarks[4, 0, 0] = int(face.landmark[105].x*width)
            Landmarks[4, 0, 1] = int((face.landmark[105].y + DELTA)*height)
            Landmarks[3, 1, 0] = int(face.landmark[334].x*width)
            Landmarks[3, 1, 1] = int((face.landmark[334].y - DELTA)*height)
            Landmarks[4, 1, 0] = int(face.landmark[334].x*width)
            Landmarks[4, 1, 1] = int((face.landmark[334].y + DELTA)*height)
            Landmarks[7, 0, 0] = int(face.landmark[55].x*width)
            Landmarks[7, 0, 1] = int((face.landmark[55].y - DELTA)*height)
            Landmarks[8, 0, 0] = int(face.landmark[55].x*width)
            Landmarks[8, 0, 1] = int((face.landmark[55].y + DELTA)*height)
            Landmarks[7, 1, 0] = int(face.landmark[285].x*width)
            Landmarks[7, 1, 1] = int((face.landmark[285].y - DELTA)*height)
            Landmarks[8, 1, 0] = int(face.landmark[285].x*width)
            Landmarks[8, 1, 1] = int((face.landmark[285].y + DELTA)*height)

            Landmarks[27, 0, 0], Landmarks[27, 0, 1] = getCrossPoint(
                face.landmark[207].x*width,face.landmark[207].y*height,
                face.landmark[135].x*width,face.landmark[135].y*height,
                face.landmark[152].x*width,face.landmark[152].y*height,
                face.landmark[149].x*width,face.landmark[149].y*height)
            Landmarks[27, 1, 0], Landmarks[27, 1, 1] = getCrossPoint(
                face.landmark[433].x*width,face.landmark[433].y*height,
                face.landmark[397].x*width,face.landmark[397].y*height,
                face.landmark[152].x*width,face.landmark[152].y*height,
                face.landmark[378].x*width,face.landmark[378].y*height)
    return Landmarks

def getProfileLandmarks(imgPath):
    profileLandmarks = np.zeros((30, 2, 2))
    IndexListUsing68 = []
    IndexListUsing81 = [
        [72, 1, 0],
        [72, 1, 1],
        [37, 11, 0],
        [46, 11, 1],
    ]
    IndexListUsingMP = [
        [103, 2, 0],
        [332, 2, 1],
        [9, 5, 0],
        [9, 5, 1],
        [8, 6, 0],
        [8, 6, 1],
        [112, 16, 0],
        [341, 16, 1],
        [219, 18, 0],
        [455, 18, 1],
        [145, 14, 0],
        [374, 14, 1],
        [154, 15, 0],
        [381, 15, 1],
        [159, 10, 0],
        [386, 10, 1],
        [247, 9, 0],
        [467, 9, 1],
        [157, 13, 0],
        [384, 13, 1],
        [2, 19, 0],
        [2, 19, 1],
        [326, 20, 0],
        [326, 20, 1],
        [267, 21, 0],
        [267, 21, 1],
        [152, 29, 0],
        [152, 29, 1],
        [148, 28, 0],
        [377, 28, 1],
        [172, 26, 0],
        [397, 26, 1],
        [58, 22, 0],
        [288, 22, 1],
        [17, 25, 0],
        [17, 25, 1],
        [14, 24, 0],
        [14, 24, 1],
        [61, 23, 0],
        [291, 23, 1],
        [227, 17, 0],
        [454, 17, 1],
    ]

    profileLandmarks = getLandmarksUsing68(imgPath, IndexListUsing68, profileLandmarks)
    profileLandmarks = getLandmarksUsing81(imgPath, IndexListUsing81, profileLandmarks)
    profileLandmarks = getLandmarksUsingMP(imgPath, IndexListUsingMP, profileLandmarks)
    return profileLandmarks.tolist()

def mainProcess(image:UploadFile):
    return {"points":getProfileLandmarks(storeImage(image))}