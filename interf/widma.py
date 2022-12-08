from program import DataAnalyser, Expression, Parametr
import sympy as sp

#DataAnalyser("csv.csv").print_param_list()

[c_op, c_ol, z_op, z_ol, odl_ekr, s1_1, s1_2, odl_ekr2, s2_1, s2_2, odl_ekr3, dx1, dx2, dx3, dx4, dx5,] = DataAnalyser("csv.csv").single_params


a, b, d, m, l, x, = sp.symbols("a, b, d, m, l, x,")

sred_expr = Expression((a+b)/2)

lambda_red = 632.8 

x_dyf = Parametr("x_dyfr", expr=sred_expr)
x_s1 = Parametr("x_s1", expr=sred_expr)
x_s2 = Parametr("x_s2", expr=sred_expr)

x_dyf.calculate({
    a:c_ol,
    b:c_op,
})

x_dyf_ziel = Parametr("x_dyfr", expr=sred_expr)

x_dyf_ziel.calculate({
    a:z_ol,
    b:z_op,
})

d_siatki = Parametr("d_siatki", expr=Expression(lambda_red*1*sp.sqrt(x**2+l**2)/x))  # stała siatki na podstawie prążków pierwszego rzędu


d_siatki.calculate({
    x:x_dyf,
    l:odl_ekr,
})

dł_ziel = Parametr("dl_swiatlo_ziel", expr=Expression(d*x/sp.sqrt(x**2+l**2))) #dł w nanometrach
dł_ziel.calculate({
    d:d_siatki,
    x:x_dyf_ziel,
    l:odl_ekr
})


a1_1 = Parametr("a_pojedyncza_1rz", expr=Expression(2*lambda_red*l/x))
a1_2 = Parametr("a_pojedyncza_2rz", expr=Expression(2*2*lambda_red*l/x))
a1_1.calculate({l:odl_ekr2, x:s1_1})
a1_2.calculate({l:odl_ekr2, x:s1_2})

a1 = Parametr("a_pojedyncza", expr=sred_expr)
a1.calculate({a:a1_1, b:a1_2})


a2_1 = Parametr("a_podwojna_1rz", expr=Expression(2*lambda_red*l/x))
a2_2 = Parametr("a_podwojna_2rz", expr=Expression(2*2*lambda_red*l/x))
a2_1.calculate({l:odl_ekr3, x:s2_1})
a2_2.calculate({l:odl_ekr3, x:s2_2})

a2 = Parametr("a_podwojna", expr=sred_expr)
a2.calculate({a:a2_1, b:a2_2})

dx_sr = Parametr("srednie_dx", expr=Expression((a+b+d+l+m)/5))
dx_sr.calculate({
    a:dx1, b:dx2, d:dx3, l:dx4, m:dx5
})

d_szczeliny = Parametr("d_szczeliny", expr=Expression(lambda_red*l/d))
d_szczeliny.calculate({l:odl_ekr3, d:dx_sr})

# # # l1 = Parametr("l1", 667.8)
# # # l2 = Parametr("l2",587.6)
# # # l3 = Parametr("l3",501.6)
# # # l4 = Parametr("l4",471.3)
# # l5 = Parametr("l5", 447.1)
# l1 = 667.8
# l2 = 587.6
# l3 = 502.6
# l4= 471.3
# l5 = 447.1
# L = [l1, l2, l3, l4, l5]

# # de = Expression(l/sp.sin(a))

# D1 = Parametr("d1")
# D2 = Parametr("d2")
# D3 = Parametr("d3")
# D4 = Parametr("d4")
# D5 = Parametr("d5")


# for n in range(1, 6):
#     e = Expression(sp.Rational(globals()[f"l{n}"], 1)/sp.sin(a))
#     globals()[f"D{n}"].expr =e
#     subs = {
#             #l: globals()[f"l{n}"],
#             a:globals()[f"d_{n}"]
#         }
#     globals()[f"D{n}"].calculate(subs)
#     # globals()[f"D{n}"].calculate(subs)


# e = Expression((d1+d2+d3+d4+d5)/5)

# d_mean = Parametr("d_sr", expr= e)

# d_mean.calculate(
#     {
#         d1:D1,
#         d2:D2,
#         d3:D3,
#         d4:D4,
#         d5:D5,
#     }
# )

# w1 = Parametr("wzo", expr = Expression(d*sp.sin(a)))
# w2 = Parametr("wnie", expr = Expression(d*sp.sin(a)))
# k1 = Parametr("kzie", expr = Expression(d*sp.sin(a)))
# k2 = Parametr("kzo", expr = Expression(d*sp.sin(a)))

# w1.calculate({d:d_mean, a:w_zo})
# w2.calculate({d:d_mean, a:w_n})
# k1.calculate({d:d_mean, a:k_zie})
# k2.calculate({d:d_mean, a:w_zo})

