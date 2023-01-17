import math
from program import *
import sympy as sp

[Kat0_1, KatBr_1, Kat0_2, KatBr_2, Kat0_3, KatBr_3, Kat0_4, KatBr_4] = DataAnalyser("o2.csv").single_params

K0, K1, a = sp.symbols("K0, K1, a")


k1 = Parametr("kątb1", expr=Expression((K0-K1)))
k2 = Parametr("kątb2", expr=Expression((K0-K1)))
k3 = Parametr("kątb3", expr=Expression((K0-K1)))
k4 = Parametr("kątb4", expr=Expression((K0-K1)))



for i in range(1, 5):
    subs = {
        K0:globals()[f"Kat0_{i}"],
        K1:globals()[f"KatBr_{i}"]
    }
    globals()[f"k{i}"].calculate(subs)
    

for i in range(1, 5):
    n = 2*math.pi/360
    globals()[f"k{i}"].change_unit(n, "rad")

n1 = Parametr("wsp1", expr=Expression(sp.tan(a)))
n2 = Parametr("wsp2", expr=Expression(sp.tan(a)))
n3 = Parametr("wsp3", expr=Expression(sp.tan(a)))
n4 = Parametr("wsp4", expr=Expression(sp.tan(a)))

for i in range(1, 5):
    subs={a:globals()[f'k{i}']}
    globals()[f"n{i}"].calculate(subs)


