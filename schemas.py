from typing import Optional, List, Any
from pydantic import BaseModel, Field
import math
from PIL import ImageDraw, ImageFont


class frontProfileSchema(BaseModel):
    gender: int
    racial: str
    eyeSeparationRatio: float = Field(round=2)
    facialThirds: List[float]
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
    
class UserSchema(BaseModel):
    name: Optional[str] = None
    mail: str
    pswd: str

class PremiumSchema:
    mail: str
    plan: int
    def __init__(self, mail, plan):
        self.mail = mail
        self.plan = plan

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __init__(self, src):
        self.x = src["x"]
        self.y = src["y"]

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x+other.x, self.y+other.y)
        else:
            return TypeError("Unsupported operand type(s) for +: 'Point' and '{}'".format(type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x-other.x, self.y-other.y)
        else:
            return TypeError("Unsupported operand type(s) for -: 'Point' and '{}'".format(type(other).__name__))
      
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Cannot divide by zero")
            return Point(self.x/other, self.y/other)
        else:
            return TypeError("Unsupported operand type(s) for /: 'Point' and '{}'".format(type(other).__name__))
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x*other, self.y*other)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'Point' and '{type(other).__name__}'")

    def getVector(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def transform(self, ZERO, srcWidth, tarWidth):
        return (self - ZERO) * tarWidth / srcWidth
    
    def drawPoint(self, draw):
        R = 3
        draw.ellipse((self.x-R, self.y-R, self.x+R, self.y+R))

    def drawLetter(self, draw, str):
        R= 10
        FONT_SIZE = 20
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE)
        draw.text((self.x-R, self.y-R), str, font=font, fill = (0,0,0))

class Line:
    def __init__(self, head:Point, tail:Point):
        self.head = head
        self.tail = tail

    def getLength(self):
        return (self.tail - self.head).getVector()
    
    def drawPoints(self, draw):
        self.head.drawPoint(draw)
        self.tail.drawPoint(draw)

    def drawLine(self, draw):
        draw.line(self.line(), fill=(0, 255, 0), width = 1)
    
    def drawLetter(self, draw, str):
        center = (self.head + self.tail) / 2
        center.drawLetter(draw, str)
        
    def drawStrLine(self, draw, str):
        self.drawLine(draw)
        self.drawPoints(draw)
        self.drawLetter(draw, str)
    
    def line(self):
        return (self.head.x, self.head.y, self.tail.x, self.tail.y)
class Rect:
    def __init__(self, leftTop:Point, rightBottom:Point):
        self.leftTop = leftTop
        self.rightBottom = rightBottom
        self.center = (leftTop+rightBottom) / 2

    def __init__(self, Xs:[], Ys:[]):
        self.leftTop = Point(min(Xs), min(Ys))
        self.rightBottom = Point(max(Xs), max(Ys))
        self.center = (self.leftTop + self.rightBottom) / 2

    def __init__(self, center:Point, radius):
        self.leftTop = center - Point(radius, radius)
        self.rightBottom = center + Point(radius, radius)
        self.center = center

    def __init__(self, pts):
        Xs = []
        Ys = []
        for pt in pts:
            Xs.append(pt.x)
            Ys.append(pt.y)
        self = Rect(Xs, Ys)

    def area(self):
        return (self.leftTop.x, self.leftTop.y, self.rightBottom.x, self.rightBottom.y)
    
    def getContainRect(self):       
        return Rect(self.center, self.getRadius())
    
    def getRadius(self):
        return Line(self.leftTop, self.rightBottom).getLength() / 2
    
    def getContainArea(self):
        return self.getContainRect.area()
    
    def getEdgeLength(self):
        return self.rightBottom.x - self.leftTop.x
    
    def transformPts(self, pts, TARGET_EDGE_LENGTH):
        currentEdgeLength = self.getEdgeLength()
        resPts = []
        for pt in pts:
            resPts.append(pt.transform(self.leftTop, currentEdgeLength, TARGET_EDGE_LENGTH))
        
        return resPts

class ImageOverviewSchema(BaseModel):
    ID: str
    front: str
    side: str
    points: List[Any]