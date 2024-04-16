import imp
import numpy as np
import serial

# Load the module from the file path
imageCapture = imp.load_source('imageCapture', 'SnapAndCrop/imageCapture.py')
imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py')
imageProcessing = imp.load_source('imageProcessing', 'ImageProcessing.py')
resetGame = imp.load_source('resetGame', 'Reset.py')

serial_port1 = '/dev/cu.usbmodem14301'  # Replace 'COM3' with the appropriate serial port
serial_port2 = '/dev/cu.usbmodem14301' 
baud_rate = 9600

# Create serial connection
ser1 = serial.Serial(serial_port1, baud_rate)
ser2 = serial.Serial(serial_port2, baud_rate)


def main(inputImPath, outputImPath):
    waitingForSerial = True
    data = 0
    while waitingForSerial:
       if ser1.in_waiting > 0:
            data = ser1.readline().decode().strip()
            waitingForSerial = False
    data = data.split(',')

    if data[1] == 1:
        print("got here1")
        resetGame.resetGame()
    elif data[2]: 
        print("got here2")      
        imageCapture.takeImage(inputImPath)
        imageFixing.imageCropAndWarp(inputImPath, outputImPath)
        [oldBoard, diff] = imageProcessing.im2boardstate(outputImPath)
        [mof, neg_indices, pos_indices, arr_str] = imageProcessing.mofupdate(diff)  #issue in generating the mock fen
        halfFEN = imageProcessing.FENupdate (arr_str)
        [FEN, ap, WCK, WCQ, BCK, BCQ, mn, tn, fennaddon] = imageProcessing.addFENextras_fm (mof, halfFEN)
        [NBMnotValid, newFEN] = imageProcessing.StockfishComp(FEN)
        [newBoardState] = imageProcessing.fen2mof(newFEN)
        #oldBoard = oldBoard.tolist() # because it comes in as a numpy
        answer = imageProcessing.movementDirections(oldBoard, FEN, newBoardState, newFEN)
        print('old board:', oldBoard)
        numpyNewBoard = np.array(newBoardState) #helps me visualize
        print('new board:', numpyNewBoard)
        print("got here3")
        print(answer)
        ser2.write(answer.encode())
        robotWorking = True
        while robotWorking:
            if ser2.in_waiting > 0:
                ser1.write("0,1".encode())
    elif data[2]:
        ser1.write("0,1".encode()) #[robotDone, gameOver, validMove]

main('Images/raw_image.jpg','Images/transformed_image.jpg')


#imageProcessing.resetGame()