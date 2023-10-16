from typing import Union

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware

from schemas import GetFrontMarkRequestSchema
from schemas import GetSideMarkRequestSchema
import os
from PIL import Image

import face_landmarks
import side_landmarks

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

###########SIDE PROFILE###########


def gonial_angle_score(angle, gender):
    level_count = 7
    min_range_array = [
        [112, 109.5, 106, 102, 97, 92, 80],
        [114, 111, 108, 104, 99, 94, 80],
    ]
    max_range_array = [
        [123, 125.5, 129, 133, 138, 143, 160],
        [125, 128, 131, 135, 140, 146, 160],
    ]
    score_array = [40, 20, 10, 5, -20, -40, -70]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def nasofrontal_angle_score(angle, gender):
    level_count = 6
    min_range_array = [[106, 101, 97, 94, 88, 70], [122, 117, 113, 110, 107, 70]]
    max_range_array = [[129, 134, 138, 141, 147, 170], [143, 148, 152, 155, 158, 170]]
    score_array = [15, 7.5, 3.75, 1.876, -7.5, -15]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def mandibular_plane_angle_score(angle, gender):
    level_count = 6
    min_range_array = [[15, 14, 12.5, 10, 8, 0], [15, 14, 12.5, 10, 8, 0]]
    max_range_array = [[22, 27, 30, 32.5, 35, 45], [23, 27, 30, 32.5, 35, 45]]
    score_array = [12.5, 6.25, 3.125, 1.5625, -12.5, -20]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def ramus_mandible_ratio_score(ratio, gender):
    level_count = 6
    min_range_array = [
        [0.59, 0.54, 0.49, 0.41, 0.33, 0.1],
        [0.52, 0.48, 0.42, 0.34, 0.26, 0.1],
    ]
    max_range_array = [
        [0.78, 0.83, 0.88, 0.96, 1.04, 1.5],
        [0.70, 0.75, 0.8, 0.88, 0.96, 1.5],
    ]
    score_array = [10, 5, 2.5, 1.25, -5, -10]
    for i in range(level_count):
        if (
            ratio >= min_range_array[1 - gender][i]
            and ratio <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def facial_convexity_glabella_score(angle, gender):
    level_count = 6
    min_range_array = [[168, 171, 163, 160, 155, 140], [166, 163, 161, 159, 155, 140]]
    max_range_array = [[176, 179, 181, 183, 184, 195], [175, 178, 180, 182, 184, 195]]
    score_array = [10, 5, 2.5, -2.5, -10, -30]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def submental_cervical_angle_score(angle, gender):
    level_count = 5
    min_range_array = [[91, 81, 81, 75, 50], [91, 81, 81, 75, 50]]
    max_range_array = [[110, 120, 130, 140, 160], [110, 120, 130, 140, 160]]
    score_array = [10, 5, 2.5, -5, -10]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def nasofacial_angle_score(angle, gender):
    level_count = 6
    min_range_array = [[30, 36, 28, 26.5, 25.5, 10], [30, 36, 28, 26.5, 25.5, 10]]
    max_range_array = [[36, 40, 42, 43.5, 44.5, 60], [36, 40, 42, 43.5, 44.5, 60]]
    score_array = [9, 4.5, 2.25, 1.125, -4.5, -9]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def nasolabial_angle_score(angle, gender):
    level_count = 7
    min_range_array = [[94, 90, 85, 81, 70, 65, 30], [96, 92, 87, 83, 79, 74, 30]]
    max_range_array = [
        [117, 121, 126, 130, 140, 150, 190],
        [118, 122, 127, 131, 144, 154, 190],
    ]
    score_array = [7.5, 3.75, 1.875, 0.9375, -3.75, -7.5, -15]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def orbital_vector_score(value, gender):
    if value == "positive":
        return 7.5
    elif value == "slightly positive":
        return 3.75
    elif value == "neutral":
        return 1.875
    elif value == "slightly negative":
        return -3.75
    elif value == "very negative":
        return -7.5
    return -7.5


def total_facial_convexity_score(angle, gender):
    level_count = 7
    min_range_array = [
        [137.5, 135.5, 132.5, 129.5, 126.5, 124.5, 100],
        [137.5, 135.5, 132.5, 129.5, 126.5, 124.5, 100],
    ]
    max_range_array = [
        [148.5, 150.5, 153.5, 156.5, 159.5, 161.5, 180],
        [148.5, 150.5, 153.5, 156.5, 159.5, 161.5, 180],
    ]
    score_array = [7.5, 3.75, 1.875, -3.75, -7.5, -15, -30]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def mentolabial_angle_score(angle, gender):
    level_count = 6
    min_range_array = [[108, 94, 80, 75, 65, 40], [93, 79, 70, 65, 62, 40]]
    max_range_array = [[130, 144, 158, 165, 175, 200], [125, 139, 153, 160, 175, 200]]
    score_array = [7.5, 3.75, 1.875, -1.875, -3.75, -7.5]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def facial_convexity_nasion_score(angle, gender):
    level_count = 6
    min_range_array = [[163, 160, 158, 155, 152, 120], [161, 158, 156, 153, 152, 120]]
    max_range_array = [[179, 173, 175, 178, 181, 195], [179, 173, 175, 178, 181, 195]]
    score_array = [5, 2.5, 1.25, 0.625, -5, -15]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def nasal_projection_score(value, gender):
    level_count = 6
    min_range_array = [
        [0.55, 0.5, 0.45, 0.37, 0.3, 0.1],
        [0.52, 0.47, 0.42, 0.34, 0.3, 0.1],
    ]
    max_range_array = [
        [0.68, 0.75, 0.78, 0.86, 0.95, 1.4],
        [0.68, 0.75, 0.78, 0.86, 0.95, 1.4],
    ]
    score_array = [5, 2.5, 1.25, 0.625, -5, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def nasal_wh_ratio_score(value, gender):
    level_count = 6
    min_range_array = [
        [0.62, 0.55, 0.49, 0.45, 0.4, 0.1],
        [0.68, 0.61, 0.55, 0.51, 0.45, 0.1],
    ]
    max_range_array = [
        [0.88, 0.95, 1.01, 1.05, 1.1, 1.6],
        [0.93, 1.0, 1.06, 1.1, 1.13, 1.6],
    ]
    score_array = [5, 2.5, 1.25, 0.625, -5, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def ricketts_E_line_score(value, gender):
    if value == "ideal":
        return 5
    elif value == "near ideal":
        return 2.5
    else:
        return 0


def holdaway_H_line_score(value, gender):
    if value == "ideal":
        return 5
    elif value == "near ideal":
        return 2.5
    else:
        return 0


def steiner_S_line_score(value, gender):
    if value == "ideal":
        return 5
    elif value == "near ideal":
        return 2.5
    else:
        return 0


def burstone_line_score(value, gender):
    if value == "ideal":
        return 5
    elif value == "near ideal":
        return 2.5
    else:
        return 0


def nasomental_angle_score(angle, gender):
    level_count = 6
    min_range_array = [[125, 120, 118, 116, 114, 100], [125, 120, 118, 116, 114, 100]]
    max_range_array = [
        [132, 133.5, 134.5, 136.5, 138.5, 150],
        [132, 133.5, 134.5, 136.5, 138.5, 150],
    ]
    score_array = [5, 2.5, 1.25, 0.625, -2.5, -10]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def gonion_mouth_relationship_score(value, gender):
    if value == "below":
        return 5
    elif value == "in_line":
        return 1
    elif value == "above":
        return 0
    else:
        return -5


def recession_relative_frankfort_plane_score(value, gender):
    if value == "none":
        return 5
    elif value == "slight":
        return 1
    elif value == "moderate":
        return 0
    else:
        return -10


def browridge_inclination_angle_score(angle, gender):
    level_count = 7
    min_range_array = [[13, 10, 8, 6, 4, 2, 0], [10, 7, 5, 3, 1, 1, 0]]
    max_range_array = [[24, 27, 29, 31, 33, 36, 45], [22, 25, 27, 29, 31, 39, 45]]
    score_array = [4, 2, 1, 0.5, -2, -10, -20]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def nasal_tip_angle_score(angle, gender):
    level_count = 6
    min_range_array = [[112, 108, 104, 100, 97, 70], [118, 115, 111, 108, 105, 70]]
    max_range_array = [[125, 129, 133, 137, 140, 170], [131, 134, 138, 141, 144, 170]]
    score_array = [4, 2, 1, 0.5, -2, -4]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


###########FRONT PROFILE###########


def facial_thirds_score(value, gender):
    level_count = 7
    min_range_array_favor = [
        [29.5, 28, 26.5, 25, 23.5, 22.5, 18],
        [30, 29.5, 27, 25, 24, 23, 18],
    ]
    max_range_array_favor = [
        [36.5, 38, 39.5, 41, 42.5, 43.5, 50],
        [36, 37.5, 39, 41, 42, 43, 50],
    ]

    min_range_array_basic = [
        [31.5, 30.5, 29, 26.5, 25, 24, 18],
        [31.5, 31, 29.5, 29.5, 28, 27, 18],
    ]
    max_range_array_basic = [
        [34.5, 35.5, 37, 39.5, 41, 42, 50],
        [34.5, 35, 36.5, 37.5, 38, 39, 50],
    ]
    score_array = [30, 15, 7.5, 3.75, -15, -30, -40]
    if gender:
        is_favor = 0
        if value[2] >= value[0] and value[2] >= value[1]:
            is_favor = 1
        if is_favor:
            for i in range(level_count):
                for index in range(3):
                    if (
                        value[index] < min_range_array_favor[1 - gender][i]
                        or value[index] > max_range_array_favor[1 - gender][i]
                    ):
                        break
                    if index == 2:
                        return score_array[i]
        else:
            for i in range(level_count):
                for index in range(3):
                    if (
                        value[index] < min_range_array_basic[1 - gender][i]
                        or value[index] > max_range_array_basic[1 - gender][i]
                    ):
                        break
                    if index == 2:
                        return score_array[i]
    else:
        is_favor = 0
        if value[2] <= value[0] and value[2] <= value[1]:
            is_favor = 1
        if is_favor:
            for i in range(level_count):
                for index in range(3):
                    if (
                        value[index] < min_range_array_favor[1 - gender][i]
                        or value[index] > max_range_array_favor[1 - gender][i]
                    ):
                        break
                    if index == 2:
                        return score_array[i]
        else:
            for i in range(level_count):
                for index in range(3):
                    if (
                        value[index] < min_range_array_basic[1 - gender][i]
                        or value[index] > max_range_array_basic[1 - gender][i]
                    ):
                        break
                    if index == 2:
                        return score_array[i]
    return score_array[-1]


def lateral_canthal_tilt_score(value, gender):
    level_count = 7
    min_range_array = [[5.2, 4, 3, 0, -2, -4, -10], [6, 4.8, 3.6, 1.5, 0, -3, -10]]
    max_range_array = [
        [8.5, 9.7, 10.7, 13.7, 15.7, 17.9, 25],
        [9.6, 10.8, 12, 14.1, 15.6, 18.2, 25],
    ]
    score_array = [25, 12.5, 6.25, 3.125, -6.25, -25, -40]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def facial_wh_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [1.9, 1.85, 1.8, 1.75, 1.7, 1.66, 1.3],
        [1.9, 1.85, 1.8, 1.75, 1.7, 1.66, 1.3],
    ]
    max_range_array = [
        [2.06, 2.11, 2.16, 2.21, 2.26, 2.3, 2.3],
        [2.06, 2.11, 2.16, 2.21, 2.26, 2.3, 2.3],
    ]
    score_array = [25, 12.5, 6.25, 3.125, -6.25, -12.5, -25]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def jaw_frontal_angle_score(value, gender):
    level_count = 7
    min_range_array = [
        [84.5, 80.5, 76.5, 72.5, 69.5, 66.5, 40],
        [86, 82.5, 79, 75.5, 72, 69, 40],
    ]
    max_range_array = [
        [95, 99, 103, 107, 110, 113, 150],
        [97, 100.5, 104, 107.5, 111, 114, 150],
    ]
    score_array = [25, 12.5, 6.25, 3.125, -6.25, -12.5, -25]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def cheekbone_high_setedness_score(value, gender):
    level_count = 7
    min_range_array = [[81, 76, 70, 65, 60, 55, 10], [83, 79, 73, 68, 63, 58, 10]]
    max_range_array = [[100, 81, 76, 70, 65, 60, 55], [100, 83, 79, 73, 68, 63, 58]]
    score_array = [20, 12.5, 6.25, 3.125, -3.125, -12.5, -20]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def total_facial_wh_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [1.33, 1.3, 1.26, 1.23, 1.2, 1.18, 1.0],
        [1.29, 1.26, 1.22, 1.19, 1.17, 1.15, 1.0],
    ]
    max_range_array = [
        [1.38, 1.41, 1.45, 1.48, 1.51, 1.53, 1.7],
        [1.35, 1.38, 1.42, 1.45, 1.47, 1.49, 1.7],
    ]
    score_array = [15, 7.5, 3.75, 0, -3.75, -7.5, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def bigonial_width_score(value, gender):
    level_count = 7
    min_range_array = [
        [85.5, 83.5, 80.5, 77.5, 75, 70, 50],
        [81.5, 79.5, 76.5, 73.5, 70.5, 69, 50],
    ]
    max_range_array = [
        [92, 94, 97, 100, 102.5, 105, 120],
        [88.5, 90.5, 93.5, 96.5, 99.5, 102, 120],
    ]
    score_array = [15, 7.5, 3.75, 1.875, -3.75, -7.5, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def chin_philtrum_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [2.05, 1.87, 1.75, 1.55, 1.2, 1.0, 0.1],
        [2.0, 1.85, 1.7, 1.5, 1.2, 1.0, 0, 1],
    ]
    max_range_array = [
        [2.55, 2.73, 2.85, 3.05, 3.55, 3.85, 5.0],
        [2.5, 2.65, 2.8, 3, 3.5, 3.8, 5.0],
    ]
    score_array = [12.5, 6.25, 3.125, 1.5625, -6.25, -12.5, -25]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def neck_width_score(value, gender):
    level_count = 7
    min_range_array = [[90, 85, 80, 75, 70, 65, 30], [75, 69, 67, 65, 62, 57, 30]]
    max_range_array = [
        [100, 102, 105, 107, 75, 70, 130],
        [87, 93, 95, 97, 100, 103, 130],
    ]
    score_array = [10, 5, 1, -5, -10, -20, -50]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def mouth_nose_width_ratio(value, gender):
    level_count = 7
    min_range_array = [
        [1.38, 1.34, 1.3, 1.26, 1.22, 1.18, 0.9],
        [1.45, 1.4, 1.35, 1.3, 1.25, 1.21, 0.9],
    ]
    max_range_array = [
        [1.53, 1.57, 1.61, 1.65, 1.69, 1.73, 2.2],
        [1.67, 1.72, 1.77, 1.82, 1.87, 1.91, 2.2],
    ]
    score_array = [10, 5, 2.5, 1.25, -5, -10, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def midface_ratio(value, gender):
    level_count = 7
    min_range_array = [
        [0.93, 0.9, 0.88, 0.85, 0.8, 0.77, 0.5],
        [1.0, 0.97, 0.95, 0.92, 0.87, 0.84, 0.5],
    ]
    max_range_array = [
        [1.01, 1.04, 1.06, 1.09, 1.14, 1.17, 1.5],
        [1.1, 1.13, 1.15, 1.18, 1.23, 1.26, 1.5],
    ]
    score_array = [10, 5, 2.5, 1.25, -5, -10, -20]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def eyebrow_position_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [0, 0.65, 0.95, 1.2, 1.5, 1.8, 2.1],
        [0.4, 0.3, 0, 1.15, 1.35, 1.85, 2.1],
    ]
    max_range_array = [
        [0.65, 0.95, 1.2, 1.5, 1.8, 2.1, 4.0],
        [0.85, 1, 1.15, 1.35, 1.85, 2.4, 4.0],
    ]
    score_array = [10, 5, 2.5, 0, -5, -10, -20]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def eye_spacing_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [0.9, 0.86, 0.81, 0.76, 0.71, 0.67, 0.4],
        [0.9, 0.86, 0.81, 0.76, 0.71, 0.67, 0.4],
    ]
    max_range_array = [
        [1.01, 1.05, 1.07, 1.08, 1.1, 1.15, 2],
        [1.01, 1.05, 1.07, 1.08, 1.1, 1.15, 2],
    ]
    score_array = [10, 5, 2.5, 0, -5, -10, -20]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def eye_aspect_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [2.8, 2.6, 2.4, 2.2, 2, 1.8, 0],
        [2.55, 2.35, 2.15, 1.95, 1.75, 1.8, 0],
    ]
    max_range_array = [
        [3.6, 3.8, 4, 4.2, 4.4, 4.6, 6],
        [3.2, 3.4, 3.6, 3.8, 4.0, 4.6, 6],
    ]
    score_array = [10, 5, 2.5, 1.25, -5, -10, -20]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def lower_upper_lip_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [1.4, 1.1, 0.9, 0.7, 0.4, 0.1, 0.1],
        [1.35, 1.05, 0.85, 0.75, 0.35, 0.1, 0.1],
    ]
    max_range_array = [
        [2.0, 2.3, 2.5, 2.7, 3.0, 3.5, 5],
        [2.0, 2.3, 2.5, 2.7, 3.0, 3.5, 5],
    ]
    score_array = [7.5, 3.75, 1.875, 0.9375, -3.75, -7.5, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def deviation_IAA_score(value, gender):
    level_count = 6
    min_range_array = [[0, 2.5, 5, 10, 15, 20], [0, 2.5, 5, 10, 15, 20]]
    max_range_array = [[2.5, 5, 10, 15, 20, 100], [2.5, 5, 10, 15, 20, 100]]
    score_array = [7, 3.75, 1.875, 0.9375, -3.75, -7.5]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def eyebrow_tilt_score(value, gender):
    level_count = 6
    min_range_array = [[5, 3, 0, -2, -4, -15], [11, 9, 6, 4, 2, -15]]
    max_range_array = [[13, 15, 18, 20, 22, 40], [18.7, 20.7, 23.7, 25.7, 27.7, 40]]
    score_array = [6, 3, 1.5, -3, -6, -12]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def bitemporal_width_score(value, gender):
    level_count = 7
    min_range_array = [[84, 82, 79, 77, 74, 71, 50], [79, 76, 73, 70, 67, 65, 50]]
    max_range_array = [
        [95, 97, 100, 102, 105, 108, 125],
        [92, 95, 98, 101, 104, 106, 125],
    ]
    score_array = [5, 2.5, 1.25, -2.5, -5, -10, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def lower_third_proporation_score(value, gender):
    level_count = 6
    min_range_array = [
        [30.6, 29.6, 28.4, 27.2, 26.6, 20],
        [31.2, 30.2, 29.2, 28.2, 27.2, 20],
    ]
    max_range_array = [[34, 35, 36.2, 37.4, 38, 45], [34.5, 35.5, 36.5, 37.5, 38.5, 45]]
    score_array = [5, 2.5, 1.25, -2.5, -5, -10]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def lpsilateral_alar_angle_score(value, gender):
    level_count = 7
    min_range_array = [[84, 82, 79, 77, 75, 73, 50], [84, 82, 79, 77, 75, 73, 50]]
    max_range_array = [
        [95, 97, 100, 102, 104, 106, 150],
        [95.5, 97.5, 100.5, 102.5, 104.5, 106.5, 150],
    ]
    score_array = [2.5, 1.25, 0.63, 0, -1.25, -2.5, -5]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def medial_canthal_angle(value, gender):
    level_count = 7
    min_range_array = [[29, 25, 21, 18, 15, 10, 5], [33, 29, 22, 19, 16, 13, 5]]
    max_range_array = [[47, 51, 57, 63, 69, 75, 120], [51, 55, 61, 65, 71, 77, 120]]
    score_array = [10, 5, 2.5, -2.5, -5, -10, -15]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def eye_separation_ratio_score(value, gender):
    level_count = 7
    min_range_array = [
        [44.3, 43.6, 43.1, 42.6, 42, 41, 35],
        [45, 44.3, 43.8, 43.3, 42.7, 42, 35],
    ]
    max_range_array = [
        [47.4, 48.4, 48.9, 49.4, 50, 51, 58],
        [47.9, 48.6, 49.1, 49.6, 50.2, 51, 58],
    ]
    score_array = [35, 17.5, 8.75, 4.375, -8.75, -17.5, -35]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i]
    return score_array[-1]


def side_input(
    gender: int,
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
    sum = 0
    temp_sum = gonial_angle_score(gonialAngle, gender)
    print("Gonial angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = nasofrontal_angle_score(nasofrontalAngle, gender)
    print("Nasofrontal angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = mandibular_plane_angle_score(mandibularPlaneAngle, gender)
    print("Mandibular plane angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = ramus_mandible_ratio_score(ramus2MandibleRatio, gender)
    print("Ramus mandible ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = facial_convexity_glabella_score(facialConvexityGlabella, gender)
    print("Facial convexity glabella score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = submental_cervical_angle_score(submentalCervicalAngle, gender)
    print("Submental cervical angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = nasofacial_angle_score(nasofacialAngle, gender)
    print("Nasofacial angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = nasolabial_angle_score(nasolabialAngle, gender)
    print("Nasolabial angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = orbital_vector_score(orbitalVector, gender)
    print("Orbital vector score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = total_facial_convexity_score(totalFacialConvexity, gender)
    print("Total facial convexity score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = mentolabial_angle_score(mentolabialAngle, gender)
    print("Mentolabial angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = facial_convexity_nasion_score(facialConvexityNasion, gender)
    print("Facial convexity nasion score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = nasal_projection_score(nasalProjection, gender)
    print("Nasal Projection score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = nasal_wh_ratio_score(nasalW2HRatio, gender)
    print("Nasal W to H ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = ricketts_E_line_score(rickettsELine, gender)
    print("Ricketts E line score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = holdaway_H_line_score(holdawayHLine, gender)
    print("Holdaway H line score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = steiner_S_line_score(steinerSLine, gender)
    print("Steiner S line score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = burstone_line_score(burstoneLine, gender)
    print("Burstone line score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = nasomental_angle_score(nasomentalAngle, gender)
    print("Nasomental angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = gonion_mouth_relationship_score(gonion2MouthRelationship, gender)
    print("Gonion, mouth relationship score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = recession_relative_frankfort_plane_score(
        recessionRelative2FrankfortPlane, gender
    )
    print("Recession relative frankfort plane score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = browridge_inclination_angle_score(browridgeInclinationAngle, gender)
    print("Browridge inclination angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = nasal_tip_angle_score(nasalTipAngle, gender)
    print("Nasal tip angle score is ", temp_sum)
    sum = sum + temp_sum

    print("Total Side Profile score is ", sum)
    print(
        "Total side profile percentage is ",
        sum / SIDE_PROFILE_TOTAL_SCORE_MAX * 100,
        "%",
    )
    return sum, sum / SIDE_PROFILE_TOTAL_SCORE_MAX * 100


def front_input(
    gender: int,
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
    sum = 0

    print(gender, eyeSeparationRatio)
    print(type(gender), type(eyeSeparationRatio))

    temp_sum = eye_separation_ratio_score(eyeSeparationRatio, gender)
    print("Eye separation ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = facial_thirds_score(facialThirds, gender)
    print("Facial thirds score is ", temp_sum, facialThirds, gender)
    sum = sum + temp_sum

    temp_sum = lateral_canthal_tilt_score(lateralCanthalTilt, gender)
    print("Lateral canthal tilt score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = facial_wh_ratio_score(facialWHRatio, gender)
    print("Facial width-to-height ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = jaw_frontal_angle_score(jawFrontalAngle, gender)
    print("Jaw frontal angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = cheekbone_high_setedness_score(cheekBoneHeight, gender)
    print("Cheekbone high setedness score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = total_facial_wh_ratio_score(totalFacialWHRatio, gender)
    print("Total face width-to-height ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = bigonial_width_score(bigonialWidth, gender)
    print("Bigonial width score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = chin_philtrum_ratio_score(chin2PhiltrumRatio, gender)
    print("Chin philtrum ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = neck_width_score(neckWidth, gender)
    print("Neck width score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = mouth_nose_width_ratio(mouthWidth2NoseWidthRatio, gender)
    print("Mouth, nose width ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = midface_ratio(midFaceRatio, gender)
    print("Midface ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = eyebrow_position_ratio_score(eyebrowPositionRatio, gender)
    print("Eyebrow position ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = eye_spacing_ratio_score(eyeSpacingRatio, gender)
    print("Eye spacing ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = eye_aspect_ratio_score(eyeAspectRatio, gender)
    print("Eye aspect ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = lower_upper_lip_ratio_score(lowerLip2UpperLipRatio, gender)
    print("Lower, upper lip ratio score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = deviation_IAA_score(deviationOfJFA2IAA, gender)
    print("Deviation IAA score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = eyebrow_tilt_score(eyebrowTilt, gender)
    print("Eyebrow tilt score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = bitemporal_width_score(bitemporalWidth, gender)
    print("Bitemporal width score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = lower_third_proporation_score(lowerThirdProporation, gender)
    print("Lower third proporation score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = lpsilateral_alar_angle_score(ipsilateralAlarAngle, gender)
    print("Lpsilateral alar angle score is ", temp_sum)
    sum = sum + temp_sum

    temp_sum = medial_canthal_angle(medialCanthalAngle, gender)
    print("Medial canthal angle score is ", temp_sum)
    sum = sum + temp_sum

    print("Front profile score is ", sum)
    print(
        "Total front profile percentage is ",
        sum / FRONT_PROFILE_TOTAL_SCORE_MAX * 100,
        "%",
    )
    return sum, sum / FRONT_PROFILE_TOTAL_SCORE_MAX * 100


@app.post("/getfrontmark")
def get_front_mark(
    body: GetFrontMarkRequestSchema,
):
    print(body)
    # print (body.bigonialWidth)
    mark, percentage = front_input(**body.dict())
    return {"mark": mark, "percent": percentage}


@app.post("/getsidemark")
def get_side_mark(
    body: GetSideMarkRequestSchema,
):
    print(body)
    # print (body.bigonialWidth)
    mark, percentage = side_input(**body.dict())
    return {"mark": mark, "percent": percentage}

@app.post("/frontmagic")
async def upload_image(image: UploadFile):
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

    return {"message": "Image uploaded successfully",
            "points": result_points.tolist()}

@app.post("/sidemagic")
async def upload_image(image: UploadFile):
    # Create a folder named "images" if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Save the uploaded image to the "images" folder
    file_path = os.path.join("images", "temp.jpg")
    img = Image.open(image.file)
    width = int(img.width * (800 / img.height))
    img = img.resize((width, 800))
    img.save(file_path)


    result_points = side_landmarks.process_image(file_path)
    print(result_points)

    return {"message": "Image uploaded successfully",
            "points": result_points}


@app.post("/get_test/")
def get_test():
    return {"result": "good"}