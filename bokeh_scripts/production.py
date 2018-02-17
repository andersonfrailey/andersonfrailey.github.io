from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models.widgets import Slider, TextInput
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, HoverTool, CustomJS
from bokeh.embed import file_html
from bokeh.resources import CDN


# create a figure
# y = AK^aL^1-a
def output(l):
    a = 1
    alpha = .25
    beta = 1. - alpha
    k = 10
    y = a * (k ** alpha) * (l ** beta)
    return y


def update(attrname, old, new):
    cds.data['y'] = [output(x) for x in cds.data['labor']]


labor = [i for i in range(101)]
y = [output(x) for x in labor]
cds = ColumnDataSource(data={'labor': labor, 'y': y})

callback = CustomJS(args=dict(source=cds), code="""
    var data = source.data;
    var A = productivity.value;
    var alpha = alpha.value;
    var beta = 1 - alpha;
    var k = capital.value;

    l = data['labor']
    y = data['y']
    for (i = 0; i < y.length; i++){
        y[i] = A * Math.pow(k, alpha) * Math.pow(l[i], beta);
    }
    source.change.emit();
""")

alpha_input = Slider(start=0, end=1, step=0.01, value=.25, title='Alpha',
                     callback=callback)
capital_input = TextInput(title='Capital', value='10', callback=callback)
productivity_input = TextInput(title='Productivity', value='1',
                               callback=callback)
# assign call back arguments
callback.args['productivity'] = productivity_input
callback.args['alpha'] = alpha_input
callback.args['capital'] = capital_input

# create figure with labor on the x-axis
f = figure(title='Cobb-Douglas', width=550, height=500)
f.line(x='labor', y='y', line_width=2, source=cds)
hover = HoverTool(tooltips=[('Output', '@y'), ('Labor', '@labor')])
f.add_tools(hover)
f.legend.location = 'bottom_right'
f.xaxis.axis_label = 'Labor'
f.yaxis.axis_label = 'Production'


input_column = column(productivity_input, capital_input, alpha_input)
layout = row(f, input_column)

# used for development purposes
curdoc().add_root(layout)

# export HTML file to embed
html = file_html(layout, CDN, 'production')
html_file = open('../_includes/production.html', 'w')
html_file.writelines(html)
html_file.close()
