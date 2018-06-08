from __future__ import absolute_import, division, print_function

import sys

if __name__ == '__main__':
  from xia2_regression.util.fetch_test_data import fetch_test_data

  help_message = '''
Usage: xia2_regression.fetch_test_data [-h | --help] [destination]

Where:
  -h, --help      Show this message
  [destination]   Target directory for files, created if not present.
                  Defaults to <build>/xia2_regression.

This program is used to fetch xia2 example data from:

  http://dials.diamond.ac.uk/xia2/test_data

to xia2_regression - if the data are already there will not download again.
'''.strip()

  if "--help" in sys.argv or "-h" in sys.argv:
    print(help_message)
  elif len(sys.argv) < 2:
    fetch_test_data()
  else:
    print("Downloading into directory %s" % sys.argv[1])
    fetch_test_data(sys.argv[1])
