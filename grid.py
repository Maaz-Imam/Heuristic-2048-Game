import random
import copy
import pygame as pg

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.grid[random.randint(0, size - 1)][random.randint(0, size - 1)] = 2

        self.score = 0
        self.flag = 0
        
        pg.init()
        self.myfont = pg.font.SysFont('Arial', 30)
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
            2048: (237, 194, 46),
        }
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("2048")

    def render(self):
        self.screen.fill((187, 173, 160))  # Background color
        self.handle_events()
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                color = self.colors.get(value, (100, 105, 100))  # Default to gray for unknown values
                pg.draw.rect(self.screen, color, (j * self.cell_size + self.padding, i * self.cell_size + self.padding,
                                                  self.cell_size - 2 * self.padding, self.cell_size - 2 * self.padding))
                if value != 0:
                    text = self.myfont.render(str(value), True, (0, 0, 0))  # Black text
                    text_rect = text.get_rect(center=(j * self.cell_size + self.cell_size / 2,
                                                       i * self.cell_size + self.cell_size / 2))
                    self.screen.blit(text, text_rect)
        pg.display.flip()
        
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
    
    def is_safe(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == 0
    
    def is_full(self):
        if self.move_up(copy.deepcopy(self.grid)) or self.move_down(copy.deepcopy(self.grid)) or self.move_left(copy.deepcopy(self.grid)) or self.move_right(copy.deepcopy(self.grid)):
            return False
        return True
    
    def reset(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.grid[random.randint(0, self.size - 1)][random.randint(0, self.size - 1)] = 2
        self.score = 0
        return copy.deepcopy(self.grid)

    def generate_new_cell(self):
        x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        while not self.is_safe(x, y):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self.grid[x][y] = 2 if random.random() < 0.9 else 4
    
    def move_up(self, grid=None):
        if grid is None:
            grid = self.grid
        moved = False
        for j in range(self.size):
            for i in range(1, self.size):
                if grid[i][j] == 0:
                    continue
                x = i
                while x > 0 and grid[x - 1][j] == 0:
                    x -= 1
                if x == 0 or (grid[x - 1][j] != grid[i][j]):
                    grid[x][j] = grid[i][j]
                    if x != i:
                        grid[i][j] = 0
                        moved = True
                else:
                    grid[x - 1][j] *= 2
                    self.score += grid[x - 1][j]  # adding to total score
                    grid[i][j] = 0
                    moved = True
        return moved
                    
    def move_down(self, grid=None):
        if grid is None:
            grid = self.grid
        moved = False
        for j in range(self.size):
            for i in range(self.size - 2, -1, -1):
                if grid[i][j] == 0:
                    continue
                x = i
                while x < self.size - 1 and grid[x + 1][j] == 0:
                    x += 1
                if x == self.size - 1 or (grid[x + 1][j] != grid[i][j]):
                    grid[x][j] = grid[i][j]
                    if x != i:
                        grid[i][j] = 0
                        moved = True
                else:
                    grid[x + 1][j] *= 2
                    self.score += grid[x + 1][j]  # adding to total score
                    grid[i][j] = 0
                    moved = True
                    
        return moved
            
    def move_left(self, grid=None):
        if grid is None:
            grid = self.grid
        moved = False
        for j in range(self.size):
            for i in range(self.size):
                if grid[i][j] == 0:
                    continue
                x = j
                while x > 0 and grid[i][x - 1] == 0:
                    x -= 1
                if x == 0 or (grid[i][x - 1] != grid[i][j]):
                    grid[i][x] = grid[i][j]
                    if x != j:
                        grid[i][j] = 0
                        moved = True
                else:
                    grid[i][x - 1] *= 2
                    self.score += grid[i][x - 1]  # adding to total score
                    grid[i][j] = 0
                    moved = True
        return moved
            
    def move_right(self, grid=None):
        if grid is None:
            grid = self.grid
        moved = False
        for j in range(self.size):
            for i in range(self.size - 1, -1, -1):
                if grid[i][j] == 0:
                    continue
                x = j
                while x < self.size - 1 and grid[i][x + 1] == 0:
                    x += 1
                if x == self.size - 1 or (grid[i][x + 1] != grid[i][j]):
                    grid[i][x] = grid[i][j]
                    if x != j:
                        grid[i][j] = 0
                        moved = True
                else:
                    grid[i][x + 1] *= 2
                    self.score += grid[i][x + 1]  # adding to total score
                    grid[i][j] = 0
                    moved = True
        return moved
    
    def step(self, action):
        # Store the current state before taking the action
        current_state = copy.deepcopy(self.grid)
        current_score = self.score

        # Perform the action
        if action == 'w':
            moved = self.move_up()
        elif action == 's':
            moved = self.move_down()
        elif action == 'a':
            moved = self.move_left()
        elif action == 'd':
            moved = self.move_right()
        else:
            raise ValueError("Invalid action")

        # Check if the board has changed after the action
        if moved:
            # Generate a new cell after the action
            self.generate_new_cell()

            # Calculate the reward
            reward = self.score - current_score
            # Check if the game is over
            done = self.is_full()
        else:
            # If the action didn't change the board, penalize with a negative reward
            reward = -0.1
            done = False

        # Return the next state, reward, and whether the episode is done
        next_state = copy.deepcopy(self.grid)
        return next_state, reward, done
