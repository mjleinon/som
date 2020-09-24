# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:49:27 2020

@author: M Leinonen
"""

import matplotlib.pyplot as plt
import numpy as np

def arrayshow_flipped(data, label='colorMap'):
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    ax.set_title(label)
    plt.imshow(data, origin="upper")
    ax.set_aspect('equal')
    
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()


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
                    
                
    
    
