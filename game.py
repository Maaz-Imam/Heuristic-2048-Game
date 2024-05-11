import os
from numpy import hstack, ndindex
import numpy as np
from grid import Grid
import random

class Solver:
    def __init__(self, size):
        self.size = size
        self.env = Grid(size)
        
    def no_moves(self):
        if self.next_move_predictor()[1] == 0:
            return True 
    
    def next_move_predictor(self):
        directions = ['w', 's', 'a', 'd']
        next_score = {'w': 0, 's': 0, 'a': 0, 'd': 0}

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

            # Apply expectimax algorithm
            # score = self.expectimax(grid_copy, depth=2, is_chance=True)
            score = self.get_score(grid_copy)
            next_score[direction] = score

        print("Final predictions:", next_score)
        return max(next_score.items(), key=lambda x: x[1])

    def expectimax(self, grid, depth, is_chance):
        if depth == 0 or self.env.is_full():
            return self.get_score(grid)

        if is_chance:
            empty_cells = self.get_empty_cells(grid)
            total_score = 0
            total_weight = 0
            for cell in empty_cells:
                x, y = cell
                new_grid = [row[:] for row in grid]
                new_grid[x][y] = 2 
                score = self.expectimax(new_grid, depth - 1, is_chance=True)
                # Weighted sum by the probability of new tile (0.9 for 2, 0.1 for 4)
                total_score += score * 0.9
                total_weight += 0.9
                new_grid[x][y] = 4  # Assume new tile is 4
                score = self.expectimax(new_grid, depth - 1, is_chance=False)
                total_score += score * 0.1
                total_weight += 0.1
            return total_score / total_weight if total_weight > 0 else 0
        else:
            directions = ['w', 's', 'a', 'd']
            total_score = 0
            for direction in directions:
                new_grid = [row[:] for row in grid]
                if direction == 'w':
                    self.env.move_up(new_grid)
                elif direction == 's':
                    self.env.move_down(new_grid)
                elif direction == 'a':
                    self.env.move_left(new_grid)
                elif direction == 'd':
                    self.env.move_right(new_grid)
                score = self.expectimax(new_grid, depth - 1, is_chance=True)
                total_score += score
            return total_score / len(directions)

    def get_empty_cells(self, grid):
        return [(i, j) for i in range(self.size) for j in range(self.size) if grid[i][j] == 0]


    def score_adjacent_tiles(self, grid):
        """
        The function `score_adjacent_tiles` calculates the average of the scores obtained from counting and
        finding the mean of neighboring tiles on a grid.
        
        """
        return (self.score_count_neighbor(grid) + self.score_mean_neighbor(grid)) / 2



    def score_snake(self, grid, base_value=0.30):
        # From https://github.com/davidluescher/2048-ai/blob/master/heuristicai.py
        """
        The function `score_snake` calculates the score of a game grid in a snake-like game by combining
        values from different directions.
        """
        score = 0
        rewardArray = [base_value ** i for i in range(16)]
        for i in range(2):
            gridArray = hstack((grid[0], grid[1][::-1], grid[2], grid[3][::-1]))
            score = max(score, (rewardArray * gridArray).sum())
            score = max(score, (rewardArray[::-1] * gridArray).sum())
            gridArray = hstack((grid[0][::-1], grid[1], grid[2][::-1], grid[3]))
            score = max(score, (rewardArray * gridArray).sum())
            score = max(score, (rewardArray[::-1] * gridArray).sum())
            grid = grid.T
        return score


    def score_mean_neighbor(self, newgrid):
        """
        Calculate the mean(average) of  tiles with the same values that are adjacent in a row/column.
        """
        horizontal_sum, count_horizontal = self.check_neighbor(newgrid)
        vertical_sum, count_vertical = self.check_neighbor(newgrid.T)
        if count_horizontal == 0 or count_vertical == 0:
            return 0
        return horizontal_sum / count_horizontal + vertical_sum / count_vertical


    def check_neighbor(self, grid):
        """
        Returns the sum and total number (count) of tiles with the same values that are adjacent in a row/column.
        """
        count = 0
        sum = 0
        for row in grid:
            previous = -1
            for tile in row:
                if previous == tile:
                    sum += tile
                    count += 1
                previous = tile
        return sum, count


    def score_count_neighbor(self, grid):
        _, horizontal_count = self.check_neighbor(grid)
        _, vertical_count = self.check_neighbor(grid.T)
        return horizontal_count + vertical_count


    def calculate_empty_tiles(self, grid):
        empty_tiles = 0
        for x, y in ndindex(grid.shape):
            if grid[x, y] == 0:
                empty_tiles += 1
        return empty_tiles


    def get_score(self, grid):
        grid = np.array(grid)
        return (1.5 * self.score_adjacent_tiles(grid) + 3 * self.score_snake(grid) + 2 * self.calculate_empty_tiles(grid)) / 6

    def run(self):
        while True:
            os.system("cls")
            if self.env.is_full():
                print("\nTOTAL SCORE:", self.env.score, "\n")
                print(self.env.render())
                if self.env.flag and self.no_moves():
                    print("\n\nX---X---X  GAME OVER  X---X---X\n\n")
                    input()
                    break
                os.system("cls")

            print("\nTOTAL SCORE:", self.env.score, "\n")
            self.env.render()

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
    

if __name__ == "__main__":
    size = 4
    solver = Solver(size)
    solver.run()
