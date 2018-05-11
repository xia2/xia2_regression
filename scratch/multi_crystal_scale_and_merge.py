from __future__ import print_function
import os

def run(args):
  mtz_files = []
  unhandled_args = []

  for arg in args:
    print(arg)
    if os.path.isfile(arg):
      if arg[-4:] == '.mtz':
        mtz_files.append(arg)
        continue
      elif arg[-5:] == '.json':
        json_files.append(arg)
        continue
    unhandled_args.append(arg)

  mtz_files.sort(key=os.path.getmtime)
  print(mtz_files)

  hklin = mtz_files
  hklout = 'sorted.mtz'

  pointgroup, reindex_op = decide_pointgroup(hklin, hklout)
  print(pointgroup, reindex_op)

  hklin = hklout
  hklout = 'scaled.mtz'
  scale(hklin, hklout)


def decide_pointgroup(hklin, hklout):

  from xia2.Wrappers.CCP4.Pointless import Pointless
  from xia2.lib.bits import auto_logfiler
  pointless = Pointless()
  auto_logfiler(pointless)
  pointless.set_hklin(hklin)
  pointless.set_hklout(hklout)
  pointless.set_allow_out_of_sequence_files(allow=True)
  pointless.decide_pointgroup()
  possible = pointless.get_possible_lattices()
  pointgroup = pointless.get_pointgroup()
  reindex_op =  pointless.get_reindex_operator()
  probably_twinned = pointless.get_probably_twinned()

  return pointgroup, reindex_op

def scale(hklin, hklout):
  from xia2.Handlers.Phil import PhilIndex
  PhilIndex.params.xia2.settings.multiprocessing.nproc = 1
  from xia2.Wrappers.CCP4.Aimless import Aimless
  from xia2.lib.bits import auto_logfiler
  aimless = Aimless()
  auto_logfiler(aimless)
  aimless.set_surface_link(False) # multi-crystal
  aimless.set_hklin(hklin)
  aimless.set_hklout(hklout)
  aimless.set_surface_tie(PhilIndex.params.ccp4.aimless.surface_tie)
  #aimless.set_surface_link(PhilIndex.params.ccp4.aimless.surface_link)
  aimless.set_secondary(PhilIndex.params.ccp4.aimless.secondary)
  aimless.scale()


if __name__ == '__main__':
  import sys
  run(sys.argv[1:])

