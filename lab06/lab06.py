from program import DataAnalyser, Expression, Parametr
import sympy as sp
from sympy import pi, Rational, sqrt

#DataAnalyser("L06 - Arkusz2.csv").print_param_list()

m = sp.symbols("m")
m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12 = sp.symbols("m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12")
m_drut = 0.145

[r, l, m_1, m_2, m_3, m_4, m_5, m_6, m_7, m_8, m_9, m_10, m_11, m_12, f_1_1, f_1_2, f_1_3, f_1_4, f_2_1, f_2_2, f_2_3, f_2_4, f_3_1, f_3_2, f_3_3, f_3_4, f_4_1, f_4_2,
f_4_3, f_4_4, f_5_1, f_5_2, f_5_3, f_5_4, f_6_1, f_6_2,
f_6_3, f_6_4, f_7_1, f_7_2, f_7_3, f_7_4, f_8_1, f_8_2, f_8_3,
f_8_4, f_9_1, f_9_2, f_9_3, f_9_4, f_10_1, f_10_2, f_10_3, f_10_4] = DataAnalyser("L06 - Arkusz2.csv").single_params

freqs = [
    [f_1_1, f_1_2, f_1_3, f_1_4,],
    [f_2_1, f_2_2, f_2_3, f_2_4,],
    [f_3_1, f_3_2, f_3_3, f_3_4,],
    [f_4_1, f_4_2,f_4_3, f_4_4,],
    [f_5_1, f_5_2, f_5_3, f_5_4,],
    [f_6_1, f_6_2,f_6_3, f_6_4,],
    [f_7_1, f_7_2, f_7_3, f_7_4,],
    [f_8_1, f_8_2, f_8_3,f_8_4,],
    [f_9_1, f_9_2, f_9_3, f_9_4,],
    [f_10_1, f_10_2, f_10_3, f_10_4],
]

for el in [m_1, m_2, m_3, m_4, m_5, m_6, m_7, m_8, m_9, m_10, m_11, m_12]:
    el.change_unit(0.001, 'kg')


sF_expr = Expression(expr=sqrt(m*9.81), description="pierw z F")

sF1 = Parametr("F_1", expr=sF_expr)
sF2 = Parametr("F_2", expr=sF_expr)
sF3 = Parametr("F_3", expr=sF_expr)
sF4 = Parametr("F_4", expr=sF_expr)
sF5 = Parametr("F_5", expr=sF_expr)
sF6 = Parametr("F_6", expr=sF_expr)
sF7 = Parametr("F_7", expr=sF_expr)
sF8 = Parametr("F_8", expr=sF_expr)
sF9 = Parametr("F_9", expr=sF_expr)
sF10 = Parametr("F_10", expr=sF_expr)

M1 = Parametr("M_1", expr=Expression(m3+m4+m9+0.145))
M2 = Parametr("M_2", expr=Expression(m3+m4+m9+m5+0.145))
M3 = Parametr("M_3", expr=Expression(m3+m4+m9+m5+m1+0.145))
M4 = Parametr("M_4", expr=Expression(m3+m4+m9+m5+m1+m6+0.145))
M5 = Parametr("M_5", expr=Expression(m3+m4+m9+m5+m1+m6+m2+0.145))
M6 = Parametr("M_6", expr=Expression(m3+m4+m9+m5+m1+m6+m2+m12+0.145))
M7 = Parametr("M_7", expr=Expression(m3+m4+m9+m5+m1+m6+m2+m12+m11+0.145))
M8 = Parametr("M_8", expr=Expression(m3+m4+m9+m5+m1+m6+m2+m12+m11+m7+0.145))
M9 = Parametr("M_9", expr=Expression(m3+m4+m9+m5+m1+m6+m2+m12+m11+m7+m8+0.145))
M10 = Parametr("M_10", expr=Expression(m3+m4+m9+m5+m1+m6+m2+m12+m11+m7+m8+m10+0.145))

subs_m = {
    m1:m_1,
    m2:m_2,
    m3:m_3,
    m4:m_4,
    m5:m_5,
    m6:m_6,
    m7:m_7,
    m8:m_8,
    m9:m_9,
    m10:m_10,
    m11:m_11,
    m12:m_12,
}
#calculate weights
for i in range(10):
    globals()[f"M{i+1}"].calculate(subs_m)

# calculate sFs
for i in range(10):
    globals()[f"sF{i+1}"].calculate({m:globals()[f"M{i+1}"]})
