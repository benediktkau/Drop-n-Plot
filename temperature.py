import matplotlib.animation as ani
import matplotlib.pyplot as plt
import pandas as pd


def main():
    font = {'family': 'Verdana',
            'weight': 'normal',
            'size': 8,
            'color': 'grey'
            }

    timeInterval = 'day'
    filename = 'covid.csv'

    df, dfType = readData(filename)

    df.plot()
    plt.show()
    return

    # Smoothening
    smootheningMethod = 'cubic'
    df = smoothening(df, smootheningMethod)

    return

    # Layout
    fig, ax = plt.subplots()
    plt.ylabel('Degrees', fontdict=font, rotation='horizontal', loc='top')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    plt.xticks(fontsize=8, color='grey')
    plt.yticks(fontsize=8, color='grey')
    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')

    # plt.show
    # plt.savefig('chart.png')
    # return 

    # Animation
    def animate(i):
        plt.plot(df[:i].index, df[:i].values, 'darkorange')
        plt.title('Temperature \n' + str(df.index[i].strftime('%Y')))

    animator = ani.FuncAnimation(fig, animate, interval=50, frames=df.size - 1)
    animator.save('temperature.gif', dpi=200)


def readData(filename):
    df = pd.read_csv(filename, delimiter=',', header='infer', squeeze=True, index_col=0, parse_dates=True)
    if isinstance(df, pd.Series):
        df.index = pd.to_datetime(df.index, format='%Y')
        dfType = 'Series'
    else:
        # df.transpose()
        print(df)

        dfType = 'DataFrame'
    return df, dfType


def smoothening(df, method):
    # https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
    df_resampled = df.resample('Q').mean()  # add months to data
    df_interpolated = df_resampled.interpolate(method=method)
    return df_interpolated


main()
