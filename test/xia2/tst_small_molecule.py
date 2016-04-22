from __future__ import division

import os
import libtbx.load_env
from xia2_regression.test.xia2 import run_xia2_tolerant

xia2_regression = libtbx.env.under_build("xia2_regression")
data_dir = os.path.join(xia2_regression, "test_data", "small_molecule_example")
assert os.path.exists(data_dir), 'Please run xia2_regression.fetch_test_data first'

def exercise_dials():
  command_line_args = ['-dials', '-small_molecule',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.56356)
Sweep: SWEEP1
Files ***
Images: 1 to 900
Beam 208.78 214.29 => 208.86 214.37
Distance 191.42 => 194.05
Date: Thu Apr 14 12:41:44 2016
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                    	  0.64(0.03)      1.74(10%)	  0.64(0.03)
Low resolution limit                     	 11.21(0.20)	 11.21(**)	  0.65(**)
Completeness                             	 92.8(3.0)	100.0(3.0)	 48.3(**)
Multiplicity                             	  3.2   	  3.3    	  2.3(0.3)
I/sigma                                  	  4.5(0.3)	 14.4(5.0)	  0.8(1.0)
CC half                                  	0.997(0.5%)	0.998(1.0%)	0.677(50%)
Cell:   9.414  16.989  15.182  90.000 100.816  90.000
Spacegroup: P 1 21/n 1
"""
  run_xia2_tolerant(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds():
  command_line_args = ['-3di', '-small_molecule',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.56356)
Sweep: SWEEP1
Files ***
Images: 1 to 900
Beam 208.78 214.29 => 208.86 214.37
Distance 191.42 => 194.05
Date: Thu Apr 14 12:41:44 2016
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                    	  0.64(0.03)      1.74(10%)	  0.64(0.03)
Low resolution limit                     	 11.21(0.20)	 11.21(**)	  0.65(**)
Completeness                             	 92.8(3.0)	100.0(3.0)	 48.3(**)
Multiplicity                             	  3.2   	  3.3    	  2.3(0.3)
I/sigma                                  	  4.5(0.3)	 14.4(5.0)	  0.8(1.0)
CC half                                  	0.997(0.5%)	0.998(1.0%)	0.677(50%)
Cell:   9.414  16.989  15.182  90.000 100.816  90.000
Spacegroup: P 1 21/n 1
"""

  run_xia2_tolerant(command_line_args, expected_summary=expected_summary,
           expected_data_files=expected_data_files)


def exercise_xds_ccp4a():
  command_line_args = ['-3di', '-small_molecule', 'scaler=ccp4a',
                       'trust_beam_centre=True', 'nproc=2',
                       'read_all_image_headers=False', data_dir]

  expected_data_files = [
    'AUTOMATIC_DEFAULT_scaled.mtz',
    'AUTOMATIC_DEFAULT_scaled.sca',
    'AUTOMATIC_DEFAULT_scaled_unmerged.mtz',
    'AUTOMATIC_DEFAULT_scaled_unmerged.sca']

  expected_summary = """\
Project: AUTOMATIC
Crystal: DEFAULT
Sequence length: 0
Wavelength: NATIVE (0.56356)
Sweep: SWEEP1
Files ***
Images: 1 to 900
Beam 208.78 214.29 => 208.86 214.37
Distance 191.42 => 194.05
Date: Thu Apr 14 12:41:44 2016
For AUTOMATIC/DEFAULT/NATIVE:
High resolution limit                    	  0.64(0.04)      1.74(10%)	  0.64(0.04)
Low resolution limit                     	 11.21(0.20)	 11.21(**)	  0.65(**)
Completeness                             	 95.8(3.0)	100.0(3.0)	 48.3(**)
Multiplicity                             	  3.2   	  3.3(0.7)    	  2.3(0.3)
I/sigma                                  	  4.5(1.0)	 14.4(5.0)	  0.8(1.0)
CC half                                  	0.997(0.5%)	0.998(1.0%)	0.677(50%)
Cell:   9.414  16.989  15.182  90.000 100.816  90.000
Spacegroup: P 1 21/n 1
"""

  run_xia2_tolerant(command_line_args, expected_summary=expected_summary,
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
