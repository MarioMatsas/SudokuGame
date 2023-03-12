from dokusan import generators

def generateBoard(difficulty):
    array = [[],[],[],[],[],[],[],[],[]]
    boardValues = str(generators.random_sudoku(avg_rank=difficulty))
    for row in array:
        for j in range(9):
            row.append(int(boardValues[j]))
        boardValues = boardValues[9: len(boardValues)] 
    return array     

