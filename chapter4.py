import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)
# print(img.shape)
# img[:] = 255,0,0

# =================
# SHAPES ON IMAGES
# =================

# The 1st arg is the image, 2nd is the Starting Point, 3rd is the Ending Point, 4th is the Color, & 5th is the
# Thickness
cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)
cv2.rectangle(img, (0,0), (250, 350), (0, 0, 255), 2)
cv2.circle(img, (400, 50), 30, (255, 255, 0), 5)

# ==============
# TEXT ON SHAPES
# ==============

# The 1st arg is the image, 2nd is the text, 3rd is the Starting Point, 4th is the Font Style, 5th is the Scale,
# 6th is the Color, 7th is the Thickness
cv2.putText(img, " OPENCV ", (300, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 3)

cv2.imshow("Image", img)
cv2.waitKey(0)