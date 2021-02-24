import cv2
import numpy as np

width_img = 480
height_img = 640

# ===========================
# FOR WEBCAM

# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
# cap.set(10, 150)
# ===========================


def pre_processing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)

    return imgThres


def get_contours(img_arg):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img_arg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest


def reorder(my_pts):
    print(my_pts.shape)
    my_pts = my_pts.reshape((4, 2))
    my_newpts = np.zeros((4, 1, 2), np.int32)
    add = my_pts.sum(1)
    # print("Add", add)

    my_newpts[0] = my_pts[np.argmin(add)]
    my_newpts[3] = my_pts[np.argmax(add)]
    diff = np.diff(my_pts, axis=1)
    my_newpts[1] = my_pts[np.argmin(diff)]
    my_newpts[2] = my_pts[np.argmax(diff)]
    # print("New Points", my_newpts)
    return my_newpts


def get_warp(img_arg, con_arg):
    con_arg = reorder(con_arg)
    pts1 = np.float32(con_arg)
    pts2 = np.float32([
        [0, 0],
        [width_img, 0],
        [0, height_img],
        [width_img, height_img]
    ])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img_arg, matrix, (width_img, height_img))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (width_img, height_img))

    return imgCropped


def stack_images(scale, img_array):
    rows = len(img_array)
    cols = len(img_array[0])
    rowsAvailable = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape [:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = cv2.resize(
                        img_array[x][y],
                        (img_array[0][0].shape[1], img_array[0][0].shape[0]),
                        None, scale, scale
                    )
                if len(img_array[x][y].shape) == 2: img_array[x][y]= cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = cv2.resize(
                    img_array[x],
                    (img_array[0].shape[1], img_array[0].shape[0]),
                    None, scale, scale
                )
            if len(img_array[x].shape) == 2: img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(img_array)
        ver = hor
    return ver

# ====================================================
# FOR WEBCAM

# while True:
#     success, img = cap.read()
#     img = cv2.resize(img, (width_img, height_img))
#     imgContour = img.copy()
#
#     imgThres = pre_processing(img)
#     biggest = get_contours(imgThres)
#     if biggest.size != 0:
#         imgWarped = get_warp(img, biggest)
#         imageArray = (
#             [img, imgThres],
#             [imgContour, imgWarped]
#         )
#     else:
#         imageArray = (
#             [img, imgThres]
#         )
#
#     stackedImages = stack_images(0.3, imageArray)
#
#     cv2.imshow("Workflow",  stackedImages)
#     # cv2.imshow("ImageWarped", imgWarped)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# =====================================================


# ================
# FOR SINGLE IMAGE
# ================

img = cv2.imread("Resources/paper.jpg")
imgContour = img.copy()

imgThres = pre_processing(img)
biggest = get_contours(imgThres)
imgWarped = get_warp(img, biggest)

imageArray = (
    [img, imgThres],
    [imgContour, imgWarped]
)
stackedImages = stack_images(0.3, imageArray)

cv2.imshow("Workflow",  stackedImages)
cv2.waitKey(0)
