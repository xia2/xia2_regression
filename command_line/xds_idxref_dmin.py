from __future__ import division
from __future__ import print_function

def main(xparm_file, spot_file):

  import dxtbx
  from dxtbx.serialize.xds import to_crystal
  models = dxtbx.load(xparm_file)
  crystal_model = to_crystal(xparm_file)

  from dxtbx.model.experiment.experiment_list import Experiment, ExperimentList
  experiment = Experiment(beam=models.get_beam(),
                          detector=models.get_detector(),
                          goniometer=models.get_goniometer(),
                          scan=models.get_scan(),
                          crystal=crystal_model)

  detector = experiment.detector
  beam = experiment.beam
  goniometer = experiment.goniometer
  scan = experiment.scan

  from iotbx.xds import spot_xds
  spot_xds_handle = spot_xds.reader()
  spot_xds_handle.read_file(spot_file)

  from cctbx.array_family import flex
  centroids_px = flex.vec3_double(spot_xds_handle.centroid)
  miller_indices = flex.miller_index(spot_xds_handle.miller_index)

  # only those reflections that were actually indexed
  centroids_px = centroids_px.select(miller_indices != (0,0,0))
  miller_indices = miller_indices.select(miller_indices != (0,0,0))

  ub = crystal_model.get_A()

  d_spacings = [1.0 / (ub * mi).length() for mi in miller_indices]

  print(max(d_spacings))

  # Convert Pixel coordinate into mm/rad
  x, y, z = centroids_px.parts()
  x_mm, y_mm = detector[0].pixel_to_millimeter(flex.vec2_double(x, y)).parts()
  z_rad = scan.get_angle_from_array_index(z, deg=False)
  centroids_mm = flex.vec3_double(x_mm, y_mm, z_rad)

  # then convert detector position to reciprocal space position

  # based on code in dials/algorithms/indexing/indexer2.py
  s1 = detector[0].get_lab_coord(flex.vec2_double(x_mm, y_mm))
  s1 = s1/s1.norms() * (1/beam.get_wavelength())
  S = s1 - beam.get_s0()
  reciprocal_space_points = S.rotate_around_origin(
    goniometer.get_rotation_axis(),
    -z_rad)

  d_spacings = 1/reciprocal_space_points.norms()
  dmax = flex.max(d_spacings)
  print(dmax)

if __name__ == '__main__':
  import sys
  main('XPARM.XDS', 'SPOT.XDS')
