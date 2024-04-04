from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
import matplotlib.pyplot as plt


def find_corners(coordinates):
    # Convert coordinates to numpy array
    pts = np.array(coordinates, dtype=np.int32)

    # Compute convex hull
    hull = cv2.convexHull(pts)

    # Approximate the convex hull to get the corners
    epsilon = 0.1 * cv2.arcLength(hull, True)
    approx = cv2.approxPolyDP(hull, epsilon, True)

    # Return the approximated corners
    return approx.reshape(-1, 2)


CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="ulxWhbY1nxtlA240URf6"
)


result = CLIENT.infer("output_image.jpg", model_id="chessboard-1hk4y/3")

# Load the image
original_img = cv2.imread('output_image.jpg')

standard_width = 800
standard_height = 600

coordinates = [(int(coord['x']), int(coord['y'])) for coord in result.get("predictions")[0].get("points")]


def plot_coordinates(image_path, coordinates):
    # Load the image
    image = plt.imread('output_image.jpg')

    # Plot the image
    plt.imshow(image)

    # Extract x and y coordinates
    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]

    # Plot the coordinates
    plt.scatter(x_coords, y_coords, color='red', marker='o')

    # Show plot
    plt.show()

# Example usage:
image_path = 'example.jpg'  # Path to your image
plot_coordinates(image_path, coordinates)
corners = find_corners(coordinates)
print(corners)






# # Extract the minimum and maximum x and y values
# x_min = min(coord[0] for coord in coordinates)
# x_max = max(coord[0] for coord in coordinates)
# y_min = min(coord[1] for coord in coordinates)
# y_max = max(coord[1] for coord in coordinates)

# cropped_image = original_img[y_min:y_max, x_min:x_max]

src_corners = np.float32(corners)
dst_corners = np.float32([[0, 0], [standard_width, 0], [0, standard_height], [standard_width, standard_height]])
perspective_matrix = cv2.getPerspectiveTransform(src_corners, dst_corners)

# # # Apply the perspective transform
# result = cv2.warpPerspective(original_img, perspective_matrix,  (standard_width, standard_height))

# # # Save the result
# cv2.imwrite('perspective_shifted_image.jpg', result)
# cv2.imwrite('cropped_image.jpg', cropped_image)




# corner_coordinates = np.float32([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]])

# # Define the new corner coordinates for the perspective shift
# new_corner_coordinates = np.float32([[0, 0], [cropped_image.shape[1], 0], [0, cropped_image.shape[0]], [cropped_image.shape[1], cropped_image.shape[0]]])

# # Compute the perspective transform matrix
# perspective_matrix = cv2.getPerspectiveTransform(corner_coordinates, new_corner_coordinates)

# # Apply the perspective transform
# perspective_shifted_image = cv2.warpPerspective(cropped_image, perspective_matrix, (cropped_image.shape[1], cropped_image.shape[0]))

# # Display the perspective-shifted image
# cv2.imshow("Perspective Shifted Image", perspective_shifted_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# # Save the cropped image
# cv2.imwrite('cropped_image.jpg', perspective_shifted_image)
