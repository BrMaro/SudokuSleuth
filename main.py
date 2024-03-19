import pprint
import pygame
import time
import numpy as np

pygame.init()
clock = pygame.time.Clock()
WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, WIDTH), pygame.DOUBLEBUF)
pygame.display.set_caption("Sudoku Solver")
font = pygame.font.Font('freesansbold.ttf', 32)
game = 9

BORDER_BLINK_INTERVAL = 1000
SOLVING_SPEED = 0.000005

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
text_rects = []


original_board = [
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
board = original_board
immediately_solved_board= original_board.copy()


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows
        self.border_visible = False
        self.blink_timer = 0
        self.blink_interval = BORDER_BLINK_INTERVAL
        self.clicked = False

    def draw(self, win):
        if self.border_visible:
            pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.width), 2)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def blink_if_clicked(self, current_time):
        if self.clicked:
            print("Blinking")
            # Get the current time
            time_since_last_blink = current_time - self.blink_timer  # Calculate time since last blink
            if time_since_last_blink >= self.blink_interval:
                print("time for next blink")
                self.border_visible = not self.border_visible
                print(self.border_visible)
                self.blink_timer = current_time

    def click(self):
        print(f"Node {self.row, self.col} clicked")
        self.clicked = True

    def stop_blinking(self):
        print("Stop blinking")
        self.clicked = False
        self.border_visible = False


def get_node_clicked(grid):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for row in grid:
        for node in row:
            if node.x < mouse_x < node.x + node.width and node.y < mouse_y < node.y + node.width:
                return node.row, node.col


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
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap), 1)
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width), 1)
    for i in range(0, rows + 3, 3):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap), 5)
    for j in range(0, rows + 3, 3):
        pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width), 5)


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)


def render_numbers_on_board(win, width, rows, board):
    gap = width // rows
    start_y = gap // 2

    for row in range(len(board)):
        start_x = gap // 2  # Reset start_x for each row
        for col in range(len(board[row])):
            if original_board[row][col] == -1:
                text = font.render(str(board[row][col]) if board[row][col] != -1 else ' ', True, GREY)
                textRect = text.get_rect()
                textRect.center = (start_x, start_y)
                text_rects.append(textRect)
                win.blit(text, textRect)
            else:
                text = font.render(str(board[row][col]) if board[row][col] != -1 else ' ', True, BLACK)
                textRect = text.get_rect()
                textRect.center = (start_x, start_y)
                text_rects.append(textRect)
                win.blit(text, textRect)
            start_x += gap
        start_y += gap


def render_original_board(win, width, rows):
    gap = width // rows
    start_y = gap // 2

    for row in range(len(original_board)):
        start_x = gap // 2  # Reset start_x for each row
        for col in range(len(original_board[row])):
            text = font.render(str(original_board[row][col]) if original_board[row][col] != -1 else ' ', True, BLACK)
            textRect = text.get_rect()
            textRect.center = (start_x, start_y)
            win.blit(text, textRect)
            start_x += gap
        start_y += gap

    pygame.display.update()


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


def solve_sudoku_generator(puzzle):
    row, col = find_next_empty(puzzle)

    if row is None:
        yield puzzle
        return

    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            yield puzzle
            yield from solve_sudoku_generator(puzzle)

    puzzle[row][col] = -1


def main(win, width):
    ROWS = 9

    program_running = True
    animation_started = False
    clicked_node = None
    solving_generator = solve_sudoku_generator(board)

    while program_running:
        grid = make_grid(ROWS, width)
        draw(win, grid, ROWS, width)
        render_original_board(win, width, ROWS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mousedown")
                if pygame.mouse.get_pressed()[0] and not animation_started:
                    for row in grid:
                        for node in row:
                            if node.x < event.pos[0] < node.x + node.width and node.y < event.pos[
                                1] < node.y + node.width:
                                node.click()
                                clicked_node = node

            if event.type == pygame.KEYDOWN:
                print("keydown")
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                    if clicked_node:
                        row, col = get_node_clicked(grid)
                        original_board[col][row] = int(event.unicode)
                        clicked_node.stop_blinking()
                        clicked_node = None

                if event.key == pygame.K_SPACE and not animation_started:  # START BUTTON
                    animation_started = True

                if event.key == pygame.K_ESCAPE and animation_started:  # PAUSE BUTTON
                    animation_started = False

                if event.key == pygame.K_RETURN:
                    solve_sudoku(immediately_solved_board)
                    print(immediately_solved_board)
                    animation_started = False
                    render_numbers_on_board(win, width, ROWS, immediately_solved_board)

        current_time = pygame.time.get_ticks()
        for row in grid:
            for node in row:
                node.blink_if_clicked(current_time)

        if animation_started:
            try:
                success = next(solving_generator)
                render_numbers_on_board(win, width, ROWS, board)
                time.sleep(SOLVING_SPEED)

            except StopIteration as e:
                print("No more steps")
                animation_started = False
        pygame.display.update()
    pygame.quit()


main(WIN, WIDTH)
