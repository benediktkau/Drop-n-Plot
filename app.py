import logging
import os
import sys

from flask import Flask, render_template, request

import helpers
import plot_class

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = helpers.UPLOAD_FOLDER
app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", plotFilename='../static/temperature.gif')


@app.route("/plot", methods=["GET", "POST"])
def plot():
    if request.method == "POST":
        """ Deleting old files """
        helpers.deleteOldFiles()
        logging.debug('Old File Deleted')

        """ Handling file upload """
        if request.files['file'] == '':
            pass

        try:
            uploadedFile = request.files['file']
            if uploadedFile.filename != '':
                uploadedFile.save(uploadedFile.filename)
        except Exception:
            return render_template('templates/sorry.html', text="Sorry, there was a problem with your file upload")

        plotTitle = request.form.get('plotname')
        if plotTitle == '':
            plotTitle = 'Untitled'

        """ Handling Plotting """

        plotObject = plot_class.Plot(uploadedFile.filename)
        plotFilename = plotObject.main(plotTitle)  # concatenate filename of plot result
        try:
            os.remove(uploadedFile.filename)
        except FileNotFoundError:
            logging.warning('No file could be removed.')

        return render_template('plot.html', plotFilename=plotFilename,
                               defaults={'plotFilename': '../static/temperature.gif'})


    else:
        return render_template("plot.html", plotFilename='../static/temperature.gif')


if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(debug=True)
