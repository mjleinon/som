from som import *
from plotsom import *

k = SOMNetwork()
k.get_data("iris.txt")
k.train()

"plot examples over dimension pairs:"
p = plotsom.PlotSOM(k)
p.plot_nodes()
p.plot_nodes((1,2))
p.plot_nodes((0,2))
p.plot_nodes((0,3))
