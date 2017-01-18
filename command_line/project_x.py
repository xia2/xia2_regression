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
r = 0.1
  .type = float
  .help = 'Effective radius of relp'
d_min = 0.0
  .type = float
  .help = 'Highest resolution for calculation'
oversample = 1
  .type = int
  .help = 'Oversample rate'
png = 'project_x.png'
  .type = str
  .help = 'Output name for .png'
png_width = 8
  .type = float
  .help = 'Width, inches'
png_height = 6
  .type = float
  .help = 'Height, inches'
png_dpi = 200
  .type = int
  .help = 'Pixels per inch'
''', process_includes=True)

from scitbx import simplex
from scitbx.array_family import flex
import random

def generate_start(values, offset):
  assert len(values) == len(offset)
  start = [values]
  for j, o in enumerate(offset):
    next = values.deep_copy()
    next[j] += o
    start.append(next)
  return start

class simple_simplex(object):
  def __init__(self, values, offset, evaluator):
    self.evaluator = evaluator
    self.n = len(values)
    self.x = values
    self.starting_simplex = generate_start(values, offset)
    self.fcount = 0

    optimizer = simplex.simplex_opt(dimension=self.n,
                                    matrix=self.starting_simplex,
                                    evaluator=self,
                                    tolerance=1e-10,
                                    max_iter=1000000)

    self.x = optimizer.get_solution()
    return self.x

  def target(self, vector):
    return self.evaluator.evaluate(vector)

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
    params = self.params
    data = map.as_numpy_array()
    fig = pyplot.gcf()
    fig.set_size_inches(params.png_width, params.png_height)
    pyplot.imshow(data, cmap='gray_r')
    pyplot.savefig(filename, dpi=params.png_dpi)
    return

  def evaluate(self, vector):
    # compute and score vector of params (order == [metrical matrix params],
    # [orientation params], r; return 1.0/cc
    xmap = self.compute_xmap(vector)
    cc, n = self.score(self.pixels, xmap)
    return 1.0 / abs(cc)

  def compute_xmap(self, vector):
    cell_parms = self.cucp.get_param_vals()
    orientation_parms = self.cop.get_param_vals()
    assert len(vector) == len(cell_parms) + len(orientation_parms) + 1
    tst_cell = vector[:len(cell_parms)]
    tst_orientation = vector[len(cell_parms):len(cell_parms) +
                             len(orientation_parms)]
    tst_r = vector[-1]

    self.cucp.set_param_vals(tst_cell)
    self.cop.set_param_vals(tst_orientation)

    from scitbx import matrix
    from xia2_regression import x_map

    print '%.3f %.3f %.3f %.3f %.3f %.3f' % \
      tuple(self.crystal.get_unit_cell().parameters()),
    print '%.3f %.3f %.3f' % tuple(tst_orientation), '%.3f' % tst_r

    RUBi = (self.R * matrix.sqr(self.crystal.get_A())).inverse()
    distance_map = x_map(self.panel, self.beam, RUBi, self.params.oversample,
                         tst_r, self.params.d_min)

    return distance_map

  def score(self, idata, distance_map):
    from scitbx.array_family import flex
    nslow, nfast = idata.focus()

    # try to find points on here > 1% (for arguments sake)
    binary_map = distance_map.deep_copy()
    binary_map.as_1d().set_selected(binary_map.as_1d() > 0.01, 1)
    binary_map = binary_map.iround()
    binary_map.reshape(flex.grid(1, nslow, nfast))

    # find connected regions of spots - hacking code for density modification
    from cctbx import masks
    from cctbx import uctbx
    uc = uctbx.unit_cell((1, nslow, nfast, 90, 90, 90))
    flood_fill = masks.flood_fill(binary_map, uc)
    binary_map = binary_map.as_1d()

    data = idata.as_double().as_1d()

    mean_cc = 0.0

    for j in range(flood_fill.n_voids()):
      sel = binary_map == (j + 2)

      # select pixels for this void; if any are -ve i.e. bad pixels
      # exclude from calculation

      d = data.select(sel)
      if flex.min(d) < 0:
        continue

      m = distance_map.as_1d().select(sel)
      mean_cc += flex.linear_correlation(d, m).coefficient()


    print 'Score: %.3f' % (1.0 / (mean_cc / flood_fill.n_voids()))

    return mean_cc / flood_fill.n_voids(), flood_fill.n_voids()

  def run(self):
    from dials.util.command_line import Command
    from dials.array_family import flex
    from scitbx import matrix
    from dials.util.options import flatten_experiments
    import math

    params, options = self.parser.parse_args(show_diff_phil=True)

    self.params = params

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
    if hasattr(imageset, "get_array_range"):
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

    self.R = R

    # need to decide how to handle multiple plots...
    assert(len(detector) == 1)

    panel = detector[0]
    pixels = data[0]

    self.panel = panel
    self.pixels = pixels
    self.beam = beam

    assert len(crystals) == 1
    crystal = crystals[0]

    # play with symmetry stuff - yay for short class names
    from dials.algorithms.refinement.parameterisation.crystal_parameters \
      import CrystalUnitCellParameterisation, \
      CrystalOrientationParameterisation

    self.crystal = crystal
    self.cucp = CrystalUnitCellParameterisation(crystal)
    self.cop = CrystalOrientationParameterisation(crystal)

    # 0-point and deltas
    values = flex.double(self.cucp.get_param_vals() +
                         self.cop.get_param_vals() + [params.r])
    offset = flex.double([0.01 * v for v in self.cucp.get_param_vals()] +
                         [0.1, 0.1, 0.1, 0.01])

    # create simplex
    refined_values = simple_simplex(values, offset, self)

    # use results
    distance_map = self.compute_xmap(refined_values)

    score, n_objects = self.score(pixels, distance_map)

    print 'Score was: %.3f over %d objects' % (score, n_objects)

    # plot output
    self.plot_map(distance_map, params.png)

if __name__ == '__main__':
  from dials.util import halraiser
  try:
    script = Script()
    script.run()
  except Exception as e:
    halraiser(e)
