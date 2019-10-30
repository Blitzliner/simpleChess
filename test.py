# -*- coding: utf-8 -*-
import unittest
from board import Board, chess

class TestChess(unittest.TestCase):
    def test_initial_pawn_moves(self):
        board = Board()
        board.init()
        pawn = board.figures[chess.A2]
        assert chess.A3 in pawn.moves(board, chess.A2), "A3 not in moves"
        assert chess.A4 in pawn.moves(board, chess.A2), "A4 not in moves" 
        assert len(pawn.moves(board, chess.A2)) == 2, "Too many pawn moves" 
    
    def test_initial_knight_moves(self):
        board = Board()
        board.init()
        pawn = board.figures[chess.B1]
        assert chess.A3 in pawn.moves(board, chess.B1), "A3 not in moves"
        assert chess.C3 in pawn.moves(board, chess.B1), "C3 not in moves" 
        assert len(pawn.moves(board, chess.B1)) == 2, "Too many knight moves" 
    
    def test_init_fen(self):
        board = Board()
        #board.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        board.parse_fen("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
        print(board)
    
if __name__ == '__main__':
    unittest.main()