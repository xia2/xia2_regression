# xia2 tests - these may require the xia2_regression or dials_regression
# repositories to be available...

from __future__ import absolute_import, division, print_function

from libtbx.test_utils.pytest import discover

tst_list = [
    ["$D/test/xia2/tst_small_molecule.py", "dials"],
    ["$D/test/xia2/tst_small_molecule.py", "xds"],
    ["$D/test/xia2/tst_small_molecule.py", "xds_ccp4a"],
    ["$D/test/xia2/tst_insulin.py", "2d"],
    ["$D/test/xia2/tst_mad_example.py", "dials"],
    ["$D/test/xia2/tst_mad_example.py", "xds"],
    ["$D/test/xia2/tst_mad_example.py", "xds_ccp4a"],
    ["$D/test/xia2/tst_X4_wide.py", "dials"],
    ["$D/test/xia2/tst_X4_wide.py", "xds"],
    ["$D/test/xia2/tst_X4_wide.py", "xds_ccp4a"],
    ["$D/test/xia2/tst_X4_wide.py", "dials_split"],
    ["$D/test/xia2/tst_X4_wide.py", "xds_split"],
    ["$D/test/xia2/tst_X4_wide.py", "xds_ccp4a_split"],
] + discover()
