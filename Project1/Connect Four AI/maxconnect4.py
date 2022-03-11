#Adam Albawab | CSE 4308-002 | March 8, 2022
import sys
from MaxConnect4Game import *
import time
import re

def interactiveGame(currentGame, curr_player):
    currentGame.printGameBoard()
    currentGame.countScore()
    print(' Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    if curr_player == 'human-next':
        while currentGame.getPieceCount() != 42:
            print("\n It is your turn.")
            humanMove = input(" Enter a number between 1 and 7 to insert your piece: ")
            if humanMove and " " not in humanMove and humanMove!="\n" and re.match(r"[1-7]",str(humanMove)):
                humanMove=int(humanMove)
            if not 0<len(str(humanMove))<2 or isinstance(humanMove,str):
                print("\n Invalid column, re-enter column number.")
                continue
            if not currentGame.playPiece(humanMove - 1):
                print("\n Column number: %d is full. Try another column." % humanMove)
                continue
            currentGame.printGameBoard()
            currentGame.gameFile = open("human.txt", 'w')
            currentGame.printGameBoardToFile()
            currentGame.gameFile.close()
            print(' Score: Player1 = %d, Player-2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            if currentGame.getPieceCount() == 42:
                currentGame.countScore()
                #print(' Score: Player1 = %d, Player-2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
                print("\n No more moves possible.")
                break
            else:
                print("\n Computer is making a decision for next " + str(currentGame.depth) + " moves...")
                #start_time = time.time()
                currentGame.changeTurn()
                currentGame.aiPlay()
                #print(" Time: " + str(round(time.time() - start_time,4))+" seconds.")
                currentGame.printGameBoard()
                currentGame.gameFile = open('computer.txt', 'w')
                currentGame.printGameBoardToFile()
                currentGame.gameFile.close()
                currentGame.countScore()
                print(' Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    else:
        print("\n Computer is making a decision for next " + str(currentGame.depth) + " moves...")
        #start_time = time.time()
        currentGame.aiPlay()
        #print(" Time: " + str(round(time.time() - start_time,4))+" seconds.")
        currentGame.gameFile = open('computer.txt', 'w')
        currentGame.printGameBoardToFile()
        currentGame.gameFile.close()
        currentGame.countScore()
        interactiveGame(currentGame, 'human-next')

    if currentGame.getPieceCount() == 42:
        if currentGame.player1Score > currentGame.player2Score:
            print(" The game is over. Player 1 has won!")
        if currentGame.player1Score < currentGame.player2Score:
            print(" The game is over. Player 2 has won!")
        if currentGame.player1Score == currentGame.player2Score:
            print(" The game is over. The players have tied!")
        sys.exit()


def oneMoveGame(currentGame):
    if currentGame.piece_count >= 42: # Is the board full already?
        print('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)
    
    #start_time = time.time()
    currentGame.aiPlay() # Make a move
    #elapsed = round(time.time() - start_time,3)

    print (' Game state after move:')
    currentGame.printGameBoard()

    currentGame.countScore()
    print(' Score: Player1 = %d, Player-2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    #print(" Time: " + str(elapsed)+" seconds.")

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print('Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = MaxConnect4game()

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameboard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print('\n Game state before move:')
    # Update a few game variables based on initial state and print the score
    currentGame.pieceCount = currentGame.getPieceCount()
    currentGame.depth=argv[4]
    if game_mode == 'interactive':
        interactiveGame(currentGame, argv[3]) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.

if __name__ == '__main__':    
    main(sys.argv)