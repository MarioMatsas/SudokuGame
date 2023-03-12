from sudoku_generator import generateBoard

#Check if the number you want to place appears in the same row 
def checkHorizontal(row, num, board):
    for col in range(9):
        if board[row][col] == num:
            return False
    return True

#Check if the number you want to place appears in the same column
def checkVertical(col, num, board):
    for row in range(9):
        if board[row][col] == num:
            return False
    return True

#Check if the number you want to place appears in the same sub-grid
def checkSubGrid(row, col, num, board):
    xCord = row//3
    yCord = col//3

    for i in range(xCord*3, xCord*3+3):
        for j in range(yCord*3, yCord*3+3):
            if board[i][j] == num:
                return False
    return True

#Check if the number you want to place is overall valid
def isValid(row, col, num, board):
    return checkHorizontal(row, num, board) and checkVertical(col, num, board) and checkSubGrid(row, col, num, board)

#Solve the given sudoku board
def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  #Check if the spot is empty
                for num in range(1, 10):
                    if isValid(row, col, num, board):
                        board[row][col] = num

                        if solve(board):
                            return True
                        else:
                            board[row][col] = 0
                return False
    return True


