from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import os
from app.services.draw_service import CompleteMarkPoints, DrawDottedLines, DrawPoints, DrawReferenceLines, DrawSolidLines, GetAreaImage, GetCanva, GetFeatureArea, GetReferenceLines, RemakePointArrayBaseOnCrop, RemakePointArrayBaseOnImgSize
from app.services.geo_service import getIntersection, getVertical

position_list = [
    [{"x": 61.26482213438737, "y": 0}, {"x": 61.26482213438737, "y": 0}],
    [{"x": 439.2648221343874, "y": 226}, {"x": 439.2648221343874, "y": 226}],
    [{"x": 293.2648221343874, "y": 273}, {"x": 593.2648221343874, "y": 287}],
    [{"x": 330.2648221343874, "y": 329}, {"x": 547.2648221343874, "y": 341}],
    [{"x": 330.2648221343874, "y": 342}, {"x": 546.2648221343874, "y": 354}],
    [{"x": 439.2648221343874, "y": 346}, {"x": 439.2648221343874, "y": 346}],
    [{"x": 438.2648221343874, "y": 357}, {"x": 438.2648221343874, "y": 357}],
    [{"x": 411.2648221343874, "y": 361}, {"x": 468.2648221343874, "y": 364}],
    [{"x": 410.2648221343874, "y": 370}, {"x": 468.2648221343874, "y": 372}],
    [{"x": 331.2648221343874, "y": 367}, {"x": 550.2648221343874, "y": 374}],
    [{"x": 362.2648221343874, "y": 365}, {"x": 516.2648221343874, "y": 372}],
    [{"x": 341.2648221343874, "y": 371}, {"x": 540.2648221343874, "y": 378}],
    [{"x": 368.2648221343874, "y": 373.5}, {"x": 512.2648221343874, "y": 377.5}],
    [{"x": 390.2648221343874, "y": 369}, {"x": 489.2648221343874, "y": 374}],
    [{"x": 366.2648221343874, "y": 381}, {"x": 515.2648221343874, "y": 386}],
    [{"x": 396.2648221343874, "y": 379}, {"x": 493.2648221343874, "y": 385}],
    [{"x": 405.2648221343874, "y": 384}, {"x": 474.2648221343874, "y": 389}],
    [{"x": 283.2648221343874, "y": 402}, {"x": 600.2648221343874, "y": 400}],
    [{"x": 398.2648221343874, "y": 473}, {"x": 482.2648221343874, "y": 474}],
    [{"x": 440.2648221343874, "y": 501}, {"x": 440.2648221343874, "y": 501}],
    [{"x": 461.2648221343874, "y": 493}, {"x": 461.2648221343874, "y": 493}],
    [{"x": 461.2648221343874, "y": 529}, {"x": 461.2648221343874, "y": 529}],
    [{"x": 293.2648221343874, "y": 532}, {"x": 586.2648221343874, "y": 536}],
    [{"x": 374.2648221343874, "y": 538}, {"x": 509.2648221343874, "y": 538}],
    [{"x": 439.2648221343874, "y": 546}, {"x": 439.2648221343874, "y": 546}],
    [{"x": 438.2648221343874, "y": 572}, {"x": 438.2648221343874, "y": 572}],
    [{"x": 312.2648221343874, "y": 566}, {"x": 562.2648221343874, "y": 576}],
    [{"x": 293.8552924461787, "y": 567.9939761936935}, {"x": 573.8172785963732, "y": 589.2680559870346}],
    [{"x": 366.2648221343874, "y": 628}, {"x": 506.2648221343874, "y": 635}],
    [{"x": 440.2648221343874, "y": 652}, {"x": 440.2648221343874, "y": 652}],
    [{"x": 239, "y": 82}],
    [{"x": 223, "y": 106}],
    [{"x": 169, "y": 203}],
    [{"x": 243, "y": 258}],
    [{"x": 225, "y": 332}],
    [{"x": 182, "y": 257}],
    [{"x": 130, "y": 327}],
    [{"x": 282, "y": 335}],
    [{"x": 512, "y": 349}],
    [{"x": 123, "y": 334}],
    [{"x": 105, "y": 359}],
    [{"x": 110, "y": 375}],
    [{"x": 202, "y": 372}],
    [{"x": 129, "y": 393}],
    [{"x": 143, "y": 401}],
    [{"x": 135, "y": 445}],
    [{"x": 198, "y": 468}],
    [{"x": 134, "y": 483}],
    [{"x": 154, "y": 523}],
    [{"x": 455, "y": 540}],
    [{"x": 135, "y": 561}],
    [{"x": 176, "y": 604}],
    [{"x": 198, "y": 599}],
    [{"x": 288, "y": 598}],
    [{"x": 220, "y": 570}],
    [{"x": 332, "y": 769}],
    [{"x": 168, "y": 327}],
    [{"x": 241, "y": 302}],
    [{"x": 134, "y": 493}],
    [{"x": 118, "y": 385}]
  ]

ZERO = 0.0001

def midpoint(x1, y1, x2, y2):
    return (x1 + x2) / 2, (y1 + y2) / 2

def draw_point(draw, point, dot_color=(255, 0, 0), dot_size=2):
    draw.ellipse((point[0]-dot_size*2, point[1]-dot_size*2, point[0]+dot_size*2, point[1]+dot_size*2), dot_color)

