
import numpy as np

class Node:
    
    def __init__(self, xy, value):
        self.xy = xy
        self.val = value
        self.owns = []
            
    def update(self, vector, alfa):
        self.val += alfa*(vector-self.val)
        
    
def indices_circle(r):
    r = max(r,2)
    quart = [(0,1),(1,0),(0,1),(1,0)]
    i = 0
    for xsign,ysign in zip((1,-1,-1,1),(1,1,-1,-1)):     
        for x in range(quart[i][0],r):
            y = np.round(np.sqrt(r**2-x**2))
            for yi in range(quart[i][1],int(y)):
                yield (x*xsign,yi*ysign)
        i += 1

def indices_square(r):
    r = max(r,2)
    quart = [(0,1),(1,0),(0,1),(1,0)]
    i = 0
    for xsign,ysign in zip((1,-1,-1,1),(1,1,-1,-1)):     
        for x in range(quart[i][0],r):
            for y in range(quart[i][1],r):
                yield (x*xsign,y*ysign)
        i += 1

class SOMNetwork:
    """
    SELF-ORGINIZING MAP - AKA KOHONEN NETWORK
    """
    "Grid structure, nodes in lattice, dims are for number of rows and number of columns"
    def __init__(self, dims=(10,10), nvar=4, alfa=1.0, r=2.0, setup_mode="slope", indices="circle"):
        
        self.nodes = []
        self.alfa = alfa
        self.r = np.sqrt(dims[0]**2+dims[1]**2)*r
        self.setup_mode=setup_mode
        self.nvar = nvar
        self.dims = dims
        self.r_max = np.sqrt(dims[0]**2+dims[1]**2)
        
        if indices=="circle":
            self.neighbours = indices_circle
        elif indices=="square":
            self.neighbours = indices_square
            
    def data_set_metrics(self):
        self.maxes = np.amax(self.data_array,axis=0)
        self.means = np.mean(self.data_array,axis=0)
        
    def clear_assignments(self):
        "empties datapoints from nodes"
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                self.nodes[i][j].owns = []
        
    def get_data(self, f, cols=(0,4), sepr=" "):
        "gets data from file and sets up nodes into their initial position"
        vectors = []
        with open(f) as txtfile:
            for line in txtfile: 
                s = line.split(sepr)
                row = s[cols[0]:cols[1]]
                vectors.append([float(x) for x in row])
        txtfile.close()
           
        self.data = vectors
        self.data_array = np.array(self.data)
        self.data_set_metrics()
        self.setup(self.dims,self.nvar,mode=self.setup_mode)
        
        self.n = len(self.data)
        
    def set_data(self, dataset):
        self.data = list(dataset)
        self.data_array = np.array(self.data)
        self.data_set_metrics()
        self.setup(self.dims,self.nvar,mode=self.setup_mode)
        
        self.n = len(self.data)
              
              
    def train(self,last=4,n_epochs=25,save_history=False):
        "trains the SOM - sets up node weights going trough data over epochs"
        
        self.history = []
        
        last = min(last,len(self.data[0]))
        
        for epoch in range(n_epochs):
            i = 1
            self.clear_assignments()
            for n in np.random.permutation(len(self.data)): 
                row = self.data[n]
                self.winner(row[0:last],indx=i)
                i += 1
                
                if save_history:
                    self.history.append(self.get_state())
            
    def setup(self, dims, nvar=4, scale=1, mode="random"):
        
        for row in range(dims[0]):
            self.nodes.append([])
            
        nvar = min(nvar,len(self.data[0]))
            
        for i in range(0,dims[0]):
            for j in range(0,dims[1]):
                if mode == "random":
                    valv = (np.random.rand(nvar)-0.5)*scale*2+self.means
                    self.nodes[i].append(Node(xy=[i,j],value=valv))    
                elif mode=="slope":
                    valv = np.array([float(i+j*n)/self.maxes[n] for n in range(nvar)])       
                    self.nodes[i].append(Node(xy=[i,j],value=valv))  
                elif mode=="pca":
                    pass
                
    def get_state(self):
        for i in self.iterate_nodes():
            pass
     
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
        
        for node in self.iterate_nodes():
            d = self.distance(node.val, np.array(vector))
            if d < mindist:
                mindist = d
                imin = node.xy
            else:
                pass
        
        self.nodes[imin[0]][imin[1]].owns.append(indx)
        self.pull(vector,imin,indx)  
    
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
        return np.exp(-t/(self.n*self.alfa))*np.exp(-r/self.r)
        
    def pull_alt(self,vector,xy,indx):
        "pulls nearby nodes in in the map in the direction of a vector, time runs with input data index"
        
        nlvl = int((self.r_max+1)*(self.n-indx)/(self.n))
        nlvl = max(nlvl,1)
        x,y = xy[0],xy[1]
        
        alfa_val = self.alfa_func(indx,0)
        self.nodes[x][y].update(vector,alfa_val)
        
        pull_vector = self.nodes[x][y].val
        
        for di,dj in self.neighbours(nlvl):
            i,j = x+di,y+dj
            if i>=0 and j>=0: 
                r = np.sqrt(di**2+dj**2)
                alfa_val = self.alfa_func(indx,r)
                try:
                    self.nodes[i][j].update(pull_vector,alfa_val)
                except:
                    pass
                
    def pull(self,vector,xy,indx):
        "pulls nearby nodes in in the map in the direction of a vector, time runs with input data index"
        
        nlvl = int((self.r_max+1)*(self.n-indx)/(self.n))
        nlvl = max(nlvl,1)
        x,y = xy
        
        alfa_val = self.alfa_func(indx,0)
        self.nodes[x][y].update(vector,alfa_val)
        
        for di,dj in self.neighbours(nlvl):
            i,j = x+di,y+dj
            if i>=0 and j>=0: 
                r = np.sqrt(di**2+dj**2)
                alfa_val = self.alfa_func(indx,r)
                try:
                    self.nodes[i][j].update(vector,alfa_val)
                except:
                    pass
        
    def iterate_nodes(self):
        for row in self.nodes:
            for node in row:
                yield(node)
                
    def enumerate_nodes(self):
        for node in enumerate(self.nodes):
            yield(node)
                
    def create_u_matrix(self):
        "u-matriisi on solu solulta distanssien summat naapureihin, right?"
        self.u_matrix = np.zeros(self.dims)
        for node in self.iterate_nodes():
            dsum = 0
            x,y = node.xy
            for di,dj in [(1,0),(0,1),(-1,0),(0,-1)]:
                try:
                    dsum += np.sqrt(np.sum((self.nodes[x+di][y+dj].val-node.val)**2))
                except:
                    continue
            self.u_matrix[x][y] = dsum
            
    def create_owner_matrix(self):
        self.owner_matrix = np.zeros(self.dims)
        for node in self.iterate_nodes():
            x,y = node.xy
            try:
                self.owner_matrix[x][y] = len(self.nodes[x][y].owns)
            except:
                continue
