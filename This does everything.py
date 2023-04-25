#########
#IMPORTS#
#########

from stockfish import Stockfish

# Create Stockfish instance
stockfish = Stockfish(path=r"C:\Users\youss\Downloads\stockfish_15.1_win_x64_popcnt\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe")
import cv2
import numpy as np
from Segmented_Code import *

###################
#Image Proccessing#
###################

# Load the image
imageName = '\SM-2.jpg'
imagepath = r"C:\Users\youss\trial\SM-Trial" + imageName
image = cv2.imread(imagepath)
pbs = np.loadtxt(r"C:\Users\youss\trial\Text Files\boardstate.txt")

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
    purple_lower = np.array([130, 50, 50])
    purple_upper = np.array([170, 255, 255])

    # Create a mask for the green and purple dots
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    purple_mask = cv2.inRange(hsv, purple_lower, purple_upper)

    # Count the number of green and purple pixels in the cell
    green_count = cv2.countNonZero(green_mask)
    purple_count = cv2.countNonZero(purple_mask)

    # Determine if there is a green dot, purple dot, or neither in the cell
    if green_count > purple_count:
        board_array[i // 8, i % 8] = 5
    elif purple_count > green_count:
        board_array[i // 8, i % 8] = 2
    else:
        board_array[i // 8, i % 8] = 0

# Print the board array
print('this is the boardstate')
print(board_array)
np.savetxt(r'C:\Users\youss\trial\Text Files\prevboardstate.txt', pbs, fmt='%d')
np.savetxt(r"C:\Users\youss\trial\Text Files\boardstate.txt", board_array, fmt='%d')

#Print the differences between board arrays
diff = board_array-pbs
print('these are the differences')
print(diff)

#saves the differences array
np.savetxt(r"C:\Users\youss\trial\Text Files\differences.txt", diff, fmt='%d')

###############################################################################################################
#Outputs are:
#Board_array, which is the board state
#pbs, which is previous board state
#diff, which is the differences betwee board state and pbs
################################################################################################################

####################################################################
#translates differences to mof file to create new mock - fen string#
####################################################################

#opens mof file
with open(r"C:\Users\youss\trial\Text Files\mof.txt", 'r') as file:
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

# Print the indices of the negative and positive values
print("Negative indices:", neg_indices)
print("Positive indices:", pos_indices)

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
with open(r"C:\Users\youss\trial\Text Files\mof.txt", "w") as f:
    f.write(arr_str)

##################################################################################
# Outputs are:
# mof.txt file with updated mof
##################################################################################

##################################################
#Translates Mock - FEN to FEN string for computer#
##################################################

# Open the file for reading
with open(r"C:\Users\youss\trial\Text Files\mof.txt", 'r') as file:
    # Read the contents of the file into a string
    file_contents = file.read()

# Initialize an empty 2D array to store the characters
characters = []

# Initialize a temporary row to store the characters in each row
temp_row = []

# Loop through each character in the string and add it to the 2D array (ignoring spaces and newlines)
for i, char in enumerate(file_contents):
    if char != ' ' and char != '\n':
        temp_row.append(char)

        # If the temporary row contains 8 characters, add it to the 2D array and start a new row
        if len(temp_row) == 8:
            characters.append(temp_row)
            temp_row = []

# If there are any remaining characters in the temporary row, add it to the 2D array as a partial row
if len(temp_row) > 0:
    characters.append(temp_row)

# Print out the 2D array of characters
for row in characters:
    print(row)

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

################################################################################################
#Outputs a nearly complete FEN string as output_str variable
################################################################################################

###################################################################################################
# Adds Fen Extras to end of FEN string to make it "Legal FEN"
# Addons:
# Active Color
# Castle Rights
# En Passant -  Hard to do -- will put it as always Enpassant illegal for simplicity
# Half Move Clock - Only for 50 move Rule, Will always set as 0 for simplicity
# Move Number
###################################################################################################

#reads the fen extras 
#Move Number, White Castle, Black Castle
with open(r"C:\Users\youss\trial\Text Files\fenExtras.txt", 'r') as file:
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
    print('active peice is black')
else:
    ap = 'w'
    print('active peice is white')

#move number
mn = int((value[0] + (value[0]%2))/ 2)
mn = str(mn)

#Interprets the meaning of the values
value[0] = str(value[0])
print('turn number ' + value[0])
print('move number ' + mn)
if (value[1] == 'True'):
    print("white can castle Kingside")
    WCK = 'K'
else:
    print('white cant castle Kingside')
    WCK = ''

if (value[2] == 'True'):
    print("white can castle Queenside")
    WCQ = 'Q'
else:
    print('white cant castle Queenside')
    WCQ = ''

if (value[3] == 'True'):
    print("black can castle Kingside")
    BCK = 'k'
else:
    print('black cant castle Kingside')
    BCK = ''

if (value[4] == 'True'):
    print("black can castle Queenside")
    BCQ = 'q'
else:
    print('black cant castle Queenside')
    BCQ = ''

#addon string
fenaddon = ' ' + ap + ' ' + WCK+WCQ+BCK+BCQ + ' - 0 ' + mn

#print(fenaddon)

#new fen string
output_str = output_str+fenaddon
print(output_str)

#updates fenextras
with open(r"C:\Users\youss\trial\Text Files\fenExtras.txt", "w") as file:
    # Write the extracted values back to the file
    file.write(f"{value[0]} {str(value[1])} {str(value[2])} {str(value[3])} {str(value[4])}")

#writes fen string into fen.txt
with open(r'C:\Users\youss\trial\Text Files\fen.txt', 'w') as file:
    # Read the contents of the file into a string
    file_contents = file.write(output_str)

##################################################################################################
# Stockfish/computational component
# Checks if the fen string is valid
# Calculates next best move
# provides new fen string based on next best move
##################################################################################################

#Checks If FEN is valid
fen = output_str
result = stockfish.is_fen_valid(fen)

# Print the result
print("Is fen valid")
print(result)

#sets the board position as current fen string
stockfish.set_fen_position(fen)

#next best move
NBM = stockfish.get_best_move()
stockfish.make_moves_from_current_position([NBM])
newFEN = stockfish.get_fen_position()
print ('Next Best Move is ' + NBM)
print ('this would be the new FEN')
print(newFEN)

#Movement commands for bot
find_distances (NBM)