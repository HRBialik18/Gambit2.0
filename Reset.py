import numpy
def resetGame():
    with open('Text Files/Omof.txt', 'r') as input_file:
        # Read the contents of the input file
        file_contents = input_file.read()

        # Open the output file in write mode
        with open('Text Files/mof.txt', 'w') as output_file:
            # Write the contents of the input file to the output file
            output_file.write(file_contents)
    print("Reset mof")

    with open('Text Files/OriginalBoardState', 'r') as input_file:
        # Read the contents of the input file
        file_contents = input_file.read()

        # Open the output file in write mode
        with open('Text Files/boardstate.txt', 'w') as output_file:
            # Write the contents of the input file to the output file
            output_file.write(file_contents)

        with open('Text Files/prevboardstate.txt', 'w') as output_file:
            # Write the contents of the input file to the output file
            output_file.write(file_contents)
    print("Reset boardstate")
    print("reset prevboardstate")

    with open('Text Files/OfenExtras.txt', 'r') as input_file:
        # Read the contents of the input file
        file_contents = input_file.read()

        # Open the output file in write mode
        with open('Text Files/fenExtras.txt', 'w') as output_file:
            # Write the contents of the input file to the output file
            output_file.write(file_contents)
    print('reset fen extras')