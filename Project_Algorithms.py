"""
Othello Game.

State = 2D array of size mxn
    Contents: 0 = empty
              1 = player 1
              2 = player 2
              3 = player 3...
state[y][x]
state = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,1,2,0,0,0],
         [0,0,0,2,1,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

"""
from Project_UI import *
import random
import os
import copy
# TRANSLATE_CHAR = {0:" ", 1:"W", 2:"B", 3:"R", 4:"G"}
# state = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,2,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
# state2 = [[2,2,2,0,0,0,0,0],
#           [2,1,2,2,2,2,2,0],
#           [2,2,1,1,1,1,2,0],
#           [0,2,1,0,1,1,2,0],
#           [0,2,1,1,1,1,2,0],
#           [0,2,1,1,1,1,2,0],
#           [0,2,1,1,1,1,2,0],
#           [0,2,2,2,2,2,2,0]]

prodSys = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
nPlayers = 4
depthLimit = 1
nodeCount = [0,0]

def isValidState(state,x,y):
    return True if (x >= 0 and x < len(state[0]) and y >= 0 and y < len(state)) else False

def stateOccupied(state,x,y):
    return True if (isValidState(state,x,y) and state[x][y] != 0) else False

def isValidMove(state, x, y):
    # Check that space is empty
    if not (isValidState(state,x,y) and not stateOccupied(state,x,y)):  return False
    # Check if an adjacent state is occupied (ie. playable)
    occupied = False; i = 0
    while (not occupied) and (i < len(prodSys)):
        occupied = stateOccupied(state, x+prodSys[i][0], y+prodSys[i][1])
        i += 1
    return occupied



def isGameOver(state):
    for y in range(len(state)):
        for x in range(len(state[0])):
            if state[x][y] == 0: return False
    return True

def move(state, x, y, player):
    newState = copy.deepcopy(state)
    newState[x][y] = player
    return capture(newState,x,y,player)

def capture(state, x, y, player):
    for action in prodSys:
        flag = False
        newX = x + action[0];  newY = y + action[1]
        while isValidState(state,newX,newY):
            # print("  (%s,%s), (%s,%s), (%s), state=%s, player=%s" % (x,y,newX,newY,action,state[newX][newY],player))
            if (state[newX][newY] == player):
                break
            elif (state[newX][newY] == 0):
                flag = True
                break
            else:
                newX = newX + action[0]
                newY = newY + action[1]

        if flag or not isValidState(state,newX,newY):
            continue
        nCaptures = max(abs(newX-x), abs(newY-y)) - 1
        # print("nCaptures:", nCaptures)
        for i in range(nCaptures):
            state[x+(action[0]*(i+1))][y+(action[1]*(i+1))] = player
    return state

#capture test
# displayUI(capture(move(state,5,4,2),5,4,2))
# displayUI(state2)
# displayUI(capture(move(state2,3,3,2),3,3,2))

def nextPlayer(player, nPlayers):
    return (player % nPlayers) + 1



class Node:

    def __init__(self, state, parent, x, y, player, value = [], allScores = []):
        self.state = state
        self.parent = parent
        self.x = x
        self.y = y
        self.player = player
        self.value = value
        self.allScores = allScores


    def __repr__(self):
        return "\n(%s, PAR=%s, x=%s, y=%s, PLAYER=%s, VAL=%s, SCORE=%s)" % (self.state, self.parent, self.x, self.y, self.player, self.value, self.allScores)


def successors(node):
    s = []
    for y in range(len(node.state)):
        for x in range(len(node.state[0])):
            if isValidMove(node.state,x,y):
                newState = move(node.state, x, y,node.player)
                newNode = Node(newState, node, x, y, nextPlayer(node.player, nPlayers))
                # print(node.state, "\n", newNode.state)
                if (node.state != newNode.state):
                    global nodeCount; nodeCount[0]+=1
                    s.append(newNode)
                # s.append(newState)
    # print("S[player%s] = \n" % (playerX), s)

    # print("S[player%s] = " % (playerX))
    # for x in s: print(x)
    return s

def calculateScore(state):
    score = []
    for i in range(nPlayers+1):
        score.append(0)
    for y in range(len(state)):
        for x in range(len(state[0])):
            score[state[x][y]] += 1
    score.pop(0)
    return score

def heuristic(node):
    newNode = Node(node.state, node.parent, node.x, node.y, node.player, node.value, calculateScore(node.state))
    return newNode


def maxN(node, depth):
    # depthLimit = 2
    if isGameOver(node.state) or depth >= depthLimit:
        return heuristic(node)
    else:
        value = float("-inf")
        previousValue = value
        tuple = []
        resultNode = node
        successorList = successors(node)
        random.shuffle(successorList)
        for s in successorList:
            # print(s)
            nodeCount[1]+=1
            tempNode = maxN(s, depth+1)
            # print("          value=%s, tempNodeScore=%s, prevTuple=%s, newTuple=%s, player=%s"%(value,tempNode.allScores[node.player-1],resultNode.allScores,tempNode.allScores,node.player))
            value = max(value, tempNode.allScores[node.player-1])
            if value != previousValue:
                previousValue = value
                resultNode = tempNode
        return resultNode

def whoWon(scores):
    maxScore = -1
    index = -1
    for i in range(len(scores)):
        if scores[i] > maxScore:
            maxScore = scores[i]
            index = i

    tie = False
    tieIndex = []
    for i in range(len(scores)):
        for j in range(len(scores)):
            if i != j and scores[i] == scores[j] and scores[i] == maxScore:
                tie = True
                if (i not in tieIndex): tieIndex.append(i)
                if (j not in tieIndex): tieIndex.append(j)
    if (tie):
        print("There is a tie between the following players:")
        for i in range(len(tieIndex)):
            print("  Player %s with a score of %s"%(tieIndex[i]+1,scores[i]))
    else:
        print("Player %s wins with a score of %s"%(index+1,maxScore))


def gridCreator(gridSize, type, players):
    # players = 2
    # start = "central"
    # gridSize = (6,6)
    grid = []
    for y in range(gridSize[0]):
        row = []
        for x in range(gridSize[1]):
            row.append(0)
        grid.append(row)

    x=gridSize[0]; y=gridSize[1]
    if type == "c":
        grid[(x//2)-1][(y//2)-1] = 1
        grid[(x//2)][(y//2)-1] = 2
        grid[(x//2)-1][(y//2)] = 2
        grid[(x//2)][(y//2)] = 1
    elif type == "p":
        for i in range(4):
            xOff = 1; yOff = 1
            if i == 0: xOff = 1; yOff = 1
            if i == 1: xOff = 3; yOff = 1
            if i == 2: xOff = 1; yOff = 3
            if i == 3: xOff = 3; yOff = 3
            p1 = 1; p2 = 2
            if players == 4 and (i==1 or i==2): p1 = 3; p2 = 4

            x = ((gridSize[0]//4)*xOff)
            y = ((gridSize[1]//4)*yOff)
            grid[x-1][y-1] = p1
            grid[x  ][y-1] = p2
            grid[x-1][y  ] = p2
            grid[x  ][y  ] = p1
    return grid


def testMaxN():
    node = Node(state, [], [], [], 1)
    res = maxN(node, 0)
    print(res)
    print("\n\nNodecount:", nodeCount)
    displayUI(res.state)
    while res.parent != []:
        res = res.parent
        displayUI(res.state)
    # print(successors(node))
# testMaxN()
