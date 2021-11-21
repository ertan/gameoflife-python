import curses
import random
import time

SEED = 20180926
ALIVE = '1'
DEAD = ' '

class GameOfLife:
    def __init__(self, size: int):
        if (size < 2):
            exit('Size has to be greater or equal to 2')
        random.seed(SEED)
        flat_world = random.choices([DEAD, ALIVE], k = (size * size))
        self.world = [flat_world[i*size:(i+1)*size] for i in range(size)]

    def __str__(self):
        world = ''
        for i in range(len(self.world)):
            world += ' '.join(self.world[i]) + '\n'
        return world

    def _count_alive_neighbors(self, row: int, col: int):
        if len(self.world) == 0 or len(self.world[0]) == 0:
            return 0
        alive_neighbors = 0
        if (row - 1 >= 0):
            if (self.world[row-1][col] == ALIVE):
                alive_neighbors += 1
            if (col - 1 >= 0 and self.world[row-1][col-1] == ALIVE):
                alive_neighbors += 1
            if (col + 1 < len(self.world[0]) and self.world[row - 1][col + 1] == ALIVE):
                alive_neighbors += 1
        if (row + 1 < len(self.world)):
            if (self.world[row + 1][col] == ALIVE):
                alive_neighbors += 1
            if (col - 1 >= 0 and self.world[row + 1][col - 1] == ALIVE):
                alive_neighbors += 1
            if (col + 1 < len(self.world[0]) and self.world[row + 1][col + 1] == ALIVE):
                alive_neighbors += 1
        if (col - 1 >= 0 and self.world[row][col - 1] == ALIVE):
            alive_neighbors += 1
        if (col + 1 < len(self.world[0]) and self.world[row][col + 1] == ALIVE):
            alive_neighbors += 1
        return alive_neighbors   

    def step(self):
        new_dead = []
        new_alive = []
        for i in range(len(self.world)):
            for j in range(len(self.world[0])):
                alive_neighbors = self._count_alive_neighbors(i, j)
                if (self.world[i][j] == ALIVE):
                    # Any live cell with two or three live neighbours survives.
                    # All other live cells die in the next generation.
                    if (alive_neighbors < 2 or alive_neighbors > 3):
                        new_dead.append((i, j))
                else:
                    # Any dead cell with three live neighbours becomes a live cell.
                    if (alive_neighbors == 3):
                        new_alive.append((i, j))
        for (i, j) in new_dead:
            assert self.world[i][j] == ALIVE
            self.world[i][j] = DEAD
        for (i, j) in new_alive:
            assert self.world[i][j] == DEAD
            self.world[i][j] = ALIVE


def main():
    size = int(input('Please enter the size of the world '))
    step_count = int(input('Please enter the number of steps you would like to run '))
    screen = curses.initscr()
    g = GameOfLife(size)
    for _ in range(step_count):
        screen.clear()
        screen.addstr(str(g))
        screen.refresh()
        g.step()
        time.sleep(0.5)
    curses.endwin()


if __name__ == "__main__":
    main()