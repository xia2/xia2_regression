from dials.array_family import flex
import cPickle as pickle
import math
import sys
from scitbx import matrix
import scitbx.math as smath
import json

def nint(a):
  return int(round(a))

def scorify(params):
  rx, ry, rz = params
  R = matrix.sqr(smath.euler_angles_as_matrix((rx, ry, rz), deg=True))
  score = 0.0
  for j in range(data.size()):
    if i_s[j] < 3:
      continue
    hkl = data['miller_index'][j]
    q = R * UB * hkl
    score += i_s[j] * abs((q + s0).length() - matrix.col(data['s1'][j]).length())
  return score

from scitbx import simplex

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
    self.n = len(values)
    self.x = values
    self.starting_simplex = generate_start(values, offset)
    self.fcount = 0

    optimizer = simplex.simplex_opt(dimension=self.n,
                                    matrix=self.starting_simplex,
                                    evaluator=evaluator,
                                    tolerance=1e-10,
                                    max_iter=max_iter)

    self.x = optimizer.get_solution()
    return

  def get_solution(self):
    return self.x

  def target(self, vector):
    score = scorify(vector)
    return score

class Apple(object):

  def __init__(self, reflection_file, experiment_file):
    # make a pie

    data = pickle.load(open(reflection_file, 'rb'))
    print '%d reflections' % data.size()

    self.data = data.select(data['intensity.sum.variance'] > 0)

    i = data['intensity.sum.value']
    v = data['intensity.sum.variance']
    s = flex.sqrt(v)
    self.i_s = i/s

    from dxtbx.model.experiment.experiment_list import ExperimentListFactory
    expt = ExperimentListFactory.from_json_file(experiment_file)
    panel = expt.detectors()[0][0]
    crystal = expt.crystals()[0]
    self.s0 = matrix.col(expt.beams()[0].get_s0())
    wavelength = expt.beams()[0].get_wavelength()

    # make a list of observed q positions

    self.qobs = []
    for j in range(data.size()):
      x, y, z = data['xyzobs.px.value'][j]
      p = matrix.col(panel.get_pixel_lab_coord((x, y)))
      q = p.normalize() / wavelength - self.s0
      self.qobs.append(q)

    self.wavelength = wavelength
    self.panel = panel
    self.beam = expt.beams()[0]

    # slurp data from $somewhere

    imageset = expt.imagesets()[0]
    self.raw_data = imageset.get_raw_data(0)[0]

    from dials.algorithms.refinement.parameterisation.crystal_parameters \
      import CrystalUnitCellParameterisation, \
      CrystalOrientationParameterisation

    self.crystal = crystal
    self.cucp = CrystalUnitCellParameterisation(crystal)
    self.cop = CrystalOrientationParameterisation(crystal)

    self.zero()

    # 0-point and deltas
    values = flex.double(self.cucp.get_param_vals() +
                         self.cop.get_param_vals())
    offset = flex.double([0.01 * v for v in self.cucp.get_param_vals()] +
                         [0.1, 0.1, 0.1])

    initial = crystal.get_unit_cell()
    self.cells = []
    self.best_score = 1e99
    initial_score = self.target(values)
    doohicky = simple_simplex(values, offset, self, 2000)
    best = doohicky.get_solution()
    print 'Initial cell:', initial
    print 'Final cell:  ', crystal.get_unit_cell()
    print 'Score change', initial_score, self.target(best, do_print=False)
    self.best = best

  def plot_map(self, map, filename):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot
    data = map.as_numpy_array()
    fig = pyplot.gcf()
    pyplot.imshow(data, cmap='gray_r')
    pyplot.savefig(filename, dpi=400)
    return

  def plot_log_map(self, map, filename):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot

    negative = (map.as_1d() <= 0)
    map.as_1d().set_selected(negative, 1)
    logmap = flex.log10(map.as_double())

    data = logmap.as_numpy_array()
    fig = pyplot.gcf()
    pyplot.imshow(data, cmap='gray_r')
    pyplot.savefig(filename, dpi=400)
    return

  def render_distance(self):
    distance_map = flex.double(flex.grid(self.raw_data.focus()))
    origin = self.panel.get_origin()
    fast = self.panel.get_fast_axis()
    slow = self.panel.get_slow_axis()
    nfast, nslow = self.panel.get_image_size()

    UB = matrix.sqr(self.crystal.get_A())
    UBi = UB.inverse()

    from xia2_regression import q_map
    distance_map = q_map(self.panel, self.beam, UB, 1)
    return distance_map

  def target(self, vector, do_print=False):
    cell_parms = self.cucp.get_param_vals()
    orientation_parms = self.cop.get_param_vals()
    assert len(vector) == len(cell_parms) + len(orientation_parms)
    tst_cell = vector[:len(cell_parms)]
    tst_orientation = vector[len(cell_parms):len(cell_parms) +
                             len(orientation_parms)]

    self.cucp.set_param_vals(tst_cell)
    self.cop.set_param_vals(tst_orientation)

    from scitbx import matrix

    if do_print:
      print 'Cell: %.3f %.3f %.3f %.3f %.3f %.3f' % \
        tuple(self.crystal.get_unit_cell().parameters())
      print 'Phi(1,2,3): %.3f %.3f %.3f' % tuple(tst_orientation)

    UB = matrix.sqr(self.crystal.get_A())

    score = self.score(UB)

    if score < self.best_score:
      self.best_score = score
      self.cells.append(self.crystal.get_unit_cell().parameters())
    return score

  def score_old(self, RUB):
    score = 0.0
    for j in range(self.data.size()):
      hkl = self.data['miller_index'][j]
      q = RUB * hkl
      score += self.i_s[j] * abs(
        (q + self.s0).length() - matrix.col(self.data['s1'][j]).length())
    return score

  def score(self, UB):
    score = 0.0
    for j in range(self.data.size()):
      hkl = self.data['miller_index'][j]
      q = UB * hkl
      qo = self.qobs[j]
      score += (q - qo).length() ** 2
    return score

  def plotify(self):
    vector = self.best
    cell_parms = self.cucp.get_param_vals()
    orientation_parms = self.cop.get_param_vals()
    assert len(vector) == len(cell_parms) + len(orientation_parms)
    tst_cell = vector[:len(cell_parms)]
    tst_orientation = vector[len(cell_parms):len(cell_parms) +
                             len(orientation_parms)]

    self.cucp.set_param_vals(tst_cell)
    self.cop.set_param_vals(tst_orientation)

    from scitbx import matrix

    UB = matrix.sqr(self.crystal.get_A())
    data = self.data
    self.maxq = 0
    for j in range(data.size()):
      hkl = data['miller_index'][j]
      q = UB * hkl
      qo = self.qobs[j]
      print (q - qo).length(), self.i_s[j], self.dq0[j]
      if (q - qo).length() > self.maxq:
        self.maxq = (q - qo).length()

    return

  def zero(self):
    from scitbx import matrix

    UB = matrix.sqr(self.crystal.get_A())
    data = self.data
    self.dq0 = []
    for j in range(data.size()):
      hkl = data['miller_index'][j]
      q = UB * hkl
      qo = self.qobs[j]
      self.dq0.append((q - qo).length())

    return

import copy
apple = Apple(sys.argv[1], sys.argv[2])
apple.plotify()
distance_map = apple.render_distance()
raw_data = apple.raw_data
maxq = apple.maxq
close = (distance_map.as_1d() < (2 * maxq))
far = (distance_map.as_1d() >= (2 * maxq))
spot = copy.deepcopy(raw_data)
background = copy.deepcopy(raw_data)
spot.as_1d().set_selected(far, -1)
background.as_1d().set_selected(close, -1)

apple.plot_log_map(spot, 'spot.png')
apple.plot_log_map(background, 'background.png')
