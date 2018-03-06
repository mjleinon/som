
import math
import random


class Node:
    
    def __init__(self, xy, value=None):
        self.xy = xy
        self.val = value
        self.owns = []
        
    def update(self, vector, alfa): 
        ii = 0
        for i in vector:
            self.val[ii] += alfa*(i - self.val[ii])
            ii += 1

def indices(lvl):
    #Manual adjacent indices in grid
    xlot = [(1,0,-1,0),
            (1,-1,-1,1),
            (0,1,2,2,2,1,0,-1,-2,-2,-2,-1),
            (3,3,2,1,0,-1,-2,-3,-3,-3,-2,-1,0,1,2,3),
            (4,4,3,3,2,1,0,-1,-2,-3,-3,-4,-4,-4,-3,-3,-2,-1,0,1,2,3,3,4),
            ]
    ylot = [(0,-1,0,1),
            (1,1,-1,-1),
            (2,2,1,0,-1,-2,-2,-2,-1,0,1),
            (0,-1,-2,-3,-3,-3,-2,-1,0,1,2,3,3,3,2,1,0),
            (0,-1,-2,-3,-3,-4,-4,-4,-3,-3,-2,-1,0,1,2,3,3,4,4,4,3,3,2,1),
            ]
    for i in zip(xlot[lvl],ylot[lvl]):
        yield i           
            
class SOM:
    #Grid structure, nodes in lattice, dims are for number of rows and number of columns
    def __init__(self, f, dim=[10,10], ivar=4, alfa=1.0,dt=30, r=10):
        
        self.nodes = []
        self.setup(dim,nvar=ivar,mode="random")
        self.data = self.file_vectors(f)
        self.alfa = alfa
        self.r = r
        self.dt = dt
       
    def file_vectors(self, f, first=0,last=5):
        
        txtfile = open(f)
        vectors = []
        while True:
            line = txtfile.readline()
            if line == "":
                break
            s = line.split()
            vectors.append(s[first:last])
        return vectors
              
    def train(self,last=4):
        
        i = 1
        for row in self.data:
            vec = [float(xx) for xx in row[0:last]]
            self.winner(vec,indx=i)
            i += 1
            
    def setup(self, dim, nvar=4, rr=[-0.5,0.5], mode="random"):
        
        for row in range(0,dim[0]):
            self.nodes.append([])
        
        if mode in ("pca","slope"):
            scale = 10.0
            
        for i in range(0,dim[0]):
            for j in range(0,dim[1]):
                if mode == "random":
                    valv = [random.uniform(rr[0],rr[1]) for x in range(0,nvar)]
                    valv = [round(xx,4) for xx in valv] 
                    self.nodes[i].append(Node(xy=[i,j],value=valv))    
                elif mode=="slope":
                    valv = [(i+scale*j)]*nvar         
                    self.nodes[i].append(Node(xy=[i,j],value=valv))                
     
     
    def dgrid(self, node1, node2):
        #distance of two node-coordinates in the map
        return map(lambda one,two: one-two,node1.xy,node2.xy) 
    
    def distance(self, v1, v2, dtype="euclid"):
        #distance of two vectors in input space
        summa = 0
        i = 0  
        while True:
            if i > len(v1)-1:
                break      
            if dtype == "euclid":
                summa += (v1[i]-v2[i])**2
            elif dtype == "manhattan":
                summa += abs(v1[i]-v2[i])
            i += 1
            
        if dtype == "euclid":
            return math.sqrt(summa)    
        else:
            return summa
    
    def winner(self, vector, first=0, last=4, indx=1):
        #chooses the closest map node to input vector and pulls its neighbours
        mindist = self.distance(self.nodes[0][0].val[first:last], vector)
        winner = self.nodes[0][0]
        imin = [0,0]
        
        for col in self.nodes:
            for node in col:
                d = self.distance(node.val[first:last+1], vector)
                if d < mindist:
                    mindist = d
                    winner = node
                    imin = node.xy
                else:
                    pass
        
        self.nodes[imin[0]][imin[1]].owns += [indx]
        #self.nodes[imin[0]][imin[1]].owns.append(vector)
        self.pull(vector,winner,indx)
                      
        #return winner,imin        
    
    def get_node(self,i,j):
        #returns a map node
        if i<0 or j<0:
            return None
        try:
            r = self.nodes[i][j]
            return r
        except:
            return None
    
    def alfa_func(self,t,r):
        
        n = len(self.data)
        alfa = self.alfa
        return math.exp(-r/self.r)*math.exp(-t/n)*alfa
    
    def pull(self,vector,node,indx):
        #pulls nearby nodes in in the map in the direction of a vector
        n = len(self.data)
        t = n-indx
        nlvl = abs(divmod(t,self.dt)[0]+1)
        
        x,y = node.xy[0],node.xy[1]
        alfa_val = self.alfa_func(t,0.01)
        self.nodes[x][y].update(vector,alfa_val)
        
        lvls = range(0,n)[0:nlvl]
        
        for lvl in lvls:
            for ind in indices(lvl):
                try:
                    i,j = x+ind[0],y+ind[1]
                    r = math.sqrt(ind[0]**2+ind[1]**2)
                    alfa_val = self.alfa_func(t,r)
                    self.nodes[i][j].update(vector,alfa_val)
                except:
                    pass
     
    def strmap(self,vecs=True):
        #list of node vectors 
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
