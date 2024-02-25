from math import sqrt


def getTL(a, b):
    x = min(a['x'], b['x'])
    y = min(a['y'], b['y'])
    return {'x': x, 'y': y}

def getBR(a, b):
    x = max(a['x'], b['x'])
    y = max(a['y'], b['y'])
    return {'x': x, 'y': y}

def getCenter(a, b):
    x = (a['x'] + b['x']) / 2
    y = (a['y'] + b['y']) / 2
    return {'x': x, 'y': y}

def getDistance(a, b):
    x = a['x'] - b['x']
    y = a['y'] - b['y']
    return sqrt(2 * (x**2 + y**2))

def getRectArea(c, r):  # center, radius
    TL = {'x': c['x'] - r, 'y': c['y'] - r}
    BR = {'x': c['x'] + r, 'y': c['y'] + r}
    return TL, BR

def lineFromPoints(P, Q):
    A = Q['y'] - P['y']
    B = P['x'] - Q['x']
    C = A * P['x'] + B * P['y']
    return A, B, C

def getIntersection(A, B):
    A1, B1, C1 = lineFromPoints(A[0], A[1])
    A2, B2, C2 = lineFromPoints(B[0], B[1])
    determinant = A1 * B2 - A2 * B1
    if determinant == 0:
        return None
    else:
        x = (C1 * B2 - C2 * B1) / determinant
        y = (A1 * C2 - A2 * C1) / determinant
        return {'x': x, 'y': y}
    
def getSlope(point1, point2):
    try:
        return (point2['y'] - point1['y']) / (point2['x'] - point1['x'])
    except ZeroDivisionError:
        return float('inf')

def getParallel(a, ref):
    slope_ref = getSlope(ref[0], ref[1])
    if slope_ref == float('inf'):
        b = {'x': a[0], 'y': a[1] + 1}
    else:
        delta_x = 1
        delta_y = slope_ref * delta_x
        b = {'x': a['x'] + delta_x, 'y': a['y'] + delta_y}
    return b

def getVertical(a, ref):
    slope_ref = getSlope(ref[0], ref[1])
    if slope_ref == 0:
        b = {'x': a['x'], 'y': a['y'] + 1}
    elif slope_ref == float('inf'):
        b = {'x': a['x'] + 1, 'y': a['y']}
    else:
        slope_perpendicular = -1 / slope_ref
        delta_x = 1
        delta_y = slope_perpendicular * delta_x
        b = {'x': a['x'] + delta_x, 'y': a['y'] + delta_y}
    return b