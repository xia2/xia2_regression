from download import download

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
  download_num = 0
  progress_mask = " [%%%dd / %%d] " % len(str(download_count))

  for url in sorted(download_list):
    download_num = download_num + 1
    filename = download_list[url]

    print progress_mask % (download_num, download_count),
    if skip_existing_files and os.path.exists(filename):
      print "skipping", url, ": file exists"
    else:
      result = download(url, filename)
      if result == -1:
        success = False

  if not success:
    raise RuntimeError, 'some downloads failed, please try again.'

  return

if __name__ == '__main__':
  import os
  cwd = os.path.split(os.getcwd())[-1]
  if cwd != 'xia2_regression':
    raise RuntimeError, 'only run this from xia2_regression'
  fetch_test_data()

