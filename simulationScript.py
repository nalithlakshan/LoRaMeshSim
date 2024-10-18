import loraMeshSimulator as sim

#-------------------------------------------------------------------------------------
# Simulation config
#-------------------------------------------------------------------------------------
node = sim.node
nodes = sim.nodes
env =sim.env
maxDist =sim.maxDist

gw = sim.node(env, 4.6*maxDist, 1*maxDist, "gw")

e1 = node(env, 1*maxDist, 1*maxDist, "ed")
e2 = node(env, 1.5*maxDist, 1.5*maxDist, "ed")
e3 = node(env, 1.5*maxDist, 0.5*maxDist, "ed")
e3 = node(env, 2.8*maxDist, 1.5*maxDist, "ed")

r1 = node(env, 1.9*maxDist, 1*maxDist, "rp")
r2 = node(env, 2.8*maxDist, 1*maxDist, "rp")
r3 = node(env, 3.7*maxDist, 1*maxDist, "rp")

sim.networkConfig()

#Sensor Network
for i in range(len(nodes)):
    if (nodes[i].type.lower() == "ed"):
        env.process(nodes[i].transmit(env))

#Actuator Network
# for i in range(len(nodes)):
#     if (nodes[i].type.lower() == "gw"):
#         print("HELLO!!!!!!!!!!!!!")
#         env.process(nodes[i].transmit(env))

#prepare show
if (sim.graphics == 1):
    sim.plt.xlim([0, sim.xmax])
    sim.plt.ylim([0, sim.ymax])
    sim.plt.draw()
    sim.plt.show()

# start simulation
sim.totalSimPackets = 5
env.run()

#-----------------------------------------------------------------------
#Print simulation stat
print ("No of nodes: ", len(nodes)) #FIX
print ("AvgSendTime (exp. distributed):",sim.avgSendTime)
print ("Experiment: ", sim.experiment)
print ("Simulation Time: ",env.now/60000,"mins")
print ("Full Collision: ", sim.full_collision)

#print "sent packets: ", sent
print ("sent packet seq numbers: ", sim.totalSimPackets)

#print received packets at each repeater/gateway FIX
for i in range(0,len(nodes)):
    if(nodes[i].type.lower() == "rp"):
        print("packets received at Repeater",nodes[i].id, ":", nodes[i].recPackets) 
    elif(nodes[i].type.lower() == "gw"):
        print("packets received at Gateway",nodes[i].id, ":", nodes[i].recPackets) 
    else:
        print("packets received at End-device",nodes[i].id, ":", nodes[i].recPackets) 

# print all collisions and losses
print ("collided packets: ", sim.collidedPackets)
print ("lost packets: ", sim.lostPackets)
print("gw received packets: ", sim.packetsRecBS)

# data extraction rate
der = len(sim.packetsRecBS)/float(sim.totalSimPackets)
print("DER:", der)

# this can be done to keep graphics visible
if (sim.graphics == 1):
    input('Press Enter to continue ...')