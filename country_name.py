import cv2
import numpy as np
import cv2
import cvzone
import pickle
from cvzone.HandTrackingModule import HandDetector


# variabels --> start
map_file = "map.p"
countries_file = "countries.p"

if countries_file:
    file_obj = open(countries_file, "rb")
    polygons = pickle.load(file_obj)
    file_obj.close()
    print(f"Loaded {len(polygons)} countries")
else:
    polygons = []

cam_id = 2
width, height = 1920, 1080

cap = cv2.VideoCapture(cam_id)
cap.set(3, width)
cap.set(4, height)

counter = 0

detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5 )

file_obj = open(map_file, "rb")
map_points = pickle.load(file_obj)
file_obj.close()
print(f"Loaded map coordinates: ", map_points)
# variables --> end



def warpImage(img, points, size=[1920, 1080]):
    """
    warps image based on selected points
    img: image to be warped
    points: array of clicked points
    size: size of warped image
    """
    points1 = np.float32(points)
    points2 = np.float32([[0,0], [size[0], 0], [0, size[1]], [size[0], size[1]]])
    matrix = cv2.getPerspectiveTransform(points1, points2)
    image_output = cv2.warpPerspective(img, matrix, (size[0], size[1]))
    return image_output, matrix

def warpSingelPoint(point, matrix):

    pointHomogeneous = np.array([[point[0], point[1], 1]], dtype=np.float32)
    pointHomogeneousTransformed = np.dot(matrix, pointHomogeneous.T).T
    pointWarped = pointHomogeneousTransformed[0, :2] / pointHomogeneousTransformed[0, 2]

    return pointWarped

def getFingerLocation(img, imageWarped):

    hands, img = detector.findHands(img, draw = False, flipType = True)

    if hands:
        hand1 = hands[0]
        indexFinger = hand1["lmlist"][8][0:2]
        cv2.circle(img, indexFinger, 5, (255, 0, 255), cv2.FILLED)
        warpedPoint = warpSingelPoint(indexFinger, matrix)
        warpedPoint = int(warpedPoint[0]), int(warpedPoint[1])
        cv2.circle(imageWarped, warpedPoint, 5, (255, 0, 0), cv2.FILLED)
    else:
        warped_point = None

    return warped_point

while True:
    succes, img = cap.read()
    imageWarped, matrix = warpImage(img, map_points)

    imageStacked = cvzone.stackImages([img, imageWarped], 2, 0.3)

    warpedPoints = getFingerLocation(img, imageWarped)

    cv2.imshow("Stacked Image", imageStacked)
    
    key = cv2.waitKey(1)