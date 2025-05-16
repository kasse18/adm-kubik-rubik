import kociemba.face as face
import threading as thr
import kociemba.cubie as cubie
import kociemba.symmetries as sy
import kociemba.coord as coord
from kociemba.enums import Move
import kociemba.moves as mv
import kociemba.pruning as pr
import time
from kociemba.defs import N_MOVE


class SolverThread(thr.Thread):

    def __init__(self, cb_cube, rot, inv, ret_length, timeout, start_time, solutions, terminated, shortest_length):
        thr.Thread.__init__(self)
        self.cb_cube = cb_cube
        self.co_cube = None
        self.rot = rot
        self.inv = inv
        self.sofar_phase1 = None
        self.sofar_phase2 = None
        self.phase2_done = False
        self.lock = thr.Lock()
        self.ret_length = ret_length
        self.timeout = timeout
        self.start_time = start_time

        self.cornersave = 0

        self.solutions = solutions
        self.terminated = terminated
        self.shortest_length = shortest_length

    def search_phase2(self, corners, ud_edges, slice_sorted, dist, togo_phase2):
        if self.terminated.is_set() or self.phase2_done:
            return
        if togo_phase2 == 0 and slice_sorted == 0:
            self.lock.acquire()
            man = self.sofar_phase1 + self.sofar_phase2
            if len(self.solutions) == 0 or (len(self.solutions[-1]) > len(man)):

                if self.inv == 1:
                    man = list(reversed(man))
                    man[:] = [Move((m // 3) * 3 + (2 - m % 3)) for m in man]
                man[:] = [Move(sy.conj_move[N_MOVE * 16 * self.rot + m]) for m in man]
                self.solutions.append(man)
                self.shortest_length[0] = len(man)

            if self.shortest_length[0] <= self.ret_length:
                self.terminated.set()
            self.lock.release()
            self.phase2_done = True
        else:
            for m in Move:
                if m in [Move.R1, Move.R3, Move.F1, Move.F3,
                         Move.L1, Move.L3, Move.B1, Move.B3]:
                    continue

                if len(self.sofar_phase2) > 0:
                    diff = self.sofar_phase2[-1] // 3 - m // 3
                    if diff in [0, 3]:
                        continue
                else:
                    if len(self.sofar_phase1) > 0:
                        diff = self.sofar_phase1[-1] // 3 - m // 3
                        if diff in [0, 3]:
                            continue

                corners_new = mv.corners_move[18 * corners + m]
                ud_edges_new = mv.ud_edges_move[18 * ud_edges + m]
                slice_sorted_new = mv.slice_sorted_move[18 * slice_sorted + m]

                classidx = sy.corner_classidx[corners_new]
                sym = sy.corner_sym[corners_new]
                dist_new_mod3 = pr.get_corners_ud_edges_depth3(
                    40320 * classidx + sy.ud_edges_conj[(ud_edges_new << 4) + sym])
                dist_new = pr.distance[3 * dist + dist_new_mod3]
                if max(dist_new, pr.cornslice_depth[24 * corners_new + slice_sorted_new]) >= togo_phase2:
                    continue

                self.sofar_phase2.append(m)
                self.search_phase2(corners_new, ud_edges_new, slice_sorted_new, dist_new, togo_phase2 - 1)
                self.sofar_phase2.pop(-1)

    def search(self, flip, twist, slice_sorted, dist, togo_phase1):
        if self.terminated.is_set():
            return
        if togo_phase1 == 0:  # phase 1 solved

            if time.monotonic() > self.start_time + self.timeout and len(self.solutions) > 0:
                self.terminated.set()

            if self.sofar_phase1:
                m = self.sofar_phase1[-1]
            else:
                m = Move.U1

            if m in [Move.R3, Move.F3, Move.L3, Move.B3]:
                corners = mv.corners_move[18 * self.cornersave + m - 1]
            else:
                corners = self.co_cube.corners
                for m in self.sofar_phase1:
                    corners = mv.corners_move[18 * corners + m]
                self.cornersave = corners

            togo2_limit = min(self.shortest_length[0] - len(self.sofar_phase1), 11)
            if pr.cornslice_depth[24 * corners + slice_sorted] >= togo2_limit:
                return

            u_edges = self.co_cube.u_edges
            d_edges = self.co_cube.d_edges
            for m in self.sofar_phase1:
                u_edges = mv.u_edges_move[18 * u_edges + m]
                d_edges = mv.d_edges_move[18 * d_edges + m]
            ud_edges = coord.u_edges_plus_d_edges_to_ud_edges[24 * u_edges + d_edges % 24]

            dist2 = self.co_cube.get_depth_phase2(corners, ud_edges)
            for togo2 in range(dist2, togo2_limit):
                self.sofar_phase2 = []
                self.phase2_done = False
                self.search_phase2(corners, ud_edges, slice_sorted, dist2, togo2)
                if self.phase2_done:
                    break

        else:
            for m in Move:
                if dist == 0 and togo_phase1 < 5 and m in [Move.U1, Move.U2, Move.U3, Move.R2,
                                                           Move.F2, Move.D1, Move.D2, Move.D3,
                                                           Move.L2, Move.B2]:
                    continue

                if len(self.sofar_phase1) > 0:
                    diff = self.sofar_phase1[-1] // 3 - m // 3
                    if diff in [0, 3]:
                        continue

                flip_new = mv.flip_move[18 * flip + m]
                twist_new = mv.twist_move[18 * twist + m]
                slice_sorted_new = mv.slice_sorted_move[18 * slice_sorted + m]

                flipslice = 2048 * (slice_sorted_new // 24) + flip_new
                classidx = sy.flipslice_classidx[flipslice]
                sym = sy.flipslice_sym[flipslice]
                dist_new_mod3 = pr.get_flipslice_twist_depth3(2187 * classidx + sy.twist_conj[(twist_new << 4) + sym])
                dist_new = pr.distance[3 * dist + dist_new_mod3]
                if dist_new >= togo_phase1:
                    continue

                self.sofar_phase1.append(m)
                self.search(flip_new, twist_new, slice_sorted_new, dist_new, togo_phase1 - 1)
                self.sofar_phase1.pop(-1)

    def run(self):
        cb = None
        if self.rot == 0:
            cb = cubie.CubieCube(self.cb_cube.cp, self.cb_cube.co, self.cb_cube.ep, self.cb_cube.eo)
        elif self.rot == 1:
            cb = cubie.CubieCube(sy.symCube[32].cp, sy.symCube[32].co, sy.symCube[32].ep, sy.symCube[32].eo)
            cb.multiply(self.cb_cube)
            cb.multiply(sy.symCube[16])
        elif self.rot == 2:
            cb = cubie.CubieCube(sy.symCube[16].cp, sy.symCube[16].co, sy.symCube[16].ep, sy.symCube[16].eo)
            cb.multiply(self.cb_cube)
            cb.multiply(sy.symCube[32])
        if self.inv == 1:
            tmp = cubie.CubieCube()
            cb.inv_cubie_cube(tmp)
            cb = tmp

        self.co_cube = coord.CoordCube(cb)

        dist = self.co_cube.get_depth_phase1()
        for togo1 in range(dist, 20):
            self.sofar_phase1 = []
            self.search(self.co_cube.flip, self.co_cube.twist, self.co_cube.slice_sorted, dist, togo1)


def solve(cubestring, max_length=20, timeout=3):
    fc = face.FaceCube()
    s = fc.from_string(cubestring)
    if s != cubie.CUBE_OK:
        return s
    cc = fc.to_cubie_cube()
    s = cc.verify()
    if s != cubie.CUBE_OK:
        return s

    my_threads = []
    s_time = time.monotonic()

    shortest_length = [999]
    solutions = []
    terminated = thr.Event()
    terminated.clear()
    syms = cc.symmetries()
    if len(list({16, 20, 24, 28} & set(syms))) > 0:
        tr = [0, 3]
    else:
        tr = range(6)
    if len(list(set(range(48, 96)) & set(syms))) > 0:
        tr = list(filter(lambda x: x < 3, tr))
    for i in tr:
        th = SolverThread(cc, i % 3, i // 3, max_length, timeout, s_time, solutions, terminated, shortest_length)
        my_threads.append(th)
        th.start()
    for t in my_threads:
        t.join()
    s = ''
    if len(solutions) > 0:
        for m in solutions[-1]:
            s += m.name + ' '
    return s + '(' + str(len(s) // 3) + 'f)'

def solveto(cubestring, goalstring, max_length=20, timeout=3):
    fc0 = face.FaceCube()
    fcg = face.FaceCube()
    s = fc0.from_string(cubestring)
    if s != cubie.CUBE_OK:
        return 'first cube ' + s
    s = fcg.from_string(goalstring)
    if s != cubie.CUBE_OK:
        return 'second cube ' + s
    cc0 = fc0.to_cubie_cube()
    s = cc0.verify()
    if s != cubie.CUBE_OK:
        return 'first cube ' + s
    ccg = fcg.to_cubie_cube()
    s = ccg.verify()
    if s != cubie.CUBE_OK:
        return 'second cube ' + s
    cc = cubie.CubieCube()
    ccg.inv_cubie_cube(cc)
    cc.multiply(cc0)

    my_threads = []
    s_time = time.monotonic()

    s_length = [999]
    solutions = []
    terminated = thr.Event()
    terminated.clear()
    syms = cc.symmetries()
    if len(list({16, 20, 24, 28} & set(syms))) > 0:
        tr = [0, 3]
    else:
        tr = range(6)
    if len(list(set(range(48, 96)) & set(syms))) > 0:
        tr = list(filter(lambda x: x < 3, tr))
    for i in tr:
        th = SolverThread(cc, i % 3, i // 3, max_length, timeout, s_time, solutions, terminated, [999])
        my_threads.append(th)
        th.start()
    for t in my_threads:
        t.join()
    s = ''
    if len(solutions) > 0:
        for m in solutions[-1]:
            s += m.name + ' '
    return s + '(' + str(len(s) // 3) + 'f)'
