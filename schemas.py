from typing import List
from pydantic import BaseModel, Field


class frontProfileSchema(BaseModel):
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

class sideProfileSchema(BaseModel):
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

class MeasurementOverview:
    name = ""
    score = 0
    max = 0
    value = 0
    range = ""
    note = ""
    advice = ""
    def __init__(self, name, score, max, value, range, note, advice) -> None:
        self.name = name
        self.score = score
        self.max = max
        self.value = value
        self.range = range
        self.note = note
        self.advice = advice

class profileResponseSchema:
    score = 0.0
    detailScores = []
    notes = []
    maxScores = []
    idealRanges = []
    measureNames = []
    advices = []

    def update(self, overview:MeasurementOverview):
        self.score = self.score + overview.score
        self.detailScores.append(overview.score)
        self.notes.append(overview.note)
        self.maxScores.append(overview.max)
        self.idealRanges.append(overview.range)
        self.advice.append(overview.advice)

    def result(self):
        resp = {
            "score" : self.score,
            "scores" : self.detailScores,
            "notes" : self.notes,
            "maxs" : self.maxScores,
            "ranges" : self.idealRanges,
            "names" : self.measureNames,
            "advices" : self.advices
        }
        return resp