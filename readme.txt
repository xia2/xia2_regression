This repository has now been superseded.

All tests can be found in the xia2 repository, and to run the regression
tests use the --regression flag on pytest, eg.

  pytest --regression

To explicitly download the test files run

  dials.fetch_test_data



original repository readme.txt:
-------------------------------


Regression tests for xia2 - files small enough to keep in subversion. Larger
files will be uploaded to

http://dials.diamond.ac.uk/xia2/test_data/

and pulled off the network to execute tests.

Beware (i) this may take some time and (ii) quite a lot of data may end up in
the build folder.
