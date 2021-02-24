import cv2
import numpy as np

# (462, 623, 3), where 462 is the Height, 623 is the Weight, and 3 is the no. of channels, i.e. BGR
img = cv2.imread("Resources/lambo.png")
print(img.shape)

# The width comes first & then the height, in the OpenCV function
imgResize = cv2.resize(img, (1000, 500))
print(imgResize.shape)

# To Crop an image, we don't need any openCV function, we can just use Matrix Functionality
# In Matrix functionality, height comes before than the width
imgCropped = img[0:200, 200:500]

cv2.imshow("Image", img)
cv2.imshow("Image Resize", imgResize)
cv2.imshow("Image Cropped", imgCropped)

cv2.waitKey(0)