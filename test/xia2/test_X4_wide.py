from __future__ import absolute_import, division, print_function

import os

from libtbx.test_utils import open_tmp_directory
from xia2_regression.test.xia2 import run_xia2_tolerant

split_xinfo_template = lambda data_dir: """/
BEGIN PROJECT AUTOMATIC
BEGIN CRYSTAL DEFAULT

BEGIN WAVELENGTH NATIVE
WAVELENGTH 0.979500
END WAVELENGTH NATIVE

BEGIN SWEEP SWEEP1
WAVELENGTH NATIVE
DIRECTORY %s
IMAGE X4_wide_M1S4_2_0001.cbf
START_END 1 40
BEAM 219.84 212.65
END SWEEP SWEEP1

BEGIN SWEEP SWEEP2
WAVELENGTH NATIVE
DIRECTORY %s
IMAGE X4_wide_M1S4_2_0001.cbf
START_END 45 90
BEAM 219.84 212.65
END SWEEP SWEEP2

END CRYSTAL DEFAULT
END PROJECT AUTOMATIC
""" % (data_dir, data_dir)

def test_dials(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "X4_wide")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = ['pipeline=dials', 'nproc=1', 'trust_beam_centre=True',
                       'read_all_image_headers=False', 'truncate=cctbx',
                       data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("X4_wide.dials", command_line_args,
           expected_data_files=expected_data_files)


def test_dials_split(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "X4_wide")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template(data_dir)

  command_line_args = ['pipeline=dials', 'nproc=1', 'njob=2', 'mode=parallel',
                       'trust_beam_centre=True', 'xinfo=%s' % xinfo_file]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("X4_wide_split.dials", command_line_args,
           expected_data_files=expected_data_files)


def test_xds(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "X4_wide")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = ['pipeline=3di', 'nproc=1', 'trust_beam_centre=True',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("X4_wide.xds", command_line_args,
           expected_data_files=expected_data_files)


def test_xds_split(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "X4_wide")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template(data_dir)

  command_line_args = ['pipeline=3di', 'nproc=1', 'njob=2', 'mode=parallel',
                       'trust_beam_centre=True', 'xinfo=%s' %xinfo_file]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("X4_wide_split.xds", command_line_args,
           expected_data_files=expected_data_files)


def test_xds_ccp4a(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "X4_wide")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  command_line_args = [
    'pipeline=3di', 'nproc=1', 'scaler=ccp4a', 'trust_beam_centre=True', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("X4_wide.ccp4a", command_line_args,
           expected_data_files=expected_data_files)


def test_xds_ccp4a_split(xia2_regression_build, ccp4):
  data_dir = os.path.join(xia2_regression_build, "test_data", "X4_wide")
  assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template(data_dir)

  command_line_args = [
    'pipeline=3di', 'nproc=1', 'scaler=ccp4a', 'njob=2',
    'merging_statistics.source=aimless',
    'trust_beam_centre=True', 'mode=parallel', 'xinfo=%s' % xinfo_file]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("X4_wide_split.ccp4a", command_line_args,
           expected_data_files=expected_data_files)
