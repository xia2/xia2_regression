#!/usr/bin/env python

from __future__ import print_function
import os
import shutil
import sys
import time
import urllib2

# Download URL to local file
# copied from bootstrap script
class Downloader(object):
  def download_to_file(self, url, file, log=sys.stdout, status=True):
    """Downloads a URL to file. Returns the file size.
       Returns -1 if the downloaded file size does not match the expected file
       size
       Returns -2 if the download is skipped due to the file at the URL not
       being newer than the local copy (with matching file sizes).
    """

    socket = urllib2.urlopen(url)

    file_size = int(socket.info().getheader('Content-Length'))
    # There is no guarantee that the content-length header is set

    remote_mtime = 0
    try:
      remote_mtime = time.mktime(socket.info().getdate('last-modified'))
    except:
      pass

    if (file_size > 0):
      if (remote_mtime > 0):
        # check if existing file matches remote size and timestamp
        try:
          (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
          if (size == file_size) and (remote_mtime == mtime):
            log.write("local copy is current\n")
            socket.close()
            return -2
        except:
          # proceed with download if timestamp/size check fails for any reason
          pass

      hr_size = (file_size, "B")
      if (hr_size[0] > 500): hr_size = (hr_size[0] / 1024, "kB")
      if (hr_size[0] > 500): hr_size = (hr_size[0] / 1024, "MB")
      log.write("%.1f %s\n" % hr_size)
      if status:
        log.write("    [0%")
        log.flush()

    received = 0
    block_size = 8192
    progress = 1
    # Allow for writing the file immediately so we can empty the buffer
    tmpfile = file + '.tmp'

    f = open(tmpfile, 'wb')
    while 1:
      block = socket.read(block_size)
      received += len(block)
      f.write(block)
      if status and (file_size > 0):
        while (100 * received / file_size) > progress:
          progress += 1
          if (progress % 20) == 0:
            log.write("%d%%" % progress)
          elif (progress % 2) == 0:
            log.write(".")
          log.flush()

      if not block: break
    f.close()
    socket.close()

    if status and (file_size > 0):
      log.write("]\n")
      log.flush()

    # Do not overwrite file during the download. If a download temporarily fails we
    # may still have a clean, working (yet older) copy of the file.
    shutil.move(tmpfile, file)

    if (file_size > 0) and (file_size != received):
      return -1

    if remote_mtime > 0:
      # set file timestamp if timestamp information is available
      from stat import ST_ATIME
      st = os.stat(file)
      atime = st[ST_ATIME] # current access time
      os.utime(file,(atime,remote_mtime))

    return received


def download(url, target, status_prefix=''):
  '''Download a url to a target file, including path relative to cwd,
  making directory if necessary. Returns the file size or return code.'''

  dirname, filename = os.path.split(target)
  if dirname:
    try:
      os.makedirs(dirname)
    except:
      pass

  print(status_prefix, "downloading", url, ": ", end=' ')
  result = None
  retries = 3
  while (result is None) and (retries >= 0):
    try:
      result = Downloader().download_to_file(url, target, status=False)
    except urllib2.HTTPError as e:
      print(e)
      retries = retries - 1
      if retries >= 0:
        sleep = [15,10,5][retries]
        print("\nRetrying in %d seconds..." % sleep)
        time.sleep(sleep)
      else:
        print("\nGiving up.\n")
        raise
  return result

def test():
  url = 'http://dials.diamond.ac.uk/xia2/test_data/filelist.dat'

  import tempfile
  import shutil

  tempdir = tempfile.mkdtemp('xia2')

  download(url, os.path.join(tempdir, 'filelist.dat'))

  for record in open(os.path.join(tempdir, 'filelist.dat')):
    print(record.strip())

  print('OK')

  shutil.rmtree(tempdir)

if __name__ == '__main__':
  test()
