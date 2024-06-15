"""
This is responsible for storing the current state/scene of the chess game. Check Valid move and maitain a Move Log.
"""
class GameState():


    def __init__(self):
        # board is a 8x8 2 dimensional list. Eaxh element of the list has 2 character.
        # 1st character represents the color of the piece. 2nd character represent the tyoe of the piece.
        # "--" this represents empty space on the board with no piece.
        self.board =[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False



    '''
    takes a move as a parameter and executes it.
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Know the history of the move.
        self.whiteToMove = not self.whiteToMove #Swap Players
        #update kings location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
    '''
    Undo the last move made.
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure that there is a move to undo.
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Swap Players
            #update kings posion when moved and needed.
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    """
    -make the move
    -generate all possible moves for the opposing player
    -see if any of the moves attack your king
    -if your king is safe, it is a valid move and add it to a 1ist
    -return the list of valid moves only
    """
    '''
    all moves considering checks
    '''
    def getValidMoves(self):
        #1. Generate all possible moves.
        moves = self.getAllPossibleMoves()
        #2. for each move, make the move.
        for i in range(len(moves)-1, -1, -1): #When removing from a list go backwards because when the index changes, it doesn't affect the next in line.
            self.makeMove(moves[i])
            #3. Generate all opponent's moves.
            #4. for each of your oponent's moves, see if they are attacking the king.
            self.whiteToMove = not self.whiteToMove #
            if self.inCheck():
                moves.remove(moves[i]) #5. if they do attack the king, it's not a valid move.
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0: #either checkmate or stalemate.
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    '''
    determine if the current player is in check.
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    determine if the enemy can attack the square r, c.
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn.
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back

        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is underattack.
                return True
            return False

    '''
    all moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #No. of rows
            for c in range(len(self.board[r])): #No. of coloums.
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #Calls the appropriate move functions based on piece functions

        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": #1 Square pawn advance move check.
                moves.append(Move((r,c),(r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 Square pawn advance move check.
                    moves.append(Move((r,c),(r-2,c), self.board))

            if c-1 >= 0: #Captures to the left.
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture.
                    moves.append(Move((r, c),(r-1, c-1), self.board))
            if c+1 <= 7: #Captures to the right.
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture.
                    moves.append(Move((r, c),(r-1, c+1), self.board))

        else: #Black Pawn Movement
            if self.board[r + 1][c] == "--": #1 Square pawn advance move check.
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 Square pawn advance move check.
                    moves.append(Move((r,c), (r+2,c), self.board))

            if c-1 >= 0: #Captures to the left.
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture.
                    moves.append(Move((r, c),(r+1, c-1), self.board))
            if c+1 <= 7: #Captures to the right.
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture.
                    moves.append(Move((r, c),(r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on boand
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty Space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) #Combination of ()+-2,+-1)
        allycolor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor: #not an ally piece. (enpty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #Diagonal movement
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on boand
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty Space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    overriding the equals method.
    '''
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
