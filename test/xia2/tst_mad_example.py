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

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files %s/12287_1_E1_###.img
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.14
Distance 170.00 => 168.98
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files %s/12287_1_E2_###.img
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.14
Distance 170.00 => 168.96
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                       1.64    7.33    1.64
Low resolution limit                        52.43   52.43   1.68
Completeness                                97.6    97.0    81.7
Multiplicity                                4.3     3.4     2.7
I/sigma                                     12.9    26.5    1.9
Rmerge                                      0.048   0.026   0.336
CC half                                     0.997   0.997   0.805
Anomalous completeness                      96.3    95.5    75.3
Anomalous multiplicity                      2.3     2.3     1.5
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                       1.64    7.33    1.64
Low resolution limit                        43.06   43.06   1.68
Completeness                                95.7    98.5    69.3
Multiplicity                                4.2     3.4     2.3
I/sigma                                     13.5    26.4    2.2
Rmerge                                      0.047   0.028   0.336
CC half                                     0.998   0.999   0.815
Anomalous completeness                      93.4    99.4    57.2
Anomalous multiplicity                      2.2     2.3     1.3
Cell:  51.457  51.457 157.304  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds():

  data_dir = os.path.join(xia2_regression, "test_data", "mad_example")
  assert os.path.exists(data_dir)
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

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files %s/12287_1_E1_###.img
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.23
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files %s/12287_1_E2_###.img
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.18
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                           1.65    7.38    1.65
Low resolution limit                            43.15   43.15   1.69
Completeness                                    97.6    93.8    86.0
Multiplicity                                    4.3     3.4     2.9
I/sigma                                         17.8    40.1    2.2
Rmerge                                          0.042   0.021   0.39
CC half                                         0.998   0.997   0.738
Anomalous completeness                          93.1    85.1    79.3
Anomalous multiplicity                          2.2     2.3     1.6
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.65    7.38    1.65
Low resolution limit                            43.15   43.15   1.69
Completeness                                    95.9    92.4    76.8
Multiplicity                                    4.2     3.2     2.7
I/sigma                                         19.4    44.1    2.2
Rmerge                                          0.039   0.018   0.37
CC half                                         0.999   0.999   0.769
Anomalous completeness                          90.5    79.9    71.4
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

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files %s/12287_1_E1_###.img
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.23
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files %s/12287_1_E2_###.img
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.18
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                           1.66    7.42    1.66
Low resolution limit                            39.4    39.4    1.7
Completeness                                    98.6    97.5    89.5
Multiplicity                                    4.4     3.5     2.9
I/sigma                                         13.8    27.8    2.0
Rmerge                                          0.052   0.028   0.39
CC half                                         0.995   0.996   0.757
Anomalous completeness                          97.4    97.1    82.0
Anomalous multiplicity                          2.3     2.3     1.6
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.66    7.42    1.66
Low resolution limit                            39.4    39.4    1.7
Completeness                                    97.3    99.5    79.4
Multiplicity                                    4.3     3.4     2.8
I/sigma                                         14.1    27.0    2.1
Rmerge                                          0.05    0.032   0.375
CC half                                         0.995   0.992   0.78
Anomalous completeness                          96.0    99.4    74.4
Anomalous multiplicity                          2.3     2.3     1.5
Cell:  51.566  51.566 157.597  90.000  90.000  90.000
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
