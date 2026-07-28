# Duck Game Engine (working pre-currentBoard refactor)
import random
INVALID = -1
EMPTY = 0
CURRENT_AI="Gary"

PLAYER1BODY = 1
PLAYER1BEAK = 2

PLAYER2BODY = 3
PLAYER2BEAK = 4
selectedX = None
selectedY = None

currentPlayer = 1
currentOrientation = 0

fig = None
ax = None
selectedMap=0
selectedAI=0




def ResetBoard(mapNumber=0):

    global board

    board=[]

    if mapNumber==0:

        # Classic

        board=[
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],

            [-1,-1,-1,-1,0,0,0,0,0],
            [-1,-1,-1,-1,0,0,0,0,0],
            [-1,-1,-1,-1,0,0,0,0,0],
            [-1,-1,-1,-1,0,0,0,0,0],
            [-1,-1,-1,-1,0,0,0,0,0],
            [-1,-1,-1,-1,0,0,0,0,0]
        ]

    elif mapNumber==1:

        # River

        board=[
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0],
            [0,0,0,0,-1,0,0,0,0]
        ]

    elif mapNumber==2:

        # Empty

        board=[
    [-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1, 0, 0, 0, 0, 0, 0, 0,-1],
    [-1, 0, 0, 0, 0, 0, 0, 0,-1],
    [-1, 0, 0, 0, 0, 0, 0, 0,-1],
    [-1, 0, 0, 0, 0, 0, 0, 0,-1],
    [-1, 0, 0, 0, 0, 0, 0, 0,-1],
    [-1, 0, 0, 0, 0, 0, 0, 0,-1],
    [-1, 0, 0, 0, 0, 0, 0, 0,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ]

def PrintBoard():
    for y in range(len(board)):
        for x in range(len(board[y])):
            v=board[y][x]
            if v==INVALID: print(" ",end=" ")
            elif v==EMPTY: print(".",end=" ")
            elif v==PLAYER1BODY: print("Y",end=" ")
            elif v==PLAYER1BEAK: print("B",end=" ")
            elif v==PLAYER2BODY: print("G",end=" ")
            elif v==PLAYER2BEAK: print("b",end=" ")
        print()

def SquareExists(x,y):
    if x<0 or x>8 or y<0 or y>8: return False
    return board[y][x]!=INVALID

def SquareEmpty(x,y):
    return SquareExists(x,y) and board[y][x]==EMPTY

def MyBeak(x,y,player):
    if not SquareExists(x,y): return False
    if player==1: return board[y][x]==PLAYER1BEAK
    return board[y][x]==PLAYER2BEAK

duckOrientations=[
[[0,0],[-1,0],[-1,-1],[-2,-1]],
[[0,0],[0,-1],[1,-1],[1,-2]],
[[0,0],[1,0],[1,1],[2,1]],
[[0,0],[0,1],[-1,1],[-1,2]],
[[0,0],[1,0],[1,-1],[2,-1]],
[[0,0],[0,1],[1,1],[1,2]],
[[0,0],[-1,0],[-1,1],[-2,1]],
[[0,0],[0,-1],[-1,-1],[-1,-2]]
]

def CheckMove(x,y,o,player):
    d=duckOrientations[o]
    bx=x+d[0][0]; by=y+d[0][1]
    if not SquareExists(bx,by): return False
    if (not SquareEmpty(bx,by)) and (not MyBeak(bx,by,player)): return False
    for i in range(1,4):
        xx=x+d[i][0]; yy=y+d[i][1]
        if not SquareExists(xx,yy): return False
        if not SquareEmpty(xx,yy): return False
    return True

def FindAllMoves(player):
    m=[]
    for y in range(9):
        for x in range(9):
            for o in range(len(duckOrientations)):
                if CheckMove(x,y,o,player):
                    m.append([x,y,o])
    return m

def PlaceDuck(x,y,o,player):
    d=duckOrientations[o]
    bx=x+d[0][0]; by=y+d[0][1]
    if SquareEmpty(bx,by):
        board[by][bx]=PLAYER1BEAK if player==1 else PLAYER2BEAK
    for i in range(1,4):
        xx=x+d[i][0]; yy=y+d[i][1]
        board[yy][xx]=PLAYER1BODY if player==1 else PLAYER2BODY

def ChangePlayer(player):
    return 2 if player==1 else 1

def CopyBoard(oldBoard):
    new = []
    for row in oldBoard:
        new.append(row[:])
    return new
def RandomMove(player):

    moves = FindAllMoves(player)

    if len(moves) == 0:
        return False

    move = random.choice(moves)

    PlaceDuck(move[0], move[1], move[2], player)

    return True
def CountBeaks(player):

    total = 0

    if player == 1:
        beak = PLAYER1BEAK
    else:
        beak = PLAYER2BEAK

    for row in board:
        for square in row:
            if square == beak:
                total += 1

    return total
def CountNeighbours(row, col):

    total = 0

    for dr in [-1,0,1]:
        for dc in [-1,0,1]:

            if dr == 0 and dc == 0:
                continue

            newRow = row + dr
            newCol = col + dc

            if newRow < 0 or newRow > 8:
                continue

            if newCol < 0 or newCol > 8:
                continue

            if board[newRow][newCol] != EMPTY:
                total += 1

    return total
#terrance enginges

def CreateVisited():

    visited = []

    for row in board:

        newRow = []

        for square in row:
            newRow.append(False)

        visited.append(newRow)

    return visited
def FloodFill(startRow, startCol, visited, player, otherPlayer):

    queue = []
    queue.append([startRow,startCol])

    visited[startRow][startCol] = True

    size = 0
    touchesMe = False
    touchesThem = False
    
    if player == 1:
        myBeak = PLAYER1BEAK
        theirBeak = PLAYER2BEAK
    else:
        myBeak = PLAYER2BEAK
        theirBeak = PLAYER1BEAK

    while len(queue) > 0:

        square = queue.pop(0)

        row = square[0]
        col = square[1]

        size += 1

        for dr in [-1,0,1]:
            for dc in [-1,0,1]:

                if abs(dr) + abs(dc) != 1:
                    continue

                newRow = row + dr
                newCol = col + dc

                if newRow < 0 or newRow > 8:
                    continue

                if newCol < 0 or newCol > 8:
                    continue

                if board[newRow][newCol] == myBeak:
                    touchesMe = True
                    continue

                if board[newRow][newCol] == theirBeak:
                    touchesThem = True
                    continue

                if visited[newRow][newCol]:
                    continue

                if board[newRow][newCol] != EMPTY:
                    continue

                visited[newRow][newCol] = True
                queue.append([newRow,newCol])

    return [size, touchesMe, touchesThem]

def CanIWin(player):

    moves = FindAllMoves(player)

    if len(moves) == 0:
        return False

    otherPlayer = ChangePlayer(player)

    global board

    for move in moves:

        oldBoard = board
        board = CopyBoard(board)

        PlaceDuck(move[0], move[1], move[2], player)

        if CanIWin(otherPlayer) == False:

            board = oldBoard
            return True

        board = oldBoard

    return False

def BartholomewMove(player):
#restriction for data purposes
    moves = FindAllMoves(player)

    print(len(moves))

    if len(moves) > 60:
        return GreedyMove(player, Octavia)

    if len(moves) == 0:
        return False

    otherPlayer = ChangePlayer(player)

    global board

    for move in moves:

        oldBoard = board
        board = CopyBoard(board)

        PlaceDuck(move[0], move[1], move[2], player)

        if CanIWin(otherPlayer) == False:

            board = oldBoard

            PlaceDuck(move[0], move[1], move[2], player)

            return True

        board = oldBoard

    return GreedyMove(player, Octavia)
    #PlaceDuck(moves[0][0], moves[0][1], moves[0][2], player)


    return True

#engines
def Gary(player, otherPlayer,move):

    return len(FindAllMoves(player))

def Velma(player, otherPlayer,move):

    return -len(FindAllMoves(otherPlayer))
    
def Octavia(player, otherPlayer,move):

    myMoves = len(FindAllMoves(player))
    otherMoves = len(FindAllMoves(otherPlayer))

    return myMoves - otherMoves

def Cuthbert(player, otherPlayer, move):

    return CountBeaks(player)
def Barry(player, otherPlayer, move):

    myMoves = len(FindAllMoves(player))
    otherMoves = len(FindAllMoves(otherPlayer))

    score = myMoves - otherMoves

    row = move[0]
    col = move[1]
    orientation = move[2]

    for i in range(1,4):

        bodyRow = row + duckOrientations[orientation][i][0]
        bodyCol = col + duckOrientations[orientation][i][1]

        score += CountNeighbours(bodyRow, bodyCol)

    return score
def Terrance(player, otherPlayer, move):

    myMoves = len(FindAllMoves(player))
    otherMoves = len(FindAllMoves(otherPlayer))

    score = myMoves - otherMoves

    visited = CreateVisited()

    for row in range(9):
        for col in range(9):

            if board[row][col] != EMPTY:
                continue

            if visited[row][col]:
                continue

            region = FloodFill(row, col, visited, player, otherPlayer)

            size = region[0]
            touchesMe = region[1]
            touchesThem = region[2]

            if touchesMe and not touchesThem:
                score += size

            if touchesThem and not touchesMe:
                score -= size

    return score
    
def GreedyMove(player,ScoreFunction):

    moves = FindAllMoves(player)

    if len(moves) == 0:
        return False

    bestMove = moves[0]
    bestScore = -1

    for move in moves:

        global board

        oldBoard = board
        board = CopyBoard(board)

        PlaceDuck(move[0], move[1], move[2], player)
        if player == 1:
            otherPlayer = 2
        else:
            otherPlayer = 1

        myMoves = len(FindAllMoves(player))
        otherMoves = len(FindAllMoves(otherPlayer))

        score = ScoreFunction(player, otherPlayer, move)

        board = oldBoard

        # We'll work this out next.

        if score > bestScore:
            bestScore = score
            bestMove = move

    PlaceDuck(bestMove[0], bestMove[1], bestMove[2], player)

    return True

def HumanMove(player):

    moves = FindAllMoves(player)

    if len(moves) == 0:
        return False

    print()
    print("========================")
    print("Available moves")
    print("========================")

    for i, move in enumerate(moves):
        print(f"{i:2}: x={move[0]}  y={move[1]}  orientation={move[2]}")

    while True:

        try:

            choice = int(input("\nChoose move number: "))

            if 0 <= choice < len(moves):

                move = moves[choice]

                PlaceDuck(move[0], move[1], move[2], player)

                return True

            print("Please enter one of the move numbers shown.")

        except ValueError:

            print("Please enter a number.")

def AI(player):

    if selectedAI==0:
        return GreedyMove(player,Gary)

    elif selectedAI==1:
        return GreedyMove(player,Velma)

    elif selectedAI==2:
        return GreedyMove(player,Terrance)

    elif selectedAI==3:
        return GreedyMove(player,Octavia)

    elif selectedAI==4:
        return GreedyMove(player,Cuthbert)

    elif selectedAI==5:
        return GreedyMove(player,Barry)

    elif selectedAI==6:
        return BartholomewMove(player)
    
ResetBoard()


# player = 1
#
# while True:
#
#     print()
#     PrintBoard()
#     print()
#
#     if player == 1:
#
#         print("YOUR TURN")
#
#         success = HumanMove(player)
#
#     else:
#
#         print("AI THINKING...")
#
#         success = AI(player)
#
#     if success == False:
#
#         print()
#
#         if player == 1:
#             print("You have no legal moves.")
#             print("AI wins!")
#         else:
#             print("AI has no legal moves.")
#             print("You win!")
#
#         break
#
#     player = 2 if player == 1 else 1
#
# print()
# PrintBoard()