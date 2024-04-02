from inference_sdk import InferenceHTTPClient
import cv2


CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="ulxWhbY1nxtlA240URf6"
)

result = CLIENT.infer("images.jpeg", model_id="chessboard-1hk4y/3")

# Load the image
image = cv2.imread('output_image.jpg')

# Convert coordinates to tuples of integers
coordinates = [(int(coord['x']), int(coord['y'])) for coord in result.get("predictions")[0].get("points")]

# Sort coordinates by x and y values
coordinates.sort(key=lambda x: (x[1], x[0]))

# Extract the minimum and maximum x and y values
x_min = min(coord[0] for coord in coordinates)
x_max = max(coord[0] for coord in coordinates)
y_min = min(coord[1] for coord in coordinates)
y_max = max(coord[1] for coord in coordinates)

# Crop the image
cropped_image = image[y_min:y_max, x_min:x_max]

# Save the cropped image
cv2.imwrite('cropped_image.jpg', cropped_image)

