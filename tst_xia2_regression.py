from __future__ import division
from __future__ import print_function

import scitbx.array_family.flex  # import dependency
import xia2_regression

def tst_xia2_regression():
  assert(xia2_regression.make_list(4) == [j for j in range(4)])
  assert(sum(xia2_regression.make_flex(10)) == \
         xia2_regression.sum(xia2_regression.make_flex(10)))
  from dxtbx.model.detector import Detector
  d = Detector()
  print(xia2_regression.detector_as_string(d))
  print('OK')

def tst2():
  import sys
  from dxtbx import load
  if len(sys.argv) < 2:
    return
  i = load(sys.argv[1])
  detector = i.get_detector()
  beam = i.get_beam()
  from scitbx import matrix
  m = matrix.sqr((1, 0, 0, 0, 1, 0, 0, 0, 1))
  print(scitbx.array_family.flex.sum(
      xia2_regression.x_map(detector[0], beam, m, 1, 0.1)))
  d = i.get_raw_data()
  print(d.focus())

if __name__ == '__main__':
  tst_xia2_regression()
  tst2()
