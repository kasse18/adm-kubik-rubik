from os import path
import array as ar
import kociemba.cubie as cb
import kociemba.enums as enums
from kociemba.defs import FOLDER, N_TWIST, N_FLIP, N_SLICE_SORTED, N_CORNERS, N_UD_EDGES, N_MOVE

a = cb.CubieCube()

fname = "move_twist"
if not path.isfile(path.join(FOLDER, fname)):
    print("creating " + fname + " table...")
    twist_move = ar.array('H', [0 for i in range(N_TWIST * N_MOVE)])
    for i in range(N_TWIST):
        a.set_twist(i)
        for j in enums.Color:
            for k in range(3):
                a.corner_multiply(cb.basicMoveCube[j])
                twist_move[N_MOVE * i + 3 * j + k] = a.get_twist()
            a.corner_multiply(cb.basicMoveCube[j])
    fh = open(path.join(FOLDER, fname), "wb")
    twist_move.tofile(fh)
else:
    print("loading " + fname + " table...")
    fh = open(path.join(FOLDER, fname), "rb")
    twist_move = ar.array('H')
    twist_move.fromfile(fh, N_TWIST * N_MOVE)
fh.close()

fname = "move_flip"
if not path.isfile(path.join(FOLDER, fname)):
    print("creating " + fname + " table...")
    flip_move = ar.array('H', [0 for i in range(N_FLIP * N_MOVE)])
    for i in range(N_FLIP):
        a.set_flip(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                flip_move[N_MOVE * i + 3 * j + k] = a.get_flip()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(path.join(FOLDER, fname), "wb")
    flip_move.tofile(fh)
else:
    print("loading " + fname + " table...")
    fh = open(path.join(FOLDER, fname), "rb")
    flip_move = ar.array('H')
    flip_move.fromfile(fh, N_FLIP * N_MOVE)
fh.close()

fname = "move_slice_sorted"
if not path.isfile(path.join(FOLDER, fname)):
    print("creating " + fname + " table...")
    slice_sorted_move = ar.array('H', [0 for i in range(N_SLICE_SORTED * N_MOVE)])
    for i in range(N_SLICE_SORTED):
        if i % 200 == 0:
            print('.', end='', flush=True)
        a.set_slice_sorted(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                slice_sorted_move[N_MOVE * i + 3 * j + k] = a.get_slice_sorted()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(path.join(FOLDER, fname), "wb")
    slice_sorted_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(path.join(FOLDER, fname), "rb")
    slice_sorted_move = ar.array('H')
    slice_sorted_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()

fname = "move_u_edges"
if not path.isfile(path.join(FOLDER, fname)):
    print("creating " + fname + " table...")
    u_edges_move = ar.array('H', [0 for i in range(N_SLICE_SORTED * N_MOVE)])
    for i in range(N_SLICE_SORTED):
        if i % 200 == 0:
            print('.', end='', flush=True)
        a.set_u_edges(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                u_edges_move[N_MOVE * i + 3 * j + k] = a.get_u_edges()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(path.join(FOLDER, fname), "wb")
    u_edges_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(path.join(FOLDER, fname), "rb")
    u_edges_move = ar.array('H')
    u_edges_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()

fname = "move_d_edges"
if not path.isfile(path.join(FOLDER, fname)):
    print("creating " + fname + " table...")
    d_edges_move = ar.array('H', [0 for i in range(N_SLICE_SORTED * N_MOVE)])
    for i in range(N_SLICE_SORTED):
        if i % 200 == 0:
            print('.', end='', flush=True)
        a.set_d_edges(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                d_edges_move[N_MOVE * i + 3 * j + k] = a.get_d_edges()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(path.join(FOLDER, fname), "wb")
    d_edges_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(path.join(FOLDER, fname), "rb")
    d_edges_move = ar.array('H')
    d_edges_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()

fname = "move_ud_edges"
if not path.isfile(path.join(FOLDER, fname)):
    print("creating " + fname + " table...")
    ud_edges_move = ar.array('H', [0 for i in range(N_UD_EDGES * N_MOVE)])
    for i in range(N_UD_EDGES):
        if (i+1) % 600 == 0:
            print('.', end='', flush=True)
        if (i+1) % 48000 == 0:
            print('')
        a.set_ud_edges(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                if j in [enums.Color.R, enums.Color.F, enums.Color.L, enums.Color.B] and k != 1:
                    continue
                ud_edges_move[N_MOVE * i + 3 * j + k] = a.get_ud_edges()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(path.join(FOLDER, fname), "wb")
    ud_edges_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(path.join(FOLDER, fname), "rb")
    ud_edges_move = ar.array('H')
    ud_edges_move.fromfile(fh, N_UD_EDGES * N_MOVE)
fh.close()

fname = "move_corners"
if not path.isfile(path.join(FOLDER, fname)):
    print("creating " + fname + " table...")
    corners_move = ar.array('H', [0 for i in range(N_CORNERS * N_MOVE)])
    for i in range(N_CORNERS):
        if (i+1) % 200 == 0:
            print('.', end='', flush=True)
        if(i+1) % 16000 == 0:
            print('')
        a.set_corners(i)
        for j in enums.Color:
            for k in range(3):
                a.corner_multiply(cb.basicMoveCube[j])
                corners_move[N_MOVE * i + 3 * j + k] = a.get_corners()
            a.corner_multiply(cb.basicMoveCube[j])
    fh = open(path.join(FOLDER, fname), "wb")
    corners_move.tofile(fh)
    fh.close()
    print()
else:
    print("loading " + fname + " table...")
    fh = open(path.join(FOLDER, fname), "rb")
    corners_move = ar.array('H')
    corners_move.fromfile(fh, N_CORNERS * N_MOVE)
fh.close()
