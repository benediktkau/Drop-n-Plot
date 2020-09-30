import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# new attempt with temperature
df = pd.read_csv('temperature.csv', delimiter=',', header='infer', squeeze=True, infer_datetime_format=True, index_col=0)

fig, ax = plt.subplots()
plt.ylabel('Degrees')
plt.xlabel('Years')

def animate(i):
    plt.plot(df[:i].index, df[:i].values, 'b')

import matplotlib.animation as ani
animator = ani.FuncAnimation(fig, animate, interval = 50, frames=140)
animator.save('temperature.gif', dpi=200)