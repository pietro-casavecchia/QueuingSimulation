
# import numpy
import numpy as np
import matplotlib.pyplot as plt
  
# Using poisson() method
gfg = np.random.poisson(3, 100)
  
count, bins, ignored = plt.hist(gfg)
print(gfg)
plt.show()