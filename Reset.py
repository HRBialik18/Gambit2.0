import numpy

with open(r"C:\Users\youss\trial\Text Files\Omof.txt", 'r') as input_file:
    # Read the contents of the input file
    file_contents = input_file.read()

    # Open the output file in write mode
    with open(r"C:\Users\youss\trial\Text Files\mof.txt", 'w') as output_file:
        # Write the contents of the input file to the output file
        output_file.write(file_contents)
print("Reset mof")

with open(r"C:\Users\youss\trial\Text Files\OriginalBoardState", 'r') as input_file:
    # Read the contents of the input file
    file_contents = input_file.read()

    # Open the output file in write mode
    with open(r"C:\Users\youss\trial\Text Files\boardstate.txt", 'w') as output_file:
        # Write the contents of the input file to the output file
        output_file.write(file_contents)

    with open(r"C:\Users\youss\trial\Text Files\prevboardstate.txt", 'w') as output_file:
        # Write the contents of the input file to the output file
        output_file.write(file_contents)
print("Reset boardstate")
print("reset prevboardstate")

with open(r"C:\Users\youss\trial\Text Files\Ofenextras.txt", 'r') as input_file:
    # Read the contents of the input file
    file_contents = input_file.read()

    # Open the output file in write mode
    with open(r"C:\Users\youss\trial\Text Files\fenextras.txt", 'w') as output_file:
        # Write the contents of the input file to the output file
        output_file.write(file_contents)
print('reset fen extras')