from sympy import diff, symbols, solve, plot, latex

eps, sig, r = symbols('eps sig r')

#Removing # from eps and sig below will turn eps and sig into normal variables  of python symbols.
eps = 0.997
sig = 3.4 # Angstrom, the potential value is zero at this distance

V = 4*eps*((sig/r)**12 - (sig/r)**6)

Fr = -diff(V, r)

print("Fr is: ", Fr)
print(solve(Fr, r)[1]) # to get where the force is zero, in this case 3.816 Angstrom

plot(V, Fr, (r, 0, 10), xlabel='Distance', axis_center=(0,0), ylim=(-3*eps,4*eps), xlim=(0,10*sig))
