import cv2
print("Package Imported")

# ==================
# Importing an Image
# ==================

# imshow takes 2 arguments, the first is the name of the window, and the second is the name of the img
# img = cv2.imread("Resources/lena.png")
# cv2.imshow("Output",  img)
# cv2.waitKey(0)

# ==================
# Importing a Video
# ==================

# cap = cv2.VideoCapture("Resources/test_video.mp4")

# Since a video is a sequence of Images, hence we need a while loop to iterate over all the frames of the video
# while True:
#     success, img = cap.read()
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# ======================
# Importing from webcam
# ======================

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
