from __future__ import division

import os

import libtbx.load_env
from libtbx.test_utils import open_tmp_directory

xia2_regression = libtbx.env.under_build("xia2_regression")

from xia2_regression.test.xia2 import run_xia2


def exercise_dials():

  data_dir = os.path.join(xia2_regression, "test_data", "mad_example")
  assert os.path.exists(data_dir)
  command_line_args = [
    '-dials', 'nproc=1', 'njob=2', 'mode=parallel', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.mtz']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files %s/12287_1_E1_###.img
Images: 1 to 60
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files %s/12287_1_E2_###.img
Images: 1 to 60
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                           1.64    6.14    1.64
Low resolution limit                            52.49   52.49   1.7
Completeness                                    97.5    98.6    83.0
Multiplicity                                    4.2     3.5     2.8
I/sigma                                         10.2    16.8    2.2
Rmerge                                          0.055   0.039   0.318
CC half                                         0.997   0.994   0.823
Anomalous completeness                          96.4    99.4    76.5
Anomalous multiplicity                          2.3     2.3     1.6
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.62    6.06    1.62
Low resolution limit                            43.11   43.11   1.68
Completeness                                    94.9    98.5    70.9
Multiplicity                                    4.1     3.5     2.5
I/sigma                                         9.6     15.3    2.2
Rmerge                                          0.057   0.041   0.313
CC half                                         0.998   0.997   0.833
Anomalous completeness                          93.3    98.8    66.2
Anomalous multiplicity                          2.2     2.3     1.4
Cell:  51.522  51.522 157.484  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds():

  data_dir = os.path.join(xia2_regression, "test_data", "mad_example")
  assert os.path.exists(data_dir)
  command_line_args = [
    '-3d', 'nproc=1', 'njob=2', 'mode=parallel', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.mtz']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files %s/12287_1_E1_###.img
Images: 1 to 60
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files %s/12287_1_E2_###.img
Images: 1 to 60
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                           1.64    7.33    1.64
Low resolution limit                            43.15   43.15   1.68
Completeness                                    96.9    92.9    80.7
Multiplicity                                    4.2     3.3     2.8
I/sigma                                         17.7    39.4    2.1
Rmerge                                          0.042   0.021   0.4
CC half                                         0.998   0.996   0.729
Anomalous completeness                          92.3    83.1    74.6
Anomalous multiplicity                          2.2     2.3     1.6
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.65    7.19    1.65
Low resolution limit                            43.15   43.15   1.7
Completeness                                    95.9    96.1    74.5
Multiplicity                                    4.2     3.4     2.7
I/sigma                                         19.6    43.2    2.3
Rmerge                                          0.038   0.018   0.359
CC half                                         0.999   0.999   0.764
Anomalous completeness                          90.8    90.9    70.0
Anomalous multiplicity                          2.2     2.3     1.5
Cell:  51.570  51.570 157.610  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds_ccp4a():

  data_dir = os.path.join(xia2_regression, "test_data", "mad_example")
  assert os.path.exists(data_dir)
  command_line_args = [
    '-3d', 'scaler=ccp4a', 'nproc=1', 'njob=2', 'mode=parallel', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.sca',
    'AUTOMATIC_DEFAULT_scaled_WAVE1.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.mtz']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files %s/12287_1_E1_###.img
Images: 1 to 60
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files %s/12287_1_E2_###.img
Images: 1 to 60
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                           1.66    5.99    1.66
Low resolution limit                            39.4    39.4    1.73
Completeness                                    98.3    99.1    89.0
Multiplicity                                    4.4     3.7     3.0
I/sigma                                         13.6    27.3    2.2
Rmerge                                          0.052   0.028   0.356
CC half                                         0.989   0.951   0.68
Anomalous completeness                          97.3    98.3    81.7
Anomalous multiplicity                          2.3     2.4     1.7
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.66    5.99    1.66
Low resolution limit                            39.4    39.4    1.73
Completeness                                    97.0    99.5    80.0
Multiplicity                                    4.3     3.7     2.8
I/sigma                                         13.8    26.1    2.3
Rmerge                                          0.05    0.031   0.323
CC half                                         0.984   0.901   0.789
Anomalous completeness                          95.7    98.6    74.8
Anomalous multiplicity                          2.3     2.4     1.5
Cell:  51.566  51.566 157.600  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  run_xia2(command_line_args, expected_summary=expected_summary,
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
