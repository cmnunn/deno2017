import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot
import matplotlib.pyplot as plt

RUN_TYPES = ['test_2to1_asym','test_2to1_sym','test_3to1_asym',
             'test_4to3_sym','test_5to2_alt','test_5to2_asym',
             'test_6to3_sym', 'test_2to1_asym_nogov','test_2to1_sym_nogov',
             'test_3to1_asym_nogov','test_4to3_sym_nogov','test_5to2_alt_nogov',
             'test_5to2_asym_nogov','test_6to3_sym_nogov']

for RUN_TYPE in RUN_TYPES:
    
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
    
        step_values = []

        for file_num in range(1,11):
            step_values.append(float(plot_values[file_num][i]))

        median_values.append(np.median(step_values))
        std_dev_values.append(np.std(step_values))

    stat_plot.append(x_values)
    stat_plot.append(median_values)
    stat_plot.append(std_dev_values)

    # Plot
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

        titlefont = dict(size=24),

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
