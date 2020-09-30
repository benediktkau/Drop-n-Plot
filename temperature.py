import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sc

def main():

    font = {'family': 'sans-serif',
            'color':  'black',
            'weight': 'normal',
            'size': 10,
            }

    # new attempt with temperature
    df = pd.read_csv('temperature.csv', delimiter=',', header='infer', squeeze=True, index_col=0)
    df.index = pd.to_datetime(df.index, format='%Y')
    
    # Smoothening
    df_resampled = df.resample('Q').mean() #add months to data
    
    df_interpolated = df_resampled.interpolate(method='cubic')
    df = df_interpolated
    print(df_interpolated)
    
    
    

    fig, ax = plt.subplots()
    plt.ylabel('Degrees',fontdict=font)
    plt.xlabel('Years',fontdict=font)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    def animate(i):
        plt.plot(df[:i].index, df[:i].values, 'cornflowerblue')

    import matplotlib.animation as ani
    animator = ani.FuncAnimation(fig, animate, interval = 50, frames=df.size-1)
    animator.save('temperature.gif', dpi=200)


main()