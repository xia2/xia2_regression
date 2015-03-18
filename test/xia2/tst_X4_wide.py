from __future__ import division

import os

import libtbx.load_env
from libtbx.test_utils import open_tmp_directory

xia2_regression = libtbx.env.under_build("xia2_regression")

from xia2_regression.test.xia2 import run_xia2


split_xinfo_template = """/
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
"""

def exercise_dials():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = ['-dials', 'nproc=1', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 90
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.41    4.46    1.41
Low resolution limit                            29.03   29.03   1.49
Completeness                                    99.8    98.5    99.9
Multiplicity                                    5.5     5.0     5.5
I/sigma                                         8.9     32.1    2.5
Rmerge                                          0.076   0.02    0.351
CC half                                         0.998   1.0     0.901
Anomalous completeness                          99.3    99.3    99.4
Anomalous multiplicity                          3.0     3.2     2.9
Cell:  42.456  42.456  39.772  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %data_dir
  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template %(data_dir, data_dir)

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 40
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.26    4.54    1.26
Low resolution limit                            29.05   29.05   1.31
Completeness                                    94.0    98.4    86.7
Multiplicity                                    4.1     4.5     2.6
I/sigma                                         8.6     32.1    1.9
Rmerge                                          0.073   0.023   0.47
CC half                                         0.997   0.999   0.789
Anomalous completeness                          79.8    97.1    56.9
Anomalous multiplicity                          2.0     2.8     1.6
Cell:  42.509  42.509  39.800  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  command_line_args = ['-dials', 'nproc=1', 'njob=2', 'mode=parallel',
                       'xinfo=%s' %xinfo_file]
  run_xia2(command_line_args, expected_summary=expected_summary)


def exercise_xds():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = ['-3d', 'nproc=1', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 90
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                       1.31    5.86    1.31
Low resolution limit                        21.14   21.14   1.34
Completeness                                99.8    98.3    99.7
Multiplicity                                5.9     5.0     5.8
I/sigma                                     17.6    51.4    2.5
Rmerge                                      0.05    0.015   0.639
CC half                                     0.999   0.999   0.805
Anomalous completeness                      98.8    83.6    99.5
Anomalous multiplicity                      3.1     3.7     3.0
Cell:  42.430 42.430 39.800 90.000 90.000 90.000
Spacegroup: P 41 21 2
""" %data_dir

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template %(data_dir, data_dir)

  command_line_args = ['-3d', 'nproc=1', 'njob=2', 'mode=parallel',
                       'xinfo=%s' %xinfo_file]

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 40
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                       1.32    5.9     1.32
Low resolution limit                        23.95   23.95   1.35
Completeness                                99.2    98.9    91.5
Multiplicity                                5.5     4.7     3.2
I/sigma                                     16.0    41.6    2.4
Rmerge                                      0.053   0.019   0.539
CC half                                     0.999   0.999   0.74
Anomalous completeness                      95.9    79.6    64.1
Anomalous multiplicity                      2.8     3.4     2.0
Cell:  42.410  42.410  39.810  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds_ccp4a():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = ['-3d', 'nproc=1', 'scaler=ccp4a', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_free.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 90
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.34    4.44    1.34
Low resolution limit                            21.14   21.14   1.41
Completeness                                    99.9    98.5    100.0
Multiplicity                                    6.0     5.3     6.2
I/sigma                                         13.3    43.0    2.6
Rmerge                                          0.063   0.02    0.483
CC half                                         0.999   0.999   0.868
Anomalous completeness                          99.7    99.3    99.9
Anomalous multiplicity                          3.3     3.4     3.3
Cell:  42.430 42.430 39.800 90.000 90.000 90.000
Spacegroup: P 41 21 2
""" %data_dir

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template %(data_dir, data_dir)

  command_line_args = ['-3d', 'nproc=1', 'scaler=ccp4a', 'njob=2',
                       'mode=parallel', 'xinfo=%s' %xinfo_file]

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 40
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                       1.3     4.5     1.3
Low resolution limit                        23.88   23.88   1.36
Completeness                                97.9    98.7    90.6
Multiplicity                                5.2     5.0     2.8
I/sigma                                     11.0    30.5    1.9
Rmerge                                      0.075   0.033   0.572
CC half                                     0.998   0.997   0.734
Anomalous completeness                      91.5    99.3    61.8
Anomalous multiplicity                      2.7     3.1     1.7
Cell:  42.409 42.409 39.811 90.000 90.000 90.000
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
