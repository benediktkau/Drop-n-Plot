import logging
import matplotlib as plt  # pyplot
import matplotlib.pyplot

plt.use('Agg')
import pandas as pd
import datetime
import helpers
import numpy as np
import random

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}
COLORS = (
'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive',
'tab:cyan')

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
            df, datetime_index, df_type = self.read_dataframe(self.filepath)
        except FileNotFoundError as e:
            logging.critical('File not found', e)

        df, datetime_index, df_type = self.create_random_df()

        # Smoothening
        interpolation_method = 'cubic'


        if datetime_index:  # interpolation for panda datetime index
            datetime_details_dict = self.get_datetime_index_details(df.index)

            datetime_xlim_date = min(df.index) + pd.Timedelta(weeks=int((datetime_details_dict['years'] * 52 +
                                                                         datetime_details_dict['months'] * 4.3 +
                                                                         datetime_details_dict['weeks']) * 0.1),
                                                              days=int(datetime_details_dict['days'] * 0.1),
                                                              hours=int(datetime_details_dict['hours'] * 0.1),
                                                              minutes=int(datetime_details_dict['minutes'] * 0.1),
                                                              seconds=int(datetime_details_dict['seconds'] * 0.1))

            df = self.datetime_interpolation(df, datetime_details_dict['datetime_freq'], interpolation_method)

        else:  # standard interpolation
            df = self.standard_interpolation(df, interpolation_method)
            df.reset_index(drop=True, inplace=True)

        logging.info('Length dataframe' + str(len(df.index)))

        # Get xlim, ylim
        if datetime_index:
            xlim_init = (min(df.index), max(df.truncate(after=datetime_xlim_date).index))

        else:
            xlim_init = (0.1 * min(df.index), 0.1 * max(df.index))

        ylim_init = (0, 0.3 * df.values.max())

        fig = plt.pyplot.figure()
        ax = plt.pyplot.axes(xlim=xlim_init, ylim=ylim_init)
        lines = []

        if df_type == "DataFrame":
            for line in lines:
                color = COLORS[random.randint(0, len(COLORS) - 1)]
                line_artist = ax.plot([], [], lw=2, color=color)[0]
                lines.append(line_artist)
        else:
            color = COLORS[random.randint(0, len(COLORS) - 1)]
            lines = [ax.plot([], [], lw=2, color=color)[0]]


        def init():
            """

            :return:
            """

            for line in lines:
                line.set_data([], [])
            return lines

        # plt.pyplot.ylabel('Degrees', fontdict=font, rotation='horizontal', loc='top')
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
            Animation function for matplotlib FuncAnimation

            :param i: index to iterate over df
            :return: line element to be plotted
            """

            x = list(df.index[:i])

            for column, line in enumerate(lines):
                if df_type == "DataFrame":
                    y = df[df.columns[column]][:i]
                else:
                    y = df.values[:i]
                line.set_data(x, y)

            # Adapt ylim, xlim
            if not len(x) == 0 or not len(y) == 0:  # do not adapt if line is still empty

                # If plotting progressed beyond initial xlim, extent axis by new maximum
                if df.index[i] < xlim_init[0] or df.index[i] > xlim_init[1]:
                    if datetime_index:
                        ax.set_xlim(min(df.index), max(df[:i].index))
                    else:
                        ax.set_xlim(0, max(x) * 1.01)

                # If plotting progressed beyond initial ylim, extent axis by new maximum
                if df.values[i].min() < ylim_init[0] or df.values[i].max() > ylim_init[1]:
                    ax.set_ylim(df.values[:i].min(), df.values[:i].max() * 1.1)

            # print progress bar
            helpers.progress_bar(i + 2, len(df.index))

            # Add Title
            if datetime_index:
                plt.pyplot.title(plotTitle + '\n' + str(df.index[i].strftime('%Y')))
            else:
                plt.pyplot.title('\n'.join([plotTitle, str(int(df.index[i]))]))

            return lines

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
                         index_col=0, parse_dates=True)

        # Check whether index is pd.datetime format
        if isinstance(df.index, pd.DatetimeIndex):
            datetime_index = True
            df.index = pd.to_datetime(df.index, format='%Y')
        else:
            datetime_index = False

        if isinstance(df, pd.Series):
            # df.index = pd.to_datetime(df.index, format='%Y')
            df_type = 'Series'
        else:
            # df.index = pd.to_datetime(df.index)
            df_type = 'DataFrame'
            if len(df.index) < len(df.columns):
                df.transpose()

        return df, datetime_index, df_type

    @staticmethod
    def get_datetime_index_details(index) -> dict:

        datetime_details_dict = {'years': max(index).year - min(index).year,
                                 'months': max(index).month - min(index).month,
                                 'weeks': max(index).week - min(index).week,
                                 'days': max(index).day - min(index).day,
                                 'hours': max(index).hour - min(index).hour,
                                 'minutes': max(index).minute - min(index).minute,
                                 'seconds': max(index).second - min(index).second}

        # Determine the largest unit >0 to be used in the interpolation method
        for key in datetime_details_dict:
            if datetime_details_dict[key] > 0:
                datetime_details_dict['datetime_freq'] = key
                break

        print(datetime_details_dict)

        return datetime_details_dict

    @staticmethod
    def create_filename():
        """

        :return:
        """

        now = datetime.datetime.now()
        folder = 'static/'
        return folder + now.strftime("plot_%Y_%m_%d_%H_%M_%S.gif")

    @staticmethod
    def create_random_df():
        """

        :return:
        """

        df = pd.DataFrame()

        for column in range(10):
            values = np.random.randint(random.randint(-100, 0), random.randint(1,100), 10)
            df[str(column)] = values

        return df, False, "DataFrame"

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
    def datetime_interpolation(df, datetime_freq, method):
        """

        :param datetime_freq:
        :param df:
        :param method:
        :return:
        """

        # Dictionary to determine interpolation frequency
        datetime_interpolation_dict = {
            'years': 'Q',
            'quarters': 'M',
            'months': 'W',
            'weeks': 'D',
            'days': 'H',
            'hours': 'T',
            'minutes': 'S',
            'seconds': 'L',
        }

        interpolation_freq = datetime_interpolation_dict[datetime_freq]
        logging.debug('Interpolation Frequency:' + interpolation_freq)

        # https://machinelearningmastery.com/resample-interpolate-time-series-data-python/
        df_resampled = df.resample(interpolation_freq).mean()  # add quarters to data
        df_interpolated = df_resampled.interpolate(method=method)
        return df_interpolated


if __name__ == '__main__':
    new_plot = Plot('src/temperature.csv')
    new_plot.main('new plot on christmas')
