# import pygame
import pprint
import random
import sys
import time
import kociemba
from kociemba.solver import solve as kociemba_solve
import pygame
import const as c
from draw.draw import Board
from shape.cube import Cube

from PyQt5.QtWidgets import QApplication, QWidget

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Mywidget(QWidget):
    pass


def draw_move_counter(screen, font, count):
    text = font.render(f"Moves: {count}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


if __name__ == '__main__':
    pygame.init()
    cube = Cube(pygame)
    sys.excepthook = except_hook
    app = QApplication([])
    wid = Mywidget()

    size = (c.W * c.size + c.size * 2 + 4, c.H * c.size + 4)
    board = Board(c.W, c.H, cube)
    screen = pygame.display.set_mode(size)
    board.set_view(screen, 5, 5, c.size)
    pprint.pprint(board.board)
    board.full()
    board.cube.render()
    running = True

    font = pygame.font.Font(None, 36)

    while running:

        screen.fill((0, 0, 0), (0, 0, 200, 40))
        draw_move_counter(screen, font, cube.move_count)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                print(board.get_click(event.pos))
                board.render()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                for i in range(random.randint(10, 30)):
                    board.Shuffle()

                pprint.pprint(board.board)
                pprint.pprint(board.cube.cube)
                print("shapes 3")
                colors = [elem.colors for elem in board.cube.shape3]
                colors.sort()
                for color in colors:
                    print(color)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                board.ShuffleBase(pygame)
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_r:
                        board.cube.R()
                    case pygame.K_u:
                        board.cube.U()
                    case pygame.K_d:
                        board.cube.D()
                    case pygame.K_l:
                        board.cube.L()
                    case pygame.K_f:
                        board.cube.F()
                    case pygame.K_b:
                        board.cube.B()
                    case pygame.K_c:
                        board.cube.cross()
                    case pygame.K_q:
                        cube.reset_move_count()
                        board.cube.render()
                        print(board.cube.cube)
                        pprint.pprint(board.board)
                        board.cube.last_level()
                        print(board.cube.check())
                    case pygame.K_m:
                        board.problem()
                    case pygame.K_n:
                        board.cube.R()
                        board.cube.R()
                        board.cube.D()
                        board.cube.R()
                        board.cube.R()
                        board.cube.F()
                        board.cube.F()
                        board.cube.d()
                        board.cube.u()
                        board.cube.F()
                        board.cube.F()
                        board.cube.U()
                        board.cube.L()
                        board.cube.L()
                        board.cube.u()
                        board.cube.R2()
                        board.cube.f()
                        board.cube.L()
                        board.cube.U()
                        board.cube.F()
                        board.cube.R2()
                        board.cube.u()
                        board.cube.B()
                        board.cube.l()
                        board.cube.U2()
                        board.cube.f()
                    case pygame.K_p:
                        board.cube.r()
                        board.cube.D()
                        board.cube.R()
                        board.cube.D()
                        board.cube.F()
                        board.cube.d()
                        board.cube.f()
                        board.cube.d()
                        board.cube.L()
                        board.cube.d()
                        board.cube.l()
                        board.cube.d()
                        board.cube.f()
                        board.cube.D()
                        board.cube.F()
                        board.cube.D()
                        board.cube.r()
                        board.cube.D()
                        board.cube.R()
                        board.cube.D()
                        board.cube.F()
                        board.cube.d()
                        board.cube.f()
                    case pygame.K_i:
                        board.cube.r()
                        board.cube.D()
                        board.cube.R()
                        board.cube.D()
                        board.cube.F()
                        board.cube.d()
                        board.cube.f()
                        board.cube.D()
                        board.cube.D()
                        board.cube.b()
                        board.cube.D()
                        board.cube.B()
                        board.cube.D()
                        board.cube.R()
                        board.cube.d()
                        board.cube.R()
                        board.cube.R()
                        board.cube.D()
                        board.cube.R()
                        board.cube.D()
                        board.cube.F()
                        board.cube.d()
                        board.cube.f()
                    case pygame.K_w:
                        board.cube.r()
                        board.cube.d()
                        board.cube.R()
                        board.cube.D()
                        board.cube.D()
                        board.cube.l()
                        board.cube.D()
                        board.cube.L()
                        board.cube.d()
                        board.cube.F()
                        board.cube.d()
                        board.cube.f()
                    case pygame.K_t:
                        for j in range(100):
                            for i in range(random.randint(10, 20)):
                                board.Shuffle()
                            cube_test = board.cube.cube
                            board.cube.last_level()
                            print(j, board.cube.check())
                            if not board.cube.check():
                                pprint.pprint(cube_test)
                                board.cube.last_level()
                                print(j, board.cube.check())
                                if not board.cube.check():
                                    break
                            time.sleep(3)

                    case pygame.K_k:
                        try:
                            cube.reset_move_count()
                            state = cube.get_kociemba_state()
                            print(f"Состояние куба:\n{state}")

                            if any(c not in {'U', 'R', 'F', 'D', 'L', 'B'} for c in state):
                                invalid = set(state) - {'U', 'R', 'F', 'D', 'L', 'B'}
                                raise ValueError(f"Недопустимые символы: {invalid}")

                            solution = kociemba_solve(state)
                            print(f"Решение: {solution}")
                            cube.execute_algorithm(solution)

                        except Exception as e:
                            print(f"Ошибка: {str(e)}")

            if event.type == pygame.QUIT:
                running = False
            board.cube.render()
    pygame.quit()
