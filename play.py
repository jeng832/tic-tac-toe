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
    if(p == 1):
        return 2
    else:
        return 1

def human_play(h,g):
    h_before_board = copy_matrix(game.get_board(), 3)
    while True:
        g.print_board()
        print("Select grid (0~8)?")
        grid = input()
        g.action(h, grid)
        h_after_board = copy_matrix(game.get_board(), 3)
        if(np.array_equal(h_before_board, h_after_board) != True):
            break

def com_play(g, p):
    c_before_board = copy_matrix(g.get_board(), 3)
    while True:
        g.print_board()
        p.run()
        c_after_board = copy_matrix(g.get_board(), 3)
        if(np.array_equal(c_before_board, c_after_board) != True):
            break


    

game = Game()
game.reset()

print("player 1 or 2?")
human = input()
com = opposite(human)
p = Player(com, game, 0.8, 0.9)


if(human == 1):
    while True:
        human_play(human, game)
        if(game.is_done()):
            print("Game Over")
            break
        com_play(game, p)
        if(game.is_done()):
            print("Game Over")
            break

else:
    while True:
        com_play(game, p)
        if(game.is_done()):
            print("Game Over")
            break
        human_play(human, game)
        if(game.is_done()):
            print("Game Over")
            break
game.print_board()

