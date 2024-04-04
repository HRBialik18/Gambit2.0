import matplotlib.pyplot as plt

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
coordinates = [(100, 100), (200, 200), (300, 300)]  # Example coordinates
plot_coordinates(image_path, coordinates)