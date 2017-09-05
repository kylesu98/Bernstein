import numpy as np
import numpy.linalg as lin
import scipy.stats as stat

from magic import *

def normalize(x):
    return x/lin.norm(x)

class Source:
    def __init__(self, pos, amt, name=None):
        self.pos = pos
        self.amt = amt
        self.name = name

    def __str__(self):
        return self.name + ': ' + str(self.pos) + ', ' + str(self.amt)

class System:
    def __init__(self, ground):
        self.ground = ground
        self.sources = []
        self.distances = np.array([])
        self.barycenter = None
        self.p = None

    def add_source(self, src):
        self.sources.append(src)
        self.barycenter = self.calc_barycenter()
        
    def calc_barycenter(self):
        wts = np.asarray([src.amt for src in self.sources])
        wts = wts/np.sum(wts)
        cds = [src.pos for src in self.sources]
        return np.dot(wts, cds)

    def dark(self):
        span = len(self.sources)*(self.ground-self.barycenter) + self.ground
        pos = normalize(normalize(span)/max(span))
        amt = lin.norm(span)
        displacement = pos - self.ground
        z = (lin.norm(displacement) - DISPLACEMENT_MU)/DISPLACEMENT_SIGMA
        self.p = stat.norm.sf(abs(z))
        return Source(pos, amt, "Dark donor")