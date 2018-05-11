from __future__ import print_function
import random

from scitbx import simplex
from scitbx.array_family import flex

def generate_start(values, offset):
  assert len(values) == len(offset)
  start = [values]
  for j, o in enumerate(offset):
    next = values.deep_copy()
    next[j] += o
    start.append(next)
  return start

class simple_simplex(object):

  def __init__(self, values, offset, params=None):
    self.params = params
    self.n = len(values)
    self.x = values
    self.starting_simplex = generate_start(values, offset)
    self.fcount = 0

    optimizer = simplex.simplex_opt(dimension=self.n,
                                    matrix=self.starting_simplex,
                                    evaluator=self,
                                    tolerance=1e-10,
                                    max_iter=1000000)

    self.x = optimizer.get_solution()
    print("Iterations %d %d" % (optimizer.count, self.fcount))
    print("Solution %s" % str(list(self.x)))
    print("Target %f" % self.target(self.x))

  def target(self, vector):
    self.fcount += 1
    value = abs(2 * vector[0] ** 2 + 3 * (vector[1] - 2) ** 2 + 1)
    return value

if __name__ == '__main__':
  ss = simple_simplex(flex.double((3, 3)), flex.double((0.1, 0.1)))
