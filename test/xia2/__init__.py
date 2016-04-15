from __future__ import division
import os
import re
import sys
from libtbx import easy_run
from libtbx.test_utils import approx_equal, show_diff, open_tmp_directory
from dials.util.procrunner import run_process

def run_xia2(command_line_args, expected_summary, expected_data_files=[]):

  cwd = os.path.abspath(os.curdir)
  tmp_dir = os.path.abspath(open_tmp_directory())
  os.chdir(tmp_dir)

  cmd = ' '.join(['xia2'] + command_line_args)
  print cmd
  result = easy_run.fully_buffered(command=cmd).raise_if_errors()
  #result.show_stdout()

  error_file = os.path.join(tmp_dir, 'xia2.error')
  if os.path.exists(error_file):
    result.show_stdout()
    with open(error_file, 'rb') as f:
      print f.read()
  html_file = os.path.join(tmp_dir, 'xia2.html')
  assert os.path.exists(html_file), "xia2.html not present after execution"
  summary_file = os.path.join(tmp_dir, 'xia2-summary.dat')
  assert os.path.exists(summary_file), "xia2-summary.dat not present after execution"
  expected_summary_lines = expected_summary.split('\n')
  summary_text = open(summary_file, 'rb').read()
  summary_text_lines = summary_text.split('\n')
  print summary_text
  for line, expected in zip(summary_text_lines, expected_summary_lines):
    line = ' '.join(line.split())
    expected = ' '.join(expected.split())
    try:
      if 'Cell' in line:
        values_summary = [float(f) for f in line.split()[-6:]]
        values_expected = [float(f) for f in expected.split()[-6:]]
      elif 'Distance' in line or 'Beam' in line:
        values_summary = [float(f) for f in line.replace('=>', ' ').split()[1:]]
        values_expected = [float(f) for f in expected.replace('=>', ' ').split()[1:]]
      else:
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
          values_summary[:2], values_expected[:2], eps=1.5), (line, expected)
        assert approx_equal(
          values_summary[2:], values_expected[2:], eps=10), (line, expected)
      elif ('resolution limit' in line):
        # just check last value => high limit
        assert approx_equal(
          values_summary[2:], values_expected[2:], eps=5e-2), (line, expected)
      elif ('Rmerge' in line):
        assert approx_equal(
          values_summary[:2], values_expected[:2], eps=1e-2), (line, expected)
        assert approx_equal(
          values_summary[2], values_expected[2], eps=1e-1), (line, expected)
      elif ('CC half' in line):
        assert approx_equal(
          values_summary[:2], values_expected[:2], eps=6e-2), (line, expected)
        assert approx_equal(
          values_summary[2:], values_expected[2:], eps=2e-1), (line, expected)
      elif ('multiplicity' in line.lower()):
        assert approx_equal(
          values_summary, values_expected, eps=5e-1), (line, expected)
      elif ('Cell' in line):
        assert approx_equal(
          values_summary, values_expected, eps=2e-2), (line, expected)
      elif ('Distance' in line):
        assert approx_equal(
          values_summary, values_expected, eps=1e-1), (line, expected)
      elif ('Beam' in line):
        assert approx_equal(
          values_summary, values_expected, eps=2e-2), (line, expected)
      else:
        assert not show_diff(line, expected)

  for data_file in expected_data_files:
    assert os.path.exists(os.path.join('DataFiles', data_file)), data_file

  os.chdir(cwd)


def run_xia2_tolerant(command_line_args, expected_summary, expected_data_files=[]):
  cwd = os.path.abspath(os.curdir)
  tmp_dir = os.path.abspath(open_tmp_directory())
  os.chdir(tmp_dir)

  result = run_process(['xia2'] + command_line_args)

  error_file = os.path.join(tmp_dir, 'xia2.error')
  if os.path.exists(error_file):
    print open(error_file, 'r').read()
    assert False, "xia2.error present after execution"

  assert result['exitcode'] == 0, "xia2 terminated with non-zero exit code"
  assert result['stderr'] == '', "xia2 terminated with output to STDERR"
  summary_file = os.path.join(tmp_dir, 'xia2-summary.dat')
  assert os.path.exists(summary_file), "xia2-summary.dat not present after execution"

  summary_text = open(summary_file, 'rb').read()
  summary_text_lines = summary_text.split('\n')
  expected_summary_lines = expected_summary.split('\n')

  print '-' * 80

  number = re.compile('(\d*\.\d+|\d+\.?)')
  number_with_tolerance = re.compile('(\d*\.\d+|\d+\.?)\((ignore|\*\*|\d*\.\d+%?|\d+\.?%?)\)')
  output_identical = True
  for actual, expected in zip(summary_text_lines, expected_summary_lines):
    if actual == expected:
      print ' ' + actual
      continue

    actual_s = actual.split()
    expected_s = expected.split()
    actual_s = re.split(r'(\s+)', actual)
    expected_s = re.split(r'(\s+)', expected)

    valid = []
    equal = []

    for e, a in zip(expected_s, actual_s):
      if e == '***' or e.strip() == a.strip():
        equal.append(True)
        valid.append(True)
      elif e == '(ignore)':
        equal.append(False)
        valid.append(True)
      elif number_with_tolerance.match(e) and number.match(a):
        expected_value, tolerance = number_with_tolerance.match(e).groups()
        expected_value = float(expected_value)
        if tolerance == '**':
          equal.append(True)
          valid.append(True)
          continue
        if tolerance == 'ignore':
          equal.append(False)
          valid.append(True)
          continue
        if isinstance(tolerance, basestring) and '%' in tolerance: # percentage
          tolerance = expected_value * float(tolerance[:-1]) / 100
        else:
          tolerance = float(tolerance)
        equal.append(False)
        valid.append(abs(expected_value - float(a)) <= tolerance)
      else:
        equal.append(False)
        valid.append(False)

    if all(equal):
      print ' ' + actual
      continue

    expected_line = ''
    actual_line = ''
    for expected, actual, vld, eq in zip(expected_s, actual_s, valid, equal):
      template = '%%-%ds' % max(len(expected), len(actual))
      if eq:
        expected_line += template % expected
        actual_line += template % ''
      elif vld:
        expected_line += template % expected
        actual_line += template % actual
      else:
        expected_line += ' ' + template % expected + ' '
        actual_line += '*' + template % actual + '*'
        output_identical = False
    print '-' + expected_line
    if not all(valid):
      print '>' + actual_line
    else:
      print '+' + actual_line
  print '-' * 80

  for data_file in expected_data_files:
    assert os.path.exists(os.path.join('DataFiles', data_file)), "expected file %s is missing" % data_file

  html_file = os.path.join(tmp_dir, 'xia2.html')
  assert os.path.exists(html_file), "xia2.html not present after execution"

  os.chdir(cwd)
