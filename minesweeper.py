# File: proj3.py
# Author: Quintin Nguyen
# Date: 05.06.19
# Section: 15
# E-mail: bnguyen2@umbc.edu
# Description: Game simulation of Minesweeper


# prettyPrintBoard() prints the board with row and column labels,
#                    and spaces the board out so that it looks square
# Input:             board;   the rectangular 2d gameboard to print
# Output:            None;    prints the board in a pretty way
def prettyPrintBoard(board):
    print()  # empty line

    # if enough columns, print a "tens column" line above
    if len(board[0]) - 2 >= 10:
        print("{:25s}".format(""), end="")  # empty space for 1 - 9
        for i in range(10, len(board[0]) - 1):
            print(str(i // 10), end=" ")
        print()

    # create and print top numbered line
    print("       ", end="")
    # only go from 1 to len - 1, so we don't number the borders
    for i in range(1, len(board[0]) - 1):
        # only print the last digit (so 15 --> 5)
        print(str(i % 10), end=" ")
    print()

    # create the border row
    borderRow = "     "
    for col in range(len(board[0])):
        borderRow += board[0][col] + " "

    # print the top border row
    print(borderRow)

    # print all the interior rows
    for row in range(1, len(board) - 1):
        # print the row label
        print("{:3d}  ".format(row), end="")

        # print the row contents
        for col in range(len(board[row])):
            print(str(board[row][col]), end=" ")
        print()

    # print the bottom border row and an empty line
    print(borderRow, "\n")

    a = ""

    return a


# getValidFile() Prints a valid file to load the board from
# Parameters:    string; of the file the user wants to load
# Return:        list; of the printed board
def getValidFile():
    choice = input("Enter a file to load the board from: ")
    boardFile = open(choice)
    board = boardFile.readlines()

    return board


# playerBoard() Print the board that the player sees
# Parameter:    list; of the actual baord
# Return:       list; of the display board
def playerBoard(board):
    player = []

    # Iterates through touching squares
    for i in range(len(board)):
        row = board[i]
        rowList = []

        for i in range(len(row)):
            column = row[i]
            if column == " " or column == "*":
                column = "."

            rowList.append(column)

        player.append(rowList)

    return player


# fixBoard()  Just compresses the board
# Parameters: list; of the actual board
# Return:     list; of the modified board
def fixBoard(board):
    newBoard = []
    for i in range(len(board)):
        index = board[i]
        index = index[:len(index) - 1]
        newBoard.append(index)

    return newBoard


# howManyMines() Informs the user how many mines are on the board
# Parameters:    list; of the board
# Return:        string; of how many mines are on the field
def howManyMines(board, displayBoard):
    count = 0
    flags = 0

    # Counts how many mines
    for row in range(len(board)):
        rowString = board[row]

        for column in range(len(rowString)):
            if board[row][column] == "*":
                count += 1

    # Count how many flags are on the display board
    for row in range(len(displayBoard)):
        rowString = board[row]

        for column in range(len(rowString)):
            if displayBoard[row][column] == "f" and board[row][column] == "*":
                flags += 1

    totalCount = count - flags
    return totalCount


# getCoordinate() Validates user input for proper coordinates
# Parameters:     list; of the board
# Return:         list; of the row and column inputs
def getCoordinate(board):
    global row, column
    coordinate = []
    boardRows = len(board) - 2
    boardColumns = len(board[0]) - 2

    # Get valid row input
    print("Please choose the row:")
    rowInput = False
    while not rowInput:
        row = int(input("Enter a number between 1 and " + str(boardRows) + " (inclusive): "))

        if row >= 1 and row <= boardRows:
            rowInput = True
            coordinate.append(row)

        else:
            print("That number is not allowed. Please try again!")

    # Get valid column input
    print("Please choose the column")
    columnInput = False
    while not columnInput:
        column = int(input("Enter a number between 1 and " + str(boardColumns) + "(inclusive): "))

        if column >= 1 or column <= boardColumns:
            columnInput = True
            coordinate.append(column)

        else:
            print("That number is not allowed. Please try again!")

    coordinate = [row, column]

    return coordinate


# getValidChoice() Decides if the player wishes to reveal or flag
# Parameters:      None
# Return:          char; 'f' or 'r'
def getValidChoice():
    choice = ""

    validChoice = False
    while not validChoice:
        user = input("Enter 'r' to reveal the space, or \nenter 'f' \
 to mark the space with a flag: ")

        if user == 'r':
            validChoice = True
            return user

        if user == 'f':
            validChoice = True
            return user

        else:
            print("        That's not a valid action.")


# checkClue() Looks for any nearby mines
# Parameters: list; of the coordinates
#             list; of the board
# Return:     int; of how many bombs are nearby
def checkClue(coordinate, board):
    row = coordinate[0]
    column = coordinate[1]

    count = 0

    for x in range(row - 1, row + 2):

        if x < len(board[0]):
            for y in range(column - 1, column + 2):
                char = board[x][y]
                if char == "*":
                    count += 1

    return count


# printIsland() Prints open spaces and clues around the chosen coordinate
# Parameters: list; of the coordinates
#             list; of the actual board
#             list; of the display board
# Returns:    list; of the new with the island
def printIsland(coordinate, board, displayBoard):
    char = displayBoard[coordinate[0]][coordinate[1]]

    # Make sure that the spot being checked is valid
    if char == "." or char == "f":
        checkMines = 0
        for row in range(coordinate[0] - 1, coordinate[0] + 2):
            for col in range(coordinate[1] - 1, coordinate[1] + 2):
                char = board[row][col]
                if char == "*":
                    checkMines += 1

        # Recurse through open spaces to find mines or clues to create the island
        if checkMines == 0:

            displayBoard[coordinate[0]][coordinate[1]] = " "
            for row in range(coordinate[0] - 1, coordinate[0] + 2):
                for col in range(coordinate[1] - 1, coordinate[1] + 2):
                    char = displayBoard[row][col]
                    newCoordinate = [row, col]
                    printIsland(newCoordinate, board, displayBoard)

        else:
            displayBoard[coordinate[0]][coordinate[1]] = checkMines


def main():
    GAMEOVER = False

    board = getValidFile()
    board = fixBoard(board)
    displayBoard = playerBoard(board)

    prettyPrintBoard(displayBoard)
    numMines = howManyMines(board, displayBoard)
    print("There are", numMines, "left to find")

    while not GAMEOVER:

        coordinate = getCoordinate(board)
        choice = getValidChoice()

        char = board[coordinate[0]][coordinate[1]]

        if choice == "r":
            if char == "*":
                displayBoard[coordinate[0]][coordinate[1]] = "X"
                prettyPrintBoard(displayBoard)
                print("YOU BLEW A MINE! GAME OVER!")
                GAMEOVER = True

            else:
                numClues = checkClue(coordinate, board)

                if numClues > 0:
                    displayBoard[coordinate[0]][coordinate[1]] = numClues

                if numClues == 0:
                    printIsland(coordinate, board, displayBoard)
                    prettyPrintBoard(displayBoard)

                if char == "f":
                    print("The coordinate much be unflagged-first")

        if choice == "f":

            disChar = displayBoard[coordinate[0]][coordinate[1]]

            if disChar == ".":
                print("you got here")
                displayBoard[coordinate[0]][coordinate[1]] = "f"

            if disChar == "f":
                displayBoard[coordinate[0]][coordinate[1]] = "."

            if disChar == " ":
                displayBoard[coordinate[0]][coordinate[1]] = " "
                print("The coordinate cannot be flagged")

        prettyPrintBoard(displayBoard)
        print("      There are", howManyMines(board, displayBoard), "mines left to find")


main()
