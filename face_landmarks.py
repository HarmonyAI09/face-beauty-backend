import cv2
import dlib
import numpy as np
import mediapipe as mp

def get_vector_parameters(x1, y1, x2, y2):
    A = (y1 - y2) / (x1 - x2)
    B = y1 - x1 * A
    return A, B

def get_crosss_point(x1, y1, x2, y2, x3, y3, x4, y4):
    A1, B1 = get_vector_parameters(x1, y1, x2, y2)
    A2, B2 = get_vector_parameters(x3, y3, x4, y4)
    X = (B2 - B1) / (A1 - A2)
    Y = A1 * X + B1
    return X, Y

def process_image(image_path):
    result_points = np.zeros((30, 2, 2))
    good_index_in_81 = [
        [72, 1, 0],
        [72, 1, 1],
        [37, 11, 0],
        [46, 11, 1],
    ]
    good_index_in_mediapipe = [
        [103, 2, 0],
        [332, 2, 1],
        [9, 5, 0],
        [9, 5, 1],
        [8, 6, 0],
        [8, 6, 1],
        [112, 16, 0],
        [341, 16, 1],
        [219, 18, 0],
        [455, 18, 1],
        [145, 14, 0],
        [374, 14, 1],
        [154, 15, 0],
        [381, 15, 1],
        [159, 10, 0],
        [386, 10, 1],
        [247, 9, 0],
        [467, 9, 1],
        [157, 13, 0],
        [384, 13, 1],
        [2, 19, 0],
        [2, 19, 1],
        [326, 20, 0],
        [326, 20, 1],
        [267, 21, 0],
        [267, 21, 1],
        [152, 29, 0],
        [152, 29, 1],
        [148, 28, 0],
        [377, 28, 1],
        [172, 26, 0],
        [397, 26, 1],
        [58, 22, 0],
        [288, 22, 1],
        [17, 25, 0],
        [17, 25, 1],
        [14, 24, 0],
        [14, 24, 1],
        [61, 23, 0],
        [291, 23, 1],
        [227, 17, 0],
        [454, 17, 1],
    ]

    image = cv2.imread(image_path)
    kernel_size = (5, 5)
    blurred = cv2.GaussianBlur(image, kernel_size, 0)
    image = cv2.addWeighted(image, 1 + 1, blurred, -1, 0)
    height, width, channels = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    p1 = "shape_predictor_68_face_landmarks.dat"
    p2 = "shape_predictor_81_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor1 = dlib.shape_predictor(p1)
    predictor2 = dlib.shape_predictor(p2)
    rects = detector(gray, 0)
    for i, rect in enumerate(rects):
        shape1 = predictor1(gray, rect)
        shape1 = np.array([[p.x, p.y] for p in shape1.parts()])
        result_points[12, 0, 0] = (shape1[38][0] + shape1[41][0]) / 2
        result_points[12, 0, 1] = (shape1[38][1] + shape1[41][1]) / 2
        result_points[12, 1, 0] = (shape1[44][0] + shape1[47][0]) / 2
        result_points[12, 1, 1] = (shape1[44][1] + shape1[47][1]) / 2
        shape2 = predictor2(gray, rect)
        shape2 = np.array([[p.x, p.y] for p in shape2.parts()])
        for index in range(len(good_index_in_81)):
            result_points[
                good_index_in_81[index][1], good_index_in_81[index][2], 0
            ] = shape2[good_index_in_81[index][0] - 1][0]
            result_points[
                good_index_in_81[index][1], good_index_in_81[index][2], 1
            ] = shape2[good_index_in_81[index][0] - 1][1]

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    mp_holistic = mp.solutions.holistic
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=2)
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.9,
    ) as face_mesh:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        h, w, _ = image.shape
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        annotated_image = image.copy()
        if results.multi_face_landmarks:
            for index in range(len(good_index_in_mediapipe)):
                result_points[
                    good_index_in_mediapipe[index][1],
                    good_index_in_mediapipe[index][2],
                    0,
                ] = int(
                    results.multi_face_landmarks[0].landmark[good_index_in_mediapipe[index][0]].x
                    * w
                )
                result_points[
                    good_index_in_mediapipe[index][1],
                    good_index_in_mediapipe[index][2],
                    1,
                ] = int(
                    results.multi_face_landmarks[0].landmark[good_index_in_mediapipe[index][0]].y
                    * h
                )
            delta = 0.005
            result_points[3, 0, 0] = int(results.multi_face_landmarks[0].landmark[105].x * w)
            result_points[3, 0, 1] = int(
                (results.multi_face_landmarks[0].landmark[105].y - delta) * h
            )
            result_points[4, 0, 0] = int(results.multi_face_landmarks[0].landmark[105].x * w)
            result_points[4, 0, 1] = int(
                (results.multi_face_landmarks[0].landmark[105].y + delta) * h
            )
            result_points[3, 1, 0] = int(results.multi_face_landmarks[0].landmark[334].x * w)
            result_points[3, 1, 1] = int(
                (results.multi_face_landmarks[0].landmark[334].y - delta) * h
            )
            result_points[4, 1, 0] = int(results.multi_face_landmarks[0].landmark[334].x * w)
            result_points[4, 1, 1] = int(
                (results.multi_face_landmarks[0].landmark[334].y + delta) * h
            )
            result_points[7, 0, 0] = int(results.multi_face_landmarks[0].landmark[55].x * w)
            result_points[7, 0, 1] = int(
                (results.multi_face_landmarks[0].landmark[55].y - delta) * h
            )
            result_points[8, 0, 0] = int(results.multi_face_landmarks[0].landmark[55].x * w)
            result_points[8, 0, 1] = int(
                (results.multi_face_landmarks[0].landmark[55].y + delta) * h
            )
            result_points[7, 1, 0] = int(results.multi_face_landmarks[0].landmark[285].x * w)
            result_points[7, 1, 1] = int(
                (results.multi_face_landmarks[0].landmark[285].y - delta) * h
            )
            result_points[8, 1, 0] = int(results.multi_face_landmarks[0].landmark[285].x * w)
            result_points[8, 1, 1] = int(
                (results.multi_face_landmarks[0].landmark[285].y + delta) * h
            )

    result_points[27, 0, 0], result_points[27, 0, 1] = get_crosss_point(
        results.multi_face_landmarks[0].landmark[207].x * w,
        results.multi_face_landmarks[0].landmark[207].y * h,
        results.multi_face_landmarks[0].landmark[135].x * w,
        results.multi_face_landmarks[0].landmark[135].y * h,
        results.multi_face_landmarks[0].landmark[152].x * w,
        results.multi_face_landmarks[0].landmark[152].y * h,
        results.multi_face_landmarks[0].landmark[149].x * w,
        results.multi_face_landmarks[0].landmark[149].y * h,
    )
    result_points[27, 1, 0], result_points[27, 1, 1] = get_crosss_point(
        results.multi_face_landmarks[0].landmark[433].x * w,
        results.multi_face_landmarks[0].landmark[433].y * h,
        results.multi_face_landmarks[0].landmark[397].x * w,
        results.multi_face_landmarks[0].landmark[397].y * h,
        results.multi_face_landmarks[0].landmark[152].x * w,
        results.multi_face_landmarks[0].landmark[152].y * h,
        results.multi_face_landmarks[0].landmark[378].x * w,
        results.multi_face_landmarks[0].landmark[378].y * h,
    )

    for i in range(1, len(result_points)):
        cv2.circle(
            image,
            (int(result_points[i, 0, 0]), int(result_points[i, 0, 1])),
            3,
            (255, 0, 0),
            -1,
        )
        cv2.circle(
            image,
            (int(result_points[i, 1, 0]), int(result_points[i, 1, 1])),
            3,
            (255, 0, 0),
            -1,
        )

    return result_points