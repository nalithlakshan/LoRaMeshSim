import matplotlib.pyplot as plt
import numpy as np

# X- Number of Hops from Headend
x =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Y- Probability of successful delivery

# No sf,freq,timing,pwr collision detection. (causes hidden terminal problem)
# carrier sensing by relays. when medium is idle forward after a random waiting period (~100ms mean)
# When a relay is in transmit state (waiting to transmit/ transmitting) it loses its receiving packets.
# y1 = [0.983, 0.974, 0.968, 0.950, 0.944, 0.935, 0.924, 0.910, 0.904, 0.883] # 1 tag per relay
# y2 = [0.967, 0.940, 0.932, 0.918, 0.895, 0.879, 0.860, 0.843, 0.820, 0.801] # 2 tag per relay
# y3 = [0.955, 0.928, 0.900, 0.885, 0.850, 0.824, 0.809, 0.780, 0.750, 0.713] # 3 tag per relay
# y4 = [0.938, 0.910, 0.883, 0.850, 0.815, 0.785, 0.753, 0.717, 0.700, 0.654] # 4 tag per relay

# sf,freq collision detection is included. 
# carrier sensing by relays. when medium is idle forward after a random waiting period (~100ms mean)
# When a relay is in transmit state (waiting to transmit/ transmitting) it loses its receiving packets.
y1 = [0.976, 0.969, 0.954, 0.946, 0.933, 0.918, 0.909, 0.897, 0.880, 0.878] # 1 tag per relay
y2 = [0.963, 0.935, 0.926, 0.893, 0.879, 0.855, 0.839, 0.806, 0.783, 0.770] # 2 tag per relay
y3 = [0.949, 0.911, 0.888, 0.860, 0.839, 0.807, 0.776, 0.745, 0.711, 0.675] # 3 tag per relay
y4 = [0.937, 0.900, 0.866, 0.816, 0.787, 0.756, 0.715, 0.680, 0.648, 0.611] # 4 tag per relay

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
# plt.xlim(5, 20)
plt.ylim(0, 1) 

y_ticks = np.arange(0, 1.1, 0.1) 
plt.yticks(y_ticks)
plt.grid(axis='y')

# Set plot title and labels
plt.title("Fairness Evaluation for a 10 Relay Network")
plt.xlabel("Number of Hops from Headend")
plt.ylabel("Probability of Successful Delivery")

# Add legend
plt.legend()

# Display the plot
plt.show()
input('Press Enter to continue ...')