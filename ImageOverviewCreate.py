from schemas import ImageOverviewSchema, Point, Rect, Line
from PIL import Image, ImageDraw
import os

DEFAULT_LENGTH = 800
TARGET_EDGE_LENGTH = 300
BLACK = (0,0,0)
DIR = "./REPORTS/"


def createImage(index, p:ImageOverviewSchema, idxPts:[], idxNumSegs:[], idxDenSegs:[], idxSolidSegs:[],
                idxHzLines:[], idxVtLines:[], idxDotSegs:[], idxDotLines:[], idxCrossSegs:[], idxSolidLines:[],
                idxP2PHIdxABs:[], idxL2pHzs:[], idxP2LSegs:[], idxP2PVIdxABs):
    #ptsIndex : Point Indexes , [[12, 0], [12, 1], [17, 0], [17, 1]]
    img = Image.open(p.front)
    x_offset = (DEFAULT_LENGTH - img.width) // 2
    y_offset = (DEFAULT_LENGTH - img.height) // 2

    canva = Image.new('RGB', (DEFAULT_LENGTH, DEFAULT_LENGTH), BLACK)
    canva.paste(img, (x_offset, y_offset))

    pts = []
    for idxPt in idxPts:
        pts.append(Point(p.points[idxPt[0]][idxPt[1]]))

    cropArea = Rect(pts).getContainRect()
    cropImg = canva.crop(cropArea.area())
    cropImg = cropImg.resize((TARGET_EDGE_LENGTH, TARGET_EDGE_LENGTH))
    pts = cropArea.transformPts(pts, TARGET_EDGE_LENGTH)

    draw = ImageDraw.Draw(cropImg)
    
    for idx in idxNumSegs:
        Line(pts[idx[0]], pts[idx[1]]).drawAsNumeratorSegment()
    for idx in idxDenSegs:
        Line(pts[idx[0]], pts[idx[1]]).drawAsDenominatorSegment()
    for idx in idxSolidSegs:
        Line(pts[idx[0]], pts[idx[1]]).drawAsSolidSegment()
    for idx in idxDotSegs:
        Line(pts[idx[0]], pts[idx[1]]).drawAsDottedSegment()
    for idx in idxDotLines:
        Line(pts[idx[0]], pts[idx[1]]).drawAsDottedLine()    
    for idx in idxHzLines:
        Point(pts[idx]).drawAsHorizontalLine()
    for idx in idxVtLines:
        Point(pts[idx]).drawAsVerticalLine()
    for idx in idxCrossSegs:
        Line(pts[idx[0][0]], pts[idx[0][1]]).drawAsCrossSegment(Line(pts[idx[1][0]], pts[idx[1][1]]))
    for idx in idxSolidLines:
        Line(pts[idx[0]], pts[idx[1]]).drawAsSolidLine()    
    for idx in idxP2PHIdxABs:
        pts[idx[0][0]].drawAsNumeratorSegment_HZ(pts[idx[0][1]])
        pts[idx[1][0]].drawAsDenominatorSegment_HZ(pts[idx[1][1]])
    for idx in idxL2pHzs:
        Line(pts[idx[0]], pts[idx[1]]).drawAsNumeratorSegment()
        ((pts[idx[0]] + pts[idx[1]]) / 2).drawAsDenominatorSegment_HZ()
    
    for pt in pts:
        pt.drawPoint(draw)

    cropImg.save(os.path.join(DIR, f"{p.ID}/{index}.jpg"))
    return True

def drawEyeSeparationRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[12, 0], [12, 1], [17, 0], [17, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawFacialThirds(index, p:ImageOverviewSchema):
    ptsIdxs = [[1, 0], [5, 0], [19, 0], [29, 0]]
    solidSegIdxs = [[0, 1], [1, 2], [2, 3]]
    hzLineIdxs = [0, 1, 2, 3]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs, idxHzLines=hzLineIdxs)

