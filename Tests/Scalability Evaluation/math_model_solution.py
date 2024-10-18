from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
import math

N = 100
at = 1.712 
# at = 0.014
lambd = 1/300.0

cache_memory = {}

'''
Intermediate Repetition Probability Function 
    Called as: intermediate_repition_probability(p,n,m)
    Returns  : the probability of the packet successfully traversing to the gateway from current state (n,m)
'''
def intermediate_repition_probability(p, n, m=None):
    if((n,m) in cache_memory):
        return cache_memory[(n,m)]
    else:
        if(n>4):
            if(m == None):
                cache_memory[(n,m)] = intermediate_repition_probability(p, n-2, n-1)*(1-4*p) + intermediate_repition_probability(p, n-1, None)*2*p
            else:
                cache_memory[(n,m)] = intermediate_repition_probability(p, n-2, n-1)*(1-4*p) + intermediate_repition_probability(p, n-1, None)*(4*p -8*p**2)

        elif(n==4):
            if(m == None):
                cache_memory[(n,m)] = intermediate_repition_probability(p, n-2, n-1)*(1-2*p)
            else:
                cache_memory[(n,m)] = intermediate_repition_probability(p, n-2, n-1)*(1-2*p) + intermediate_repition_probability(p, n-1, None)*(2*p -8*p**2)
        
        else:
            return 1
        
        return cache_memory[(n,m)] 

'''
Repetition Probability Function 
    Called as: repition_probability(p,n) where n is the number of the repeater at the tag that generates the packet
    Returns  : the probability of the packet successfully traversing to the gateway
    Note     : Here we consider the fact that the first repetition can also happen with a backward propagation followed 
                by a forward repition of 2 hops
'''
def repition_probability(p, n):
    if(n>4):
        if((N-n)>=3):
            return intermediate_repition_probability(p, n-2, n-1)*(1-4*p) + intermediate_repition_probability(p, n-1, None)*(2*p +2*p*(1-2*p)*(1-4*p))
        elif((N-n)>0):
            return intermediate_repition_probability(p, n-2, n-1)*(1-4*p) + intermediate_repition_probability(p, n-1, None)*(2*p +2*p*(1-4*p))
        else:
            return intermediate_repition_probability(p, n-2, n-1)*(1-4*p) + intermediate_repition_probability(p, n-1, None)*(2*p)

    elif(n==4):
        if((N-n)>=3):
            return intermediate_repition_probability(p, n-2, n-1)*(1-2*p) + intermediate_repition_probability(p, n-1, None)*(2*p*(1-2*p)*(1-4*p))
        elif((N-n)>0):
            return intermediate_repition_probability(p, n-2, n-1)*(1-2*p) + intermediate_repition_probability(p, n-1, None)*(2*p*(1-4*p))
        else:      
            return intermediate_repition_probability(p, n-2, n-1)*(1-2*p)
    
    else:
        return 1


def equation(p):
    cache_memory.clear()
    networkOutputRate = 0
    for n in range(1, N+1):
        networkOutputRate += lambd*(1-p)*repition_probability(p,n)         
    return p -at*networkOutputRate


# Initial guess
initial_guess = 0.0001

# Solve the equation numerically
p = fsolve(equation, initial_guess)

Ri= lambd*N
Ro= p/at
print("Network Input Rate:", Ri)
print("Network Output Rate:", Ro)
print("DER:", Ro/Ri)

# print (cache_memory)


