from program import DataAnalyser, Expression, Parametr
import sympy as sp

#DataAnalyser("wyniki.csv").print_param_list()

[d_1, d_2, d_3, d_4, d_5, w_zo, w_n, k_zie, k_zo] = DataAnalyser("wyniki.csv").single_params


d1, d2, d3, d4, d5, l , a, d= sp.symbols("d1, d2, d3, d4, d5, l, a, d")


# # l1 = Parametr("l1", 667.8)
# # l2 = Parametr("l2",587.6)
# # l3 = Parametr("l3",501.6)
# # l4 = Parametr("l4",471.3)
# l5 = Parametr("l5", 447.1)
l1 = 667.8
l2 = 587.6
l3 = 502.6
l4= 471.3
l5 = 447.1
L = [l1, l2, l3, l4, l5]

# de = Expression(l/sp.sin(a))

D1 = Parametr("d1")
D2 = Parametr("d2")
D3 = Parametr("d3")
D4 = Parametr("d4")
D5 = Parametr("d5")


for n in range(1, 6):
    e = Expression(sp.Rational(globals()[f"l{n}"], 1)/sp.sin(a))
    globals()[f"D{n}"].expr =e
    subs = {
            #l: globals()[f"l{n}"],
            a:globals()[f"d_{n}"]
        }
    globals()[f"D{n}"].calculate(subs)
    # globals()[f"D{n}"].calculate(subs)


e = Expression((d1+d2+d3+d4+d5)/5)

d_mean = Parametr("d_sr", expr= e)

d_mean.calculate(
    {
        d1:D1,
        d2:D2,
        d3:D3,
        d4:D4,
        d5:D5,
    }
)

w1 = Parametr("wzo", expr = Expression(d*sp.sin(a)))
w2 = Parametr("wnie", expr = Expression(d*sp.sin(a)))
k1 = Parametr("kzie", expr = Expression(d*sp.sin(a)))
k2 = Parametr("kzo", expr = Expression(d*sp.sin(a)))

w1.calculate({d:d_mean, a:w_zo})
w2.calculate({d:d_mean, a:w_n})
k1.calculate({d:d_mean, a:k_zie})
k2.calculate({d:d_mean, a:w_zo})

