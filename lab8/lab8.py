from program import DataAnalyser, Expression, Parametr
import sympy as sp
from sympy import pi, Rational

analyser = DataAnalyser("pomiary.csv")
analyser.print_param_list()

[s_p, b_p, g_p, h_p , x1, t11, t12, t13, x2, t21, t22, t23, x3, t31, t32, t33, x4, t41, t42, t43, x5, t51, t52, t53, x6, t61, t62, t63, m1, m2, m3] = analyser.single_params

m, t, r, h, b, g, x = sp.symbols("m t r h b g x")

s_p.change_unit(0.01, unit="m")
b_p.change_unit(0.01, unit="m")
g_p.change_unit(0.01, unit="m")
h_p.change_unit(0.01, unit="m")
m1.change_unit(0.001, unit="kg")
m2.change_unit(0.001, unit="kg")
m3.change_unit(0.001, unit="kg")
# for i in [1, 2, 3, 4, 5, 6]:
#     globals()[f'x{i}'].change_unit(0.01, unit="m")


#PROMIEN szypuli to s_p, polowy g i b tak samo

for i in [1, 2, 3, 4, 5, 6]:
    for j in [1, 2, 3]:
        globals()[f"I_{i}{j}"] = Parametr(f"I_{i}{j}", expr=Expression(m*r*r*(((9.81*t*t)/(2*h)) - 1)))

for i in [1, 2, 3, 4, 5, 6]:
    globals()[f'l2_{i}'] = Parametr(f'l2_{i}', expr = Expression((b/2 + g/2 + x)**2))
    globals()[f'l2_{i}'].calculate({b:b_p, g:g_p, x:globals()[f'x{i}']})

for i in [1, 2, 3, 4, 5, 6]:
    for j in [1, 2, 3]:
        subs = {
            m:globals()[f'm{j}'],
            t:globals()[f"t{i}{j}"],
            r:s_p,
            h:h_p,
        }
        globals()[f"I_{i}{j}"].calculate(subs)