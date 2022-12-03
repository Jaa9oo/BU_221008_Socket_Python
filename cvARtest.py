import math
import cv2
from matplotlib import pyplot as plt
import numpy as np

# img = cv2.imread('D:\\test01.jpg', 0)

# orb = cv2.ORB_create()

# kp = orb.detect(img, None)

# kp, des = orb.compute(img, kp)

# img2 = cv2.drawKeypoints(img, kp, img, color = (0,255,0), flags = 0)
# cv2.imshow('keypoints', img2)
# cv2.waitKey(0)


MIN_MATCHES = 15

test = 'D:\\test03.jpg'

cap = cv2.imread(test, 0)
model = cv2.imread('D:\\maker2.png', 0)
img_rgb = cv2.imread(test, 0)

orb = cv2.ORB_create()

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

kp_model, des_model = orb.detectAndCompute(model, None)

kp_frame, des_frame = orb.detectAndCompute(cap, None)

matches = bf.match(des_model, des_frame)

matches = sorted(matches, key=lambda x: x.distance)

src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

h, w = model.shape
pts = np.float32([[0,0], [0,h-1], [w-1, h-1], [w-1, 0]]).reshape(-1,1,2)

dst = cv2.perspectiveTransform(pts, M)

img2 = cv2.polylines(img_rgb, [np.int32(dst)], True, 0, 3, cv2.LINE_AA)
cv2.imshow('frame', img_rgb)
cv2.waitKey(0)

if len(matches) > MIN_MATCHES:
    cap = cv2.drawMatches(model, kp_model, cap, kp_frame, matches[:MIN_MATCHES], 0, flags=2)

    cv2.imshow('frame', cap)
    cv2.waitKey(0)
else:
    print("Not Enough Match")


def projection_matrix(_camera, homography):
    homography = homography * (-1)
    rot_and_transl = np.dot(np.linalg.inv(_camera), homography)
    col_1 = rot_and_transl[:0]
    col_2 = rot_and_transl[:1]
    col_3 = rot_and_transl[:2]

    I = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
    rot_1 = col_1/I
    rot_2 = col_2/I
    translation = col_3/I
    
    c = rot_1 + rot_2
    p = np.cross(rot_1, rot_2)
    d = np.cross(c, p)
    rot_1 = np.dot(c/np.linalg.norm(c,2) + d / np.linalg.norm(d,2), 1/math.sqrt(2))
    rot_2 = np.dot(c/np.linalg.norm(c,2) + d / np.linalg.norm(d,2), 1/math.sqrt(2))
    rot_3 = np.cross(rot_1, rot_2)

    projection = np.stack((rot_1, rot_2, rot_3, translation)).T

    return np.dot(_camera, projection)


# plt.imshow(img_color),plt.show()