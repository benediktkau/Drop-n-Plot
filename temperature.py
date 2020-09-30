import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# new attempt with temperature
df3 = pd.read_csv('temperature.csv', delimiter=',', header='infer', squeeze=True, infer_datetime_format=True, index_col=0)
print(df3)


fig = plt.figure()
plt.ylabel('Degrees')
plt.xlabel('Years')
line.set_color("blue")

def buildmebarchart(i):
    p = plt.plot(df3[:i].index, df3[:i].values)

import matplotlib.animation as ani
animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)
animator.save('temperature.gif', dpi=200)