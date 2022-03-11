Name: Adam Albawab  ID#1001572887  CSE4380-002
------------------------------------------------------------
This program was written for Python 3.9.0. 
------------------------------------------------------------
The code is structured in two different programs. The first program named
maxconnect4.py is a program that contains the code used to parse the input
and call the methods contained within the MaxConnect4Game.py file as well 
as printing some of the output to screen.

The MaxConnect4Game.py file contains all of the methods used to actually
run the backend of the game as well as the AI component of the game.
The file is split into many methods. The most important methods are as follows:

1) minmaxAlgorithm - this method implements the minimax algorithm by using the
   two following methods to determine what the min and max value in order to 
   assign a utility value so that the AI can make decisions according to what
   the best move is. It is also depth-limited as the depth is dynamic as the
   program continues.
2) maxValue - this method finds the max value as well as performs half of the
   alpha-beta pruning
3) minValue - this method finds the min value as well as performs half of the
   alpha-beta pruning
4) evalFunction -  this function uses the function findConnections to find
   four, three, or two in a row for both players. Then it assigns a value
   based upon the number of these connections found. The value subtracts
   the human choices from the computer's choices while scaling them according
   to how valuable they ought to be. four is equal to a 20, three is equal to a 
   10, and 2 is equal to a 3.
5) findConnections - this calls methods used to iterate through the board and find
   all the connections for 4,3, and 2 in a row for horizontal, vertical, and diagonal.
6) countScore - This method uses convolve2d to count all of the four in a row for 
   both players and sum them up before returning them as the score.
------------------------------------------------------------------------
In order to run this program you should have Python 3.9.0 and you should
enter the following command into the command terminal:

python maxconnect4.py interactive input.txt computer-next 7

or

python maxconnect4.py one-move input.txt output.txt 7

Depending on whether you want to run one-move mode or interactive mode.
Furthermore if you want to see the time it takes to execute you should uncomment
lines 35, 38, 47, 49

Lastly, make sure the input has the same format as the sample input provided 
in this file.