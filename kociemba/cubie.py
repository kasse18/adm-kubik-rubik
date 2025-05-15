from kociemba.defs import cornerFacelet, edgeFacelet, cornerColor, edgeColor, N_SYM
from kociemba.enums import Color, Corner as Co, Edge as Ed
import kociemba.face as face
from kociemba.misc import c_nk, rotate_left, rotate_right


# U-move
cpU = [Co.UBR, Co.URF, Co.UFL, Co.ULB, Co.DFR, Co.DLF, Co.DBL, Co.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Ed.UB, Ed.UR, Ed.UF, Ed.UL, Ed.DR, Ed.DF, Ed.DL, Ed.DB, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# R-move
cpR = [Co.DFR, Co.UFL, Co.ULB, Co.URF, Co.DRB, Co.DLF, Co.DBL, Co.UBR]  # permutation of the corners
coR = [2, 0, 0, 1, 1, 0, 0, 2]  # changes of the orientations of the corners
epR = [Ed.FR, Ed.UF, Ed.UL, Ed.UB, Ed.BR, Ed.DF, Ed.DL, Ed.DB, Ed.DR, Ed.FL, Ed.BL, Ed.UR]  # permutation of the edges
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # changes of the permutations of the edges

# F-move
cpF = [Co.UFL, Co.DLF, Co.ULB, Co.UBR, Co.URF, Co.DFR, Co.DBL, Co.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Ed.UR, Ed.FL, Ed.UL, Ed.UB, Ed.DR, Ed.FR, Ed.DL, Ed.DB, Ed.UF, Ed.DF, Ed.BL, Ed.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# D-move
cpD = [Co.URF, Co.UFL, Co.ULB, Co.UBR, Co.DLF, Co.DBL, Co.DRB, Co.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DF, Ed.DL, Ed.DB, Ed.DR, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# L-move
cpL = [Co.URF, Co.ULB, Co.DBL, Co.UBR, Co.DFR, Co.UFL, Co.DLF, Co.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Ed.UR, Ed.UF, Ed.BL, Ed.UB, Ed.DR, Ed.DF, Ed.FL, Ed.DB, Ed.FR, Ed.UL, Ed.DL, Ed.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# B-move
cpB = [Co.URF, Co.UFL, Co.UBR, Co.DRB, Co.DFR, Co.DLF, Co.ULB, Co.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Ed.UR, Ed.UF, Ed.UL, Ed.BR, Ed.DR, Ed.DF, Ed.DL, Ed.BL, Ed.FR, Ed.FL, Ed.UB, Ed.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

CUBE_OK = True


class CubieCube:
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        if cp is None:
            self.cp = [Co(i) for i in range(8)]  # You may not put this as the default two lines above!
        else:
            self.cp = cp[:]
        if co is None:
            self.co = [0]*8
        else:
            self.co = co[:]
        if ep is None:
            self.ep = [Ed(i) for i in range(12)]
        else:
            self.ep = ep[:]
        if eo is None:
            self.eo = [0] * 12
        else:
            self.eo = eo[:]

    def __str__(self):
        s = ''
        for i in Co:
            s = s + '(' + str(self.cp[i]) + ',' + str(self.co[i]) + ')'
        s += '\n'
        for i in Ed:
            s = s + '(' + str(self.ep[i]) + ',' + str(self.eo[i]) + ')'
        return s

    def __eq__(self, other):
        if self.cp == other.cp and self.co == other.co and self.ep == other.ep and self.eo == other.eo:
            return True
        else:
            return False

    def to_facelet_cube(self):
        fc = face.FaceCube()
        for i in Co:
            j = self.cp[i]
            ori = self.co[i]
            for k in range(3):
                fc.f[cornerFacelet[i][(k+ori) % 3]] = cornerColor[j][k]
        for i in Ed:
            j = self.ep[i]
            ori = self.eo[i]
            for k in range(2):
                fc.f[edgeFacelet[i][(k+ori) % 2]] = edgeColor[j][k]
        return fc

    def corner_multiply(self, b):
        c_perm = [0]*8
        c_ori = [0]*8
        ori = 0
        for c in Co:
            c_perm[c] = self.cp[b.cp[c]]
            ori_a = self.co[b.cp[c]]
            ori_b = b.co[c]
            if ori_a < 3 and ori_b < 3:
                ori = ori_a + ori_b
                if ori >= 3:
                    ori -= 3
            elif ori_a < 3 <= ori_b:
                ori = ori_a + ori_b
                if ori >= 6:
                    ori -= 3
            elif ori_a >= 3 > ori_b:
                ori = ori_a - ori_b
                if ori < 3:
                    ori += 3
            elif ori_a >= 3 and ori_b >= 3:
                ori = ori_a - ori_b
                if ori < 0:
                    ori += 3
            c_ori[c] = ori
        for c in Co:
            self.cp[c] = c_perm[c]
            self.co[c] = c_ori[c]

    def edge_multiply(self, b):
        e_perm = [0]*12
        e_ori = [0]*12
        for e in Ed:
            e_perm[e] = self.ep[b.ep[e]]
            e_ori[e] = (b.eo[e] + self.eo[b.ep[e]]) % 2
        for e in Ed:
            self.ep[e] = e_perm[e]
            self.eo[e] = e_ori[e]

    def multiply(self, b):
        self.corner_multiply(b)
        self.edge_multiply(b)

    def inv_cubie_cube(self, d):
        for e in Ed:
            d.ep[self.ep[e]] = e
        for e in Ed:
            d.eo[e] = self.eo[d.ep[e]]

        for c in Co:
            d.cp[self.cp[c]] = c
        for c in Co:
            ori = self.co[d.cp[c]]
            if ori >= 3:
                d.co[c] = ori
            else:
                d.co[c] = -ori
                if d.co[c] < 0:
                    d.co[c] += 3

    def corner_parity(self):
        s = 0
        for i in range(Co.DRB, Co.URF, -1):
            for j in range(i - 1, Co.URF - 1, -1):
                if self.cp[j] > self.cp[i]:
                    s += 1
        return s % 2

    def edge_parity(self):
        s = 0
        for i in range(Ed.BR, Ed.UR, -1):
            for j in range(i - 1, Ed.UR - 1, -1):
                if self.ep[j] > self.ep[i]:
                    s += 1
        return s % 2

    def symmetries(self):
        from kociemba.symmetries import symCube, inv_idx
        s = []
        d = CubieCube()
        for j in range(N_SYM):
            c = CubieCube(symCube[j].cp, symCube[j].co, symCube[j].ep, symCube[j].eo)
            c.multiply(self)
            c.multiply(symCube[inv_idx[j]])
            if self == c:
                s.append(j)
            c.inv_cubie_cube(d)
            if self == d:
                s.append(j + N_SYM)
        return s

    def get_twist(self):
        ret = 0
        for i in range(Co.URF, Co.DRB):
            ret = 3 * ret + self.co[i]
        return ret

    def set_twist(self, twist):
        twistparity = 0
        for i in range(Co.DRB - 1, Co.URF - 1, -1):
            self.co[i] = twist % 3
            twistparity += self.co[i]
            twist //= 3
        self.co[Co.DRB] = ((3 - twistparity % 3) % 3)

    def get_flip(self):
        ret = 0
        for i in range(Ed.UR, Ed.BR):
            ret = 2 * ret + self.eo[i]
        return ret

    def set_flip(self, flip):
        flipparity = 0
        for i in range(Ed.BR - 1, Ed.UR - 1, -1):
            self.eo[i] = flip % 2
            flipparity += self.eo[i]
            flip //= 2
        self.eo[Ed.BR] = ((2 - flipparity % 2) % 2)

    def get_slice(self):
        a = x = 0
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.FR <= self.ep[j] <= Ed.BR:
                a += c_nk(11 - j, x + 1)
                x += 1
        return a

    def set_slice(self, idx):
        slice_edge = list(range(Ed.FR, Ed.BR + 1))
        other_edge = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        a = idx
        for e in Ed:
            self.ep[e] = -1

        x = 4
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1

    def get_slice_sorted(self):
        a = x = 0
        edge4 = [0]*4
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.FR <= self.ep[j] <= Ed.BR:
                a += c_nk(11 - j, x + 1)
                edge4[3 - x] = self.ep[j]
                x += 1
        b = 0
        for j in range(3, 0, -1):
            k = 0
            while edge4[j] != j + 8:
                rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1)*b + k
        return 24*a + b

    def set_slice_sorted(self, idx):
        slice_edge = [Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        other_edge = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        b = idx % 24
        a = idx // 24
        for e in Ed:
            self.ep[e] = -1

        j = 1
        while j < 4:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                rotate_right(slice_edge, 0, j)
                k -= 1
            j += 1

        x = 4
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1

    def get_u_edges(self):
        a = x = 0
        edge4 = [0]*4
        ep_mod = self.ep[:]
        for j in range(4):
            rotate_right(ep_mod, 0, 11)
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.UR <= ep_mod[j] <= Ed.UB:
                a += c_nk(11 - j, x + 1)
                edge4[3 - x] = ep_mod[j]
                x += 1
        b = 0
        for j in range(3, 0, -1):
            k = 0
            while edge4[j] != j:
                rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1)*b + k
        return 24*a + b

    def set_u_edges(self, idx):
        slice_edge = [Ed.UR, Ed.UF, Ed.UL, Ed.UB]
        other_edge = [Ed.DR, Ed.DF, Ed.DL, Ed.DB, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        b = idx % 24
        a = idx // 24
        for e in Ed:
            self.ep[e] = -1

        j = 1
        while j < 4:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                rotate_right(slice_edge, 0, j)
                k -= 1
            j += 1

        x = 4
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1
        for j in range(4):
            rotate_left(self.ep, 0, 11)

    def get_d_edges(self):
        a = x = 0
        edge4 = [0] * 4
        ep_mod = self.ep[:]
        for j in range(4):
            rotate_right(ep_mod, 0, 11)
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.DR <= ep_mod[j] <= Ed.DB:
                a += c_nk(11 - j, x + 1)
                edge4[3 - x] = ep_mod[j]
                x += 1

        b = 0
        for j in range(3, 0, -1):
            k = 0
            while edge4[j] != j + 4:
                rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1) * b + k
        return 24 * a + b

    def set_d_edges(self, idx):
        slice_edge = [Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        other_edge = [Ed.FR, Ed.FL, Ed.BL, Ed.BR, Ed.UR, Ed.UF, Ed.UL, Ed.UB]
        b = idx % 24
        a = idx // 24
        for e in Ed:
            self.ep[e] = -1

        j = 1
        while j < 4:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                rotate_right(slice_edge, 0, j)
                k -= 1
            j += 1

        x = 4
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1
        for j in range(4):
            rotate_left(self.ep, 0, 11)

    def get_corners(self):
        perm = list(self.cp)
        b = 0
        for j in range(Co.DRB, Co.URF, -1):
            k = 0
            while perm[j] != j:
                rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
        return b

    def set_corners(self, idx):
        self.cp = [i for i in Co]
        for j in Co:
            k = idx % (j + 1)
            idx //= j + 1
            while k > 0:
                rotate_right(self.cp, 0, j)
                k -= 1

    def get_ud_edges(self):
        perm = self.ep[0:8]  # duplicate first 8 elements of ep
        b = 0
        for j in range(Ed.DB, Ed.UR, -1):
            k = 0
            while perm[j] != j:
                rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
        return b

    def set_ud_edges(self, idx):
        # positions of FR FL BL BR edges are not affected
        for i in list(Ed)[0:8]:
            self.ep[i] = i
        for j in list(Ed)[0:8]:
            k = idx % (j + 1)
            idx //= j + 1
            while k > 0:
                rotate_right(self.ep, 0, j)
                k -= 1


    def verify(self):
        edge_count = [0]*12
        for i in Ed:
            edge_count[self.ep[i]] += 1
        for i in Ed:
            if edge_count[i] != 1:
                return

        s = 0
        for i in Ed:
            s += self.eo[i]
        if s % 2 != 0:
            return

        corner_count = [0] * 8
        for i in Co:
            corner_count[self.cp[i]] += 1
        for i in Co:
            if corner_count[i] != 1:
                return

        s = 0
        for i in Co:
            s += self.co[i]
        if s % 3 != 0:
            return

        if self.edge_parity() != self.corner_parity():
            return

        return CUBE_OK

basicMoveCube = [CubieCube()] * 6
basicMoveCube[Color.U] = CubieCube(cpU, coU, epU, eoU)
basicMoveCube[Color.R] = CubieCube(cpR, coR, epR, eoR)
basicMoveCube[Color.F] = CubieCube(cpF, coF, epF, eoF)
basicMoveCube[Color.D] = CubieCube(cpD, coD, epD, eoD)
basicMoveCube[Color.L] = CubieCube(cpL, coL, epL, eoL)
basicMoveCube[Color.B] = CubieCube(cpB, coB, epB, eoB)

moveCube = [CubieCube()] * 18
for c1 in Color:
    cc = CubieCube()
    for k1 in range(3):
        cc.multiply(basicMoveCube[c1])
        moveCube[3 * c1 + k1] = CubieCube(cc.cp, cc.co, cc.ep, cc.eo)
