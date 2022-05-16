from sympy import *

A, r, l, F, f = symbols("A, r, l, F, f")
deltaf = Symbol("\Delta f")
deltaA = Symbol("\Delta A")
deltar = Symbol("\Delta r")
deltaF = Symbol("\Delta F")
deltal = Symbol("\Delta l")


rho = 1/(A**2*4*l**2*pi*r**2)

deltaRho = sqrt((deltaA*rho.diff(A))**2+(deltal*rho.diff(l))**2+(deltar*rho.diff(r))**2)

subs={
    deltaA:0.07241178173,
    deltal:0.0011487923490924473,
    deltar:0.000005773502691896258,
    r:0.000275,
    l:0.8194,
    A:15.069824,
}

val = deltaRho.evalf(n=15, subs=subs)

print(val/1000)
print(latex(deltaRho))