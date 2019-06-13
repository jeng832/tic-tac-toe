import numpy as np
from player import Player
from game import Game

def copy_matrix(origin, di):
    mat = np.zeros([di, di])
    for i in range(di):
        for j in range(di):
            mat[j][i] = origin[j][i]
    return mat

def opposite(p):
    if(p == 0):
        return 1
    else:
        return 0

game = Game()
for ep in range(10):
    p = []
    game.reset()
    p.append(Player(1, game, 0.8, 0.9))
    p.append(Player(2, game, 0.8, 0.9))

    i = 1
    #game.print_board()

    while True:
        before_board = copy_matrix(game.get_board(), 3)
        #after_board = copy_matrix(before_board, 3)
        i = opposite(i)
        while True:
            p[i].learn()
            after_board = copy_matrix(game.get_board(), 3)
            #print("TURN[{}] >> player {}".format(ep, i + 1))
            if(np.array_equal(before_board, after_board) != True):
                #print("TURN[{}] >> player {}".format(ep, i + 1))
                #game.print_board()
                #raw_input()
                break
        if(game.is_done()):
            p[opposite(i)].apply_negative_reward()
            #print("Game Over")
            break

    print("==== Final ep{} ====".format(ep))
    game.print_small_board()
    if(game.judge(1) == 1):
        print("Player 1(o) win")
    elif(game.judge(1) == -1):
        print("Player 2(x) win")
    else:
        print("Draw")