def drawLateralCanthalTilt(index, p:ImageOverviewSchema):
    ptsIdxs = [[11, 0], [16, 0], [16, 1], [11, 1]]
    dotSegIdxs = [[0, 1], [1, 2]]
    dotLineIdxs = [[1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxDotSegs=dotSegIdxs, idxDotLines=dotLineIdxs)

def drawFacialWidthHeight(index, p:ImageOverviewSchema):
    ptsIdxs = [[6, 0], [21, 0], [17, 0], [17, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    hzLineIdxs = [1]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs, idxHzLines=hzLineIdxs)

def drawJawFrontalAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[26, 0], [28, 0], [28, 1], [26, 1]]
    crossSegIdxs = [[[0, 1], [2, 3]]]
    createImage(index, p, idxPts=ptsIdxs, idxCrossSegs=crossSegIdxs)

def drawCheekboneHeight(index, p:ImageOverviewSchema):
    ptsIdxs = [[12, 0], [12, 1], [17, 0], [17, 1], [21, 0]]
    solidSegIdxs = [[0, 1], [2, 3]]
    p2pHIdxsAB = [[[0, 4], [2, 4]]]
    hzLineIdxs = [4]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs, idxHzLines=hzLineIdxs, idxP2PHIdxAB = p2pHIdxsAB)

