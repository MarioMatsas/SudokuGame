import pygame
import sudoku_generator
from sudoku_solver import solve
from copy import deepcopy

#Set the window parameters
WIDTH = 550
HEIGHT = 700

#Create game window
window = pygame.display.set_mode((WIDTH, HEIGHT))

#Game difficulty(set to default)
difficulty = 250

#Get a valid sudoku board
board = sudoku_generator.generateBoard(difficulty)
boardCopy = deepcopy(board)
solvedCopy = deepcopy(board)

#Get the solution of this board
solve(solvedCopy)

#Variable used to count the number of times a button was clicked
clicks = 0

BUFFER = 5

def placeNumber(board, i, j, colour, font):
    #Place the solution on the screen
    char = font.render(str(board[i][j]), True, colour)
    window.blit(char, (50*(j+1) + 17, 50*(i+1) + 11 )) #Cordinates give us the distance form the y and x axis


def showSolution():
    global clicks
    font = pygame.font.SysFont("Times New Roman", 30)
    #If the clicks are divisable by 2, that means that the button will show the solution
    if clicks % 2 == 0:
        for i in range(9):
            for j in range(9):
                #Set text colour in case the input is the correct one, there is no input, or th einput is wrong
                if solvedCopy[i][j] == board[i][j] and board[i][j] == boardCopy[i][j]: #The colour of the original numbers stays the same
                    textColour = (20, 20, 20)
                elif solvedCopy[i][j] == board[i][j]:
                    textColour = (30, 0, 255)
                elif board[i][j] == 0:
                    textColour = (211, 211, 211) 
                else:
                    textColour = (250, 5, 5)
                #Cover the text text with a rectangle
                pygame.draw.rect(window, (251, 240, 230), ((j + 1)*50 + BUFFER, (i + 1)*50 + BUFFER , 50 - 2*BUFFER, 50 - 2*BUFFER))
                placeNumber(solvedCopy, i, j, textColour, font)
        clicks += 1
    #If the clicks are not divisable by 2, then button will hide the solution 
    else:
        for i in range(9):
            for j in range(9):
                #Hide the solution
                pygame.draw.rect(window, (251, 240, 230), ((j + 1)*50 + BUFFER, (i + 1)*50 + BUFFER, 50 - 2*BUFFER, 50 - 2*BUFFER))
                #Check whether a number has been placed in by the user
                if board[i][j] > 0 and board[i][j] == boardCopy[i][j]:
                    placeNumber(board, i, j, (20, 20, 20), font)
                elif board[i][j] > 0:
                    placeNumber(board, i, j, (30, 0, 255), font)
        clicks += 1

        
def newBoard():
    global clicks
    global board
    global boardCopy
    global solvedCopy
    global difficulty
    font = pygame.font.SysFont("Times New Roman", 30)
    if clicks % 2 != 0:
        clicks += 1
    board = sudoku_generator.generateBoard(difficulty)
    boardCopy = deepcopy(board)
    solvedCopy = deepcopy(board)
    solve(solvedCopy)
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(window, (251, 240, 230), ((j + 1)*50 + BUFFER, (i + 1)*50 + BUFFER, 50 - 2*BUFFER, 50 - 2*BUFFER))
            if board[i][j] > 0:
                placeNumber(board, i, j, (20, 20, 20), font)
    pygame.display.update()  
    

def insert(window, position):
    i, j = position[1], position[0]
    font = pygame.font.SysFont("Times New Roman", 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(boardCopy[i - 1][j - 1] != 0):
                    return
                #When placing a new number in a filled spot, covers the previous number
                pygame.draw.rect(window, (251, 240, 230), (position[0]*50 + BUFFER, position[1]*50 + BUFFER, 50 - 2*BUFFER, 50 - 2*BUFFER))
                if event.key == 48: #48 is the ASCII presentation of 0
                    board[i - 1][j - 1] = event.key - 48
                    pygame.display.update()
                    return
                if 0 < event.key - 48 < 10: #Making sure the values inputed are valid
                    char = font.render(str(event.key - 48), True, (20, 20, 20))
                    window.blit(char, (position[0]*50 + 17, position[1]*50 + 11))
                    board[i - 1][j - 1] = event.key - 48
                    pygame.display.update()
                    return
                return
            

class Button():
    def __init__(self, x, y, image, text, text_x, text_y, text_size, scale = 1):
        self.text_size = text_size
        self.text = text
        self.text_x = text_x
        self.text_y = text_y
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def clickButton(self):
        action = False
        #Mouse position
        position = pygame.mouse.get_pos()
        #Check if mouse is on the button
        if self.rect.collidepoint(position):
            #Check if the user clicked the button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        #Reset the button and allow the user to click it again
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action
    
    def draw(self, window):
        font = pygame.font.SysFont("Times New Roman", self.text_size)
        #Draw the buttons
        window.blit(self.image, (self.rect.x, self.rect.y))
        char = font.render(self.text, True, (20, 20, 20))
        window.blit(char, (self.text_x, self.text_y)) #Cordinates give us the distance form the y and x axis

        
def main():
    global clicks
    global board
    global boardCopy
    global solvedCopy
    global difficulty

    #Initializing pygame
    pygame.init() 
    
    basicImage = pygame.image.load("SudokuGame/test.png").convert_alpha()


    #Creating the buttons
    checkButton1 = Button(50, 550, basicImage, "Solution", 78, 560, 31)
    checkButton2 = Button(343, 550, basicImage, "Next Game", 353, 560, 31)
    easy = Button(50, 630, basicImage, "Easy", 73, 632, 24, 0.6)
    medium = Button(171, 630, basicImage, "Medium", 180, 632, 24, 0.6)
    hard = Button(289, 630, basicImage, "Hard", 310, 632, 24, 0.6)
    extreme = Button(407, 630, basicImage, "Extreme", 417, 632, 24, 0.6)



    #Set number font
    font = pygame.font.SysFont("Times New Roman", 30)

    #Set backround colour
    window.fill((251, 240, 230))

    #Place the buttons on the board
    checkButton1.draw(window)
    checkButton2.draw(window)
    easy.draw(window)
    medium.draw(window)
    hard.draw(window)
    extreme.draw(window)

    #Create the board
    for i in range(10):
        lineWidth = 1
        if i % 3 == 0:
            lineWidth = 3           
        
        #Adding the horizontal lines 
        pygame.draw.line(window, (0, 0, 0), (50 + 50*i, 50), (50 + 50*i, 500), lineWidth)
        #Adding the vertical lines
        pygame.draw.line(window, (0, 0, 0), (50, 50 + 50*i), (500, 50 + 50*i), lineWidth)

    #Place the given numbers on the board
    for i in range(9):
        for j in range(9):
            if board[i][j] > 0:
                placeNumber(board, i, j, (20, 20, 20), font)
    
    pygame.display.update()

    #Gane loop
    while True:

        #Event handler
        for event in pygame.event.get():
            if checkButton1.clickButton():
                showSolution()
                pygame.display.update()
            if checkButton2.clickButton():
                newBoard()
            if easy.clickButton():
                difficulty = 100
                newBoard()
            if medium.clickButton():
                difficulty = 250
                newBoard()
            if hard.clickButton():
                difficulty = 450
                newBoard()
            if extreme.clickButton():
                difficulty = 600
                newBoard()     
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                position = pygame.mouse.get_pos()
                if 50 < position[0] < 500 and 50 < position[1] < 500: 
                    insert(window, (position[0]//50, position[1]//50))
            #If you close the window the game ends
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()
