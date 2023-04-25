# ContinuousChessRobotImaging
In correlation with the chess robot, Identifies white(green) and black(purple) pieces, and continually keeps track of and updates the digital chess board to output the next best move, and following instructions for the robot

This Code Starts with Taking a pre cropped (and prespective transformed image of a board)
  - The following assumptions are made about the image:
    - The image is taken from relativly high up with good lighting
    - Each peice is (mostly) centerd on the tile
    - Each peice has a colored sticker on it to help improve recognition (green for white purple for black)
    - The size of Squares on the board are consistent
 
In the Textfiles folder you have txt files which have the following information:
  - The inital board state (OriginalBoardState)
  - The inital board state in mock fen (Omof)
  - The orignial fen-extras which holds move number and castling rights (Ofenextras)
  - These following files get updated each time the code is run:
    - Boardstate
    - Differences
    - MOF
    - Fen 
    - Fen extras
    - Previous Boardstate
    
How does it Work?
  - The image gets color perspective transformed into green and purple
  - 
  - At the same time the image gets split into 64 cells, this is done by taking board dimensions
      - This assumes that the board is cropped and that the size of squares is consistent
  - It goes through each cells and checks to see if there is a white or black peice and updates the Boardstate accordingly 
      - (boardstate is stores the color of each peice and its position)
  - It then compares the current boardstate with the previous boardstate to get a differences array.
      - This gives us the deltas which tells us what peice moved and where it moved to (think of it as standard chess algebretic notation ie. [e4e5]
  - We then update our current board which is written in "mockfen" which just expands FEN notation into an 8x8 array of peices and 0's for empty cells
  - given the updated "mockfen" board we can then compress that into FEN that the computer can read and it checks for clastling rights as well as turn number
  - We put the FEN into stockfish to get the next best move as well as the updated FEN string for the current boardstate
  - We then uncompress the FEN string to get our own digital board which we update
  - Finally it returns movement instructions for the robot.
