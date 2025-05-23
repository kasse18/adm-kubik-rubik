import kociemba.defs as defs
import kociemba.enums as enums
import kociemba.moves as mv
import kociemba.symmetries as sy
import kociemba.cubie as cb
from os import path
import array as ar

uint32 = 'I' if ar.array('I').itemsize >= 4 else 'L'

flipslice_twist_depth3 = ar.array(uint32)
corners_ud_edges_depth3 = ar.array(uint32)
cornslice_depth = None
edgeslice_depth = None


def get_flipslice_twist_depth3(ix):
    y = flipslice_twist_depth3[ix // 16]
    y >>= (ix % 16) * 2
    return y & 3


def get_corners_ud_edges_depth3(ix):
    y = corners_ud_edges_depth3[ix // 16]
    y >>= (ix % 16) * 2
    return y & 3


def set_flipslice_twist_depth3(ix, value):
    shift = (ix % 16) * 2
    base = ix >> 4
    flipslice_twist_depth3[base] &= ~(3 << shift) & 0xffffffff
    flipslice_twist_depth3[base] |= value << shift


def set_corners_ud_edges_depth3(ix, value):
    shift = (ix % 16) * 2
    base = ix >> 4
    corners_ud_edges_depth3[base] &= ~(3 << shift) & 0xffffffff
    corners_ud_edges_depth3[base] |= value << shift

def create_phase1_prun_table():
    global flipslice_twist_depth3
    total = defs.N_FLIPSLICE_CLASS * defs.N_TWIST
    fname = "phase1_prun"
    if not path.isfile(path.join(defs.FOLDER, fname)):
        print("Создание " + fname + " таблицы...")
        print('Это может занять длительное время, скорость зависит от конфигурации ПК')

        flipslice_twist_depth3 = ar.array(uint32, [0xffffffff] * (total // 16 + 1))

        cc = cb.CubieCube()
        fs_sym = ar.array('H', [0] * defs.N_FLIPSLICE_CLASS)
        for i in range(defs.N_FLIPSLICE_CLASS):
            if (i + 1) % 1000 == 0:
                print('.', end='', flush=True)
            rep = sy.flipslice_rep[i]
            cc.set_slice(rep // defs.N_FLIP)
            cc.set_flip(rep % defs.N_FLIP)

            for s in range(defs.N_SYM_D4h):
                ss = cb.CubieCube(sy.symCube[s].cp, sy.symCube[s].co, sy.symCube[s].ep,
                                  sy.symCube[s].eo)  # copy cube
                ss.edge_multiply(cc)  # s*cc
                ss.edge_multiply(sy.symCube[sy.inv_idx[s]])  # s*cc*s^-1
                if ss.get_slice() == rep // defs.N_FLIP and ss.get_flip() == rep % defs.N_FLIP:
                    fs_sym[i] |= 1 << s
        print()

        fs_classidx = 0
        twist = 0
        set_flipslice_twist_depth3(defs.N_TWIST * fs_classidx + twist, 0)
        done = 1
        depth = 0
        backsearch = False
        print('depth:', depth, 'done: ' + str(done) + '/' + str(total))
        while done != total:
            depth3 = depth % 3
            if depth == 9:
                print('backwards search...')
                backsearch = True
            if depth < 8:
                mult = 5
            else:
                mult = 1
            idx = 0
            for fs_classidx in range(defs.N_FLIPSLICE_CLASS):
                if (fs_classidx + 1) % (200 * mult) == 0:
                    print('.', end='', flush=True)
                if (fs_classidx + 1) % (16000 * mult) == 0:
                    print('')

                twist = 0
                while twist < defs.N_TWIST:

                    if not backsearch and idx % 16 == 0 and flipslice_twist_depth3[idx // 16] == 0xffffffff \
                            and twist < defs.N_TWIST - 16:
                        twist += 16
                        idx += 16
                        continue

                    if backsearch:
                        match = (get_flipslice_twist_depth3(idx) == 3)
                    else:
                        match = (get_flipslice_twist_depth3(idx) == depth3)

                    if match:
                        flipslice = sy.flipslice_rep[fs_classidx]
                        flip = flipslice % 2048
                        slice_ = flipslice >> 11
                        for m in enums.Move:
                            twist1 = mv.twist_move[18 * twist + m]
                            flip1 = mv.flip_move[18 * flip + m]
                            slice1 = mv.slice_sorted_move[432 * slice_ + m] // 24
                            flipslice1 = (slice1 << 11) + flip1
                            fs1_classidx = sy.flipslice_classidx[flipslice1]
                            fs1_sym = sy.flipslice_sym[flipslice1]
                            twist1 = sy.twist_conj[(twist1 << 4) + fs1_sym]
                            idx1 = 2187 * fs1_classidx + twist1
                            if not backsearch:
                                if get_flipslice_twist_depth3(idx1) == 3:
                                    set_flipslice_twist_depth3(idx1, (depth + 1) % 3)
                                    done += 1
                                    sym = fs_sym[fs1_classidx]
                                    if sym != 1:
                                        for k in range(1, 16):
                                            sym >>= 1
                                            if sym % 2 == 1:
                                                twist2 = sy.twist_conj[(twist1 << 4) + k]
                                                idx2 = 2187 * fs1_classidx + twist2
                                                if get_flipslice_twist_depth3(idx2) == 3:
                                                    set_flipslice_twist_depth3(idx2, (depth + 1) % 3)
                                                    done += 1

                            else:
                                if get_flipslice_twist_depth3(idx1) == depth3:
                                    set_flipslice_twist_depth3(idx, (depth + 1) % 3)
                                    done += 1
                                    break
                    twist += 1
                    idx += 1

            depth += 1
            print()
            print('depth:', depth, 'done: ' + str(done) + '/' + str(total))

        fh = open(path.join(defs.FOLDER, fname), "wb")
        flipslice_twist_depth3.tofile(fh)
    else:
        print("загрузка " + fname + " таблицы")
        fh = open(path.join(defs.FOLDER, fname), "rb")
        flipslice_twist_depth3 = ar.array(uint32)
        flipslice_twist_depth3.fromfile(fh, total // 16 + 1)
    fh.close()


def create_phase2_prun_table():
    total = defs.N_CORNERS_CLASS * defs.N_UD_EDGES
    fname = "phase2_prun"
    global corners_ud_edges_depth3
    if not path.isfile(path.join(defs.FOLDER, fname)):
        print("создание " + fname + " таблицы")

        corners_ud_edges_depth3 = ar.array(uint32, [0xffffffff] * (total // 16))
        cc = cb.CubieCube()
        c_sym = ar.array('H', [0] * defs.N_CORNERS_CLASS)
        for i in range(defs.N_CORNERS_CLASS):
            if (i + 1) % 1000 == 0:
                print('.', end='', flush=True)
            rep = sy.corner_rep[i]
            cc.set_corners(rep)
            for s in range(defs.N_SYM_D4h):
                ss = cb.CubieCube(sy.symCube[s].cp, sy.symCube[s].co, sy.symCube[s].ep,
                                  sy.symCube[s].eo)
                ss.corner_multiply(cc)
                ss.corner_multiply(sy.symCube[sy.inv_idx[s]])
                if ss.get_corners() == rep:
                    c_sym[i] |= 1 << s
        print()

        c_classidx = 0
        ud_edge = 0
        set_corners_ud_edges_depth3(defs.N_UD_EDGES * c_classidx + ud_edge, 0)
        done = 1
        depth = 0
        print('depth:', depth, 'done: ' + str(done) + '/' + str(total))
        while depth < 10:
            depth3 = depth % 3
            idx = 0
            mult = 2
            if depth > 9:
                mult = 1
            for c_classidx in range(defs.N_CORNERS_CLASS):
                if (c_classidx + 1) % (20 * mult) == 0:
                    print('.', end='', flush=True)
                if (c_classidx + 1) % (1600 * mult) == 0:
                    print('')

                ud_edge = 0
                while ud_edge < defs.N_UD_EDGES:

                    if idx % 16 == 0 and corners_ud_edges_depth3[idx // 16] == 0xffffffff \
                            and ud_edge < defs.N_UD_EDGES - 16:
                        ud_edge += 16
                        idx += 16
                        continue

                    if get_corners_ud_edges_depth3(idx) == depth3:
                        corner = sy.corner_rep[c_classidx]
                        for m in (enums.Move.U1, enums.Move.U2, enums.Move.U3, enums.Move.R2, enums.Move.F2,
                                  enums.Move.D1, enums.Move.D2, enums.Move.D3, enums.Move.L2, enums.Move.B2):
                            ud_edge1 = mv.ud_edges_move[18 * ud_edge + m]
                            corner1 = mv.corners_move[18 * corner + m]
                            c1_classidx = sy.corner_classidx[corner1]
                            c1_sym = sy.corner_sym[corner1]
                            ud_edge1 = sy.ud_edges_conj[(ud_edge1 << 4) + c1_sym]
                            idx1 = 40320 * c1_classidx + ud_edge1  # N_UD_EDGES = 40320
                            if get_corners_ud_edges_depth3(idx1) == 3:  # entry not yet filled
                                set_corners_ud_edges_depth3(idx1, (depth + 1) % 3)  # depth + 1 <= 10
                                done += 1
                                sym = c_sym[c1_classidx]
                                if sym != 1:
                                    for k in range(1, 16):
                                        sym >>= 1
                                        if sym % 2 == 1:
                                            ud_edge2 = sy.ud_edges_conj[(ud_edge1 << 4) + k]
                                            # c1_classidx does not change
                                            idx2 = 40320 * c1_classidx + ud_edge2
                                            if get_corners_ud_edges_depth3(idx2) == 3:
                                                set_corners_ud_edges_depth3(idx2, (depth + 1) % 3)
                                                done += 1

                    ud_edge += 1
                    idx += 1

            depth += 1
            print()
            print('depth:', depth, 'done: ' + str(done) + '/' + str(total))

        fh = open(path.join(defs.FOLDER, fname), "wb")
        corners_ud_edges_depth3.tofile(fh)
    else:
        print("loading " + fname + " table...")
        fh = open(path.join(defs.FOLDER, fname), "rb")
        corners_ud_edges_depth3 = ar.array(uint32)
        corners_ud_edges_depth3.fromfile(fh, total // 16)

    fh.close()


def create_phase2_cornsliceprun_table():
    fname = "phase2_cornsliceprun"
    global cornslice_depth
    if not path.isfile(path.join(defs.FOLDER, fname)):
        print("Создание " + fname + " таблицы")
        cornslice_depth = ar.array('b', [-1] * (defs.N_CORNERS * defs.N_PERM_4))
        corners = 0
        slice_ = 0
        cornslice_depth[defs.N_PERM_4 * corners + slice_] = 0
        done = 1
        depth = 0
        while done != defs.N_CORNERS * defs.N_PERM_4:
            for corners in range(defs.N_CORNERS):
                for slice_ in range(defs.N_PERM_4):
                    if cornslice_depth[defs.N_PERM_4 * corners + slice_] == depth:
                        for m in (enums.Move.U1, enums.Move.U2, enums.Move.U3, enums.Move.R2, enums.Move.F2,
                                  enums.Move.D1, enums.Move.D2, enums.Move.D3, enums.Move.L2, enums.Move.B2):
                            corners1 = mv.corners_move[18 * corners + m]
                            slice_1 = mv.slice_sorted_move[18 * slice_ + m]
                            idx1 = defs.N_PERM_4 * corners1 + slice_1
                            if cornslice_depth[idx1] == -1:  # entry not yet filled
                                cornslice_depth[idx1] = depth + 1
                                done += 1
                                if done % 20000 == 0:
                                    print('.', end='', flush=True)

            depth += 1
        print()
        fh = open(path.join(defs.FOLDER, fname), "wb")
        cornslice_depth.tofile(fh)
    else:
        print("загрузка " + fname + " таблицы")
        fh = open(path.join(defs.FOLDER, fname), "rb")
        cornslice_depth = ar.array('b')
        cornslice_depth.fromfile(fh, defs.N_CORNERS * defs.N_PERM_4)
    fh.close()

distance = ar.array('b', [0 for i in range(60)])
for i in range(20):
    for j in range(3):
        distance[3*i + j] = (i // 3) * 3 + j
        if i % 3 == 2 and j == 0:
            distance[3 * i + j] += 3
        elif i % 3 == 0 and j == 2:
            distance[3 * i + j] -= 3

create_phase1_prun_table()
create_phase2_prun_table()
create_phase2_cornsliceprun_table()
