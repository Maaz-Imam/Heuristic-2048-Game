import random
import os
import msvcrt
import copy

from grid import Grid

class Solver:
    def __init__(self, size):
        self.size = size
        self.env = Grid(size)
        
    def no_moves(self):
        if self.next_move_predictor()[1] == 0:
            return True 
        
    def next_move_predictor(self):
        self.next_score = {'w':0,'s':0,'a':0,'d':0}
        self.grid2 = copy.deepcopy(self.env.grid)

        for j in range(self.size):
            for i in range(1, self.size):
                if self.grid2[i][j] == 0:
                    continue
                x = i
                while x > 0 and self.grid2[x - 1][j] == 0:
                    x -= 1
                if x == 0 or (self.grid2[x - 1][j] != self.grid2[i][j]):
                    self.grid2[x][j] = self.grid2[i][j]
                    if x != i:
                        self.grid2[i][j] = 0
                    self.next_score['w'] =  max(self.next_score['w'],0) # adding to next score
                else:
                    self.grid2[x - 1][j] *= 2
                    self.next_score['w'] = max(self.next_score['w'],self.grid2[x - 1][j]) # adding to next score
                    self.grid2[i][j] = 0
        

        self.grid2 = copy.deepcopy(self.env.grid)
        for j in range(self.size):
            for i in range(self.size - 2, -1, -1):
                if self.grid2[i][j] == 0:
                    continue
                x = i
                while x < self.size - 1 and self.grid2[x + 1][j] == 0:
                    x += 1
                if x == self.size - 1 or (self.grid2[x + 1][j] != self.grid2[i][j]):
                    self.grid2[x][j] = self.grid2[i][j]
                    if x != i:
                        self.grid2[i][j] = 0
                    self.next_score['s'] =  max(self.next_score['s'],0) # adding to next score
                else:
                    self.grid2[x + 1][j] *= 2
                    self.next_score['s'] =  max(self.next_score['s'],self.grid2[x + 1][j]) # adding to next score
                    self.grid2[i][j] = 0
            

        self.grid2 = copy.deepcopy(self.env.grid)
        for j in range(self.size):
            for i in range(self.size):
                if self.grid2[i][j] == 0:
                    continue
                x = j
                while x > 0 and self.grid2[i][x - 1] == 0:
                    x -= 1
                if x == 0 or (self.grid2[i][x - 1] != self.grid2[i][j]):
                    self.grid2[i][x] = self.grid2[i][j]
                    if x != j:
                        self.grid2[i][j] = 0
                    self.next_score['a'] =  max(self.next_score['a'],0) # adding to next score
                else:
                    self.grid2[i][x - 1] *= 2
                    self.next_score['a'] =  max(self.next_score['a'],self.grid2[i][x - 1]) # adding to next score
                    self.grid2[i][j] = 0
    
        self.grid2 = copy.deepcopy(self.env.grid)
        for j in range(self.size):
            for i in range(self.size - 1, -1, -1):
                if self.grid2[i][j] == 0:
                    continue
                x = j
                while x < self.size - 1 and self.grid2[i][x + 1] == 0:
                    x += 1
                if x == self.size - 1 or (self.grid2[i][x + 1] != self.grid2[i][j]):
                    self.grid2[i][x] = self.grid2[i][j]
                    if x != j:
                        self.grid2[i][j] = 0
                    self.next_score['d'] =  max(self.next_score['d'],0) # adding to next score
                else:
                    self.grid2[i][x + 1] *= 2
                    self.next_score['d'] =  max(self.next_score['d'],self.grid2[i][x + 1]) # adding to next score
                    self.grid2[i][j] = 0

        print("Final predictions: ",self.next_score)
        return max(self.next_score.items(), key=lambda x: x[1])

    
    def run(self):
        while True:
            os.system("cls")
            if self.env.is_full():
                print("\nTOTAL SCORE: ",self.env.score,"\n")
                print(self.env.render())
                if self.env.flag and self.no_moves():
                    print("\n\nX---X---X  GAME OVER  X---X---X\n\n")
                    input()
                    break
                os.system("cls")

            
            print("\nTOTAL SCORE: ",self.env.score,"\n")
            print(self.env.render())

            best_move = ''
            
            if self.env.flag == 1:
                print('\n\nGoing to predict next move')
                best_move, best_score = self.next_move_predictor()

                print("Next move should be: ",best_move,"\nWith a score of: ",best_score)
            self.env.flag = 1

            print("\n\nEnter direction: ")
            direction = best_move
            print(direction)

            if direction == "w":
                self.env.move_up()
            elif direction == "s":
                self.env.move_down()
            elif direction == "a":
                self.env.move_left()
            elif direction == "d":
                self.emv.move_right()
            self.env.generate_new_cell()
    

if __name__ == "__main__":
    size = 4
    solver = Solver(size)
    solver.run()