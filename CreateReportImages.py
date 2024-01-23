from PIL import Image, ImageDraw
import numpy as np
import os
import ImageOperation

position_lists = [
    [
      { "x": 0, "y": 0 },
      { "x": 0, "y": 0 },
    ],
    [
      { "x": 375, "y": 164 },
      { "x": 375, "y": 164 },
    ], #1
    [
      { "x": 253, "y": 220 },
      { "x": 484, "y": 223 },
    ], #2
    [
      { "x": 272, "y": 270 },
      { "x": 464, "y": 272 },
    ], #3
    [
      { "x": 272, "y": 280 },
      { "x": 464, "y": 282 },
    ], #4
    [
      { "x": 368, "y": 284 },
      { "x": 368, "y": 284 },
    ], #5
    [
      { "x": 368, "y": 304 },
      { "x": 368, "y": 304 },
    ], #6
    [
      { "x": 335, "y": 294 },
      { "x": 398, "y": 294 },
    ], #7
    [
      { "x": 335, "y": 309 },
      { "x": 398, "y": 309 },
    ], #8
    [
      { "x": 270, "y": 324 },
      { "x": 471, "y": 325 },
    ], #9
    [
      { "x": 293, "y": 316 },
      { "x": 446, "y": 318 },
    ], #10
    [
      { "x": 275, "y": 329 },
      { "x": 466, "y": 330 },
    ], #11
    [
      { "x": 303, "y": 326 },
      { "x": 436, "y": 327 },
    ], #12
    [
      { "x": 325, "y": 326 },
      { "x": 415, "y": 327 },
    ], #13
    [
      { "x": 293, "y": 339 },
      { "x": 446, "y": 340 },
    ], #14
    [
      { "x": 313, "y": 339 },
      { "x": 426, "y": 340 },
    ], #15
    [
      { "x": 333, "y": 339 },
      { "x": 406, "y": 340 },
    ], #16
    [
      { "x": 225, "y": 349 },
      { "x": 530, "y": 351 },
    ], #17
    [
      { "x": 333, "y": 419 },
      { "x": 406, "y": 422 },
    ], #18
    [
      { "x": 370, "y": 450 },
      { "x": 370, "y": 450 },
    ], #19
    [
      { "x": 380, "y": 440 },
      { "x": 380, "y": 440 },
    ], #20
    [
      { "x": 380, "y": 470 },
      { "x": 380, "y": 470 },
    ], #21
    [
      { "x": 252, "y": 472 },
      { "x": 505, "y": 475 },
    ], #22
    [
      { "x": 318, "y": 482 },
      { "x": 430, "y": 482 },
    ], #23
    [
      { "x": 371, "y": 484 },
      { "x": 371, "y": 484 },
    ], #24
    [
      { "x": 371, "y": 504 },
      { "x": 371, "y": 504 },
    ], #25
    [
      { "x": 270, "y": 494 },
      { "x": 495, "y": 494 },
    ], #26
    [
      { "x": 275, "y": 514 },
      { "x": 493, "y": 524 },
    ], #27
    [
      { "x": 328, "y": 557 },
      { "x": 420, "y": 557 },
    ], #28
    [
      { "x": 370, "y": 565 },
      { "x": 370, "y": 565 },
    ], #29
    [{ "x": 244, "y": 190 }], #30
    [{ "x": 225, "y": 226 }], #31
    [{ "x": 215, "y": 292 }], #32
    [{ "x": 235, "y": 327 }], #33
    [{ "x": 225, "y": 332 }], #34
    [{ "x": 218, "y": 334 }], #35
    [{ "x": 190, "y": 375 }], #36
    [{ "x": 260, "y": 375 }], #37
    [{ "x": 400, "y": 375 }], #38
    [{ "x": 170, "y": 400 }], #39
    [{ "x": 168, "y": 405 }], #40
    [{ "x": 175, "y": 422 }], #41
    [{ "x": 225, "y": 417 }], #42
    [{ "x": 195, "y": 435 }], #43
    [{ "x": 200, "y": 440 }], #44
    [{ "x": 200, "y": 460 }], #45
    [{ "x": 237, "y": 472 }], #46
    [{ "x": 210, "y": 484 }], #47
    [{ "x": 220, "y": 500 }], #48
    [{ "x": 385, "y": 484 }], #49
    [{ "x": 220, "y": 530 }], #50
    [{ "x": 240, "y": 552 }], #51
    [{ "x": 258, "y": 554 }], #52
    [{ "x": 320, "y": 560 }], #53
    [{ "x": 220, "y": 570 }], #54
    [{ "x": 352, "y": 655 }], #55
    [{ "x": 168, "y": 327 }], #56
    [{ "x": 235, "y": 352 }], #57
    [{ "x": 210, "y": 494 }], #58
    [{ "x": 185, "y": 428 }], #59
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

def draw_parallel_line(draw, point1, point2, point3, line_color=(57, 208, 192), line_width=1, dot_size=2):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    y_intercept = y1 - slope * x1 if x2 - x1 != 0 else None
    parallel_y_intercept = y3 - slope * x3
    width, height = draw.im.size
    x_min, x_max = 0, width
    if slope == float('inf'):
        draw.line([(x1, 0), (x1, height)], fill=line_color, width=line_width)
    else:
        draw.line([(x_min, int(slope * x_min + y_intercept)), (x_max, int(slope * x_max + y_intercept))], fill=line_color, width=line_width)
        draw.line([(x_min, int(slope * x_min + parallel_y_intercept)), (x_max, int(slope * x_max + parallel_y_intercept))], fill=line_color, width=line_width)
    
    draw.ellipse((point1[0] - dot_size * 2, point1[1] - dot_size * 2, point1[0] + dot_size * 2, point1[1] + dot_size * 2), (255, 0, 0))
    draw.ellipse((point2[0] - dot_size * 2, point2[1] - dot_size * 2, point2[0] + dot_size * 2, point2[1] + dot_size * 2), (255, 0, 0))
    draw.ellipse((point3[0] - dot_size * 2, point3[1] - dot_size * 2, point3[0] + dot_size * 2, point3[1] + dot_size * 2), (255, 0, 0))
def draw_vertical_line_(draw, point1, point2, point3, line_color=(57, 208, 192), line_width=1, dot_size=2):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    y_intercept = y1 - slope * x1 if x2 - x1 != 0 else None
    width, height = draw.im.size
    x_min, x_max = 0, width
    if slope == 0:  # If the original line is horizontal
        draw.line([(x3, 0), (x3, height)], fill=line_color, width=line_width)
    elif slope == float('inf'):  # If the original line is vertical
        draw.line([(0, y3), (width, y3)], fill=line_color, width=line_width)
    else:
        perpendicular_slope = -1 / slope
        perpendicular_y_intercept = y3 - perpendicular_slope * x3
        draw.line(
            [(x_min, int(perpendicular_slope * x_min + perpendicular_y_intercept)),
             (x_max, int(perpendicular_slope * x_max + perpendicular_y_intercept))],
            fill=line_color, width=line_width
        )
    draw_infinite_line(draw, (x1, y1), (x2, y2))
    draw.ellipse((point1[0] - dot_size * 2, point1[1] - dot_size * 2, point1[0] + dot_size * 2, point1[1] + dot_size * 2),(255, 0, 0))
    draw.ellipse((point2[0] - dot_size * 2, point2[1] - dot_size * 2, point2[0] + dot_size * 2, point2[1] + dot_size * 2),(255, 0, 0))
    draw.ellipse((point3[0] - dot_size * 2, point3[1] - dot_size * 2, point3[0] + dot_size * 2, point3[1] + dot_size * 2),(255, 0, 0))

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
    print(point1, point2)
    draw.line([(point1[0], point1[1]), (point2[0], point1[1])], fill=line_color, width=line_width)
    draw.ellipse((point1[0]-dot_size*2, point1[1]-dot_size*2, point1[0]+dot_size*2, point1[1]+dot_size*2), (255, 0, 0))

def draw_solid_line_p_horizontal_line(draw, point1, point2, line_color=(0, 255, 0), line_width=4, dot_size=2):
    print(point1, point2)
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
def create_eye_separation_ratio_create(img_url, mark_points, DIR, index):
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
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True
#2
def create_facial_thirds_image(img_url, mark_points, DIR, index):
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
    x2 = mark_points[5][0]["x"]
    y2 = mark_points[5][0]["y"]
    x3 = mark_points[19][0]["x"]
    y3 = mark_points[19][0]["y"]
    x4 = mark_points[29][0]["x"]
    y4 = mark_points[29][0]["y"]
    

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
    draw.line((x4,y4,x4,y1), fill=(0,255,0), width=1)
    draw_vertical_line(draw, (x4, y4))
    draw_horizontal_line(draw, (x1,y1))
    draw_horizontal_line(draw, (x2,y2))
    draw_horizontal_line(draw, (x3,y3))
    draw_horizontal_line(draw, (x4,y4))
    draw_dotted_line(draw, (x4, y1), (x4, y2), dot_color=(255, 0, 0))
    draw_dotted_line(draw, (x4, y2), (x4, y3), dot_color=(0, 255, 0))
    draw_dotted_line(draw, (x4, y3), (x4, y4), dot_color=(0, 0, 255))
    output_filename = os.path.join(DIR, f"{create_facial_thirds_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    

    return True
#3
def create_lateral_canthal_tilt_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[11][0]["x"]
    y1 = mark_points[11][0]["y"]
    x2 = mark_points[16][0]["x"]
    y2 = mark_points[16][0]["y"]
    x3 = mark_points[16][1]["x"]
    y3 = mark_points[16][1]["y"]
    x4 = mark_points[11][1]["x"]
    y4 = mark_points[11][1]["y"]
    

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
    draw.ellipse((x1-3, y1-3, x1+3, y1+3), fill=(255, 0, 0))
    draw.ellipse((x2-3, y2-3, x2+3, y2+3), fill=(255, 0, 0))
    draw.ellipse((x3-3, y3-3, x3+3, y3+3), fill=(255, 0, 0))
    draw.ellipse((x4-3, y4-3, x4+3, y4+3), fill=(255, 0, 0))
    draw_dotted_line(draw, [x2,y2], [x1,y1])
    draw_dotted_line(draw, [x3,y3], [x4,y4])
    draw_infinite_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{create_lateral_canthal_tilt_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True
#4
def create_facial_width_to_height_ratio_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[6][0]["x"]
    y1 = mark_points[6][0]["y"]
    x2 = mark_points[21][0]["x"]
    y2 = mark_points[21][0]["y"]
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
    draw_horizontal_line(draw, (x2, y2))
    draw_horizontal_line(draw, (x1, y1))
    draw_dotted_line(draw, (x3, y3), (x4, y4))
    draw_solid_line(draw, (x1, y1), (x1, y2))
    output_filename = os.path.join(DIR, f"{create_facial_width_to_height_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True
#5
def create_jaw_frontal_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[26][0]["x"]
    y1 = mark_points[26][0]["y"]
    x2 = mark_points[28][0]["x"]
    y2 = mark_points[28][0]["y"]
    x3 = mark_points[28][1]["x"]
    y3 = mark_points[28][1]["y"]
    x4 = mark_points[26][1]["x"]
    y4 = mark_points[26][1]["y"]
    

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
    intersection_point = find_intersection([(x1,y1),(x2,y2)], [(x3,y3),(x4,y4)])
    draw_dotted_line(draw, (x1, y1), (intersection_point[0],intersection_point[1]))
    draw_dotted_line(draw, (x4, y4), (intersection_point[0],intersection_point[1]))

    output_filename = os.path.join(DIR, f"{create_jaw_frontal_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True
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
    draw_horizontal_line(draw, (x4, y4))
    draw_dotted_line(draw, (x1, y1), (x1, y2))
    draw_solid_line(draw, (x3, y3), (x3, y4))
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
def create_gonial_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[38][0]["x"]
    y1 = mark_points[38][0]["y"]
    x2 = mark_points[49][0]["x"]
    y2 = mark_points[49][0]["y"]
    x3 = mark_points[52][0]["x"]
    y3 = mark_points[52][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    draw.ellipse((x1-3, y1-3, x1+3, y1+3), fill=(255, 0, 0))
    draw.ellipse((x2-3, y2-3, x2+3, y2+3), fill=(255, 0, 0))
    draw.ellipse((x3-3, y3-3, x3+3, y3+3), fill=(255, 0, 0))
    output_filename = os.path.join(DIR, f"{create_gonial_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#24
def create_nasofrontal_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[32][0]["x"]
    y1 = mark_points[32][0]["y"]
    x2 = mark_points[35][0]["x"]
    y2 = mark_points[35][0]["y"]
    x3 = mark_points[39][0]["x"]
    y3 = mark_points[39][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    draw.ellipse((x1-3, y1-3, x1+3, y1+3), fill=(255, 0, 0))
    draw.ellipse((x2-3, y2-3, x2+3, y2+3), fill=(255, 0, 0))
    draw.ellipse((x3-3, y3-3, x3+3, y3+3), fill=(255, 0, 0))
    output_filename = os.path.join(DIR, f"{create_nasofrontal_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#25
def create_mandibular_plane_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[47][0]["x"]
    y1 = mark_points[47][0]["y"]
    x2 = mark_points[49][0]["x"]
    y2 = mark_points[49][0]["y"]
    x3 = mark_points[52][0]["x"]
    y3 = mark_points[52][0]["y"]
    x4 = mark_points[37][0]["x"]
    y4 = mark_points[37][0]["y"]
    x5 = mark_points[38][0]["x"]
    y5 = mark_points[38][0]["y"]
    
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
    draw_parallel_line(draw, (x4, y4), (x5, y5), (x2, y2))
    draw_dotted_line(draw, (x2, y2), (x3, y3))

    output_filename = os.path.join(DIR, f"{create_mandibular_plane_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#26
def create_ramus_to_mandible_ratio_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[38][0]["x"]
    y1 = mark_points[38][0]["y"]
    x2 = mark_points[49][0]["x"]
    y2 = mark_points[49][0]["y"]
    x3 = mark_points[50][0]["x"]
    y3 = mark_points[50][0]["y"]
    x4 = mark_points[37][0]["x"]
    y4 = mark_points[37][0]["y"]
    x5 = mark_points[38][0]["x"]
    y5 = mark_points[38][0]["y"]
    x6 = mark_points[52][0]["x"]
    y6 = mark_points[52][0]["y"]
    x7,y7 = ImageOperation.find_intersection_point_vertical((x3,y3),(x6,y6),(x2,y2))
    print(x7,y7)
    

    x_min = min(x1,x2,x3,x4,x5,x6,x7)
    x_max = max(x1,x2,x3,x4,x5,x6,x7)
    y_min = min(y1,y2,y3,y4,y5,y6,y7)
    y_max = max(y1,y2,y3,y4,y5,y6,y7)
    
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
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5),(x6,y6),(x7,y7)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5),(x6,y6),(x7,y7)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_solid_line(draw, (x2, y2), (x7, y7))
    draw_vertical_line_(draw, (x4, y4), (x5, y5), (x3, y3))
    draw_dotted_line(draw, (x1, y1), (x2, y2))
    draw_point(draw, (x6, y6))
    
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#27
def create_facial_convexity_glabella_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[32][0]["x"]
    y1 = mark_points[32][0]["y"]
    x2 = mark_points[43][0]["x"]
    y2 = mark_points[43][0]["y"]
    x3 = mark_points[50][0]["x"]
    y3 = mark_points[50][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#28
def create_submental_cervical_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[51][0]["x"]
    y1 = mark_points[51][0]["y"]
    x2 = mark_points[53][0]["x"]
    y2 = mark_points[53][0]["y"]
    x3 = mark_points[55][0]["x"]
    y3 = mark_points[55][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{create_submental_cervical_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#29
def create_nasofacial_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[39][0]["x"]
    y1 = mark_points[39][0]["y"]
    x2 = mark_points[35][0]["x"]
    y2 = mark_points[35][0]["y"]
    x3 = mark_points[50][0]["x"]
    y3 = mark_points[50][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{create_nasofacial_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#30
def create_nasolabial_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[41][0]["x"]
    y1 = mark_points[41][0]["y"]
    x2 = mark_points[44][0]["x"]
    y2 = mark_points[44][0]["y"]
    x3 = mark_points[45][0]["x"]
    y3 = mark_points[45][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{create_nasolabial_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#31
def create_orbital_vector_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[33][0]["x"]
    y1 = mark_points[33][0]["y"]
    x2 = mark_points[38][0]["x"]
    y2 = mark_points[38][0]["y"]
    x3 = mark_points[36][0]["x"]
    y3 = mark_points[36][0]["y"]
    x4 = mark_points[37][0]["x"]
    y4 = mark_points[37][0]["y"]
    x5 = mark_points[57][0]["x"]
    y5 = mark_points[57][0]["y"]
    draw_vertical_line_(draw, (x4, y4), (x2, y2), (x1, y1))
    draw_solid_line_p_vertical_line(draw, (x5, y5), (x1, y1))

    
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
    output_filename = os.path.join(DIR, f"{create_total_facial_convexity_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#32
def create_total_facial_convexity_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[32][0]["x"]
    y1 = mark_points[32][0]["y"]
    x2 = mark_points[40][0]["x"]
    y2 = mark_points[40][0]["y"]
    x3 = mark_points[50][0]["x"]
    y3 = mark_points[50][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{create_total_facial_convexity_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#33???
def create_mentolabial_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[58][0]["x"]
    y1 = mark_points[58][0]["y"]
    x2 = mark_points[48][0]["x"]
    y2 = mark_points[48][0]["y"]
    x3 = mark_points[50][0]["x"]
    y3 = mark_points[50][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{create_mentolabial_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#34
def create_facial_convexity_nasion_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[35][0]["x"]
    y1 = mark_points[35][0]["y"]
    x2 = mark_points[43][0]["x"]
    y2 = mark_points[43][0]["y"]
    x3 = mark_points[50][0]["x"]
    y3 = mark_points[50][0]["y"]
    

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
    draw_dotted_line(draw, (x2, y2), (x3, y3))
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#35
def create_nasal_projection_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[40][0]["x"]
    y1 = mark_points[40][0]["y"]
    x2 = mark_points[36][0]["x"]
    y2 = mark_points[36][0]["y"]
    x3 = mark_points[35][0]["x"]
    y3 = mark_points[35][0]["y"]
    x4 = mark_points[42][0]["x"]
    y4 = mark_points[42][0]["y"]
    x5 = x4
    y5 = (x3*y2-x4*y2+x4*y3-x2*y3)/(x3-x2)
    x6 = mark_points[37][0]["x"]
    y6 = mark_points[37][0]["y"]
    x7 = mark_points[38][0]["x"]
    y7 = mark_points[38][0]["y"]

    x_min = min(x1,x2,x3,x4,x5,x6,x7)
    x_max = max(x1,x2,x3,x4,x5,x6,x7)
    y_min = min(y1,y2,y3,y4,y5,y6,y7)
    y_max = max(y1,y2,y3,y4,y5,y6,y7)
    
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
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7)] = rescale((start_x, start_y), width,  [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_vertical_line_(draw, (x6, y6), (x7, y7), (x4, y4))
    draw_dotted_line(draw, (x1, y1), (x4, y1))
    draw_solid_line(draw, (x1, y1), (x5, y5))
    draw_point(draw, (x2, y2))
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#36
def create_nasal_w_to_h_ratio_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[33][0]["x"]
    y1 = mark_points[33][0]["y"]
    x2 = mark_points[40][0]["x"]
    y2 = mark_points[40][0]["y"]
    x3 = mark_points[42][0]["x"]
    y3 = mark_points[42][0]["y"]
    x4 = mark_points[36][0]["x"]
    y4 = mark_points[36][0]["y"]
    x5 = mark_points[56][0]["x"]
    y5 = mark_points[56][0]["y"]
    x6 = mark_points[37][0]["x"]
    y6 = mark_points[37][0]["y"]
    x7 = mark_points[38][0]["x"]
    y7 = mark_points[38][0]["y"]
    

    x_min = min(x1,x2,x3,x4,x5,x6,x7)
    x_max = max(x1,x2,x3,x4,x5,x6,x7)
    y_min = min(y1,y2,y3,y4,y5,y6,y7)
    y_max = max(y1,y2,y3,y4,y5,y6,y7)
    
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
    [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7)])
    draw = ImageDraw.Draw(cropped_img) 
    draw_infinite_line(draw, (x6, y6), (x7, y7))
    draw_parallel_line(draw, (x6, y6), (x7, y7), (x1, y1))
    draw_vertical_line_(draw, (x6, y6), (x7, y7), (x3, y3))
    draw_vertical_line_(draw, (x6, y6), (x7, y7), (x2, y2))
    a, b = ImageOperation.find_line_coefficients((x6, y6), (x7, y7), (x1, y1))
    ImageOperation.draw_line_to_intersection(draw, x2, y2, a, b)
    a, b = ImageOperation.find_perpendicular_line_coefficients((x6, y6), (x7, y7), (x3, y3))
    if a != float('inf'):
        ImageOperation.draw_line_to_intersection(draw, x2, y2, a, b)
    else:
        draw_dotted_line(draw, (x2, y2), (x3, y2))
    output_filename = os.path.join(DIR, f"{create_nasal_w_to_h_ratio_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#37
def create_ricketts_e_line_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[40][0]["x"]
    y1 = mark_points[40][0]["y"]
    x2 = mark_points[50][0]["x"]
    y2 = mark_points[50][0]["y"]
    x3 = mark_points[45][0]["x"]
    y3 = mark_points[45][0]["y"]
    x4 = mark_points[47][0]["x"]
    y4 = mark_points[47][0]["y"]

    x_min = min(x1,x2)
    x_max = max(x1,x2)
    y_min = min(y1,y2)
    y_max = max(y1,y2)
    
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
    draw_point(draw, (x3, y3))
    draw_point(draw, (x4, y4))
    output_filename = os.path.join(DIR, f"{create_ricketts_e_line_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#38
def create_holdaway_h_line_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[45][0]["x"]
    y1 = mark_points[45][0]["y"]
    x2 = mark_points[50][0]["x"]
    y2 = mark_points[50][0]["y"]
    

    x_min = min(x1,x2)
    x_max = max(x1,x2)
    y_min = min(y1,y2)
    y_max = max(y1,y2)
    
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
    [(x1, y1), (x2, y2)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2)])
    draw = ImageDraw.Draw(cropped_img) 
    draw_dotted_line(draw, (x1, y1), (x2, y2))
    output_filename = os.path.join(DIR, f"{create_holdaway_h_line_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#39??????????
def create_steiner_s_line_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[59][0]["x"]
    y1 = mark_points[59][0]["y"]
    x2 = mark_points[50][0]["x"]
    y2 = mark_points[50][0]["y"]
    x3 = mark_points[45][0]["x"]
    y3 = mark_points[45][0]["y"]
    x4 = mark_points[47][0]["x"]
    y4 = mark_points[47][0]["y"]
    

    x_min = min(x1,x2)
    x_max = max(x1,x2)
    y_min = min(y1,y2)
    y_max = max(y1,y2)
    
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
    draw_point(draw, (x3, y3))
    draw_point(draw, (x4, y4))
    output_filename = os.path.join(DIR, f"{create_steiner_s_line_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#40
def create_burstone_line_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[43][0]["x"]
    y1 = mark_points[43][0]["y"]
    x2 = mark_points[50][0]["x"]
    y2 = mark_points[50][0]["y"]
    

    x_min = min(x1,x2)
    x_max = max(x1,x2)
    y_min = min(y1,y2)
    y_max = max(y1,y2)
    
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
    [(x1, y1), (x2, y2)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_dotted_line(draw, (x1, y1), (x2, y2))
    output_filename = os.path.join(DIR, f"{create_burstone_line_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#41
def create_nasomental_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[35][0]["x"]
    y1 = mark_points[35][0]["y"]
    x2 = mark_points[40][0]["x"]
    y2 = mark_points[40][0]["y"]
    x3 = mark_points[50][0]["x"]
    y3 = mark_points[50][0]["y"]
    

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
    draw_dotted_line(draw, (x1,  y1), (x2, y2))
    draw_dotted_line(draw, (x3,  y3), (x2, y2))
    output_filename = os.path.join(DIR, f"{create_nasomental_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#42
def create_gonion_to_mouth_relationship_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[46][0]["x"]
    y1 = mark_points[46][0]["y"]
    x2 = mark_points[49][0]["x"]
    y2 = mark_points[49][0]["y"]    
    x4 = mark_points[37][0]["x"]
    y4 = mark_points[37][0]["y"]
    x5 = mark_points[38][0]["x"]
    y5 = mark_points[38][0]["y"]
    

    x_min = min(x1,x2,x4,x5)
    x_max = max(x1,x2,x4,x5)
    y_min = min(y1,y2,y4,y5)
    y_max = max(y1,y2,y4,y5)
    
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
    [(x1, y1), (x2, y2), (x4, y4), (x5, y5)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2), (x4, y4), (x5, y5)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_parallel_line(draw, (x4, y4), (x5, y5), (x1, y1))
    a, b = ImageOperation.find_line_coefficients((x4, y4), (x5, y5), (x1, y1))
    ImageOperation.draw_line_to_intersection(draw, x2, y2, a, b)
    output_filename = os.path.join(DIR, f"{create_gonion_to_mouth_relationship_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#43
def create_recession_relative_to_frankfort_plane_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[35][0]["x"]
    y1 = mark_points[35][0]["y"]
    x2 = mark_points[50][0]["x"]
    y2 = mark_points[50][0]["y"]
    x3 = mark_points[36][0]["x"]
    y3 = mark_points[36][0]["y"]
    x4 = mark_points[37][0]["x"]
    y4 = mark_points[37][0]["y"]
    x5 = mark_points[38][0]["x"]
    y5 = mark_points[38][0]["y"]

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
    draw_infinite_line(draw, (x5, y5), (x4, y4))
    draw_vertical_line_(draw, (x4, y4), (x5, y5), (x2, y2))
    a, b = ImageOperation.find_perpendicular_line_coefficients((x4, y4), (x5, y5), (x2, y2))
    print(a, b)
    if a == float('inf'):
        draw_solid_line_p_vertical_line(draw, (x1, y1), (x2, y2))
    else:
        ImageOperation.draw_line_to_intersection(draw, x1, y1, a, b)
    output_filename = os.path.join(DIR, f"{create_recession_relative_to_frankfort_plane_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#44
def create_browridge_inclination_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[32][0]["x"]
    y1 = mark_points[32][0]["y"]
    x2 = mark_points[31][0]["x"]
    y2 = mark_points[31][0]["y"]
    x4 = mark_points[37][0]["x"]
    y4 = mark_points[37][0]["y"]
    x5 = mark_points[38][0]["x"]
    y5 = mark_points[38][0]["y"]
    

    x_min = min(x1,x2)
    x_max = max(x1,x2)
    y_min = min(y1,y2,y1/3*2)
    y_max = max(y1,y2)
    
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
    [(x1, y1), (x2, y2)] = rescale((start_x, start_y), width, [(x1, y1), (x2, y2)])
    draw = ImageDraw.Draw(cropped_img)  
    draw_vertical_line_(draw, (x4, y4), (x5, y5), (x1, y1))
    draw_dotted_line(draw, (x2, y2), (x1, y1))

    output_filename = os.path.join(DIR, f"{create_browridge_inclination_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

#45
def create_nasal_tip_angle_image(img_url, mark_points, DIR, index):
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

    x1 = mark_points[39][0]["x"]
    y1 = mark_points[39][0]["y"]
    x2 = mark_points[40][0]["x"]
    y2 = mark_points[40][0]["y"]
    x3 = mark_points[41][0]["x"]
    y3 = mark_points[41][0]["y"]
    

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
    draw_dotted_line(draw, (x3, y3), (x2, y2))
    output_filename = os.path.join(DIR, f"{create_nasal_tip_angle_image.__name__}.jpg")
    output_filename = os.path.join(DIR, f"{index}.jpg")
    cropped_img.save(output_filename)
    return True

async def createReportImages(front_img_url, side_img_url, position_lists):
    position_lists = list(position_lists.values())
    DIR = "./REPORTS/" + (os.path.basename(front_img_url))[:-6]+"/"
    os.makedirs(DIR, exist_ok=True)

    create_eye_separation_ratio_create(front_img_url, position_lists, DIR, 1) 
    create_facial_thirds_image(front_img_url, position_lists, DIR, 2)       
    create_lateral_canthal_tilt_image(front_img_url, position_lists, DIR, 3)
    create_facial_width_to_height_ratio_image(front_img_url, position_lists, DIR, 4)
    create_jaw_frontal_angle_image(front_img_url, position_lists, DIR, 5)
    create_cheekbone_height_image(front_img_url, position_lists, DIR, 6)
    create_total_facial_height_to_width_ratio_image(front_img_url, position_lists, DIR, 7)
    create_bigonial_width_image(front_img_url, position_lists, DIR, 8)
    create_chin_to_philtrum_ratio_image(front_img_url, position_lists, DIR, 9)
    create_Neck_width__image(front_img_url, position_lists, DIR, 10)
    create_mouth_width_to_nose_width_ratio_image(front_img_url, position_lists, DIR, 11)
    create_midface_ratio_image(front_img_url, position_lists, DIR, 12)
    create_eyebrow_position_ratio_image(front_img_url, position_lists, DIR, 13)
    create_eye_spacing_ratio_image(front_img_url, position_lists, DIR, 14)
    create_eye_aspect_ratio_image(front_img_url, position_lists, DIR, 15)
    create_lower_lip_to_upper_lip_ratio_image(front_img_url, position_lists, DIR, 16)
    create_deviation_of_iaa_image(front_img_url, position_lists, DIR, 17)
    create_eyebrow_tilt_image(front_img_url, position_lists, DIR, 18)
    create_bitemporal_width_image(front_img_url, position_lists, DIR, 19)
    create_lower_third_proportion_image(front_img_url, position_lists, DIR, 20)
    create_ipsilateral_alar_angle_image(front_img_url, position_lists, DIR, 21)
    create_medial_canthal_angle_image(front_img_url, position_lists, DIR, 22)

    ###Side Functions
    create_gonial_angle_image(side_img_url, position_lists, DIR, 23)
    create_nasofrontal_angle_image(side_img_url, position_lists, DIR, 24)
    create_mandibular_plane_angle_image(side_img_url, position_lists, DIR, 25)
    create_ramus_to_mandible_ratio_image(side_img_url, position_lists, DIR, 26)
    create_facial_convexity_glabella_image(side_img_url, position_lists, DIR, 27)
    create_submental_cervical_angle_image(side_img_url, position_lists, DIR, 28)
    create_nasofacial_angle_image(side_img_url, position_lists, DIR, 29)
    create_nasolabial_angle_image(side_img_url, position_lists, DIR, 30)
    create_orbital_vector_image(side_img_url, position_lists, DIR, 31)
    create_total_facial_convexity_image(side_img_url, position_lists, DIR, 32)
    create_mentolabial_angle_image(side_img_url, position_lists, DIR, 33)
    create_facial_convexity_nasion_image(side_img_url, position_lists, DIR, 34)
    create_nasal_projection_image(side_img_url, position_lists, DIR, 35)
    create_nasal_w_to_h_ratio_image(side_img_url, position_lists, DIR, 36)
    create_ricketts_e_line_image(side_img_url, position_lists, DIR, 37)
    create_holdaway_h_line_image(side_img_url, position_lists, DIR, 38)
    create_steiner_s_line_image(side_img_url, position_lists, DIR, 39)
    create_burstone_line_image(side_img_url, position_lists, DIR, 40)
    create_nasomental_angle_image(side_img_url, position_lists, DIR, 41)
    create_gonion_to_mouth_relationship_image(side_img_url, position_lists, DIR, 42)
    create_recession_relative_to_frankfort_plane_image(side_img_url, position_lists, DIR, 43)
    create_browridge_inclination_angle_image(side_img_url, position_lists, DIR, 44)
    create_nasal_tip_angle_image(side_img_url, position_lists, DIR, 45)

create_ramus_to_mandible_ratio_image("./side.jpg", position_lists, "./REPORTS", 21)