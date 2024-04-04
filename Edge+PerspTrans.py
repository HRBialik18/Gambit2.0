from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
import matplotlib.pyplot as plt

def imageCropAndWarp():

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
        #plt.imshow(image)

        # Extract x and y coordinates
        x_coords = [coord[0] for coord in coordinates]
        y_coords = [coord[1] for coord in coordinates]

        # Plot the coordinates
        plt.scatter(x_coords, y_coords, color='red', marker='o')

        # Show plot
        #plt.show()

    # Example usage:
    image_path = 'example.jpg'  # Path to your image
    #plot_coordinates(image_path, coordinates)
    corners = find_corners(coordinates)
    plot_coordinates(image_path, corners)
    print(corners)

    def perspective_transform_to_square(image, corners):
        # Define the square shape (destination)
        square_size = 900  # Adjust as needed
        dst_corners = np.array([[0, 0], [square_size, 0], [square_size, square_size], [0, square_size]], dtype=np.float32)
        
        # Convert corners to float32 if they're not already
        corners = np.float32(corners)

        # Compute the perspective transform matrix
        transform_matrix = cv2.getPerspectiveTransform(corners, dst_corners)
        
        # Apply the perspective transform
        square_image = cv2.warpPerspective(image, transform_matrix, (square_size, square_size))
        
        return square_image

    transformed_image = perspective_transform_to_square (original_img, corners)
    #cv2.imshow('Transformed Image', transformed_image)
    cv2.imwrite('trasformed_image.jpg', transformed_image)
    cv2.destroyAllWindows()

imageCropAndWarp()

