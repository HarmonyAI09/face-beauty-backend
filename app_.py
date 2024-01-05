import uvicorn
import datetime
import hashlib

from fastapi import FastAPI, UploadFile, Request, HTTPException, File
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from schemas import GetFrontMarkRequestSchema
from schemas import GetSideMarkRequestSchema
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
import Auth
import pricing
import os
from PIL import Image
import stripe
import json
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, timedelta

import face_landmarks
import side_landmarks
import CreateReportImages
from fastapi import Form

import json
import io
from pathlib import Path
import zipfile

stripe.api_key = 'sk_test_51OAYN0ItQ91j83DilxeRLixL8nBtOwbGiJ5KSlB65qG576Eans0deS8osZ5vknUd2rej0R3FfcIOjvXiKpwBFgre003XBuMXBQ'
mongo_uri = "mongodb+srv://devguru13580:hXcQgMDBinZ8wlo4@cluster0.ehilact.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["harmony"]
users_collection = db["users"]

class PurchasePlan(BaseModel):
    email: str

def calculate_expiration_date():    
    return datetime.now() + timedelta(days=30)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

SIDE_PROFILE_TOTAL_SCORE_MAX = 194.5
FRONT_PROFILE_TOTAL_SCORE_MAX = 305.5

app.include_router(Auth.router, prefix="/api")
app.include_router(pricing.router, prefix="/pricing")

