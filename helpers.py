import datetime
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}


def deleteOldFiles():
    """
    Delete .gif plot files older than 30 minutes to save storage space

    :return:
    """

    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(currentDirectory + '/static'):

        if filename[0:4] == 'plot' and filename[-3:] == 'gif':
            stats = os.stat(currentDirectory + '/static/' + filename)
            lastEdited = datetime.datetime.fromtimestamp(stats.st_mtime)
            now = datetime.datetime.now()
            diff = (now - lastEdited).total_seconds() / 60  # get minutes since last modification
            if diff > 30:
                os.remove(currentDirectory + '/static/' + filename)


def detect_delimiter(filename):
    """

    :param filename:
    :return:
    """

    with open(filename) as csv_file:
        first_line = csv_file.readline()
        delimiters = [',', ';', ':', '|', '\t', ' ']
        delimiter_count = 0
        for delimiter in delimiters:
            if first_line.count(delimiter) > delimiter_count:
                delimiter_detected = delimiter

        csv_file.close()

    return delimiter_detected
