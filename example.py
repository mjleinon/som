from som import *

k = SOMNetwork()
k.get_data("iris.txt")
k.train()
print(k.strmap())
