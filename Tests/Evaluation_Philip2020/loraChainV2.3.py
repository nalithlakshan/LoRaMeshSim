import simpy
import random
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Rectangle

# Debug Mode
debug = 0

# turn on/off graphics
graphics = 1

# do the full collision check
full_collision = False

#carrier sensing
carrier_sensing_ed = False
carrier_sensing_rp = True

# Averaege packet sending interval of end devices
avgSendTime = 60000 #60 seconds

# Simulation Time
# simtime = 5 * avgSendTime

# experiments:
# 0: packet with longest airtime, aloha-style experiment
# 1: one with 3 frequencies, 1 with 1 frequency
# 2: with shortest packets, still aloha-style
# 3: with shortest possible packets depending on distance
# 4: all packets --> SF=7 BW=500 CR=1
experiment = 4

# These are arrays with measured values for sensitivity
#---------------SF---125-----250-----500----(BW in kHz)
sf7  = np.array([7, -126.50,-124.25,-120.75])
sf8  = np.array([8, -127.25,-126.75,-124.00])
sf9  = np.array([9, -131.25,-128.25,-127.50])
sf10 = np.array([10,-132.75,-130.25,-128.75])
sf11 = np.array([11,-134.50,-132.75,-128.75])
sf12 = np.array([12,-133.25,-132.25,-132.25])


#COLLISION CHECK
# check for collisions at receiver
def checkcollision(packet, receiverNode):

    col = 0 # flag needed since there might be several collisions for packet
    processing = 0

    for i in range(0,len(receiverNode.packetSourcesAtRx)):
        if receiverNode.packetSourcesAtRx[i].packet[receiverNode.id].processed == 1:
            processing = processing + 1
    if (processing >= maxRxReceives):
        print ("Too many packets at the receiver node. No of packets:", len(receiverNode.packetSourcesAtRx))
        packet.processed = 0
    else:
        packet.processed = 1

    if(debug):
        print ("CHECK collision for packet-{} from node {} to node {} (sf:{} bw:{}kHz freq:{:.0f}MHz) No of other packets at rx: {}".format(
            packet.seqNr, packet.nodeid,receiverNode.id, packet.sf, packet.bw, packet.freq/10.0**6, len(receiverNode.packetSourcesAtRx)-1))
    
    if(receiverNode.transmittingState == 1 and receiverNode.id != packet.nodeid):
            packet.collided = 1
            col =1
            if(debug):
                print("   --collision since node",receiverNode.id,"is in transmitting state")

    if receiverNode.packetSourcesAtRx:
        for other in receiverNode.packetSourcesAtRx:
            if other.id != packet.nodeid: 
                if(debug):
                    print (">> node {} (sf:{} bw:{}kHz freq:{:.0f}MHz)".format(
                        other.id, other.packet[receiverNode.id].sf, other.packet[receiverNode.id].bw, other.packet[receiverNode.id].freq/10.0**6))
                # simple collision
                if frequencyCollision(packet, other.packet[receiverNode.id]) \
                    and sfCollision(packet, other.packet[receiverNode.id]):
                    if full_collision:
                        if timingCollision(packet, other.packet[receiverNode.id]):
                            # check who collides in the power domain
                            c = powerCollision(packet, other.packet[receiverNode.id]) #returns a tuple of pwr collided packets
                            # 'c' may include either this packet, or the other packet, or both
                            for p in c:
                                p.collided = 1
                                if(p == packet):
                                    col = 1
                        else:
                            # no timing collision, all fine
                            pass
                    else:
                        packet.collided = 1
                        other.packet[receiverNode.id].collided = 1  # other packet also got collided, if it wasn't collided already
                        col = 1
        return col
    
    return col

#
# frequencyCollision, conditions
#
#        |f1-f2| <= 120 kHz if f1 or f2 has bw 500
#        |f1-f2| <= 60 kHz if f1 or f2 has bw 250
#        |f1-f2| <= 30 kHz if f1 or f2 has bw 125
def frequencyCollision(p1,p2):
    if (abs(p1.freq-p2.freq)<=120 and (p1.bw==500 or p2.freq==500)):  #240 not 120 ????????
        if(debug):
            print ("   --collision frequency at 500kHz bw")
        return True
    elif (abs(p1.freq-p2.freq)<=60 and (p1.bw==250 or p2.freq==250)): #120 not 60 ?????????
        if(debug):    
            print ("   --collision frequency at 250kHz bw")
        return True
    else:
        if (abs(p1.freq-p2.freq)<=30):                                #60 not 30 (at CF=125kHz) ??????????
            if(debug):
                print ("   --collision frequency at 125kHz bw")
            return True
        #else:
    if(debug):
        print ("   --no frequency coll")
    return False

