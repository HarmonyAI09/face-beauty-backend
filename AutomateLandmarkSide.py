import os
from datetime import datetime
import hashlib
from fastapi import UploadFile
from PIL import Image
import numpy as np
import cv2
import requests
from util import open_image
from face_alignment.api import FaceAlignment, LandmarksType
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = "UPLOADS"
SAMPLE_POINTS_FILE = "REFERENCE/f15.pts"
DEFAULT_LENGTH = 800
SAMPLE_RATIO = 1.0
ZERO = 0.001
INFINITE = 801

def storeImage(image:UploadFile):
    # Create a folder if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded image to the folder
    currentTime = datetime.now()
    imageID = hashlib.md5(str(currentTime).encode()).hexdigest()
    imageFileName = imageID + ".jpg"
    imageStorePath = os.path.join(UPLOAD_DIR, imageFileName)
    imageSrc = Image.open(image.file)
    imageSrc = imageSrc.convert("RGB")
    if imageSrc.width > imageSrc.height:
        width = DEFAULT_LENGTH
        height = int(imageSrc.height*DEFAULT_LENGTH/imageSrc.width)
    else:
        height = DEFAULT_LENGTH
        width = int(imageSrc.width*DEFAULT_LENGTH/imageSrc.height)
    imageResize = imageSrc.resize((width, height))
    imageResize.save(imageStorePath)
    response = requests.post(os.getenv("BG_REMOVE_API"), 
            files={'image_file':open(imageStorePath, 'rb')},
            data={'size':'auto', 'format':'jpg'},
            headers={'X-Api-key':os.getenv("BG_REMOVE_KEY")})    
    if response.status_code == requests.codes.ok:
        with open(imageStorePath, 'wb') as out :
            out.write(response.content)
    else: 
        print("Error:", response.status_code, response.text)
        return    
    imageSrc = Image.open(imageStorePath)
    if imageSrc.width > imageSrc.height:
        width = DEFAULT_LENGTH
        height = int(imageSrc.height*DEFAULT_LENGTH/imageSrc.width)
    else:
        height = DEFAULT_LENGTH
        width = int(imageSrc.width*DEFAULT_LENGTH/imageSrc.height)
    imageResize = imageSrc.resize((width, height))
    imageResize.save(imageStorePath)
    return imageStorePath

def getLandmarkUsingLib(imgPath, Landmarks):
    imgSrc = open_image(imgPath)
    face = FaceAlignment(LandmarksType._2D, enable_cuda=False, flip_input=False, use_cnn_face_detector=True)
    landmarks = face.get_landmarks(np.array(imgSrc))[-1]
    indexListLib = [0,1,4,5,7,8,12,15,20,28,29,30,33,36,44,50,54,57]
    indexListRes = [57, 42, 48, 50, 51, 52, 49, 38, 32, 36, 39, 41, 43, 57, 33, 45, 46, 58]

    for i, indexLib  in enumerate(indexListLib):
        Landmarks[indexListRes[i]-30] = landmarks[indexLib]
    
    return Landmarks
def getLandmarkForNeckNose(imgPath, Landmarks):
    imgSrc = cv2.imread(imgPath, 0)
    height, width = imgSrc.shape
    print(height, width)
    Landmarks[10] = [INFINITE, INFINITE]
    for i in range(height//4, height):
        for j in range(width):
            if imgSrc[i][j]!=255:
                if Landmarks[25][0] < j:
                    Landmarks[25][0] = j
                    Landmarks[25][1] = i
                if Landmarks[10][0] > j and i < height//4*3:
                    Landmarks[10][0] = j
                    Landmarks[10][1] = i
                break
    print(Landmarks[10], Landmarks[25], "*************")
    return Landmarks
def getLandmarkGenerate(imgPath, Landmarks):
    with open(SAMPLE_POINTS_FILE, 'r') as file:
        ptsDt = file.read()
    
    samplePts = []
    for i, ptData in enumerate(ptsDt[ptsDt.index('{')+1:ptsDt.index('}')].split('\n')):
        if ptData.strip() != '':
            x, y = map(float, ptData.strip().split())
            samplePts.append([x, y, i-1])

    ##### SET Y-value of Point0 #####
    SAMPLE_RATIO = (samplePts[25][1]-samplePts[0][1])/(samplePts[25][1]-samplePts[2][1])
    Landmarks[0] = [0, Landmarks[25][1] - (Landmarks[25][1]-Landmarks[2][1]) * SAMPLE_RATIO]

    ##### SET Y-values #####
    sortedPts = sorted(samplePts, key=lambda p: p[1])
    refStepIdxList = []
    refNullIdxList = []
    for point in sortedPts:
        if np.array_equal(Landmarks[point[2]], [0.0, 0.0]):
            refNullIdxList[-1].append(point[2])
        else:
            refStepIdxList.append(point[2])
            refNullIdxList.append([])

    for i in range(len(refStepIdxList)-1):
        head = refStepIdxList[i]
        tail = refStepIdxList[i+1]
        srcHeight = samplePts[tail][1] - samplePts[head][1]
        tgtHeight = Landmarks[tail][1] - Landmarks[head][1]
        stepRatio = srcHeight / tgtHeight
        for nullIdx in refNullIdxList[i]:
            resHeight = (samplePts[nullIdx][1] - samplePts[head][1]) / stepRatio
            Landmarks[nullIdx] = [0, Landmarks[head][1] + resHeight]

    ##### SET X-values #####
    sortedPts = sorted(samplePts, key=lambda p: p[0])
    refStepIdxList = []
    refNullIdxList = []
    for point in sortedPts:
        if Landmarks[point[2]][0] == 0:
            refNullIdxList[-1].append(point[2])
        else:
            refStepIdxList.append(point[2])
            refNullIdxList.append([])
    
    for i in range(len(refStepIdxList)-1):
        head = refStepIdxList[i]
        tail = refStepIdxList[i+1]
        srcWidth = samplePts[tail][0] - samplePts[head][0]
        tgtWidth = Landmarks[tail][0] - Landmarks[head][0] + ZERO
        stepRatio = srcWidth / tgtWidth
        for nullIdx in refNullIdxList[i]:
            resWidth = (samplePts[nullIdx][0] - samplePts[head][0]) / stepRatio
            Landmarks[nullIdx][0] = Landmarks[head][0] + resWidth
    
    print(Landmarks)
    return Landmarks

def getProfileLandmarks(imgPath):
    profileLandmarks = np.zeros((30, 2))

    profileLandmarks = getLandmarkUsingLib(imgPath, profileLandmarks)
    profileLandmarks = getLandmarkForNeckNose(imgPath, profileLandmarks)
    profileLandmarks = getLandmarkGenerate(imgPath, profileLandmarks)
    
    return profileLandmarks.tolist()

def mainProcess(image:UploadFile):
    return {"points":getProfileLandmarks(storeImage(image))}