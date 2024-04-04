import pickle
import cv2
import numpy as np

# camera settings

cam_id = 2
width, height = 1920, 1080 # change the settings regarding the phone you use

# variables
cap = cv2.VideoCapture(cam_id)
cap.set(3, width)
cap.set(4, height)
points = np.zeros((4,2), int)
counter = 0

def mousePoints(event, x, y, flags, params):
    """
    Callback function for mouse points
    """

    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        points[counter] = x, y # stores the clicked points
        counter += 1 
        print(f"Clicked points: {points}")

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


while True:
    succes, img = cap.read()

    if counter == 4:
    # save selected points to file whan 4 points selected
        file = open("map.p", "wb")
        pickle.dump(points, file)
        file.close()
        print("Points saved to file: map.p")
    
    # warp image
        image_output, matrix = warpImage(img, points)
        cv2.imshow("Output image: ", image_output)
        
    # draw circles at clicked points
    for x in range(0,4):
        cv2.circle(img, (points[x][0], points[x][1]), 3, (0, 255, 0), cv2.FILLED)
    
    cv2.imshow("Original image ", img)
    cv2.setMouseCallback("Original image ", mousePoints)

    key = cv2.waitKey(1)
    if key == ord("q"): #close window with q
        break
    

cap.release()
cv2.destroyAllWindows()