def sfCollision(p1, p2):
    if p1.sf == p2.sf:
        if(debug):
            print ("   --collision sf node {} and node {}".format(p1.nodeid, p2.nodeid))
        # p2 may have been lost too, will be marked by other checks
        return True
    if(debug):
        print ("   --no sf collision")
    return False

def powerCollision(p1, p2):
    powerThreshold = 6 # dB
    print ("   --pwr: node {0.nodeid} {0.rssi:3.2f} dBm node {1.nodeid} {1.rssi:3.2f} dBm; diff {2:3.2f} dBm".format(p1, p2, round(p1.rssi - p2.rssi,2)))
    if abs(p1.rssi - p2.rssi) < powerThreshold:
        print ("   --collision pwr both node {} and node {}".format(p1.nodeid, p2.nodeid))
        # packets are too close to each other, both collide
        # return both packets as casualties
        return (p1, p2)
    elif p1.rssi - p2.rssi < powerThreshold:
        # p2 overpowered p1, return p1 as casualty
        print ("   --collision pwr node {} overpowered node {}".format(p2.nodeid, p1.nodeid))
        return (p1,)
    print ("   --p1 wins, p2 lost")
    # p2 was the weaker packet, return it as a casualty
    return (p2,)

def timingCollision(p1, p2):
    # assuming p1 is the freshly arrived packet and this is the last check
    # we've already determined that p1 is a weak packet, so the only
    # way we can win is by being late enough (only the first n - 5 preamble symbols overlap)

    # assuming 8 preamble symbols
    Npream = 8

    # we can lose at most (Npream - 5) * Tsym of our preamble
    Tpreamb = 2**p1.sf/(1.0*p1.bw) * (Npream - 5)

    # check whether p2 ends in p1's critical section
    p2_end = p2.addTime + p2.rectime
    p1_cs = env.now + Tpreamb
    print ("   --collision timing node {} ({},{},{}) node {} ({},{})".format(
        p1.nodeid, env.now - env.now, p1_cs - env.now, p1.rectime,
        p2.nodeid, p2.addTime - env.now, p2_end - env.now
    ))
    if p1_cs < p2_end:
        # p1 collided with p2 and lost
        print ("   --not late enough")
        return True
    print ("   --saved by the preamble")
    return False

# this function computes the airtime of a packet
# according to LoraDesignGuide_STD.pdf
#
def airtime(sf,cr,pl,bw):
    '''
    H = 0        # implicit header disabled (H=0) or not (H=1)
    DE = 0       # low data rate optimization enabled (=1) or not (=0)
    Npream = 8   # number of preamble symbol (12.25  from Utz paper)

    if bw == 125 and sf in [11, 12]:
        # low data rate optimization mandated for BW125 with SF11 and SF12
        DE = 1
    if sf == 6:
        # can only have implicit header with SF6
        H = 1

    Tsym = (2.0**sf)/bw
    Tpream = (Npream + 4.25)*Tsym
    print ("sf", sf, " cr", cr, "pl", pl, "bw", bw)
    payloadSymbNB = 8 + max(math.ceil((8.0*pl-4.0*sf+28+16-20*H)/(4.0*(sf-2*DE)))*(cr+4),0)
    Tpayload = payloadSymbNB * Tsym
    return Tpream + Tpayload 
    '''
    #Overide the airtime function with 11ms constant for SF=7 BW=500kHz CR=6/7
    return 11


