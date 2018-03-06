import som.py

k = SOM()
k.get_data("iris.txt")
k.train()
print(k.strmap())
