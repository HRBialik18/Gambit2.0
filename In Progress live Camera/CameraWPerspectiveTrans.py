import cv2
import numpy as np

# Initialize variables
capturing = False
frame = None
selected_points = []

# Define mouse callback function to capture mouse events
def mouse_callback(event, x, y, flags, param):
    global frame, selected_points
    if capturing and event == cv2.EVENT_LBUTTONDOWN:
        selected_points.append((x, y))
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Capture Image', frame)

# Set up the mouse callback
cv2.namedWindow('Capture Image')
cv2.setMouseCallback('Capture Image', mouse_callback)

# Capture live feed from webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Display live feed from webcam
    cv2.imshow('Capture Image', frame)

    # Check for spacebar press to capture image
    key = cv2.waitKey(1)
    if key == ord(' '):
        capturing = True
        selected_points = []
        while capturing:
            key = cv2.waitKey(1)
            if key == ord(' '):
                capturing = False

        # Perform perspective transform
        if len(selected_points) == 4:
            src_points = np.float32([selected_points[0], selected_points[1], selected_points[2], selected_points[3]])
            dst_points = np.float32([[0, 0], [frame.shape[1], 0], [frame.shape[1], frame.shape[0]], [0, frame.shape[0]]])
            M = cv2.getPerspectiveTransform(src_points, dst_points)
            warped = cv2.warpPerspective(frame, M, (frame.shape[1], frame.shape[0]))
            cv2.imshow('Original Image', frame)
            cv2.imshow('Warped Image', warped)
            cv2.waitKey(0)

    # Check for escape key press to exit
    if key == 27:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
