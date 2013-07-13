#p2_e
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#the parameter
alpha=2
xmin=1
#generate the number
r = np.random.rand(100000)
x = xmin*(1-r)**(-1/(alpha-1))

alpha=1+len(x)*(np.sum(np.log(x)))**(-1) #1.9990980075445199
