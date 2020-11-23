import matplotlib as plt # pyplot
import matplotlib.pyplot
plt.use('Agg')
import pandas as pd
import datetime
import os


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}


class Plot:
    def __init__(self, filepath):
        self.filepath = filepath

    def main(self, plotTitle):
        font = {'family': 'Verdana',
                'weight': 'normal',
                'size': 8,
                'color': 'grey'
                }

        timeInterval = 'day'

        df, dfType = self.readData(self.filepath)
            
        # Smoothening
        smootheningMethod = 'cubic'
        #df = self.smoothening(df, smootheningMethod)

        # Layout
        fig, ax = plt.pyplot.subplots()
        plt.pyplot.ylabel('Degrees', fontdict=font, rotation='horizontal', loc='top')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        plt.pyplot.xticks(fontsize=8, color='grey')
        plt.pyplot.yticks(fontsize=8, color='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')
    

        # Animation
        def animate(i):
            plt.pyplot.legend(df.columns)
            plt.pyplot.plot(df[:i].index, df[:i].values, 'darkorange')
            plt.pyplot.title(plotTitle + '\n' + str(df.index[i].strftime('%Y')))
        plotFilename = self.fileName()

        animator = plt.animation.FuncAnimation(fig, animate, interval=50, frames=df.size - 1)
        animator.save('plotFilename.gif', dpi=100)
        
        return plotFilename


    def readData(self, filename):
        df = pd.read_csv(filename, delimiter=',', header='infer', squeeze=True, index_col=0, parse_dates=True)
        if isinstance(df, pd.Series):
            df.index = pd.to_datetime(df.index, format='%Y')
            dfType = 'Series'
        else:
            df = df.transpose()
            df.index = pd.to_datetime(df.index)
            dfType = 'DataFrame'
        return df, dfType
    
    def fileName(self):
        now = datetime.datetime.now()
        folder = 'static/'
        return folder + now.strftime("plot_%Y-%m-%d_%H:%M:%S.gif")


    def smoothening(self, df, method):
        # https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
        df_resampled = df.resample('Q').mean()  # add quarters to data
        df_interpolated = df_resampled.interpolate(method=method)
        return df_interpolated
    
def deleteOldFiles():
    """ Delete .gif plot files older than 30 minutes to save storage space """
    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(currentDirectory + '/static'):
        
        if filename[0:4] == 'plot' and filename[-3:] == 'gif':
            stats = os.stat(currentDirectory + '/static/' + filename)
            lastEdited = datetime.datetime.fromtimestamp(stats.st_mtime)
            now = datetime.datetime.now()
            diff = (now - lastEdited).total_seconds() / 60 # get minutes since last modification
            if diff > 30:
                os.remove(currentDirectory + '/static/' + filename) 

if __name__ == "__main__":
    plot = Plot(filepath='src/covid.csv')
    deleteOldFiles()
    plot.main('title')
