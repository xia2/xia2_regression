from __future__ import division
import os
from libtbx import easy_run
from libtbx.test_utils import approx_equal, show_diff, open_tmp_directory

def run_xia2(command_line_args, expected_summary, expected_data_files=[]):

  cwd = os.path.abspath(os.curdir)
  tmp_dir = os.path.abspath(open_tmp_directory())
  os.chdir(tmp_dir)

  cmd = ' '.join(['xia2'] + command_line_args)
  print cmd
  result = easy_run.fully_buffered(command=cmd).raise_if_errors()
  #result.show_stdout()

  summary_file = os.path.join(tmp_dir, 'xia2-summary.dat')
  assert os.path.exists(summary_file)
  expected_summary_lines = expected_summary.split('\n')
  summary_text = open(summary_file, 'rb').read()
  summary_text_lines = summary_text.split('\n')
  print summary_text
  for line, expected in zip(summary_text_lines, expected_summary_lines):
    line = ' '.join(line.split())
    expected = ' '.join(expected.split())
    try:
      values_summary = [float(f) for f in line.split()[-3:]]
      values_expected = [float(f) for f in expected.split()[-3:]]
    except ValueError:
      assert not show_diff(line, expected)
    else:
      if ('I/sigma' in line):
        continue # I/sigma too variable, highly dependent on sigma estimates
                 # assert approx_equal(
                 # values_summary, values_expected, eps=2e-1), (line, expected)
      elif ('completeness' in line.lower()):
        # overall / low resolution expect comparable number, high resolution
        # be much more flexible
        assert approx_equal(
          values_summary[:2], values_expected[:2], eps=1), (line, expected)
        assert approx_equal(
          values_summary[2:], values_expected[2:], eps=10), (line, expected)
      elif ('resolution limit' in line):
        # just check last value => high limit
        assert approx_equal(
          values_summary[2:], values_expected[2:], eps=5e-2), (line, expected)
      elif ('Rmerge' in line):
        assert approx_equal(
          values_summary[2:], values_expected[2:], eps=1e-2), (line, expected)
        assert approx_equal(
          values_summary[2], values_expected[2], eps=1e-1), (line, expected)
      elif ('CC half' in line):
        assert approx_equal(
          values_summary[:2], values_expected[:2], eps=2e-2), (line, expected)
        assert approx_equal(
          values_summary[2:], values_expected[2:], eps=2e-1), (line, expected)
      elif ('multiplicity' in line.lower()):
        assert approx_equal(
          values_summary, values_expected, eps=3e-1), (line, expected)
      else:
        assert not show_diff(line, expected)

  for data_file in expected_data_files:
    assert os.path.exists(os.path.join('DataFiles', data_file)), data_file

  os.chdir(cwd)