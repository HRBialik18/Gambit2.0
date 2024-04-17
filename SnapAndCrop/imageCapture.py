# importing the python open cv library
import cv2
import numpy as np

# intialize the webcam and pass a constant which is 0

def takeImage(impath):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()

    b, g, r = cv2.split(frame)

    # Reduce the intensity of the blue channel to reduce the yellow tint
    # You can adjust the scaling factor to fine-tune the effect
    adjusted_b = np.clip(b * 0.9, 0, 255).astype(np.uint8)

    # Merge the adjusted channels back together
    adjusted_image = cv2.merge((adjusted_b, g, r))

    cv2.imwrite(impath, adjusted_image)
    cam.release()
#takeImage('Images/raw_image.jpg')





def testingCropping():
    import imp
    imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py') 
    takeImage('Images/raw_image.jpg')
    imageFixing.imageCropAndWarp('Images/raw_image.jpg','Images/transformed_image.jpg')
