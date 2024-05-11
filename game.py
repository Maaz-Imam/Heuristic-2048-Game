import os
from grid import Grid

class Solver:
    def __init__(self, size):
        self.size = size
        self.env = Grid(size)
        
    def no_moves(self):
        print("--> ", self.next_move_predictor())
        if self.next_move_predictor()[1] == 0:
            return True 
    
    def next_move_predictor(self):
        directions = ['w', 's', 'a', 'd']
        next_score = {'s': 0, 'd': 0, 'a': 0, 'w': 0}

        for direction in directions:
            grid_copy = [row[:] for row in self.env.grid]

            if direction == 'w':
                self.env.move_up(grid_copy)
            elif direction == 's':
                self.env.move_down(grid_copy)
            elif direction == 'a':
                self.env.move_left(grid_copy)
            elif direction == 'd':
                self.env.move_right(grid_copy)

            score = self.calculate_score(grid_copy)
            next_score[direction] = score

        print("Final predictions:", next_score)
        return max(next_score.items(), key=lambda x: x[1])
    
    def calculate_score(self, grid):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                score += grid[i][j] * (self.size - i) * (self.size - j)

        # # Add heuristic for snake pattern
        snake_score = self.snake_pattern_score(grid)
        score += snake_score

        return score

    def snake_pattern_score(self, grid):
        snake_score = 0
        for i in range(self.size):
            if i % 2 != 0:
                for j in range(self.size):
                    snake_score += grid[i][j]
            else:
                for j in range(self.size - 1, -1, -1):
                    snake_score += grid[i][j]
        return snake_score

    def run(self):
        while True:
            # os.system("cls")
            
            best_move = ''

            if self.env.flag == 1:
                print('\n\nGoing to predict next move')
                best_move, best_score = self.next_move_predictor()

                print("Next move should be:", best_move, "\nWith a score of:", best_score)
            self.env.flag = 1

            print("\n\nEnter direction:")
            direction = best_move
            print(direction)

            if direction == "w":
                self.env.move_up()
            elif direction == "s":
                self.env.move_down()
            elif direction == "a":
                self.env.move_left()
            elif direction == "d":
                self.env.move_right()
            self.env.generate_new_cell()
            
            if self.env.is_full():
                print("\nTOTAL SCORE:", self.env.score, "\n")
                print(self.env.render())
                if self.env.flag and self.no_moves():
                    print("\n\nX---X---X  GAME OVER  X---X---X\n\n")
                    break
            # os.system("cls")

            print("\nTOTAL SCORE:", self.env.score, "\n")
            self.env.render()

    

if __name__ == "__main__":
    size = 4
    solver = Solver(size)
    solver.run()
