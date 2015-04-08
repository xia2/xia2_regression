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
High resolution limit                           1.35    6.04    1.35
Low resolution limit                            30.02   30.02   1.39
Completeness                                    99.8    99.7    100.0
Multiplicity                                    5.6     5.1     5.8
I/sigma                                         9.0     54.1    1.9
Rmerge                                          0.08    0.02    0.45
CC half                                         0.998   1.0     0.898
Anomalous completeness                          99.3    100.0   99.6
Anomalous multiplicity                          3.0     3.6     3.0
Cell:  42.455  42.455  39.772  90.000  90.000  90.000
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
High resolution limit                           1.26    5.64    1.26
Low resolution limit                            29.05   29.05   1.29
Completeness                                    95.3    99.5    87.6
Multiplicity                                    4.3     4.7     2.6
I/sigma                                         8.8     30.7    2.1
Rmerge                                          0.074   0.023   0.498
CC half                                         0.997   0.999   0.802
Anomalous completeness                          83.5    96.9    58.8
Anomalous multiplicity                          2.1     3.2     1.6
Cell:  42.509  42.509  39.800  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  command_line_args = ['-dials', 'nproc=1', 'njob=2', 'mode=parallel',
                       'xinfo=%s' %xinfo_file]
  run_xia2(command_line_args, expected_summary=expected_summary)


def exercise_xds():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = ['-3di', 'nproc=1', data_dir]

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
High resolution limit                           1.31    5.86    1.31
Low resolution limit                            21.14   21.14   1.34
Completeness                                    99.8    98.3    99.7
Multiplicity                                    5.9     5.0     5.8
I/sigma                                         17.6    51.4    2.5
Rmerge                                          0.047   0.015   0.6
CC half                                         0.999   1.0     0.8
Anomalous completeness                          98.7    81.5    99.1
Anomalous multiplicity                          3.1     3.7     3.0
Cell:  42.280  42.280  39.590  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %data_dir

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template %(data_dir, data_dir)

  command_line_args = ['-3di', 'nproc=1', 'njob=2', 'mode=parallel',
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
High resolution limit                           1.29    5.77    1.29
Low resolution limit                            23.88   23.88   1.32
Completeness                                    98.8    98.9    89.9
Multiplicity                                    5.3     4.7     2.8
I/sigma                                         15.7    45.3    2.1
Rmerge                                          0.051   0.016   0.551
CC half                                         0.999   1.0     0.717
Anomalous completeness                          94.2    78.9    63.0
Anomalous multiplicity                          2.8     3.3     1.7
Cell:  42.300  42.300  39.650  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds_ccp4a():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = ['-3di', 'nproc=1', 'scaler=ccp4a', data_dir]

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
High resolution limit                           1.35    4.48    1.35
Low resolution limit                            23.85   23.85   1.42
Completeness                                    99.9    98.7    100.0
Multiplicity                                    6.0     5.3     6.1
I/sigma                                         13.2    40.2    2.7
Rmerge                                          0.063   0.021   0.467
CC half                                         0.999   0.999   0.884
Anomalous completeness                          99.7    99.3    99.8
Anomalous multiplicity                          3.3     3.4     3.2
Cell:  42.273  42.273  39.579  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %data_dir

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template %(data_dir, data_dir)

  command_line_args = ['-3di', 'nproc=1', 'scaler=ccp4a', 'njob=2',
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
High resolution limit                           1.3     4.5     1.3
Low resolution limit                            23.88   23.88   1.36
Completeness                                    97.9    98.7    90.6
Multiplicity                                    5.2     5.0     2.8
I/sigma                                         11.0    30.5    1.8
Rmerge                                          0.066   0.025   0.543
CC half                                         0.998   0.998   0.741
Anomalous completeness                          91.5    99.3    61.8
Anomalous multiplicity                          2.7     3.1     1.7
Cell:  42.305  42.305  39.654  90.000  90.000  90.000
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
