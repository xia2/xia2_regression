#!/usr/bin/env python

from libtbx.auto_build.bootstrap import Downloader
import os
import urllib2

def download(url, target):
  '''Download a url to a target file, including path relative to cwd,
  making directory if necessary. Returns the file size.
  Returns -1 if the downloaded file size does not match the expected file size.
  Returns -2 if the download is skipped due to the file at the URL not
  being newer than the local copy (with matching file sizes).'''

  dirname, filename = os.path.split(target)
  if dirname:
    if not os.path.exists(dirname):
      os.makedirs(dirname)

  print "downloading", url, ": ",
  result = None
  retries = 3
  while (result is None) and (retries >= 0):
    try:
      result = Downloader().download_to_file(url, target)
    except urllib2.HTTPError, e:
      print e
      retries = retries - 1
      if retries >= 0:
        sleep = [15,10,5][retries]
        print "\nRetrying in %d seconds..." % sleep
        time.sleep(sleep)
      else:
        print "\nGiving up.\n"
        raise
  return result

def test():
  url = 'http://dials.diamond.ac.uk/xia2/test_data/filelist.dat'

  import tempfile
  import shutil

  tempdir = tempfile.mkdtemp('xia2')

  download(url, os.path.join(tempdir, 'filelist.dat'))

  for record in open(os.path.join(tempdir, 'filelist.dat')):
    print record.strip()

  print 'OK'

  shutil.rmtree(tempdir)

if __name__ == '__main__':
  test()
