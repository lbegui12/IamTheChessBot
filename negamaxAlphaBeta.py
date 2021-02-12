pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]



class Player:
    def __init__(self, name, depth, book_path = "./book/bookfish.bin"):
        self.name = name
        self.next_move = None
        self.depth = depth
        self.piece_square_tables = [pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]
        self.pieces_values = [100,320,330,500,900]
        self.book_path = book_path
        
    
    def findBestMove(self, board):
        self.next_move = chess.Move.null()
        try:
            self.next_move = chess.polyglot.MemoryMappedReader(self.book_path).weighted_choice(board).move
        except:            
            validMoves = list(board.legal_moves)
            random.shuffle(validMoves)
            self.findMoveNegaMaxAlphaBeta(board, validMoves, self.depth, -CHECKMATE, CHECKMATE, 1 if board.turn == chess.WHITE else -1) 
        return self.next_move
    
    
    def findMoveNegaMax(self, board, validMoves, depth, turnMultiplier):
        if depth==0:
            return turnMultiplier * self.scoreBoard(board)
        
        maxScore = -CHECKMATE
        for move in validMoves:
            board.push(move)
            nextMoves = board.legal_moves
            score = -self.findMoveNegaMax(board, nextMoves, depth-1, -turnMultiplier)
            if score>maxScore:
                maxScore=score
                if depth==self.depth:
                    self.next_move = move
            board.pop()
        return maxScore
        
    
    
    def findMoveNegaMaxAlphaBeta(self, board, validMoves, depth, alpha, beta, turnMultiplier):
        if depth==0:
            return turnMultiplier * self.scoreBoard(board)
        
        # move_ordering - to implement later (check better moves first ! )
        maxScore = -CHECKMATE
        for move in validMoves:
            board.push(move)
            nextMoves = board.legal_moves
            score = -self.findMoveNegaMaxAlphaBeta(board, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
            if score>maxScore:
                maxScore=score
                if depth==self.depth:
                    self.next_move = move
            board.pop()
            if maxScore>alpha:
                alpha=maxScore
            if alpha >= beta:
                break
        return maxScore
    
    
    '''
    Positive score is good for white, negative is good for black
    '''
    
    def scoreBoard(self, board):
        
        if board.is_checkmate():
            if board.turn == chess.WHITE:    
                return -CHECKMATE       # black wins
            else:
                return CHECKMATE        # white wins
        elif board.is_stalemate():
            return SLATEMATE
        
        score = 0
        
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))
        
        material = (self.pieces_values[0]*(wp-bp)
                   + self.pieces_values[1]*(wn-bn)
                   + self.pieces_values[2]*(wb-bb)
                   + self.pieces_values[3]*(wr-br)
                   + self.pieces_values[4]*(wq-bq))
        
        pst = self.piece_square_tables
        pawnsq = sum([pst[0][i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-pst[0][chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([pst[1][i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-pst[1][chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([pst[2][i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-pst[2][chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([pst[3][i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-pst[3][chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([pst[4][i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-pst[4][chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([pst[5][i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-pst[5][chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
        
        score = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        
        return score
            



import random 

import chess 
import chess.pgn
import datetime



CHECKMATE = 99999
SLATEMATE = 0

if __name__ == "__main__":
    
    player1 = Player("NumeroUno", 3)
    player2 = Player("Toto", 1)
    
    game = chess.pgn.Game()
    game.headers["Event"] = "Example"
    game.headers["Site"] = "Linz"
    game.headers["Date"] = str(datetime.datetime.now().date())
    game.headers["Round"] = 1
    game.headers["White"] = player1.name
    game.headers["Black"] = player2.name
    board = chess.Board()
    
    #boardvalue = 0
    
    coup = 1
    
    while not board.is_game_over():
        if board.turn:
            move = player1.findBestMove(board)
            if move != None:
                board.push(move)
            else:
                print("GameOver")
                break
            print("{}. {}".format(coup,move))
            
        else:
            move = player2.findBestMove(board)
            if move != None:
                board.push(move)
            else:
                print("GameOver")
                break
            print("{}... {}".format(coup,move))
            coup+=1
            
    game.headers["Result"] = str(board.result(claim_draw=True))
    print(game)
    
