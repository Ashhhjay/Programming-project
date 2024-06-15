#Responsible for main game, handling user input and everything happening.

import pygame as p
import ChessEngine

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8 #Dimensions of the board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
initialize a global dictionary of images, this will be called exactly once in the maitain
'''

def loadImages(): #Loads images from the Images folder
    pieces = ["bR","bN","bB","bQ","bK","bP","wR","wN","wB","wQ","wK","wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    #NOTE: We can access an image by saying 'IMAGES['WP']'

'''
The main driver for our code. This will handle user input and update the graphics accordingly.
'''
def text1(string, coordx, coordy, fontSize): #Function to set text

    font = p.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)
def text2(string, coordx, coordy, fontSize): #Function to set text

    font = p.font.Font('freesansbold.ttf', fontSize) 
    #(255,255,255) is oppsite black
    text = font.render(string, True, (255, 255, 255)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,612))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made.
    loadImages() #Only do this once before the while loop.
    running = True
    sqSelected=() #No Square is selected initially - Will keep track of last click of the user.
    playerClicks = [] #keep track of players clicks. Will have 2 tuples [(6,4), (4,4)] This is the movement.
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse Handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #if the user clicks the same square twice.
                    sqSelected = () #Deselect
                    playerClicks = [] #Clears player clicks.
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #Append for both 1st and 2nd Clicks.
                if len(playerClicks) == 2: #after 2nd click.
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #Deselect
                        playerClicks = [] #Clears player clicks.
                        if gs.whiteToMove == True:
                            totalText = text2("Player 2 Move", 256, 578, 55)
                            screen.blit(totalText[0], totalText[1])
                            p.display.update()
                            totalText = text1("Player 1 Move", 256, 578, 55)
                            screen.blit(totalText[0], totalText[1])
                            p.display.update()
                        else:
                            totalText = text2("Player 1 Move", 256, 578, 55)
                            screen.blit(totalText[0], totalText[1])
                            p.display.update()
                            totalText = text1("Player 2 Move", 256, 578, 55)
                            screen.blit(totalText[0], totalText[1])
                            p.display.update()
                    else:
                        playerClicks = [sqSelected]
            #Key Handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo when Z is pressed
                    gs.undoMove()
                    
                    moveMade = False

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current Game State.
'''

def drawGameState(screen, gs):
    drawBoard(screen) #Draws squares on the board.
    #Add in piece highlighting or move suggestions ( Future )
    drawPieces(screen, gs.board) #Draws pieces on top of those squares.

'''
draws the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
'''
draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not an empty square.
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
