import numpy as np
import mehanika_robota.mehanika.kinematika as kin
import mehanika_robota.mehanika.kretanje_krutog_tela as kkt
from mehanika_robota.roboti import Robot

M = kkt.SE3_sastavi(np.eye(3), [0, 2, 1])

S = np.array([[0, 0, 1, 0, 0, 0],
              [0, 0, 1, 1, 0, 0],
              [0, 0, 1, 2, 0, 0],
              [0, 0, 0, 0, 0, 1]], dtype=float)

B = np.array([[ 0,  0, 0, 0],
              [ 0,  0, 0, 0],
              [ 1,  1, 1, 0],
              [-2, -1, 0, 0],
              [ 0,  0, 0, 0],
              [ 0,  0, 0, 1]], dtype=float)

L = (1, 1, 1)

RRRP_prostor = Robot(M, S, segmenti=L)
RRRP_telo = Robot(M, B, segmenti=L, koord_sistem_prostor=False, vek_kolona=True)

pomeranja = [0, np.pi/2, -np.pi/2, 1]

print(RRRP_prostor.dir_kin(pomeranja))
print(RRRP_telo.dir_kin(pomeranja))
print(np.allclose(RRRP_prostor.dir_kin(pomeranja), RRRP_telo.dir_kin(pomeranja)))