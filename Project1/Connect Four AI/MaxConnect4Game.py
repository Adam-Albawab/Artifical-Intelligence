#Adam Albawab | CSE 4308-002 | March 8, 2022
#!/usr/bin/env python

import copy
import random
import sys
import pickle
import numpy as n
from scipy.signal import convolve2d

utility = {}
score_list = []
inf = float('inf')


class MaxConnect4game:
    def __init__(self):
        self.gameboard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 0
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.depth = 1

    # Get the piece count without changing it
    def getPieceCount(self):
        return sum(1 for row in self.gameboard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print(' [1 2 3 4 5 6 7]')
        print(' ---------------')
        output = str(n.array(self.gameboard)).replace(' [', ' |').replace('[[', ' |').replace(']]', '|').replace(']', '|')
        print(output)
        print(' ---------------')

    def printGameBoardToFile(self):
        for row in self.gameboard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r')
        self.gameFile.write('%s\r' % str(self.currentTurn))

    def minmaxAlgorithm(self, depth):
        current_board = pickle.loads(pickle.dumps(self.gameboard))
        for i in range(7):
            if self.playPiece(i) != None:
                if self.pieceCount == 42 or self.depth == 0:
                    self.gameboard = pickle.loads(pickle.dumps(current_board))
                    return i
                else:
                    value = self.minValue(self.gameboard, -inf, inf, depth - 1)
                    utility[i] = value
                    self.gameboard = pickle.loads(pickle.dumps(current_board))

        maxUtility = max([i for i in utility.values()])
        for i in range(7):
            if i in utility:
                if utility[i] == maxUtility:
                    utility.clear()
                    return i

    def maxValue(self, cNode, a, b, depth):
        parent = pickle.loads(pickle.dumps(cNode))
        value = -inf
        children = []
        for i in range(7):
            current_board = self.playPiece(i)
            if current_board != None:
                children.append(self.gameboard)
                self.gameboard = pickle.loads(pickle.dumps(parent))
        if children == [] or depth == 0:
            self.countScore()
            return self.evalFunction(self.gameboard)
        else:
            for n in children:
                self.gameBoard = pickle.loads(pickle.dumps(n))
                value = max(value, self.minValue(n, a, b, depth - 1))
                if value >= b:
                    return value
                a = max(a, value)
            return value

    def minValue(self, cNode, a, b, depth):
        parent = pickle.loads(pickle.dumps(cNode))
        if self.currentTurn == 1:
            enemy = 2
        else:
            enemy = 1
        value = inf
        children = []
        for i in range(7):
            current_board = self.checkPiece(i, enemy)
            if current_board != None:
                children.append(self.gameboard)
                self.gameboard = pickle.loads(pickle.dumps(parent))

        if children == [] or depth == 0:
            self.countScore()
            return self.evalFunction(self.gameboard)
        else:
            for n in children:
                self.gameboard = pickle.loads(pickle.dumps(n))
                value = min(value, self.maxValue(n, a, b, depth - 1))
                if value <= a:
                    return value
                b = min(b, value)
        return value

    def evalFunction(self, current_board):
        if self.currentTurn == 2:
            human_symbol = 1
        else:
            human_symbol = 2
        computer4s = self.findConnections(current_board, self.currentTurn, 4)
        computer3s = self.findConnections(current_board, self.currentTurn, 3)
        computer2s = self.findConnections(current_board, self.currentTurn, 2)
        human4s = self.findConnections(current_board, human_symbol, 4)
        human3s = self.findConnections(current_board, human_symbol, 3)
        human2s = self.findConnections(current_board, human_symbol, 2)
        num = (computer4s * 20 + computer3s * 10 + computer2s * 5) - (human4s * 20 + human3s * 10 + human2s * 3)
        return num

    def findConnections(self, current_board, symbol, numConnection):
        total = 0
        for x in range(6):
            for y in range(7):
                if current_board[x][y] == symbol:
                    total += self.verticalConnections(x, y, current_board, numConnection)
                    total += self.horizontalConnections(x, y, current_board, numConnection)
                    total += self.diagonalConnections(x, y, current_board, numConnection)
        return total

    def verticalConnections(self, row, column, currentBoard, numConnection):
        counter = 0
        for x in range(row, 6):
            if currentBoard[x][column] == currentBoard[row][column]:
                counter += 1
            else:
                break
        if counter >= numConnection:
            return 1
        else:
            return 0

    def horizontalConnections(self, row, column, currentBoard, numConnection):
        counter = 0
        for y in range(column, 7):
            if currentBoard[row][y] == currentBoard[row][column]:
                counter += 1
            else:
                break
        if counter >= numConnection:
            return 1
        else:
            return 0

    def diagonalConnections(self, row, column, currentBoard, numConnection):
        counter = 0
        totalConnections = 0
        y = column
        for x in range(row, 6):
            if y > 6:
                break
            elif currentBoard[x][y] == currentBoard[row][column]:
                counter += 1
            else:
                break
            y += 1
        if counter >= numConnection:
            totalConnections += 1
        counter = 0
        y = column
        for x in range(row, -1, -1):
            if y > 6:
                break
            elif currentBoard[x][y] == currentBoard[row][column]:
                counter += 1
            else:
                break
            y += 1
        if counter >= numConnection:
            totalConnections += 1
        return totalConnections

    def aiPlay(self):
        answerColumn = self.minmaxAlgorithm(int(self.depth))
        answer = self.playPiece(answerColumn)
        if not answer:
            print(' No Result')
        else:
            print(" "+(" They have inserted a piece in column %d" % (answerColumn + 1)).lstrip())
            self.changeTurn()

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameboard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameboard[i][column]:
                    self.gameboard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

    def changeTurn(self):
        if self.currentTurn == 1:
            self.currentTurn = 2
        elif self.currentTurn == 2:
            self.currentTurn = 1

    def checkPiece(self, column, enemy):
        if not self.gameboard[0][column]:
            for x in range(5, -1, -1):
                if not self.gameboard[x][column]:
                    self.gameboard[x][column] = enemy
                    self.pieceCount += 1
                    return 1

    def countScore(self):
        self.player1Score = 0
        self.player2Score = 0
        horizontal = n.array([[ 1, 1, 1, 1]])
        vertical = n.transpose(horizontal)
        diagonal = n.eye(4, dtype=n.uint8)
        reverse_diagonal = n.fliplr(diagonal)
        kernels = [horizontal, vertical, diagonal, reverse_diagonal]
        current_board=n.array(self.gameboard)
        for k in kernels:
            self.player1Score += n.sum(convolve2d(current_board==1, k, mode="valid") == 4)
        for k in kernels:
            self.player2Score += n.sum(convolve2d(current_board==2, k, mode="valid") == 4)
