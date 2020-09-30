import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import scipy

# Read dataframe
df = pd.read_csv('covid.csv', delimiter=',', header='infer')
df_interest = df.loc[
    df['Country/Region'].isin(['United Kingdom', 'US', 'Italy', 'Germany'])
    & df['Province/State'].isna()]

print(df_interest)
df_interest.rename(
    index=lambda x: df_interest.at[x, 'Country/Region'], inplace=True)
    f1 = df_interest.transpose()
print(df_interest)
df1 = df1.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])

df1 = df1.loc[(df1 != 0).any(1)]
df1.index = pd.to_datetime(df1.index)

df1 = df1.rolling(2, win_type='gaussian').sum(std=3)


color = ['red', 'green', 'blue', 'orange']
fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('No of Deaths')
plt.xlabel('Dates')





color = ['red', 'green', 'blue', 'orange']
fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('No of Deaths')
plt.xlabel('Dates')

def buildmebarchart(i=int):
    plt.legend(df1.columns)
    p = plt.plot(df1[:i].index, df1[:i].values) #note it only returns the dataset, up to the point i
    for i in range(0,4):
        p[i].set_color(color[i]) #set the colour of each curve
import matplotlib.animation as ani
animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)
#animator.save('animation.gif', dpi=300)

# new attempt with temperature
df3 = pd.read_csv('temperature.csv', delimiter=',', header='infer')
df2 = df3.transpose()
print(df2)
ax = plt.gca()

df3.plot()
plt.show()

fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('No of Deaths')
plt.xlabel('Years')
plt.plot(df2.index,df2.values)
plt.show

"""
def buildmebarchart2(i=int):
    plt.legend(df2.columns)
    p = plt.plot(df2[:i].index, df2[:i].values) #note it only returns the dataset, up to the point i
import matplotlib.animation as ani
animator = ani.FuncAnimation(fig, buildmebarchart2, interval = 100)
animator.save('newanimation.gif', dpi=300) """

#plt.show()