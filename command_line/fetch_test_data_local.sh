#!/bin/bash
set -e

echo =======================================================================
echo
echo This program fetches the xia2 example data from a local diamond machine
echo If you are not connected to the Diamond network this will fail.
echo In this case you should run   xia2_regression.fetch_test_data   instead
echo
echo =======================================================================
echo

rsync -rv g18-sc-serv-03:/scratch/jenkins_slave/workspace/dials_distribute_push/xia2_regression_data/ $(libtbx.show_build_path)/xia2_regression

echo
echo Done.
echo

# Offer to install dials_regression only if dials is present and dials_regression is missing.
libtbx.find_in_repositories dials >/dev/null 2>/dev/null || exit 0
libtbx.find_in_repositories dials_regression >/dev/null 2>/dev/null || {
  echo =======================================================================
  echo
  echo Do you want to kick-start the dials_regression repository as well?
  echo If you have already downloaded d_r this may overwrite any changes!
  echo

  read -r -p "Copy dials_regression? [y/N] " response
  echo
  echo =======================================================================
  if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
  then
    rsync -rv g18-sc-serv-03:/scratch/jenkins_slave/workspace/dials_distribute_push/dials_regression $(libtbx.find_in_repositories dials)/.. && libtbx.configure dials_regression
  fi
}

echo
echo Done.
echo
