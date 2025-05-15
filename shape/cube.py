import random
import time

import pygame.display
import itertools
from collections import deque
import const as c
from shape.shape import Shape2, Shape3

import itertools
from collections import deque


class Cube:
    def __init__(self, game):
        self.board = None
        self.game = game
        self.cube = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(6)]
        print(self.cube)
        self.colors = [c.black, c.red, c.orange, c.yellow, c.green, c.blue, c.white, c.gray]
        self.move_count = 0
        self.cube[0][1][1] = 2
        self.cube[1][1][1] = 1
        self.cube[2][1][1] = 6
        self.cube[3][1][1] = 3
        self.cube[4][1][1] = 4
        self.cube[5][1][1] = 5
        print(self.cube)
        self.shape3 = [Shape3(1, 2, 4),
                       Shape3(0, 1, 4),
                       Shape3(0, 5, 1),
                       Shape3(1, 5, 2),
                       Shape3(4, 3, 0),
                       Shape3(2, 3, 4),
                       Shape3(2, 5, 3),
                       Shape3(0, 3, 5)]
        self.shape2 = [Shape2(1, 4),
                       Shape2(0, 1),
                       Shape2(1, 5),
                       Shape2(1, 2),
                       Shape2(0, 4),
                       Shape2(0, 3),
                       Shape2(0, 5),
                       Shape2(3, 5),
                       Shape2(3, 4),
                       Shape2(2, 4),
                       Shape2(2, 5),
                       Shape2(2, 3)]

        self.cubeShape: list[list[list[int]]] = [
            [
                [4, 5, 7],
                [4, 2, 6],
                [1, 1, 2]
            ],
            [
                [1, 1, 2],
                [0, 6, 2],
                [0, 3, 3]
            ],
            [
                [0, 3, 3],
                [9, 1, 10],
                [5, 11, 6],
            ],
            [
                [5, 11, 6],
                [8, 3, 7],
                [4, 5, 7],
            ],
            [
                [4, 4, 1],
                [8, 4, 0],
                [5, 9, 0]
            ],
            [
                [2, 6, 7],
                [2, 5, 7],
                [3, 10, 6]
            ]
        ]

        self.position_color = {
            0: 2,
            1: 6,
            2: 1,
            3: 3,
            4: 4,
            5: 5,
        }
        self.color_position = {
            1: 2,
            2: 0,
            3: 3,
            4: 4,
            5: 5,
            6: 1
        }

        self.position_function = {
            0: self.B,
            1: self.U,
            2: self.F,
            3: self.D,
            4: self.L,
            5: self.R,
        }

        self.position_function_2 = {
            0: self.B2,
            1: self.U2,
            2: self.F2,
            3: self.D2,
            4: self.L2,
            5: self.R2,
        }

        self.position_function_3 = {
            0: self.b,
            1: self.u,
            2: self.f,
            3: self.d,
            4: self.l,
            5: self.r,
        }

        self.white_shape2 = []
        self.white_shape3 = []
        self.second_shape = []
        self.yellow_shape2 = []
        self.yellow_shape3 = []

        self.color_left = {
            1: 4,
            4: 2,
            2: 5,
            5: 1
        }

        self.color_right = {
            1: 5,
            4: 1,
            2: 4,
            5: 2
        }

        self.position_left = {
            0: 5,
            5: 2,
            2: 4,
            4: 0
        }

        self.cube = [
            [[2] * 3, [2] * 3, [2] * 3],  # Back (B)
            [[6] * 3, [6] * 3, [6] * 3],  # Up (U)
            [[1] * 3, [1] * 3, [1] * 3],  # Front (F)
            [[3] * 3, [3] * 3, [3] * 3],  # Down (D)
            [[4] * 3, [4] * 3, [4] * 3],  # Left (L)
            [[5] * 3, [5] * 3, [5] * 3]  # Right (R)
        ]

    def get_kociemba_state(self):
        self.shape_to_cube()

        CENTER_MAP = {
            0: 2,  # Back (B) - Оранжевый
            1: 6,  # Up (U) - Белый (было 2 → 1)
            2: 1,  # Front (F) - Красный (было 1 → 2)
            3: 3,  # Down (D) - Желтый
            4: 4,  # Left (L) - Зеленый
            5: 5  # Right (R) - Синий
        }

        for face, expected_color in CENTER_MAP.items():
            actual_color = self.cube[face][1][1]
            if actual_color != expected_color:
                raise ValueError(
                    f"Центр грани {face} должен быть {expected_color}, получен {actual_color}"
                )

        FACES_ORDER = [1, 5, 2, 3, 4, 0]

        COLOR_MAP = {
            1: 'F', 2: 'B', 3: 'D',
            4: 'L', 5: 'R', 6: 'U'
        }

        state = []
        for face in FACES_ORDER:
            # print("FACE: ", face)
            if face == 5:
                # print("Self.cube.face: ", self.cube[face])
                for i in range(3):
                    for row in range(2, -1, -1):
                        color = self.cube[face][row][i]
                        state.append(COLOR_MAP[color])
            elif face == 4:
                # print("Self.cube.face: ", self.cube[face])
                for i in range(2, -1, -1):
                    for row in range(3):
                        color = self.cube[face][row][i]
                        state.append(COLOR_MAP[color])
            elif face == 0:
                color_reversed = ""
                for row in self.cube[face]:
                    for color in row:
                        color_reversed += COLOR_MAP[color]
                state.append(color_reversed[::-1])
            else:
                for row in self.cube[face]:
                    for color in row:
                        state.append(COLOR_MAP[color])

        return ''.join(state)

    def execute_algorithm(self, algorithm):
        moves = {
            'U1': self.U, 'U2': self.U2, "U3": self.u,
            'R1': self.R, 'R2': self.R2, "R3": self.r,
            'F1': self.F, 'F2': self.F2, "F3": self.f,
            'D1': self.D, 'D2': self.D2, "D3": self.d,
            'L1': self.L, 'L2': self.L2, "L3": self.l,
            'B1': self.B, 'B2': self.B2, "B3": self.b
        }
        if self.check():
            return

        for move in algorithm.split():
            if move in moves:
                moves[move]()
                self.render()

    def reset_move_count(self):
        self.move_count = 0

    def add_board(self, board):
        self.board = board

    def draw(self, color: int, cord: list[int]):
        ind = self.cubeShape[cord[0]][cord[1]][cord[2]]
        if (cord[1] + 1) * (cord[2] + 1) % 2 == 0:
            i = self.shape2[ind].pos.index(cord[0])
            self.shape2[ind].colors[i] = color
        else:
            i = self.shape3[ind].pos.index(cord[0])
            self.shape3[ind].colors[i] = color
        self.cube[cord[0]][cord[1]][cord[2]] = color

    def check(self):
        self.shape_to_cube()
        for side in self.cube:
            for i in range(3):
                for j in range(3):
                    if side[i][j] != side[1][1]:
                        return False
        return True

    def shape_to_cube(self):
        for i in range(6):
            for k in range(3):
                for j in range(3):
                    shape_ind = self.cubeShape[i][j][k]
                    if k == 1 and j == 1:
                        color = shape_ind
                    elif (j + 1) * (k + 1) % 2 == 0:
                        t = self.shape2[shape_ind].pos.index(i)
                        color = self.shape2[shape_ind].colors[t]
                    else:
                        t = self.shape3[shape_ind].pos.index(i)
                        color = self.shape3[shape_ind].colors[t]
                    self.cube[i][j][k] = color

    def cube_to_shape(self):
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    color = self.cube[i][j][k]
                    shape_ind = self.cubeShape[i][j][k]
                    if k == 1 and j == 1:
                        continue
                    if (j + 1) * (k + 1) % 2 == 0:
                        t = self.shape2[shape_ind].pos.index(i)
                        self.shape2[shape_ind].colors[t] = color
                    else:
                        t = self.shape3[shape_ind].pos.index(i)
                        self.shape3[shape_ind].colors[t] = color

    def render(self):
        self.shape_to_cube()
        self.board.cube_to_board()
        self.board.render()
        pygame.display.flip()

    def DataSwitch(self, place: list[list[int]]):
        shape2_ind = [place[0][1], place[1][2], place[2][1], place[1][0]]
        shape3_ind = [place[0][0], place[0][2], place[2][2], place[2][0]]
        shape2 = self.shape2[:]
        shape3 = self.shape3[:]
        pos2 = [[shape2[el].pos[0], shape2[el].pos[1]] for el in shape2_ind]
        pos3 = [[shape3[el].pos[0], shape3[el].pos[1], shape3[el].pos[2]] for el in shape3_ind]
        return pos2, pos3, shape2, shape3, shape2_ind, shape3_ind

    def switch(self, ind: int):
        place = self.cubeShape[ind]
        pos2, pos3, shape2, shape3, shape2_ind, shape3_ind = self.DataSwitch(place)
        for i in range(4):
            ind2 = shape2[shape2_ind[i]].pos.index(ind)
            ind_new2 = shape2[shape2_ind[i - 1]].pos.index(ind)

            self.shape2[shape2_ind[i]] = shape2[shape2_ind[i - 1]]
            self.shape2[shape2_ind[i]].pos[ind_new2 - 1] = pos2[i][ind2 - 1]
            self.shape2[shape2_ind[i]].pos[ind_new2] = ind

            ind3 = pos3[i].index(ind)
            ind_new3 = pos3[i - 1].index(ind)
            new_pos = pos3[i][ind3 - ind_new3:] + pos3[i][:ind3 - ind_new3]
            self.shape3[shape3_ind[i]] = shape3[shape3_ind[i - 1]]
            self.shape3[shape3_ind[i]].pos = new_pos

    def U(self):
        # print("U")
        time.sleep(0.1)
        self.switch(1)
        self.move_count += 1
        self.render()

    def R(self):
        # print("R")
        time.sleep(0.1)
        self.switch(5)
        self.move_count += 1
        self.render()

    def L(self):
        # print("L")
        time.sleep(0.1)
        self.switch(4)
        self.move_count += 1
        self.render()

    def D(self):
        # print("D")
        time.sleep(0.1)
        self.switch(3)
        self.move_count += 1
        self.render()

    def F(self):
        # print("F")
        time.sleep(0.1)
        self.switch(2)
        self.move_count += 1
        self.render()

    def B(self):
        # print("B")
        time.sleep(0.1)
        self.switch(0)
        self.move_count += 1
        self.render()

    def U2(self):
        # print("U")
        time.sleep(0.1)
        self.switch(1)
        self.switch(1)
        self.move_count += 1
        self.render()

    def R2(self):
        # print("R")
        time.sleep(0.1)
        self.switch(5)
        self.switch(5)
        self.move_count += 1
        self.render()

    def L2(self):
        # print("L")
        time.sleep(0.1)
        self.switch(4)
        self.switch(4)
        self.move_count += 1
        self.render()

    def D2(self):
        # print("D")
        time.sleep(0.1)
        self.switch(3)
        self.switch(3)
        self.move_count += 1
        self.render()

    def F2(self):
        # print("F")
        time.sleep(0.1)
        self.switch(2)
        self.switch(2)
        self.move_count += 1
        self.render()

    def B2(self):
        # print("B")
        time.sleep(0.1)
        self.switch(0)
        self.switch(0)
        self.move_count += 1
        self.render()

    def u(self):
        # # print("u")
        time.sleep(0.1)
        self.switch(1)
        self.switch(1)
        self.switch(1)
        self.move_count += 1
        self.render()

    def r(self):
        # print("r")
        time.sleep(0.1)
        self.switch(5)
        self.switch(5)
        self.switch(5)
        self.move_count += 1
        self.render()

    def l(self):
        # print("l")
        time.sleep(0.1)
        self.switch(4)
        self.switch(4)
        self.switch(4)
        self.move_count += 1
        self.render()

    def d(self):
        # print("d")
        time.sleep(0.1)
        self.switch(3)
        self.switch(3)
        self.switch(3)
        self.move_count += 1
        self.render()

    def f(self):
        # print("f")
        time.sleep(0.3)
        self.switch(2)
        self.switch(2)
        self.switch(2)
        self.move_count += 1
        self.render()

    def b(self):
        # print("b")
        time.sleep(0.1)
        self.switch(0)
        self.switch(0)
        self.switch(0)
        self.move_count += 1
        self.render()

    def Shuffle(self):
        funcs = [self.U, self.B, self.D, self.F, self.R, self.L, ]
        funcs[random.randint(0, len(funcs) - 1)]()
        self.move_count = 0

    def cross_func(self, position: int):
        # print("cross_func", position)
        flag = True
        cnt = 0
        while flag:
            flag = False
            for el in self.shape2:
                if el.pos in [[1, position], [position, 1]] and 6 in el.colors:
                    cnt += 1
                    self.U()
                    flag = True
                    break
                if el.pos in [[3, position], [position, 3]] and 6 in el.colors:
                    self.D()
                    flag = True
                    break
        self.position_function[position]()
        for _ in range(cnt):
            self.u()

    def cross_func_1(self):
        for elem in self.white_shape2:
            if elem.pos != [self.color_position[elem.colors[0]], self.color_position[elem.colors[1]]]:
                if 1 in elem.pos:
                    # print("1", elem.pos, elem.colors)
                    ind_1 = elem.pos.index(1)
                    flag = True
                    while flag:
                        flag = False
                        for el in self.white_shape2:
                            if el == elem:
                                continue
                            if el.pos in [[3, elem.pos[ind_1 - 1]], [elem.pos[ind_1 - 1], 3]]:
                                self.D()
                                flag = True
                                break
                    self.position_function_2[elem.pos[ind_1 - 1]]()

    def cross_func_2(self):
        for elem in self.white_shape2:
            if elem.pos != [self.color_position[elem.colors[0]], self.color_position[elem.colors[1]]]:
                if 3 not in elem.pos:
                    # print("not 3", elem.pos, elem.colors)
                    nn = sorted(elem.pos)
                    match nn:
                        case [2, 5]:
                            self.cross_func(2)
                        case [0, 5]:
                            self.cross_func(5)
                        case [0, 4]:
                            self.cross_func(0)
                        case [2, 4]:
                            self.cross_func(4)

    def cross(self):
        self.white_shape2 = []
        for elem in self.shape2:
            if 6 in elem.colors:
                self.white_shape2.append(elem)

        flag = True
        while flag:
            flag = False
            for elem in self.white_shape2:
                if 1 in elem.pos and elem.pos != [self.color_position[elem.colors[0]],
                                                  self.color_position[elem.colors[1]]]:
                    self.cross_func_1()
                    flag = True
                    break
                if 3 not in elem.pos and elem.pos != [self.color_position[elem.colors[0]],
                                                      self.color_position[elem.colors[1]]]:
                    self.cross_func_2()
                    flag = True
                    break
        # print("final")
        for elem in self.white_shape2:
            if 1 in elem.pos:
                continue
            if elem.pos != [self.color_position[elem.colors[0]], self.color_position[elem.colors[1]]]:
                ind_wh = elem.colors.index(6)
                ind_d = elem.pos.index(3)
                while self.color_position[elem.colors[ind_wh - 1]] not in elem.pos:
                    self.D()
                if ind_d == ind_wh:
                    self.position_function_2[elem.pos[ind_wh - 1]]()
                else:
                    match elem.pos[ind_wh]:
                        case 2:
                            self.D()
                            self.R()
                            self.f()
                            self.r()
                        case 5:
                            self.D()
                            self.B()
                            self.r()
                            self.b()
                        case 0:
                            self.D()
                            self.L()
                            self.b()
                            self.l()
                        case 4:
                            self.D()
                            self.F()
                            self.l()
                            self.f()

    def first_two(self, elem):
        if 3 in elem.pos:
            ind_wh = elem.colors.index(6)
            ind_d = elem.pos.index(3)
            if ind_d == ind_wh:
                while elem.pos[ind_wh - 1] != self.color_position[elem.colors[ind_wh - 2]]:
                    self.D()
                pp = elem.pos[ind_wh - 2]
                self.position_function[pp]()
                self.D2()
                self.position_function_3[pp]()

    def first_finish_func(self, pos, elem, ind_wh):
        # print("first finish func", pos)
        while self.color_position[elem.colors[pos]] != elem.pos[pos]:
            self.D()
        pp = elem.pos[pos]
        if ind_wh != self.color_position[self.color_left[elem.colors[pos]]]:
            self.d()
            self.position_function_3[pp]()
            self.D()
            self.position_function[pp]()
        else:
            self.D()
            self.position_function[pp]()
            self.d()
            self.position_function_3[pp]()

    def first_finish(self, elem):
        # print("first_finish")
        if 3 in elem.pos:
            ind_wh = elem.colors.index(6)
            ind_d = elem.pos.index(3)
            if ind_d != ind_wh:
                match sorted([ind_wh, ind_d]):
                    case [0, 1]:
                        self.first_finish_func(2, elem, ind_wh)
                    case [1, 2]:
                        self.first_finish_func(0, elem, ind_wh)
                    case [0, 2]:
                        self.first_finish_func(1, elem, ind_wh)
                # print(elem.pos, elem.colors)

    def first_level(self):
        # print("first_level")
        self.cross()
        self.white_shape3 = []
        for elem in self.shape3:
            if 6 in elem.colors:
                self.white_shape3.append(elem)

        flag = True
        cnt = 0
        while flag:
            flag = False
            for elem in self.white_shape3:
                if 1 in elem.pos:
                    ind_wh = elem.colors.index(6)
                    ind_u = elem.pos.index(1)
                    if sorted([self.color_position[elem.colors[0]], self.color_position[elem.colors[1]],
                               self.color_position[elem.colors[2]]]) == sorted(elem.pos) and ind_u != ind_wh:
                        # print("in pos not presentation")
                        cnt += 1
                        flag = True
                        pp = elem.pos[ind_wh]
                        if self.color_left[elem.colors[ind_u]] == self.position_color[elem.pos[ind_wh]]:
                            self.position_function[pp]()
                            self.D()
                            self.position_function_3[pp]()
                        else:
                            self.position_function_3[pp]()
                            self.D()
                            self.position_function[pp]()
                    break
            if cnt == 2:
                self.D()
                cnt = 0
        flag = True
        while flag:
            flag = False
            for elem in self.white_shape3:
                if elem.pos != [self.color_position[elem.colors[0]], self.color_position[elem.colors[1]],
                                self.color_position[elem.colors[2]]]:
                    # print("not in pos retry")
                    flag = True
                    if 1 in elem.pos:
                        ind_wh = elem.colors.index(6)
                        ind_u = elem.pos.index(1)
                        if ind_u == ind_wh:
                            pp = elem.pos[ind_wh - 1]
                            pp2 = elem.pos[ind_wh - 2]
                            if self.color_left[elem.colors[ind_wh - 1]] != elem.colors[ind_wh - 2]:
                                # print("if")
                                self.position_function[pp]()
                                self.D()
                                self.position_function_3[pp]()
                            else:
                                # print("else")
                                self.position_function_3[pp2]()
                                self.D()
                                self.position_function[pp2]()
                        else:
                            pp = elem.pos[ind_wh]
                            if self.color_left[elem.colors[ind_u]] == self.position_color[elem.pos[ind_wh]]:
                                self.position_function[pp]()
                                self.D()
                                self.position_function_3[pp]()
                            else:
                                self.position_function_3[pp]()
                                self.D()
                                self.position_function[pp]()

                    self.first_two(elem)
                    self.first_finish(elem)

    def second_level(self):
        self.first_level()
        # print("second")
        self.second_shape = []
        for el in self.shape2:
            if 6 not in el.colors and 3 not in el.colors:
                self.second_shape.append(el)
        flag = True
        while flag:
            flag = False
            for elem in self.second_shape:
                if elem.pos != [self.color_position[elem.colors[0]], self.color_position[elem.colors[1]]]:
                    flag = True
                if 3 in elem.pos:
                    ind_d = elem.pos.index(3)
                    while elem.pos[ind_d - 1] != self.color_position[elem.colors[ind_d - 1]]:
                        # print(elem.pos[ind_d - 1], self.color_position[elem.colors[ind_d - 1]])
                        self.D()
                    if self.color_left[elem.colors[ind_d]] == elem.colors[ind_d - 1]:
                        # print(elem.pos, elem.colors)
                        pp = self.color_position[elem.colors[ind_d]]
                        pp2 = elem.pos[ind_d - 1]
                        self.d()
                        self.position_function_3[pp]()
                        self.D()
                        self.position_function[pp]()
                        self.D()
                        self.position_function[pp2]()
                        self.d()
                        self.position_function_3[pp2]()
                    else:
                        # print("else", elem.pos, elem.colors)
                        pp = self.color_position[elem.colors[ind_d]]
                        pp2 = elem.pos[ind_d - 1]
                        self.D()
                        self.position_function[pp]()
                        self.d()
                        self.position_function_3[pp]()
                        self.d()
                        self.position_function_3[pp2]()
                        self.D()
                        self.position_function[pp2]()
                    break
                if sorted(elem.pos) != sorted(
                        [self.color_position[elem.colors[0]], self.color_position[elem.colors[1]]]):
                    # print("hi", elem.pos, elem.colors, self.color_left[elem.colors[0]])
                    if self.position_left[elem.pos[0]] == elem.pos[1]:
                        # print("if")
                        pp = elem.pos[1]
                        pp2 = elem.pos[0]
                        self.D()
                        self.position_function[pp]()
                        self.d()
                        self.position_function_3[pp]()
                        self.d()
                        self.position_function_3[pp2]()
                        self.D()
                        self.position_function[pp2]()
                    else:
                        # print("else")
                        pp = elem.pos[0]
                        pp2 = elem.pos[1]
                        self.D()
                        self.position_function[pp]()
                        self.d()
                        self.position_function_3[pp]()
                        self.d()
                        self.position_function_3[pp2]()
                        self.D()
                        self.position_function[pp2]()
                    break
                if elem.pos != [self.color_position[elem.colors[0]], self.color_position[elem.colors[1]]]:
                    # print(elem.pos, elem.colors)
                    if self.color_left[elem.colors[0]] != elem.colors[1]:
                        pp = elem.pos[0]
                        pp2 = elem.pos[1]
                        self.d()
                        self.position_function_3[pp]()
                        self.D()
                        self.position_function[pp]()
                        self.D()
                        self.position_function[pp2]()
                        self.d()
                        self.position_function_3[pp2]()
                    else:
                        pp = elem.pos[0]
                        pp2 = elem.pos[1]
                        self.D()
                        self.position_function[pp]()
                        self.d()
                        self.position_function_3[pp]()
                        self.d()
                        self.position_function_3[pp2]()
                        self.D()
                        self.position_function[pp2]()

    def palka(self):
        # print("palka")
        self.L()
        self.D()
        self.l()
        self.d()
        self.l()
        self.F()
        self.L()
        self.f()

    def galka(self):
        # print("galka")
        self.F()
        self.L()
        self.d()
        self.l()
        self.d()
        self.L()
        self.D()
        self.l()
        self.f()

    def last_cross(self):
        # print("cross")
        pos_not_d_y = []
        for elem in self.yellow_shape2:
            if elem.colors[elem.pos.index(3)] != 3:
                pos_not_d_y.append(elem.pos[elem.pos.index(3) - 1])
        # print(pos_not_d_y)
        if len(pos_not_d_y) == 0:
            return
        if len(pos_not_d_y) == 4:
            self.palka()
            self.last_cross()
            return
        if sorted(pos_not_d_y) in [[0, 2], [4, 5]]:
            if self.shape2[8].pos[self.shape2[8].colors.index(3)] != 3:
                self.D()
            self.palka()
            self.last_cross()
            return

        while (self.shape2[7].pos[self.shape2[7].colors.index(3)] != 3 or
               self.shape2[5].pos[self.shape2[5].colors.index(3)] != 3):
            self.D()
        self.galka()
        self.last_cross()

    def last_shape3_d(self):
        # print("last_shape3_d")
        elem_d_y = []
        for elem in self.yellow_shape3:
            if elem.colors[elem.pos.index(3)] == 3:
                elem_d_y.append(elem)
        if len(elem_d_y) == 4:
            return
        if len(elem_d_y) == 1:
            while \
                    (
                            (self.shape3[6].pos[self.shape3[6].colors.index(3)] != 2
                             or
                             self.shape3[5].pos[self.shape3[5].colors.index(3)] != 3)
                            and
                            (self.shape3[5].pos[self.shape3[5].colors.index(3)] != 2
                             or
                             self.shape3[6].pos[self.shape3[6].colors.index(3)] != 3
                            )
                    ):
                self.D()
            if self.shape3[5].pos[self.shape3[5].colors.index(3)] == 3:
                self.kambria()
            else:
                self.kalibri()
            self.last_shape3_d()
            return
        if len(elem_d_y) == 0:
            while (self.shape3[6].pos[self.shape3[6].colors.index(3)] != 5 or
                   self.shape3[7].pos[self.shape3[7].colors.index(3)] != 5):
                self.D()
            self.kalibri()
            self.last_shape3_d()
            return
        while (self.shape3[6].pos[self.shape3[6].colors.index(3)] != 2):
            self.D()
        self.kalibri()
        self.last_shape3_d()

    def last_shape3(self):
        # print("last_shape3")
        cnt = [[0 for _ in range(6)] for i in range(6)]

        for elem in self.yellow_shape3:
            ind_y = elem.colors.index(3)
            cnt[elem.pos[ind_y - 1]][elem.colors[ind_y - 1]] += 1
            cnt[elem.pos[ind_y - 2]][elem.colors[ind_y - 2]] += 1
        count = 0
        ind = 0
        for i in range(len(cnt)):
            if 2 in cnt[i]:
                count += 1
                ind = i
        if count == 4:
            return
        if count == 1:
            match ind:
                case 2:
                    self.D()
                case 4:
                    self.D2()
                case 0:
                    self.d()
            self.palka()
            self.galka()
            self.last_shape3()
            return
        self.galka()
        self.palka()
        self.last_shape3()

    def kalibri(self):
        # print("kalibri")
        self.L()
        self.D()
        self.l()
        self.D()
        self.L()
        self.D()
        self.D()
        self.l()

    def kambria(self):
        # print("kambria")
        self.r()
        self.d()
        self.R()
        self.d()
        self.r()
        self.D()
        self.D()
        self.R()

    def finish(self):
        # print("finish")
        cnt = [[0 for _ in range(6)] for i in range(6)]

        for elem in self.yellow_shape3:
            ind_y = elem.colors.index(3)
            cnt[elem.pos[ind_y - 1]][elem.colors[ind_y - 1]] += 1
            cnt[elem.pos[ind_y - 2]][elem.colors[ind_y - 2]] += 1

        for elem in self.yellow_shape2:
            ind_y = elem.colors.index(3)
            cnt[elem.pos[ind_y - 1]][elem.colors[ind_y - 1]] += 1

        count = 0
        ind = 0
        for i in range(len(cnt)):
            if 3 in cnt[i]:
                count += 1
                ind = i
        if count == 4:
            return
        if count == 1:
            match ind:
                case 2:
                    self.D2()
                case 4:
                    self.d()
                case 5:
                    self.D()
            self.kalibri()
            self.D()
            self.kambria()
            self.finish()
            return
        self.kalibri()
        self.D()
        self.kambria()
        self.finish()

    def last_level(self):
        self.first_level()
        self.second_level()
        # print("last")
        self.yellow_shape2 = []
        self.yellow_shape3 = []
        for elem in self.shape2:
            if 3 in elem.colors:
                self.yellow_shape2.append(elem)
        for elem in self.shape3:
            if 3 in elem.colors:
                self.yellow_shape3.append(elem)
        self.last_cross()
        self.last_shape3_d()
        self.last_shape3()
        self.finish()
        while self.shape2[7].pos[self.shape2[7].colors.index(3) - 1] != self.color_position[
            self.shape2[7].colors[self.shape2[7].colors.index(3) - 1]]:
            self.D()