#
# this class creates a node
#
class node():
    def __init__(self, env, x, y, type):
        global nodes
        nodes.append(self)
        self.id = len(nodes)-1
        self.x = x
        self.y = y
        self.type = type #3 TYPES: end device(ed), repeater(rp), gateway(gw)

        # properties common for all types
        self.packetSourcesAtRx = []
        self.recPackets = []
        self.packet = []
        self.dist = []

        #properties specific to end-devices
        self.sent = 0
        self.period = avgSendTime
        self.packetlen = 30

        #properties specific to repeaters
        self.packetsFifo = simpy.Store(env)
        self.nTransmitters = simpy.Resource(env, capacity=1)
        self.transmittingState = 0

        # graphics for node
        global graphics
        if (graphics == 1):
            global ax
            if  (self.type.lower() == "ed"):
                ax.add_artist(plt.Circle((self.x, self.y), 5, fill=True, color='blue'))
                ax.add_artist(plt.text(self.x+6,self.y,self.id))
            elif(self.type.lower() == "rp"):
                ax.add_artist(plt.Circle((self.x, self.y), 10, fill=True, color='green'))
                ax.add_artist(plt.text(self.x+11,self.y,self.id))
            elif(self.type.lower() == "gw"):
                ax.add_artist(plt.Circle((self.x, self.y), 10, fill=True, color='red'))
                ax.add_artist(plt.text(self.x+11,self.y,self.id))
            else:
                print("Incorrect device type!")

    def createPackets(self):
        # create "virtual" packet for each other node
        for i in range(0,len(nodes)):
            d = np.sqrt((self.x-nodes[i].x)*(self.x-nodes[i].x)+(self.y-nodes[i].y)*(self.y-nodes[i].y))
            self.dist.append(d)
            self.packet.append(myPacket(self.id, 20, self.dist[i], i)) #for now packetlen is set to const 20 as default value
        print(self.type.upper(),":",self.id, "x", self.x, "y", self.y, "dist: ", self.dist)

    #only for the transmission by end-devices
    def transmit(self, env):
        while(True):
            yield env.timeout(random.expovariate(1.0/float(self.period)))

            #carrier sensing
            if(carrier_sensing_ed ==1): 
                while(len(self.packetSourcesAtRx) != 0):
                    yield env.timeout(1)
                    if(debug):
                        print("waiting till medium is idle")
            
            global packetSeq
            packetSeq = packetSeq + 1

            global totalSimPackets
            if (packetSeq > totalSimPackets):
                break

            self.sent = self.sent + 1

            global nodes
            global lostPackets
            global collidedPackets

            if(debug):
                print(f"\nT = {env.now:.2f}| Node {self.id}({self.type.upper()}) Transmitted Packet:{self.id}|{packetSeq}")

            for i in range(0, len(nodes)):
                self.packet[i].addTime = env.now
                self.packet[i].seqNr = f"{self.id}|{packetSeq}"
                
                if(self.packet[i].lost == 0): #checking if the packet reachs at node[i]
                    if (self in nodes[i].packetSourcesAtRx):
                        print("ERROR: packet",self.packet[i].seqNr, "from node",self.id,"is already in node",i,"RX")
                    else:
                        nodes[i].packetSourcesAtRx.append(self)
                        # checking collision at the start of packet reception
                        if (checkcollision(self.packet[i], nodes[i])==1):
                            self.packet[i].collided = 1
                        else:
                            self.packet[i].collided = 0
            
            # air time (take first packet rectime)
            yield env.timeout(self.packet[0].rectime)

            # if packet did not collide, add it in list of received packets
            # unless it is already in
            for i in range(0, len(nodes)):
                if(i != self.id):
                    if self.packet[i].lost:
                        lostPackets.append(f"{nodes[i].type.upper()}:{nodes[i].id} SeqNr:{self.packet[i].seqNr}")
                    else:
                        if ((self.packet[i].collided == 0) and (self.packet[i].processed == 1)):
                            if (self.packet[i].seqNr not in nodes[i].recPackets):
                                nodes[i].recPackets.append(self.packet[i].seqNr)
                                env.process(nodes[i].receive(env, self.packet[i].seqNr, self.packetlen))
                        else:
                            # XXX only for debugging
                            collidedPackets.append(f"{nodes[i].type.upper()}:{nodes[i].id} SeqNr:{self.packet[i].seqNr}")

            # complete packet has been received by base station
            # can remove it
            for i in range(0, len(nodes)):
                if (self in nodes[i].packetSourcesAtRx):
                    nodes[i].packetSourcesAtRx.remove(self)
                # reset the packet
                self.packet[i].collided = 0
                self.packet[i].processed = 0


    def receive(self, env, seqNr, packetlen):
        # yield env.timeout(repeaterProcessingTime) #wait for the processing time

        #check if it is a gateway
        if (self.type.lower() == "gw"):
            #Do no more transmissions. Account the packets received.
            # print("T =",env.now, "|GW",self.id, "Received Packet:",seqNr,"\n")
            if(debug):
                print(f"\nT = {env.now:.2f}| Node {self.id}({self.type.upper()}) Received Packet:{seqNr}")
            if seqNr not in packetsRecBS:
                packetsRecBS.append(seqNr)

        #check if it is an end-device
        elif (self.type.lower() == "ed"):
            # print("T =",env.now, "|ED",self.id, "Received Packet:",seqNr,"\n")
            if(debug):
                print(f"\nT = {env.now:.2f}| Node {self.id}({self.type.upper()}) Received Packet:{seqNr}")
        
        #if it is a repeater
        else:
            # yield env.process(self.repeat(env, seqNr, packetlen))
            if(debug):
                print(f"\nT = {env.now:.2f}| Node {self.id}({self.type.upper()}) Received Packet:{seqNr}")
            packetInfo = [seqNr,packetlen]
            self.packetsFifo.put(packetInfo)
            with self.nTransmitters.request() as req:
                yield req
                packetInfoOut = yield self.packetsFifo.get()
                yield env.process(self.repeat(env, packetInfoOut[0], packetInfoOut[1]))


    def repeat(self, env, seqNr, packetlen):
        global nodes
        global packetsRecBS
        global collidedPackets
        global lostPackets
        global repeaterProcessingTime

        # #carrier sensing
        if(carrier_sensing_rp ==1): 
            while(len(self.packetSourcesAtRx) != 0):
                yield env.timeout(1)
                if(debug):
                    print("waiting till medium is idle")

        self.transmittingState = 1
        yield env.timeout(random.expovariate(1.0/float(100))) #wait random time with mean =100ms

        if(debug):
            print(f"\nT = {env.now:.2f}| Node {self.id}({self.type.upper()}) Forwarded Packet:{seqNr}")
        
        for i in range(0, len(nodes)): #add the transmitting node itself too at its own rx
            self.packet[i].addTime = env.now
            self.packet[i].seqNr = seqNr

            if(self.packet[i].lost == 0): #checking if the packet reachs at node[i]
                if (self in nodes[i].packetSourcesAtRx):
                    print("ERROR: Packet",self.packet[i].seqNr, "from node",self.id,"is already in node",i,"RX")
                else:
                    nodes[i].packetSourcesAtRx.append(self) 
                    # checking collision at the start of packet reception
                    if (checkcollision(self.packet[i], nodes[i])==1):
                        self.packet[i].collided = 1
                    else:
                        self.packet[i].collided = 0
        
        # air time (take first packet rectime)
        yield env.timeout(self.packet[0].rectime)
        self.transmittingState = 0

        # if packet did not collide, add it in list of received packets
        # unless it is already in
        for i in range(0, len(nodes)):
            if(i != self.id):
                if (self.packet[i].lost):
                    lostPackets.append(f"{nodes[i].type.upper()}:{nodes[i].id} SeqNr:{self.packet[i].seqNr}")
                else:
                    if (self.packet[i].collided == 0):
                        if (self.packet[i].seqNr not in nodes[i].recPackets):
                            nodes[i].recPackets.append(self.packet[i].seqNr)
                            env.process(nodes[i].receive(env, self.packet[i].seqNr, packetlen))
                    else:
                        # XXX only for debugging
                        collidedPackets.append(f"{nodes[i].type.upper()}:{nodes[i].id} SeqNr:{self.packet[i].seqNr}")

        # complete packet has been received by base station
        # can remove it
        for i in range(0, len(nodes)):
            if (self in nodes[i].packetSourcesAtRx):
                nodes[i].packetSourcesAtRx.remove(self)
            # reset the packet
            self.packet[i].collided  = 0
            self.packet[i].processed = 0
    

