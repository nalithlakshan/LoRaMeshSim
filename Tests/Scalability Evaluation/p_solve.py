from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
import math

N =50
at = 1.712
lambd = 1/600.0

# def equation(p):
#     # F_p = 1 -3*p**2 +3*p**3 -p**4
#     # G_p = 1 -6*p**3 +9*p**4 -5*p**5 +p**6
#     F_p = 1 -2*p**2 +3*p**3 -p**4
#     G_p = 1 -4*p**3 +8*p**4 -5*p**5 +p**6
#     # F_p = 1 -2*p**2 +p**3
#     # G_p = 1 -2*p**2 +p**3
#     return p - at *lambd * (1 - 5*p) *F_p * sum([G_p**i for i in range(0, N)])


def equation(p):
    # C = at *lambd * (1 - p)**5
    # hop1_first = 2*p -3*p**2 +2*p**3 # 1 hop (first repition only)
    # hop2 = 1 -2*p
    # hop1_after_hop2 = 2*p-2*p**2
    # hop1_after_hop2 = 2*p-2*p**2
    # hop1_after_hop1 = p
    F_p = 1 -2*p**2 +3*p**3 -p**4
    val =0
    # print("\n", "p=",p)
    for n in range(0, N):
        for a in range(0,int(round(n/2)+1)):
            b = n-2*a 
            if(b==-1):
                b=0
            combinations = int(math.factorial(a+b)/(math.factorial(a)*math.factorial(b)))
            # print("n=", n,"\t a=", a, "\t b=", b, "\t combinations=", combinations)
            val += combinations*((1-2*p)**a)*((2*p-2*p**2)**b)*F_p
    return p - at *lambd * (1 - 1*p) *val
    # return p - at *lambd * (1 - p)**5 *F_p * sum([(1-2*p**2)*i for i in range(0, N)])

# Initial guess
initial_guess = 0.0001

# Solve the equation numerically
solution = fsolve(equation, initial_guess)

print("Numerical solution for p:", solution)
print("equation(p)=",equation(solution))

p = solution
# F_p = 1 -3*p**2 +3*p**3 -p**4
# G_p = 1 -6*p**3 +9*p**4 -5*p**5 +p**6
# print("g(p):", G_p)

Ri= lambd*N
Ro= p/at
print("Network Input Rate:", Ri)
print("Network Output Rate:", Ro)
print("DER:", Ro/Ri)

#Plotting the equation
# x_values = np.linspace(0, 1, 10000)
# y_values = equation(x_values)


# plt.plot(x_values, y_values)
# plt.title('Plot')
# plt.xlabel('p')
# plt.ylabel('Y(p)')
# plt.legend()
# plt.grid(True)
# plt.show()
