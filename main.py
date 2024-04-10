import imp
import cv2

# Load the module from the file path
imageCapture = imp.load_source('imageCapture', 'imageCapture.py')
imageFixing = imp.load_source('imageFixing', 'Edge+PerspTrans.py')
imageChopping = imp.load_source('chop_image_into_8x8', 'ChopAndIdentify.py.py')
def main():
    #imageCapture.takeImage()
    corners = imageFixing.imageCropAndWarp()
    image_with_grid = imageChopping.chop_image_into_8x8(corners)
    cv2.imshow("Image with Grid", image_with_grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
main()