import numpy as np
import cv2
import requests
import skin_detector
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import cdist

def make_no_background_image(image_path):
    image = cv2.imread(image_path)
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(image_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'k2XDaxdXet3NUy7WX34njqSJ'},
    )
    if response.status_code == requests.codes.ok:
        with open('nobackground.png', 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

def process_image(image_path):
    

    ####################   PRE PROCESSING   ######################

    #Make No Background Image
    make_no_background_image(image_path)

    #Detect Only Skin
    img=cv2.imread("nobackground.png")
    mask = skin_detector.process(img)    

    #Detect Only Face
    inter = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)))
    cv2.imwrite("sample_face.jpg", inter)

    
    ####################   MAIN PROCESSING   ######################

    #START PROCESSING
    image = cv2.imread("sample_face.jpg", 0)
    height, width = image.shape
    print(height, width)
    contour_mat = np.zeros((height, width, 1), dtype=np.uint8)

    basic_temp = []
    head_back = []
    gray_image = cv2.imread("nobackground.png", cv2.IMREAD_GRAYSCALE)
    # back_gray_image = cv2.imread("sample_face.jpg", cv2.IMREAD_GRAYSCALE)

    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    nose_position = [1000, 1000]
    neck_position = [0, 0]

    for i in range(height):
        for j in range(width):
            flag = False
            if image[i][j]==255:
                for k in range(width):
                    if gray_image[i][k]!=0:
                        contour_mat[i][k][0] = 255
                        basic_temp.append([i, k])
                        if nose_position[0] > k:
                            nose_position[0]=k
                            nose_position[1]=i
                        if neck_position[0] < k:
                            neck_position[0]=k
                            neck_position[1]=i
                        flag = True
                        break
                for k in range(width-1, -1, -1):
                    if image[i][k]!=255:
                        contour_mat[i][k][0]=255
                        head_back.append([i, k])
                        break
            if flag:
                break

    cropped_image = gray_image[basic_temp[0][0]:neck_position[1], nose_position[0]:]

    features = []

    slash = 2

    head_front = []
    head_back = []

    height, width = cropped_image.shape
    for i in range(height):
        for j in range(width):
            if cropped_image[i][j]!=0:
                head_front.append([i, j])
                break
        for j in range(width-1, 0, -1):
            if cropped_image[i][j]!=0:
                head_back.append([i, j])
                break
                

    contour_image = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(slash, len(head_front)-slash):
        contour_image[head_front[i][0]][head_front[i][1]] = [255, 0, 0]
        contour_image[head_back[i][0]][head_back[i][1]] = [255, 0, 0]

        if(head_front[i][1]-head_front[i-slash][1])*(head_front[i+slash][1]-head_front[i][1])<=0:
            contour_image[head_front[i][0]][head_front[i][1]] = 0
            # cv2.circle(contour_image, (temp[i][1],temp[i][0]), 2, (0, 0, 255), 1)
            # i+=slash
            features.append([head_front[i][1], head_front[i][0]])


    X = np.array(features)
    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=10, min_samples=1).fit(X)

    # Get the cluster labels
    labels = dbscan.labels_

    # Create sets of points based on the cluster labels
    point_sets = {}
    for i, label in enumerate(labels):
        if label not in point_sets:
            point_sets[label] = []
        point_sets[label].append(features[i])

    keys = point_sets.keys()

    noised_removed_features = []
    for key in point_sets.keys():
        x = 0
        y = 0
        for temp in point_sets[key]:
            x = x + temp[0]
            y = y + temp[1]
        
        x = x // len(point_sets[key])
        y = y // len(point_sets[key])
        noised_removed_features.append([x, y])


    noised_removed_features[0]=[head_front[0][1], head_front[0][0]]
    noised_removed_features[len(noised_removed_features)-1]=[head_front[len(head_front)-1][1], head_front[len(head_front)-1][0]]

    for i in range(len(noised_removed_features)):
        cv2.circle(contour_image, (noised_removed_features[i][0], noised_removed_features[i][1]), 2, (255,255,0), 2)
        # cv2.putText(contour_image, str(i), (noised_removed_features[i][0], noised_removed_features[i][1]), 2, 2,(255,255,0), 2 )


    ########################   MATCHING STEP     ###################################

    file_name = "./Match/f20.pts"  # Replace with your file name
    matching_image_url = "./Source/f20.jpg"

    matching_image = cv2.imread(matching_image_url)
    matching_height, matching_width, _ = matching_image.shape

    try:
        with open(file_name, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

    points = []
    start_index = file_content.index('{') + 1
    end_index = file_content.index('}')
    points_data = file_content[start_index:end_index].split('\n')


    for i, point_data in enumerate(points_data):
        if point_data.strip() != '':
            x, y = map(float, point_data.strip().split())
            points.append([x, y, i])

    matching_nose = points[10]

    h_ratio = height / (points[25][1]-points[0][1])
    w_ratio = (neck_position[0]-nose_position[0]) / (points[25][0]-points[10][0])

    # points = sorted(points, key=lambda p: p[1])

    new_pose_1 = []
    for i in range(len(points)):
        new_x = (points[i][0] - points[0][0]) * w_ratio + noised_removed_features[0][0]
        new_y = (points[i][1] - points[0][1]) * h_ratio + noised_removed_features[0][1]
        # cv2.circle(contour_image, (int(new_x), int(new_y)), 2, (255,255,255), 2)
        new_pose_1.append([new_x, new_y])

    matching_nose[0] = (matching_nose[0] - points[0][0]) * w_ratio + noised_removed_features[0][0]
    matching_nose[1] = (matching_nose[1] - points[0][1]) * h_ratio + noised_removed_features[0][1]


    print(matching_nose)

    w_ratio = abs((nose_position[0]-new_pose_1[0][0]) / (matching_nose[0]-new_pose_1[0][0]))
    h_ratio = abs((nose_position[1]-new_pose_1[0][1]) / (matching_nose[1]-new_pose_1[0][1]))


    under_area_line = []
    for i in range(noised_removed_features[-1][0]):
        for j in range(height-1,0, -1):
            if cropped_image[j][i]!=0:
                under_area_line.append([i, j])
                contour_image[j][i]=[255,255,0]
                for k in range(21, 24):
                    if i == int(new_pose_1[k][0]):
                        new_pose_1[k][1]=j
                        break
                break

    edge_points =[30, 31, 32, 35, 36, 39, 40, 41, 43, 44, 45, 47, 48, 50, 58, 59]

    for i in range(len(head_front)):
        for j in edge_points:
            index = j - 30
            if int(new_pose_1[index][1]) == int(head_front[i][0]):
                new_pose_1[index][0] = head_front[i][1]

    new_pose_1[46-30][1] = (new_pose_1[45-30][1]+new_pose_1[58-30][1])/2

    print(eyes, "*************")

    if len(eyes):
        new_pose_1[33-30] = [eyes[0][0]+eyes[0][2]/2 - nose_position[0], eyes[0][1]+eyes[0][3]/2 - basic_temp[0][0]]
    new_pose_1[56-30] = [new_pose_1[40-30][0], new_pose_1[33-30][1]]
    # for i in range(len(under_area_line)-3, 1, -1):
    #     if (under_area_line[i+2][1]-under_area_line[i][1])*(under_area_line[i][1]-under_area_line[i-2][1])<=0:
    #         print("----------------------")
    #         cv2.circle(contour_image, (int(under_area_line[i][0]), int(under_area_line[i][1])), 2, (255,255,255), 2)


    for i in range(len(points)):
        new_x = new_pose_1[i][0]
        new_y = new_pose_1[i][1]
        cv2.circle(cropped_image, (int(new_x), int(new_y)), 1, (255,0,255), 2)
    cv2.imshow("crop", cropped_image)

    result = [[coord[0] + nose_position[0], coord[1] + basic_temp[0][0]] for coord in new_pose_1]

    for i in range(len(points)):
        new_x = result[i][0]
        new_y = result[i][1]
        cv2.circle(img, (int(new_x), int(new_y)), 1, (255,0,255), 2)
    cv2.imshow("origin", img)
    cv2.waitKey(0)

    return result


print(process_image("./images/temp.jpg"))