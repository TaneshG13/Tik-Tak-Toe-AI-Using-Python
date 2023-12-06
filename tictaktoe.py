import sys
import pygame
import random
import copy
import numpy as np
from constants import *
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("TIC TAK TOE AI")
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.emptySquares = self.squares #[squares]
        self.markedSquares = 0
    def finalState(self, show=False):
        # vertical wins
        for col in range (COLS):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                if show==True:
                    pygame.draw.line(screen,STRIKE_COLOR,(col*SQ_SIZE+SQ_SIZE//2,20),(col*SQ_SIZE+SQ_SIZE//2,HEIGHT-20),LINE_WIDTH)
                return self.squares[0][col]
        # horizontal wins
        for row in range (ROWS):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                if show==True:
                    pygame.draw.line(screen,STRIKE_COLOR,(20,row*SQ_SIZE+SQ_SIZE//2),(WIDTH-20,row*SQ_SIZE+SQ_SIZE//2),LINE_WIDTH)
                return self.squares[row][0]
        # diagonal wins
        if self.squares[0][0]== self.squares[1][1] == self.squares[2][2]!=0:
            if show==True:
                pygame.draw.line(screen,STRIKE_COLOR,(20,20),(WIDTH-20,HEIGHT-20),LINE_WIDTH)
            return self.squares[0][0]
        if self.squares[0][2]== self.squares[1][1] == self.squares[2][0]!=0:
            if show==True:
                pygame.draw.line(screen,STRIKE_COLOR,(20,HEIGHT-20),(WIDTH-20,20),LINE_WIDTH)
            return self.squares[0][2]
        return 0
    def mark_squre(self,row,col,player):
        self.squares[row][col] = player
        self.markedSquares += 1
    def empty_square(self,row,col):
        return self.squares[row][col] == 0
    def getEmptySquares(self):
        emptySquares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row,col):
                    emptySquares.append((row,col))
        return emptySquares
    def isFull(self):
        return self.markedSquares == 9
    def isEmpty(self):
        return self.markedSquares == 0
    def exitWindow(self):
        if self.markedSquares == 9:
            font = pygame.font.Font('freesansbold.ttf', 32)
            font2 = pygame.font.Font('freesansbold.ttf', 72)
            text = font.render('Press R to restart', True, (0,255,0))
            text2 = font2.render('DRAW', True, (0,255,0))
            textRect = text.get_rect()
            textRect2 = text.get_rect()
            textRect.center = (WIDTH-SQ_SIZE-100, HEIGHT-SQ_SIZE)
            textRect2.center = ((WIDTH//2)+20, (HEIGHT//2))
            screen.blit(text, textRect)
            screen.blit(text2, textRect2)
        else:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Press R to restart', True, (0,255,0))
            textRect = text.get_rect()
            textRect.center = (WIDTH-SQ_SIZE-100, HEIGHT-SQ_SIZE)
            screen.blit(text, textRect)
class AI:
    def __init__(self, level = 1, player=2):
        self.level = level
        self.player = player
    
    def minimax(self, board, maximizing):
        # terminal case
        case = board.finalState()
        # Player 1 wins
        if case == 1:
            return 1, None
        # Player 2 wins
        if case == 2:
            return -1, None
        # draw
        if board.isFull():
            return 0, None
        
        # Algorithm
        if maximizing:
            maxEval = -100
            bestMove = None
            emptySquares = board.getEmptySquares()

            for (row,col) in emptySquares:
                tempBoard = copy.deepcopy(board)
                tempBoard.mark_squre(row,col,1)
                eval = self.minimax(tempBoard, maximizing= False)[0]
                if eval > maxEval:
                    maxEval = eval
                    bestMove = (row,col)
            return maxEval ,bestMove
        elif not maximizing:
            minEval = 100
            bestMove = None
            emptySquares = board.getEmptySquares()

            for (row,col) in emptySquares:
                tempBoard = copy.deepcopy(board)
                tempBoard.mark_squre(row,col,self.player)
                eval = self.minimax(tempBoard, maximizing= True)[0]
                if eval < minEval:
                    minEval = eval
                    bestMove = (row,col)

            return minEval, bestMove

    def eval(self, main_board):
        # Minimax algo choice
        eval, move = self.minimax(main_board, maximizing= False)
        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #player1 -> Cross , player2 -> Circle
        self.gamemode = "ai" 
        self.running = True
        self.showLines()
    def makeMove(self,row,col):
        self.board.mark_squre(row,col,self.player)
        self.drawFig(row,col)
        self.nextTurn()
    def showLines(self):
        screen.fill(BG_COLOR)
        # vertical
        pygame.draw.line(screen,LINE_COLOR,(SQ_SIZE,0), (SQ_SIZE,HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQ_SIZE,0), (WIDTH-SQ_SIZE,HEIGHT), LINE_WIDTH)
        # Horizontal
        pygame.draw.line(screen,LINE_COLOR,(0,SQ_SIZE), (WIDTH,SQ_SIZE), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQ_SIZE), (WIDTH,HEIGHT-SQ_SIZE), LINE_WIDTH)
    def drawFig(self,row,col):
        if self.player == 1:
            # Draw cross
            startD = (col*SQ_SIZE+OFFSET,row*SQ_SIZE+OFFSET)
            endD = (col*SQ_SIZE+SQ_SIZE-OFFSET,row*SQ_SIZE+SQ_SIZE-OFFSET)
            pygame.draw.line(screen,FIG_COLOR,startD,endD,LINE_WIDTH)
            startA = (col*SQ_SIZE+OFFSET,row*SQ_SIZE+SQ_SIZE-OFFSET)
            endA = (col*SQ_SIZE+SQ_SIZE-OFFSET,row*SQ_SIZE+OFFSET)
            pygame.draw.line(screen,FIG_COLOR,startA,endA,LINE_WIDTH)
        elif self.player == 2:
            # Draw Circle
            center = (col * SQ_SIZE + SQ_SIZE //2, row * SQ_SIZE + SQ_SIZE // 2)
            pygame.draw.circle(screen,FIG_COLOR,center,RADIUS,CIRCLE_WIDTH)
    def nextTurn(self):
        self.player = self.player % 2 + 1
    def isOver(self):
        return self.board.finalState(show=True) !=0 or self.board.isFull()
    def reset(self):
        self.__init__()

# main function for game loop
def main():
    # game object
    game = Game()
    ai = AI()
    board = game.board
    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = AI()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQ_SIZE
                col = pos[0] // SQ_SIZE

                if board.empty_square(row,col) and game.running:
                    game.makeMove(row,col)
                    if game.isOver():
                        game.running = False
                        board.exitWindow()
            
        if game.player == ai.player and game.running:
            pygame.display.update()
            # ai methods
            row,col = ai.eval(board)
            game.makeMove(row,col)
            if game.isOver():
                game.running = False
                board.exitWindow()
            
        pygame.display.update()

main()