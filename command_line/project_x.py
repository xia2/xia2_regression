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
from __future__ import print_function

import random

from libtbx.phil import parse
from scitbx import simplex
from scitbx.array_family import flex

help_message = '''

dials_regression.project_x experiment.json indexed.pickle

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
max_iter = 200
  .type = int(value_min=0)
  .help = 'Max # simplex iterations'
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
padding = 0
  .type = int(value_min=0)
  .help = 'Add padding around shoebox'
score = *indexed image
  .type = choice
unit_cell = None
  .type = floats(size=6)
  .help = 'Unit cell input'
phis = None
  .type = floats(size=3)
  .help = 'Input phi 1, 2, 3'
''', process_includes=True)


def generate_start(values, offset):
  assert len(values) == len(offset)
  start = [values]
  for j, o in enumerate(offset):
    next = values.deep_copy()
    next[j] += o
    start.append(next)
  return start

class simple_simplex(object):
  def __init__(self, values, offset, evaluator, max_iter):
    self.evaluator = evaluator
    self.n = len(values)
    self.x = values
    self.starting_simplex = generate_start(values, offset)
    self.fcount = 0

    optimizer = simplex.simplex_opt(dimension=self.n,
                                    matrix=self.starting_simplex,
                                    evaluator=self,
                                    tolerance=1e-10,
                                    max_iter=max_iter)

    self.x = optimizer.get_solution()
    return

  def get_solution(self):
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
      read_experiments=True,
      read_reflections=True)

    self.evaluations = 0

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
    self.evaluations += 1
    print('Cycle %d' % self.evaluations)
    xmap = self.compute_xmap(vector)
    if self.params.score == 'image':
      cc, n = self.score(self.pixels, xmap)
    else:
      cc, n = self.score_indexed(self.pixels, self.reflections, xmap)
    return 1.0 / max(cc, 0.01)

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

    print('Cell: %.3f %.3f %.3f %.3f %.3f %.3f' % \
      tuple(self.crystal.get_unit_cell().parameters()))
    print('Phi(1,2,3): %.3f %.3f %.3f' % tuple(tst_orientation), \
      'R: %.3f' % tst_r)

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

    if flood_fill.n_voids() > 1:
      print('Score: %.3f' % (1.0 / (mean_cc / flood_fill.n_voids())))
      return mean_cc / flood_fill.n_voids(), flood_fill.n_voids()
    else:
      print('Scoring failed')
      return 0.01, 1

  def score_indexed(self, idata, reflections, distance_map):
    from scitbx.array_family import flex

    data = idata.as_double()

    mean_cc = 0.0

    for reflection in reflections:
      x0, x1, y0, y1, z0, z1 = reflection['bbox']
      d = data[y0:y1,x0:x1].as_1d()

      if flex.min(d) < 0:
        continue

      m = distance_map[y0:y1,x0:x1].as_1d()

      mean_cc += flex.linear_correlation(d, m).coefficient()

    cc = mean_cc / len(reflections)
    print('Score: %.3f (CC=%.3f)' % (1.0 / cc, cc))
    return cc, len(reflections)

  def integrate(self, idata, distance_map):
    from scitbx.array_family import flex
    from scitbx import matrix
    nslow, nfast = idata.focus()

    # try to find points on here > 1% (for arguments sake)
    # TODO make this a PHIL parameter
    binary_map = distance_map.deep_copy()
    binary_map.as_1d().set_selected(binary_map.as_1d() > 0.01, 1)
    binary_map = binary_map.iround()
    binary_map.reshape(flex.grid(1, nslow, nfast))

    # find connected regions of spots - hacking code for density modification
    # this is used to determine the integration masks for the reflections i.e.
    # those pixels above 1% of the theoretical peak height
    from cctbx import masks
    from cctbx import uctbx
    uc = uctbx.unit_cell((1, nslow, nfast, 90, 90, 90))
    flood_fill = masks.flood_fill(binary_map, uc)
    binary_map = binary_map.as_1d()

    data = idata.as_double()

    coms = flood_fill.centres_of_mass()

    RUBi = (self.R * matrix.sqr(self.crystal.get_A())).inverse()

    winv = 1 / self.beam.get_wavelength()

    # TODO make a reflection table here & populate with all of the things
    # I am interested in for scaling i.e. HKL, I, sigI, Ibg, sigIbg,
    # scale factor, xy coordinate on the detector, ... make an
    # integrated pickle with this information for export to MTZ later...

    for j in range(flood_fill.n_voids()):
      xy = coms[j][2], coms[j][1]
      p = matrix.col(self.panel.get_pixel_lab_coord(xy)).normalize() * winv
      q = p - matrix.col(self.beam.get_s0())
      hkl = RUBi * q
      ihkl = [int(round(h)) for h in hkl]
      sel = binary_map == (j + 2)

      # select pixels for this void; if any are -ve i.e. bad pixels
      # exclude from calculation

      d = data.select(sel)
      if flex.min(d) < 0:
        continue

      # here compute the Miller index for this reflection centre
      # TODO figure out how to implement the background estimation -
      # will need to find pixels in region around this object which are
      # not in an object, determine the mean local background and
      # variance in this, then apply it to the pixels occupied by
      # the masks here...

      m = distance_map.select(sel)

      scale = flex.sum(m)
      intensity = flex.sum(d)
      background = 0

      print('%4d %4d %4d' % tuple(ihkl), '%8.4f %8.4f %8.4f' % \
        (intensity, scale, background))

  def run(self):
    from dials.util.command_line import Command
    from dials.array_family import flex
    from scitbx import matrix
    from dials.util.options import flatten_experiments
    from dials.util.options import flatten_reflections
    import math

    params, options = self.parser.parse_args(show_diff_phil=True)

    self.params = params

    experiments = flatten_experiments(params.input.experiments)
    reflections = flatten_reflections(params.input.reflections)

    if len(experiments) == 0:
      self.parser.print_help()
      return

    if len(reflections) != 1:
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

    data = imageset.get_raw_data(0)

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

    reflections = reflections[0]

    print('Read %d reflections' % len(reflections))

    indexed = reflections.select(reflections.get_flags(
      reflections.flags.indexed))

    print('Kept %d indexed reflections' % len(indexed))

    # optionally apply padding - will not use pixel data anyway
    if params.padding > 0:
      x0, x1, y0, y1, z0, z1 = indexed['bbox'].parts()
      x0 -= params.padding
      x1 += params.padding
      y0 -= params.padding
      y1 += params.padding
      panel = indexed['panel']
      for i in range(len(indexed)):
        width, height = detector[panel[i]].get_image_size()
        if x0[i] < 0: x0[i] = 0
        if x1[i] > width: x1[i] = width
        if y0[i] < 0: y0[i] = 0
        if y1[i] > height: y1[i] = height

      indexed['bbox'] = flex.int6(x0, x1, y0, y1, z0, z1)

    self.reflections = indexed

    # need to decide how to handle multiple panels... #TODO
    assert(len(detector) == 1)

    panel = detector[0]
    pixels = data[0]

    self.panel = panel
    self.pixels = pixels
    self.beam = beam

    assert len(crystals) == 1
    crystal = crystals[0]

    if params.unit_cell:
      from cctbx.uctbx import unit_cell
      uc = unit_cell(params.unit_cell)
      crystal.set_B(uc.fractionalization_matrix())

    # play with symmetry stuff - yay for short class names
    from dials.algorithms.refinement.parameterisation.crystal_parameters \
      import CrystalUnitCellParameterisation, \
      CrystalOrientationParameterisation

    self.crystal = crystal
    self.cucp = CrystalUnitCellParameterisation(crystal)
    self.cop = CrystalOrientationParameterisation(crystal)

    if params.phis:
      phi = flex.double(params.phis)
      self.cop.set_param_vals(phi)

    # 0-point and deltas
    values = flex.double(self.cucp.get_param_vals() +
                         self.cop.get_param_vals() + [params.r])
    offset = flex.double([0.01 * v for v in self.cucp.get_param_vals()] +
                         [0.1, 0.1, 0.1, 0.01])

    # if no input, create simplex
    if not params.unit_cell:
      refiner = simple_simplex(values, offset, self, params.max_iter)
      refined_values = refiner.get_solution()
    else:
      refined_values = flex.double(self.cucp.get_param_vals() +
                                   self.cop.get_param_vals() + [params.r])

    distance_map = self.compute_xmap(refined_values)

    if params.score == 'image':
      score, n_objects = self.score(pixels, distance_map)
      print('Score was: %.3f over %d objects' % (score, n_objects))
    else:
      score, n_objects = self.score_indexed(pixels, self.reflections,
                                            distance_map)
      print('Score was: %.3f over %d objects' % (score, n_objects))

    # plot output
    self.plot_map(distance_map, params.png)
    self.integrate(pixels, distance_map)

if __name__ == '__main__':
  from dials.util import halraiser
  try:
    script = Script()
    script.run()
  except Exception as e:
    halraiser(e)
