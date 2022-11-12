import cv2
from matplotlib import pyplot as plt

img_gray = cv2.imread('c:/01.jpg',0) #cv2.IMREAD_GRAYSCALE
img_color = cv2.imread('c:/01.jpg',1) #cv2.IMREAD_COLOR
cv2.imshow('gray', img_gray)
cv2.imshow('color', img_color)
cv2.waitKey(0) 

# plt.imshow(img_color),plt.show()