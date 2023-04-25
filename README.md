# ContinuousChessRobotImaging

This project is in correlation with a chess robot and aims to identify white (green) and black (purple) chess pieces in an image, continuously update a digital chess board, and output the next best move for the robot based on instructions.

## Image Assumptions

The code starts with a pre-cropped and perspective-transformed image of a chessboard. The following assumptions are made about the image:

- The image is taken from a relatively high angle with good lighting.
- Each piece is mostly centered on its corresponding tile.
- Each piece has a colored sticker (green for white, purple for black) to aid in recognition.
- The size of squares on the chessboard is consistent.

## Textfiles Folder

The "Textfiles" folder contains the following text files:

- `OriginalBoardState`: The initial board state.
- `Omof`: The initial board state in mock FEN notation.
- `Ofenextras`: The original FEN extras, which holds move number and castling rights.
- The following files get updated each time the code is run:
  - `Boardstate`: Updated board state.
  - `Differences`: Differences array, which stores the deltas indicating what piece moved where.
  - `MOF`: Updated mock FEN notation board.
  - `Fen`: Updated FEN notation board, including castling rights and turn number.
  - `Fenextras`: Updated FEN extras, including move number and castling rights.
  - `PreviousBoardstate`: Previous board state for comparison.

## How it Works

The image is color perspective-transformed into green and purple channels. Simultaneously, the image is split into 64 cells based on the assumed board dimensions, assuming a cropped image with consistent square sizes. The code then iterates through each cell to check for white or black chess pieces, updating the board state accordingly (where board state stores the color and position of each piece).

Next, the code compares the current board state with the previous board state to generate a differences array, which indicates the deltas or moves in standard algebraic notation (e.g., [e4e5]). The current "mockfen" board (an 8x8 array of pieces and 0's for empty cells) is then updated based on the differences array.

Using the updated "mockfen" board, the code generates FEN notation that can be read by a computer, taking into account castling rights and turn number. The FEN notation is then input into Stockfish to obtain the next best move and the updated FEN string for the current board state.

Finally, the code uncompresses the FEN string to update the digital board, and returns movement instructions for the robot.

## dependencies
- OpenCV
- Numpy
- https://pypi.org/project/stockfish/ 
- Subprocess
