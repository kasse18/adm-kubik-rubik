import pygame

from shape.cube import Cube


class Board:
    def __init__(self, width: int, height: int, cube: Cube):
        self.width = width
        self.height = height
        self.board = [[7 for _ in range(width)] for _ in range(height)]
        self.cube = cube
        self.cube_to_board()
        self.cube.add_board(self)

        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.color = 0
        self.colorCNT = [8 for _ in range(6)]
        self.posNotChange = [(1, 4), (4, 4), (7, 4), (10, 4), (4, 1), (4, 7)]

    def cube_to_board(self):
        self.board[0][3:6] = self.cube.cube[0][0]
        self.board[1][3:6] = self.cube.cube[0][1]
        self.board[2][3:6] = self.cube.cube[0][2]
        self.board[3][3:6] = self.cube.cube[1][0]
        self.board[4][3:6] = self.cube.cube[1][1]
        self.board[5][3:6] = self.cube.cube[1][2]
        self.board[6][3:6] = self.cube.cube[2][0]
        self.board[7][3:6] = self.cube.cube[2][1]
        self.board[8][3:6] = self.cube.cube[2][2]
        self.board[9][3:6] = self.cube.cube[3][0]
        self.board[10][3:6] = self.cube.cube[3][1]
        self.board[11][3:6] = self.cube.cube[3][2]
        self.board[3][0:3] = self.cube.cube[4][0]
        self.board[4][0:3] = self.cube.cube[4][1]
        self.board[5][0:3] = self.cube.cube[4][2]
        self.board[3][6:] = self.cube.cube[5][0]
        self.board[4][6:] = self.cube.cube[5][1]
        self.board[5][6:] = self.cube.cube[5][2]
        #print(f"CUBE TO BOARD SELF.CUBE: {self.cube.cube}")

    def board_to_cube(self):
        self.cube.cube[0][0] = self.board[0][3:6]
        self.cube.cube[0][1] = self.board[1][3:6]
        self.cube.cube[0][2] = self.board[2][3:6]
        self.cube.cube[0][1] = self.board[3][3:6]
        self.cube.cube[1][1] = self.board[4][3:6]
        self.cube.cube[1][2] = self.board[5][3:6]
        self.cube.cube[2][0] = self.board[6][3:6]
        self.cube.cube[2][1] = self.board[7][3:6]
        self.cube.cube[2][2] = self.board[8][3:6]
        self.cube.cube[3][0] = self.board[9][3:6]
        self.cube.cube[3][1] = self.board[10][3:6]
        self.cube.cube[3][2] = self.board[11][3:6]
        self.cube.cube[4][0] = self.board[3][0:3]
        self.cube.cube[4][1] = self.board[4][0:3]
        self.cube.cube[4][2] = self.board[5][0:3]
        self.cube.cube[5][0] = self.board[3][6:]
        self.cube.cube[5][1] = self.board[4][6:]
        self.cube.cube[5][2] = self.board[5][6:]
        #print(f"BOARD TO CUBE SELF.CUBE: {self.cube.cube}")

    def set_view(self, screen, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.screen = screen

    def render(self):
        self.board_to_cube()
        # self.cube.render()
        self.screen.fill((128, 128, 128))
        size = self.cell_size
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(self.screen, self.cube.colors[self.board[i][j]],
                                 (self.top + size * j, self.left + size * i, size, size), )
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(self.screen, self.cube.colors[7],
                                 (self.top + size * j, self.left + size * i, size, size), 2)
        for i in range(self.height // 3):
            for j in range(self.width // 3):
                pygame.draw.rect(self.screen, self.cube.colors[7],
                                 (self.top + size * j * 3, self.left + size * i * 3, size * 3, size * 3), 4)
        for i in range(1, 7):
            pygame.draw.rect(self.screen, self.cube.colors[i],
                             (self.top + size * 10, self.left + size * (i + 2), size, size), )
            if self.colorCNT[i - 1] == 0:
                pygame.draw.rect(self.screen, self.cube.colors[0],
                                 (self.top + size * 10 + 10, self.left + size * (i + 2) + 10, size - 20, size - 20), 4)

            if self.color == i:
                if self.colorCNT[i - 1] == 0:
                    self.color = 0
                else:
                    pygame.draw.rect(self.screen, self.cube.colors[0],
                                     (self.top + size * 10, self.left + size * (i + 2), size, size), 4)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell[1] == 10 and cell[0] in [3, 4, 5, 6, 7, 8]:
            self.color = [3, 4, 5, 6, 7, 8].index(cell[0]) + 1
            if self.colorCNT[self.color - 1] == 0:
                self.color = 0
            return cell
        if cell[1] >= self.width:
            return cell
        if self.board[cell[0]][cell[1]] == 7:
            return cell
        if cell is not None:
            self.func(cell)
        return cell

    def get_cell(self, pos):
        pos = list(pos)
        if self.left < pos[0] < (self.width + 2) * self.cell_size and self.top < pos[1] < self.height * self.cell_size:
            pos[0] -= self.left
            pos[1] -= self.top
            return (pos[1] // self.cell_size, pos[0] // self.cell_size)
        return None

    def func(self, pos):
        if pos in self.posNotChange:
            return
        if self.board[pos[0]][pos[1]] not in [7, 0]:
            self.colorCNT[self.board[pos[0]][pos[1]] - 1] += 1
        if pos[1] < 3:
            i = 4
        elif pos[1] > 5:
            i = 5
        else:
            i = pos[0] // 3
        self.cube.draw(self.color, [i, pos[0] % 3, pos[1] % 3])
        self.board[pos[0]][pos[1]] = self.color
        self.colorCNT[self.color - 1] -= 1

    def full(self):
        self.color = 1
        for i in range(6, 9):
            for j in range(3, 6):
                self.func((i, j))
        self.color = 2
        for i in range(0, 3):
            for j in range(3, 6):
                self.func((i, j))
        self.color = 3
        for i in range(9, 12):
            for j in range(3, 6):
                self.func((i, j))
        self.color = 4
        for i in range(3, 6):
            for j in range(3):
                self.func((i, j))
        self.color = 5
        for i in range(3, 6):
            for j in range(6, 9):
                self.func((i, j))
        self.color = 6
        for i in range(3, 6):
            for j in range(3, 6):
                self.func((i, j))

    def problem(self):
        board = [[[1, 2, 4], [4, 6, 5], [2, 5, 3]],
 [[4, 6, 5], [4, 6, 2], [1, 1, 5]],
 [[4, 4, 2], [1, 1, 3], [2, 2, 3]],
 [[3, 3, 1], [1, 3, 3], [5, 5, 2]],
 [[6, 6, 3], [3, 4, 6], [5, 5, 6]],
 [[1, 2, 6], [4, 5, 4], [6, 5, 4]]]
        self.cube.cube = board
        self.cube_to_board()
        self.cube.cube_to_shape()
        self.render()

    def Shuffle(self):
        self.cube.Shuffle()
        self.cube.render()
        self.cube_to_board()
        self.render()

    def ShuffleBase(self, pygame):
        funcs = [
            self.cube.f,
            self.cube.R,
            self.cube.u,
            self.cube.B,
            self.cube.l,
            self.cube.D,
            self.cube.F,
            self.cube.r,
            self.cube.U,
            self.cube.b,
            self.cube.L,
            self.cube.d,
            self.cube.R
        ]
        i = 0
        for func in funcs:
            i += 1
            func()
            self.cube.render()
            self.cube_to_board()
            self.render()
            pygame.display.flip()
        self.cube.cross()
