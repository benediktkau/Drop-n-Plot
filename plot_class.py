import logging
import matplotlib as plt  # pyplot
import matplotlib.pyplot
plt.use('Agg')
import pandas as pd
import datetime
import helpers

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}


class Plot:
    def __init__(self, filepath):
        self.filepath = filepath

    def main(self, plotTitle):
        """

        :param plotTitle:
        :return:
        """

        font = {'family': 'Verdana',
                'weight': 'normal',
                'size': 8,
                'color': 'grey'
                }

        timeInterval = 'day'

        try:
            df, dfType = self.readData(self.filepath)
        except FileNotFoundError as e:
            logging.critical('File not found', e)
            exit(1)

        print(df)
        print(dfType)

        # Smoothening
        smootheningMethod = 'cubic'
        # df = self.smoothening(df, smootheningMethod)

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
            """

            :param i:
            :return:
            """

            #plt.pyplot.legend(df.columns)
            plt.pyplot.plot(df[:i].index, df[:i].values, 'darkorange')
            plt.pyplot.title(plotTitle + '\n' + str(df.index[i].strftime('%Y')))

        plotFilename = self.fileName()

        animator = plt.animation.FuncAnimation(fig, animate, interval=50, frames=df.size - 1)
        animator.save('plotFilename.gif', dpi=100)

        return plotFilename

    def readData(self, filename):
        """
        Read data

        :param filename:
        :return:
        """

        # Get delimiter
        delimiter = helpers.detect_delimiter(filename)

        # Read Dataframe or Series
        df = pd.read_csv(filename, delimiter=delimiter, header='infer', squeeze=True, index_col=0, parse_dates=True)

        if isinstance(df, pd.Series):
            df.index = pd.to_datetime(df.index, format='%Y')
            dfType = 'Series'
        else:
            df = df.transpose()
            df.index = pd.to_datetime(df.index)
            dfType = 'DataFrame'
        return df, dfType

    @staticmethod
    def fileName():
        """

        :return:
        """

        now = datetime.datetime.now()
        folder = 'static/'
        return folder + now.strftime("plot_%Y-%m-%d_%H:%M:%S.gif")

    @staticmethod
    def smoothening(df, method):
        """

        :param df:
        :param method:
        :return:
        """

        # https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
        df_resampled = df.resample('Q').mean()  # add quarters to data
        df_interpolated = df_resampled.interpolate(method=method)
        return df_interpolated


if __name__ == '__main__':
    new_plot = Plot('src/temperature.csv')
    new_plot.main('new plot on christmas')
