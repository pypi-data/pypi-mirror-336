import os
import mmap
import struct
import random
import torch
import chess

PACKED_SFEN_VALUE_BYTES = 40
INPUTS = (64 * 10 + 1) * 64  

HUFFMAN_MAP = {
    0b000: chess.PAWN,
    0b001: chess.KNIGHT,
    0b010: chess.BISHOP,
    0b011: chess.ROOK,
    0b100: chess.QUEEN
}

def twos(v, w):
    return v - int((v << 1) & 2**w)

class BitReader:
    def __init__(self, bytes_data, at):
        self.bytes = bytes_data
        self.seek(at)

    def readBits(self, n):
        r = self.bits & ((1 << n) - 1)
        self.bits >>= n
        self.position -= n
        return r

    def refill(self):
        while self.position <= 24:
            self.bits |= self.bytes[self.at] << self.position
            self.position += 8
            self.at += 1

    def seek(self, at):
        self.at = at
        self.bits = 0
        self.position = 0
        self.refill()

class ToTensor(object):
    def __call__(self, sample):
        bd, _, outcome, score = sample
        us = torch.tensor([bd.turn])
        them = torch.tensor([not bd.turn])
        outcome = torch.tensor([outcome])
        score = torch.tensor([score])
        from .nnue import get_halfkp_indices
        white, black = get_halfkp_indices(bd)
        return us.float(), them.float(), white.float(), black.float(), outcome.float(), score.float()

class RandomFlip(object):
    def __call__(self, sample):
        bd, move, outcome, score = sample
        mirror = random.choice([False, True])
        if mirror:
            bd = bd.mirror()
        return bd, move, outcome, score

class NNUEBinData(torch.utils.data.Dataset):
    def __init__(self, filename, transform=ToTensor()):
        super(NNUEBinData, self).__init__()
        self.filename = filename
        self.len = os.path.getsize(filename) // PACKED_SFEN_VALUE_BYTES
        self.transform = transform
        self.file = None

    def __len__(self):
        return self.len

    def get_raw(self, idx):
        if self.file is None:
            self.file = open(self.filename, 'r+b')
            self.bytes = mmap.mmap(self.file.fileno(), 0)

        base = PACKED_SFEN_VALUE_BYTES * idx
        br = BitReader(self.bytes, base)

        bd = chess.Board(fen=None)
        bd.turn = not br.readBits(1)
        white_king_sq = br.readBits(6)
        black_king_sq = br.readBits(6)
        bd.set_piece_at(white_king_sq, chess.Piece(chess.KING, chess.WHITE))
        bd.set_piece_at(black_king_sq, chess.Piece(chess.KING, chess.BLACK))
        assert(black_king_sq != white_king_sq)

        for rank_ in range(8)[::-1]:
            br.refill()
            for file_ in range(8):
                i = chess.square(file_, rank_)
                if white_king_sq == i or black_king_sq == i:
                    continue
                if br.readBits(1):
                    piece_index = br.readBits(3)
                    piece = HUFFMAN_MAP[piece_index]
                    color = br.readBits(1)
                    bd.set_piece_at(i, chess.Piece(piece, not color))
                    br.refill()

        br.seek(base + 32)
        score = twos(br.readBits(16), 16)
        move = br.readBits(16)
        to_ = move & 63
        from_ = (move & (63 << 6)) >> 6

        br.refill()
        ply = br.readBits(16)
        bd.fullmove_number = ply // 2

        move = chess.Move(from_square=chess.SQUARES[from_], to_square=chess.SQUARES[to_])
        game_result = br.readBits(8)
        outcome = {1: 1.0, 0: 0.5, 255: 0.0}[game_result]
        return bd, move, outcome, score

    def __getitem__(self, idx):
        item = self.get_raw(idx)
        return self.transform(item)

    def __getstate__(self):
        state = self.__dict__.copy()
        state['file'] = None
        state.pop('bytes', None)
        return state
