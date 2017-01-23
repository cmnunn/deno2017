import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot
import matplotlib.pyplot as plt

RUN_TYPE = 'test_2to1_asym'

x_vals = []

for i in range(5000):
    x_vals.append(i) 

plot_values = []
plot_values.append(x_vals)


# Read Values
for run_count in range(10):
    input_file = RUN_TYPE + '/' + RUN_TYPE + '_run' + str(run_count)  + '.txt'
  
    y_values = []

    with open(input_file, 'r') as data_file:
        for line in data_file:        
            y_values.append(line.strip())

    plot_values.append(y_values)


# Stat Stuff
stat_plot = []
x_values = []
median_values = []
std_dev_values = []

for step in range(50):
    i = step * 100
    
    x_values.append(plot_values[0][i])
    
    step_values = [float(plot_values[1][i]), float(plot_values[2][i]), float(plot_values[3][i]),
                   float(plot_values[4][i]), float(plot_values[5][i]), float(plot_values[6][i]),
                   float(plot_values[7][i]), float(plot_values[8][i]), float(plot_values[9][i]),
                   float(plot_values[10][i])]

    median_values.append(np.median(step_values))
    std_dev_values.append(np.std(step_values))

stat_plot.append(x_values)
stat_plot.append(median_values)
stat_plot.append(std_dev_values)

'''
# Raw Data Plot
plt.figure()

plot_title = 'Raw Data: ' + RUN_TYPE 
plt.title(plot_title, fontsize=46)

for plot_count in range(1,11):
    plot_label = 'run ' + str(plot_count)
    plt.plot(plot_values[0], plot_values[plot_count], label=plot_label, linewidth=4.0)

plt.xlabel("time ( seconds )", fontsize=42)
plt.ylabel("vehicle count", fontsize=42)

plt.tick_params(axis='both', which='major', labelsize=36)
plt.legend(loc=4, fontsize=36)
plt.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.07)
'''

data = [
    go.Scatter(
        x = stat_plot[0],
        y = stat_plot[1],

        error_y = dict(
            type = 'data',
            array = stat_plot[2],
            visible = True,
            color = '#85144B',
            opacity = 0.7
        ),

        line = dict(width=5)
    )
]


layout = go.Layout(
    title = 'Run Type: ' + RUN_TYPE + '</br>10 Run Trial with Std. Dev.',
    autosize = True,

    xaxis = dict(
        autorange =  True,
        showgrid=True,
        title = 'step count'
    ),
    yaxis = dict(
        autorange = True,
        showgrid=True,
        title = 'vehicle count'
        ),
)

fig = go.Figure(data=data, layout=layout)

plot(fig, filename=RUN_TYPE)
