'''
Tag Distribution    Success Probability     Sim results (no sf,f col.)      Sim results (with sf,f col.)
----------------    -------------------     --------------------------      ----------------------------
16 0 0 0 0 0 0 0     0.974                  0.987                           0.978
8  8 0 0 0 0 0 0     0.966                  0.964                           0.955
4  4 4 4 0 0 0 0     0.948                  0.943                           0.932
2  2 2 2 2 2 2 2     0.924                  0.919                           0.905
0  0 0 0 4 4 4 4     0.923                  0.919                           0.904
0  0 0 0 0 0 8 8     0.920                  0.918                           0.903
0  0 0 0 0 0 0 16    0.924                  0.923                           0.908

Simulation Time is 5hr each with tags transmitting at a 1min mean interval {SF:7, BW:500kHz, CR:6/7, f:860Mhz}
'''
import matplotlib.pyplot as plt
import numpy as np


x = ['16 0..','8 8 0..','4 4 4 4 0..','2 2 2..2 2 2','..0 4 4 4 4','..0 8 8', '..0 16']
y1 = [0.974, 0.966, 0.948, 0.924, 0.923, 0.920, 0.924]
y2 = [0.987, 0.964, 0.943, 0.919, 0.919, 0.918, 0.923]
y3 = [0.978, 0.955, 0.932, 0.905, 0.904, 0.903, 0.908]

plt.ylim(0.8, 1)

# plt.plot(x, y1, label='Philip_2020')
# plt.scatter(x, y1)
# plt.plot(x, y2, label='Sim without col')
# plt.scatter(x, y2)
plt.plot(x, y3, label='Sim with col')
plt.scatter(x, y3)

# Set plot title and labels
plt.title("Skewed Tag Distributions")
plt.xlabel("Tag Distribution Types")
plt.ylabel("Probability of Successful Delivery")

# Add legend
# plt.legend()

# Display the plot
plt.show()
input('Press Enter to continue ...')