from kociemba.enums import Facelet as Fc, Color as Cl

# Сопоставление позиций углов
cornerFacelet = [[Fc.U9, Fc.R1, Fc.F3], [Fc.U7, Fc.F1, Fc.L3], [Fc.U1, Fc.L1, Fc.B3], [Fc.U3, Fc.B1, Fc.R3],
                 [Fc.D3, Fc.F9, Fc.R7], [Fc.D1, Fc.L9, Fc.F7], [Fc.D7, Fc.B9, Fc.L7], [Fc.D9, Fc.R9, Fc.B7]
                 ]

# Сопоставление позиций граней
edgeFacelet = [[Fc.U6, Fc.R2], [Fc.U8, Fc.F2], [Fc.U4, Fc.L2], [Fc.U2, Fc.B2], [Fc.D6, Fc.R8], [Fc.D2, Fc.F8],
               [Fc.D4, Fc.L8], [Fc.D8, Fc.B8], [Fc.F6, Fc.R4], [Fc.F4, Fc.L6], [Fc.B6, Fc.L4], [Fc.B4, Fc.R6]
               ]

# Сопоставление цветов углов
cornerColor = [[Cl.U, Cl.R, Cl.F], [Cl.U, Cl.F, Cl.L], [Cl.U, Cl.L, Cl.B], [Cl.U, Cl.B, Cl.R],
               [Cl.D, Cl.F, Cl.R], [Cl.D, Cl.L, Cl.F], [Cl.D, Cl.B, Cl.L], [Cl.D, Cl.R, Cl.B]
               ]

# Сопоставление цветов граней
edgeColor = [[Cl.U, Cl.R], [Cl.U, Cl.F], [Cl.U, Cl.L], [Cl.U, Cl.B], [Cl.D, Cl.R], [Cl.D, Cl.F],
             [Cl.D, Cl.L], [Cl.D, Cl.B], [Cl.F, Cl.R], [Cl.F, Cl.L], [Cl.B, Cl.L], [Cl.B, Cl.R]
             ]

'''Константы'''
N_PERM_4 = 24
N_CHOOSE_8_4 = 70
N_MOVE = 18

N_TWIST = 2187
N_FLIP = 2048
N_SLICE_SORTED = 11880
N_SLICE = N_SLICE_SORTED // N_PERM_4
N_FLIPSLICE_CLASS = 64430

N_U_EDGES_PHASE2 = 1680
# N_D_EDGES_PHASE2 = 1680
N_CORNERS = 40320
N_CORNERS_CLASS = 2768
N_UD_EDGES = 40320

N_SYM = 4
N_SYM_D4h = 16
FOLDER = "kociemba/twophase"  # Папка с таблицами
