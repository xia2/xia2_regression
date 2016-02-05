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
Distance 190.18 => 192.11
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
Beam 220.00 212.48 => 219.89 212.60
Distance 190.18 => 192.22
Date: Fri Feb  8 13:23:40 2013
Sweep: SWEEP2
Files %s/X4_wide_M1S4_2_####.cbf
Images: 45 to 90
Beam 220.00 212.48 => 219.82 212.69
Distance 190.18 => 192.68
Date: Fri Feb  8 13:24:24 2013
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                           1.27    5.68    1.27
Low resolution limit                            30.01   30.01   1.3
Completeness                                    99.3    99.8    92.8
Multiplicity                                    5.0     4.7     3.4
I/sigma                                         7.8     21.6    1.0
Rmerge                                          0.078   0.031   0.613
CC half                                         0.997   0.999   0.805
Anomalous completeness                          96.3    96.8    74.3
Anomalous multiplicity                          2.6     3.2     2.0
Cell:  42.438  42.438  39.713  90.000  90.000  90.000
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
High resolution limit                       1.22    5.46    1.22
Low resolution limit                        21.14   21.14   1.25
Completeness                                99.8    98.7    100.0
Multiplicity                                5.9     5.1     6.0
I/sigma                                     14.1    48.9    1.4
Rmerge                                      0.054   0.017   1.085
CC half                                     0.999   1.0     0.567
Anomalous completeness                      99.0    84.3    99.7
Anomalous multiplicity                      3.1     3.6     3.1
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
High resolution limit                       1.21    5.41    1.21
Low resolution limit                        23.88   23.88   1.24
Completeness                                98.9    99.1    91.1
Multiplicity                                5.3     4.7     3.0
I/sigma                                     12.8    42.3    1.5
Rmerge                                      0.059   0.021   0.992
CC half                                     0.999   0.999   0.51
Anomalous completeness                      94.7    86.3    67.8
Anomalous multiplicity                      2.8     3.1     1.8
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
High resolution limit                       1.25    5.59    1.25
Low resolution limit                        21.13   21.13   1.28
Completeness                                99.9    98.6    100.0
Multiplicity                                6.0     5.4     6.0
I/sigma                                     11.0    40.6    1.3
Rmerge                                      0.071   0.019   0.808
CC half                                     0.999   0.999   0.709
Anomalous completeness                      99.7    100.0   100.0
Anomalous multiplicity                      3.2     3.6     3.1
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
High resolution limit                       1.25    5.59    1.25
Low resolution limit                        23.88   23.88   1.28
Completeness                                99.4    99.0    92.5
Multiplicity                                5.6     5.1     3.2
I/sigma                                     9.3     28.2    1.0
Rmerge                                      0.075   0.031   0.739
CC half                                     0.998   0.996   0.705
Anomalous completeness                      97.0    100.0   68.4
Anomalous multiplicity                      2.9     3.4     1.9
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
