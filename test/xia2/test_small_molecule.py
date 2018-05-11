from __future__ import absolute_import, division, print_function

import os

from xia2_regression.test.xia2 import run_xia2_tolerant

def test_dials(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "small_molecule_example")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = ['pipeline=dials', 'small_molecule=True',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("small_molecule.dials", command_line_args,
           expected_data_files=expected_data_files)


def test_xds(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "small_molecule_example")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = ['pipeline=3dii', 'small_molecule=True',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("small_molecule.xds", command_line_args,
           expected_data_files=expected_data_files)


def test_xds_ccp4a(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "small_molecule_example")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = ['pipeline=3dii', 'small_molecule=True', 'scaler=ccp4a',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("small_molecule.ccp4a", command_line_args,
           expected_data_files=expected_data_files)
