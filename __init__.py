from __future__ import division
try:
  import boost.python
except Exception:
  ext = None
else:
  ext = boost.python.import_ext("xia2_regression_ext", optional=True)

if not ext is None:
  from xia2_regression_ext import *
