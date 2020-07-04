#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import argparse
import multiprocessing
import os
import subprocess
import time
import yaml

from utility import ExitFailure
from utility import pycolor as pc

proc = []

#_______________________________________________________________________________
def Wait(maxproc=None):
  if maxproc is None:
    maxproc = ( multiprocessing.cpu_count() - os.getloadavg()[0] ) * 0.9
  while len(proc) >= maxproc:
    for p in proc:
      if p.poll() is not None:
        proc.remove(p)
    #print(' ... processing {}'.format(len(proc)) + pc.up)
    time.sleep(0.01)

#_______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('macro_py', help='macro.py')
  parser.add_argument('run_list', help='run list')
  parser.add_argument('option', nargs='*', help='run list')
  parsed, unparsed = parser.parse_known_args()
  if not os.path.isfile(parsed.macro_py):
    ExitFailure('No such file : ' + parsed.macro_py)
  if not os.path.isfile(parsed.run_list):
    ExitFailure('No such file : ' + parsed.run_list)
  with open(parsed.run_list, 'r') as f:
    data = yaml.load(f.read())
  try:
    start = time.time()
    for run_number, parsets in sorted(data['RUN'].items()):
      command = [parsed.macro_py, str(run_number)]
      for o in parsed.option:
        command.append(o)
      print('command = ' + pc.Form('{}'.format(command), pc.magenta))
      proc.append(subprocess.Popen(command))
      Wait()
    nproc = len(data['RUN'].items())
    print('')
    while len(proc) != 0:
      for p in proc:
        if p.poll() is not None:
          proc.remove(p)
      print(pc.up + ' ... processing {}/{}'.format(nproc - len(proc), nproc))
      time.sleep(0.01)
    end = time.time()
    print('processing time : {:.3f} s'.format(end - start))
  except KeyboardInterrupt:
    pass
