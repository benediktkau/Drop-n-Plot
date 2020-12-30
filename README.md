# Drop'n'Plot
____

### Create animated plots from .csv files
- implemented in Python
- graphical user interface in Flask
- interpolation ensures smooth animations even for small datasets
- returns **.gif animation** (ca. 10-15 seconds in duration)

![FLASK GUI](https://github.com/benediktkau/Drop-n-Plot/blob/main/github_readme_res/example3.png)

### Without GUI 
_(Python, matplotlib FuncAnimation)_
- run **plot_class.py**
- required argument: filepath to .csv file
- progress bar in command prompt

### With GUI (Flask)
_(Flask)_
- run Flask; application is in **app.py**
- progress bar in command prompt
- TODO: progress bar in GUI web interface

![Example Plot 1](https://github.com/benediktkau/Drop-n-Plot/blob/main/github_readme_res/example2.gif)


#### Format of .csv file
- all standard delimiters are supported (, ; : | tab space)
- if possible, column 0 should be an index
- if the index is in datetime format, it should be in the Python datetime.datetime package format

![Example Plot 2](https://github.com/benediktkau/Drop-n-Plot/blob/main/github_readme_res/example3.png)
