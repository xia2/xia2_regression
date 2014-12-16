from __future__ import division

import os

import libtbx.load_env
from libtbx import easy_run
#from libtbx.test_utils import approx_equal
from libtbx.test_utils import open_tmp_directory

xia2_regression = libtbx.env.under_build("xia2_regression")

def exercise_1():
  cwd = os.path.abspath(os.curdir)
  tmp_dir = os.path.abspath(open_tmp_directory())
  os.chdir(tmp_dir)

  data_dir = os.path.join(xia2_regression, "test_data", "mad_example")
  assert os.path.exists(data_dir)
  options = ['-2d', 'nproc=1']
  cmd = "xia2 %s %s" %(" ".join(options), data_dir)
  print cmd
  result = easy_run.fully_buffered(command=cmd).raise_if_errors()
  #result.show_stdout()
  assert os.path.exists(
    os.path.join(tmp_dir, "DataFiles/AUTOMATIC_DEFAULT_scaled_WAVE1.sca"))
  assert os.path.exists(
    os.path.join(tmp_dir, "DataFiles/AUTOMATIC_DEFAULT_scaled_WAVE2.sca"))
  assert os.path.exists(
    os.path.join(tmp_dir, "DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged_WAVE1.sca"))
  assert os.path.exists(
    os.path.join(tmp_dir, "DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged_WAVE2.sca"))
  # XXX should probably test the data quality here too somehow


def exercise_2():
  cwd = os.path.abspath(os.curdir)
  tmp_dir = os.path.abspath(open_tmp_directory())
  os.chdir(tmp_dir)

  data_dir = os.path.join(xia2_regression, "test_data", "insulin")
  assert os.path.exists(data_dir)
  options = ['-2d', 'nproc=1']

  with open('subset.xinfo', 'wb') as f:
    print >> f, """\
BEGIN PROJECT AUTOMATIC
BEGIN CRYSTAL DEFAULT

BEGIN WAVELENGTH NATIVE
WAVELENGTH 0.979000
END WAVELENGTH NATIVE

BEGIN SWEEP SWEEP1
WAVELENGTH NATIVE
DIRECTORY %s
IMAGE insulin_1_001.img
START_END 1 15
BEAM  94.34  94.50
END SWEEP SWEEP1

BEGIN SWEEP SWEEP2
WAVELENGTH NATIVE
DIRECTORY %s
IMAGE insulin_1_001.img
START_END 22 42
BEAM  94.34  94.50
END SWEEP SWEEP2

END CRYSTAL DEFAULT
END PROJECT AUTOMATIC
""" %(data_dir, data_dir)

  cmd = "xia2 %s -xinfo subset.xinfo" %(" ".join(options))
  print cmd
  result = easy_run.fully_buffered(command=cmd).raise_if_errors()
  #result.show_stdout()
  assert os.path.exists(
    os.path.join(tmp_dir, "DataFiles/AUTOMATIC_DEFAULT_scaled.sca"))
  assert os.path.exists(
    os.path.join(tmp_dir, "DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged.sca"))
  # XXX should probably test the data quality here too somehow


def run(args):
  exercises = (exercise_1, exercise_2)
  if len(args):
    args = [int(arg) for arg in args]
    for arg in args: assert arg > 0
    exercises = [exercises[arg-1] for arg in args]

  for exercise in exercises:
    exercise()

if __name__ == '__main__':
  import sys
  from libtbx.utils import show_times_at_exit
  show_times_at_exit()
  run(sys.argv[1:])