#
# this function creates a packet (associated with a node)
# it also sets all parameters, currently random
#
class myPacket():
    def __init__(self, nodeid, plen, distance, rxRepeaterId):
        global experiment
        global Ptx
        global gamma
        global d0
        global var
        global Lpld0
        global GL
        global minsensi
        self.seqNr = None


        # new: base station ID
        self.rxRepeaterId = rxRepeaterId
        self.nodeid = nodeid
        # randomize configuration values
        # self.sf = random.randint(6,12)
        # self.cr = random.randint(1,4)
        # self.bw = random.choice([125, 250, 500])
        self.sf = 7
        self.cr = 1
        self.bw = 500
        self.freq = 860000000


        # for certain experiments override these
        # if experiment==1 or experiment == 0:
        #     self.sf = 12
        #     self.cr = 4
        #     self.bw = 125

        # for certain experiments override these
        # if experiment==2:
        #     self.sf = 6
        #     self.cr = 1
        #     self.bw = 500


        # for experiment 3 find the best setting
        # OBS, some hardcoded values
        Prx = Ptx  ## zero path loss by default

        # log-shadow
        print("Distance", distance)

        if(distance != 0):
            Lpl = Lpld0 + 10*gamma*math.log10(distance/d0)
        else:
            Lpl = 0
        print ("Ptx: ",Ptx)
        print ("Lpl: ",Lpl)
        Prx = Ptx - GL - Lpl
        print ("Prx: ", Prx)
        print ("MinSensi: ",minsensi)

        if (experiment == 3):
            minairtime = 9999
            minsf = 0
            minbw = 0

            for i in range(0,6):
                for j in range(1,4):
                    if (sensi[i,j] < Prx):
                        self.sf = sensi[i,0]
                        if j==1:
                            self.bw = 125
                        elif j==2:
                            self.bw = 250
                        else:
                            self.bw=500
                        at = airtime(self.sf,4,20,self.bw)
                        if at < minairtime:
                            minairtime = at
                            minsf = self.sf
                            minbw = self.bw

            self.rectime = minairtime
            self.sf = minsf
            self.bw = minbw
            if (minairtime == 9999):
                print ("does not reach the destination node")
                exit(-1)

        # transmission range, needs update XXX
        self.transRange = 150
        self.pl = plen
        self.symTime = (2.0**self.sf)/self.bw
        self.arriveTime = 0
        self.rssi = Prx
        # frequencies: lower bound + number of 61 Hz steps
        self.freq = 860000000 + random.randint(0,2622950)

        # for certain experiments override these and
        # choose some random frequences
        if experiment == 1:
            self.freq = random.choice([860000000, 864000000, 868000000])
        else:
            self.freq = 860000000

        self.rectime = airtime(self.sf,self.cr,self.pl,self.bw)
        # denote if packet is collided
        self.collided = 0
        self.processed = 0
        # mark the packet as lost when it's rssi is below the sensitivity
        # don't do this for experiment 3, as it requires a bit more work
        if experiment != 3:
            self.lost = self.rssi < minsensi
            print ("node {} rxRepeaterId {} lost {}".format(self.nodeid, self.rxRepeaterId, self.lost))

