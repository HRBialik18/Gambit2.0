import numpy as np
import cv2

def chop_image_into_squares(image, corners):
    # Convert corners to NumPy array if not already
    corners = np.array(corners, dtype=np.float32)

    # Define the number of rows and columns of squares
    rows = 8
    cols = 8

    # Calculate the step size for each row and column
    horizontal_step = (corners[1][0] - corners[0][0]) / cols
    vertical_step = (corners[2][1] - corners[0][1]) / rows

    # Draw red lines for the vertical grid lines
    for i in range(cols + 1):
        start_point = (int(corners[0][0] + i * horizontal_step), int(corners[0][1]))
        end_point = (int(corners[0][0] + i * horizontal_step), int(corners[0][1] + vertical_step * rows))
        cv2.line(image, start_point, end_point, (0, 0, 255), 2)

    # Draw red lines for the horizontal grid lines
    for i in range(rows + 1):
        start_point = (int(corners[0][0]), int(corners[0][1] + i * vertical_step))
        end_point = (int(corners[0][0] + horizontal_step * cols), int(corners[0][1] + i * vertical_step))
        cv2.line(image, start_point, end_point, (0, 0, 255), 2)

    # Return the image with grid lines
    return image

# Load the transformed image
transformed_image = cv2.imread("trasformed_image.jpg")

# Define the corner coordinates of the quadrilateral
# You can use the returned corner coordinates from your existing function
corners = [[0., 0.], [900., 0.], [900., 900.], [0., 900.]]

# Draw grid lines directly on the transformed image
image_with_grid = chop_image_into_squares(transformed_image, corners)

# Display the image with grid lines
cv2.imshow("Image with Grid", image_with_grid)
cv2.waitKey(0)
cv2.destroyAllWindows()