def drawTotalfaceHeightWidth(index, p:ImageOverviewSchema):
    ptsIdxs = [[1, 0], [29, 1], [17, 0], [17, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawBigonialWidth(index, p:ImageOverviewSchema):
    ptsIdxs = [[17, 0], [17, 1], [22, 0], [22, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawChinPhiltrumRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[20, 0], [21, 1], [25, 0], [29, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawNeckWidth(index, p:ImageOverviewSchema):
    ptsIdxs = [[22, 0], [22, 1], [27, 0], [27, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawMouthWidthNoseWidthRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[18, 0], [18, 1], [23, 0], [23, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawMidfaceRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[12, 0], [12, 1], [21, 0]]
    hzLineIdxs = [2]
    l2pHzIdxs = [[0, 1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxHzLines=hzLineIdxs, idxL2pHzs=l2pHzIdxs)

def drawEyebrowPositionRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[10, 0], [14, 0], [12, 0], [12, 1], [8, 0], [8, 1], [10, 1], [14, 1]]
    denIdxs = [[0, 1], [6, 7]]
    solidSegIdxs = [[2, 3]]
    p2LDotSegIdxs = [[4, 2, 3], [5, 2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxDenSegs=denIdxs, idxSolidSegs=solidSegIdxs, idxP2LSegs=p2LDotSegIdxs)

def drawEyeSpacingRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[11, 0], [16, 0], [16, 1], [9, 1]]
    vtLineIdxs = [0, 1, 2, 3]
    numIdxs = [[1, 2]]
    p2pVtIdxs = [[1, 0], [2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxVtLines=vtLineIdxs, idxNumSegs=numIdxs, idxP2PVIdxABs=p2pVtIdxs)

def drawEyeAspectRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[10, 1], [14, 1], [16, 1], [11, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawLowerLipUpplerLipRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[21, 0], [24, 0], [25, 0]]
    numIdxs = [[0, 1]]
    denIdxs = [[1, 2]]
    hzLineIdxs = [0]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs, idxHzLines=hzLineIdxs)

def drawDeviationIAA(index, p:ImageOverviewSchema):
    ptsIdxs = [[11, 0], [11, 1], [19, 0], [26, 0], [26, 1], [28, 0], [28, 1]]
    solidSegIdxs = [[0, 2], [1, 2]]
    crossSegIdxs = [[[3, 4], [5, 6]]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs, idxCrossSegs=crossSegIdxs)

def drawEyebrowTilt(index, p:ImageOverviewSchema):
    ptsIdxs = [[7, 1], [4, 1]]
    solidSegIdxs = [[0, 1]]
    hzLineIdxs = [0]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs, idxHzLines=hzLineIdxs)

def drawBitemporalWidth(index, p:ImageOverviewSchema):
    ptsIdxs = [[2, 0], [2, 1], [17, 0], [17, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawLowerThirdProporation(index, p:ImageOverviewSchema):
    ptsIdxs = [[19, 0], [24, 0], [29, 0]]
    hzLineIdxs = [0, 1, 2]
    numIdxs = [[0, 1]]
    denIdxs = [[0, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxHzLines=hzLineIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawIpsilateralAlarAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[9, 0], [9, 1], [19, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawMedialCanthanAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[16, 1], [13, 1], [15, 1]]
    solidSegIdxs = [[0, 1], [0, 2]]
    createImage(index, p, idx=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawGonialAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[38, 0], [49, 0], [52, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawNasofrontalAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[32, 0], [35, 0], [39, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawMandibularPlanAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[47, 0], [49, 0], [52, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawRamusMandibleRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[38, 0], [49, 0], [54, 0]]
    numIdxs = [[0, 1]]
    denIdxs = [[1, 2]]
    vtLineIdxs = [2]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs, idxVtLines=vtLineIdxs)

def drawFacialConvexityGlabella(index,p:ImageOverviewSchema ):
    ptsIdxs = [[32, 0], [43, 0], [50, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawSubmentalCervicalAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[51, 0], [53, 0], [55, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawNasofacialAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[39, 0], [35, 0], [50, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawNasolabialAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[41, 0], [44, 0], [45, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawOrbitalVector(index, p:ImageOverviewSchema):
    ptsIdxs = [[33, 0], [38, 0], [36, 0], [37, 0], [57, 0]]
    vtLineIdxs = [0]
    hzLineIdxs = [1]
    createImage(index, p, idxPts=ptsIdxs, idxHzLines=hzLineIdxs, idxVtLines=vtLineIdxs)

def drawTotalFacialHWRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[1, 0], [29, 1], [17, 0], [17, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawBigonialWidth(index, p:ImageOverviewSchema):
    ptsIdxs = [[17, 0], [17, 1], [22, 0], [22, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawChinPhiltrunRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[20, 0], [21, 1], [25, 0], [29, 1]]
    numIdxs = [[0, 1]]
    denIdxs = [[2, 3]]
    createImage(index, p, idxPts=ptsIdxs, idxNumSegs=numIdxs, idxDenSegs=denIdxs)

def drawTotalFacialConvexity(index, p:ImageOverviewSchema):
    ptsIdxs = [[32, 0], [40, 0], [50, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawMentolabialAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[58, 0], [48, 0], [50, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawFacialConvexityNasion(index, p:ImageOverviewSchema):
    ptsIndex = [[35, 0], [43, 0], [50, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIndex, idxSolidSegs=solidSegIdxs)

def drawNasalProjection(index, p:ImageOverviewSchema):
    ptsIdxs = [[40, 0], [36, 0], [35, 0], [42, 0]]
    solidSegIdxs = [[0, 1], [1, 4]]
    hzLineIdxs = [1, ]
    vtLineIdxs = [0, 3]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs, idxHzLines=hzLineIdxs, idxVtLines=vtLineIdxs)

def drawNasalWHRatio(index, p:ImageOverviewSchema):
    ptsIdxs = [[33, 0], [40, 0], [42, 0], [36, 0], [56, 0]]
    solidSegIdxs = [[0, 1], [1, 4]]
    hzLineIdxs = [1, ]
    vtLineIdxs = [0, 3]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs, idxHzLines=hzLineIdxs, idxVtLines=vtLineIdxs)
    

def drawRickettsELine(index, p:ImageOverviewSchema):
    ptsIdxs = [[40, 0], [50, 0]]
    solidSegIdxs = [[0, 1]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawHoldawayHLine(index, p:ImageOverviewSchema):
    ptsIdxs = [[45, 0], [50, 0]]
    solidSegIdxs = [[0, 1]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawSteinerSLine(index, p:ImageOverviewSchema):
    ptsIdxs = [[59, 0], [50, 0]]
    solidSegIdxs = [[0, 1]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawCreateBurstoneLine(index, p:ImageOverviewSchema):
    ptsIdxs = [[43, 0], [50, 0]]
    solidSegIdxs = [[0, 1]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawNasomentalAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[35, 0], [40, 0], [50, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidLines=solidSegIdxs)

def drawGonionMouthRelationship(index, p:ImageOverviewSchema):
    ptsIdxs = [[47, 0], [49, 0]]
    solidSegIdxs = [[0, 1]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def drawRecessionRelativeFrankfortPlane(index, p:ImageOverviewSchema):
    ptsIdxs = [[35, 0], [54, 0]]
    solidLineIdxs = [[0, 1]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidLines=solidLineIdxs)

def drawBrowridgeInclinationAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[32, 0], [31, 0]]
    solidSegIdxs = [[0, 1]]
    vtLineIdxs = [0]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs, idxVtLines=vtLineIdxs)

def drawNasalTipAngle(index, p:ImageOverviewSchema):
    ptsIdxs = [[36, 0], [40, 0], [41, 0]]
    solidSegIdxs = [[0, 1], [1, 2]]
    createImage(index, p, idxPts=ptsIdxs, idxSolidSegs=solidSegIdxs)

def mainProcess(profile:ImageOverviewSchema):
    return True