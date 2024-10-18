import matplotlib.pyplot as plt
import numpy as np

# X- Number of relays in chain
x =  [5, 10, 15, 20]

# Y- Probability of successful delivery

# No sf,freq,timing,pwr collision detection. (causes hidden terminal problem)
# carrier sensing by relays. when medium is idle forward after a random waiting period (~100ms mean)
# When a relay is in transmit state (waiting to transmit/ transmitting) it loses its receiving packets.
# y1 = [0.980, 0.942, 0.889, 0.832] # 1 tag per relay
# y2 = [0.959, 0.888, 0.805, 0.714] # 2 tag per relay
# y3 = [0.940, 0.843, 0.733, 0.638] # 3 tag per relay
# y4 = [0.923, 0.799, 0.685, 0.569] # 4 tag per relay

# sf,freq collision detection is included. 
# carrier sensing by relays. when medium is idle forward after a random waiting period (~100ms mean)
# When a relay is in transmit state (waiting to transmit/ transmitting) it loses its receiving packets.
y1 = [0.975, 0.933, 0.869, 0.811] # 1 tag per relay
y2 = [0.950, 0.867, 0.776, 0.680] # 2 tag per relay
y3 = [0.931, 0.818, 0.697, 0.600] # 3 tag per relay
y4 = [0.908, 0.766, 0.638, 0.539] # 4 tag per relay

# Create line plots
plt.plot(x, y1, label='1 tag per relay')
plt.scatter(x, y1)
plt.plot(x, y2, label='2 tag per relay')
plt.scatter(x, y2)
plt.plot(x, y3, label='3 tag per relay')
plt.scatter(x, y3)
plt.plot(x, y4, label='4 tag per relay')
plt.scatter(x, y4)

# Set x-axis and y-axis ranges
plt.xlim(5, 20)
plt.ylim(0, 1) 

y_ticks = np.arange(0, 1.1, 0.1) 
plt.yticks(y_ticks)
plt.grid(axis='y')

# Set plot title and labels
plt.title("Uniform Tag Distributions")
plt.xlabel("Number of Relays")
plt.ylabel("Probability of Successful Delivery")

# Add legend
plt.legend()

# Display the plot
plt.show()
input('Press Enter to continue ...')