
import numpy as np

class Node:
    
    def __init__(self, xy, value):
        self.xy = xy
        self.val = value
        self.owns = []
            
    def update(self, vector, alfa):
        self.val += alfa*(vector-self.val)
                
def indices(lvl):
  
  pi = np.pi
  r = 1
  n = 1
  
  for i in range(lvl):
    a = 0
    increment = (2*np.pi)/(4*n)
    for a in range(1,4*n-1):
      yield np.floor(r*np.cos(a)),np.floor(r*np.sin(a))
      a = a + increment
    r += 1
    n += 1

class SOM:
    "Grid structure, nodes in lattice, dims are for number of rows and number of columns"
    def __init__(self, dims=(10,10), ivar=4, alfa=1.0, dt=30, r=10):
        
        self.nodes = []
        self.setup(dims,nvar=ivar,mode="random")
        self.alfa = alfa
        self.r = r
        self.dt = dt
       
    def get_data(self, f, cols=(0,5)):
        
        txtfile = open(f)
        vectors = []
        while True:
            line = txtfile.readline()
            if line == "":
                break
            s = line.split()
            vectors.append(s[cols[0]:cols[1]])
        self.data = vectors
        txtfile.close()
              
    def train(self,last=4):
        
        i = 1
        for row in self.data:
            vec = np.array([float(xx) for xx in row[0:last]])
            self.winner(vec,indx=i)
            i += 1
            
    def setup(self, dims, nvar=4, scale=1, mode="random"):
        
        for row in range(0,dims[0]):
            self.nodes.append([])
            
        for i in range(0,dims[0]):
            for j in range(0,dims[1]):
                if mode == "random":
                    valv = np.random.rand(nvar)*scale
                    self.nodes[i].append(Node(xy=[i,j],value=valv))    
                elif mode=="slope":
                    valv = range(i+j,i+j+nvar)         
                    self.nodes[i].append(Node(xy=[i,j],value=valv))                
     
     
    def dgrid(self, node1, node2):
        "distance of two node-coordinates in the map"
        return map(lambda one,two: one-two,node1.xy,node2.xy) 
    
    def distance(self, v1, v2, dtype="euclid"):
        if dtype == "euclid":return(np.sqrt(sum((v1-v2)**2)))
        elif dtype == "manhattan":return(sum(abs(v1-v2)))
        else:return 0
        
    def winner(self, vector, first=0, last=4, indx=1):
        "chooses the closest map node to input vector and pulls its neighbours"
        mindist = self.distance(self.nodes[0][0].val, np.array(vector))
        imin = [0,0]
        
        for row in self.nodes:
            for node in row:
                d = self.distance(node.val, np.array(vector))
                if d < mindist:
                    mindist = d
                    imin = node.xy
                else:
                    pass
        
        self.nodes[imin[0]][imin[1]].owns.append(indx)
        #self.nodes[imin[0]][imin[1]].owns.append(vector)
        self.pull(vector,imin,indx)
                      
        #return winner,imin        
             
    def get_node(self,i,j):
        "returns a map node"
        if i<0 or j<0:
            return None
        try:
            r = self.nodes[i][j]
            return r
        except:
            return None
    
    def alfa_func(self,t,r):
        "pull function coefficient decreasing with time and radius"
        n = len(self.data)
        alfa = self.alfa
        return np.exp(-r/self.r)*np.exp(-t/n)*alfa
    
    def pull(self,vector,xy,indx):
        "pulls nearby nodes in in the map in the direction of a vector, time runs with input data index"
        t = len(self.data)-indx
        nlvl = abs(divmod(t,self.dt)[0]+1)
        
        x,y = xy[0],xy[1]
        alfa_val = self.alfa_func(t,1)
        self.nodes[x][y].update(vector,alfa_val)
              
        for lvl in range(0,nlvl):
            for ind in indices(lvl):
                i,j = x+ind[0],y+ind[1]
                r = np.sqrt(ind[0]**2+ind[1]**2)
                alfa_val = self.alfa_func(t,r)
                if i>0 and j>0:
                    try:
                        self.nodes[i][j].update(vector,alfa_val)
                    except:
                        pass
     
    def strmap(self,vecs=True):
        "list of node vectors or input indices belonging to node vectors"
        rstring = ""
        for row in self.nodes:
            scol = ""
            for node in row:
                rstring += ";"
                if vecs:
                    for dim in node.val:
                        rstring += " "+str(dim)+","
                else:
                    for i in node.owns:
                        rstring += " "+str(i)+","
            rstring += " "+str(scol)+"\n"
            rstring += "-- \n"
        return rstring     