def networkConfig():
    global nodes
    for i in range(len(nodes)):
        nodes[i].createPackets()

# ----------------------------------------------------------------------------------
# "main" program
# ----------------------------------------------------------------------------------

# global stuff
env = simpy.Environment()

# global value of packet sequence numbers
packetSeq = 0

# list of nodes
nodes = []
repeaterProcessingTime = 100
# maximum number of packets the node rx can receive at the same time
maxRxReceives = 8

# list of received packets (accounting reception at all the nodes)
collidedPackets=[]
lostPackets = []
#global packet seq numbers received at gateways
packetsRecBS = []

# max distance: 300m in city, 3000 m outside (5 km Utz experiment)
# also more unit-disc like according to Utz
# nrCollisions = 0
# nrReceived = 0
# nrProcessed = 0

#Path loss function parameters
Ptx = 14
gamma = 2.08
d0 = 40.0
var = 0           # variance ignored for now
Lpld0 = 127.41
GL = 0

sensi = np.array([sf7,sf8,sf9,sf10,sf11,sf12])

## figure out the minimal sensitivity for the given experiment
minsensi = -200.0
if experiment in [0,1,4]:
    minsensi = sensi[5,2]  # 5th row is SF12, 2nd column is BW125
elif experiment == 2:
    minsensi = -112.0   # no experiments, so value from datasheet
