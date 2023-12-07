import os
import datetime
import hashlib
from fastapi import UploadFile
from PIL import Image
import numpy as np
import cv2
import dlib
import mediapipe as mp

UPLOAD_DIR = "UPLOADS"
DEFAULT_LENGTH = 800

def storeImage(image:UploadFile):
    # Create a folder if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded image to the folder
    currentTime = datetime.now()
    imageID = hashlib.md5(str(currentTime).encode()).hexdigest()
    imageFileName = imageID + ".jpg"
    imageStorePath = os.path.join(UPLOAD_DIR, imageFileName)
    imageSrc = Image.open(image.file)
    if imageSrc.width > imageSrc.height:
        width = DEFAULT_LENGTH
        height = int(imageSrc.height*DEFAULT_LENGTH/imageSrc.width)
    else:
        height = DEFAULT_LENGTH
        width = int(imageSrc.width*DEFAULT_LENGTH/imageSrc.height)
    imageResize = imageSrc.resize((width, height))
    imageResize.save(imageStorePath)
    return imageStorePath

def getLandmarksUsing81(imgPath):
    imgGray = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    p = "shape_predictor_81_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)
    


def getProfileLandmarks(imgPath):
    profileLandmarks = np.zeros((30, 2, 2))
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

    img = cv2.imread(imgPath)
    img_Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

