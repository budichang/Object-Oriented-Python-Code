# Game class

from Square import *
import random

class Game():
    START_LEFT = 35
    START_TOP = 30
    PLAY_SOUND = True
    DONT_PLAY_SOUND = False

    def __init__(self, window):
        self.window = window
        '''
        The game board is made up of 4 rows and 4 columns - 16 squares,
        with 15 labelled images (1 to 15) and a blank square image.
        However, because Python lists and tuples start at zero, the squares
        are internally numbered (indexed) 0 to 15, like this:
             0  1  2  3
             4  5  6  7
             8  9 10 11
            12 13 14 15
        (A Square is an area of the window, each contains a tile, which is movable.)

        The following is a dict of squareNumber:tuple.  Each tuple contains all
        moves (vertical and horizontal neighbors) that can switch with this square.
        For example, for Square 0, only Squares 1 and 4 are legal moves.
        '''

        LEGAL_MOVES_DICT = {
            0:(1, 4),
            1:(0, 2, 5),
            2:(1, 3, 6),
            3:(2, 7),
            4:(0, 5, 8),
            5:(1, 4, 6, 9),
            6:(2, 5, 7, 10),
            7:(3, 6, 11),
            8:(4, 9, 12),
            9:(5, 8, 10, 13),
            10:(6, 9, 11, 14),
            11:(7, 10, 15),
            12:(8, 13),
            13:(9, 12, 14),
            14:(10, 13, 15),
            15:(11, 14)}

        yPos = Game.START_TOP
        self.squaresList = []

        # Create list of Tile objects
        for row in range(0, 4):
            xPos = Game.START_LEFT
            for col in range(0, 4):
                squareNumber = (row * 4) + col
                legalMovesTuple = LEGAL_MOVES_DICT[squareNumber]
                oSquare = Square(self.window, xPos, yPos, squareNumber, legalMovesTuple)
                self.squaresList.append(oSquare)
                xPos = xPos + SQUARE_WIDTH
            yPos = yPos + SQUARE_HEIGHT

        self.soundTick = pygame.mixer.Sound('sounds/tick.wav')
        self.soundApplause = pygame.mixer.Sound('sounds/applause.wav')
        self.soundNope = pygame.mixer.Sound('sounds/nope.wav')

        self.playing = False
        self.startNewGame()

    def startNewGame(self):
        # Tell all Squares to reset themselves
        for oSquare in self.squaresList:
            oSquare.reset()

        self.openSquareNumber = STARTING_OPEN_SQUARE_NUMBER  # index of the open space

        for i in range(0, 200):  # make 200 arbitrary moves to randomize
            legalMovesForThisTile = self.squaresList[self.openSquareNumber].getLegalMoves()
            nextMoveNumber = random.choice(legalMovesForThisTile)

            # switch Tiles associated with Squares
            self.switch(nextMoveNumber, Game.DONT_PLAY_SOUND)
            self.openSquareNumber = nextMoveNumber

        self.playing = True
        #print('Open space is at index:', self.openSquareNumber)

    def gotClick(self, clickLoc):
        if not self.playing:
            return  # game is over, waiting for Restart button

        for oSquare in self.squaresList:
            if oSquare.clickedInside(clickLoc):
                squareNumber = oSquare.getSquareNumber()
                # print('Got a mouseDown on square number:', squareNumber)
                legalMovesForOpenSpaceTuple = self.squaresList[self.openSquareNumber].getLegalMoves()
                legalMove = squareNumber in legalMovesForOpenSpaceTuple

                if legalMove:
                    self.switch(squareNumber, Game.PLAY_SOUND)
                else:  # illegal move (not next to the open space)
                    self.soundNope.play()
                return

    # Switch the Tile of a Square with the open space
    def switch(self, squareNumberToSwitch, playMoveSound):
        oSquareToMove1 = self.squaresList[squareNumberToSwitch]
        oSquareToMove2 = self.squaresList[self.openSquareNumber]

        oSquareToMove1.switch(oSquareToMove2)

        self.openSquareNumber = squareNumberToSwitch  # set the new number of open space

        if playMoveSound == Game.PLAY_SOUND:
            self.soundTick.play()

    def checkForWin(self):
        if not self.playing:
            return False

        for number in range(0, NSQUARES):
            if not self.squaresList[number].isTileInProperPlace(number):
                return False

        # All in proper place, game over
        self.playing = False
        self.soundApplause.play()
        return True

    def getGamePlaying(self):
        return self.playing

    def stopPlaying(self):
        self.playing = False

    def draw(self):
        for oSquare in self.squaresList:
            oSquare.draw()
