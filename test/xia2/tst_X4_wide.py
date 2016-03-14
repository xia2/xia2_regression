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
  command_line_args = ['-dials', 'nproc=1', 'trust_beam_centre=True',
                       'read_all_image_headers=False', data_dir]

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
Beam 220.00 212.48 => 219.87 212.63
Distance 190.18 => 192.06
Date: Fri Feb  8 13:23:40 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                             1.20    3.26    1.20
Low resolution limit                             28.94   28.94    1.22
Completeness                                    100.0    99.9   100.0
Multiplicity                                      5.6     5.3     5.5
I/sigma                                           7.3    20.2     1.2
Rmerge(I+/-)                                    0.090   0.040   0.808
CC half                                         0.997   0.998   0.796
Anomalous completeness                           99.3    99.8     5.1
Anomalous multiplicity                            3.1     3.3     2.9
Cell:  42.335  42.335  39.642  90.000  90.000  90.000
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
Distance 190.18 => 192.14
Date: Fri Feb  8 13:23:40 2013
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
Beam 220.00 212.48 => 219.82 212.68
Distance 190.18 => 192.68
Date: Fri Feb  8 13:24:24 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                             1.28    3.47    1.28
Low resolution limit                             28.99   29.00    1.30
Completeness                                     99.3    99.6    87.3
Multiplicity                                      5.0     4.7     2.7
I/sigma                                           7.6    21.5     1.1
Rmerge(I+/-)                                    0.078   0.031   0.516
CC half                                         0.998   0.998   0.816
Anomalous completeness                           96.2    98.2     3.1
Anomalous multiplicity                            2.8     3.0     1.7
Cell:  42.435  42.435  39.705  90.000  90.000  90.000
Spacegroup: P 41 21 2
""" %(data_dir, data_dir)

  command_line_args = ['-dials', 'nproc=1', 'njob=2', 'mode=parallel',
                       'trust_beam_centre=True', 'xinfo=%s' %xinfo_file]
  run_xia2(command_line_args, expected_summary=expected_summary)


def exercise_xds():

  data_dir = os.path.join(xia2_regression, "test_data", "X4_wide")
  assert os.path.exists(data_dir)
  command_line_args = ['-3di', 'nproc=1', 'trust_beam_centre=True',
                       'read_all_image_headers=False', data_dir]

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
Distance 190.18 => 192.06
Date: Fri Feb  8 13:23:40 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                             1.22    3.31    1.22
Low resolution limit                             21.14   21.14    1.24
Completeness                                    100.0    99.7   100.0
Multiplicity                                      5.9     5.3     6.0
I/sigma                                          12.3    35.1     1.3
Rmerge(I+/-)                                    0.054   0.022   1.069
CC half                                         0.999   0.999   0.558
Anomalous completeness                           99.0    91.5     5.2
Anomalous multiplicity                            3.2     3.4     3.2
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
Distance 190.18 => 191.99
Date: Fri Feb  8 13:23:40 2013
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
Beam 220.00 212.48 => 219.86 212.68
Distance 190.18 => 191.97
Date: Fri Feb  8 13:24:24 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                             1.21    3.28    1.21
Low resolution limit                             23.88   23.88    1.23
Completeness                                     99.0    99.7    90.8
Multiplicity                                      5.3     5.0     2.9
I/sigma                                          12.8    43.3     1.4
Rmerge(I+/-)                                    0.059   0.027   1.045
CC half                                         0.999   0.999   0.499
Anomalous completeness                           94.7    91.8     3.5
Anomalous multiplicity                            3.0     3.2     1.8
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
Distance 190.18 => 192.06
Date: Fri Feb  8 13:23:40 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                             1.24    3.36    1.24
Low resolution limit                             21.13   21.13    1.26
Completeness                                    100.0   100.0   100.0
Multiplicity                                      6.0     5.6     6.0
I/sigma                                          10.3    40.6     1.0
Rmerge(I+/-)                                    0.074   0.024   0.884
CC half                                         0.999   0.999   0.670
Anomalous completeness                           99.7    99.7     5.3
Anomalous multiplicity                            3.3     3.5     3.2
Cell:  42.263  42.263  39.571  90.000  90.000  90.000
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
    'merging_statistics.source=aimless',
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
Distance 190.18 => 191.99
Date: Fri Feb  8 13:23:40 2013
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
Beam 220.00 212.48 => 219.86 212.68
Distance 190.18 => 191.97
Date: Fri Feb  8 13:24:24 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                             1.26    5.64    1.26
Low resolution limit                             23.88   23.88    1.29
Completeness                                     99.5    99.0    94.6
Multiplicity                                      5.6     5.1     4.0
I/sigma                                           9.1    27.0     1.1
Rmerge(I+/-)                                    0.077   0.030   0.742
CC half                                         0.997   0.997   0.752
Anomalous completeness                           97.8   100.0    78.4
Anomalous multiplicity                            3.0     3.4     2.3
Cell:  42.304  42.304  39.660  90.000  90.000  90.000
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
