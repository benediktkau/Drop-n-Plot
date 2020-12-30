import logging
import matplotlib as plt
import matplotlib.pyplot
import pandas as pd
import helpers
import numpy as np
import random

plt.use('Agg')  # used in backend

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}
COLORS = (
    'tab:orange', 'tab:blue', 'tab:red', 'tab:green', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive',
    'tab:cyan')
MILLISECONDS_BETWEEN_FRAMES = 100
ANIMATION_DURATION = 10  # seconds
QUALITY_DPI = 200

LINEPLOT = True

logging.basicConfig(filename='dropnplot_log.log',
                    level=logging.INFO,
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


class Plot:
    def __init__(self, filepath):
        self.filepath = filepath
        if filepath == '':
            # Generate Random Dataframe
            self.df, self.datetime_index, self.df_type = self.create_random_df()

        else:
            # Load File
            try:
                self.df, self.datetime_index, self.df_type = self.read_dataframe(self.filepath)
            except FileNotFoundError as e:
                logging.critical('File not found' + str(e))

    def main(self, plot_title):
        """

        :param plot_title:
        :return:
        """
        # Get frame numbers required
        frame_num = helpers.get_frame_num(MILLISECONDS_BETWEEN_FRAMES, 10)
        logging.info('frame number:' + str(frame_num))

        # Smoothening
        interpolation_method = 'cubic'

        if self.datetime_index:  # interpolation for panda datetime index
            datetime_details_dict = self.get_datetime_index_details(self.df.index)

            datetime_xlim_date = min(self.df.index) + pd.Timedelta(weeks=int((datetime_details_dict['years'] * 52 +
                                                                         datetime_details_dict['months'] * 4.3 +
                                                                         datetime_details_dict['weeks']) * 0.1),
                                                              days=int(datetime_details_dict['days'] * 0.1),
                                                              hours=int(datetime_details_dict['hours'] * 0.1),
                                                              minutes=int(datetime_details_dict['minutes'] * 0.1),
                                                              seconds=int(datetime_details_dict['seconds'] * 0.1))

            try:
                self.df = self.datetime_interpolation(self.df, datetime_details_dict['datetime_freq'], frame_num,
                                                 interpolation_method)
            except Exception as e:
                logging.warning('Interpolation Failed: ' + str(e))
            else:
                logging.info('Interpolation Successful')

            frame_interval = helpers.get_frame_interval(ANIMATION_DURATION, len(self.df.index))

        else:  # standard interpolation
            try:
                self.df = self.standard_interpolation(self.df, frame_num, interpolation_method)
            except Exception as e:
                logging.warning('Interpolation Failed: ' + str(e))
            else:
                logging.info('Interpolation Successful')

            frame_interval = MILLISECONDS_BETWEEN_FRAMES
            self.df.reset_index(drop=True, inplace=True)

        logging.info('Length dataframe' + str(len(self.df.index)))

        """ ATTEMPT SCATTER """
        # plt.pyplot.savefig('attempt_scatter.png')

        # Get xlim, ylim
        if self.datetime_index:
            xlim_init = (min(self.df.index), max(self.df.truncate(after=datetime_xlim_date).index))

        else:
            xlim_init = (0.1 * min(self.df.index), 0.1 * max(self.df.index))

        ylim_init = (0, 0.3 * self.df.values.max())

        fig = plt.pyplot.figure()
        ax = plt.pyplot.axes(xlim=xlim_init, ylim=ylim_init)
        # plt.pyplot.ylabel('Degrees', fontdict=font, rotation='horizontal', loc='top')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        plt.pyplot.xticks(fontsize=8, color='grey')
        plt.pyplot.yticks(fontsize=8, color='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        if LINEPLOT:
            lines = []

            if self.df_type == "DataFrame":
                for index in range(len(self.df.columns)):
                    color = COLORS[index]
                    line_artist = ax.plot([], [], lw=2, color=color)[0]
                    lines.append(line_artist)
            else:
                color = COLORS[random.randint(0, len(COLORS) - 1)]
                lines.append(ax.plot([], [], lw=2, color=color)[0])

        else:
            scat = plt.pyplot.scatter([], [], cmap='gist_heat', alpha=0.5, marker='.')

        def init_line():
            """

            :return:
            """
            if LINEPLOT:
                for line in lines:
                    line.set_data([], [])
                return lines

            else:
                scat.set_offsets([])
                return scat,


        datetime_index = self.datetime_index
        df = self.df

        # Animation
        def animate_line(i):
            """
            Animation function for matplotlib FuncAnimation

            :param i: index to iterate over df
            :return: line element to be plotted
            """

            x = list(df.index[:i])

            if LINEPLOT:

                for column, line in enumerate(lines):
                    if self.df_type == "DataFrame":
                        y = df[df.columns[column]][:i]
                    else:
                        y = df.values[:i]
                    line.set_data(x, y)

            else:
                y = df.values[:i]
                scat.set_offsets([x[:i], y[:i]])

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
                    ax.set_ylim(df.values[:i].min() * 1.1, df.values[:i].max() * 1.1)

            # print progress bar
            helpers.progress_bar(i + 2, len(df.index))

            # Add Title
            if datetime_index:
                plt.pyplot.title(plot_title + '\n' + str(df.index[i].strftime('%Y')))
            else:
                plt.pyplot.title('\n'.join([plot_title, str(int(df.index[i]))]))

            if LINEPLOT:
                return lines
            else:
                return scat

        # Create Plot
        filename_plot = helpers.create_filename()

        # Call animate() function
        animator = plt.animation.FuncAnimation(fig,
                                               animate_line,
                                               interval=frame_interval,
                                               frames=len(self.df.index) - 1,
                                               init_func=init_line,
                                               blit=True,
                                               repeat_delay=300)

        # Save file as GIF
        animator.save(filename_plot, dpi=QUALITY_DPI)

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
                df = df.transpose()

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

        return datetime_details_dict


    @staticmethod
    def create_random_df():
        """

        :return:
        """

        df = pd.DataFrame()

        for column in range(10):
            values = np.random.randint(random.randint(-100, 0), random.randint(1, 100), 10)
            df[str(column)] = values

        return df, False, "DataFrame"


    @staticmethod
    def standard_interpolation(df, frame_num, method):
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
        reindex_index = np.linspace(index_min, index_max, frame_num)
        df_reindex = df.reindex(reindex_index)

        # Interpolate New Values
        df_interpolated = df_reindex.interpolate(method=method)

        return df_interpolated

    @staticmethod
    def datetime_interpolation(df, datetime_freq, frame_num, method):
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
    new_plot = Plot('temperature.csv')
    new_plot.main("Drop'n'Plot")
