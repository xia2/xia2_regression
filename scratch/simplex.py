from scitbx import simplex
from scitbx.array_family import flex
import random

class simple_simplex(object):

  def __init__(self, values):
    self.n = len(values)
    self.x = values
    self.starting_simplex = []
    self.fcount = 0
    for ii in range(self.n + 1):
        self.starting_simplex.append(flex.double((ii + 0.1 * random.random(),
                                                  ii + 1 + 0.1 * random.random())))
    optimizer = simplex.simplex_opt(dimension = self.n,
                                    matrix = self.starting_simplex,
                                    evaluator = self,
                                    tolerance = 1e-10)
    self.x = optimizer.get_solution()
    print "SIMPLEX ITRATIONS", optimizer.count, self.fcount, "SOLUTION", list(self.x), self.target(self.x)

  def target(self, vector):
    self.fcount += 1
    origin = flex.double((1.0, 2.0))
    vector -= origin
    value = flex.sum(vector * vector)
    print value
    return value

if __name__ == '__main__':
  ss = simple_simplex(flex.double((3, 3)))
