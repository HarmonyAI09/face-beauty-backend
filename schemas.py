from typing import List
from pydantic import BaseModel, Field


class GetFrontMarkRequestSchema(BaseModel):
    gender: int
    eyeSeparationRatio: float
    facialThirds: list
    lateralCanthalTilt: float
    facialWHRatio: float
    jawFrontalAngle: float
    cheekBoneHeight: float
    totalFacialWHRatio: float
    bigonialWidth: float
    chin2PhiltrumRatio: float
    neckWidth: float
    mouthWidth2NoseWidthRatio: float
    midFaceRatio: float
    eyebrowPositionRatio: float
    eyeSpacingRatio: float
    eyeAspectRatio: float
    lowerLip2UpperLipRatio: float
    ipsilateralAlarAngle: float
    deviationOfJFA2IAA: float
    eyebrowTilt: float
    bitemporalWidth: float
    lowerThirdProporation: float
    medialCanthalAngle: float


class GetSideMarkRequestSchema(BaseModel):
    gender: int
    gonialAngle: float
    nasofrontalAngle: float
    mandibularPlaneAngle: float
    ramus2MandibleRatio: float
    facialConvexityGlabella: float
    submentalCervicalAngle: float
    nasofacialAngle: float
    nasolabialAngle: float
    orbitalVector: str
    totalFacialConvexity: float
    mentolabialAngle: float
    facialConvexityNasion: float
    nasalProjection: float
    nasalW2HRatio: float
    rickettsELine: str
    holdawayHLine: str
    steinerSLine: str
    burstoneLine: str
    nasomentalAngle: float
    gonion2MouthRelationship: str
    recessionRelative2FrankfortPlane: str
    browridgeInclinationAngle: float
    nasalTipAngle: float
