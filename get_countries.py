import cv2
import numpy as np
import pickle



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

current_polygon = []

file_obj = open(map_file, "rb")
map_points = pickle.load(file_obj)
file_obj.close()
print(f"Loaded map coordinates: ", map_points)
# variables --> end



def mousePoints(event, x, y, flags, params,):

    global counter, current_polygon

    if event == cv2.EVENT_LBUTTONDOWN:

        current_polygon.append((x, y))

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
    imageWarped, _ =warpImage(img, map_points)

    key = cv2.waitKey(1)

    #save key when we select points
    if key == ord("s") and len(current_polygon) > 2: 
        country_name = input("Enter country name: ")
        polygons.append([current_polygon, country_name])
        current_polygon = []
        counter += 1
        print("Number of countries saved: ",len(polygons))

    if key == ord("d"):
        polygons.pop()

    if key == ord("q"):
        fileObject = open(countries_file, "wb")
        pickle.dump(polygons, fileObject)
        fileObject.close()
        print(f"Saved {len(polygons)} countries")
        break

    if current_polygon:
        cv2.polylines(imageWarped, [np.array(current_polygon)], isClosed=True, color=(0, 0, 255), thickness=2)
    
    overlay = imageWarped.copy()

    for polygon, name in polygons:
        cv2.polylines(imageWarped, [np.array(polygon)], isClosed=True, color= (0, 255, 0), thickness=2)
        cv2.fillPoly(overlay, [np.array(polygon)], (0, 255, 0))
        
    cv2.addWeighted(overlay, 0.35, imageWarped, 0.65, 0, imageWarped)
    
    cv2.imshow("Warped Image", imageWarped)

    cv2.setMouseCallback("Warped Image", mousePoints)

    