#!/usr/bin/env python

def download(url, target):
  '''Download a url to a target file, including path relative to cwd,
  making directory if necessary, throw exception if target file already
  present.'''

  import os
  import urllib2

  if os.path.exists(target):
    raise RuntimeError, 'file %s exists' % target

  dirname, filename = os.path.split(target)

  if dirname:
    if not os.path.exists(dirname):
      os.makedirs(dirname)

  open(target, 'wb').write(urllib2.urlopen(url).read())

  return

def test():
  url = 'http://dials.diamond.ac.uk/xia2/test_data/filelist.dat'

  import tempfile
  import os
  import shutil

  tempdir = tempfile.mkdtemp('xia2')

  download(url, os.path.join(tempdir, 'filelist.dat'))

  for record in open(os.path.join(tempdir, 'filelist.dat')):
    print record.strip()

  print 'OK'

  shutil.rmtree(tempdir)

if __name__ == '__main__':
  test()