def draw_dotted_line(draw, point1, point2, dot_spacing=10, dot_color=(0, 255, 0), dot_size=2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    line_length = (delta_x**2 + delta_y**2)**0.5
    num_dots = int(line_length / dot_spacing)
    step_x = delta_x / (num_dots + ZERO)
    step_y = delta_y / (num_dots + ZERO)
    for i in range(num_dots):
        x = int(point1[0] + i * step_x)
        y = int(point1[1] + i * step_y)
        draw.ellipse((x-dot_size, y-dot_size, x+dot_size, y+dot_size), fill=dot_color)        
    draw.ellipse((point1[0]-dot_size*2, point1[1]-dot_size*2, point1[0]+dot_size*2, point1[1]+dot_size*2), (255, 0, 0))
    draw.ellipse((point2[0]-dot_size*2, point2[1]-dot_size*2, point2[0]+dot_size*2, point2[1]+dot_size*2), (255, 0, 0))
def draw_dotted_line_p_vertical_line(draw, point1, point2, dot_spacing=10, dot_color=(0, 255, 0), dot_size=2, line_color=(0, 255, 0), line_width=4):
    # Draw the dotted line between point1 and point2
    delta_x = point2[0] - point1[0]
    delta_y = 0
    line_length = (delta_x**2 + delta_y**2)**0.5
    num_dots = int(line_length / dot_spacing)
    step_x = delta_x / (num_dots + ZERO)
    step_y = delta_y / (num_dots + ZERO)
    for i in range(num_dots):
        x = int(point1[0] + i * step_x)
        y = int(point1[1] + i * step_y)
        draw.ellipse((x - dot_size, y - dot_size, x + dot_size, y + dot_size), fill=dot_color)

    # Draw circles at the specified points
    draw.ellipse((point1[0] - dot_size * 2, point1[1] - dot_size * 2, point1[0] + dot_size * 2, point1[1] + dot_size * 2), (255, 0, 0))
    draw.ellipse((point2[0] - dot_size * 2, point2[1] - dot_size * 2, point2[0] + dot_size * 2, point2[1] + dot_size * 2), (255, 0, 0))
def draw_solid_line(draw, point1, point2, line_color=(0, 255, 0), line_width=4, dot_size=2):
    draw.line([point1, point2], fill=line_color, width=line_width)
    draw.ellipse((point1[0]-dot_size*2, point1[1]-dot_size*2, point1[0]+dot_size*2, point1[1]+dot_size*2), (255, 0, 0))
    draw.ellipse((point2[0]-dot_size*2, point2[1]-dot_size*2, point2[0]+dot_size*2, point2[1]+dot_size*2), (255, 0, 0))
def draw_infinite_line(draw, point1, point2, line_color=(57, 208, 192), line_width=1, dot_size=2):
    x1, y1 = point1
    x2, y2 = point2
    slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    y_intercept = y1 - slope * x1 if x2 - x1 != 0 else None
    width, height = draw.im.size
    x_min, x_max = 0, width
    y_min, y_max = 0, height
    if slope == float('inf'):
        draw.line([(x1, y_min), (x1, y_max)], fill=line_color, width=line_width)
    else:
        draw.line([(x_min, int(slope * x_min + y_intercept)), (x_max, int(slope * x_max + y_intercept))], fill=line_color, width=line_width)
    draw.ellipse((point1[0] - dot_size * 2, point1[1] - dot_size * 2, point1[0] + dot_size * 2, point1[1] + dot_size * 2), (255, 0, 0))
    draw.ellipse((point2[0] - dot_size * 2, point2[1] - dot_size * 2, point2[0] + dot_size * 2, point2[1] + dot_size * 2), (255, 0, 0))

def draw_horizontal_line(draw, point, line_color=(57, 208, 192), line_width=1, ellipse_color=(255, 0, 0), ellipse_radius=4):
    y = point[1]
    width = draw.im.size[0]
    draw.line((0, y, width, y), fill=line_color, width=line_width)
    draw.ellipse((point[0] - ellipse_radius, y - ellipse_radius, point[0] + ellipse_radius, y + ellipse_radius), fill=ellipse_color)
def draw_vertical_line(draw, point, line_color=(57, 208, 192), line_width=1, ellipse_color=(255, 0, 0), ellipse_radius=4):
    x = point[0]
    height = draw.im.size[1]
    draw.line((x, 0, x, height), fill=line_color, width=line_width)
    draw.ellipse((x - ellipse_radius, point[1] - ellipse_radius, x + ellipse_radius, point[1] + ellipse_radius), fill=ellipse_color)
def draw_solid_line_p_vertical_line(draw, point1, point2, line_color=(0, 255, 0), line_width=4, dot_size=2):
    draw.line([(point1[0], point1[1]), (point2[0], point1[1])], fill=line_color, width=line_width)
    draw.ellipse((point1[0]-dot_size*2, point1[1]-dot_size*2, point1[0]+dot_size*2, point1[1]+dot_size*2), (255, 0, 0))

def draw_solid_line_p_horizontal_line(draw, point1, point2, line_color=(0, 255, 0), line_width=4, dot_size=2):
    draw.line([(point1[0], point1[1]), (point1[0], point2[1])], fill=line_color, width=line_width)
    draw.ellipse((point1[0]-dot_size*2, point1[1]-dot_size*2, point1[0]+dot_size*2, point1[1]+dot_size*2), (255, 0, 0))

def draw_full_length_dotted_line(draw, point1, point2, image_size, color=(0, 255, 0), width=1, dot_length=10, space_length=5):
    # Calculate the direction vector and its length
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    length = (dx**2 + dy**2)**0.5
    dx, dy = dx / length, dy / length  # Normalize

    # Extend the line to cover the entire image
    extend_length = max(image_size)
    start_point = (int(point1[0] - dx * extend_length), int(point1[1] - dy * extend_length))
    end_point = (int(point2[0] + dx * extend_length), int(point2[1] + dy * extend_length))

    # Calculate total length for dotted pattern
    total_length = (extend_length * 2) + length
    num_dots = int(total_length / (dot_length + space_length))

    for i in range(num_dots):
        dot_start = i * (dot_length + space_length)
        dot_end = dot_start + dot_length

        # Calculate the start and end points of each dot
        segment_start = (int(start_point[0] + dx * dot_start), int(start_point[1] + dy * dot_start))
        segment_end = (int(start_point[0] + dx * dot_end), int(start_point[1] + dy * dot_end))

        # Draw each dot
        draw.line([segment_start, segment_end], fill=color, width=width)

def calculate_slope(point1, point2):
    # Calculate the slope (m) of the line
    return (point2[1] - point1[1]) / (point2[0] - point1[0])

def calculate_y_intercept(point, slope):
    # Calculate the y-intercept (b) of the line
    return point[1] - slope * point[0]

def find_intersection(line1, line2):
    # Calculate slopes and y-intercepts
    slope1 = calculate_slope(line1[0], line1[1])
    slope2 = calculate_slope(line2[0], line2[1])
    y_intercept1 = calculate_y_intercept(line1[0], slope1)
    y_intercept2 = calculate_y_intercept(line2[0], slope2)

    # Check if lines are parallel
    if slope1 == slope2:
        return None  # Parallel lines do not intersect

    # Calculate intersection point
    x_intersect = (y_intercept2 - y_intercept1) / (slope1 - slope2)
    y_intersect = slope1 * x_intersect + y_intercept1

    return (x_intersect, y_intersect)

def rescale(startpoint, width, points):
    scaled_points = []
    for point in points:
        scaled_x = (point[0] - startpoint[0]) * 300 / width
        scaled_y = (point[1] - startpoint[1]) * 300 / width
        scaled_points.append((scaled_x, scaled_y))
    return scaled_points

###Front Functions
#1
def create_eye_separation_ratio_image(points, RLs, DIR, index, canvas):
    indexes = [12, 17]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines    = [(points[12][0], points[12][1])]
    solidLines  = [(points[17][0], points[17][1])]
    drawPoints  = [points[12][0], points[12][1],
                   points[17][0], points[17][1],]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)
