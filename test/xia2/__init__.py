from __future__ import absolute_import, division, print_function

from six.moves import cStringIO as StringIO
import glob
import os
import re
import sys

from procrunner import run_process

def ccp4_version():
  result = run_process(['refmac5', '-i'], print_stdout=False)
  assert result['exitcode'] == 0 and not result['timeout']
  version = re.search('patch level *([0-9]+)\.([0-9]+)\.([0-9]+)', result['stdout'])
  assert version
  return [int(v) for v in version.groups()]

def xds_version():
  result = run_process(['xds'], print_stdout=False)
  assert result['exitcode'] == 0 and not result['timeout']
  version = re.search('BUILT=([0-9]+)\)', result['stdout'])
  assert version
  return int(version.groups()[0])

def run_xia2_tolerant(test_name, command_line_args, expected_data_files=[]):
  cwd = os.path.abspath(os.curdir)
  tmp_dir = os.path.join(os.curdir, 'xia2_regression.%s' % test_name)
  try:
    os.mkdir(tmp_dir)
  except OSError as exc:
    import errno
    if exc.errno == errno.EEXIST and os.path.isdir(tmp_dir):
      pass
    else:
      raise

  os.chdir(tmp_dir)

  ccp4 = ccp4_version()
  xds = xds_version()
  result = run_process(['xia2'] + command_line_args)

  error_file = 'xia2.error'
  if os.path.exists(error_file):
    print(open(error_file, 'r').read(), file=sys.stderr)
    sys.exit("xia2.error present after execution")

  assert result['stderr'] == '', "xia2 terminated with output to STDERR:\n" + result['stderr']
  assert result['exitcode'] == 0, "xia2 terminated with non-zero exit code (%d)" % result['exitcode']
  summary_file = 'xia2-summary.dat'
  assert os.path.exists(summary_file), "xia2-summary.dat not present after execution"

  summary_text = open(summary_file, 'rb').read()
  summary_text_lines = summary_text.split('\n')
  template_name = 'result.%s.%d.%d.%d.%d' % (test_name, ccp4[0], ccp4[1], ccp4[2], xds)
  template_name = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..')), template_name)
  with open(template_name, 'w') as fh:
    fh.write(generate_tolerant_template(summary_text_lines))

  expected_result_dir = os.path.join(os.path.dirname(__file__), 'expected')
  expected_result_file, expected_result_file_version = None, None
  if os.path.exists(expected_result_dir):
    for f in os.listdir(expected_result_dir):
      if f.startswith('result.%s' % test_name) and os.path.isfile(os.path.join(expected_result_dir, f)):
        candidate_version = re.search("\.([0-9]+)\.([0-9]+)\.([0-9]+)(\.([0-9]+))?$", f)
        if candidate_version:
          candidate_version = [int(v) if v else 0 for v in candidate_version.group(1,2,3,5)]
          major, minor, revision, xdsrev = candidate_version
          cmaj, cmin, crev = ccp4
          xdsv = xds
          # ensure file is not made for a newer CCP4 version
          if cmaj < major: continue
          if cmaj == major and cmin < minor: continue
          if cmaj == major and cmin == minor and crev < revision: continue
          # ensure file is not made for a newer XDS version
          if xdsv < xdsrev: continue
          if expected_result_file is not None and expected_result_file_version is not None:
            cmaj, cmin, crev, xdsv = expected_result_file_version
            # ensure file is for a more recent version than any already found file
            if cmaj > major: continue
            if cmaj == major and cmin > minor: continue
            if cmaj == major and cmin == minor and crev > revision: continue
            if xdsv > xdsrev: continue
          expected_result_file = f
          expected_result_file_version = candidate_version
        elif expected_result_file is None:
          expected_result_file = f
  assert expected_result_file is not None, "Could not find expected results file to compare actual results to"
  with open(os.path.join(expected_result_dir, expected_result_file), 'r') as fh:
    expected_summary_lines = fh.readlines()

  compare = StringIO()
  print('Detected CCP4 version %d.%d.%d' % (ccp4[0], ccp4[1], ccp4[2]), file=compare)
  print('Detected XDS revision %d' % xds, file=compare)
  print('Comparing output against %s' % expected_result_file, file=compare)
  print('-' * 80, file=compare)

  number = re.compile('(-?\d*\.\d+|-?\d+\.?)')
  number_with_tolerance = re.compile('(-?\d*\.\d+|-?\d+\.?)\((ignore|\*\*|\d*\.\d+%?|\d+\.?%?)\)')
  output_identical = True
  for actual, expected in zip(summary_text_lines, expected_summary_lines):
    if actual == expected:
      print(' ' + actual, file=compare)
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
        if number.match(e).groups()[0] == a:
          # identical value, but missing brackets
          equal.append(True)
          valid.append(True)
          continue
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
      print(' ' + actual, file=compare)
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
    print('-' + expected_line, file=compare)
    if not all(valid):
      print('>' + actual_line, file=compare)
    else:
      print('+' + actual_line, file=compare)
  print('-' * 80, file=compare)

  for data_file in expected_data_files:
    if not os.path.exists(os.path.join('DataFiles', data_file)):
      print("> expected file %s is missing" % data_file, file=compare)
      output_identical = False

  html_file = 'xia2.html'
  if not os.path.exists(html_file):
    print("> xia2.html not present after execution", file=compare)
    output_identical = False

  os.chdir(cwd)
  if not output_identical:
    sys.stderr.write(compare.getvalue())
    sys.exit("xia2 output failing tolerance checks")
  sys.stdout.write(compare.getvalue())

def generate_tolerant_template(lines):
  tolerances = {
    'Distance': [ '', '0.1' ],
    'High resolution limit': [ '5%', '10%', '**', '0.02' ],
    'Low resolution limit': [ '5%', '**', '**', '0.03' ],
    'Completeness': [ '5%', '5%', '10', '5%' ],
    'Multiplicity': [ '0.2', '0.2', '0.2', '0.2' ],
    'I/sigma': [ '15%', '**', '0.3', '0.3' ],
    'Rmerge(I+/-)': [ '10%', '10%', '15%', '10%' ],
    'CC half': [ '2%', '0.2', '0.2', '0.2' ],
    'Anomalous completeness': [ '2%', '5%', '10', '2%' ],
    'Anomalous multiplicity': [ '0.5', '0.5', '0.5', '0.5' ],
    'Cell:': [ '0.5%', '0.5%', '0.5%',
        lambda x:'0.5%' if x != '90.000' and x != '120.000' else '',
        lambda x:'0.5%' if x != '90.000' and x != '120.000' else '',
        lambda x:'0.5%' if x != '90.000' and x != '120.000' else '']
  }
  number = re.compile('(\d*\.\d+|\d+\.?)')
  f = []
  for l in lines:
    if l.startswith('Files '): l = 'Files ***'
    items = re.split(r'(\s+)', l)
    number_positions = [ pos for pos, item in enumerate(items) if number.match(item) ]
    if number_positions and number_positions[0] > 0:
      prefix = ''.join(items[0:number_positions[0]]).strip()
      if prefix in tolerances:
        for num, pos in enumerate(number_positions):
          tolerance = tolerances[prefix][num]
          if callable(tolerance): tolerance = tolerance(items[pos])
          if tolerance != '': tolerance = '(%s)' % tolerance
          items[pos] += tolerance
        l = ''.join(items)
    f.append(l)
  return "\n".join(f)
