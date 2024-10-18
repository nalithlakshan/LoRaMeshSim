import matplotlib.pyplot as plt
import numpy as np
import random


data = []

for i in range(1000000):
    data.append(random.expovariate(1.0/5.0))
    # data.append(random.uniform(2.5,7.5))
    # data.append(np.random.normal(5.0,1))

plt.hist(data, bins=100, density=True, alpha=0.7, color='b')
# plt.title("Exponential Distribution with Mean=5")
# plt.title("Uniform Distribution with Mean=5")
plt.title("Normal Distribution with Mean=5 Variance =1")
plt.xlabel("Random Variable")
plt.ylabel("Probability Density")
plt.show()