# Dimension of Board #
SIZE = 3

# Board Symbols #
NA = "?"
Xs = "X"
Os = "O"

# Utilities for Minimax Algorithm #
POSITIVE_INFINITY = 1e500
NEGATIVE_INFINITY = -1e500

def generateKey (i, j):
  
  return str(i) + "," + str(j)
  
def showBoard (board):

  printable = ""

  for i in range (SIZE):
    for j in range (SIZE):
      
      key = generateKey(i, j)
      printable += " " + board[key] + " "
    
      if (j < (SIZE - 1)):
        printable += "|"
    
    if (i < (SIZE - 1)):
      printable += "\n---|---|---\n"

  print ("\nBoard:\n\n" + printable + "\n")
def setBoard ():
  
  board = {}
  
  for i in range (SIZE):
    for j in range (SIZE):
      
      key = generateKey(i, j)
      board[key] = NA
      
  return board
  
def winningConditions ():
  
  conditions = []
  
  """
    The game of tic-tac-toe is won, when a player procures all of the squares in:
      - Any of the rows, OR
      - Any of the columns, OR
      - The left diagonal, OR
      - The right diagonal.
  """
  
  lDiag = []
  rDiag = []
  
  for i in range(SIZE):
    
    row = []
    col = []
    
    lDiag.append(generateKey(i, i))
    rDiag.append(generateKey(i, (SIZE - (i + 1))))
    
    for j in range(SIZE):
      
      row.append(generateKey(i, j))
      col.append(generateKey(j, i))
    
    conditions.append(row)
    conditions.append(col)
  
  conditions.append(lDiag)
  conditions.append(rDiag)
  
  return conditions
def wonBy (board, symbol):
  
  WINNING_CONDITIONS = winningConditions()
  
  for winningCondition in WINNING_CONDITIONS:
    
    won = True
    for square in winningCondition:
        
      if (board[square] != symbol):
        won = False
        break
        
    if (won):
      return True
          
  return False
  
def availableMoves (board):
  
  moves = []
  
  for i in range(SIZE):
    for j in range(SIZE):
      
      key = generateKey(i, j)
      if (board[key] == NA):
        moves.append(key)
  
  return moves
def minimax (board, maximize, alpha, beta, player, computer):
  
  moves = availableMoves(board)
  
  if (wonBy(board, computer)):
    return {
      'mv': 1,
      'mb': board
    }
  elif (wonBy(board, player)):
    return {
      'mv': -1,
      'mb': board
    }
  elif (len(moves) == 0):
    return {
      'mv': 0,
      'mb': board
    }
  
  if (maximize):
    
    maxValue = NEGATIVE_INFINITY
    maximizedBoard = None
    
    for move in moves:
      
      next = dict.copy(board)
      next[move] = computer
      
      maxi = minimax (next, False, alpha, beta, player, computer)
      
      if (maxi['mv'] > maxValue):
        maxValue = maxi['mv']
        maximizedBoard = next
      
      alpha = max(alpha, maxValue)
      if beta <= alpha:
        break
      
    return {
      'mv': maxValue,
      'mb': maximizedBoard
    }
  else:
    
    minValue = POSITIVE_INFINITY
    minimizedBoard = None
    
    for move in moves:
      
      next = dict.copy(board)
      next[move] = player
      
      mini = minimax (next, True, alpha, beta, player, computer)
      
      if (mini['mv'] < minValue):
        minValue = mini['mv']
        minimizedBoard = next
        
      beta = min( beta, minValue)
      if beta <= alpha:
        break
    
    return {
      'mv': minValue,
      'mb': minimizedBoard
    }
def playersMove (board, player):
  
  validInput = False
  statement = ""
  
  while not(validInput):
    
    statement = input("\nPlayer's Move: ")
  
    if (statement in board.keys() and board[statement] == NA):
      validInput = True
      
    else:
      print("\nInvalid input; please try again.\nReminder: enter an input in the form of 'row,column' (in base 0)\n")
  
  board[statement] = player

  return board
    
def ticTacToe (board, player, computer):
  
  WIN_CONDITIONS = winningConditions()
  MAX_TURNS = SIZE * SIZE

  showBoard(board)

  turn = 0
  order = [Xs, Os]

  while (turn < MAX_TURNS):
    
    print("Turn #", (turn + 1))
    
    if (order[turn % 2] == player):
      
      board = playersMove(board, player)
      showBoard(board)
      
      if (wonBy(board, player)):
        print("Victory.")
        return +1
      
    else:
      
      board = minimax(board, True, NEGATIVE_INFINITY, POSITIVE_INFINITY, player, computer)['mb']
      showBoard(board)
    
      if (wonBy(board, computer)):
        print("Defeat.")
        return -1
    
    turn += 1
  
  print("Draw.")
  return 0
  
def main ():

  print ("Tic-Tac-Toe")
  
  score = 0
  terminate = False
  while not(terminate):
    
    board = setBoard()
    player = None
    computer = None
    
    validInput = False
    while not(validInput):
      
      symbol = input("\nXs or Os? ")
      
      if (symbol == "Xs"):
        player = Xs
        computer = Os
        validInput = True
      elif (symbol == "Os"):
        player = Os
        computer = Xs
        validInput = True
      else:
        print("\nInvalid input. Reminder: enter either 'Xs' or 'Ys'.")
        
    score += ticTacToe(board, player, computer)
    
    validInput = False
    while not(validInput):
      
      again = input("\nPlay Again (Y or N)? ")
      
      if (again == "Y"):
        validInput = True
      elif (again == "N"):
        print("\nFinal score:", score)
        return
      else:
        print("\nInvalid input. Reminder: enter either 'Y' or 'N'.")
    
if (__name__ == "__main__"):
  main()