#!/usr/bin/env python
import argparse
import numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
from skimage import draw
import matplotlib.pyplot as plt
from PIL import Image
import requests
import cv2

from face_alignment.api import FaceAlignment, LandmarksType, NetworkSize
from util import read_list, show_result, CRF, open_image

def main(path):
        im = open_image(path)
        # resize for memory
        width, height = im.size
        if height > 800:
            im = im.resize((int(800*width/height), 800))
            width, height = im.size

        # use 2D-FAN detect landmarks
        fa = FaceAlignment(LandmarksType._2D, enable_cuda=True,
                           flip_input=False, use_cnn_face_detector=True)
        try:
            landmarks = fa.get_landmarks(np.array(im))[-1]
            landmarks[:,1] = height - landmarks[:,1]
        except:
            pass

        lm = np.array(im)
        for i in range(landmarks.shape[0]):
            rr, cc = draw.circle_perimeter(height-landmarks[i,1].astype('int32'), landmarks[i,0].astype('int32'), 2)
            lm[rr, cc, :] = np.array((255, 0, 0))
        print(lm.shape)
        img = Image.fromarray(lm, "RGB")
        img.save("result.jpg")
        
        return landmarks, width, height

def mapping_func(path):
    side_lib, width, height = main(path)
    result_marks = [[0.0,0.0]] * 30
    lib_index = [0,1,4,5,7,8,12,15,20,28,29,30,33,36,44,50,54,57]
    result_index = [57, 42, 48, 50, 51, 52, 49, 38, 32, 36, 39, 41, 43, 57, 33, 45, 46, 58]
    for i in range(len(lib_index)):
      result_marks[result_index[i]-30] = [side_lib[lib_index[i]][0], height-side_lib[lib_index[i]][1]]
    print(result_marks)
    return result_marks, width, height

def main_process(path):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': '7Rpyut6AoqWqTFEMB7zjEita'},
    )
    if response.status_code == requests.codes.ok:
        with open('nobackground.jpg', 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

    reference_points, width, height = mapping_func(path)

    im = cv2.imread("nobackground.jpg", 0)    
    im = cv2.resize(im, (width, height))

    neck_position = [0, 0]
    nose_position = [801, 801]

    for i in range(height-1, height//4, -1):
        for j in range(width):
            flag = False
            if im[i][j]!=0:
                        if neck_position[0] < j:
                            neck_position[0]=j
                            neck_position[1]=i
                        if nose_position[0]>j and i < height//4*3:
                          nose_position[0]=j
                          nose_position[1]=i
                        flag = True
                        break
            if flag:
                break
    print("NECK", neck_position)
    
    reference_points[25] = neck_position
    reference_points[10] = nose_position

    source_points_path = "./f15.pts"
    return_points = [[0,0]] * 30
    try:
      with open(source_points_path, 'r') as file:
        file_content = file.read()
    except FileNotFoundError:
      print("Source Points File Not Found.")
    
    points = []
    start_index = file_content.index('{') + 1
    end_index = file_content.index('}')
    points_data = file_content[start_index:end_index].split('\n')

    index = 0
    for i, point_data in enumerate(points_data):
        if point_data.strip() != '':
            x, y = map(float, point_data.strip().split())
            points.append([x, y, index])
            index+=1
    
    sample_ratio = (points[25][1]-points[0][1])/(points[25][1]-points[2][1])
    reference_points[0]= [0, reference_points[25][1] - (reference_points[25][1]-reference_points[2][1]) * sample_ratio]

    sorted_points = sorted(points, key=lambda p: p[1])

    ref_step_index = []
    ref_empty_step_index=[]
    for i, point in enumerate(sorted_points):
      if np.array_equal(reference_points[point[2]], [0.0, 0.0]):
        ref_empty_step_index[len(ref_empty_step_index)-1].append(point[2])
      else:
        ref_step_index.append(point[2])
        ref_empty_step_index.append([])
    
    for i in range(len(ref_step_index)-1):
      start = ref_step_index[i]
      end = ref_step_index[i+1]
      main_height = points[end][1]-points[start][1]
      new_height = reference_points[end][1]-reference_points[start][1]
      step_ratio = main_height / new_height
      print(start, end, main_height, new_height, step_ratio, ref_empty_step_index[i])
      for j in ref_empty_step_index[i]:
        temp_height = (points[j][1]-points[start][1])/step_ratio
        reference_points[j]=[0, reference_points[start][1]+temp_height]

    sorted_points = sorted(points, key=lambda p: p[0])
    # print(sorted_points)
    ref_step_index = []
    ref_empty_step_index=[]
    for i, point in enumerate(sorted_points):
      print(i, ref_step_index, point)
      if reference_points[point[2]][0]==0:
        ref_empty_step_index[len(ref_empty_step_index)-1].append(point[2])
      else:
        ref_step_index.append(point[2])
        ref_empty_step_index.append([])
    
    for i in range(len(ref_step_index)-1):
      start = ref_step_index[i]
      end = ref_step_index[i+1]
      main_width = points[end][0]-points[start][0]
      new_width = reference_points[end][0]-reference_points[start][0]
      step_ratio = main_width / new_width
      for j in ref_empty_step_index[i]:
        temp_width= (points[j][0]-points[start][0])/step_ratio
        reference_points[j]=[reference_points[start][0]+temp_width, reference_points[j][1]]

    # for i in range(30):
    #   cv2.circle(im, (int(reference_points[i][0]), int(reference_points[i][1])), 2, (255, 0, 0), 1)
    #   cv2.putText(im, str(i), (int(reference_points[i][0]), int(reference_points[i][1])), 1, 1, (255,0,0), 1)

    # cv2.imwrite("ttt.jpg", im)
    # print(reference_points)
    return reference_points

main_process("f15.jpg")