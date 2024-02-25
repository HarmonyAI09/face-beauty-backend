from PIL import Image, ImageDraw
from app.services.geo_service import getBR, getCenter, getDistance, getIntersection, getParallel, getRectArea, getTL, getVertical

ZERO = 0.0001

def RemakePointArrayBaseOnImgSize(url, points):
    img = Image.open(url)
    SRC_LENGTH = 800
    TARGET_LENGTH = max(img.height, img.width)
    res_points = []
    for couple in points:
        res_couple = []
        for point in couple:
            src_x = point["x"]
            src_y = point["y"]
            target_x = src_x * TARGET_LENGTH / SRC_LENGTH
            target_y = src_y * TARGET_LENGTH / SRC_LENGTH
            res_couple.append({"x": target_x, "y": target_y})
        res_points.append(res_couple)
    return res_points

def GetCanva(url):
    img = Image.open(url)
    BACKGROUND_COLOR = (0, 0, 0)
    edge = max(img.height, img.width)
    offset = ((edge - img.width) // 2, (edge - img.height) // 2)
    canvas = Image.new('RGB', (edge, edge), BACKGROUND_COLOR)
    canvas.paste(img, offset)
    return canvas

def GetFeatureArea(points, indexes, circular=False):
    TL = {"x": float('inf'), "y": float('inf')}   # Top, Left
    BR = {"x": float('-inf'), "y": float('-inf')}   # Bottom, Right

    for index in indexes:
        for point in points[index]:
            TL = getTL(TL, point)
            BR = getBR(BR, point)

    C = getCenter(TL, BR)   # Center
    R = getDistance(C, TL)  # Radius

    if circular:
        return C, R
    else:
        return getRectArea(C, R), R*2
    
def GetAreaImage(canvas: Image, TL, BR, TARGET_SIZE = (300, 300)) -> Image:
    crop = canvas.crop((TL['x'], TL['y'], BR['x'], BR['y']))
    crop = crop.resize(TARGET_SIZE)
    return crop

def RemakePointArrayBaseOnCrop(TL, W, points, TARGET_WIDTH = 300):
    res_points = []
    for couple in points:
        res_couple = []
        for point in couple:
            x = (point['x'] - TL['x']) * TARGET_WIDTH / W
            y = (point['y'] - TL['y']) * TARGET_WIDTH / W
            res_couple.append({'x': x, 'y': y})
        res_points.append(res_couple)
    return res_points

def extendLine(x1, y1, x2, y2, length=1000):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        return (x1, y1 - length, x1, y2 + length)
    elif dy == 0:
        return (x1 - length, y1, x1 + length, y1)
    else:
        m = dy / dx
        b = y1 - m * x1
        x_start = x1 - length
        y_start = m * x_start + b
        x_end = x2 + length
        y_end = m * x_end + b
        return (x_start, y_start, x_end, y_end)

def DrawInfiniteLine(painter, a, b):
    stx, sty, edx, edy = extendLine(a['x'], a['y'], b['x'], b['y'])
    painter.line((stx, sty, edx, edy), fill=(57, 208, 192))

def DrawReferenceLines(painter:ImageDraw, RLs, indexes):
    for index in indexes:
        st = RLs[index][0]
        ed = RLs[index][1]
        DrawInfiniteLine(painter, st, ed)

def DrawDottedLine(painter, st, ed, space=10, color=(0, 255, 0), size=2):
    delta_x = ed['x'] - st['x']
    delta_y = ed['y'] - st['y']
    length = (delta_x**2 + delta_y**2)**0.5
    count_dots = int(length / space)
    step_x = delta_x / (count_dots + ZERO)
    step_y = delta_y / (count_dots + ZERO)
    for i in range(count_dots):
        x = st['x'] + i * step_x
        y = st['y'] + i * step_y
        painter.ellipse((x-size, y-size, x+size, y+size), fill=color)

def DrawSolidLine(painter, st, ed, color=(0, 255, 0), width=4):
    st = (st['x'], st['y'])
    ed = (ed['x'], ed['y'])
    painter.line([st, ed], fill=color, width=width)

def DrawDottedLines(painter:ImageDraw, lines):
    for line in lines:
        A = line[0]
        B = line[1]
        DrawDottedLine(painter, A, B)

def DrawSolidLines(painter:ImageDraw, lines):
    for line in lines:
        A = line[0]
        B = line[1]
        DrawSolidLine(painter, A, B)

def DrawPoint(painter, point, color=(255, 0, 0), size=4):
    painter.ellipse((point['x']-size, point['y']-size, point['x']+size, point['y']+size), color)

def DrawPoints(painter:ImageDraw, points):
    for point in points:
        DrawPoint(painter, point)

def CompleteMarkPoints(points, RLs):
    # Point 54
    points[54][0] = getIntersection((points[49][0], points[52][0]), RLs[5])
    points[34][0] = getIntersection((points[40][0], points[35][0]), RLs[3])
    points[56][0] = getIntersection(RLs[4], RLs[6])
    return points

def GetReferenceLines(points):
    lines = [({'x': 0, 'y': 0}, {'x': 0, 'y': 0})]
    # Reference 1
    ref = (points[37][0], points[38][0])
    lines.append(ref)

    indexes = [49, 42, 40, 50, 33, 32, 33]
    flags   = [ 0,  1,  1,  1,  0,  1,  1]    
    for index, flag in zip(indexes, flags):
        a = points[index][0]
        if flag:
            b = getVertical(a, ref)

        else:
            b = getParallel(a, ref)
        lines.append((a, b))

    # Reference 9
    ref = (points[1][0], points[29][0])
    indexes = [17,  7, 12, 1, 5, 19, 29, 16, 21, 9, 9, 24, 6, 16, 16]
    flags   = [-1, -1, -1, 0, 0,  0,  0, -1,  0, 1, 2,  0, 0,  1,  2]
    for index, flag in zip(indexes, flags):
        a = points[index][0]
        if flag == -1:
            b = points[index][1]
        elif flag == 0:
            b = getVertical(a, ref)
        elif flag == 1:
            b = getParallel(a, ref)
        elif flag == 2:
            a = points[index][1]
            b = getParallel(a, ref)
        lines.append((a, b))
    lines.append(ref)

    return lines
