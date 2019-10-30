# -*- coding: utf-8 -*-
#from figures import Color, Pawn, King, Knight, Bishop, Queen, Rook
#todo:
#move list, return, track moves
#max allowed moves 50 Without Beating or pawn movement
#upgrade pawn to queen/etc
#Stellungswiederholung
#King <-> Rook
#check for each move own king, See king
#Remis unentschieden
#en passant: Schlagen des gegnrischen bauerns unnittelbar nach doppelschritt
#checkmate schach-matt
#check schach
#korrekte notation als dokumentation und input
    
class Chess():
    def __init__(self):
        for i in range(1, 9):
            for j in range(1, 9):
                key = chr(i+64) + str(j)
                self.__dict__[key] = (i, j)
        self.__dict__["WHITE"] = "w"
        self.__dict__["BLACK"] = "b"
        
    def __setattr__(self, attr, value):
        raise NotImplementedError()
    
chess = Chess()
    
class Figure:    
    def __init__(self, color):
        self.color = color
        self.moved = False
        self.unicode = { chess.WHITE : " ", chess.BLACK : " " }
        #self.position
        #todo: self.last_move =""
    
    def __str__(self):
        return self.unicode[self.color]
        
    def add(self, pos, step):
        if self.color is chess.WHITE:
            return (pos[0]+step[0], pos[1]+step[1])
        else:
            return (pos[0]+step[0], pos[1]-step[1])
        
    def occupied(self, board, pos):
        if pos in board.figures:
            if board.figures[pos].color is not self.color:
                return True # position if occupied by the opponent
            else:
                return -1 # position is occupied by same color
        return False # position is not occupied by a figure
    
    def inrange(self, pos):
        if pos[0] in range(1, 9) and pos[1] in range(1, 9):
            return True
        return False
                    
    def check(self, board, position, steplist, iterate=False):
        moves = []
        for step in steplist:
            pos = position
            while True:
                pos = self.add(pos, step)
                if self.inrange(pos) is True and self.occupied(board, pos) != -1:
                    moves.append(pos)
                else:
                    break
                if not iterate:
                    break
        return moves
   
    def moves(self, board, position):
        raise NotImplementedError()
    
class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.unicode = { chess.WHITE : "♙", chess.BLACK : "♟" }
        
    def en_passant(self, board, position):
        if board.en_passant is not None:
            if board.active_color is self.color:
                pos = self.add(position, (1,1))
                if pos is board.en_passant:
                    return pos
                pos = self.add(position, (-1,1))
                if pos is board.en_passant:
                    return pos
        return None
        
    def moves(self, board, position):
        moves = []
        pos = self.add(position, (1, 1))
        if self.inrange(pos) is True and self.occupied(board, pos) is True: moves.append(pos)
        pos = self.add(position, (-1, 1))
        if self.inrange(pos) is True and self.occupied(board, pos) is True: moves.append(pos)
        pos = self.add(position, (0, 1))
        if self.inrange(pos) is True and self.occupied(board, pos) is False: moves.append(pos)
        pos = self.add(position, (0, 2))
        if self.inrange(pos) is True and self.occupied(board, pos) is False and not self.moved: moves.append(pos)
        pos = self.en_passant(board, position)
        if pos is not None:
            moves.append(pos)
        return moves

class King(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.unicode = { chess.WHITE : "♔", chess.BLACK : "♚" }
    def moves(self, board, position):
        steps = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(-1,1))
        return self.check(board, position, steps)
   
class Queen(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.unicode = { chess.WHITE : "♕", chess.BLACK : "♛" }
    def moves(self, board, position):
        steps = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(-1,1))
        return self.check(board, position, steps, True)
    
class Rook(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.unicode = { chess.WHITE : "♖", chess.BLACK : "♜" }
    def moves(self, board, position):
        steps = ((1,0),(0,1),(-1,0),(0,-1))
        return self.check(board, position, steps, True)
    
class Bishop(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.unicode = { chess.WHITE : "♗", chess.BLACK : "♝" }
    def moves(self, board, position):
        steps = ((1,1),(1,-1),(-1,-1),(-1,1))
        return self.check(board, position, steps, True)
    
class Knight(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.unicode = { chess.WHITE : "♘", chess.BLACK : "♞" }
    def moves(self, board, position):
        steps = ((2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1))
        return self.check(board, position, steps)
    
class Board():
    def __init__(self):
        self.figures = {}
        self.moves = []
        self.en_passant_cell = None
        self.active_color = chess.WHITE
        self.castling = "KQkq"
        self.half_move = 0 #number of halfmoves since the last capture or pawn advance
        self.full_move = 1 #starts at 1
        
    def init(self):
        self.figures = {}
        self.moves = []
        self.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        
    #Forsyth–Edwards Notation (FEN)
    def parse_fen(self, dat):
        dat = dat.split()
        if len(dat) != 6:
            raise ValueError("Invalid FEN")
        else:
            self._set_figures(dat[0])
            self.active_color = dat[1]
            self.castling = dat[2]
            self.en_passant = dat[3]
            self.half_move = dat[4]
            self.full_move = dat[5]
        
    def _set_figures(self, dat):
        pos_x = 1
        pos_y = 8
        rows = dat.split('/')
        for row in rows:
            pos_x = 1
            for c in row:
                if c.isdigit() is True:
                    pos_x = pos_x + int(c)
                else:
                    self._add_figure(c, (pos_x, pos_y))
                pos_x = pos_x + 1
            pos_y = pos_y - 1
        
    def _add_figure(self, c_type, pos):
        color = chess.WHITE
        if c_type.islower() is True:
            color = chess.BLACK
        c = c_type.lower()
        if c == 'p': self._add(pos, Pawn(color))
        elif c == 'r': self._add(pos, Rook(color))
        elif c == 'n': self._add(pos, Knight(color))
        elif c == 'b': self._add(pos, Bishop(color))
        elif c == 'q': self._add(pos, Queen(color))
        elif c == 'k': self._add(pos, King(color))
        else: raise ValueError(F"Invalid Argument: {c}")
        
    def _add(self, position, fig):
        self.figures[position] = fig
    
    def do_move(self, move):
        if move[0] in self.figures:
            if move[1] in self.figures[move[0]].moves():
                if move[1] in self.figures:
                    del self.figures[move[1]]
                fig = self.figures[move[0]]
                del self.figures[move[0]]
                self.figures[move[1]] = fig
                self.moves.append(move)
            else:
                raise ValueError("Wrong move: cannot move figure to this position")
        else:
            raise ValueError("Wrong move: starting position not valid")
            
    def __str__(self):
        ret = "  a b c d e f g h\n"
        for j in range(8, 0, -1):
            ret += F"{j}"
            for i in range(8, 0, -1):
                ret += F" {str(self.figures.get((i, j), '.'))}"
            ret += F" {j}\n"
        ret += "  a b c d e f g h "
        return ret
        
    
if __name__ == '__main__':
    
    board = Board()
    board.init()
    
    for pos, fig in board.figures.items():
        #print(F"{fig} {pos}")
        if fig.color is chess.WHITE:
            print(F"{fig}/{pos}: {fig.moves(board, pos)}")
            #print(fig.moves(board, pos))
    print(board)
    
    