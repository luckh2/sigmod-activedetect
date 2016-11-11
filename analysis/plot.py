#!/usr/bin/env python
#
# pip install pygg wuutils
from pygg import *
from wuutils import *

legend_bottom = legend + theme(**{
  "legend.position":esc("bottom"),
  "legend.margin": "unit(0, 'cm')"
})



scale = 0.75

rows = [[0.24 , 0.39  , 0.34   , 0.84   , 0.93  ,  1],
[0.39  ,  0.36  ,  0.31  ,  0.61  ,  0.84 ,   1],
[0.91  ,  0.84  ,  0.76  ,  0.98  , 0.98 ,   1],
[0.01  ,  0.2 , 0.21  ,  0.61  ,  0.69  ,  1],
[0.07  ,  0.14  ,  0.1 , 0.71  ,  0.84  ,  1],
[0.44  ,  0.26  ,  0.56  ,  0.8 , 0.94  ,  1],
[0.01  ,  0.03   , 0.04   , 1  , 0.98   , 1],
[0.66  ,  0.61  ,  0.62  ,  0.82  ,  0.94 ,   1]]
datasets = ['Census', 'Housing', 'Sensor', 'NFL', 'Titanic', 'Retail' , 'Emergency', 'EEG']
approaches = ['MCD', 'ISO', 'BC-Q', 'BC-Q,MV', 'BC-Q,MV,NN', 'Custom Rules']

data = []
for dataset, row in zip(datasets, rows):
  d = dict(zip(approaches, row))
  d['dataset'] = dataset
  data.append(d)
data = fold(data, approaches)

legend_none += theme(**{
  "text": element_text(size=11),
  "axis.text": element_text(size=11),
  "strip.background": element_rect(fill=esc("#f2f2f2"), color=esc("#c0c0c0")),
  "strip.text": element_text(color=esc("#111111"))
})

p = ggplot(data, aes(x='key', y='val', color='key', shape='key'))
p += facet_wrap("~dataset", ncol=4)
p += coord_flip()
p += geom_point(size=1.8)
p += guides(shape="FALSE", size="FALSE")
p += axis_labels("", "F1 Score", "discrete", "continuous", 
    xkwargs=dict(lim=map(esc, list(reversed(approaches)))), 
    ykwargs=dict(lim=[0,1], breaks=[0, 0.25, .5, .75, 1], labels=map(esc, ["0", ".25", ".5", ".75", "1"])))
p += legend_none
ggsave("daccuracy.png", p, width=8, height=3.5, scale=scale)




rows = [[106.1 ,  3.2, 1.3 ,4.4, 5.7, 2.5],
  [16.1 ,   0.7 ,0.06   , 0.14 ,   0.56    ,0.09],
  [567, 62.9   , 7.3 ,9.6, 25.4 ,   10.1],
  [1078.4 , 183 ,64.1  ,  69.6   , 88.4   , 64.1],
  [59.4   , 14.5  ,  6.1, 6.4,8.5 ,6.6],
  [5672.6 , 234.7  , 88.7  ,  96.7 ,   183.4 ,  94.3],
  [877.2  , 145.1  , 36.1 ,   56.9  ,  148.5,   50.5],
  [1453.1 , 556.4  , 49.3  ,  82.1  ,  169.4 ,  48.1]]

data = []
for dataset, row in zip(datasets, rows):
  d = dict(zip(approaches, row))
  d['dataset'] = dataset
  data.append(d)
data = fold(data, approaches)

p = ggplot(data, aes(x='key', y='val', color='key', shape='key'))
p += facet_wrap("~dataset", ncol=4)
p += coord_flip()
p += geom_point(size=1.8)
p += legend_none
p += guides(shape="FALSE", size="FALSE")
p += axis_labels("", "Time (s, log)", "discrete", "log10", 
    xkwargs=dict(lim=map(esc, list(reversed(approaches)))),
    ykwargs=dict(breaks=[1, 60, 60*60], labels=map(esc, ["1s", "1m", "1hr"])))
ggsave("druntime.png", p, width=8, height=3.5, scale=scale)










scale = 0.6