def side_input(
    gender: int,
    racial: str,
    gonialAngle: float,
    nasofrontalAngle: float,
    mandibularPlaneAngle: float,
    ramus2MandibleRatio: float,
    facialConvexityGlabella: float,
    submentalCervicalAngle: float,
    nasofacialAngle: float,
    nasolabialAngle: float,
    orbitalVector: str,
    totalFacialConvexity: float,
    mentolabialAngle: float,
    facialConvexityNasion: float,
    nasalProjection: float,
    nasalW2HRatio: float,
    rickettsELine: str,
    holdawayHLine: str,
    steinerSLine: str,
    burstoneLine: str,
    nasomentalAngle: float,
    gonion2MouthRelationship: str,
    recessionRelative2FrankfortPlane: str,
    browridgeInclinationAngle: float,
    nasalTipAngle: float,
):
    sum = 0.0

    scores = []
    notes = []
    max_scores = []
    ranges = []
    current_values = []
    measurement_names = []
    advices = []

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = gonial_angle_score(gonialAngle, gender, racial)
    print("Gonial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = nasofrontal_angle_score(nasofrontalAngle, gender, racial)
    print("Nasofrontal angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    advices.append(advice)
    sum = sum + temp_sum

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = mandibular_plane_angle_score(mandibularPlaneAngle, gender, racial)
    print("Mandibular plane angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = ramus_mandible_ratio_score(ramus2MandibleRatio, gender, racial)
    print("Ramus mandible ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = facial_convexity_glabella_score(facialConvexityGlabella, gender, racial)
    print("Facial convexity glabella score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = submental_cervical_angle_score(submentalCervicalAngle, gender, racial)
    print("Submental cervical angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = nasofacial_angle_score(nasofacialAngle, gender, racial)
    print("Nasofacial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = nasolabial_angle_score(nasolabialAngle, gender, racial)
    print("Nasolabial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = orbital_vector_score(orbitalVector, gender, racial)
    print("Orbital vector score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = total_facial_convexity_score(totalFacialConvexity, gender, racial)
    print("Total facial convexity score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = mentolabial_angle_score(mentolabialAngle, gender, racial)
    print("Mentolabial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = facial_convexity_nasion_score(facialConvexityNasion, gender, racial)
    print("Facial convexity nasion score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = nasal_projection_score(nasalProjection, gender, racial)
    print("Nasal Projection score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = nasal_wh_ratio_score(nasalW2HRatio, gender, racial)
    print("Nasal W to H ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = ricketts_E_line_score(rickettsELine, gender, racial)
    print("Ricketts E line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = holdaway_H_line_score(holdawayHLine, gender, racial)
    print("Holdaway H line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = steiner_S_line_score(steinerSLine, gender, racial)
    print("Steiner S line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = burstone_line_score(burstoneLine, gender, racial)
    print("Burstone line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = nasomental_angle_score(nasomentalAngle, gender, racial)
    print("Nasomental angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = gonion_mouth_relationship_score(gonion2MouthRelationship, gender, racial)
    print("Gonion, mouth relationship score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = recession_relative_frankfort_plane_score(
        recessionRelative2FrankfortPlane, gender, racial
    )
    print("Recession relative frankfort plane score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = browridge_inclination_angle_score(browridgeInclinationAngle, gender, racial)
    print("Browridge inclination angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = nasal_tip_angle_score(nasalTipAngle, gender, racial)
    print("Nasal tip angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    print("Total Side Profile score is ", sum)
    print(
        "Total side profile percentage is ",
        sum / SIDE_PROFILE_TOTAL_SCORE_MAX * 100,
        "%",
    )
    return (
        sum,
        sum / SIDE_PROFILE_TOTAL_SCORE_MAX * 100,
        scores,
        notes,
        max_scores,
        ranges,
        current_values,
        measurement_names,
        advices,
    )


def front_input(
    gender: int,
    racial: str,
    eyeSeparationRatio: float,
    facialThirds: list,
    lateralCanthalTilt: float,
    facialWHRatio: float,
    jawFrontalAngle: float,
    cheekBoneHeight: float,
    totalFacialWHRatio: float,
    bigonialWidth: float,
    chin2PhiltrumRatio: float,
    neckWidth: float,
    mouthWidth2NoseWidthRatio: float,
    midFaceRatio: float,
    eyebrowPositionRatio: float,
    eyeSpacingRatio: float,
    eyeAspectRatio: float,
    lowerLip2UpperLipRatio: float,
    ipsilateralAlarAngle: float,
    deviationOfJFA2IAA: float,
    eyebrowTilt: float,
    bitemporalWidth: float,
    lowerThirdProporation: float,
    medialCanthalAngle: float,
):
    sum = 0.0

    print(midFaceRatio)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    facialThirds = [round(x, 2) for x in facialThirds]
    lateralCanthalTilt = round(lateralCanthalTilt, 2)
    facialWHRatio = round(facialWHRatio, 2)
    jawFrontalAngle = round(jawFrontalAngle, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    eyeSeparationRatio = round(eyeSeparationRatio, 2)
    

    print(midFaceRatio)
    print("888888888888")


    scores = []
    notes = []
    max_scores = []
    ranges = []
    current_values = []
    measurement_names = []
    advices = []

    print(gender, eyeSeparationRatio)
    print(type(gender), type(eyeSeparationRatio))

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = eye_separation_ratio_score(eyeSeparationRatio, gender, racial)
    print("Eye separation ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = facial_thirds_score(facialThirds, gender, racial)
    print("Facial thirds score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    print(type(sum), type(temp_sum), "*********************************", sum)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = lateral_canthal_tilt_score(lateralCanthalTilt, gender, racial)
    print("Lateral canthal tilt score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = facial_wh_ratio_score(facialWHRatio, gender, racial)
    print("Facial width-to-height ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = jaw_frontal_angle_score(jawFrontalAngle, gender, racial)
    print("Jaw frontal angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = cheekbone_high_setedness_score(cheekBoneHeight, gender, racial)
    print("Cheekbone high setedness score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = total_facial_wh_ratio_score(totalFacialWHRatio, gender, racial)
    print("Total face width-to-height ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = bigonial_width_score(bigonialWidth, gender, racial)
    print("Bigonial width score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = chin_philtrum_ratio_score(chin2PhiltrumRatio, gender, racial)
    print("Chin philtrum ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = neck_width_score(neckWidth, gender, racial)
    print("Neck width score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = mouth_nose_width_ratio(mouthWidth2NoseWidthRatio, gender, racial)
    print("Mouth, nose width ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = midface_ratio(midFaceRatio, gender, racial)
    print("Midface ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = eyebrow_position_ratio_score(eyebrowPositionRatio, gender, racial)
    print("Eyebrow position ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = eye_spacing_ratio_score(eyeSpacingRatio, gender, racial)
    print("Eye spacing ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = eye_aspect_ratio_score(eyeAspectRatio, gender, racial)
    print("Eye aspect ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = lower_upper_lip_ratio_score(lowerLip2UpperLipRatio, gender, racial)
    print("Lower, upper lip ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = deviation_IAA_score(deviationOfJFA2IAA, gender, racial)
    print("Deviation IAA score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = eyebrow_tilt_score(eyebrowTilt, gender, racial)
    print("Eyebrow tilt score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = bitemporal_width_score(bitemporalWidth, gender, racial)
    print("Bitemporal width score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = lower_third_proporation_score(lowerThirdProporation, gender, racial)
    print("Lower third proporation score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = lpsilateral_alar_angle_score(ipsilateralAlarAngle, gender, racial)
    print("Lpsilateral alar angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)

    (
        temp_sum,
        note,
        max_score,
        range,
        current_value,
        measurement_name,
        advice,
    ) = medial_canthal_angle(medialCanthalAngle, gender, racial)
    print("Medial canthal angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum
    advices.append(advice)
    return (
        sum,
        sum / FRONT_PROFILE_TOTAL_SCORE_MAX * 100,
        scores,
        notes,
        max_scores,
        ranges,
        current_values,
        measurement_names,
        advices,
    )


@app.post("/getfrontmark")
def get_front_mark(
    body: GetFrontMarkRequestSchema,
):
    (
        mark,
        percentage,
        scores,
        notes,
        max_scores,
        ranges,
        current_values,
        measurement_names,
        advices,
    ) = front_input(**body.dict())
    return {
        "mark": mark,
        "percent": percentage,
        "scores": scores,
        "notes": notes,
        "max_scores": max_scores,
        "ranges": ranges,
        "current_values": current_values,
        "measurement_names": measurement_names,
        "advice": advices,
    }


@app.post("/getsidemark")
def get_side_mark(
    body: GetSideMarkRequestSchema,
):
    (
        mark,
        percentage,
        scores,
        notes,
        max_scores,
        ranges,
        current_values,
        measurement_names,
        advices,
    ) = side_input(**body.dict())
    return {
        "mark": mark,
        "percent": percentage,
        "scores": scores,
        "notes": notes,
        "max_scores": max_scores,
        "ranges": ranges,
        "current_values": current_values,
        "measurement_names": measurement_names,
        "advice": advices,
    }


@app.post("/frontmagic")
async def upload_front_image(image: UploadFile):
    # Create a folder named "images" if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Save the uploaded image to the "images" folder
    file_path = os.path.join("images", "temp.jpg")
    img = Image.open(image.file)
    width = int(img.width * (800 / img.height))
    img = img.resize((width, 800))
    img.save(file_path)

    result_points = face_landmarks.process_image(file_path)
    print(result_points)

    return {"message": "Image uploaded successfully", "points": result_points.tolist()}


class Result(BaseModel):
    points: list[list[float]]


@app.post("/sidemagic")
async def upload_side_image(image: UploadFile):
    # Create a folder named "images" if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Save the uploaded image to the "images" folder
    file_path = os.path.join(".", "temp.jpg")
    img = Image.open(image.file)
    width = int(img.width * (800 / img.height))
    img = img.resize((width, 800))
    img.save(file_path)

    result_points = side_landmarks.process_image(file_path)
    print(result_points, type(result_points))
    response_data = Result(points=result_points)

    # return {"message": "Image uploaded successfully", "points": result_points.tolist()}
    # return {"message": "Image uploaded successfully", "points": "111"}
    return JSONResponse(content=response_data.dict())


@app.post("/generatemeasurementimages")
async def GenerateMeasurementImages(
    front: UploadFile = Form(...),
    side: UploadFile = Form(...),
    points: str = Form(...)
):
    print("~~~~~~~~~~generate measurement images request")
    currentTime = datetime.now()
    currentIndex = hashlib.md5(str(currentTime).encode()).hexdigest()
    
    # Save frontImage with currentIndex name
    frontImage_path = f"UPLOADS/{currentIndex}_0.jpg"
    with open(frontImage_path, "wb") as f:
        f.write(front.file.read())

    # # Save sideImage with currentIndex name
    sideImage_path = f"UPLOADS/{currentIndex}_1.jpg"
    with open(sideImage_path, "wb") as f:
        f.write(side.file.read())

    await CreateReportImages.createReportImages(frontImage_path, sideImage_path, json.JSONDecoder().decode(points))

    print(currentIndex)
    image_directory =  Path(f"REPORTS/{currentIndex}_0")

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i in range(1, 46):
            # image_path = f"REPORTS/{currentIndex}_0" + "/" + str(i) + ".jpg"
            image_path = Path(f"REPORTS/{currentIndex}") / f"{i}.jpg"
            # if image_path.is_file() and image_path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                # Add only image files to the zip archive
            zip_file.write(image_path, arcname=image_path.name)
            print(image_path)

    # Rewind the buffer to the beginning
    zip_buffer.seek(0)

    # Set the appropriate response headers
    headers = {
        "Content-Disposition": "attachment; filename=images.zip",
        "Content-Type": "application/zip",
    }

    # Return the zip file as a StreamingResponse
    return StreamingResponse(io.BytesIO(zip_buffer.read()), headers=headers)


@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/asd")
async def root():
    return {"message": "hello world asd"}

@app.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    data = await request.json()
    plan = data.get("plan")
    userEmail = data.get("userEmail")
    print(userEmail)
    print(plan)
    metadata = {
    "plan": plan,
    "userEmail": userEmail
    }
    
    if plan == "Buy Premium":
        price_id = "price_1OC6ypItQ91j83DijyVq8rbK"  # Replace with your actual price ID
    elif plan == "Buy Enterprise":
        price_id = "price_1OC90iItQ91j83DiPSgNiVUs"  # Replace with your actual price ID
    else:
        raise HTTPException(status_code=400, detail="Invalid plan selected")


        
    checkout_session = stripe.checkout.Session.create(

        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        metadata=metadata,
        success_url='https://master.d1i3eyf13fhgw2.amplifyapp.com/checkout-success',
        cancel_url='https://master.d1i3eyf13fhgw2.amplifyapp.com/pricing',
    )
    print(price_id)

    
    return {"url": checkout_session.url}


endpoint_secret = 'whsec_XsvOoUqxzhUH72aQIkMLrVe1qaYJPC5k'

@app.post("/webhook")
async def my_webhook_view(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        raise HTTPException(status_code=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise HTTPException(status_code=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
      session = event['data']['object']
      plan = session['metadata']['plan']
      userEmail = session['metadata']['userEmail']
      expire_date = calculate_expiration_date()
      if(plan == "Buy Premium"):
          result = users_collection.update_one({"email": userEmail}, {"$set": {"lvl": 1, "expire_day": expire_date}})
          if result.modified_count:
              return {"message": "Premium plan purchased successfully, expires on: " + expire_date.strftime("%Y-%m-%d")}
          else:
              raise HTTPException(status_code=404, detail="User not found or already on premium level")
      elif(plan == "Buy Enterprise"):
          result = users_collection.update_one({"email": userEmail}, {"$set": {"lvl": 2, "expire_day": expire_date}})
          if result.modified_count:
              return {"message": "Professional plan purchased successfully, expires on: " + expire_date.strftime("%Y-%m-%d")}
          else:
              raise HTTPException(status_code=404, detail="User not found or already on premium level")

        
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
