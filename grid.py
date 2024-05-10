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
        self.myfont = pg.font.SysFont('Arial', 40)
        self.screen_width = 400
        self.screen_height = 400
        self.cell_size = self.screen_width // self.size
        self.padding = 10
        self.colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("2048")

    def render(self):
        self.screen.fill((187, 173, 160))  # Background color
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                color = self.colors.get(value, (255, 255, 255))  # Default to white for unknown values
                pg.draw.rect(self.screen, color, (j * self.cell_size + self.padding, i * self.cell_size + self.padding,
                                                  self.cell_size - 2 * self.padding, self.cell_size - 2 * self.padding))
                if value != 0:
                    text = self.myfont.render(str(value), True, (0, 0, 0))  # Black text
                    text_rect = text.get_rect(center=(j * self.cell_size + self.cell_size / 2,
                                                       i * self.cell_size + self.cell_size / 2))
                    self.screen.blit(text, text_rect)
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