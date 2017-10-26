#
# See https://github.com/dials/dials/wiki/pytest for documentation on how to
# write and run pytest tests, and an overview of the available features.
#

from __future__ import absolute_import, division, print_function

import pytest
from dials.conftest import (dials_regression, xia2_regression,
                            xia2_regression_build)
from libtbx.test_utils.pytest import libtbx_collector

pytest_collect_file = libtbx_collector()
