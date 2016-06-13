from __future__ import division

import os
import libtbx.load_env
from libtbx.test_utils import open_tmp_directory
xia2_regression = libtbx.env.under_build("xia2_regression")
from xia2_regression.test.xia2 import run_xia2_tolerant

data_dir = os.path.join(xia2_regression, "test_data", "mad_example")
assert os.path.exists(data_dir)


def exercise_dials():
  command_line_args = [
    '-dials', 'nproc=1', 'njob=2', 'mode=parallel',
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


def exercise_xds():
  command_line_args = [
    '-3di', 'nproc=1', 'njob=2', 'mode=parallel',
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


def exercise_xds_ccp4a():
  command_line_args = [
    '-3di', 'scaler=ccp4a', 'nproc=1', 'njob=2', 'mode=parallel',
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


def run(args):
  exercises = (exercise_xds, exercise_xds_ccp4a, exercise_dials)
  if args:
    exercises = [globals().get('exercise_%s' %arg) for arg in args]
  for exercise in exercises:
    exercise()

if __name__ == '__main__':
  import sys
  from libtbx.utils import show_times_at_exit
  show_times_at_exit()
  run(sys.argv[1:])
