#########
#IMPORTS#
#########

from stockfish import Stockfish

# Create Stockfish instance
stockfish = Stockfish(path= './stockfish')
import cv2
import numpy as np

###############################################################################################################################
#Function Definitions for easier Testing
###############################################################################################################################


def im2boardstate (impath): #Image to Boardstate and diff arrays
    
    #ARGS : Name of Image File

    #Returns : Array of Boardstate in 2,0,5 and array of differences with negative values as well

    #Loads the image
    
    image = cv2. imread(impath)
    image = cv2.GaussianBlur(image, (11,11), 0)
    pbs = np.loadtxt('Text Files/boardstate.txt')
    # Get the dimensions of the image
    height, width, channels = image.shape

    # Calculate the width and height of each cell in the grid
    cell_width = int(width / 8)
    cell_height = int(height / 8)

    # Split the image into a 8x8 grid of cells
    cells = []
    for i in range(8):
        for j in range(8):
            # Extract the cell from the image
            x = j * cell_width
            y = i * cell_height
            cell = image[y:y+cell_height, x:x+cell_width]
            cells.append(cell)
    # Process each cell in the grid and create the array
    board_array = np.zeros((8, 8), dtype=int)
    for i, cell in enumerate(cells):
        # Convert to HSV color space
        hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)

        # Define color ranges for green and purple dots
        green_lower = np.array([35, 50, 50])
        green_upper = np.array([75, 255, 255])
        purple_lower = np.array([110, 50, 150])
        purple_upper = np.array([160, 255, 255])
        # Create a mask for the green and purple dots
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        purple_mask = cv2.inRange(hsv, purple_lower, purple_upper)

        # Count the number of green and purple pixels in the cell
        green_count = cv2.countNonZero(green_mask)
        purple_count = cv2.countNonZero(purple_mask)

        # Determine if there is a green dot, purple dot, or neither in the cell
        if green_count > purple_count and green_count > 40:
            board_array[i // 8, i % 8] = 5
        elif purple_count > green_count and purple_count > 40:
            board_array[i // 8, i % 8] = 2
        else:
            board_array[i // 8, i % 8] = 0

    # Saves Board Arrays
    np.savetxt('Text Files/prevboardstate.txt', pbs, fmt='%d')
    np.savetxt('Text Files/boardstate.txt', board_array, fmt='%d')

    #Calculates Differences
    diff = board_array-pbs

    #saves the differences array
    np.savetxt('Text Files/differences.txt', diff, fmt='%d')

    return [board_array, diff]

#[board_array, diff] = im2boardstate('image2.jpg')
#print(board_array)
#print(diff)

''' 
def manimputboardstate (): #Manual change in Boardstate to new diff array

    #NO ARGUMENTS, JUST TAKES BOARD STATE AND PBS TEXT FILES FROM FOLDERS
    #RETURNS A DIFFERENCE ARRAY LIKE im2boardstate

    array1 = np.loadtxt('Text Files/prevboardstate.txt')
    array2 = np.loadtxt('Text Files/boardstate.txt')

    # create an empty 2D array to store the differences
    diff = array2-array1

    # Save the resulting array
    np.savetxt('Text Files/differences.txt', diff, fmt='%d')

    pbs = np.loadtxt('Text Files/boardstate.txt')
    np.savetxt('Text Files/prevboardstate.txt', pbs, fmt='%d')

    return diff
'''
# diff = manimputboardstate()
#print(diff)

def mofupdate (diff): #Given Diff Array, Updates MOCK fen

    #ARGS: TAKES A DIFFERENCE ARRAY FROM EITHER im2boardstate or manimputboardstate
    #RETURNS A NEW MOF STRING, Neg_Indicies, Pos_indicies for debugging purposes

    #opens mof file
    with open('Text Files/mof.txt', 'r') as file:
        # Initialize an empty 2D array
        mof = [[]]

        # Read the file one character at a time
        for char in file.read():
            # Ignore spaces and newlines
            if char != ' ' and char != '\n':
                # Append the character to the last sublist in the 2D array
                mof[-1].append(char)
                # If the sublist has 8 characters, start a new sublist
                if len(mof[-1]) == 8:
                    mof.append([])


    #notes locations of the negative and positive values in differences

    neg_indices = np.argwhere(diff < 0)
    pos_indices = np.argwhere(diff > 0)

    #saves row and column only for normal moves and white takes black moves
    if(len(pos_indices)>0 and len(neg_indices)>0):
        row1, col1 = neg_indices[0]
        row2, col2 = pos_indices[0]

    #update MOF file
    #determines what kind of move is played and translates that into the mof.txt file
    if (len(neg_indices) == 1 and len(pos_indices) == 1): # Standard movements (no takes) or white takes black
        #for one negative value and one positive value
        mof[row2][col2] = mof[row1][col1]
        mof[row1][col1] = '0'
    elif (len(neg_indices) > 1 and len(pos_indices) == 0): #black takes white
        #for two negative values
        row1, col1 = neg_indices[0]
        row2, col2 = neg_indices[1]
        if (abs(diff[row1][col1])>abs(diff[row2][col2])):
            mof[row1][col1] = mof[row2][col2]
            mof[row2][col2] = '0'
        else:
            mof[row2][col2] = mof[row1][col1]
            mof[row1][col1] = '0'
    elif (len(neg_indices) == 2 and len(pos_indices) == 2): # castles
        negR1, negC1 = neg_indices[0]
        negR2, negC2 = neg_indices[1]
        posR1, posC1 = pos_indices[0]
        posR2, posC2 = pos_indices[1]
        if(negR1 == 7 and negR2 == 7): #white castle
            if(negC2 == 7): #KINGSIDE
                mof[negR1][negC1] = '0'
                mof[negR2][negC2] = '0'
                mof[posR1][posC1] = 'R'
                mof[posR2][posC2] = 'K'
            elif(negC1 == 0): #QUEENSIDE
                mof[negR1][negC1] = '0'
                mof[negR2][negC2] = '0'
                mof[posR1][posC1] = 'K'
                mof[posR2][posC2] = 'R'
        elif(negR1 == 0 and negR2 == 0): #black castle
            if(negC2 == 7): #KINGSIDE
                mof[negR1][negC1] = '0'
                mof[negR2][negC2] = '0'
                mof[posR1][posC1] = 'r'
                mof[posR2][posC2] = 'k'
            elif(negC1 == 0): #QUEENSIDE
                mof[negR1][negC1] = '0'
                mof[negR2][negC2] = '0'
                mof[posR1][posC1] = 'r'
                mof[posR2][posC2] = 'k'
    arr_str = "\n".join([" ".join(row) for row in mof])

    # save the string to a text file
    with open('Text Files/mof.txt', "w") as f:
        f.write(arr_str)

    return [mof, neg_indices, pos_indices, arr_str]

#[newMOF, neg_indicies, pos_indicies, MOFtxt] = mofupdate(diff)
#print(MOFtxt)
#print(neg_indicies)
#print(pos_indicies)

def FENupdate (newMOF): #Given Mock Fen gives peice information in FEN notatoin
    # Initialize an empty 2D array to store the characters
    characters = []

    # Initialize a temporary row to store the characters in each row
    temp_row = []

    # Loop through each character in the string and add it to the 2D array (ignoring spaces and newlines)
    for i, char in enumerate(newMOF):
        if char != ' ' and char != '\n':
            temp_row.append(char)

            # If the temporary row contains 8 characters, add it to the 2D array and start a new row
            if len(temp_row) == 8:
                characters.append(temp_row)
                temp_row = []

    # If there are any remaining characters in the temporary row, add it to the 2D array as a partial row
    if len(temp_row) > 0:
        characters.append(temp_row)

    output_str = ""

    # Loop through each row in the 2D array
    for row in characters:
        # Initialize a counter for consecutive zeros
        zero_count = 0

        # Loop through each character in the row
        for char in row:
            # If the character is nonzero, add it to the output string and reset the zero count
            if char != '0':
                if zero_count > 0:
                    output_str += str(zero_count)
                    zero_count = 0
                output_str += char
            # If the character is zero, increment the zero count
            else:
                zero_count += 1

        # If there are any remaining consecutive zeros at the end of the row, add them to the output string
        if zero_count > 0:
            output_str += str(zero_count)

        # Add a forward slash between each row
        output_str += "/"

    # Remove the last forward slash from the output string
    output_str = output_str[:-1]

    if (newMOF != "no differences detected"):
        return output_str
    else:
        return 'no changes made to FEN'

#halfFEN = FENupdate (MOFtxt)
#print(halfFEN)
'''
def addFENextras_hm (newMOF, halfFEN): #Only if image is taken between EACH MOVE - given mock FEN and the peice information from halFEN Gets Full fen 

    #ARGS: New MOF and Half Fen string from FENUPDATE
    #RETURNS : FullFEN, Active Peice, White Castle KS, White Caslte QS, Black Castle KS, Black castle QS, Move #, Turn #
    mof = newMOF
    #Move Number, White Castle, Black Castle
    with open('Text Files/fenExtras.txt', 'r') as file:
        contents = file.read()

        # Split the contents by whitespace
        value = contents.split()

    #makes adjustments to fen extras
    #adds turn to turn-counter
    value[0] = int(value[0])
    value[0] = value[0] + 1

    #checks if white can castle at all
    if (mof[7][4] != 'K'): #checks to see if king moved
        value[1] = 'false'
        value[2] = 'false'
    else:
        #checks white castle queenside
        if(mof[7][0] != 'R'):#checks to see if shortside rook moved
            value[2] = 'false'
        #checks white castle kingside
        if(mof[7][7] != 'R'):#checks to see if longside rook moved
            value[1] = 'false'

    #checks if black can castle at all
    if (mof[0][4] != 'k'): #checks for black king
        value[3] = 'false'
        value[4] = 'false'
    else:
        #checks white castle queenside
        if(mof[0][0] != 'r'):#checks for shortisde rook
            value[4] = 'false'
        #checks white castle kingside
        if(mof[0][7] != 'r'):#checks for longside rook
            value[3] = 'false'

    #active piece
    if (value[0] %2 == 0):
        ap = 'b'
    else:
        ap = 'w'
    #move number
    mn = int((value[0] + (value[0]%2))/ 2)
    mn = str(mn)

    #Interprets the meaning of the values
    value[0] = str(value[0])

    if (value[1] == 'True'):
        WCK = 'K'
    else:
        WCK = ''

    if (value[2] == 'True'):
        WCQ = 'Q'
    else:
        WCQ = ''

    if (value[3] == 'True'):
        BCK = 'k'
    else:
        BCK = ''

    if (value[4] == 'True'):
        BCQ = 'q'
    else:
        BCQ = ''

    #addon string
    fenaddon = ' ' + ap + ' ' + WCK+WCQ+BCK+BCQ + ' - 0 ' + mn


    #new fen string
    FEN = halfFEN +fenaddon

    #updates fenextras
    with open('Text Files/fenExtras.txt', "w") as file:
        # Write the extracted values back to the file
        file.write(f"{value[0]} {str(value[1])} {str(value[2])} {str(value[3])} {str(value[4])}")

    #writes fen string into fen.txt
    with open('Text Files/fen.txt', 'w') as file:
        # Read the contents of the file into a string
        file_contents = file.write(FEN)

    return [FEN, ap, WCK, WCQ, BCK, BCQ, mn, value[0], fenaddon]
'''
#[FEN, ap, WCK, WCQ, BCK, BCQ, mn, tn, fennaddon] = addFENextras_hm (newMOF, halfFEN)
#print(FEN)
#print(fennaddon)

def addFENextras_fm (newMOF, halfFEN): #Only if image is taken between FULL MOVE -  same as other addFENextras but has to be used with engine  
    mof = newMOF
    output_str = halfFEN

    #reads the fen extras 
    #Move Number, White Castle, Black Castle
    with open('Text Files/fenExtras.txt', 'r') as file:
        contents = file.read()

        # Split the contents by whitespace
        value = contents.split()

    #makes adjustments to fen extras
    #adds turn to turn-counter
    value[0] = int(value[0])
    value[0] = value[0] + 2

    #checks if white can castle at all
    if (mof[7][4] != 'K'): #checks to see if king moved
        value[1] = 'false'
        value[2] = 'false'
    else:
        #checks white castle queenside
        if(mof[7][0] != 'R'):#checks to see if shortside rook moved
            value[2] = 'false'
        #checks white castle kingside
        if(mof[7][7] != 'R'):#checks to see if longside rook moved
            value[1] = 'false'

    #checks if black can castle at all
    if (mof[0][4] != 'k'): #checks for black king
        value[3] = 'false'
        value[4] = 'false'
    else:
        #checks white castle queenside
        if(mof[0][0] != 'r'):#checks for shortisde rook
            value[4] = 'false'
        #checks white castle kingside
        if(mof[0][7] != 'r'):#checks for longside rook
            value[3] = 'false'

    #active piece
    ap = 'b'

    #move number
    mn = int((value[0] + (value[0]%2))/ 2)
    mn = str(mn)

    #Interprets the meaning of the values
    value[0] = str(value[0])
    if (value[1] == 'True'):
        WCK = 'K'
    else:
        WCK = ''

    if (value[2] == 'True'):
        WCQ = 'Q'
    else:
        WCQ = ''

    if (value[3] == 'True'):
        BCK = 'k'
    else:
        BCK = ''

    if (value[4] == 'True'):
        BCQ = 'q'
    else:
        BCQ = ''

    #addon string
    fenaddon = ' ' + ap + ' ' + WCK+WCQ+BCK+BCQ + ' - 0 ' + mn

    #new fen string
    FEN = output_str+fenaddon

    #updates fenextras
    with open('Text Files/fenExtras.txt', "w") as file:
        # Write the extracted values back to the file
        file.write(f"{value[0]} {str(value[1])} {str(value[2])} {str(value[3])} {str(value[4])}")

    #writes fen string into fen.txt
    with open('Text Files/fen.txt', 'w') as file:
        # Read the contents of the file into a string
        file_contents = file.write(output_str)

    return [FEN, ap, WCK, WCQ, BCK, BCQ, mn, value[0], fenaddon]

# [FEN, ap, WCK, WCQ, BCK, BCQ, mn, tn, fennaddon] = addFENextras_fm (newMOF, halfFEN)
#print(FEN)
#print(fennaddon)

def StockfishComp (fen):
    fenvalidity = stockfish.is_fen_valid(fen)
    if fenvalidity := True:
        #sets the board position as current fen string
        stockfish.set_fen_position(fen)

        #next best move
        NBM = stockfish.get_best_move()
        stockfish.make_moves_from_current_position([NBM])
        newFEN = stockfish.get_fen_position()
    else:
        print('fen not valid')
    return [NBM, newFEN]

# [NBM, newFEN] = StockfishComp (FEN)
# print (NBM)
# print (newFEN)

def parse_fen(fen):
    board = []
    ranks = fen.split('/')
    for rank in ranks:
        row = []
        for char in rank:
            if char.isdigit():
                for i in range(int(char)):
                    row.append('0')
            else:
                row.append(char)
        board.append(row)
    return board

#newMOF = parse_fen(fen)

def replace_letters(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j].isupper():
                arr[i][j] = '5'
            elif arr[i][j].islower():
                arr[i][j] = '2'
    return arr

#newBoardState = replace_letters(arr)

def fen2mof(FEN: str):

    componenets = FEN.split()
    board = parse_fen(componenets[0])
    with open('Text Files/mof.txt', "w") as f:
        for i in range(8):
            for j in range(8):
                f.write(str(board[i][j]))
                f.write(' ')
            f.write('\n')
    boardState = replace_letters(board)
    #print(boardState)

    with open('Text Files/boardstate.txt', "w") as f:
        for i in range(8):
            for j in range(8):
                f.write(str(boardState[i][j]))
                f.write(' ')
            f.write('\n')
    return [boardState]

#I THINK THIS IS TESTING:
#FEN = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
#[newBoardState] = fen2mof(FEN)
#print('Board state:', newBoardState)


def read_txt_file(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the contents of the file and split by lines
        lines = file.readlines()
        
        # Initialize an empty 2D array to store the integers
        array_2d = []
        
        # Loop through each line and split by whitespace to get individual values
        for line in lines:
            values = line.strip().split()
            
            # Convert the values to integers and append to the 2D array
            array_2d.append([int(value) for value in values])
    
    # Return the 2D array of integers
    return array_2d

def sfdiff ():
    boardState = read_txt_file('Text Files/boardstate.txt')
    prevboardState = read_txt_file('Text Files/prevboardstate.txt')
    diff = boardState-prevboardState

    return diff

#sfdiff = sfdiff()
#print (sfdiff)


# Define the chessboard dimensions
BOARD_SIZE = 8

# Define the mapping of file (column) letters to corresponding indices
FILE_MAPPING = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

# Define the mapping of rank (row) numbers to corresponding indices
RANK_MAPPING = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

def get_file_and_rank(square):
    """Get the file (column) and rank (row) of a square in algebraic notation."""
    file = square[0]
    rank = square[1]
    return FILE_MAPPING[file], RANK_MAPPING[rank]

def get_square_from_file_and_rank(file, rank):
    """Get the square in algebraic notation from a file (column) and rank (row) index."""
    file_letter = [k for k, v in FILE_MAPPING.items() if v == file][0]
    rank_number = [k for k, v in RANK_MAPPING.items() if v == rank][0]
    return file_letter + rank_number

def calculate_tile_distance(start_square, end_square):
    """Calculate the number of tiles to move from the start square to the end square."""
    start_file, start_rank = get_file_and_rank(start_square)
    end_file, end_rank = get_file_and_rank(end_square)
    file_distance = start_file - end_file
    rank_distance = start_rank - end_rank
    return [file_distance, rank_distance]

def calculate_new_position(start_square, end_square):
    """Calculate the new position of the piece after moving from the start square to the end square."""
    start_file, start_rank = get_file_and_rank(start_square)
    end_file, end_rank = get_file_and_rank(end_square)
    new_file = end_file
    new_rank = end_rank
    return get_square_from_file_and_rank(new_file, new_rank)

def getpos (move: str):
    pos1 = move[0] + move[1]
    pos2 = move[2] + move[3]
    return [pos1, pos2]

def find_positions(move):
    pos1, pos2 = getpos(move)
    start_square1 = 'h8'
    end_square1 = pos1
    start_square2 =end_square1
    end_square2 = pos2 
    return [start_square1, end_square1, start_square2, end_square2]

def find_distances(move):
    pos = [0,0,0,0]
    pos[0], pos[1], pos[2], pos[3] = find_positions(move)
    print('Go to moving peice')
    tile_distance, rank_distance = calculate_tile_distance(pos[0], pos[1])
    new_position = calculate_new_position(pos[0], pos[1])
    print("Number of tiles to move:", tile_distance,"left",  rank_distance, "down")
    print("New position after move:", new_position)
    print('grab')

    print ('go to end position')
    tile_distance2, rank_distance2 = calculate_tile_distance(pos[2], pos[3])
    new_position2 = calculate_new_position(pos[2], pos[3])
    print("Number of tiles to move:", tile_distance2, "left",  rank_distance2, "down")
    print("New position after move:", new_position2)
    return

def updateELO (diff):
    elo = 3500 / (11 - diff)
    stockfish.set_elo_rating(elo)


def movementDirections(oldBoard, oldFEN, newBoard, newFEN):
    oldRow = 0
    oldCol = 0
    newRow = 0
    newCol = 0
    replacing = 0

    oldFEN = oldFEN.split()
    newFEN = newFEN.split()

    if oldFEN[2] != newFEN[2]:
        if oldFEN[2] == 'KQkq':
            return "30000"
        elif newFEN[2] == 'KQq':
            return "40000"

    for i, (row1, row2) in enumerate(zip(oldBoard, newBoard)):
        for j, (oldBoardElement, newBoardElement) in enumerate(zip(row1, row2)):
            if int(oldBoardElement) != int(newBoardElement):
                if (int(oldBoardElement) != 0) & (int(newBoardElement) != 0): #if neither are zero, means we're doing a replacement
                    replacing = 1
                    newRow = i
                    newCol = j
                    #print("piece to remove")
                    #print(f"oldBoard[{i}][{j}] = {oldBoardElement}")
                    #print(f"newBoard[{i}][{j}] = {newBoardElement}")
                elif int(oldBoardElement) != 0: #if the old board is not zero but the new board is then this is the locaiton that the piece used to be
                    oldRow = i
                    oldCol = j
                    #print("found olf location")
                    #print(f"oldBoard[{i}][{j}] = {oldBoardElement}")
                    #print(f"newBoard[{i}][{j}] = {newBoardElement}")
                else: #meaning that the new board is not zero but the old board was so we're moving to a new spot without knocking anybody
                    newRow = i
                    newCol = j
                    #print("found new location")
                    #print(f"oldBoard[{i}][{j}] = {oldBoardElement}")
                    #print(f"newBoard[{i}][{j}] = {newBoardElement}")

    return f"{replacing}{oldCol}{oldRow}{newCol}{newRow}"

'''
    for col in range(8):
        for row in range(8):
            if int(oldBoard[col][row]) != int(newBoard[col][row]):
                if (int(oldBoard[col][row]) != 0) & (int(newBoard[col][row]) != 0): #if neither are zero, means we're doing a replacement
                    repRow = row
                    repCol = col
                    newRow = row
                    newCol = col
                elif int(oldBoard[col][row]) != 0: #if the old board is not zero but the new board is then this is the locaiton that the piece used to be
                    oldRow = row
                    oldCol = col
                else: #meaning that the new board is not zero but the old board was so we're moving to a new spot without knocking anybody
                    newRow = row
                    newCol = col
'''

'''
def get_chess_move(prev_fen, next_fen):

    prev_fen = prev_fen.split()
    next_fen = next_fen.split()

    prev_board = prev_fen[0].split('/')
    next_board = next_fen[0].split('/')
    
    # Check for castling
    if prev_fen[2] != next_fen[2]:
        if next_fen[2] == 'KQkq':
            return "O-O~F"
        elif next_fen[2] == 'KQq':
            return "O-O-O~F"

    # Iterate over each square on the board
    for rank in range(8):
        for file in range(8):
            # Check if the piece on the board has changed
            if prev_board[rank][file] != next_board[rank][file]:
                # Identify the starting and ending squares of the move
                start_square = f"{chr(ord('a')+file)}{8-rank}"
                end_square = f"{chr(ord('a')+file)}{8-rank-1}"
                # Check if a capture occurred
                if next_board[rank][file] != '.':
                    return f"{start_square}~{end_square}~T"
                else:
                    return f"{start_square}~{end_square}~F"
    
    return "~F"  # If no differences are found
'''

