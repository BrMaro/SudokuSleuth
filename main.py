import pprint
import pygame
import time


pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Sudoku Solver")
font = pygame.font.Font('freesansbold.ttf', 32)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
AQUA = (100, 200, 200)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def get_pos(self):
        return self.row, self.col


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
    for i in range(0, rows, 3):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap), 3)
    for j in range(0, rows, 3):
        pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width), 3)


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def render_numbers_on_board(win, width, rows):
    gap = width // rows
    start_y = gap // 2

    for row in range(len(board)):
        start_x = gap // 2  # Reset start_x for each row
        for col in range(len(board[row])):
            text = font.render(str(board[row][col]) if board[row][col] != -1 else ' ', True, BLACK)
            textRect = text.get_rect()
            textRect.center = (start_x, start_y)
            win.blit(text, textRect)
            start_x += gap
        start_y += gap

    pygame.display.update()


# pp = pprint.PrettyPrinter()
#
board = [
    [3, 9, -1, -1, 5, -1, -1, -1, -1],
    [-1, -1, -1, 2, -1, -1, -1, -1, 5],
    [-1, -1, -1, 7, 1, 9, -1, 8, -1],
    [-1, 5, -1, -1, 6, 8, -1, -1, -1],
    [2, -1, 6, -1, -1, 3, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 4],
    [5, -1, -1, -1, -1, -1, -1, -1, -1],
    [6, 7, -1, 1, -1, 5, -1, 4, -1],
    [1, -1, 9, -1, -1, -1, 2, -1, -1]
]


def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None


def is_valid(puzzle, guess, row, col):
    if guess in puzzle[row]:
        return False

    if guess in [puzzle[i][col] for i in range(9)]:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False
    return True


def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)

    if row is None:
        return True

    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True

    puzzle[row][col] = -1

    return False


#
def main(win, width):
    ROWS = 9
    grid = make_grid(ROWS, width)
    draw(win, grid, ROWS, width)
    program_running = True
    animation_started = False

    while program_running:

        if animation_started:
            solve_sudoku(board)
            time.sleep(2)


        render_numbers_on_board(win, width, ROWS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not animation_started:
                    animation_started = True

    pygame.quit()


main(WIN, WIDTH)

# solve_sudoku(board)
#
# pp.pprint((board))
