# nlpstats-proto
Prototyping ideas for an NLP stats GUI

Todo:
* add `matplotlib.use('Agg')` under your import. The following got rid of the problem for me, but some other variation may work.
```
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
```
* Add a path prefix to the svg filenames, ideadlly as a function parameter for each function (`def plot_hist(score1, score2, output_dir:`).
* Low priority: consider using the svg text property in your charts, for more consistent export https://stackoverflow.com/questions/34387893/output-matplotlib-figure-to-svg-with-text-as-text-not-curves

Resources:
* https://bootsnipp.com/forms
* https://www.w3schools.com/howto/howto_js_tabs.asp
* https://stackoverflow.com/questions/34387893/output-matplotlib-figure-to-svg-with-text-as-text-not-curves
