import numpy as np

class UnactableException(Exception):
    pass

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros([3, 3])
        self.done = False

    def actable(self, p, a):
        if(self.board[a / 3][a % 3] == 0):
            return True
        return False
        
    def action(self, p, a):
        if(self.board[a / 3][a % 3] == 0):
            self.board[a / 3][a % 3] = p
        return self.board

    def opposite(self, p):
        if(p == 1):
            return 2
        if(p == 2):
            return 1

    def judge(self, p):
        if(self.judge_win(p)):
            return 1
        if(self.judge_win(self.opposite(p))):
            return -1
        return 0

    def judge_win(self, p):
        for i in range(3):
            if((self.board[i][0] == p) and (self.board[i][0] == self.board[i][1]) and (self.board[i][1] == self.board[i][2])):
                return True
        for i in range(3):
            if((self.board[0][i] == p) and (self.board[0][i] == self.board[1][i]) and (self.board[1][i] == self.board[2][i])):
                return True
        if((self.board[0][0] == p) and (self.board[0][0] == self.board[1][1]) and (self.board[1][1] == self.board[2][2])):
            return True
        if((self.board[0][2] == p) and (self.board[0][2] == self.board[1][1]) and (self.board[1][1] == self.board[2][0])):
            return True
        return False

    def judge_draw(self):
        if(self.is_done()):
            if((self.judge_win(1) == False) and (self.judge_win(2) == False)):
                return True
        return False 

    def is_done(self):
        if(self.judge_win(1) or self.judge_win(2)):
            return True
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] == 0):
                    return False
        return True


    def print_board(self):
        print("=============")
        print("= {} = {} = {} =".format(self.player(self.board[0][0]), self.player(self.board[0][1]), self.player(self.board[0][2])))
        print("=============")
        print("= {} = {} = {} =".format(self.player(self.board[1][0]), self.player(self.board[1][1]), self.player(self.board[1][2])))
        print("=============")
        print("= {} = {} = {} =".format(self.player(self.board[2][0]), self.player(self.board[2][1]), self.player(self.board[2][2])))
        print("=============")

    def print_small_board(self):
        print("{}{}{}".format(self.player(self.board[0][0]), self.player(self.board[0][1]), self.player(self.board[0][2])))
        print("{}{}{}".format(self.player(self.board[1][0]), self.player(self.board[1][1]), self.player(self.board[1][2])))
        print("{}{}{}".format(self.player(self.board[2][0]), self.player(self.board[2][1]), self.player(self.board[2][2])))

    def player(self, p):
        if(p == 0):
            return " "
        elif(p == 1):
            return "o"
        elif(p == 2):
            return "x"


    def get_board(self):
        return self.board

