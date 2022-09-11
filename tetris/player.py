from time import sleep

from board import Direction, Rotation, Action
from random import Random


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class ZaksPlayer(Player):
    def __init__(self):
        pass

    def print_board(self, board):
        print("----------")
        for y in range(24):
            s = ""
            for x in range(10):
                if board.falling is not None and (x, y) in board.falling.cells:
                    s = s + "*"
                elif (x, y) in board.cells:
                    s = s + "#"
                else:
                    s = s + "."
            print(s, y)

    def landed(self, board):
        if board.falling is not None:
            return False
        return True

    def height(self, board):
        heights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for x in range(0, 10):
            for y in range(0, 24):
                if (x, y) in board.cells:
                    heights[x] = y
                    break
        return heights

    def num_holes(self, board):
        columnheight = self.height(board)
        holes = 0
        for x in range(0, 10):
            for y in range(columnheight[x], 24):
                if (x, y) not in board.cells:
                    holes += 1
        print("holes:", holes)
        return holes

    def discards(self, board, sandbox):
        # print("dis: ", board.discards_remaining)
        if self.num_holes(sandbox) > self.num_holes(board):
            if board.discards_remaining > 0:
                board.discards_remaining -= 1
                return ("Discard")

    def agg_height(self, board):
        aggregate = 0
        for x in range(0, 10):
            height = 0
            for y in range(0, 24):
                if (x, y) in board.cells:
                    height = 24 - y
                    break
            aggregate = aggregate + height
        return aggregate

    def filled_lines(self, board, sandbox):
        boardblocks = 0
        sandboxblocks = 0
        for y in range(0, 24):
            for x in range(0, 10):
                if sandbox.cells is not None and (x, y) in board.cells:
                    boardblocks += 1
        for y in range(0, 24):
            for x in range(0, 10):
                if sandbox.cells is not None and (x, y) in sandbox.cells:
                    sandboxblocks += 1
        filled = (boardblocks + 4 - sandboxblocks) // 10
        if filled < 0:
            filled = 0
        return filled

    def bumpiness(self, board):
        columnheights = self.height(board)
        bumps = 0
        for x in range(0, 9):
            if columnheights[x] > columnheights[x + 1]:
                bumps = bumps + columnheights[x] - columnheights[x + 1]
            elif columnheights[x] < columnheights[x + 1]:
                bumps = bumps + columnheights[x + 1] - columnheights[x]
        return bumps

    def minimumHeight(self, sandbox):
        miny = 24
        columnheight = self.height(sandbox)
        for x in range(0,10):
            if columnheight[x] < miny:
                miny = columnheight[x]
        return miny

    def score_board(self, board, sandbox):
        aggheight = self.agg_height(sandbox)
        holes = self.num_holes(sandbox)

        filledrows = self.filled_lines(board, sandbox)
        bumpiness = self.bumpiness(sandbox)
        miny = self.minimumHeight(sandbox)
        a = -0.2
        b = -0.5
        c = -1.2
        d = -0.3
        e = -0.1
        if filledrows == 1:
            b = -3
        elif filledrows == 2:
            b = 1.5
        elif filledrows == 3:
            b = 4
        elif filledrows == 4:
            b = 6
        if miny <= 12:
            b = 0
            c = -1.5
            d = -0.4
            e = -0.01
        score = (a * aggheight) + (b * filledrows) + (c * holes) + (d * bumpiness) + (e * miny)
        return score

    def choose_action(self, board):

        # for othercol in range(0, 10):
        #     for otherrot in range(0, maxrot):
        #         othermoves = []
        #         landed = False
        #         newsandbox = sandbox.clone()
        #         xpos = newsandbox.falling.left
        #         shape = str(newsandbox.falling.shape)[6]
        #         if shape == "I":
        #             maxrot = 2
        #         elif shape == "J":
        #             maxrot = 4
        #         elif shape == "L":
        #             maxrot = 4
        #         elif shape == "0":
        #             maxrot = 0
        #         elif shape == "S":
        #             maxrot = 2
        #         elif shape == "T":
        #             maxrot = 4
        #         elif shape == "Z":
        #             maxrot = 2
        #         elif shape == "B":
        #             maxrot = 0
        #         for otherrotations in range(0, otherrot):
        #             if not landed:
        #                 landed = newsandbox.rotate(Rotation.Anticlockwise)
        #                 othermoves.append(Rotation.Anticlockwise)
        #                 if not landed:
        #                     xpos = newsandbox.falling.left
        #                 else:
        #                     break
        #             else:
        #                 break
        #         while xpos > othercol and not landed:
        #             landed = newsandbox.move(Direction.Left)
        #             othermoves.append(Direction.Left)
        #             if not landed:
        #                 xpos -= 1
        #         while xpos < othercol and not landed:
        #             landed = newsandbox.move(Direction.Right)
        #             othermoves.append(Direction.Right)
        #             if not landed:
        #                 xpos += 1
        #         if not landed:
        #             newsandbox.move(Direction.Drop)
        #             othermoves.append(Direction.Drop)
        #         score = self.score_board(board, newsandbox)
        #         if self.filled_lines(sandbox, newsandbox, 8) == 4:
        #             moves.append(othermoves)
        #             return moves
        #         print("score", score)

        bestmove = []
        bestscore = -100000
        minholes = 240
        for columns in range(0, 10):
            for targetrot in range(0, 4):
                moves = []
                landed = False
                sandbox = board.clone()
                xpos = sandbox.falling.left
                for rotations in range(0, targetrot):
                    if not self.landed(sandbox):
                        landed = sandbox.rotate(Rotation.Anticlockwise)
                        moves.append(Rotation.Anticlockwise)
                        if not landed:
                            xpos = sandbox.falling.left
                        else:
                            break
                    else:
                        break
                # print("width: ", width)
                # print("R: ", sandbox.falling.right)
                # print("L: ", sandbox.falling.left)
                while xpos > columns and not landed:
                    landed = sandbox.move(Direction.Left)
                    moves.append(Direction.Left)
                    if not landed:
                        xpos -= 1
                while xpos < columns and not landed:
                    landed = sandbox.move(Direction.Right)
                    moves.append(Direction.Right)
                    if not landed:
                        xpos += 1
                if not landed:
                    sandbox.move(Direction.Drop)
                    moves.append(Direction.Drop)
                if self.discards(board, sandbox) == "Discard":
                    bestmove.append(Action.Discard)
                # elif self.discards(board, sandbox) == "Bomb":
                # bestmove.append(Action.Bomb)
                else:
                    score = self.score_board(board, sandbox)
                    if score > bestscore:
                        bestscore = score
                        bestmove = moves
                self.print_board(sandbox)
            # assert(False)
        return bestmove

SelectedPlayer = ZaksPlayer
