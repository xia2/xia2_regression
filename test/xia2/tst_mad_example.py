from __future__ import division

import os
import libtbx.load_env
from libtbx.test_utils import open_tmp_directory
xia2_regression = libtbx.env.under_build("xia2_regression")
from xia2_regression.test.xia2 import run_xia2_tolerant, ccp4_is_newer_or_equal_to

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

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.14
Distance 170.00 => 169.06
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.14
Distance 170.00 => 169.04
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                             1.55    4.21    1.55
Low resolution limit                             52.45   52.48    1.58
Completeness                                     92.5   100.0    57.3
Multiplicity                                      4.1     4.0     2.2
I/sigma                                          11.6    29.1     1.1
Rmerge(I+/-)                                    0.050   0.027   0.482
CC half                                         0.997   0.997   0.598
Anomalous completeness                           90.4    98.1     2.6
Anomalous multiplicity                            2.2     2.5     1.2
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                             1.58    4.29    1.58
Low resolution limit                             43.08   43.10    1.61
Completeness                                     90.7   100.0    39.5
Multiplicity                                      4.0     4.1     1.6
I/sigma                                          12.7    29.3     1.1
Rmerge(I+/-)                                    0.048   0.028   0.523
CC half                                         0.998   0.999   0.512
Anomalous completeness                           86.1    99.8     0.9
Anomalous multiplicity                            2.2     2.5     1.1
Cell:  51.480  51.480 157.370  90.000  90.000  90.000
Spacegroup: P 41 21 2
"""

  if ccp4_is_newer_or_equal_to(7, 0, 14): expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.14
Distance 170.00 => 169.07(0.1)
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.14
Distance 170.00 => 169.03(0.1)
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit               1.55(5%)    4.21(10%)   1.55(**)
Low resolution limit               52.45(5%)   52.48(**)    1.58(**)
Completeness                       92.5(5%)   100.0(2%)    57.3(5%)
Multiplicity                        4.1(0.2)    4.0(0.2)    2.2(0.2)
I/sigma                            11.6(5%)    29.1(5%)     1.1(0.2)
Rmerge(I+/-)                      0.050(5%)   0.027(5%)   0.482(5%)
CC half                           0.997(2%)   0.997(2%)   0.598(5%)
Anomalous completeness             90.4(2%)    98.1(5%)     2.6(2%)
Anomalous multiplicity              2.2(2%)     2.5(2%)     1.2(2%)
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit               1.58(5%)    4.29(10%)   1.58(**)
Low resolution limit               43.08(5%)   43.10(**)    1.61(**)
Completeness                       90.7(5%)   100.0(2%)    39.5(5%)
Multiplicity                        4.0(0.2)    4.1(0.2)    1.6(0.2)
I/sigma                            12.7(5%)    29.3(5%)     1.1(0.2)
Rmerge(I+/-)                      0.048(5%)   0.028(5%)   0.523(5%)
CC half                           0.998(2%)   0.999(2%)   0.512(5%)
Anomalous completeness             86.1(2%)    99.8(5%)     0.9(2%)
Anomalous multiplicity              2.2(2%)     2.5(2%)     1.1(2%)
Cell:  51.480(0.5%)  51.480(0.5%) 157.370(0.5%)  90.000  90.000  90.000
Spacegroup: P 41 21 2
"""

  run_xia2_tolerant(command_line_args, expected_summary=expected_summary,
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

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.28
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.27
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                             1.58    4.29    1.58
Low resolution limit                             36.80   36.81    1.61
Completeness                                     94.1    96.9    65.2
Multiplicity                                      4.1     3.9     2.4
I/sigma                                          16.4    43.1     1.4
Rmerge(I+/-)                                    0.043   0.021   0.546
CC half                                         0.998   0.997   0.570
Anomalous completeness                           89.8    87.8     3.2
Anomalous multiplicity                            2.3     2.5     1.3
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                             1.57    4.26    1.57
Low resolution limit                             43.15   43.17    1.60
Completeness                                     90.9    94.5    56.9
Multiplicity                                      4.0     3.8     2.2
I/sigma                                          17.8    47.9     1.2
Rmerge(I+/-)                                    0.039   0.019   0.578
CC half                                         0.999   0.999   0.515
Anomalous completeness                           85.6    81.2     2.5
Anomalous multiplicity                            2.2     2.5     1.2
Cell:  51.570  51.570 157.610  90.000  90.000  90.000
Spacegroup: P 41 21 2
"""

  run_xia2_tolerant(command_line_args, expected_summary=expected_summary,
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

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: WAVE1 (0.97966)
Sweep: SWEEP1
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.28
Date: Sun Sep 26 14:01:35 2004
Wavelength: WAVE2 (1.00000)
Sweep: SWEEP2
Files ***
Images: 1 to 60
Beam 108.95 105.10 => 108.98 105.15
Distance 170.00 => 169.27
Date: Sun Sep 26 14:05:43 2004
For AUTOMATIC/DEFAULT/WAVE1:
High resolution limit                             1.58    4.29    1.58
Low resolution limit                             39.40   39.41    1.61
Completeness                                     94.8    99.8    65.7
Multiplicity                                      4.2     4.1     2.4
I/sigma                                          12.5    30.4     1.4
Rmerge(I+/-)                                    0.054   0.028   0.524
CC half                                         0.995   0.997   0.658
Anomalous completeness                           93.2    97.8     3.2
Anomalous multiplicity                            2.3     2.5     1.3
For AUTOMATIC/DEFAULT/WAVE2:
High resolution limit                             1.56    4.23    1.56
Low resolution limit                             39.40   39.42    1.59
Completeness                                     91.5   100.0    54.9
Multiplicity                                      4.1     4.1     2.1
I/sigma                                          12.6    30.7     1.0
Rmerge(I+/-)                                    0.051   0.030   0.569
CC half                                         0.994   0.996   0.491
Anomalous completeness                           89.0    99.7     2.3
Anomalous multiplicity                            2.2     2.5     1.2
Cell:  51.566  51.566 157.598  90.000  90.000  90.000
Spacegroup: P 41 21 2
"""

  run_xia2_tolerant(command_line_args, expected_summary=expected_summary,
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
