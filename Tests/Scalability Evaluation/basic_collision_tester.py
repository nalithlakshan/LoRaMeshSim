
import simpy
import random
import numpy as np
import math
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg

N = 20
at = 1712 #ms
DER = 0.7
avgSendTime = 30000
lambd = 1/avgSendTime

device1_packets = 0
device2_packets = 0
device3_packets = 0
no_of_collisions_dev3 = 0

T1 = 0
T2 = 0
T3 = 0

def device1():
    global device1_packets
    global device3_packets
    global T1
    while(device3_packets<100000):
        T1 = 0
        yield env.timeout(random.expovariate(1.0/float(avgSendTime)))
        T1 = 1
        yield env.timeout(at)
        device1_packets += 1
    
def device2():
    global device2_packets
    global device3_packets
    global T2
    while(device3_packets<100000):
        T2 = 0
        yield env.timeout(random.expovariate(1.0/float(avgSendTime)))
        T2 = 1
        yield env.timeout(at)
        device2_packets += 1

def device3():
    global device3_packets
    global no_of_collisions_dev3
    global T3
    while(device3_packets<100000):
        T3 = 0
        yield env.timeout(random.expovariate(1.0/float(avgSendTime)))
        col =0
        T3 = 1
        if(T1 == 1 or T2 == 1):
            col = 1
        yield env.timeout(at)
        device3_packets += 1
        if(T1 == 1 or T2 == 1):
            col = 1
        no_of_collisions_dev3 += col
        col =0

env = simpy.Environment()
env.process(device1())
env.process(device2())
env.process(device3())
env.run()

print(device1_packets)
print(device2_packets)
print(device2_packets)
print(no_of_collisions_dev3)

p = at*lambd
u = 1/at/1000

print("collision rate = p  =", (N*lambd/(u+N*lambd)))
print("calc collision rate =", no_of_collisions_dev3/device2_packets)