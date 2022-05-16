from program import DataAnalyser, Expression, Parametr
import sympy as sp
from sympy import pi, Rational

# DataAnalyser("FIZLAB_L03.csv").print_param_list()

[
    cz_d,
    cz_s,
    cz_1,
    cz_3,
    cz_5,
    cz_7,
    cz_9,
    b_d,
    b_s,
    b_1,
    b_3,
    b_5,
    b_7,
    b_9,
    Tcz1,
    Tcz3,
    Tcz5,
    Tcz7,
    Tcz9,
    Tb1,
    Tb3,
    Tb5,
    Tb7,
    Tb9,
] = DataAnalyser("FIZLAB_L03.csv").single_params


# d - dł, s - szer, r - odległość od SM, T - okres
d, s, r, T = sp.symbols("d, s, r, T")

# równanie na g
expr_g = (4 * pi ** 2) * ((Rational(1, 12) * (d ** 2 + s ** 2) + r ** 2) / (r * T ** 2))
g = Expression(expr=expr_g, description="stala g")

# poarametry g z pojedynczych pomiarów
gcz1 = Parametr("g_cz1", expr=g)
gcz3 = Parametr("g_cz3", expr=g)
gcz5 = Parametr("g_cz5", expr=g)
gcz7 = Parametr("g_cz7", expr=g)
gcz9 = Parametr("g_cz9", expr=g)
gb1 = Parametr("g_b1", expr=g)
gb3 = Parametr("g_b3", expr=g)
gb5 = Parametr("g_b5", expr=g)
gb7 = Parametr("g_b7", expr=g)
gb9 = Parametr("g_b9", expr=g)

# zmiana jednostek długości cm na m
for param in [
    cz_d,
    cz_s,
    cz_1,
    cz_3,
    cz_5,
    cz_7,
    cz_9,
    b_d,
    b_s,
    b_1,
    b_3,
    b_5,
    b_7,
    b_9,
]:
    param.change_unit(0.01, unit="m")

# obliczanie wartości g dla pojedynczych pomiarów
for i in [1, 3, 5, 7, 9]:
    for color in ["cz", "b"]:
        subs = {
            d: globals()[f"{color}_d"],
            s: globals()[f"{color}_s"],
            r: globals()[f"{color}_{i}"],
            T: globals()[f"T{color}{i}"],
        }
        globals()[f"g{color}{i}"].calculate(subs)


# obliczanie średniego g
G = [gcz1, gcz3, gcz5, gcz7, gcz9, gb1, gb3, gb5, gb7, gb9]
g_avg_expr = 0
for g in G:
    g_avg_expr += g.symbol
g_avg_expr /= 10

expr_g_avg = Expression(g_avg_expr, description="srednia g")

g_avg = Parametr("srednie_g", expr=expr_g_avg)

g_subs = dict()
for i in [1, 3, 5, 7, 9]:
    for color in ["cz", "b"]:
        g_subs[f"g_{color}{i}"] = globals()[f"g{color}{i}"]

g_avg.calculate(g_subs)

# średnie g dla wahadel

gav_cz = (gcz1.symbol+ gcz3.symbol+ gcz5.symbol+ gcz7.symbol+ gcz9.symbol)/5
gav_b = (gb1.symbol+ gb3.symbol+ gb5.symbol+ gb7.symbol+ gb9.symbol)/5


