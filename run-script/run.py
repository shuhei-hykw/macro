#!/usr/bin/env python3

import argparse
import os
import psutil
import time
import sys
import yaml

import runmacro
import settings

yml_data = None
macro_set = ['TFitBH1']

#______________________________________________________________________________
def nidles():
  return psutil.cpu_count() - os.getloadavg()[0]

#______________________________________________________________________________
def nruns(runs):
  n = 0
  for r in runs:
    n += r.isrunning()
  return n

#______________________________________________________________________________
def read(run_list_path):
  global yml_data
  print('Read {}'.format(run_list_path))
  with open(run_list_path, 'r') as f:
    yml_data = yaml.load(f.read())

#______________________________________________________________________________
def run(macro_key, compile=True, batch=True, interactive=False, quiet=True):
  if yml_data is None:
    print('#E run list is not read')
    return
  runs = []
  max_runs = int(nidles() - 1)
  print('max runs =', max_runs)
  for run_number in yml_data['RUN']:
    while nruns(runs) >= max_runs:
      max_runs = int(nidles() - 1)
      print('max runs =', max_runs)
      time.sleep(1)
    runs.append(runmacro.RunMacro(macro_key, run_number,
                                  quiet=True, sync=False))
    runs[-1].run()
  while nruns(runs) > 0:
    time.sleep(1)
  for r in runs:
    r.update()

#______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('run_list_path',
                      help='target run list path')
  parser.add_argument('macro_key', nargs='?',
                      help='target macro head')
  args = parser.parse_args()
  if args.macro_key is not None:
    macro_set = [args.macro_key]
  try:
    read(args.run_list_path)
    for key in macro_set:
      run(key)
  except KeyboardInterrupt:
    print('\nQuit')
