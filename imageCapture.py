# importing the python open cv library
import cv2

# intialize the webcam and pass a constant which is 0

def takeImage():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cv2.imwrite('output_image.jpg', frame)
    cam.release()
