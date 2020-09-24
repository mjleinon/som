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

"u-matrix and ownermatrix of trained network:"
k.create_u_matrix()
arrayshow_flipped(k.u_matrix, label="U-matrix 10x10 SOM")

k.create_owner_matrix()
arrayshow_flipped(k.owner_matrix, label="OWN-matrix 10x10 SOM")