#2
def create_facial_thirds_image(points, RLs, DIR, index, canvas):
    indexes = [29, 19, 5, 1]
    RLIndexes = [12, 13, 14, 15]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    # TEMP POINT
    temp1 = getIntersection((points[1][0], getVertical(points[1][0], RLs[13])), RLs[13])
    temp2 = getIntersection((temp1, getVertical(temp1, RLs[14])), RLs[14])
    temp3 = getIntersection((temp2, getVertical(temp2, RLs[15])), RLs[15])

    dotLines    = [(points[1][0], temp1),
                   (temp1, temp2),
                   (temp2, temp3)]
    solidLines  = []
    drawPoints  = [points[29][0], points[19][0], points[5][0], points[1][0], temp1, temp2, temp3]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)
#3
def create_lateral_canthal_tilt_image(points, RLs, DIR, index, canvas):
    indexes = [11, 16]
    RLIndexes = [16]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines    = [(points[11][0], points[16][0]),
                   (points[11][1], points[16][1]),]
    solidLines  = []
    drawPoints  = [points[11][0], points[11][1],
                   points[16][0], points[16][1],]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)
#4
def create_facial_width_to_height_ratio_image(points, RLs, DIR, index, canvas):
    indexes = [17, 21, 6]
    RLIndexes = [17, 21]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    # TEMP POINT
    temp = getIntersection((points[6][0], getVertical(points[6][0], RLs[17])), RLs[17])

    dotLines    = [(points[17][0], points[17][1]),]
    solidLines  = [(points[6][0], temp)]
    drawPoints  = [points[17][0], points[17][1],
                   points[6][0], points[21][0], temp]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)
#5
def create_jaw_frontal_angle_image(points, RLs, DIR, index, canvas):
    indexes = [26, 28]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    # TEMP POINT
    temp = getIntersection((points[26][0], points[28][0]), (points[26][1], points[28][1]))

    dotLines    = [(points[26][0], temp),
                   (points[26][1], temp),]
    solidLines  = []
    drawPoints  = [points[26][0], points[26][1],
                   points[28][0], points[28][1], temp]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)
