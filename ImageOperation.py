from PIL import Image, ImageDraw

def draw_solid_from_p2line_parallel(draw, point1, point2, point3, point4, line_color=(255, 0, 0), line_width=4, dot_size=2):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    slope_original = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    y_intercept_original = y1 - slope_original * x1 if x2 - x1 != 0 else None

    slope_parallel = (y4 - y3) / (x4 - x3) if x4 - x3 != 0 else float('inf')
    y_intercept_parallel = y3 - slope_parallel * x3 if x4 - x3 != 0 else None

    width, height = draw.im.size
    x_min, x_max = 0, width

    # Calculate the intersection point of the original line and the parallel line
    intersection_x = (y_intercept_parallel - y_intercept_original) / (slope_original - slope_parallel)
    intersection_y = slope_original * intersection_x + y_intercept_original

    # Draw the line from point1 to the intersection point
    draw.line([(x1, y1), (int(intersection_x), int(intersection_y))], fill=line_color, width=line_width)

    # Draw the points
    draw.ellipse((point1[0] - dot_size * 2, point1[1] - dot_size * 2, point1[0] + dot_size * 2, point1[1] + dot_size * 2), line_color)
    draw.ellipse((point2[0] - dot_size * 2, point2[1] - dot_size * 2, point2[0] + dot_size * 2, point2[1] + dot_size * 2), line_color)
    draw.ellipse((point3[0] - dot_size * 2, point3[1] - dot_size * 2, point3[0] + dot_size * 2, point3[1] + dot_size * 2), line_color)
    draw.ellipse((point4[0] - dot_size * 2, point4[1] - dot_size * 2, point4[0] + dot_size * 2, point4[1] + dot_size * 2), line_color)
def find_line_coefficients(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    parallel_y_intercept = y3 - slope * x3
    return slope, parallel_y_intercept

def find_line(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    parallel_y_intercept = y2 - slope * x2
    return slope, parallel_y_intercept

def find_perpendicular_line_coefficients(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    slope_original = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    slope_perpendicular = -1 / slope_original if slope_original != 0 else float('inf')
    perpendicular_y_intercept = y3 - slope_perpendicular * x3
    return slope_perpendicular, perpendicular_y_intercept


def get_vertical_line_from_point(x0, y0, a, b):
    slope = a
    slope_perpendicular = -1 / slope if slope != 0 else float('inf')
    if slope == 0:
        return float('inf'), x0
    a_perpendicular = slope_perpendicular
    b_perpendicular = -slope_perpendicular * x0 + y0
    return a_perpendicular, b_perpendicular

def draw_line_to_intersection(draw, x0, y0, a, b, line_color=(0, 255, 0), line_width=4, dot_size=2):
    if a == 0:
        # Original line is horizontal, draw a vertical line
        draw.line([(x0, y0), (x0, b)], fill=line_color, width=line_width)

        # Draw points
        draw.ellipse((x0 - dot_size, y0 - dot_size, x0 + dot_size, y0 + dot_size), (255,0,0))
        draw.ellipse((x0 - dot_size, b - dot_size, x0 + dot_size, b + dot_size), (255,0,0))
    elif abs(a) == float('inf'):
        # Original line is vertical, draw a horizontal line
        draw.line([(x0, y0), (b, y0)], fill=line_color, width=line_width)

        # Draw points
        draw.ellipse((x0 - dot_size, y0 - dot_size, x0 + dot_size, y0 + dot_size), (255,0,0))
        draw.ellipse((b - dot_size, y0 - dot_size, b + dot_size, y0 + dot_size), (255,0,0))
    else:
        # Calculate perpendicular line coefficients
        a_perpendicular, b_perpendicular = get_vertical_line_from_point(x0, y0, a, b)

        # Calculate intersection point
        intersection_x = (b_perpendicular - b) / (a - a_perpendicular)
        intersection_y = a * intersection_x + b

        # Draw the line from (x0, y0) to the intersection point
        draw.line([(x0, y0), (int(intersection_x), int(intersection_y))], fill=line_color, width=line_width)

        # Draw points
        draw.ellipse((x0 - dot_size, y0 - dot_size, x0 + dot_size, y0 + dot_size), (255,0,0))
        draw.ellipse((int(intersection_x) - dot_size, int(intersection_y) - dot_size,
                      int(intersection_x) + dot_size, int(intersection_y) + dot_size), (255,0,0))

def find_intersection_point(point1, point2, point3, point4):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4
    print(x1,y1,x2,y2,x3,y3,x4,y4)
    slope1 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    slope2 = (y4 - y3) / (x4 - x3) if x4 - x3 != 0 else float('inf')
    print(slope1, slope2)
    if slope1 == slope2:
        return None  
    intersection_x = (slope1 * x1 - slope2 * x3 + y3 - y1) / (slope1 - slope2)
    intersection_y = slope1 * (intersection_x - x1) + y1
    return intersection_x, intersection_y

def find_intersection_point_vertical(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    if x2 == x3:
        return x2, y1
    slope_line = (y3 - y2) / (x3 - x2)
    y_intercept_line = y2 - slope_line * x2
    intersection_x = x1
    intersection_y = slope_line * intersection_x + y_intercept_line

    return intersection_x, intersection_y