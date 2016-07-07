from __future__ import division

import os
import libtbx.load_env
from xia2_regression.test.xia2 import run_xia2_tolerant

xia2_regression = libtbx.env.under_build("xia2_regression")
data_dir = os.path.join(xia2_regression, "test_data", "small_molecule_example")
assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

def exercise_dials():
  command_line_args = ['-dials', 'small_molecule=True',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("small_molecule.dials", command_line_args,
           expected_data_files=expected_data_files)


def exercise_xds():
  command_line_args = ['-3dii', 'small_molecule=True',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("small_molecule.xds", command_line_args,
           expected_data_files=expected_data_files)


def exercise_xds_ccp4a():
  command_line_args = ['-3dii', 'small_molecule=True', 'scaler=ccp4a',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  run_xia2_tolerant("small_molecule.ccp4a", command_line_args,
           expected_data_files=expected_data_files)

def run(args):
  exercises = (exercise_xds, exercise_xds_ccp4a, exercise_dials)
  if len(args):
    exercises = [globals().get('exercise_%s' %arg) for arg in args]

  for exercise in exercises:
    exercise()

if __name__ == '__main__':
  import sys
  from libtbx.utils import show_times_at_exit
  show_times_at_exit()
  run(sys.argv[1:])
