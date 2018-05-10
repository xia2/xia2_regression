from __future__ import absolute_import, division, print_function

import sys

if __name__ == '__main__':
  from xia2_regression.util.fetch_test_data import fetch_test_data

  help_message = '''

This program is used to fetch xia2 example data from:

http://dials.diamond.ac.uk/xia2/test_data

to xia2_regression - if the data are already there will not download again.

'''

  if len(sys.argv) < 2:
    fetch_test_data()
  else:
    print "Downloading into directory %s" % sys.argv[1]
    fetch_test_data(sys.argv[1])