elif experiment == [3, 5]:
    minsensi = np.amin(sensi) ## Experiment 3 can use any setting, so take minimum

Lpl = Ptx - minsensi
print ("amin", minsensi, "Lpl", Lpl)
maxDist = d0*(10**((Lpl-Lpld0)/(10.0*gamma))) #CORRECTED MISTAKE HERE: REPLACED 'e' with 10
print ("maxDist:", maxDist)

# base station placement
# bsx = maxDist+10
# bsy = maxDist+10
# xmax = bsx + maxDist + 20
# ymax = bsy + maxDist + 20
# maxX = 2 * maxDist * math.sin(60*(math.pi/180)) # == sqrt(3) * maxDist
# print "maxX ", maxX
# maxY = 2 * maxDist * math.sin(30*(math.pi/180)) # == maxdist
# print "maxY", maxY 
# maxDist = 100


#-------------------------------------------------------------------------------------
# Simulation config
#-------------------------------------------------------------------------------------
# no_of_repeaters = int(input("Number of repeaters: "))
# no_of_tags_per_repeater = int(input("Number of tags per repeater: "))
# sim_time = int(input("Simulation Time in Minutes: "))
no_of_repeaters = 10
no_of_tags_per_repeater = int(input("Number of tags per repeater: "))
sim_time = int(input("Simulation Time in Minutes: "))

xmax = (no_of_repeaters+2)*maxDist
ymax = 4*maxDist

# prepare graphics and add sink
if (graphics == 1):
    plt.ion()
    plt.figure()
    ax = plt.gcf().gca()

    ax.add_patch(Rectangle((0, 0), xmax, ymax, fill=None, alpha=1))

# Generating Nodes
for i in range(no_of_repeaters):
    node(env, (i+1)*maxDist*0.99, 2*maxDist*0.99, "rp")
    for j in range(no_of_tags_per_repeater):
        node(env, (i+1)*maxDist*0.99, (2+1/(j+1))*maxDist*0.99, "ed")

gw = node(env, (no_of_repeaters+1)*maxDist*0.99, 2*maxDist*0.99, "gw")   

networkConfig()

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
if (graphics == 1):
    plt.xlim([0, xmax])
    plt.ylim([0, ymax])
    plt.draw()
    plt.show()

# start simulation
# env.run(until=simtime)
totalSimPackets = no_of_repeaters * no_of_tags_per_repeater *sim_time
env.run()

#-----------------------------------------------------------------------
#Print simulation stat
print ("No of nodes: ", len(nodes)) #FIX
print ("AvgSendTime (exp. distributed):",avgSendTime)
print ("Experiment: ", experiment)
print ("Full Collision: ", full_collision)

#print "sent packets: ", sent
print ("sent packet seq numbers: ", totalSimPackets)

# print received packets at each repeater/gateway FIX
if(debug):
    for i in range(0,len(nodes)):
        if(nodes[i].type.lower() == "rp"):
            print("\npackets received at Repeater",nodes[i].id, ":", nodes[i].recPackets) 
        elif(nodes[i].type.lower() == "gw"):
            print("\npackets received at Gateway",nodes[i].id, ":", nodes[i].recPackets) 
        # else:
        #     print("\npackets received at End-device",nodes[i].id, ":", nodes[i].recPackets) 

if(debug):
    # print all collisions and losses
    print ("collided packets: ", collidedPackets)
    # print ("lost packets: ", lostPackets)
    print("gw received packets: ", packetsRecBS)

#Simulation Time
print("\nSImulation Time: ",env.now/60000,"mins")

# data extraction rate
der = len(packetsRecBS)/float(totalSimPackets)
print("DER:", der)

sent_packets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
recived_packets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for node in nodes:
    no_of_hops_index = 10 -round(node.x/maxDist*0.99)
    if(node.type.lower() == 'ed'):
        sent_packets[no_of_hops_index] += node.sent

        for seqNr in packetsRecBS:
            x,y =seqNr.split("|")
            if(node.id == int(x)):
                recived_packets[no_of_hops_index] += 1

print(sent_packets)
print(recived_packets)
print("\nProbabilities of Success")
for i in range(10):
    print(recived_packets[i]/float(sent_packets[i]))

# this can be done to keep graphics visible
if (graphics == 1):
    input('Press Enter to continue ...')