#6
def create_cheekbone_height_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[12][0]["x"]
    y1 = mark_points[12][0]["y"]
    x2 = mark_points[12][1]["x"]
    y2 = mark_points[12][1]["y"]
    x3 = mark_points[17][0]["x"]
    y3 = mark_points[17][0]["y"]
    x4 = mark_points[17][1]["x"]
    y4 = mark_points[17][1]["y"]
    x5 = mark_points[21][0]["x"]
    y5 = mark_points[21][0]["y"]
    

    x_min = min(x1,x2,x3,x4,x5)
    x_max = max(x1,x2,x3,x4,x5)
    y_min = min(y1,y2,y3,y4,y5)
    y_max = max(y1,y2,y3,y4,y5)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_solid_line(draw, (x1, y1), (x2, y2), (57, 208, 192))
    draw_solid_line(draw, (x3, y3), (x4, y4), (57, 208, 192))
    draw_solid_line(draw, ((x1+x2)/2,(y1+y2)/2), ((x1+x2)/2,y5))
    draw_dotted_line(draw, ((x1+x2)/2-20,(y3+y4)/2), ((x1+x2)/2-20,y5))
    draw_horizontal_line(draw, (x5, y5))
    output_filename = os.path.join(DIR, f"{create_cheekbone_height_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#7
def create_total_facial_height_to_width_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[1][0]["x"]
    y1 = mark_points[1][0]["y"]
    x2 = mark_points[29][0]["x"]
    y2 = mark_points[29][0]["y"]
    x3 = mark_points[17][0]["x"]
    y3 = mark_points[17][0]["y"]
    x4 = mark_points[17][1]["x"]
    y4 = mark_points[17][1]["y"]
    

    x_min = min(x1,x2,x3,x4)
    x_max = max(x1,x2,x3,x4)
    y_min = min(y1,y2,y3,y4)
    y_max = max(y1,y2,y3,y4)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_dotted_line(draw, (x1, y1), (x2, y2))
    draw_solid_line(draw, (x3, y3), (x4, y4))
    output_filename = os.path.join(DIR, f"{create_total_facial_height_to_width_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#8
def create_bigonial_width_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[17][0]["x"]
    y1 = mark_points[17][0]["y"]
    x2 = mark_points[17][1]["x"]
    y2 = mark_points[17][1]["y"]
    x3 = mark_points[22][0]["x"]
    y3 = mark_points[22][0]["y"]
    x4 = mark_points[22][1]["x"]
    y4 = mark_points[22][1]["y"]
    

    x_min = min(x1,x2,x3,x4)
    x_max = max(x1,x2,x3,x4)
    y_min = min(y1,y2,y3,y4)
    y_max = max(y1,y2,y3,y4)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_solid_line(draw, (x1, y1), (x2, y2))
    draw_dotted_line(draw, (x3, y3), (x4, y4))
    output_filename = os.path.join(DIR, f"{create_bigonial_width_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#9
def create_chin_to_philtrum_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[20][0]["x"]
    y1 = mark_points[20][0]["y"]
    x2 = mark_points[21][1]["x"]
    y2 = mark_points[21][1]["y"]
    x3 = mark_points[25][0]["x"]
    y3 = mark_points[25][0]["y"]
    x4 = mark_points[29][1]["x"]
    y4 = mark_points[29][1]["y"]
    

    x_min = min(x1,x2,x3,x4)
    x_max = max(x1,x2,x3,x4)
    y_min = min(y1,y2,y3,y4)
    y_max = max(y1,y2,y3,y4)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_horizontal_line(draw, (x2, y2))
    draw_solid_line(draw, (x1, y1), (x1, y2))
    draw_dotted_line(draw, (x3, y3), (x4, y4))

    output_filename = os.path.join(DIR, f"{create_chin_to_philtrum_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#10
def create_Neck_width__image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[22][0]["x"]
    y1 = mark_points[22][0]["y"]
    x2 = mark_points[22][1]["x"]
    y2 = mark_points[22][1]["y"]
    x3 = mark_points[27][0]["x"]
    y3 = mark_points[27][0]["y"]
    x4 = mark_points[27][1]["x"]
    y4 = mark_points[27][1]["y"]
    

    x_min = min(x1,x2,x3,x4)
    x_max = max(x1,x2,x3,x4)
    y_min = min(y1,y2,y3,y4)
    y_max = max(y1,y2,y3,y4)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_solid_line(draw, (x1, y1), (x2, y2))
    draw_dotted_line(draw, (x3, y3), (x4, y4))
    output_filename = os.path.join(DIR, f"{create_Neck_width__image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#11
def create_mouth_width_to_nose_width_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[18][0]["x"]
    y1 = mark_points[18][0]["y"]
    x2 = mark_points[18][1]["x"]
    y2 = mark_points[18][1]["y"]
    x3 = mark_points[23][0]["x"]
    y3 = mark_points[23][0]["y"]
    x4 = mark_points[23][1]["x"]
    y4 = mark_points[23][1]["y"]
    

    x_min = min(x1,x2,x3,x4)
    x_max = max(x1,x2,x3,x4)
    y_min = min(y1,y2,y3,y4)
    y_max = max(y1,y2,y3,y4)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_solid_line(draw, (x1, y1), (x2, y2))
    draw_dotted_line(draw, (x3, y3), (x4, y4))
    output_filename = os.path.join(DIR, f"{create_mouth_width_to_nose_width_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#12
def create_midface_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[12][0]["x"]
    y1 = mark_points[12][0]["y"]
    x2 = mark_points[12][1]["x"]
    y2 = mark_points[12][1]["y"]
    x3 = mark_points[21][0]["x"]
    y3 = mark_points[21][0]["y"]
    

    x_min = min(x1,x2,x3)
    x_max = max(x1,x2,x3)
    y_min = min(y1,y2,y3)
    y_max = max(y1,y2,y3)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3)])
    draw = ImageDraw.Draw(cropped_img)  
    draw.ellipse((x1-3, y1-3, x1+3, y1+3), fill=(255, 0, 0))
    draw.ellipse((x2-3, y2-3, x2+3, y2+3), fill=(255, 0, 0))
    draw.ellipse((x3-3, y3-3, x3+3, y3+3), fill=(255, 0, 0))
    draw_horizontal_line(draw, (x3, y3))
    draw_dotted_line(draw, (x1, y1), (x2, y2), dot_color=(57, 208, 192))
    draw_solid_line(draw, ((x1+x2)/2, (y1+y2)/2), ((x1+x2)/2, y3))
    output_filename = os.path.join(DIR, f"{create_midface_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#13
def create_eyebrow_position_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[10][0]["x"]
    y1 = mark_points[10][0]["y"]
    x2 = mark_points[14][0]["x"]
    y2 = mark_points[14][0]["y"]
    x3 = mark_points[12][0]["x"]
    y3 = mark_points[12][0]["y"]
    x4 = mark_points[12][1]["x"]
    y4 = mark_points[12][1]["y"]
    x5 = mark_points[8][0]["x"]
    y5 = mark_points[8][0]["y"]
    x6 = mark_points[8][1]["x"]
    y6 = mark_points[8][1]["y"]
    x7 = mark_points[10][1]["x"]
    y7 = mark_points[10][1]["y"]
    x8 = mark_points[14][1]["x"]
    y8 = mark_points[14][1]["y"]
    

    x_min = min(x1,x2,x3,x4,x5,x6,x7,x8)
    x_max = max(x1,x2,x3,x4,x5,x6,x7,x8)
    y_min = min(y1,y2,y3,y4,y5,y6,y7,y8)
    y_max = max(y1,y2,y3,y4,y5,y6,y7,y8)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_infinite_line(draw, (x3, y3), (x4, y4))
    draw_solid_line(draw, (x1, y1), (x2, y2))
    draw_solid_line(draw, (x7, y7), (x8, y8))
    draw_dotted_line(draw, (x5, y5), (x5, y3))
    draw_dotted_line(draw, (x6, y6), (x6, y3))
    output_filename = os.path.join(DIR, f"{create_eyebrow_position_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)

    return True

#14
def create_eye_spacing_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[9][0]["x"]
    y1 = mark_points[9][0]["y"]
    x2 = mark_points[16][0]["x"]
    y2 = mark_points[16][0]["y"]
    x3 = mark_points[16][1]["x"]
    y3 = mark_points[16][1]["y"]
    x4 = mark_points[9][1]["x"]
    y4 = mark_points[9][1]["y"]
    x5=x4
    y5 = (y2-y3) * (x4-x2) / (x2-x3) + y2
    

    x_min = min(x1,x2,x3,x4,x5)
    x_max = max(x1,x2,x3,x4,x5)
    y_min = min(y1,y2,y3,y4,y5)
    y_max = max(y1,y2,y3,y4,y5)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_vertical_line(draw, (x1, y1))
    draw_vertical_line(draw, (x2, y2))
    draw_vertical_line(draw, (x3, y3))
    draw_vertical_line(draw, (x4, y4))
    draw_solid_line(draw,(x2,y2),(x1,y2))
    draw_dotted_line(draw,(x2,y2+20),(x3,y2+20))
    draw_solid_line(draw,(x3,y3),(x4,y3))
    output_filename = os.path.join(DIR, f"{create_eye_spacing_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#15
def create_eye_aspect_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[10][1]["x"]
    y1 = mark_points[10][1]["y"]
    x2 = mark_points[14][1]["x"]
    y2 = mark_points[14][1]["y"]
    x3 = mark_points[16][1]["x"]
    y3 = mark_points[16][1]["y"]
    x4 = mark_points[11][1]["x"]
    y4 = mark_points[11][1]["y"]
    x5 = mark_points[10][0]["x"]
    y5 = mark_points[10][0]["y"]
    x6 = mark_points[14][0]["x"]
    y6 = mark_points[14][0]["y"]
    x7 = mark_points[16][0]["x"]
    y7 = mark_points[16][0]["y"]
    x8 = mark_points[11][0]["x"]
    y8 = mark_points[11][0]["y"]
    

    x_min = min(x1,x2,x3,x4,x5,x6,x7,x8)
    x_max = max(x1,x2,x3,x4,x5,x6,x7,x8)
    y_min = min(y1,y2,y3,y4,y5,y6,y7,y8)
    y_max = max(y1,y2,y3,y4,y5,y6,y7,y8)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5,y5),(x6,y6),(x7,y7),(x8,y8)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5,y5),(x6,y6),(x7,y7),(x8,y8)])
    draw = ImageDraw.Draw(cropped_img)
    draw_solid_line(draw, (x1,y1),(x2,y2))
    draw_solid_line(draw, (x5,y5),(x6,y6))
    draw_dotted_line(draw, (x3,y3),(x4,y4))
    draw_dotted_line(draw, (x7,y7),(x8,y8))
    output_filename = os.path.join(DIR, f"{create_eye_aspect_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#16
def create_lower_lip_to_upper_lip_ratio_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[21][0]["x"]
    y1 = mark_points[21][0]["y"]
    x2 = mark_points[24][0]["x"]
    y2 = mark_points[24][0]["y"]
    x3 = mark_points[25][0]["x"]
    y3 = mark_points[25][0]["y"]
    

    x_min = min(x1,x2,x3)
    x_max = max(x1,x2,x3)
    y_min = min(y1,y2,y3)
    y_max = max(y1,y2,y3)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_horizontal_line(draw, (x1, y1))
    draw_solid_line(draw, (x2, y2), (x2, y1))
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{create_lower_lip_to_upper_lip_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#17
def create_deviation_of_iaa_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[9][0]["x"]
    y1 = mark_points[9][0]["y"]
    x2 = mark_points[9][1]["x"]
    y2 = mark_points[9][1]["y"]
    x3 = mark_points[19][0]["x"]
    y3 = mark_points[19][0]["y"]
    x4 = mark_points[26][0]["x"]
    y4 = mark_points[26][0]["y"]
    x5 = mark_points[26][1]["x"]
    y5 = mark_points[26][1]["y"]
    x6 = mark_points[28][0]["x"]
    y6 = mark_points[28][0]["y"]
    x7 = mark_points[28][1]["x"]
    y7 = mark_points[28][1]["y"]

    intersection = find_intersection([(x4,y4),(x6,y6)],[(x5,y5),(x7,y7)])
    
    x_min = min(x1,x2,x3,x4,intersection[0])
    x_max = max(x1,x2,x3,x4,intersection[0])
    y_min = min(y1,y2,y3,y4,intersection[1])
    y_max = max(y1,y2,y3,y4,intersection[1])
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), intersection] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), intersection])
    draw = ImageDraw.Draw(cropped_img)  
    draw_dotted_line(draw, (x1, y1), (x3, y3))
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    draw_dotted_line(draw, (x4, y4), (intersection[0],intersection[1]))
    draw_dotted_line(draw, (x5, y5), (intersection[0],intersection[1]))
    output_filename = os.path.join(DIR, f"{create_deviation_of_iaa_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#18
def create_eyebrow_tilt_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[7][1]["x"]
    y1 = mark_points[7][1]["y"]
    x2 = mark_points[4][1]["x"]
    y2 = mark_points[4][1]["y"]
    x3 = mark_points[7][0]["x"]
    y3 = mark_points[7][0]["y"]
    x4 = mark_points[4][0]["x"]
    y4 = mark_points[4][0]["y"]

    x_min = min(x1,x2,x3,x4)
    x_max = max(x1,x2,x3,x4)
    y_min = min(y1,y2,y3,y4)
    y_max = max(y1,y2,y3,y4)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2),(x3,y3),(x4,y4)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2),(x3,y3),(x4,y4)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_infinite_line(draw, (x1, y1), (x3, y3))
    draw_dotted_line(draw, (x1, y1), (x2, y2))
    draw_dotted_line(draw, (x3, y3), (x4, y4))

    output_filename = os.path.join(DIR, f"{create_eyebrow_tilt_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#19
def create_bitemporal_width_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[2][0]["x"]
    y1 = mark_points[2][0]["y"]
    x2 = mark_points[2][1]["x"]
    y2 = mark_points[2][1]["y"]
    x3 = mark_points[17][0]["x"]
    y3 = mark_points[17][0]["y"]
    x4 = mark_points[17][1]["x"]
    y4 = mark_points[17][1]["y"]
    

    x_min = min(x1,x2,x3,x4)
    x_max = max(x1,x2,x3,x4)
    y_min = min(y1,y2,y3,y4)
    y_max = max(y1,y2,y3,y4)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_dotted_line(draw, (x1, y1), (x2, y2))
    draw_solid_line(draw, (x3, y3), (x4, y4))
    output_filename = os.path.join(DIR, f"{create_bitemporal_width_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#20
def create_lower_third_proportion_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[19][0]["x"]
    y1 = mark_points[19][0]["y"]
    x2 = mark_points[24][0]["x"]
    y2 = mark_points[24][0]["y"]
    x3 = mark_points[29][0]["x"]
    y3 = mark_points[29][0]["y"]
    

    x_min = min(x1,x2,x3)
    x_max = max(x1,x2,x3)
    y_min = min(y1,y2,y3)
    y_max = max(y1,y2,y3)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_horizontal_line(draw, (x1, y1))
    draw_horizontal_line(draw, (x2, y2))
    draw_horizontal_line(draw, (x3, y3))
    draw_dotted_line(draw, (x2, y2), (x2, y1))
    draw_solid_line(draw, (x3-20, y3), (x3-20, y1))
    output_filename = os.path.join(DIR, f"{create_lower_third_proportion_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#21
def create_ipsilateral_alar_angle_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[9][0]["x"]
    y1 = mark_points[9][0]["y"]
    x2 = mark_points[9][1]["x"]
    y2 = mark_points[9][1]["y"]
    x3 = mark_points[19][0]["x"]
    y3 = mark_points[19][0]["y"]
    
    x_min = min(x1,x2,x3)
    x_max = max(x1,x2,x3)
    y_min = min(y1,y2,y3)
    y_max = max(y1,y2,y3)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_dotted_line(draw, (x1, y1), (x3, y3))
    draw_dotted_line(draw, (x2, y2), (x3, y3))

    output_filename = os.path.join(DIR, f"{create_ipsilateral_alar_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#22
def create_medial_canthal_angle_image(img_url, mark_points, DIR, index):
    img = Image.open(img_url)
    
    # Calculate the updated dimensions while maintaining aspect ratio
    if img.height >= img.width:
        updated_height = 800
        updated_width = img.width * 800 / img.height
    else:
        updated_width = 800
        updated_height = img.height * 800 / img.width

    img = img.resize((int(updated_width), int(updated_height)))
    canvas = Image.new('RGB', (800, 800), (0, 0, 0))

    x_offset = (800 - img.width) // 2
    y_offset = (800 - img.height) // 2

    canvas.paste(img, (x_offset, y_offset))
    draw = ImageDraw.Draw(canvas)  

    x1 = mark_points[16][1]["x"]
    y1 = mark_points[16][1]["y"]
    x2 = mark_points[13][1]["x"]
    y2 = mark_points[13][1]["y"]
    x3 = mark_points[15][1]["x"]
    y3 = mark_points[15][1]["y"]
    

    x_min = min(x1,x2,x3)
    x_max = max(x1,x2,x3)
    y_min = min(y1,y2,y3)
    y_max = max(y1,y2,y3)
    
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    half_side_length = max(x_max - center_x, y_max - center_y)

    # Define the square's bounding coordinates
    square_x_min = max(center_x - half_side_length, 0)
    square_y_min = max(center_y - half_side_length, 0)
    square_x_max = min(center_x + half_side_length, 800)
    square_y_max = min(center_y + half_side_length, 800)

    # Crop the image to the square
    cropped_img = canvas.crop((square_x_min-10, square_y_min-10, square_x_max+10, square_y_max+10))
    cropped_img = cropped_img.resize((300, 300))
    width = half_side_length*2+20
    start_x = center_x - half_side_length - 10
    start_y = center_y - half_side_length -10
    [(x1, y1), (x2, y2), (x3, y3)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_dotted_line(draw, (x1, y1), (x2, y2))
    draw_dotted_line(draw, (x3, y3), (x1, y1))
    output_filename = os.path.join(DIR, f"{create_medial_canthal_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True


###side
#23
def create_gonial_angle_image(points, RLs, DIR, index, canvas):
    indexes = [38, 49, 52]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[38][0], points[49][0]),
                (points[52][0], points[49][0]),]
    solidLines = []
    drawPoints = [points[52][0], points[49][0], points[38][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#24
def create_nasofrontal_angle_image(points, RLs, DIR, index, canvas):
    indexes = [32, 35, 39]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[32][0], points[35][0]),
                (points[39][0], points[35][0]),]
    solidLines = []
    drawPoints = [points[32][0], points[35][0], points[39][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#25
def create_mandibular_plane_angle_image(points, RLs, DIR, index, canvas):
    indexes = [52, 49]
    RLIndexes = [2, ]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[52][0], points[49][0])]
    solidLines = []
    drawPoints = [points[52][0], points[49][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#26
def create_ramus_to_mandible_ratio_image(points, RLs, DIR, index, canvas):
    indexes = [38, 49, 54]
    RLIndexes = [5, ]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[38][0], points[49][0])]
    solidLines = [(points[49][0], points[54][0])]
    drawPoints = [points[38][0], points[49][0], points[54][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#27
def create_facial_convexity_glabella_image(points, RLs, DIR, index, canvas):
    indexes = [32, 43, 50]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[32][0], points[43][0]),
                (points[43][0], points[50][0]),]
    solidLines = []
    drawPoints = [points[32][0], points[43][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)
    
    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#28
def create_submental_cervical_angle_image(points, RLs, DIR, index, canvas):
    indexes = [51, 53, 55]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[51][0], points[53][0]),
                (points[55][0], points[53][0]),]
    solidLines = []
    drawPoints = [points[51][0], points[53][0], points[55][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#29
def create_nasofacial_angle_image(points, RLs, DIR, index, canvas):
    indexes = [50, 35, 39]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[50][0], points[35][0]),
                (points[39][0], points[35][0]),]
    solidLines = []
    drawPoints = [points[50][0], points[35][0], points[39][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#30
def create_nasolabial_angle_image(points, RLs, DIR, index, canvas):
    indexes = [45, 44, 41]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[45][0], points[44][0]),
                (points[44][0], points[41][0]),]
    solidLines = []
    drawPoints = [points[45][0], points[44][0], points[41][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#31
def create_orbital_vector_image(points, RLs, DIR, index, canvas):
    indexes = [33, 57, 46]
    RLIndexes = [8]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = []
    solidLines = []
    drawPoints = [points[33][0], points[57][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)
    
    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#32
def create_total_facial_convexity_image(points, RLs, DIR, index, canvas):
    indexes = [32, 40, 50]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[32][0], points[40][0]),
                (points[40][0], points[50][0]),]
    solidLines = []
    drawPoints = [points[32][0], points[40][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)
    
    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#33
def create_mentolabial_angle_image(points, RLs, DIR, index, canvas):
    indexes = [58, 48, 50]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[58][0], points[48][0]),
                (points[48][0], points[50][0]),]
    solidLines = []
    drawPoints = [points[58][0], points[48][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#34
def create_facial_convexity_nasion_image(points, RLs, DIR, index, canvas):
    indexes = [35, 43, 50]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[35][0], points[43][0]),
                (points[43][0], points[50][0]),]
    solidLines = []
    drawPoints = [points[35][0], points[43][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#35
def create_nasal_projection_image(points, RLs, DIR, index, canvas):
    indexes = [34, 35, 40, 42]
    RLIndexes = [3, ]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    # TEMP POINT
    temp = getIntersection((points[40][0], getVertical(points[40][0], RLs[3])), RLs[3])

    dotLines = [(points[40][0], temp)]
    solidLines = [(points[40][0], points[34][0])]
    drawPoints = [points[40][0], points[34][0], points[42][0], points[35][0], temp]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#36
def create_nasal_w_to_h_ratio_image(points, RLs, DIR, index, canvas):
    indexes = [40, 56, 33, 42]
    RLIndexes = [3, 4, 6]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    # TEMP POINT
    temp = getIntersection((points[40][0], getVertical(points[40][0], RLs[3])), RLs[3])

    dotLines = [(points[40][0], temp)]
    solidLines = [(points[40][0], points[56][0])]
    drawPoints = [points[40][0], points[56][0], points[33][0], points[42][0], temp]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)    

#37
def create_ricketts_e_line_image(points, RLs, DIR, index, canvas):
    indexes = [45, 47, 50, 40]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[40][0], points[50][0])]
    solidLines = []
    drawPoints = [points[45][0], points[47][0], points[40][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#38
def create_holdaway_h_line_image(points, RLs, DIR, index, canvas):
    indexes = [47, 50, 45]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[45][0], points[50][0])]
    solidLines = []
    drawPoints = [points[45][0], points[47][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#39
def create_steiner_s_line_image(points, RLs, DIR, index, canvas):
    indexes = [59, 50, 45]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[59][0], points[50][0])]
    solidLines = []
    drawPoints = [points[45][0], points[59][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#40
def create_burstone_line_image(points, RLs, DIR, index, canvas):
    indexes = [43, 50, 45, 47]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[43][0], points[50][0])]
    solidLines = []
    drawPoints = [points[45][0], points[47][0], points[50][0], points[43][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#41
def create_nasomental_angle_image(points, RLs, DIR, index, canvas):
    indexes = [35, 50, 40]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[35][0], points[40][0]),
                (points[50][0], points[40][0]),]
    solidLines = []
    drawPoints = [points[35][0], points[40][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#42
def create_gonion_to_mouth_relationship_image(points, RLs, DIR, index, canvas):
    indexes = [46, 49]
    RLIndexes = [2, ]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = []
    solidLines = []
    drawPoints = [points[46][0], points[49][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#43
def create_recession_relative_to_frankfort_plane_image(points, RLs, DIR, index, canvas):
    indexes = [35, 50]
    RLIndexes = [5, ]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = []
    solidLines = []
    drawPoints = [points[35][0], points[50][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#44
def create_browridge_inclination_angle_image(points, RLs, DIR, index, canvas):
    indexes = [31, 32]
    RLIndexes = [7, ]
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[31][0], points[32][0])]
    solidLines = []
    drawPoints = [points[31][0], points[32][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

#45
def create_nasal_tip_angle_image(points, RLs, DIR, index, canvas):
    indexes = [39, 40, 41]
    RLIndexes = []
    (TL, BR), W = GetFeatureArea(points, indexes)    # TopLeft, BottomRight, Width
    crop = GetAreaImage(canvas, TL, BR)
    painter = ImageDraw.Draw(crop)
    points = RemakePointArrayBaseOnCrop(TL, W, points)
    RLs = RemakePointArrayBaseOnCrop(TL, W, RLs)

    dotLines = [(points[39][0], points[40][0]),
                (points[41][0], points[40][0]),]
    solidLines = []
    drawPoints = [points[39][0], points[40][0], points[41][0]]
    
    DrawReferenceLines(painter, RLs, RLIndexes)
    DrawDottedLines(painter,dotLines)
    DrawSolidLines(painter, solidLines)
    DrawPoints(painter, drawPoints)

    output_filename = os.path.join(DIR, f"{index}.jpg")
    crop.save(output_filename)

async def createReportImages(f_url = None, s_url = None, position_lists = None):
    print(f_url, s_url)
    position_lists = list(position_lists.values())
    # f_url = r"E:\WorkSpace\face-beauty-backend\UPLOADS\0.jpg"
    # s_url = r"E:\WorkSpace\face-beauty-backend\UPLOADS\1.jpg"
    # position_lists = position_list
    DIR = "./UPLOADS/" + (os.path.basename(f_url))[:-5]+"/"
    os.makedirs(DIR, exist_ok=True)
    f_points = RemakePointArrayBaseOnImgSize(f_url, position_lists[:30]) if os.path.exists(f_url) else position_lists[:30]
    s_points = RemakePointArrayBaseOnImgSize(s_url, position_lists[30:]) if os.path.exists(s_url) else position_lists[30:]
    points = f_points + s_points
    RLs = GetReferenceLines(points)
    points = CompleteMarkPoints(points, RLs)

    if os.path.exists(f_url):
        f_canvas = GetCanva(f_url)
        create_eye_separation_ratio_image(points, RLs, DIR, 0, f_canvas)
        create_facial_thirds_image(points, RLs, DIR, 1, f_canvas)
        create_lateral_canthal_tilt_image(points, RLs, DIR, 2, f_canvas)
        create_facial_width_to_height_ratio_image(points, RLs, DIR, 3, f_canvas)
        create_jaw_frontal_angle_image(points, RLs, DIR, 4, f_canvas)
        create_cheekbone_height_image(f_url, position_lists, DIR, 5)
        create_total_facial_height_to_width_ratio_image(f_url, position_lists, DIR, 6)
        create_bigonial_width_image(f_url, position_lists, DIR, 7)
        create_chin_to_philtrum_ratio_image(f_url, position_lists, DIR, 8)
        create_Neck_width__image(f_url, position_lists, DIR, 9)
        create_mouth_width_to_nose_width_ratio_image(f_url, position_lists, DIR, 10)
        create_midface_ratio_image(f_url, position_lists, DIR, 11)
        create_eyebrow_position_ratio_image(f_url, position_lists, DIR, 12)
        create_eye_spacing_ratio_image(f_url, position_lists, DIR, 13)
        create_eye_aspect_ratio_image(f_url, position_lists, DIR, 14)
        create_lower_lip_to_upper_lip_ratio_image(f_url, position_lists, DIR, 15)
        create_deviation_of_iaa_image(f_url, position_lists, DIR, 16)
        create_eyebrow_tilt_image(f_url, position_lists, DIR, 17)
        create_bitemporal_width_image(f_url, position_lists, DIR, 18)
        create_lower_third_proportion_image(f_url, position_lists, DIR, 19)
        create_ipsilateral_alar_angle_image(f_url, position_lists, DIR, 20)
        create_medial_canthal_angle_image(f_url, position_lists, DIR, 21)

    if os.path.exists(s_url):
        s_canvas = GetCanva(s_url)
        create_gonial_angle_image(points, RLs, DIR, 22, s_canvas)
        create_nasofrontal_angle_image(points, RLs, DIR, 23, s_canvas)
        create_mandibular_plane_angle_image(points, RLs, DIR, 24, s_canvas)
        create_ramus_to_mandible_ratio_image(points, RLs, DIR, 25, s_canvas)
        create_facial_convexity_glabella_image(points, RLs, DIR, 26, s_canvas)
        create_submental_cervical_angle_image(points, RLs, DIR, 27, s_canvas)
        create_nasofacial_angle_image(points, RLs, DIR, 28, s_canvas)
        create_nasolabial_angle_image(points, RLs, DIR, 29, s_canvas)
        create_orbital_vector_image(points, RLs, DIR, 30, s_canvas)
        create_total_facial_convexity_image(points, RLs, DIR, 31, s_canvas)
        create_mentolabial_angle_image(points, RLs, DIR, 32, s_canvas)
        create_facial_convexity_nasion_image(points, RLs, DIR, 33, s_canvas)
        create_nasal_projection_image(points, RLs, DIR, 34, s_canvas)
        create_nasal_w_to_h_ratio_image(points, RLs, DIR, 35, s_canvas)
        create_ricketts_e_line_image(points, RLs, DIR, 36, s_canvas)
        create_holdaway_h_line_image(points, RLs, DIR, 37, s_canvas)
        create_steiner_s_line_image(points, RLs, DIR, 38, s_canvas)
        create_burstone_line_image(points, RLs, DIR, 39, s_canvas)
        create_nasomental_angle_image(points, RLs, DIR, 40, s_canvas)
        create_gonion_to_mouth_relationship_image(points, RLs, DIR, 41, s_canvas)
        create_recession_relative_to_frankfort_plane_image(points, RLs, DIR, 42, s_canvas)
        create_browridge_inclination_angle_image(points, RLs, DIR, 43, s_canvas)
        create_nasal_tip_angle_image(points, RLs, DIR, 44, s_canvas)

# createReportImages()