from typing import Union

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware

from schemas import GetFrontMarkRequestSchema
from schemas import GetSideMarkRequestSchema
import os
from PIL import Image

import face_landmarks
# import side_landmarks
import front_profile_calc
import side_profile_calc

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/getfrontmark")
def get_front_mark(
    body: GetFrontMarkRequestSchema,
):
    # print (body.bigonialWidth)
    (
        mark,
        percentage,
        scores,
        notes,
        max_scores,
        ranges,
        current_values,
        measurement_names,
        advices
    ) = front_input(**body.dict())
    print(
        mark,
        percentage,
        scores,
        notes,
        max_scores,
        ranges,
        current_values,
        measurement_names,
        advices
    )
    return {
        "mark": mark,
        "percent": percentage,
        "scores": scores,
        "notes": notes,
        "max_scores": max_scores,
        "ranges": ranges,
        "current_values": current_values,
        "measurement_names": measurement_names,
        "advice":advices
    }


@app.post("/getsidemark")
def get_side_mark(
    body: GetSideMarkRequestSchema,
):
    print(body)
    # print (body.bigonialWidth)
    (
        mark,
        percentage,
        scores,
        notes,
        max_scores,
        ranges,
        current_values,
        measurement_names,
        advices
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


@app.post("/sidemagic")
async def upload_side_image(image: UploadFile):
    # Create a folder named "images" if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Save the uploaded image to the "images" folder
    file_path = os.path.join("images", "temp.jpg")
    img = Image.open(image.file)
    width = int(img.width * (800 / img.height))
    img = img.resize((width, 800))
    img.save(file_path)

    # result_points = side_landmarks.process_image(file_path)
    result_points = [[0,0]]*30
    print(result_points)

    return {"message": "Image uploaded successfully", "points": result_points}
