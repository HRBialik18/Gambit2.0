import imp
import numpy as np

# Load the module from the file path
imageCapture = imp.load_source('imageCapture', 'SnapAndCrop/Edge+PerspTrans.py')
imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py')
imageProcessing = imp.load_source('imageProcessing', 'ImageProcessing.py')

def main(inputImPath, outputImPath):
    #imageProcessing.resetGame()
    #imageCapture.takeImage(inputImPath)
    #imageFixing.imageCropAndWarp(inputImPath, outputImPath)
    [oldBoard, diff] = imageProcessing.im2boardstate(outputImPath)
    [mof, neg_indices, pos_indices, arr_str] = imageProcessing.mofupdate(diff)  #issue in generating the mock fen
    halfFEN = imageProcessing.FENupdate (arr_str)
    [FEN, ap, WCK, WCQ, BCK, BCQ, mn, tn, fennaddon] = imageProcessing.addFENextras_fm (mof, halfFEN)
    [NBM, newFEN] = imageProcessing.StockfishComp(FEN)
    [newBoardState] = imageProcessing.fen2mof(newFEN)
    oldBoard = oldBoard.tolist() # because it comes in as a numpy
    
    [repRow, repCol, oldRow, oldCol, newRow, newCol] = imageProcessing.movementDirections(oldBoard, newBoardState )
    #print('old board:', board_array)
    numpyNewBoard = np.array(newBoardState) #helps me visualize
    print('new board:', numpyNewBoard)
    #print([repRow, repCol, oldRow, oldCol, newRow, newCol])
    #return [repRow, repCol, oldRow, oldCol, newRow, newCol]

main('Images/Tester Images/board.jpeg','Images/Tester Images/move2Cropped.jpg')


#imageProcessing.resetGame()