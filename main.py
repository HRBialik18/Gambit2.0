import imp

# Load the module from the file path
imageCapture = imp.load_source('imageCapture', 'SnapAndCrop/Edge+PerspTrans.py')
imageFixing = imp.load_source('imageFixing', 'SnapAndCrop/Edge+PerspTrans.py')
imageProcessing = imp.load_source('imageProcessing', 'ImageProcessing.py')

def main(inputImPath, outputImPath):
    imageProcessing.resetGame()
    #imageCapture.takeImage(inputImPath)
    imageFixing.imageCropAndWarp(inputImPath, outputImPath)
    [board_array, diff] = imageProcessing.im2boardstate(outputImPath)
    [mof, neg_indices, pos_indices, arr_str] = imageProcessing.mofupdate(diff)
    halfFEN = imageProcessing.FENupdate (arr_str)
    [FEN, ap, WCK, WCQ, BCK, BCQ, mn, tn, fennaddon] = imageProcessing.addFENextras_fm (mof, halfFEN)
    [NBM, newFEN] = imageProcessing.StockfishComp (FEN)
    [newBoardState] = imageProcessing.fen2mof(newFEN)
    [repRow, repCol, oldRow, oldCol, newRow, newCol] = imageProcessing.movementDirections(board_array, newBoardState )
    print('old board:', board_array)
    print('new board', newBoardState)
    print([repRow, repCol, oldRow, oldCol, newRow, newCol])
main('Images/board.jpeg','Images/transformed_image.jpg')


#imageProcessing.resetGame()