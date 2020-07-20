# nlpstats-proto
Prototyping ideas for an NLP stats GUI

## Haotian's Todo (Done @07.19.2020):
* add `matplotlib.use('Agg')` for .png or `matplotlib.use('Svg')` for .png under your import. The following got rid of the problem for me, but some other variation may work (https://matplotlib.org/3.2.0/tutorials/introductory/usage.html).
```
import matplotlib
matplotlib.use('Svg')
from matplotlib import pyplot as plt
```
* Add a path prefix to the svg filenames, ideadlly as a function parameter for each function (`def plot_hist(score1, score2, output_dir):`).
* Low priority: consider using the svg text property in your charts, for more consistent export https://stackoverflow.com/questions/34387893/output-matplotlib-figure-to-svg-with-text-as-text-not-curves

## Timeline

1. Finish plumbing DA tab and implement the todo list (before next meeting).
2. Connect effect size functions to UI (before 7/21 meeting)
