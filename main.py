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
    measurement_name = "Gonial angle(°)"
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
    notes = ["Your jaw has an ideal shape. Since your Gonial angle is neither too obtuse or acute, your jaw is likely neither too square or steep/rounded in shape.",
             "Your jawline has a near ideal shape. Your jaw's structure may be slightly more rounded or squared than is preferred, but it is still within a harmonious range.",
             "Although your jawline does not have the most preferred shape, it still has a normal shape. Your jaw's structure may be slightly more rounded or squared than is preferred, but it is still within a normal range.",
             "Although your jawline does not have the most preferred shape, it still is within a reasonably normal range. Your jaw's structure may be noticeably rounded or squared, but it may not be enough to indicate facial abnormality.",
             "Your jawline's shape would not generally be considered favorable. It is either too square (low value) or rounded and lacking angularity (high value).",
             "Your jawline is beginning to stray into the extremes and would not generally be considered harmonious. It is likely that your jaw is either too square or rounded in shape."
             "Your jawline shape is at the extremes and would not generally be considered harmonious. It is likely that your jaw is either too square or rounded in shape."]
    
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name


def nasofrontal_angle_score(angle, gender):
    measurement_name = "Nasofrontal angle (°)"
    level_count = 6
    min_range_array = [[106, 101, 97, 94, 88, 70], [122, 117, 113, 110, 107, 70]]
    max_range_array = [[129, 134, 138, 141, 147, 170], [143, 148, 152, 155, 158, 170]]
    score_array = [15, 7.5, 3.75, 1.876, -7.5, -15]
    notes = ["The angle formed between your brow ridge and nose is pleasant. Your brow region is neither too soft or harsh.",
             "Although not ideal, the angle formed between your brow ridge and nose is generally pleasant. Your brow region is neither too soft or harsh.",
             "Although not ideal, the angle formed between your brow ridge and nose is within a normal range. Your brow region is may begin to appear too protrusive (low values) or soft (high values).",
             "Although not ideal, the angle formed between your brow ridge and nose is within a reasonably normal range. Your brow region is may appear too protrusive (low values) or soft (high values).",
             "The angle formed between your brow ridge and nose is outside of a normal range. Your brow region is may appear too protrusive (low values) or soft (high values).",
             "The angle formed between your brow ridge and nose is outside at the extremes, indicating a lack of facial harmony. Your brow region is may appear too protrusive (low values) or soft (high values)."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name


def mandibular_plane_angle_score(angle, gender):
    measurement_name = "Mandibular plane angle (°)"
    level_count = 6
    min_range_array = [[15, 14, 12.5, 10, 8, 0], [15, 14, 12.5, 10, 8, 0]]
    max_range_array = [[22, 27, 30, 32.5, 35, 45], [23, 27, 30, 32.5, 35, 45]]
    score_array = [12.5, 6.25, 3.125, 1.5625, -12.5, -20]
    notes = ["The slope of your mandible is harmonious, being neither too flat or downward grown. This is usually indicative of a healthy jaw and normal growth pattern.",
             "While not perfectly ideal, the slope of your mandible is harmonious, being neither too flat or downward grown. This is usually indicative of a healthy jaw and normal growth pattern.",
             "While not an ideal shape, the slope of your mandible is within a normal range of values. At this point, the growth of your jaw may indicate some hyper/hypo-divergent growth patterns, but it also may not.",
             "The slope of your mandible is slightly outside of a normal range of values. At this point, the growth of your jaw may indicate some hyper/hypo-divergent growth patterns. Your jaw may be either too flat (low values) or too steep (high values).",
             "The slope of your mandible is outside of a normal range of values. At this point, the growth of your jaw indicates some hyper/hypo-divergent growth patterns. Your jaw may be either too flat (low values) or too steep (high values).",
             "The slope of your mandible is far outside of a normal range of values. At this point, the growth of your jaw indicates some hyper/hypo-divergent growth patterns. Your jaw may be either too flat (low values) or too steep (high values)."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name


def ramus_mandible_ratio_score(ratio, gender):
    measurement_name = "Mandibular plane angle (°)"
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
    notes= ["The length of your ramus relative your mandible is harmonious. Your ramus is neither too long or short.",
            "Although not ideal, the length of your ramus relative your mandible is generally harmonious. Your ramus is neither too long or short.",
            "Although not ideal, the length of your ramus relative your mandible is within a normal range of values. Your ramus is neither too long or short.",
            "The length of your ramus relative your mandible is beginning to fall outside of the normal range. Your ramus may be considered too short (low values) or too long (high values).",
            "The length of your ramus relative your mandible falls outside of the normal range. Your ramus can be considered too short (low values) or too long (high values).",
            "Although not ideal, the length of your ramus relative your mandible is within a normal range of values. Your ramus is neither too long or short."]
    for i in range(level_count):
        if (
            ratio >= min_range_array[1 - gender][i]
            and ratio <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], ratio, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], ratio, measurement_name

def facial_convexity_glabella_score(angle, gender):
    measurement_name = "Facial convexity (glabella) (°)"
    level_count = 6
    min_range_array = [[168, 171, 163, 160, 155, 140], [166, 163, 161, 159, 155, 140]]
    max_range_array = [[176, 179, 181, 183, 184, 195], [175, 178, 180, 182, 184, 195]]
    score_array = [10, 5, 2.5, -2.5, -10, -30]
    notes = ["You have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with no severe overjet or underbite.",
             "Although not perfectly harmonious, you have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with perhaps some minor overjet (low values) or underbite (high values).",
             "Although not perfectly harmonious, you have a normal shape of the side profile. Neither part of your face -- upper, middle, or lower are in extreme disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
             "Your side profile shape is beginning to stray outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
             "Your side profile shape is outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
             "Your side profile shape is far outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in extreme disharmony to one another. You certainly have some occlusal issues like perhaps an overjet (low values) or underbite (high values)."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def submental_cervical_angle_score(angle, gender):
    measurement_name = "Submental cervical angle (°)"
    level_count = 5
    min_range_array = [[91, 81, 81, 75, 50], [91, 81, 81, 75, 50]]
    max_range_array = [[110, 120, 130, 140, 160], [110, 120, 130, 140, 160]]
    score_array = [10, 5, 2.5, -5, -10]
    notes = ["The angle between your neck and lower jaw is harmonious and defined.",
             "Although not perfectly ideal, the angle between your neck and lower jaw is generally harmonious and defined.",
             "Although not perfectly ideal, the angle between your neck and lower jaw is within a normal range.",
             "The angle between your neck and lower jaw is outside of the normal range and may indicate lacking jaw definition.",
             "The angle between your neck and lower jaw is far outside of the normal range and may indicate lacking jaw definition."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def nasofacial_angle_score(angle, gender):
    measurement_name = "Nasofacial angle (°)"
    level_count = 6
    min_range_array = [[30, 36, 28, 26.5, 25.5, 10], [30, 36, 28, 26.5, 25.5, 10]]
    max_range_array = [[36, 40, 42, 43.5, 44.5, 60], [36, 40, 42, 43.5, 44.5, 60]]
    score_array = [9, 4.5, 2.25, 1.125, -4.5, -9]
    notes = ["This angle indicates a harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
             "While not perfectly ideal, your angle indicates a harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
             "While not perfectly ideal, your angle indicates a normal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This may indicate that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle.",
             "Your angle indicates a slightly abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This may indicate that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle.",
             "Your angle indicates an abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This indicates that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle.",
             "Your angle indicates an extremely abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This indicates that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def nasolabial_angle_score(angle, gender):
    measurement_name = "Nasolabial angle (°)"
    level_count = 7
    min_range_array = [[94, 90, 85, 81, 70, 65, 30], [96, 92, 87, 83, 79, 74, 30]]
    max_range_array = [
        [117, 121, 126, 130, 140, 150, 190],
        [118, 122, 127, 131, 144, 154, 190],
    ]
    score_array = [7.5, 3.75, 1.875, 0.9375, -3.75, -7.5, -15]
    notes = ["Your nose has a pleasant and ideal shape. Your nose is likely not too upturned or droopy and your philtrum probably has a pleasant shape.",
             "Your nose has a pleasant shape. Your nose is likely not too upturned or droopy and your philtrum probably has a pleasant shape.",
             "While not ideal, your nose has a normal shape. Your nose may begin to appear noticeably upturned or droopy and your philtrum may have a less than ideal shape.",
             "While not ideal, your nose has a reasonably normal shape. Your nose may begin to appear noticeably upturned or droopy and your philtrum may have a less than ideal shape.",
             "Your nose has an abnormal shape. Your nose may be noticeably upturned (high values) or droopy (low values) and your philtrum may have a less than ideal shape.",
             "Your nose has an extremely abnormal shape. Your nose may be noticeably upturned (high values) or droopy (low values) and your philtrum may have a less than ideal shape.",
             "Your nose has an extremely abnormal shape. Your nose may be noticeably upturned (high values) or droopy (low values) and your philtrum may have a less than ideal shape."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def orbital_vector_score(value, gender):
    measurement_name = "Orbital vector"
    if value == "positive":
        return 7.5, "Your nose has a pleasant and ideal shape. Your nose is likely not too upturned or droopy and your philtrum probably has a pleasant shape.", 7.5, "Positive", value, measurement_name
    elif value == "slightly positive":
        return 3.75, "You have a slightly positive orbital vector, indicating no infraorbital hollowing. This is a youthful feature that is generally considered attractive.", 7.5, "Positive", value, measurement_name
    elif value == "neutral":
        return 1.875, "You have a neutral orbital vector, indicating no infraorbital hollowing. While you could have more soft tissue protrusion under your eyes, this is a feature that is generally considered attractive.", 7.5, "Positive", value, measurement_name
    elif value == "slightly negative":
        return -3.75, "You have a slightly negative orbital vector, indicating some infraorbital hollowing. While you could have more soft tissue protrusion under your eyes, this is not yet extreme hollowing.", 7.5, "Positive", value, measurement_name
    elif value == "very negative":
        return -7.5, "You have a very negative orbital vector, indicating noticeable infraorbital hollowing. This is generally considered an unattractive feature.", 7.5, "Positive", value, measurement_name
    return -7.5, "You have a very negative orbital vector, indicating noticeable infraorbital hollowing. This is generally considered an unattractive feature.", 7.5, "Positive", value, measurement_name

def total_facial_convexity_score(angle, gender):
    measurement_name = "Total facial convexity"
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
    notes = ["The harmony of your lateral profile is pleasant when considering your nose. This means that your nose harmonizes well with the projection of your brow ridge and chin.",
             "The harmony of your lateral profile is generally pleasant when considering your nose. This means that your nose harmonizes well with the projection of your brow ridge and chin.",
             "The harmony of your lateral profile is normal when considering your nose. This means that your nose harmonizes reasonably well with the projection of your brow ridge and chin.",
             "The harmony of your lateral profile is beginning to appear abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin.",
             "The harmony of your lateral profile is abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin.",
             "The harmony of your lateral profile is extremely abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin.",
             "The harmony of your lateral profile is extremely abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def mentolabial_angle_score(angle, gender):
    measurement_name = "Mentolabial angle"
    level_count = 6
    min_range_array = [[108, 94, 80, 75, 65, 40], [93, 79, 70, 65, 62, 40]]
    max_range_array = [[130, 144, 158, 165, 175, 200], [125, 139, 153, 160, 175, 200]]
    score_array = [7.5, 3.75, 1.875, -1.875, -3.75, -7.5]
    notes = ["You have a pleasant contour of the chin. The indent formed between your chin is neither too deep or flat.",
             "You have a generally pleasant contour of the chin. The indent formed between your chin is neither too deep or flat.",
             "You have a normal contour of the chin. The indent formed between your chin could be a bit more normalized since it is either too indented (low values) or flat (high values).",
             "You have a slightly abnormal contour of the chin. The indent formed between your chin could be a bit more normalized since it is either too indented (low values) or flat (high values).",
             "You have an abnormal contour of the chin. The indent formed between your chin could be a bit more normalized since it is too indented (low values) or flat (high values).",
             "You have an extremely abnormal contour of the chin. The indent formed between your chin could be a bit more normalized since it is too indented (low values) or flat (high values)."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def facial_convexity_nasion_score(angle, gender):
    measurement_name = "Facial convexity (nasion)"
    level_count = 6
    min_range_array = [[163, 160, 158, 155, 152, 120], [161, 158, 156, 153, 152, 120]]
    max_range_array = [[179, 173, 175, 178, 181, 195], [179, 173, 175, 178, 181, 195]]
    score_array = [5, 2.5, 1.25, 0.625, -5, -15]
    notes = ["You have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with no severe overjet or underbite.",
             "Although not perfectly harmonious, you have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with perhaps some minor overjet (low values) or underbite (high values).",
             "Although not perfectly harmonious, you have a normal shape of the side profile. Neither part of your face -- upper, middle, or lower are in extreme disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
             "Your side profile shape is beginning to stray outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
             "Your side profile shape is outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
             "Your side profile shape is far outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in extreme disharmony to one another. You certainly have some occlusal issues like perhaps an overjet (low values) or underbite (high values)."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def nasal_projection_score(value, gender):
    measurement_name = "Nasal projection"
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
    notes = ["You have an ideal nasal projection. Your nose is not too pronounced or unprojected.",
             "You have a near ideal nasal projection. Your nose is not too pronounced or unprojected.",
             "While not ideal, you have a normal nasal projection. Your nose may be considered slightly too projected (high values) or unprojected (low values).",
             "You have a slightly abnormal nasal projection. Your nose may be slightly too projected (high values) or unprojected (low values).",
             "You have an abnormal nasal projection. Your nose is slightly too projected (high values) or unprojected (low values).",
             "You have an extremely abnormal nasal projection. Your nose is slightly too projected (high values) or unprojected (low values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def nasal_wh_ratio_score(value, gender):
    measurement_name = "Nasal W to H ratio"
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
    notes = ["You have an ideal Nasal WHR. The projection of your nose is proportionate relative to its height.",
             "You have a near ideal Nasal WHR. The projection of your nose is proportionate relative to its height.",
             "You have a normal Nasal WHR. The projection of your nose is reasonably proportionate relative to its height.",
             "You have a slightly abnormal Nasal WHR. The projection of your nose may be slightly too much (high values) or too little (low values) compared to its height.",
             "You have an abnormal Nasal WHR. The projection of your nose may be too much (high values) or too little (low values) compared to its height.",
             "You have an extremely abnormal Nasal WHR. The projection of your nose may be too much (high values) or too little (low values) compared to its height."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def ricketts_E_line_score(value, gender):
    measurement_name = "Ricketts' E line"
    if value == "ideal":
        return 5, "You have a pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name
    elif value == "near ideal":
        return 2.5, "You have a reasonably pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name
    else:
        return 0, "You do not have a pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name

def holdaway_H_line_score(value, gender):
    measurement_name = "Holdaway H line"
    if value == "ideal":
        return 5, "You have a pleasant harmony between your chin and lips according to this specific assessment.", 5, "Ideal", value, measurement_name
    elif value == "near ideal":
        return 2.5, "You have a reasonably pleasant harmony between your chin and lips according to this specific assessment.", 5, "Ideal", value, measurement_name
    else:
        return 0, "You have an unpleasant harmony between your chin and lips according to this specific assessment.", 5, "Ideal", value, measurement_name

def steiner_S_line_score(value, gender):
    measurement_name = "Steiner S line"
    if value == "ideal":
        return 5, "You have a pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name
    elif value == "near ideal":
        return 2.5, "You have a reasonably pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name
    else:
        return 0, "You do not have a pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name

def burstone_line_score(value, gender):
    measurement_name = "Burstone line"
    if value == "ideal":
        return 5, "You have a pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name
    elif value == "near ideal":
        return 2.5, "You have a reasonably pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name
    else:
        return 0, "You do not have a pleasant harmony between your chin, lips, and nose according to this specific assessment.", 5, "Ideal", value, measurement_name

def nasomental_angle_score(angle, gender):
    measurement_name = "Nasomental angle (°)"
    level_count = 6
    min_range_array = [[125, 120, 118, 116, 114, 100], [125, 120, 118, 116, 114, 100]]
    max_range_array = [
        [132, 133.5, 134.5, 136.5, 138.5, 150],
        [132, 133.5, 134.5, 136.5, 138.5, 150],
    ]
    score_array = [5, 2.5, 1.25, 0.625, -2.5, -10]
    notes = ["This angle indicates a harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
             "This angle indicates a reasonably harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
             "While not ideal, this angle indicates a normal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a normal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
             "This angle indicates a slightly abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have an abnormal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
             "This angle indicates an abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It probably indicates that you have an abnormal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
             "This angle indicates an extremely abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It probably indicates that you have an extremely abnormal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def gonion_mouth_relationship_score(value, gender):
    measurement_name = "Gonion to mouth relationship"
    if value == "below":
        return 5, "Your ramus has sufficient vertical growth.", 5, "Below", value, measurement_name
    elif value == "in_line":
        return 1, "Your ramus has normal vertical growth, but could ideally have more length.", 5, "Below", value, measurement_name
    elif value == "above":
        return 0, "Your ramus has lacking vertical growth.", 5, "Below", value, measurement_name
    else:
        return -5, "Your ramus has severely lacking vertical growth.", 5, "Below", value, measurement_name

def recession_relative_frankfort_plane_score(value, gender):
    measurement_name = "Recession relative to frankfort plane"
    if value == "none":
        return 5, "According to this assessment, you have no notable recession regarding the position of your chin relative to your nasion.", 5, "None", value, measurement_name
    elif value == "slight":
        return 1, "According to this assessment, you have slight recession regarding the position of your chin relative to your nasion.", 5, "None", value, measurement_name
    elif value == "moderate":
        return 0, "According to this assessment, you have moderate recession regarding the position of your chin relative to your nasion.", 5, "None", value, measurement_name
    else:
        return -10, "According to this assessment, you have extreme recession regarding the position of your chin relative to your nasion.", 5, "None", value, measurement_name

def browridge_inclination_angle_score(angle, gender):
    measurement_name = "Browridge inclination angle (°)"
    level_count = 7
    min_range_array = [[13, 10, 8, 6, 4, 2, 0], [10, 7, 5, 3, 1, 1, 0]]
    max_range_array = [[24, 27, 29, 31, 33, 36, 45], [22, 25, 27, 29, 31, 39, 45]]
    score_array = [4, 2, 1, 0.5, -2, -10, -20]
    notes = ["Your forehead is not overly sloped back or flat. It is harmonious in shape.",
             "While not ideal, your forehead is not overly sloped back or flat.",
             "While not ideal, your forehead has a normal shape. It is not overly sloped back (high values) or flat (low values).",
             "Your forehead has a slightly  abnormal shape. It is likely overly sloped back (high values) or flat (low values).",
             "Your forehead has an abnormal shape. It is likely overly sloped back (high values) or flat (low values).",
             "Your forehead has an extremely abnormal shape. It is either overly sloped back (high values) or flat (low values).",
             "Your forehead has an extremely abnormal shape. It is either overly sloped back (high values) or flat (low values)."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name

def nasal_tip_angle_score(angle, gender):
    measurement_name = "Nasal tip angle (°)"
    level_count = 6
    min_range_array = [[112, 108, 104, 100, 97, 70], [118, 115, 111, 108, 105, 70]]
    max_range_array = [[125, 129, 133, 137, 140, 170], [131, 134, 138, 141, 144, 170]]
    score_array = [4, 2, 1, 0.5, -2, -4]
    notes = ["You have a harmonious nasal tip that is not overly upturned or droopy.",
             "You have a generally harmonious nasal tip that is not overly upturned or droopy.",
             "You have a normal nasal tip angle, but it may be considered slightly too upturned (high values) or droopy (low values).",
             "You have an abnormal nasal tip angle, indicating that your nose is either too upturned (high values) or droopy (low values).",
             "You have an abnormal nasal tip angle, indicating that your nose is either too upturned (high values) or droopy (low values).",
             "You have an extremely abnormal nasal tip angle, indicating that your nose is either too upturned (high values) or droopy (low values)."]
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i]
            and angle <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], angle, measurement_name


###########FRONT PROFILE###########
def facial_thirds_score(value, gender):
    measurement_name = "Facial thirds (%)"
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
    notes = ["Your facial thirds are harmoniously distributed, leading to a balanced appearance of the upper, middle, and lower parts of your face.",
             "Although not ideal, your facial thirds are harmoniously distributed, leading to a balanced appearance of the upper, middle, and lower parts of your face.",
             "Although not ideal, your facial thirds are normally distributed, leading to a reasonably balanced appearance of the upper, middle, and lower parts of your face. One of your thirds may begin to appear overly short or long in relation to the others.",
             "Your facial thirds are slightly abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds likely appears overly short or long in relation to the others.",
             "Your facial thirds are abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds appears overly short or long in relation to the others.",
             "Your facial thirds are extremely abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds appears overly short or long in relation to the others.",
             "Your facial thirds are extremely abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds appears overly short or long in relation to the others."]
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
                        return score_array[i], notes[i], score_array[0], [min_range_array_favor[1-gender][0], max_range_array_favor[1 - gender][0]], value, measurement_name
        else:
            for i in range(level_count):
                for index in range(3):
                    if (
                        value[index] < min_range_array_basic[1 - gender][i]
                        or value[index] > max_range_array_basic[1 - gender][i]
                    ):
                        break
                    if index == 2:
                        return score_array[i], notes[i], score_array[0], [min_range_array_basic[1-gender][0], max_range_array_basic[1 - gender][0]], value, measurement_name
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
                        return score_array[i], notes[i], score_array[0], [min_range_array_favor[1-gender][0], max_range_array_favor[1 - gender][0]], value, measurement_name
        else:
            for i in range(level_count):
                for index in range(3):
                    if (
                        value[index] < min_range_array_basic[1 - gender][i]
                        or value[index] > max_range_array_basic[1 - gender][i]
                    ):
                        break
                    if index == 2:
                        return score_array[i], notes[i], score_array[0], [min_range_array_basic[1-gender][0], max_range_array_basic[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array_basic[1-gender][0], max_range_array_basic[1 - gender][0]], value, measurement_name

def lateral_canthal_tilt_score(value, gender):
    measurement_name = "Lateral Canthal Tilt (°)"
    level_count = 7
    min_range_array = [[5.2, 4, 3, 0, -2, -4, -10], [6, 4.8, 3.6, 1.5, 0, -3, -10]]
    max_range_array = [
        [8.5, 9.7, 10.7, 13.7, 15.7, 17.9, 25],
        [9.6, 10.8, 12, 14.1, 15.6, 18.2, 25],
    ]
    score_array = [25, 12.5, 6.25, 3.125, -6.25, -25, -40]
    notes = ["Your eyes have a harmonious tilt, meaning they are not overly droopy or upturned.",
             "Your eyes have a generally harmonious tilt, meaning they are not overly droopy or upturned.",
             "Although not perfectly ideal, your eyes have a normal tilt, meaning they are not overly droopy or upturned.",
             "Your eyes have a slightly abnormal tilt. They may begin to appear slightly droopy (low values) or overly upturned (high values)",
             "Your eyes have a slightly abnormal tilt. They may begin to appear slightly droopy (low values) or overly upturned (high values)",
             "Your eyes have an abnormal tilt.  They appear overly droopy (low values) or overly upturned (high values)",
             "Your eyes have an extremely  abnormal tilt.  They appear overly droopy (low values) or overly upturned (high values)"]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def facial_wh_ratio_score(value, gender):
    measurement_name = "Facial width-to-height ratio"
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
    notes = ["You have an ideal FWHR, indicating a facial width and midface height that harmonize well with one another. Your midface region (i.e., FWHR) is not overly compact or elongated in shape.",
             "You have a near ideal FWHR, indicating a facial width and midface height that harmonize well with one another. Your midface region (i.e., FWHR) is not overly compact or elongated in shape.",
             "Although not ideal, you have a normal FWHR, indicating a facial width and midface height that harmonize reasonably well with one another. Your midface region (i.e., FWHR) may begin to appear slightly long or compact, but it is not an aesthetic flaw.",
             "You have a normal FWHR, indicating a facial width and midface height that harmonize reasonably well with one another. Your midface region (i.e., FWHR) may begin to appear slightly long or compact, but it is not a large aesthetic flaw.",
             "You have a slightly abnormal FWHR, indicating a facial width and midface height that do not harmonize that well. Your midface region (i.e., FWHR) likely appears overly long or overly compact. Still, this is not at the extremes.",
             "You have an abnormal FWHR, indicating a facial width and midface height that do not harmonize that well. Your midface region (i.e., FWHR) likely appears overly long or overly compact. Your ratio is beginning to stray into the extremes.",
             "You have an extremely abnormal FWHR, indicating a facial width and midface height that do not harmonize that well. Your midface region (i.e., FWHR) likely appears overly long or overly compact. Your ratio is at the extremes."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def jaw_frontal_angle_score(value, gender):
    measurement_name = "Jaw frontal angle (°)"
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
    notes = ["Your jaw has an ideal contour in the front profile, indicated by a harmonious angle in this assessment.",
             "Your jaw has a near ideal contour in the front profile, indicated by a harmonious angle in this assessment.",
             "Your jaw has a slightly unideal contour in the front profile. It may be considered either slightly too flat (high values) or steep (low values).",
             "Your jaw has a slightly unideal contour in the front profile. It may be considered either slightly too flat (high values) or steep (low values).",
             "Your jaw has an unideal contour in the front profile. It is considered either slightly too flat (high values) or steep (low values).",
             "Your jaw has an extremely unideal contour in the front profile. It is considered either slightly too flat (high values) or steep (low values).",
             "Your jaw has an extremely unideal contour in the front profile. It is considered either slightly too flat (high values) or steep (low values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def cheekbone_high_setedness_score(value, gender):
    measurement_name = "Cheekbone height (%)"
    level_count = 7
    min_range_array = [[81, 76, 70, 65, 60, 55, 10], [83, 79, 73, 68, 63, 58, 10]]
    max_range_array = [[100, 81, 76, 70, 65, 60, 55], [100, 83, 79, 73, 68, 63, 58]]
    score_array = [20, 12.5, 6.25, 3.125, -3.125, -12.5, -20]
    notes = ["You have high cheekbones, which are generally preferred when it comes to facial aesthetics.",
             "Although not incredibly high-set, you still have reasonably high cheekbones, which are generally preferred when it comes to facial aesthetics.",
             "You do not have what would be considered high cheekbones, but your cheekbones are also not low-set. They could be considered medium to perhaps ever so slightly high set.",
             "You do not have what would be considered high cheekbones, but your cheekbones are also not low-set. They could be considered medium set.",
             "You have what would be classified as low set cheekbones, where the widest part of your face is likely more towards the base of your nose rather than closer to your eyes.",
             "You have what would be classified as low set cheekbones, where the widest part of your face is likely more towards the base of your nose rather than closer to your eyes. This can lead to a droopy or melted face appearance and your face generally lacks the structure that is considered attractive.",
             "You have what would be classified as extremely low set cheekbones, where the widest part of your face is likely more towards the base of your nose rather than closer to your eyes. This can lead to a droopy or melted face appearance and your face generally lacks the structure that is considered attractive."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def total_facial_wh_ratio_score(value, gender):
    measurement_name = "Total facial height-to-width ratio"
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
    notes = ["You have an ideal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is neither too long or compact.",
             "You have a near ideal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is neither too long or compact.",
             "Although not ideal, you have a normal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is perhaps ever so slightly too long (high values) or short (low values).",
             "You have a slightly abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is perhaps slightly too long (high values) or short (low values).",
             "You have an abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is too long (high values) or short (low values).",
             "You have an extremely abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is too long (high values) or short (low values).",
             "You have an extremely abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is too long (high values) or short (low values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def bigonial_width_score(value, gender):
    measurement_name = "Bigonial width (%)"
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
    notes = ["You have an ideal jaw width. Your jaw is neither too wide or narrow relative to your total facial width.",
             "You have a near ideal jaw width. Your jaw is neither too wide or narrow relative to your total facial width.",
             "Although not ideal, you have a normal width. Your jaw may be slightly too narrow (low values) or wide (high values).",
             "You have a normal width. Your jaw may be either slightly too narrow (low values) or wide (high values), but it does not likely appear abnormal in terms of facial harmony.",
             "You have an abnormal width. Your jaw can be considered either too narrow (low values) or wide (high values).",
             "You have an abnormal width. Your jaw can be considered either too narrow (low values) or wide (high values).",
             "You have an extremely abnormal width. Your jaw can be considered either too narrow (low values) or wide (high values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def chin_philtrum_ratio_score(value, gender):
    measurement_name = "Chin to philtrum ratio"
    level_count = 6
    min_range_array = [
        [2.05, 1.87, 1.75, 1.55, 1.2, 1.0, 0.1],
        [2.0, 1.85, 1.7, 1.5, 1.2, 1.0, 0, 1],
    ]
    max_range_array = [
        [2.55, 2.73, 2.85, 3.05, 3.55, 3.85, 5.0],
        [2.5, 2.65, 2.8, 3, 3.5, 3.8, 5.0],
    ]
    score_array = [12.5, 6.25, 3.125, 1.5625, -6.25, -12.5, -25]
    notes = ["Your chin is harmoniously proportioned relative to your philtrum. This indicates that neither your chin or philtrum are too long or short.",
             "While not perfectly ideal, your chin is harmoniously proportioned relative to your philtrum. This indicates that neither your chin or philtrum are not excessively long or short.",
             "While not perfectly ideal, your chin is normally proportioned relative to your philtrum. This indicates that neither your chin or philtrum are not excessively long or short.",
             "Your chin is somewhat abnormally proportioned relative to your philtrum. This can indicate that your chin is too short (low values) or tall (high values) relative to your philtrum.",
             "Your chin is abnormally proportioned relative to your philtrum. This can indicate that your chin is too short (low values) or tall (high values) relative to your philtrum.",
             "Your chin is abnormally proportioned relative to your philtrum. This can indicate that your chin is too short (low values) or tall (high values) relative to your philtrum.",
             ""]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def neck_width_score(value, gender):
    measurement_name = "Neck Width (%)"
    level_count = 7
    min_range_array = [[90, 85, 80, 75, 70, 65, 30], [75, 69, 67, 65, 62, 57, 30]]
    max_range_array = [
        [100, 102, 105, 107, 75, 70, 130],
        [87, 93, 95, 97, 100, 103, 130],
    ]
    score_array = [10, 5, 1, -5, -10, -20, -50]
    notes = ["You have an ideal neck width that adds balance to your facial appearance.",
             "You have a near ideal neck width that adds balance to your facial appearance.",
             "Although not perfectly harmonious, you have a normal neck width.",
             "Your neck can be considered slightly too narrow (low values) or too wide (high values).",
             "Your neck can be considered too narrow (low values) or too wide (high values).",
             "Your neck can be considered extremely narrow (low values) or extremely wide (high values).",
             "Your neck can be considered extremely narrow (low values) or extremely wide (high values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def mouth_nose_width_ratio(value, gender):
    measurement_name = "Mouth width to nose width ratio"
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
    notes = ["Your mouth width harmonizes extremely well with your nose width.",
             "Your mouth width harmonizes well with your nose width.",
             "Your mouth width harmonizes reasonably well with your nose width. Your nose/mouth may be considered slightly too narrow or wide, resulting in a less than ideal proportion.",
             "Your mouth width does not harmonize that well with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion.",
             "Your mouth width does not harmonize well with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion.",
             "Your mouth width harmonizes poorly with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion.",
             "Your mouth width harmonizes extremely poorly with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def midface_ratio(value, gender):
    measurement_name = "Midface ratio"
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
    notes = ["You have a harmonious interior (or central) midface structure that is neither too compact or elongated.",
             "You have a generally harmonious interior (or central) midface structure that is neither too compact or elongated.",
             "You have a reasonably harmonious interior (or central) midface structure. It may be considered slightly too elongated (low values) or compact (high values).",
             "You have a slightly unharmonious interior (or central) midface structure. It may be considered too elongated (low values) or compact (high values).",
             "You have an unharmonious interior (or central) midface structure. It can be considered too elongated (low values) or compact (high values).",
             "You have an extremely unharmonious interior (or central) midface structure. It can be considered too elongated (low values) or compact (high values).",
             "You have an extremely unharmonious interior (or central) midface structure. It can be considered too elongated (low values) or compact (high values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def eyebrow_position_ratio_score(value, gender):
    measurement_name = "Eyebrow position ratio"
    level_count = 7
    min_range_array = [
        [0, 0.65, 0.95, 1.2, 1.5, 1.8, 2.1],
        [0.4, 0.3, 0, 1.15, 1.35, 1.85, 2.1],
    ]
    max_range_array = [
        [0.65, 0.95, 1.2, 1.5, 1.8, 2.1, 4.0],
        [0.85, 1, 1.35, 1.75, 2, 2.3, 4.0],
    ]
    score_array = [10, 5, 2.5, 0, -5, -10, -20]
    notes = ["You have an ideal positioning of your eyebrows above your eyes. A lower position is typically preferred among younger demographics. Your eyebrows could generally be considered low-set, which typically leads to a more striking appearance.",
             "You have a near ideal positioning of your eyebrows above your eyes. Your eyebrows could be considered medium-low set in the male range, and medium set in the female range.",
             "You have a normal positioning of your eyebrows above your eyes. Your eyebrows could be considered medium set in the male range, and medium-high set in the female range.",
             "You have a normal positioning of your eyebrows above your eyes. Your eyebrows could be considered slightly high set in the male range, and high set in the female range.",
             "You have a slightly abnormal positioning of your eyebrows above your eyes. Your eyebrows could be considered high set. This may lead to the appearance of a more elongated midface region.",
             "You have an unideal positioning of your eyebrows above your eyes. Your eyebrows could be considered very high set. This may lead to the appearance of a more elongated midface region.",
             "You have an unideal positioning of your eyebrows above your eyes. Your eyebrows could be considered extremely high set. This may lead to the appearance of a more elongated midface region."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def eye_spacing_ratio_score(value, gender):
    measurement_name = "Eye spacing ratio"
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
    notes = ["Your eyes have a harmonious spacing relative to one another.",
             "Your eyes have a generally harmonious spacing relative to one another.",
             "Although not ideal, your eyes have a normal spacing relative to one another. They may appear slightly close together (low values) or far apart (high values), but it is nothing extreme.",
             "Although not ideal, your eyes have a normal spacing relative to one another. They may appear somewhat close together (low values) or far apart (high values), but it is nothing extreme.",
             "Your eyes have an abnormal spacing relative to one another. They may appear either overly close together (low values) or far apart (high values).",
             "Your eyes have an extremely abnormal spacing relative to one another. They may appear either overly close together (low values) or far apart (high values).",
             "Your eyes have an extremely abnormal spacing relative to one another. They may appear either overly close together (low values) or far apart (high values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def eye_aspect_ratio_score(value, gender):
    measurement_name = "Eye aspect ratio"
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
    notes = ["Your eyes have an ideal shape in terms of their width and height. Your eyes are neither too narrow and elongated or round in shape.",
             "Your eyes have a near ideal shape in terms of their width and height. Your eyes are neither too narrow and elongated or round in shape.",
             "Your eyes have a normal shape in terms of their width and height. Your eyes may be considered either slightly too round (low values) or narrow (high values) in shape.",
             "Your eyes have a slightly abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape.",
             "Your eyes have an abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape. Overly round eyes can begin to look too beady and overly narrow one's lack the ability to display emotional cues as well. Both extremes are generally not attractive.",
             "Your eyes have an extremely abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape. Overly round eyes can begin to look too beady and overly narrow one's lack the ability to display emotional cues as well. Both extremes are generally not attractive.",
             "Your eyes have an extremely abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape. Overly round eyes can begin to look too beady and overly narrow one's lack the ability to display emotional cues as well. Both extremes are generally not attractive."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def lower_upper_lip_ratio_score(value, gender):
    measurement_name = "Lower lip to upper lip ratio"
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
    notes = ["Your lower and upper lip are ideally proportioned relative to one another.",
             "Your lower and upper lip are near ideally proportioned relative to one another.",
             "Although not ideal, your lower and upper lip are normally proportioned relative to one another. Your upper lip may be slightly too full (high values) or thin (low values) relative to your upper lip.",
             "Your lower and upper lip are slightly abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip.",
             "Your lower and upper lip are abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip.",
             "Your lower and upper lip are abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip.",
             "Your lower and upper lip are abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def deviation_IAA_score(value, gender):
    measurement_name = "Deviation of IAA(Ipsilateral alar angle) & JFA(Jaw frontal angle)"
    level_count = 6
    min_range_array = [[0, 2.5, 5, 10, 15, 20], [0, 2.5, 5, 10, 15, 20]]
    max_range_array = [[2.5, 5, 10, 15, 20, 100], [2.5, 5, 10, 15, 20, 100]]
    score_array = [7, 3.75, 1.875, 0.9375, -3.75, -7.5]
    notes = ["You have an ideal harmony between your JFA and IAA.",
             "You have a near ideal harmony between your JFA and IAA.",
             "You have a normal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info.",
             "You have a normal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info.",
             "You have an abnormal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info.",
             "You have an extremely abnormal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def eyebrow_tilt_score(value, gender):
    measurement_name = "Eyebrow tilt"
    level_count = 6
    min_range_array = [[5, 3, 0, -2, -4, -15], [11, 9, 6, 4, 2, -15]]
    max_range_array = [[13, 15, 18, 20, 22, 40], [18.7, 20.7, 23.7, 25.7, 27.7, 40]]
    score_array = [6, 3, 1.5, -3, -6, -12]
    notes = ["Your eyebrows have an ideal tilt. They are neither too upturned or droopy when accounting for inter-sex variability.",
             "Your eyebrows have a near ideal tilt. They are neither too upturned or droopy when accounting for inter-sex variability.",
             "Although not ideal, your eyebrows have a normal tilt. They may be considered slightly too upturned (high values) or droopy (low values) when accounting for inter-sex variability.",
             "Your eyebrows have a slightly abnormal tilt. They may be considered too upturned (high values) or droopy (low values) when accounting for inter-sex variability.",
             "Your eyebrows have an abnormal tilt. They may be considered too upturned (high values) or droopy (low values) when accounting for inter-sex variability.",
             "Your eyebrows have an extermely abnormal tilt. They may be considered too upturned (high values) or droopy (low values) when accounting for inter-sex variability."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def bitemporal_width_score(value, gender):
    measurement_name = "Bitemporal width"
    level_count = 7
    min_range_array = [[84, 82, 79, 77, 74, 71, 50], [79, 76, 73, 70, 67, 65, 50]]
    max_range_array = [
        [95, 97, 100, 102, 105, 108, 125],
        [92, 95, 98, 101, 104, 106, 125],
    ]
    score_array = [5, 2.5, 1.25, -2.5, -5, -10, -15]
    notes = ["Your forehead has an ideal width relative to your cheekbones. Your forehead is neither too narrow nor wide.",
             "Your forehead has a near ideal width relative to your cheekbones. Your forehead is neither too narrow nor wide.",
             "Although not ideal, your forehead has a normal width relative to your cheekbones. Your forehead may be considered either slightly too wide (high values) or narrow (low values).",
             "Your forehead has a slightly abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values).",
             "Your forehead has an abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values).",
             "Your forehead has an extremely abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values).",
             "Your forehead has an extremely abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def lower_third_proporation_score(value, gender):
    measurement_name = "Lower third proportion"
    level_count = 6
    min_range_array = [
        [30.6, 29.6, 28.4, 27.2, 26.6, 20],
        [31.2, 30.2, 29.2, 28.2, 27.2, 20],
    ]
    max_range_array = [[34, 35, 36.2, 37.4, 38, 45], [34.5, 35.5, 36.5, 37.5, 38.5, 45]]
    score_array = [5, 2.5, 1.25, -2.5, -5, -10]
    notes = ["Your lower third has a harmonious spacing between its features.",
             "Your lower third has a harmonious spacing between its features.",
             "Although not ideal, your lower third has a normal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either slightly too short (low values) or long (high values) relative to the lower portion (chin/lower lip).",
             "Your lower third has a slightly abnormal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either too short (low values) or long (high values) relative to the lower portion (chin/lower lip).",
             "Your lower third has an abnormal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either too short (low values) or long (high values) relative to the lower portion (chin/lower lip).",
             "Your lower third has an extremely abnormal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either too short (low values) or long (high values) relative to the lower portion (chin/lower lip)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def lpsilateral_alar_angle_score(value, gender):
    measurement_name = "Ipsilateral alar angle"
    level_count = 7
    min_range_array = [[84, 82, 79, 77, 75, 73, 50], [84, 82, 79, 77, 75, 73, 50]]
    max_range_array = [
        [95, 97, 100, 102, 104, 106, 150],
        [95.5, 97.5, 100.5, 102.5, 104.5, 106.5, 150],
    ]
    score_array = [2.5, 1.25, 0.63, 0, -1.25, -2.5, -5]
    notes = ["Your midface structure retains a harmonious balance.",
             "Your midface structure retains a harmonious balance.",
             "Although not perfectly ideal, your midface structure retains a normal balance. Your angle may indicate a slightly elongated nasal region and close set eyes (low values). Or, it may indicate a slightly short nose and wide set eyes (high values).",
             "Although not perfectly ideal, your midface structure retains a normal balance. Your angle may indicate a slightly elongated nasal region and close set eyes (low values). Or, it may indicate a slightly short nose and wide set eyes (high values).",
             "Your midface structure lacks balance. Your angle may indicate an elongated nasal region and close set eyes (low values). Or, it may indicate a short nose and wide set eyes (high values).",
             "Your midface structure lacks balance. Your angle may indicate an extremely elongated nasal region and close set eyes (low values). Or, it may indicate a short nose and wide set eyes (high values).",
             "Your midface structure lacks balance. Your angle may indicate an extremely elongated nasal region and close set eyes (low values). Or, it may indicate a short nose and wide set eyes (high values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def medial_canthal_angle(value, gender):
    measurement_name = "Medial canthal angle"
    level_count = 7
    min_range_array = [[29, 25, 21, 18, 15, 10, 5], [33, 29, 22, 19, 16, 13, 5]]
    max_range_array = [[47, 51, 57, 63, 69, 75, 120], [51, 55, 61, 65, 71, 77, 120]]
    score_array = [10, 5, 2.5, -2.5, -5, -10, -15]
    notes = ["The inner corner of your eye is harmonious. It has distinct shape and angularity, while not being overly angular.",
             "The inner corner of your eye is generally harmonious. It has distinct shape and angularity, while not being overly angular.",
             "The inner corner of your eye is somewhat harmonious. It may either lack some distinct angularity (high values) or be overly sharp (low values).",
             "The inner corner of your eye is somewhat disharmonious. It may either lack some distinct angularity (high values) or be overly sharp (low values).",
             "The inner corner of your eye is  disharmonious. It either lacks some distinct angularity (high values) or is overly sharp (low values).",
             "The inner corner of your eye is very disharmonious. It either lacks some distinct angularity (high values) or is overly sharp (low values).",
             "The inner corner of your eye is extremely disharmonious. It either lacks some distinct angularity (high values) or is overly sharp (low values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

def eye_separation_ratio_score(value, gender):
    measurement_name = "Eye separation ratio"
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
    notes = ["Your eyes are harmoniously spaced relative to your facial width.",
             "While not perfectly ideal, your eyes are generally harmoniously spaced relative to your facial width.",
             "While not perfectly ideal, your eyes are still normally spaced relative to your facial width. They may begin to appear either slightly close set (low values) or wide set (high values).",
             "Your eyes have a slightly abnormal spacing relative to your facial width. They may begin to appear either close set (low values) or wide set (high values).",
             "Your eyes have a moderately abnormal spacing relative to your facial width. They may begin to appear either too close set (low values) or wide set (high values).",
             "Your eyes have an abnormal spacing relative to your facial width. They appear either too close set (low values) or wide set (high values).",
             "Your eyes have an extremely abnormal spacing relative to your facial width. They appear either too close set (low values) or wide set (high values)."]
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i]
            and value <= max_range_array[1 - gender][i]
        ):
            return score_array[i], notes[i], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name
    return score_array[-1], notes[-1], score_array[0], [min_range_array[1-gender][0], max_range_array[1 - gender][0]], value, measurement_name

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

    scores = []
    notes = []
    max_scores = []
    ranges = []
    current_values = []
    measurement_names = []

    temp_sum, note, max_score, range, current_value, measurement_name = gonial_angle_score(gonialAngle, gender)
    print("Gonial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = nasofrontal_angle_score(nasofrontalAngle, gender)
    print("Nasofrontal angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = mandibular_plane_angle_score(mandibularPlaneAngle, gender)
    print("Mandibular plane angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = ramus_mandible_ratio_score(ramus2MandibleRatio, gender)
    print("Ramus mandible ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = facial_convexity_glabella_score(facialConvexityGlabella, gender)
    print("Facial convexity glabella score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = submental_cervical_angle_score(submentalCervicalAngle, gender)
    print("Submental cervical angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = nasofacial_angle_score(nasofacialAngle, gender)
    print("Nasofacial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = nasolabial_angle_score(nasolabialAngle, gender)
    print("Nasolabial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = orbital_vector_score(orbitalVector, gender)
    print("Orbital vector score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = total_facial_convexity_score(totalFacialConvexity, gender)
    print("Total facial convexity score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = mentolabial_angle_score(mentolabialAngle, gender)
    print("Mentolabial angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = facial_convexity_nasion_score(facialConvexityNasion, gender)
    print("Facial convexity nasion score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = nasal_projection_score(nasalProjection, gender)
    print("Nasal Projection score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = nasal_wh_ratio_score(nasalW2HRatio, gender)
    print("Nasal W to H ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = ricketts_E_line_score(rickettsELine, gender)
    print("Ricketts E line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = holdaway_H_line_score(holdawayHLine, gender)
    print("Holdaway H line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = steiner_S_line_score(steinerSLine, gender)
    print("Steiner S line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = burstone_line_score(burstoneLine, gender)
    print("Burstone line score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = nasomental_angle_score(nasomentalAngle, gender)
    print("Nasomental angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = gonion_mouth_relationship_score(gonion2MouthRelationship, gender)
    print("Gonion, mouth relationship score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = recession_relative_frankfort_plane_score(recessionRelative2FrankfortPlane, gender)
    print("Recession relative frankfort plane score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = browridge_inclination_angle_score(browridgeInclinationAngle, gender)
    print("Browridge inclination angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = nasal_tip_angle_score(nasalTipAngle, gender)
    print("Nasal tip angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    print("Total Side Profile score is ", sum)
    print(
        "Total side profile percentage is ",
        sum / SIDE_PROFILE_TOTAL_SCORE_MAX * 100,
        "%",
    )
    return sum, sum / SIDE_PROFILE_TOTAL_SCORE_MAX * 100, scores, notes, max_scores, ranges, current_values, measurement_names

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

    scores = []
    notes = []
    max_scores = []
    ranges = []
    current_values = []
    measurement_names = []

    print(gender, eyeSeparationRatio)
    print(type(gender), type(eyeSeparationRatio))

    temp_sum, note, max_score, range, current_value, measurement_name = eye_separation_ratio_score(eyeSeparationRatio, gender)
    print("Eye separation ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = facial_thirds_score(facialThirds, gender)
    print("Facial thirds score is ", temp_sum, facialThirds, gender)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = lateral_canthal_tilt_score(lateralCanthalTilt, gender)
    print("Lateral canthal tilt score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = facial_wh_ratio_score(facialWHRatio, gender)
    print("Facial width-to-height ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = jaw_frontal_angle_score(jawFrontalAngle, gender)
    print("Jaw frontal angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = cheekbone_high_setedness_score(cheekBoneHeight, gender)
    print("Cheekbone high setedness score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = total_facial_wh_ratio_score(totalFacialWHRatio, gender)
    print("Total face width-to-height ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = bigonial_width_score(bigonialWidth, gender)
    print("Bigonial width score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = chin_philtrum_ratio_score(chin2PhiltrumRatio, gender)
    print("Chin philtrum ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = neck_width_score(neckWidth, gender)
    print("Neck width score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = mouth_nose_width_ratio(mouthWidth2NoseWidthRatio, gender)
    print("Mouth, nose width ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = midface_ratio(midFaceRatio, gender)
    print("Midface ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = eyebrow_position_ratio_score(eyebrowPositionRatio, gender)
    print("Eyebrow position ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = eye_spacing_ratio_score(eyeSpacingRatio, gender)
    print("Eye spacing ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = eye_aspect_ratio_score(eyeAspectRatio, gender)
    print("Eye aspect ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = lower_upper_lip_ratio_score(lowerLip2UpperLipRatio, gender)
    print("Lower, upper lip ratio score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = deviation_IAA_score(deviationOfJFA2IAA, gender)
    print("Deviation IAA score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = eyebrow_tilt_score(eyebrowTilt, gender)
    print("Eyebrow tilt score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = bitemporal_width_score(bitemporalWidth, gender)
    print("Bitemporal width score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = lower_third_proporation_score(lowerThirdProporation, gender)
    print("Lower third proporation score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = lpsilateral_alar_angle_score(ipsilateralAlarAngle, gender)
    print("Lpsilateral alar angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    temp_sum, note, max_score, range, current_value, measurement_name = medial_canthal_angle(medialCanthalAngle, gender)
    print("Medial canthal angle score is ", temp_sum)
    scores.append(temp_sum)
    notes.append(note)
    max_scores.append(max_score)
    ranges.append(range)
    current_values.append(current_value)
    measurement_names.append(measurement_name)
    sum = sum + temp_sum

    print("Front profile score is ", sum)
    print(
        "Total front profile percentage is ",
        sum / FRONT_PROFILE_TOTAL_SCORE_MAX * 100,
        "%",
    )
    return sum, sum / FRONT_PROFILE_TOTAL_SCORE_MAX * 100, scores, note, max_scores, ranges, current_values, measurement_names


@app.post("/getfrontmark")
def get_front_mark(
    body: GetFrontMarkRequestSchema,
):
    print(body)
    # print (body.bigonialWidth)
    mark, percentage, scores, notes, max_scores, ranges, current_values, measurement_names = front_input(**body.dict())
    print(mark, percentage, scores, notes)
    return {"mark": mark, "percent": percentage, "scores": scores, "notes": notes, "max_scores": max_scores, "ranges": ranges, "current_values": current_values,
            "measurement_names": measurement_names}


@app.post("/getsidemark")
def get_side_mark(
    body: GetSideMarkRequestSchema,
):
    print(body)
    # print (body.bigonialWidth)
    mark, percentage, scores, notes, max_scores, ranges, current_values, measurement_names = side_input(**body.dict())
    return {"mark": mark, "percent": percentage, "scores": scores, "notes": notes, "max_scores": max_scores, "ranges": ranges, "current_values": current_values,
            "measurement_names": measurement_names}

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

    return {"message": "Image uploaded successfully",
            "points": result_points.tolist()}

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

    result_points = side_landmarks.process_image(file_path)
    print(result_points)

    return {"message": "Image uploaded successfully",
            "points": result_points}
