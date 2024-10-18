from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
import math

N = 7
at = 1.712
lambd = 1/300.0

NodeList = []

class Node:
    def __init__(self, n, prev=None):
        NodeList.append(self)
        self.id = len(NodeList)-1
        self.n = n
        self.next1  = None
        self.next2  = None
        self.next1p = None
        self.next2p = None
        self.prev   = prev
        self.prevp  = None

        if(n>4):
            self.next1 = Node(n-2, self)
            self.next1.prev = self
            self.next1.prevp = "1-2p"
            self.next1p = "1-2p"

            self.next2 = Node(n-1, self)
            self.next2.prev = self
            if(self.prevp =="1-2p"):
                self.next2.prevp = "2p-2p^2"
                self.next2p = "2p-2p^2"
            elif(self.prev == None):
                self.next2.prevp = "2p-3p^2+2p^3"
                self.next2p = "2p-3p^2+2p^3"
            else:
                self.next2.prevp = "p"
                self.next2p = "p"

        if(n==4):
            self.next1 = Node(n-2, self)
            self.next1.prev = self
            if(self.prev == None):
                self.next1.prevp = "1-3p^2+2p^3"
                self.next1p = "1-3p^2+2p^3"
            else:
                self.next1.prevp = "1-p"
                self.next1p = "1-p"

        if(n==3):
            self.next1 = Node(n-2, self)
            self.next1.prev = self
            self.next1.prevp = "1"
            self.next1p = "1"
        
        if(n==2):
            self.next1 = Node(n-2, self)
            self.next1.prev = self
            self.next1.prevp = "1"
            self.next1p = "1"

        if(n==1):
            self.next1 = Node(n-1, self)
            self.next1.prev = self
            self.next1.prevp = "1"
            self.next1p = "1"


def RepetitionSuccessProbability(n):
    global NodeList 
    NodeList= []
    A = Node(n)
    EndNodes = []
    exponentData =[]
    debug = 0

    for x in NodeList:
        if(x.n == 0):
            EndNodes.append(x)

    if(debug == 1):
        print("NodeList in the Graph:")
        for x in NodeList:
            if(x.next1!=None):
                a =x.next1.id
            else:
                a = "None"
            if(x.next2!=None):
                b =x.next2.id
            else:
                b = "None"
            if(x.prev!=None):
                c =x.prev.id
            else:
                c = "None"
            print("id=", x.id, "\t n=",x.n, "\t next1=", a, "\t next1p=", x.next1p, "\t next2=", b, "\t next2p=", x.next2p, "\t prev=", c, "\t prevp=", x.prevp)

        print("\nNumber of end nodes in the graph =",len(EndNodes))

        print("\nAll possible routes in the Graph:")

    for y in EndNodes:
        mul =[]
        node = y
        while(node.prev != None):
            mul.append(node.prevp)
            node = node.prev
        if(debug):
            print(mul)

        #List of exponents
            #0 -(1-2p)
            #1 -(2p-2p^2)
            #2 -(p)
            #3 -(1-p)
            #4 -(2p-3p^2+2p^3)
            #5 -(1-3p^2+2p^3)
        exponents =[0,0,0,0,0,0]
        for k in mul:
            if(k == "1-2p"):
                exponents[0] += 1
            if(k == "2p-2p^2"):
                exponents[1] += 1
            if(k == "p"):
                exponents[2] += 1
            if(k == "1-p"):
                exponents[3] += 1
            if(k == "2p-3p^2+2p^3"):
                exponents[4] += 1
            if(k == "1-3p^2+2p^3"):
                exponents[5] += 1
        exponentData.append(exponents)
        if(debug):
            print(exponents)
    if(debug):
        print("\nList of exponent data:")
        print(exponentData)
    return exponentData


def equation(p):
    val = 0
    for n in range(1, N+1):
        exponentData = RepetitionSuccessProbability(n)
        # print(exponentData)
        for x in exponentData:
            val +=(1-2*p)**(x[0]) *(2*p-2*p**2)**(x[1]) *(p)**(x[2]) *(1-p)**(x[3]) *(2*p-3*p**2+2*p**3)**(x[4]) *(1-3*p**2+2*p**3)**(x[5])
            # val +=(1-4*p)**(x[0]) *(4*p-8*p**2)**(x[1]) *(2*p)**(x[2]) *(1-2*p)**(x[3]) *(4*p-12*p**2+16*p**3)**(x[4]) *(1-12*p**2+16*p**3)**(x[5])
    
    return p -at*lambd*(1-p)*val


# Initial guess
initial_guess = 0.0001

# Solve the equation numerically
p = fsolve(equation, initial_guess)

print("Numerical solution for p:", p)
print("equation(p)=",equation(p))

Ri= lambd*N
Ro= p/at
print("Network Input Rate:", Ri)
print("Network Output Rate:", Ro)
print("DER:", Ro/Ri)





