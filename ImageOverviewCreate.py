from schemas import ImageOverviewSchema, Point, Rect, Line
from PIL import Image, ImageDraw

DEFAULT_LENGTH = 800
TARGET_EDGE_LENGTH = 300
BLACK = (0,0,0)


def ctEyeSeparationRatioImg(p:ImageOverviewSchema, index):
    img = Image.open(p.front)
    x_offset = (DEFAULT_LENGTH - img.width) // 2
    y_offset = (DEFAULT_LENGTH - img.height) // 2

    canva = Image.new('RGB', (DEFAULT_LENGTH, DEFAULT_LENGTH), BLACK)
    canva.paste(img, (x_offset, y_offset))

    pts = []
    pts.append(Point(p.points[12][0]))
    pts.append(Point(p.points[12][1]))
    pts.append(Point(p.points[17][0]))
    pts.append(Point(p.points[12][1]))

    cropArea = Rect(pts).getContainRect()
    cropImg = canva.crop(cropArea.area())
    cropImg = cropImg.resize((TARGET_EDGE_LENGTH, TARGET_EDGE_LENGTH))
    pts = cropArea.transformPts(pts, TARGET_EDGE_LENGTH)

    draw = ImageDraw.Draw(cropImg)

    Line(pts[0], pts[1]).drawStrLine(draw, "A")
    Line(pts[2], pts[3]).drawStrLine(draw, "B")
    





def mainProcess(profile:ImageOverviewSchema):
    ctEyeSeparationRatioImg(profile, 1)
    return True