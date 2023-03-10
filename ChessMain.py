"""
This is the main file for the chess game. It will be used to run the game.
"""
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512  # 400 is another option
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # Note: We can access an image by saying 'IMAGES['wp']'

"""
The main driver for our code. This will handle user input and updating the graphics.
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()  # only do this once, before the while loop
    drawBoard(screen)  # draw squares on the board
    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, column))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                column = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, column):  # the user clicked the same square twice
                    sqSelected = ()
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, column)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                if len(playerClicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()  # reset user clicks
                    playerClicks = []
                    
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        

"""
Responsible for all the graphics within a current game state.
"""
def drawGameState(screen, gs):
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares
    
"""
Draw the squares on the board. The top left square is always light.
"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Draw the pieces on the board using the current GameState.board.
"""    
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
    
if __name__ == "__main__":
    main()
    