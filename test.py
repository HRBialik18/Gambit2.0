import imp
import numpy as np
import cv2
import serial

# Load the module from the file path
imageCapture = imp.load_source('imageCapture', 'SnapAndCrop/imageCapture.py')
imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py')
imageProcessing = imp.load_source('imageProcessing', 'ImageProcessing.py')
resetGame = imp.load_source('resetGame', 'Reset.py')

inputImPath = 'Images/raw_image.jpg'
outputImPath = 'Images/transformed_image.jpg'

print("finding robot move")  
cam = cv2.VideoCapture(1)
# image capture    
imageCapture.takeImage(inputImPath, cam)
print('picture taken')
imageFixing.imageCropAndWarp(inputImPath, outputImPath)
print ('picture cropped')

# image processing and stockfish
errCount = 0
[oldBoard, diff, mof, arr_str] = imageProcessing.iserror(outputImPath)
if isinstance(diff, np.ndarray):
    errCount = 5

if errCount == 5:
    halfFEN = imageProcessing.FENupdate (arr_str)
    [FEN, ap, WCK, WCQ, BCK, BCQ, mn, tn, fennaddon] = imageProcessing.addFENextras_fm (mof, halfFEN)
    [NBMnotValid, newFEN] = imageProcessing.StockfishComp(FEN)
    #if NBMnotValid: #not sure that this is done correctly. Supposed to recieve from the motors that the move is complete and give that info to the lcd
        #ser1.write("0,0,0".encode())
        # else:
    [newBoardState] = imageProcessing.fen2mof(newFEN)
    #oldBoard = oldBoard.tolist() # because it comes in as a numpy
    answer = imageProcessing.movementDirections(oldBoard, FEN, newBoardState, newFEN)

    #helps me visualize the board states
    print('old board:', oldBoard)
    numpyNewBoard = np.array(newBoardState)
    print('new board:', numpyNewBoard)
    print("actually gonna do the move")
    print(answer)
else:
    print ("Error")
