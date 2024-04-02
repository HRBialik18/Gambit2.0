import cv2
import subprocess

# Global variables for ROI selection
refPt = []
cropping = False

# Initialize the webcam
cap = cv2.VideoCapture(1)

def click_and_crop(event, x, y, flags, param):
    """
    Mouse callback function for ROI selection.
    """
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        # Draw a rectangle around the ROI
        cv2.rectangle(frame, refPt[0], refPt[1], (0, 0, 0), 2)
        cv2.imshow("Webcam", frame)

cv2.namedWindow("Webcam")
cv2.setMouseCallback("Webcam", click_and_crop)

show_grid = True

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    if show_grid:
        # Draw a 12x12 grid overlay on the webcam frame
        grid_size = 12
        frame_height, frame_width, _ = frame.shape
        cell_width = frame_width // grid_size
        cell_height = frame_height // grid_size

        for i in range(0, frame_width, cell_width):
            cv2.line(frame, (i, 0), (i, frame_height), (0, 255, 0), 1)
        for j in range(0, frame_height, cell_height):
            cv2.line(frame, (0, j), (frame_width, j), (0, 255, 0), 1)
    
    cv2.imshow('Webcam', frame)

    # Wait for key events
    key = cv2.waitKey(1) & 0xFF

    if key == ord('1'):
        try:
            # Run the "everything.py" script using subprocess
            subprocess.run(['python', 'everything.py'])
        except FileNotFoundError:
            print("Failed to run 'everything.py'. File not found.")
    elif key == ord('2'):
        try:
            # Run the "reset.py" script using subprocess
            subprocess.run(['python', 'reset.py'])
        except FileNotFoundError:
            print("Failed to run 'reset.py'. File not found.")
    elif key == ord('3'):
         show_grid = not show_grid
    elif key == ord('q'):
        break

    if len(refPt) == 2:
        # Capture and save the ROI as "image.jpg"
        roi = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imwrite('LivePicture\image.jpg', roi)
        print("ROI captured and saved as 'image.jpg'.")
        refPt = []

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

print("Exiting...")
