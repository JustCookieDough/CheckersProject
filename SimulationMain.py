import pygame as p, random as r
import Variables as v, Peice, Square, StatisticsPanel


def main():
    p.init()  # just some setup stuff
    screen = p.display.set_mode((v.NUM_OF_SQUARES * v.SQ_SIZE + v.STAT_PANEL_WIDTH, v.NUM_OF_SQUARES * v.SQ_SIZE))
    clock = p.time.Clock()
    running = True
    paused = False
    sqList = spawnBoard()  # these lines spawn the pieces and board tiles
    redPeiceList = spawnRedPeices()
    blackPeiceList = spawnBlackPeices()
    while running:  # main loop of the function
        for e in p.event.get():  # checks for keyboard events and exiting
            if e.type == p.QUIT:  # stops the game if user clicks the x
                running = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    running = False
                if e.key == p.K_UP:
                    v.MAX_FPS *= 2
                if e.key == p.K_DOWN:
                    v.MAX_FPS /= 2
                if e.key == p.K_SPACE:
                    paused = not paused
        if not paused:
            for list in sqList: # draws all of the squares every frame
                for s in list:
                    s.draw(screen)
            for list in [redPeiceList, blackPeiceList]: # draws all peices
                for peice in list:
                    peice.draw(screen)
                shuffleList = list  # creates a randomly shuffled verson of the peice lists, and then moves the first peice it can in this list
                r.shuffle(shuffleList)  # this prevents an infinite loop halting the program if one player cant move
                for peice in shuffleList:
                    if peice.getPossibleMovements or peice.getPossibleAttacks:
                        peice.update(redPeiceList, blackPeiceList)
                        break
            if len(redPeiceList) == 0:  # win detection
                v.BLACK_WINS += 1
                redPeiceList = spawnRedPeices()
                blackPeiceList = spawnBlackPeices()
            if len(blackPeiceList) == 0:
                v.RED_WINS += 1
                redPeiceList = spawnRedPeices()
                blackPeiceList = spawnBlackPeices()
        try: # handles divide by zero errors
            StatisticsPanel.drawPanel(screen, "Red Wins: " + str(v.RED_WINS) + "\nBlack Wins: " + str(v.BLACK_WINS) + "\nTotal Games: " + str(v.BLACK_WINS + v.RED_WINS) + "\nRed Win %: " + str(int(100*(v.RED_WINS/(v.RED_WINS + v.BLACK_WINS)))) + "\nBlack Win %: " + str(int(100*(v.BLACK_WINS/(v.RED_WINS + v.BLACK_WINS)))) + "\n\n\nMax FPS: " + str(v.MAX_FPS) + "\nPaused: " +str(paused)) # draws the stat panel
        except ZeroDivisionError:
            StatisticsPanel.drawPanel(screen, "Red Wins: " + str(v.RED_WINS) + "\nBlack Wins: " + str(v.BLACK_WINS) + "\nTotal Games: " + str(v.BLACK_WINS + v.RED_WINS) + "\nRed Win %: 0\nBlack Win %: 0" + "\n\n\nMax FPS: " + str(v.MAX_FPS) + "\nPaused: " + str(paused)) # draws the stat panel
        p.display.flip()
        clock.tick(v.MAX_FPS) # updates screen at a given interval
    p.quit()


def spawnBoard(): # function that creates a list with the boards
    sqList = []
    for i in range(v.NUM_OF_SQUARES):
        sqList.append([])
        for j in range(v.NUM_OF_SQUARES):
            sqList[i].append(Square.Square(i, j))
    return sqList


def spawnRedPeices(): # function the creates a list with peices
    redPeiceList = []
    for i in range(v.NUM_OF_SQUARES):
        if i % 2 == 0:
            s = Peice.RedPeice(i, v.NUM_OF_SQUARES - 2)
            redPeiceList.append(s)
        else:
            s = Peice.RedPeice(i, v.NUM_OF_SQUARES - 1)
            redPeiceList.append(s)
            s = Peice.RedPeice(i, v.NUM_OF_SQUARES - 3)
            redPeiceList.append(s)
    return redPeiceList


def spawnBlackPeices(): # function the creates a list with peices
    blackPeiceList = []
    for i in range(v.NUM_OF_SQUARES):
        if i % 2 == 0:
            s = Peice.BlackPeice(i, 0)
            blackPeiceList.append(s)
            s = Peice.BlackPeice(i, 2)
            blackPeiceList.append(s)
        else:
            s = Peice.BlackPeice(i, 1)
            blackPeiceList.append(s)
    return blackPeiceList


main()
