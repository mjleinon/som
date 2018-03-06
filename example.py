import som.py

kohonen = SOM("iris.txt",dim=[5,5]) 
kohonen.train() 
print(kohonen.strmap(False))
