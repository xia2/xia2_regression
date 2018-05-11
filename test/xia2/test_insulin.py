from __future__ import absolute_import, division, print_function

import os

from xia2_regression.test.xia2 import run_xia2_tolerant

def test_2d(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "insulin")
  assert os.path.exists(data_dir)

  command_line_args = [
    'pipeline=2di', 'nproc=1', 'trust_beam_centre=True', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_NATIVE_SWEEP1_INTEGRATE.mtz',
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("insulin.2d", command_line_args,
           expected_data_files=expected_data_files)
