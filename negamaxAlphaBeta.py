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
    def __init__(self, name, depth):
        self.name = name
        self.next_move = None
        self.depth = depth
        self.pst = [pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]
        self.pieces_values = [100,320,330,500,900]
        
    
    def findBestMove(self, board):
        global nextMove
        nextMove = chess.Move.null()
        validMoves = list(board.legal_moves)
        #print(validMoves)
        random.shuffle(validMoves)
        #print(validMoves)
        self.findMoveNegaMaxAlphaBeta(board, validMoves, self.depth, -CHECKMATE, CHECKMATE, 1 if board.turn == chess.WHITE else -1) 
        return nextMove
    
    
    
    
    def findMoveNegaMaxAlphaBeta(self, board, validMoves, depth, alpha, beta, turnMultiplier):
        global nextMove
        if depth==0:
            return turnMultiplier * self.scoreBoard(board)
        
        # move_ordering - implement later 
        maxScore = -CHECKMATE
        for move in validMoves:
            board.push(move)
            nextMoves = board.legal_moves
            score = -self.findMoveNegaMaxAlphaBeta(board, nextMoves, depth-1, -beta, -alpha, -1*turnMultiplier)
            if score>maxScore:
                maxScore=score
                if depth==self.depth:
                    nextMove=move
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
            #print("CHEKCMATE")
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
        
        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
        
        pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
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
    
    player1 = Player("NumeroUno", 4)
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
    
