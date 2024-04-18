import imp

# Load the module from the file path
imageCapture = imp.load_source('imageCapture', 'SnapAndCrop/imageCapture.py')
imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py')
imageProcessing = imp.load_source('imageProcessing', 'ImageProcessing.py')

def test(inputImPath, outputImPath):
    imageCapture.takeImage(inputImPath)
    imageFixing.imageCropAndWarp(inputImPath, outputImPath)
    [oldBoard, diff] = imageProcessing.im2boardstate(outputImPath)
    print('old board:', oldBoard)
#test('Images/raw_image.jpg','Images/transformed_image.jpg')