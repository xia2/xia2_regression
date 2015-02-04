def fetch_test_data_index():
  from download import download

  index_url = 'http://dials.diamond.ac.uk/xia2/test_data/filelist.dat'
  download(index_url, 'filelist.dat')
  return 'filelist.dat'

files_to_download = {
  'http://www.ccp4.ac.uk/tutorials/tutorial_files/blend_tutorial/data02.tgz':
  'blend_tutorial/data02.tgz',
}

def fetch_test_data(target_dir = ''):
  import os
  from download import download

  if (target_dir == ''):
    import libtbx.load_env
    target_dir = libtbx.env.under_build('xia2_regression')

  if not os.path.exists(target_dir):
    os.mkdir(target_dir)
  os.chdir(target_dir)

  index = fetch_test_data_index()

  try:
    for record in open(index):
      filename = record.strip()
      url = 'http://dials.diamond.ac.uk/xia2/' + filename
      if not os.path.exists(filename):
        print filename
        download(url, filename)
      else:
        size = os.stat(filename).st_size
        if size == 0:
          print '%s exists, but empty, downloading' % filename
          download(url, filename, error_if_exists=False)
        else:
          print '%s exists' % filename

  finally:
    os.remove(index)

  for url, filename in files_to_download.iteritems():
    if not os.path.exists(filename):
      os.makedirs(os.path.split(filename)[0])
      download(url, filename)
      size = os.stat(filename).st_size
      if size == 0:
        print '%s exists, but empty, downloading' % filename
        download(url, filename, error_if_exists=False)
      else:
        print '%s exists' % filename

  return

if __name__ == '__main__':
  import os
  cwd = os.path.split(os.getcwd())[-1]
  if cwd != 'xia2_regression':
    raise RuntimeError, 'only run this from xia2_regression'
  fetch_test_data()

