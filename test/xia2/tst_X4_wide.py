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
  command_line_args = ['-dials', 'nproc=1', 'trust_beam_centre=True', data_dir]

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
Beam 220.00 212.48 => 219.87 212.62
Distance 190.18 => 192.05
Date: Fri Feb  8 13:23:40 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.19    5.32    1.19
Low resolution limit                            28.93   28.93   1.22
Completeness                                    99.9    99.6    100.0
Multiplicity                                    5.6     5.1     5.3
I/sigma                                         7.7     19.6    1.3
Rmerge                                          0.09    0.036   0.92
CC half                                         0.997   0.999   0.801
Anomalous completeness                          99.3    100.0   99.3
Anomalous multiplicity                          2.9     3.4     2.8
Cell:  42.331  42.331  39.638  90.000  90.000  90.000
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
Beam 220.00 212.48 => 219.90 212.60
Distance 190.18 => 192.26
Date: Fri Feb  8 13:23:40 2013
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
Beam 220.00 212.48 => 219.87 212.65
Distance 190.18 => 191.83
Date: Fri Feb  8 13:24:24 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.26    5.64    1.26
Low resolution limit                            29.95   29.95   1.29
Completeness                                    99.5    99.8    95.4
Multiplicity                                    5.0     4.7     4.3
I/sigma                                         7.9     20.2    1.5
Rmerge                                          0.077   0.03    0.574
CC half                                         0.998   0.999   0.851
Anomalous completeness                          97.0    96.8    83.7
Anomalous multiplicity                          2.6     3.2     2.4
Cell:  42.361  42.361  39.624  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  command_line_args = ['-dials', 'nproc=1', 'njob=2', 'mode=parallel',
                       'trust_beam_centre=True', 'xinfo=%s' %xinfo_file]
  run_xia2(command_line_args, expected_summary=expected_summary)


def exercise_xds():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = ['-3di', 'nproc=1', 'trust_beam_centre=True', data_dir]

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
Beam 220.00 212.48 => 219.86 212.59
Distance 190.18 => 192.16
Date: Fri Feb  8 13:23:40 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.22    5.46    1.22
Low resolution limit                            21.14   21.14   1.25
Completeness                                    99.9    98.7    100.0
Multiplicity                                    5.9     5.1     6.0
I/sigma                                         14.1    48.4    1.4
Rmerge                                          0.054   0.018   1.084
CC half                                         0.999   1.0     0.578
Anomalous completeness                          98.9    84.3    99.7
Anomalous multiplicity                          3.1     3.6     3.1
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
                       'trust_beam_centre=True', 'xinfo=%s' %xinfo_file]

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 40
Beam 220.00 212.48 => 219.88 212.58
Distance 190.18 => 192.18
Date: Fri Feb  8 13:23:40 2013
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
Beam 220.00 212.48 => 219.86 212.68
Distance 190.18 => 191.95
Date: Fri Feb  8 13:24:24 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.22    5.46    1.22
Low resolution limit                            23.88   23.88   1.25
Completeness                                    99.0    99.1    91.1
Multiplicity                                    5.4     4.8     2.9
I/sigma                                         12.9    42.1    1.5
Rmerge                                          0.06    0.022   0.96
CC half                                         0.998   0.999   0.566
Anomalous completeness                          95.4    88.6    66.8
Anomalous multiplicity                          2.8     3.2     1.8
Cell:  42.300  42.300  39.650  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds_ccp4a():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = [
    '-3di', 'nproc=1', 'scaler=ccp4a', 'trust_beam_centre=True', data_dir]

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
Beam 220.00 212.48 => 219.86 212.59
Distance 190.18 => 192.16
Date: Fri Feb  8 13:23:40 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.24    5.55    1.24
Low resolution limit                            23.85   23.85   1.27
Completeness                                    99.9    99.1    100.0
Multiplicity                                    6.0     5.4     6.0
I/sigma                                         10.6    39.3    1.2
Rmerge                                          0.072   0.021   0.909
CC half                                         0.999   1.0     0.685
Anomalous completeness                          99.7    100.0   99.9
Anomalous multiplicity                          3.2     3.6     3.1
Cell:  42.275  42.275  39.578  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %data_dir

  run_xia2(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)

  tmp_dir = os.path.abspath(open_tmp_directory())
  xinfo_file = os.path.join(tmp_dir, 'split.xinfo')
  with open(xinfo_file, 'wb') as f:
    print >> f, split_xinfo_template %(data_dir, data_dir)

  command_line_args = [
    '-3di', 'nproc=1', 'scaler=ccp4a', 'njob=2',
    'trust_beam_centre=True', 'mode=parallel', 'xinfo=%s' %xinfo_file]

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.97950)
Sweep: SWEEP1
Files %s/X4_wide_M1S4_2_####.cbf
Images: 1 to 40
Beam 220.00 212.48 => 219.88 212.58
Distance 190.18 => 192.18
Date: Fri Feb  8 13:23:40 2013
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
Beam 220.00 212.48 => 219.86 212.68
Distance 190.18 => 191.95
Date: Fri Feb  8 13:24:24 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.25    5.59    1.25
Low resolution limit                            23.88   23.88   1.28
Completeness                                    99.6    99.0    95.2
Multiplicity                                    5.6     5.1     4.1
I/sigma                                         9.1     27.0    1.1
Rmerge                                          0.078   0.037   0.774
CC half                                         0.997   0.994   0.699
Anomalous completeness                          97.7    100.0   78.1
Anomalous multiplicity                          3.0     3.4     2.4
Cell:  42.308  42.308  39.658  90.000  90.000  90.000
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
