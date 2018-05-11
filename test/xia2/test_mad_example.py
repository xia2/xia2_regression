from __future__ import absolute_import, division, print_function

import os

from xia2_regression.test.xia2 import run_xia2_tolerant

def test_dials(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "mad_example")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = [
    'pipeline=dials', 'nproc=1', 'njob=2', 'mode=parallel',
    'trust_beam_centre=True', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.mtz']

  run_xia2_tolerant("mad_example.dials", command_line_args,
           expected_data_files=expected_data_files)


def test_xds(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "mad_example")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = [
    'pipeline=3di', 'nproc=1', 'njob=2', 'mode=parallel',
    'trust_beam_centre=True', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.mtz']

  run_xia2_tolerant("mad_example.xds", command_line_args,
           expected_data_files=expected_data_files)


def test_xds_ccp4a(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "mad_example")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = [
    'pipeline=3di', 'scaler=ccp4a', 'nproc=1', 'njob=2', 'mode=parallel',
    'trust_beam_centre=True', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.mtz']

  run_xia2_tolerant("mad_example.ccp4a", command_line_args,
           expected_data_files=expected_data_files)
