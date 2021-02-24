import cv2
import numpy as np

frameWidth = 1000
frameHeight = 1000
cap = cv2.VideoCapture(0)
cap.set(3, 1500)
cap.set(4, 2000)
cap.set(10, 150)


my_colors = [
    [5, 107, 0, 19, 255, 255],  #Orange
    [126, 49, 89, 166, 141, 154],  #Purple
    [57, 76, 0, 100, 255, 255]  #Green
]
my_colvals = [
    [51, 153, 255],
    [255, 0, 255],
    [0, 255, 0]
]  # BGR

my_points = []  # [x, y, colID]


def find_color(img_arg, colors, colvals):
    imgHSV = cv2.cvtColor(img_arg, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for col in colors:
        lower = np.array(col[0:3])
        upper = np.array(col[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = get_contours(mask)
        # cv2.circle(img_res, (x, y), 10, colvals[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints


def get_contours(img_arg):
    contours, hierarchy = cv2.findContours(img_arg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(img_res, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y


def draw_on_canvas(pts, colvals):
    for pt in pts:
        cv2.circle(img_res, (pt[0], pt[1]), 15, colvals[pt[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img_res = img.copy()
    newPts = find_color(img, my_colors, my_colvals)

    if len(newPts) != 0:
        for newP in newPts:
            my_points.append(newP)
    if len(my_points) != 0:
        draw_on_canvas(my_points, my_colvals)

    cv2.imshow("Result", img_res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
