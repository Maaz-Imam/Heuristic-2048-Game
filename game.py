import random
import os
import msvcrt
import copy

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.grid[random.randint(0, size - 1)][random.randint(0, size - 1)] = 2

        self.grid2 = copy.deepcopy(self.grid)
        self.next_score = {'w':0,'s':0,'a':0,'d':0}
        self.flag = 0
        self.score = 0

    def __str__(self):
        return '\n'.join(['\t|\t'.join([str(cell) for cell in row]) for row in self.grid])

    def is_safe(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == 0
    
    def is_full(self):
        return all([cell != 0 for row in self.grid for cell in row])
    
    def no_moves(self):
        if self.next_move_predictor()[1] == 0:
            return True 
    
    def next_move_predictor(self):
        self.next_score = {'w':0,'s':0,'a':0,'d':0}
        # print('Copying for w')
        self.grid2 = copy.deepcopy(self.grid)
        # Move Up
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
                    # self.grid[i][j] = 0
                    self.next_score['w'] =  max(self.next_score['w'],0) # adding to next score
                    # print('Scoring for w: ',self.next_score['w'])
                else:
                    self.grid2[x - 1][j] *= 2
                    self.next_score['w'] = max(self.next_score['w'],self.grid2[x - 1][j]) # adding to next score
                    # print('Scoring for w: ',self.grid2[x - 1][j])
                    self.grid2[i][j] = 0
        

        # print('Copying for s')
        self.grid2 = copy.deepcopy(self.grid)
        # Move Down
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
                    # print('Scoring for s: ',self.next_score['s'])
                else:
                    self.grid2[x + 1][j] *= 2
                    self.next_score['s'] =  max(self.next_score['s'],self.grid2[x + 1][j]) # adding to next score
                    # print('Scoring for s: ',self.grid2[x + 1][j])
                    self.grid2[i][j] = 0
            

        # print('Copying for a')    
        self.grid2 = copy.deepcopy(self.grid)
        # Move Left
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
                    # print('Scoring for a: ',self.next_score['a'])
                else:
                    self.grid2[i][x - 1] *= 2
                    self.next_score['a'] =  max(self.next_score['a'],self.grid2[i][x - 1]) # adding to next score
                    # print('Scoring for a: ',self.grid2[i][x - 1])
                    self.grid2[i][j] = 0
    

        # print('Copying for d')
        self.grid2 = copy.deepcopy(self.grid)
        # Move Right
        for j in range(self.size):
            for i in range(self.size - 1, -1, -1):
                if self.grid2[i][j] == 0:
                    continue
                x = j
                while x < self.size - 1 and self.grid2[i][x + 1] == 0:
                    x += 1
                # print(i, x)
                if x == self.size - 1 or (self.grid2[i][x + 1] != self.grid2[i][j]):
                    self.grid2[i][x] = self.grid2[i][j]
                    if x != j:
                        self.grid2[i][j] = 0
                    self.next_score['d'] =  max(self.next_score['d'],0) # adding to next score
                    # print('Scoring for d: ',self.next_score['d'])
                else:
                    self.grid2[i][x + 1] *= 2
                    self.next_score['d'] =  max(self.next_score['d'],self.grid2[i][x + 1]) # adding to next score
                    # print('Scoring for d: ',self.grid2[i][x + 1])
                    self.grid2[i][j] = 0

        print("Final predictions: ",self.next_score)
        return max(self.next_score.items(), key=lambda x: x[1])

    
    def generate_new_cell(self):
        x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        while not self.is_safe(x, y):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self.grid[x][y] = 2 if random.random() < 0.9 else 4
    
    def run(self):
        while True:
            os.system("cls")
            if self.is_full():
                print("\nTOTAL SCORE: ",self.score,"\n")
                print(self)
                if self.flag and self.no_moves():
                    print("\n\nX---X---X  GAME OVER  X---X---X\n\n")
                    break
                os.system("cls")

            
            print("\nTOTAL SCORE: ",self.score,"\n")
            print(self)

            best_move = ''
            
            if self.flag == 1:
                print('\n\nGoing to predict next move')
                best_move, best_score = self.next_move_predictor()

                print("Next move should be: ",best_move,"\nWith a score of: ",best_score)
            self.flag = 1

            print("\n\nEnter direction: ")
            direction = best_move
            print(direction)

            if direction == "w":
                self.move_up()
            elif direction == "s":
                self.move_down()
            elif direction == "a":
                self.move_left()
            elif direction == "d":
                self.move_right()
            self.generate_new_cell()
    
    def move_up(self):
        for j in range(self.size):
            for i in range(1, self.size):
                if self.grid[i][j] == 0:
                    continue
                x = i
                while x > 0 and self.grid[x - 1][j] == 0:
                    x -= 1
                if x == 0 or (self.grid[x - 1][j] != self.grid[i][j]):
                    self.grid[x][j] = self.grid[i][j]
                    if x != i:
                        self.grid[i][j] = 0
                    # self.grid[i][j] = 0
                else:
                    self.grid[x - 1][j] *= 2
                    self.score += self.grid[x - 1][j] # adding to total score
                    self.grid[i][j] = 0
                    
    def move_down(self):
        for j in range(self.size):
            for i in range(self.size - 2, -1, -1):
                if self.grid[i][j] == 0:
                    continue
                x = i
                while x < self.size - 1 and self.grid[x + 1][j] == 0:
                    x += 1
                if x == self.size - 1 or (self.grid[x + 1][j] != self.grid[i][j]):
                    self.grid[x][j] = self.grid[i][j]
                    if x != i:
                        self.grid[i][j] = 0
                else:
                    self.grid[x + 1][j] *= 2
                    self.score += self.grid[x + 1][j] # adding to total score
                    self.grid[i][j] = 0
            
    def move_left(self):
        for j in range(self.size):
            for i in range(self.size):
                if self.grid[i][j] == 0:
                    continue
                x = j
                while x > 0 and self.grid[i][x - 1] == 0:
                    x -= 1
                if x == 0 or (self.grid[i][x - 1] != self.grid[i][j]):
                    self.grid[i][x] = self.grid[i][j]
                    if x != j:
                        self.grid[i][j] = 0
                else:
                    self.grid[i][x - 1] *= 2
                    self.score += self.grid[i][x - 1] # adding to total score
                    self.grid[i][j] = 0
    
    def move_right(self):
        for j in range(self.size):
            for i in range(self.size - 1, -1, -1):
                if self.grid[i][j] == 0:
                    continue
                x = j
                while x < self.size - 1 and self.grid[i][x + 1] == 0:
                    x += 1
                # print(i, x)
                    
                if x == self.size - 1 or (self.grid[i][x + 1] != self.grid[i][j]):
                    self.grid[i][x] = self.grid[i][j]
                    if x != j:
                        self.grid[i][j] = 0
                else:
                    self.grid[i][x + 1] *= 2
                    self.score += self.grid[i][x + 1] # adding to total score
                    self.grid[i][j] = 0
            

if __name__ == "__main__":
    grid = Grid(4)
    grid.run()