rows = [ ["Naive", 2754, 5691, 8672, 11016, 14002],
["Materialization", 2943, 3116, 3154, 3201, 3241],
["Indexing", 2043, 2058, 2061, 2074, 2099]]
labels = ["Optimization", 1, 2, 3, 4, 5]
data = []

for row in rows:
  d = dict(zip(labels, row))
  data.append(d)
data = fold(data, labels[1:])
for d in data:
  d['key'] = int(d['key'])



p = ggplot(data, aes(x='key', y='val', color='Optimization', group="Optimization", shape="Optimization"))
p += geom_line()
p += geom_point(size=2)
p += legend_bottom
p += guides(size="FALSE")
p += axis_labels("Boost-and-Clean Iteration", "Time (s)", "continuous", "continuous",
    ykwargs=dict(lim=[0, 4.5*60*60], breaks=[0, 30*60, 60*60, 2*60*60, 3*60*60, 4*60*60], labels=map(esc, ["0", "30m", "1hr", "2hr", "3hr", "4hr"])))
p += ggtitle(esc("BoostClean Runtime (no parallelism)"))
ggsave("opt1.png", p, width=8, height=3.5, scale=scale)




rows = [["Random Forest", 0.71, 0.74, 0.77, 0.76, 0.75],
["SVM", 0.69, 0.70, 0.71, 0.73, 0.71],
["Logistic Regression", 0.68, 0.72, 0.73, 0.72, 0.70]]
labels = ["Opt", 1, 2, 3, 4, 5]

data = []
for row in rows:
  d = dict(zip(labels, row))
  data.append(d)
data = fold(data, labels[1:])
for d in data:
  d['key'] = int(d['key'])


p = ggplot(data, aes(x='key', y='val', color='Opt', group="Opt", shape="Opt"))
p += geom_line()
p += geom_point(size=2)
p += legend_bottom
p += guides(size="FALSE")
p += axis_labels("Boost-and-Clean Iteration", "Classifier Accuracy", "continuous", "continuous",
  ykwargs=dict(lim=[.5, .8], breaks=[0.5, .6, 0.7, 0.8 ]))
p += ggtitle(esc("BoostClean Accuracy for Different Models"))
ggsave("learn.png", p, width=8, height=3.5, scale=scale)









#
#
# Runtime Plots
#
#


rows = [('Repair Selection', 2072, 1346, 682, 375, 234),
('Error Detect', 306, 312, 319, 293, 366),
('Load Data', 44, 44, 44, 44, 44)]
labels = ('approach', '1 Core', '2 Core', '4 Core', '8 Core', '16 Core')

data = []
for row in rows:
  d = dict(zip(labels, row))
  data.append(d)
data = fold(data, labels[1:])


p = ggplot(data, aes(x='key', y='val', fill='approach', group="key"))
p += geom_bar(position=esc("stack"), stat=esc("identity"), width=0.5)
p += legend_bottom
p += guides(shape="FALSE", size="FALSE")
p += axis_labels("", "Time", "discrete", "continuous", 
    xkwargs=dict(lim=map(esc, labels[1:])),
    ykwargs=dict(breaks=[10*60, 20*60, 30*60], labels=map(esc, ["10m", "20min", "30min"])))
p += ggtitle(esc("Training Runtime on FEC"))
ggsave("runtime.png", p, width=8, height=3.5, scale=scale)


data = []
labels = ['Training', 'Prediction', 'Prediction No NN']
for x,v in zip(labels, [9316,19746, 23746]):
  data.append(dict(key=x, val=v/1000.))
print data

p = ggplot(data, aes(x='key', y='val', fill='key'))
p += geom_bar(stat=esc("identity"), width=0.5)
p += legend_none
p += axis_labels("", "Thousand Records/sec", "discrete", "continuous",
    xkwargs=dict(lim=map(esc, labels)))
    #ykwargs=dict(breaks=[10*60, 20*60, 30*60], labels=map(esc, ["10m", "20min", "30min"])))
p += ggtitle(esc("Throughput on FEC"))
ggsave("runtime2.png", p, width=8, height=3.5, scale=scale)








