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
Distance 170.00 => 169.05
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files %s/12287_1_E2_###.img
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.14
Distance 170.00 => 169.07
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                           1.55    6.93    1.55
Low resolution limit                            52.45   52.45   1.59
Completeness                                    92.6    97.0    60.1
Multiplicity                                    4.1     3.5     2.2
I/sigma                                         11.8    26.7    1.2
Rmerge                                          0.049   0.026   0.486
CC half                                         0.997   0.997   0.674
Anomalous completeness                          90.5    95.8    53.2
Anomalous multiplicity                          2.2     2.3     1.2
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.57    6.84    1.57
Low resolution limit                            43.07   43.07   1.61
Completeness                                    89.6    98.8    39.4
Multiplicity                                    4.0     3.5     1.5
I/sigma                                         12.9    26.6    1.1
Rmerge                                          0.047   0.028   0.432
CC half                                         0.998   0.998   0.569
Anomalous completeness                          84.6    99.6    16.6
Anomalous multiplicity                          2.1     2.3     1.1
Cell:  51.473  51.473 157.354  90.000  90.000  90.000
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
High resolution limit                           1.58    6.89    1.58
Low resolution limit                            43.15   43.15   1.62
Completeness                                    94.4    94.5    68.2
Multiplicity                                    4.1     3.4     2.5
I/sigma                                         16.4    40.2    1.5
Rmerge                                          0.043   0.02    0.505
CC half                                         0.998   0.997   0.568
Anomalous completeness                          89.8    84.8    64.2
Anomalous multiplicity                          2.2     2.3     1.4
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.56    6.98    1.56
Low resolution limit                            43.15   43.15   1.6
Completeness                                    90.7    92.4    57.1
Multiplicity                                    4.0     3.3     2.1
I/sigma                                         17.6    44.2    1.2
Rmerge                                          0.039   0.018   0.553
CC half                                         0.999   0.999   0.505
Anomalous completeness                          84.9    80.1    47.8
Anomalous multiplicity                          2.1     2.3     1.2
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
High resolution limit                           1.58    6.89    1.58
Low resolution limit                            39.4    39.4    1.62
Completeness                                    94.9    97.5    68.5
Multiplicity                                    4.2     3.5     2.5
I/sigma                                         12.5    27.9    1.4
Rmerge                                          0.053   0.028   0.512
CC half                                         0.996   0.995   0.638
Anomalous completeness                          93.1    96.4    64.6
Anomalous multiplicity                          2.2     2.3     1.4
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                           1.56    6.98    1.56
Low resolution limit                            39.4    39.4    1.6
Completeness                                    91.6    99.6    57.3
Multiplicity                                    4.1     3.5     2.2
I/sigma                                         12.6    27.1    1.1
Rmerge                                          0.051   0.032   0.558
CC half                                         0.996   0.986   0.608
Anomalous completeness                          89.0    99.5    48.1
Anomalous multiplicity                          2.2     2.3     1.2
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
