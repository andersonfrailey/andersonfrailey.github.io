---
layout: post
title: Visualizing the TCJA with Bokeh
---

Throughout tax reform season a seemingly endless stream of tables, plots, and charts filled Twitter to show the distributional effects of the Tax Cuts and Jobs Act. I particularly liked [Jonathan Schwabish’s piece](https://www.urban.org/urban-wire/how-we-can-better-visualize-analysis-tax-reform-legislation) on how he created a graph to make a report by the Joint Committee on Taxation (JCT) more engaging. I decided to recreate his work using [Bokeh](https://bokeh.pydata.org/en/latest/) and the open-source [Tax-Calculator](https://github.com/open-source-economics/Tax-Calculator/).

The following work was conducted using Tax-Calculator version 0.14.3 and Bokeh version 0.12.13.

<script src="https://gist.github.com/andersonfrailey/5420577a1432c8f747c28eebce21f98d.js"></script>

The first step is to create two calculator objects - one for the baseline (current law), and one for the reform. If you’re working directly with the source code, there is a folder in the Tax-Calculator that contains JSON files representing a number of reform provisions including the TCJA. If you’ve downloaded the [taxcalc](https://anaconda.org/ospc/taxcalc) package via [Conda](https://conda.io/docs/), you can download these files on [GitHub](https://github.com/open-source-economics/Tax-Calculator/tree/master/taxcalc/reforms).

Tax-Calculator requires a representative dataset of tax-units. As a core maintainer of Tax-Calculator and the supporting [TaxData](https://github.com/open-source-economics/taxdata) repository, I have access to the IRS Public Use File (PUF), which is what I used here. If you do not have access to the PUF, Tax-Calculator comes with a similar file derived from the Current Population Survey. To use this file, replace `rec = tc.Records(data='../Tax-Calculator/puf.csv')` with `rec = tc.Records.cps_constructor()`.

<script src="https://gist.github.com/andersonfrailey/8dd09e22142af5e714d200dd4fc1aac5.js"></script>

Two functions will be used to create the plots. The first, `find_perc`, is used to find what percent of tax filers face each change in tax liability and then the left and right edges for each section within the bars.

The second, `plot`, contains all of the logic needed to create a plot for each year.

<script src="https://gist.github.com/andersonfrailey/7ccac5057b413cb44a8d3e80d4eb0e44.js"></script>

Creating the plots was simple enough. First a [Bokeh figure](https://bokeh.pydata.org/en/latest/docs/reference/plotting.html#bokeh-plotting) is created, then it is populated with stacked bars for each income group. Each of the bars is made up of five [hbar glyphs](https://bokeh.pydata.org/en/latest/docs/reference/plotting.html#bokeh.plotting.figure.Figure.hbar) stacked together.

When working with hbar glyphs, you need to specify the y location; height (thickness); and left and right edges of each bar. My y-axis placement decisions were arbitrary. As in Schwabish's piece, I wanted the bar for all tax filers to be placed slightly higher than the others, but that's all I took into consideration. You could change the location and spacing to be whatever tickles your fancy.

For formatting, I used the Bokeh's visual styling capabilities. The `FuncTickFormatter` allows you to use Javascript or a Python function to format the y-axis labels. I'm not comfortable working with Javascript right now so I defined a Python function - `ticker` - that returned the label I wanted based on the y value of each bar. There may be a more elegant way to achieve the same results, but this was a quick and easy solution. It should be noted that if you want to format the axes with a Python function, you will also need to install `Flexx` (`conda install -c bokeh flexx`).

<script src="https://gist.github.com/andersonfrailey/617b82053d36952072dc643ab1c61c1b.js"></script>

Once the functions have been defined, all that is left to do is loop through each of the years, advancing both calculators a year at a time, and pass the data needed into the plotting functions.

<script src="https://gist.github.com/andersonfrailey/285ca68b7e7f54dcc4f4c15c22fc777f.js"></script>

![_config.yml]({{ site.baseurl }}/images/tcja2018.png)
![_config.yml]({{ site.baseurl }}/images/tcja2019.png)
![_config.yml]({{ site.baseurl }}/images/tcja2020.png)
![_config.yml]({{ site.baseurl }}/images/tcja2021.png)
![_config.yml]({{ site.baseurl }}/images/tcja2022.png)
![_config.yml]({{ site.baseurl }}/images/tcja2023.png)
![_config.yml]({{ site.baseurl }}/images/tcja2024.png)
![_config.yml]({{ site.baseurl }}/images/tcja2025.png)
![_config.yml]({{ site.baseurl }}/images/tcja2026.png)
![_config.yml]({{ site.baseurl }}/images/tcja2027.png)

### Resources:
[Bokeh](https://bokeh.pydata.org/en/latest/index.html)  
[Tax-Calculator](https://github.com/open-source-economics/Tax-Calculator/)
