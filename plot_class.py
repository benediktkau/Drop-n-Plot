import logging
import matplotlib as plt  # pyplot
import matplotlib.pyplot

plt.use('Agg')
import pandas as pd
import datetime
import helpers
import numpy as np

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

logging.basicConfig(filename='dropnplot_log',
                    level=logging.INFO,
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


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
            df, datetime_index = self.read_dataframe(self.filepath)
        except FileNotFoundError as e:
            logging.critical('File not found', e)
            exit(1)

        # Smoothening
        interpolation_method = 'cubic'

        if datetime_index: # interpolation for panda datetime index
            df = self.datetime_interpolation(df, interpolation_method)
        else: # standard interpolation
            df = self.standard_interpolation(df, interpolation_method)
            df.reset_index(drop=True, inplace=True)

        logging.info('Length dataframe' + str(len(df.index)))

        # Get xlim, ylim
        if datetime_index:
            xlim_init = (min(df.index), max(df.index))
            ylim_init = (min(df.values), max(df.values))
        else:
            xlim_init = (0.1 * min(df.index), 0.1 * max(df.index))
            ylim_init = (0, 0.3 * max(df.values))

        fig = plt.pyplot.figure()
        ax = plt.pyplot.axes(xlim=xlim_init, ylim=ylim_init)
        line, = ax.plot([], [], lw=2)

        def init():
            """

            :return:
            """
            line.set_data([], [])
            return line,

        plt.pyplot.ylabel('Degrees', fontdict=font, rotation='horizontal', loc='top')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        plt.pyplot.xticks(fontsize=8, color='grey')
        plt.pyplot.yticks(fontsize=8, color='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # plt.pyplot.plot(df.index, df.values)
        # plt.pyplot.savefig('newplot.png', dpi=200)

        # Animation
        def animate(i):
            """

            :param i:
            :return:
            """

            # plt.pyplot.legend(df.columns)
            # plt.pyplot.plot(df[:i].index, df[:i].values, 'darkorange')

            x = list(df.index[:i])
            y = df.values[:i]

            line.set_data(x, y)

            # Adapt ylim, xlim
            if not len(x) == 0 or not len(y) == 0:
                if df.index[i] < xlim_init[0] or df.index[i] > xlim_init[1]:
                    ax.set_xlim(0, max(x) * 1.01)

                if df.values[i] < ylim_init[0] or df.values[i] > ylim_init[1]:
                    ax.set_ylim(min(y), max(y) * 1.1)

            # print progress bar
            helpers.progress_bar(i + 2, len(df.index))

            # Add Title
            if datetime_index:
                plt.pyplot.title(plotTitle + '\n' + str(df.index[i].strftime('%Y')))
            else:
                plt.pyplot.title('\n'.join([plotTitle, str(int(df.index[i]))]))

            return line,

        filename_plot = self.create_filename()

        # Call animate() function
        animator = plt.animation.FuncAnimation(fig,
                                               animate,
                                               interval=50,
                                               frames=len(df.index) - 1,
                                               init_func=init,
                                               blit=True,
                                               repeat_delay=300)

        # Save file as gif
        animator.save(filename_plot, dpi=300)

        return filename_plot

    def read_dataframe(self, filename):
        """
        Read data

        :param filename:
        :return:
        """

        # Get delimiter
        delimiter = helpers.detect_delimiter(filename)

        # Read Dataframe or Series
        df = pd.read_csv(filename, delimiter=delimiter, header='infer', squeeze=True,
                         index_col=0 , parse_dates=True)

        # Check whether index is pd.datetime format
        if isinstance(df.index, pd.DatetimeIndex):
            datetime_index = True
            df.index = pd.to_datetime(df.index, format='%Y')
        else:
            datetime_index = False


        if isinstance(df, pd.Series):
            # df.index = pd.to_datetime(df.index, format='%Y')
            dfType = 'Series'
        else:
            df = df.transpose()
            # df.index = pd.to_datetime(df.index)
            dfType = 'DataFrame'

        return df, datetime_index

    @staticmethod
    def create_filename():
        """

        :return:
        """

        now = datetime.datetime.now()
        folder = 'static/'
        return folder + now.strftime("plot_%Y_%m_%d_%H_%M_%S.gif")

    @staticmethod
    def standard_interpolation(df, method):
        """
        Interpolate data for smooth curve if no datetime index has been detected.

        :param df:
        :param method:
        :return:
        """

        # Start, Stop of Index
        index_min = min(df.index)
        index_max = max(df.index)

        # Reindex (new data entries wil be NaN)
        reindex_index = np.linspace(index_min, index_max, 100)
        df_reindex = df.reindex(reindex_index)

        # Interpolate New Values
        df_interpolated = df_reindex.interpolate(method='cubic')

        return df_interpolated

    @staticmethod
    def datetime_interpolation(df, method):
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
    # new_plot.new()

    new_plot.main('new plot on christmas')
