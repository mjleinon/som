# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:49:27 2020

@author: Mikko
"""

import matplotlib.pyplot as plt
import numpy as np

class PlotSOM:
    
    def __init__(self, som):
        self.som = som

    def plot_nodes(self, variables=(0,1), plotlines=True):
        fig = plt.figure()
        ix,iy = variables[0],variables[1]
        plt.scatter([i[ix] for i in self.som.data],[i[iy] for i in self.som.data],c="b",figure=fig)

        if plotlines:
            for i in range(len(self.som.nodes)):
                for j in range(len(self.som.nodes[i])):
                    node = self.som.nodes[i][j]
                    if j!=0:
                        nodeprev = self.som.nodes[i][j-1]
                        plt.plot([node.val[ix],nodeprev.val[ix]],[node.val[iy],nodeprev.val[iy]],figure=fig,c="#6c3376")
                    if i!=0:
                        nodeprev = self.som.nodes[i-1][j]
                        plt.plot([node.val[ix],nodeprev.val[ix]],[node.val[iy],nodeprev.val[iy]],figure=fig,c="#6c3376")
                            
        plt.scatter([n.val[ix] for n in self.som.iterate_nodes()],[n.val[iy] for n in self.som.iterate_nodes()],c="r",figure=fig)
                    
                
    def strmap(self,values=True):
        "list of node vectors or input indices belonging to node vectors"
        rstring = ""
        for row in self.som.nodes:
            srow = ""
            for node in row:
                if values:
                    for dim in node.val:
                        srow += " "+str(dim)+","
                    srow += "; \n"    
                else:
                    for i in node.owns:
                        srow += " "+str(i)+","
                    srow += "; \n"    
            rstring += " "+str(srow)
            rstring += "-- \n"
        return rstring 
    
    def table_map(self):
        rstring = ""
        for row in self.som.nodes:
            srow = ""
            for node in row:
                pass
    
    
    
