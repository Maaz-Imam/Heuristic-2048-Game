import random
import os
import msvcrt

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.grid[random.randint(0, size - 1)][random.randint(0, size - 1)] = 2
        self.score = 0

    def __str__(self):
        return '\n'.join(['\t|\t'.join([str(cell) for cell in row]) for row in self.grid])

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
            if self.is_full():
                print("Game Over")
                break
            os.system("cls")
            print("\nTOTAL SCORE: ",self.score,"\n")
            print(self)
            print("\nEnter direction: ")
            direction = msvcrt.getch().decode()
            # print(direction)
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