from typing import List
from pydantic import BaseModel, Field


class GetFrontMarkRequestSchema(BaseModel):
    gender: int
    racial: str
    eyeSeparationRatio: float = Field(round=2)
    facialThirds: list
    lateralCanthalTilt: float = Field(round=2)
    facialWHRatio: float = Field(round=2)
    jawFrontalAngle: float = Field(round=2)
    cheekBoneHeight: float = Field(round=2)
    totalFacialWHRatio: float = Field(round=2)
    bigonialWidth: float = Field(round=2)
    chin2PhiltrumRatio: float = Field(round=2)
    neckWidth: float = Field(round=2)
    mouthWidth2NoseWidthRatio: float = Field(round=2)
    midFaceRatio: float = Field(round=2)
    eyebrowPositionRatio: float = Field(round=2)
    eyeSpacingRatio: float = Field(round=2)
    eyeAspectRatio: float = Field(round=2)
    lowerLip2UpperLipRatio: float = Field(round=2)
    ipsilateralAlarAngle: float = Field(round=2)
    deviationOfJFA2IAA: float = Field(round=2)
    eyebrowTilt: float = Field(round=2)
    bitemporalWidth: float = Field(round=2)
    lowerThirdProporation: float = Field(round=2)
    medialCanthalAngle: float = Field(round=2)


class GetSideMarkRequestSchema(BaseModel):
    gender: int
    racial: str
    gonialAngle: float = Field(round=2)
    nasofrontalAngle: float = Field(round=2)
    mandibularPlaneAngle: float = Field(round=2)
    ramus2MandibleRatio: float = Field(round=2)
    facialConvexityGlabella: float = Field(round=2)
    submentalCervicalAngle: float = Field(round=2)
    nasofacialAngle: float = Field(round=2)
    nasolabialAngle: float = Field(round=2)
    orbitalVector: str
    totalFacialConvexity: float = Field(round=2)
    mentolabialAngle: float = Field(round=2)
    facialConvexityNasion: float = Field(round=2)
    nasalProjection: float = Field(round=2)
    nasalW2HRatio: float = Field(round=2)
    rickettsELine: str
    holdawayHLine: str
    steinerSLine: str
    burstoneLine: str
    nasomentalAngle: float = Field(round=2)
    gonion2MouthRelationship: str
    recessionRelative2FrankfortPlane: str
    browridgeInclinationAngle: float = Field(round=2)
    nasalTipAngle: float = Field(round=2)
