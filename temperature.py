import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sc

def main():

    font = {'family': 'Verdana',
            'color':  'black',
            'weight': 'normal',
            'size': 8,
            'color': 'grey'
            }

    # new attempt with temperature
    df = pd.read_csv('temperature.csv', delimiter=',', header='infer', squeeze=True, index_col=0)
    df.index = pd.to_datetime(df.index, format='%Y')
    
    # Smoothening
    smootheningMethod = 'cubic'
    df = smoothening(df, smootheningMethod)

    # Layout
    fig, ax = plt.subplots()
    plt.ylabel('Degrees',fontdict=font, rotation='horizontal', verticalalignment='baseline', loc='top')
    #plt.xlabel('Years',fontdict=font)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    plt.xticks(fontsize=8, color='grey')
    plt.yticks(fontsize=8, color='grey')
    plt.plot(df.index, df.values, 'cornflowerblue')
    plt.show
    plt.savefig('chart.png')
    return

    def animate(i):
        plt.plot(df[:i].index, df[:i].values, 'cornflowerblue')
        plt.title('Temperature \n' + str(df.index[i].strftime('%Y')))
 
    import matplotlib.animation as ani
    animator = ani.FuncAnimation(fig, animate, interval = 50, frames=df.size-1)
    animator.save('temperature.gif', dpi=200)

def smoothening(df, method):
    # https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
    df_resampled = df.resample('Q').mean() #add months to data
    df_interpolated = df_resampled.interpolate(method=method)
    df = df_interpolated
    return df_interpolated
    
main()