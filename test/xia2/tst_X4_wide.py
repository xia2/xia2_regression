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
High resolution limit                           1.39    4.4     1.39
Low resolution limit                            30.03   30.03   1.47
Completeness                                    99.8    98.7    100.0
Multiplicity                                    5.5     4.9     5.6
I/sigma                                         8.6     31.5    2.4
Rmerge                                          0.078   0.022   0.362
Anomalous completeness                          99.3    99.3    99.4
Anomalous multiplicity                          3.0     3.2     2.9
Cell:  42.474  42.474  39.753  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %data_dir

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)

  #tmp_dir = os.path.abspath(open_tmp_directory())
  #xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  #with open(xinfo_file, 'wb') as f:
    #print >> f, split_xinfo_template %(data_dir, data_dir)

  #command_line_args = ['-dials', 'nproc=1', 'njob=2', 'mode=parallel',
                       #'xinfo=%s' %xinfo_file]
  #run_xia2(command_line_args, expected_summary=expected_summary)


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
High resolution limit                           1.31    5.86    1.31
Low resolution limit                            21.14   21.14   1.34
Completeness                                    99.8    98.3    99.7
Multiplicity                                    5.9     5.0     5.8
I/sigma                                         17.6    51.4    2.5
Rmerge                                          0.047   0.015   0.601
Anomalous completeness                          98.6    81.5    99.1
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
High resolution limit                           1.3     5.81    1.3
Low resolution limit                            23.88   23.88   1.33
Completeness                                    98.8    98.9    90.4
Multiplicity                                    5.3     4.7     2.7
I/sigma                                         16.0    45.0    2.2
Rmerge                                          0.05    0.016   0.564
Anomalous completeness                          94.1    80.0    57.9
Anomalous multiplicity                          2.8     3.3     1.7
Cell:  42.300  42.300  39.650  90.000  90.000  90.000
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
Anomalous completeness                          99.7    99.3    99.9
Anomalous multiplicity                          3.3     3.4     3.3
Cell:  42.274  42.274  39.579  90.000  90.000  90.000
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
High resolution limit                           1.3     4.5     1.3
Low resolution limit                            23.88   23.88   1.36
Completeness                                    97.9    98.7    90.6
Multiplicity                                    5.2     5.0     2.8
I/sigma                                         11.0    30.5    1.9
Rmerge                                          0.066   0.025   0.544
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
