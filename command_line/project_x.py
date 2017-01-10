#!/usr/bin/env libtbx.python
#
# xia2_regression.project_x.py
#
#  Copyright (C) 2016 Diamond Light Source
#
#  Author: Graeme Winter
#
#  This code is distributed under the BSD license, a copy of which is
#  included in the root directory of this package.
#
# Exploring some ideas with synchrotron still images, work in progress, your
# mileage will vary, if this kills your kitten then I hold no responsibility
# etc. ad nauseum.

from __future__ import division
from libtbx.phil import parse

help_message = '''

dials_regression.project_x experiment.json

'''

phil_scope = parse('''
r = 0.05
  .type = float
  .help = 'Effective radius of relp'
png = 'project_x.png'
  .type = str
  .help = 'Output name for .png'
''', process_includes=True)

def nint(a):
  return int(round(a))

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
      check_format=True,
      read_experiments=True)

  def plot_map(self, map, filename):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot
    data = map.as_numpy_array()
    pyplot.imshow(data)
    pyplot.savefig(filename)
    return

  def run(self):
    from dials.util.command_line import Command
    from dials.array_family import flex
    from scitbx import matrix
    from dials.util.options import flatten_experiments
    import math

    params, options = self.parser.parse_args(show_diff_phil=True)

    experiments = flatten_experiments(params.input.experiments)

    if len(experiments) == 0:
      self.parser.print_help()
      return

    # verify that these experiments correspond to exactly one imageset, one
    # detector, one beam (obviously)
    for experiment in experiments[1:]:
      assert experiment.imageset == experiments[0].imageset
      assert experiment.beam == experiments[0].beam
      assert experiment.detector == experiments[0].detector

    # now perform some calculations - the only things different from one
    # experiment to the next will be crystal models
    crystals = [experiment.crystal for experiment in experiments]
    detector = experiments[0].detector
    beam = experiments[0].beam
    imageset = experiments[0].imageset

    # derived quantities
    wavelength = beam.get_wavelength()
    s0 = matrix.col(beam.get_s0())

    # this should be working only on single images at the moment
    assert imageset.get_array_range()[1] - imageset.get_array_range()[0] == 1

    # really slow code follows - (i) move this to C++ and (ii) work out a
    # way to not loop over all pixels doing relatively expensive calculations
    # for every pixel and (iii) work out a neater way of looping over the
    # panels and dealing with the mm to pixel mapping

    data = imageset.get_raw_data(0)

    assert len(data) == len(detector)

    # in here do some jiggery-pokery to cope with this being interpreted as
    # a rotation image in here i.e. if scan is not None; derive goniometer
    # matrix else set this to identity

    scan = experiments[0].scan
    goniometer = experiments[0].goniometer

    if scan and goniometer:
      # FIXME check the logic here that everthing is correct - R, F, S etc.
      angle = scan.get_angle_from_array_index(
        0.5 * sum(imageset.get_array_range()))
      axis = matrix.col(goniometer.get_rotation_axis_datum())
      F = matrix.sqr(goniometer.get_fixed_rotation())
      S = matrix.sqr(goniometer.get_setting_rotation())
      R = S * axis.axis_and_angle_as_r3_rotation_matrix(angle, deg=True) * F
    else:
      R = matrix.sqr((1, 0, 0, 0, 1, 0, 0, 0, 1))

    # need to decide how to handle multiple plots...
    assert(len(detector) == 1)

    distance_map = flex.double(flex.grid(data[0].focus()))

    RUBinvs = [ (R * matrix.sqr(crystal.get_A())).inverse() for crystal in crystals ]

    for panel, pixels in zip(detector, data):
      origin = panel.get_origin()
      fast = panel.get_fast_axis()
      slow = panel.get_slow_axis()
      nfast, nslow = panel.get_image_size()

      for j in range(nslow):
        print j
        for i in range(nfast):

          # this is indexing into the array so works in slow, fast frame
          pixel = pixels[(j,i)]

          # this function works in the fast, slow coordinate frame
          x = matrix.col(panel.get_pixel_lab_coord((i,j))).normalize()
          q = x * (1.0 / wavelength) - s0

          # this code is *so slow* it will make your eyes swirl
          _d = 1
          for RUBinv in RUBinvs:
            rhkl = RUBinv * q
            hkl = map(nint, rhkl.elems)
            d = (matrix.col(hkl) - rhkl).length()
            if d < _d: _d = d
          # score as a Gaussian with weight defined as params.r
          distance_map[(j,i)] = math.exp(-(_d / params.r) ** 2)

    # plot output
    self.plot_map(distance_map, params.png)

if __name__ == '__main__':
  from dials.util import halraiser
  try:
    script = Script()
    script.run()
  except Exception as e:
    halraiser(e)
