class KociembaSolver:
    def __init__(self, cubestring):
        if len(cubestring) != 54:
            raise ValueError("Некорректная длина строки состояния (должна быть 54 символа)")
        self.cubestring = cubestring
        self._validate_cubestring()

        # Таблицы предвычислений
        self.phase1_table = {}
        self.phase2_table = {}
        self._generate_tables()

    def _validate_cubestring(self):
        """Проверка символов в строке состояния"""
        valid_chars = {'U', 'D', 'F', 'B', 'L', 'R'}
        for c in self.cubestring:
            if c not in valid_chars:
                raise ValueError(f"Недопустимый символ: {c}")

    def _generate_tables(self):
        """Генерация таблиц предвычислений"""
        self._generate_phase1_table()
        self._generate_phase2_table()

    def _generate_phase1_table(self):
        """Генерация таблицы для фазы 1"""
        # Пример: BFS от целевого состояния фазы 1
        target = self._phase1_target()
        queue = deque([(target, [])])
        self.phase1_table[target] = []

        while queue:
            state, moves = queue.popleft()
            for move in self._phase1_moves():
                new_state = self._apply_phase1_move(state, move)
                if new_state not in self.phase1_table:
                    self.phase1_table[new_state] = moves + [move]
                    queue.append((new_state, moves + [move]))

    def _phase1_target(self):
        """Целевое состояние фазы 1 (ориентация ребер + углы)"""
        return "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    def _phase1_moves(self):
        """Допустимые ходы для фазы 1"""
        return ['U', 'D', 'L', 'R', 'F', 'B', 'U2', 'D2', 'L2', 'R2', 'F2', 'B2']

    def _create_phase1_target_state(self):
        """Кодирование целевого состояния фазы 1"""
        # Формат: [ориентация 12 ребер] + [позиции 8 углов]
        return tuple([0] * 12 + list(range(8)))

    def _apply_phase1_move(self, state, move):
        """Применение хода к состоянию фазы 1"""
        # Реализация вращения грани (пример для U)
        if move == 'U':
            new_state = (
                state[6] + state[3] + state[0] +
                state[7] + state[4] + state[1] +
                state[8] + state[5] + state[2] +
                state[9:18] +  # F, R, B, L
                state[18:45] + # D
                state[45:]     # Остальные грани
            )
        # ... аналогично для других ходов ...
        return new_state

    def _generate_phase2_table(self):
        """Генерация таблицы для фазы 2"""
        target = self._phase2_target()
        queue = deque([(target, [])])
        self.phase2_table[target] = []

        while queue:
            state, moves = queue.popleft()
            for move in self._phase2_moves():
                new_state = self._apply_phase2_move(state, move)
                if new_state not in self.phase2_table:
                    self.phase2_table[new_state] = moves + [move]
                    queue.append((new_state, moves + [move]))

    def _phase2_target(self):
        """Целевое состояние фазы 2 (полностью собранный куб)"""
        return "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    def _phase2_moves(self):
        """Допустимые ходы для фазы 2"""
        return ['U', 'D', 'R2', 'L2', 'F2', 'B2']

    def _create_phase2_target_state(self):
        """Кодирование целевого состояния фазы 2"""
        # Формат: [позиции 8 углов] + [позиции 4 ребер U/D]
        return tuple(list(range(8)) + [0] * 4)

    def _apply_phase2_move(self, state, move):
        """Применение хода к состоянию фазы 2"""
        corner_pos, edge_pos = state[:8], state[8:]

        # Обновление позиций углов
        new_corner_pos = self._update_corner_positions(corner_pos, move)

        # Обновление позиций ребер
        new_edge_pos = self._update_edge_positions(edge_pos, move)

        return tuple(new_corner_pos + new_edge_pos)

    # Вспомогательные методы преобразования состояний
    def _update_edge_orientation(self, ori, move):
        """Обновление ориентации ребер"""
        # Реализация зависит от конкретного хода
        return ori  # Заглушка

    def _update_corner_positions(self, pos, move):
        """Обновление позиций углов"""
        # Реализация перестановок углов
        return pos  # Заглушка

    def _update_edge_positions(self, pos, move):
        """Обновление позиций ребер"""
        # Реализация перестановок ребер
        return pos  # Заглушка

    def solve(self):
        """Основной метод решения"""
        # Фаза 1: Поиск пути до промежуточного состояния
        phase1_solution = self._phase1_bfs()

        # Фаза 2: Поиск пути до полной сборки
        phase2_solution = self._phase2_bfs()

        return phase1_solution + phase2_solution

    def _phase1_bfs(self):
        # Поиск в ширину для фазы 1
        queue = deque([(self.cube.get_state(), [])])
        visited = set()

        while queue:
            state, moves = queue.popleft()

            if self._is_phase1_solved(state):
                return moves

            for move in self._get_phase1_moves():
                new_state = self._apply_move(state, move)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, moves + [move]))

        return []

    def _phase2_bfs(self):
        """Поиск в ширину для фазы 2"""
        queue = deque([(self.cube.get_state(), [])])
        visited = set()
        phase2_moves = ['U', 'D', 'R2', 'L2', 'F2', 'B2']

        while queue:
            state, moves = queue.popleft()

            if self._is_solved(state):
                return moves

            for move in phase2_moves:
                new_state = self._apply_move(state, move)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, moves + [move]))

        return []

    def _is_phase1_solved(self, state):
        """Проверка условий завершения фазы 1"""
        # 1. Проверка ориентации ребер (все ребра правильно ориентированы)
        edges = [
            state[1], state[3], state[5], state[7],  # U-рёбра
            state[46], state[50], state[52],  # D-рёбра
            state[10], state[14], state[19], state[23],  # E-слой
        ]

        # Цвета центров для проверки ориентации
        centers = {'U': 'U', 'D': 'D', 'F': 'F', 'B': 'B', 'L': 'L', 'R': 'R'}

        # Проверка ориентации каждого ребра
        for edge in edges:
            color1, color2 = edge
            if (color1 not in centers or color2 not in centers):
                return False
            if (centers[color1] not in ['U', 'D'] and
                    centers[color2] not in ['U', 'D']):
                return False

        # 2. Проверка четности угловых перестановок
        corner_coords = [0, 2, 6, 8, 9, 11, 15, 17]
        corners = [state[i] for i in corner_coords]
        return self._check_corner_parity(corners)

    def _check_corner_parity(self, corners):
        """Проверка четности угловых перестановок"""
        # Алгоритм подсчета инверсий
        inversions = 0
        for i in range(len(corners)):
            for j in range(i + 1, len(corners)):
                if corners[i] > corners[j]:
                    inversions += 1
        return inversions % 2 == 0

    def _get_phase1_moves(self):
        # Допустимые ходы для фазы 1
        return ['U', 'D', 'L', 'R', 'F', 'B',
                'U2', 'D2', 'L2', 'R2', 'F2', 'B2']

    def _apply_move(self, state, move):
        """Применение хода к состоянию куба"""
        # Преобразование строки состояния в матрицу
        cube = self._string_to_cube(state)

        # Определение типа вращения
        face = move[0]
        turns = 1 if len(move) == 1 else 2 if move[1] == '2' else -1

        # Применение вращения
        rotated = self._rotate_face(cube, face, turns)
        return self._cube_to_string(rotated)

    def _rotate_face(self, cube, face, turns):
        """Вращение грани куба"""
        # Маппинг граней
        face_idx = {'U': 0, 'D': 1, 'F': 2, 'B': 3, 'L': 4, 'R': 5}[face]
        new_face = [row[:] for row in cube[face_idx]]

        # Поворот матрицы 3x3
        if turns == 1:
            new_face = list(zip(*new_face[::-1]))  # CW
        elif turns == -1:
            new_face = list(zip(*new_face))[::-1]  # CCW
        else:
            new_face = [row[::-1] for row in new_face[::-1]]  # 180

        # Обновление смежных граней
        # ... (реализация перемещения краевых элементов) ...

        return cube

    def _string_to_cube(self, s):
        """Преобразование строки в 3D матрицу"""
        return [list(s[i * 9:i * 9 + 9]) for i in range(6)]

    def _cube_to_string(self, cube):
        return ''.join([''.join(row) for face in cube for row in face])

    def _is_solved(self, state):
        """Проверка полностью собранного состояния"""
        solved = [
            'UUUUUUUUU',  # U
            'RRRRRRRRR',  # R
            'FFFFFFFFF',  # F
            'DDDDDDDDD',  # D
            'LLLLLLLLL',  # L
            'BBBBBBBBB'  # B
        ]
        return all(face in state for face in solved)


# class Cube:
#     def __init__(self):
#         # Инициализация куба в собранном состоянии
#         self.state = [
#             [['W'] * 3 for _ in range(3)],  # Up
#             [['Y'] * 3 for _ in range(3)],  # Down
#             [['R'] * 3 for _ in range(3)],  # Front
#             [['O'] * 3 for _ in range(3)],  # Back
#             [['G'] * 3 for _ in range(3)],  # Left
#             [['B'] * 3 for _ in range(3)]  # Right
#         ]
#
#     def get_state(self):
#         # Возвращает строковое представление состояния
#         return ''.join([''.join(row) for face in self.state for row in face])
#
#     def apply_moves(self, moves):
#         # Применение последовательности ходов
#         for move in moves:
#             self._rotate(move)
#
#     def _rotate(self, move):
#         # Реализация вращения грани
#         pass
#
#
# # Пример использования
# cube = Cube()
# solver = KociembaSolver(cube)
# cube.apply_moves(["R", "U", "R'", "U'"])  # Перемешать
# solution = solver.solve()
# print("Решение:", ' '.join(solution))