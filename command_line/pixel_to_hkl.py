#!/usr/bin/env libtbx.python
#
# xia2_regression.pixel_to_hkl.py
#
#  Copyright (C) 2016 Diamond Light Source
#
#  Author: Graeme Winter
#
#  This code is distributed under the BSD license, a copy of which is
#  included in the root directory of this package.
#
# Jiffy application: given experiments.json compute HKL for pixel

from __future__ import division
from libtbx.phil import parse

help_message = '''

xia2_regression.pixel_to_hkl experiment.json

'''

phil_scope = parse('''
pixel_fast_slow = None
  .type = ints(size=2)
  .help = 'Fast, slow coordinates of pixel'
  .multiple = true
''', process_includes=True)

class Script(object):
  '''A class for running the script.'''

  def __init__(self):
    from dials.util.options import OptionParser
    import libtbx.load_env

    usage = 'usage: %s [options] experiments.json' \
            % libtbx.env.dispatcher_name

    self.parser = OptionParser(
      usage=usage,
      phil=phil_scope,
      epilog=help_message,
      check_format=False,
      read_experiments=True)

  def run(self):
    from dials.util.command_line import Command
    from dials.array_family import flex
    from scitbx import matrix
    from dials.util.options import flatten_experiments
    import math

    params, options = self.parser.parse_args(show_diff_phil=True)

    self.params = params

    experiments = flatten_experiments(params.input.experiments)
    if len(experiments) != 1:
      self.parser.print_help()
      return

    # now perform some calculations - the only things different from one
    # experiment to the next will be crystal models
    crystal = experiments[0].crystal
    detector = experiments[0].detector
    beam = experiments[0].beam
    imageset = experiments[0].imageset

    # derived quantities
    wavelength = beam.get_wavelength()
    s0 = matrix.col(beam.get_s0())

    # this should be working only on single images at the moment
    if hasattr(imageset, "get_array_range"):
      assert imageset.get_array_range()[1] - imageset.get_array_range()[0] == 1

    # in here do some jiggery-pokery to cope with this being interpreted as
    # a rotation image in here i.e. if scan is not None; derive goniometer
    # matrix else set this to identity

    scan = experiments[0].scan
    goniometer = experiments[0].goniometer

    if scan and goniometer:
      angle = scan.get_angle_from_array_index(
        0.5 * sum(imageset.get_array_range()))
      axis = matrix.col(goniometer.get_rotation_axis_datum())
      F = matrix.sqr(goniometer.get_fixed_rotation())
      S = matrix.sqr(goniometer.get_setting_rotation())
      R = S * axis.axis_and_angle_as_r3_rotation_matrix(angle, deg=True) * F
    else:
      R = matrix.sqr((1, 0, 0, 0, 1, 0, 0, 0, 1))

    # need to decide how to handle multiple panels... #TODO
    assert(len(detector) == 1)

    panel = detector[0]

    RUBi = (R * matrix.sqr(crystal.get_A())).inverse()


    for pixel in params.pixel_fast_slow:
      pixel = (pixel[0] + 0.5, pixel[1] + 0.5)
      p = matrix.col(panel.get_pixel_lab_coord(pixel))
      q = p.normalize() / wavelength - s0
      hkl = RUBi * q
      print '%d %d' % pixel, '=> %.3f %.3f %.3f' % hkl.elems


if __name__ == '__main__':
  from dials.util import halraiser
  try:
    script = Script()
    script.run()
  except Exception as e:
    halraiser(e)
