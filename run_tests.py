# xia2 tests - these may require the xia2_regression or dials_regression
# repositories to be available...

from __future__ import division
from libtbx import test_utils
import libtbx.load_env

tst_list = (
    ["$D/test/xia2/tst_X4_wide.py", "dials"],
    ["$D/test/xia2/tst_X4_wide.py", "xds"],
    ["$D/test/xia2/tst_X4_wide.py", "xds_ccp4a"],
    ["$D/test/command_line/tst_xia2.py", "1"],
    ["$D/test/command_line/tst_xia2.py", "2"],
)

def run () :

  build_dir = libtbx.env.under_build("xia2")
  dist_dir = libtbx.env.dist_path("xia2")
  test_utils.run_tests(build_dir, dist_dir, tst_list)

if (__name__ == "__main__"):
  run()
