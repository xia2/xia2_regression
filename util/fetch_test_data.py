def fetch_test_data_index():
  from download import download

  index_url = 'http://dials.diamond.ac.uk/xia2/test_data/filelist.dat'
  download(index_url, 'filelist.dat')
  return 'filelist.dat'

def fetch_test_data():
  import os
  import libtbx.load_env
  from download import download

  xia2_regression = libtbx.env.dist_path('xia2_regression')
  os.chdir(xia2_regression)
  
  index = fetch_test_data_index()
  
  for record in open(index):
    filename = record.strip()
    url = 'http://dials.diamond.ac.uk/xia2/' + filename
    if not os.path.exists(filename):
      print filename
      download(url, filename)
    else:
      print '%s exists' % filename

  os.remove(index)

  return

if __name__ == '__main__':
  import os
  cwd = os.path.split(os.getcwd())[-1]
  if cwd != 'xia2_regression':
    raise RuntimeError, 'only run this from xia2_regression'
  fetch_test_data()

