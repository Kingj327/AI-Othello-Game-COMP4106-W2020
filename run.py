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
from Project_Algorithms import *
import random
import os
import copy
import time
# TRANSLATE_CHAR = {0:" ", 1:"W", 2:"B", 3:"R", 4:"G"}
state = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,2,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
state2P = [[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,1,2,0,0,0],
           [0,0,0,2,1,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0]]
state4P = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,1,2,0,0,0,0,0,0,3,4,0,0,0],
           [0,0,0,2,1,0,0,0,0,0,0,4,3,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,1,3,0,0,0,0,0,0,4,2,0,0,0],
           [0,0,0,3,1,0,0,0,0,0,0,2,4,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

state2P1 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]

state4Pocket = gridCreator([16,16], "p", 4)
state2Pocket = gridCreator([32,32], "p", 2)
state2Central = gridCreator([32,32], "c", 2)

START_STATE = state4Pocket
# prodSys = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
# nPlayers = 2
# nodeCount = [0,0]
# displayUI(state)




def A(state):
    x=-1; y=-1
    while not isValidMove(state,x,y):
        x = random.randint(0, len(state[0])-1)
        y = random.randint(0, len(state)-1)
    return x, y



def run(state):
    player = 1
    iteration = 0
    while not isGameOver(state):
        os.system('cls' if os.name=='nt' else 'clear')
        print("\n\niteration:", iteration)
        x, y = A(state)
        state = move(state, x, y, player)
        displayUI(state)
        player = nextPlayer(player, nPlayers)
        iteration += 1
    print("Complete.")

def run2(state):
    player = 1
    iteration = 1
    node = Node(START_STATE, [], [], [], 1)
    print("\n\nStart State:")
    displayUI(node.state)
    while not isGameOver(node.state):


        node = maxN(node,0)

        # displayUI(node.state)
        # while node.parent != []:
        #     if (node.parent.parent == []):
        #         break
        #     else:
        #         node = node.parent

        # print(node)
        if depthLimit > 1:
            for i in range(depthLimit-1):
                node = node.parent
        os.system('cls' if os.name=='nt' else 'clear')
        print("\n\niteration:", iteration)
        displayUI(node.state)
        print("Score:", node.allScores)
        print("Move: (%s,%s), Piece: %s"%(node.x,node.y,TRANSLATE_CHAR[player]))
        # print(node)
        time.sleep(0.1)
        # player = nextPlayer(player, nPlayers)
        player = node.player
        iteration += 1
    print("Complete.")
    whoWon(node.allScores)

# run(state)
run2(state)
# displayUI(gridCreator([32,32], "p", 4))
