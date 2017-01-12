from __future__ import division
import scitbx.array_family.flex # import dependency
import xia2_regression

def tst_xia2_regression():
  assert(xia2_regression.make_list(4) == [j for j in range(4)])
  assert(sum(xia2_regression.make_flex(10)) == \
         xia2_regression.sum(xia2_regression.make_flex(10)))
  from dxtbx.model.detector import Detector
  d = Detector()
  print xia2_regression.detector_as_string(d)
  print 'OK'

if __name__ == '__main__':
  tst_xia2_regression()
