import imp
import numpy as np
import serial

# Load the module from the file path
imageCapture = imp.load_source('imageCapture', 'SnapAndCrop/imageCapture.py')
imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py')
imageProcessing = imp.load_source('imageProcessing', 'ImageProcessing.py')
resetGame = imp.load_source('resetGame', 'Reset.py')

serial_port1 = '/dev/cu.usbmodem14301'  # Replace 'COM3' with the appropriate serial port
serial_port2 = '/dev/cu.usbmodem14301'#'/dev/cu.usbmodem141101 - IOUSBHostDevice' #'/dev/cu.usbmodem14301' 
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
            print("data:", data)
            waitingForSerial = False
    data = data.split(',')

    if data[1] == '1':
        print("game setup")
        imageProcessing.updateELO(int(data[0]))
        resetGame.resetGame()
    elif data[2] == '1': 
        print("finding robot move")      
        imageCapture.takeImage(inputImPath)
        imageFixing.imageCropAndWarp(inputImPath, outputImPath)
        [oldBoard, diff] = imageProcessing.im2boardstate(outputImPath)
        [mof, neg_indices, pos_indices, arr_str] = imageProcessing.mofupdate(diff)  #issue in generating the mock fen
        halfFEN = imageProcessing.FENupdate (arr_str)
        [FEN, ap, WCK, WCQ, BCK, BCQ, mn, tn, fennaddon] = imageProcessing.addFENextras_fm (mof, halfFEN)
        [NBMnotValid, newFEN] = imageProcessing.StockfishComp(FEN)
        if NBMnotValid: #not sure that this is done correctly
            ser1.write("0,0,0".encode())
        else:
            [newBoardState] = imageProcessing.fen2mof(newFEN)
            #oldBoard = oldBoard.tolist() # because it comes in as a numpy
            answer = imageProcessing.movementDirections(oldBoard, FEN, newBoardState, newFEN)
            print('old board:', oldBoard)
            numpyNewBoard = np.array(newBoardState) #helps me visualize
            print('new board:', numpyNewBoard)
            print("actually gonna do the move")
            print(answer)
            ser2.write(answer.encode())
            robotWorking = True
            while robotWorking:
                if ser2.in_waiting > 0:
                    ser1.write("0,1,1".encode())
    elif data[2]:
        print("aborted game")
        ser1.write("0,1,1".encode()) #[robotDone, gameOver, validMove]

while True:
    main('Images/raw_image.jpg','Images/transformed_image.jpg')


#imageProcessing.resetGame()

