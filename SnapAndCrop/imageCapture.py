# importing the python open cv library
import cv2

# intialize the webcam and pass a constant which is 0

def takeImage(impath):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cv2.imwrite(impath, frame)
    cam.release()
#takeImage('Images/raw_image.jpg')





def testingCropping():
    import imp
    imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py') 
    takeImage('Images/raw_image.jpg')
    imageFixing.imageCropAndWarp('Images/raw_image.jpg','Images/transformed_image.jpg')
#testingCropping()