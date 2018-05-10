from __future__ import absolute_import, division, print_function

import multiprocessing

from xia2_regression.util.download import download

files_to_download = {
  'http://www.ccp4.ac.uk/tutorials/tutorial_files/blend_tutorial/data02.tgz':
    'blend_tutorial/data02.tgz',
}

def fetch_test_data_index():
  index_url = 'http://dials.diamond.ac.uk/xia2/test_data/filelist.dat'

  result = download(index_url, 'filelist.dat')
  if result == -1:
    raise RuntimeError, 'Could not download file list.'

  index = {}
  for record in open('filelist.dat'):
    filename = record.strip()
    url = 'http://dials.diamond.ac.uk/xia2/' + filename
    index[url] = filename
  return index

def fetch_test_data(target_dir = '', skip_existing_files=True):
  import os

  if (target_dir == ''):
    import libtbx.load_env
    target_dir = libtbx.env.under_build('xia2_regression')

  if not os.path.exists(target_dir):
    os.mkdir(target_dir)
  os.chdir(target_dir)

  success = True

  download_list = fetch_test_data_index()
  download_list.update(files_to_download)

  download_count = len(download_list)
  progress_mask = " [%%%dd / %%d] " % len(str(download_count))

  urls = sorted(download_list)
  pool = multiprocessing.Pool(3) # number of parallel downloads
  results = []

  for num in range(0, download_count):
    url = urls[num]
    filename = download_list[url]

    status_prefix = progress_mask % (num + 1, download_count)
    if skip_existing_files and os.path.exists(filename):
      print(status_prefix, "skipping", url, ": file exists")
    else:
      results.append(pool.apply_async(download, (url, filename, status_prefix)))

  success = True
  for result in results:
    if result.get(timeout=600) == -1:
      success = False
  if not success:
    raise RuntimeError, 'some downloads failed, please try again.'
