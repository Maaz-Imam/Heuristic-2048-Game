import random
import os
import msvcrt
import copy
import pygame as pg

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.grid[random.randint(0, size - 1)][random.randint(0, size - 1)] = 2

        self.grid2 = copy.deepcopy(self.grid)
        self.next_score = {'w':0,'s':0,'a':0,'d':0}
        self.flag = 0
        self.score = 0
        
        pg.init()
        self.myfont = pg.font.SysFont('Arial', 30)
        self.screen = pg.display.set_mode((400, 400))
        pg.display.set_caption("2048")

    def render(self):
        self.screen.fill((255, 255, 255))
        for i in range(self.size):
            for j in range(self.size):
                pg.draw.rect(self.screen, (0, 0, 0), (i * 100, j * 100, 100, 100), 2)
                text = self.myfont.render(str(self.grid[i][j]), False, (0, 0, 0))
                self.screen.blit(text, (i * 100 + 30, j * 100 + 30))
        pg.display.flip()
            
            
        # return '\n'.join(['\t|\t'.join([str(cell) for cell in row]) for row in self.grid])

    def is_safe(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == 0
    
    def is_full(self):
        return all([cell != 0 for row in self.grid for cell in row])
    

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