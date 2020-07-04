#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess

import run_number

default_ana_type = 'DstXiAna'
default_log_dir = 'log'

#_______________________________________________________________________________
def hadd():
  pass

#_______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('module_number', type=int, help='module number')
  parser.add_argument('ana_type', nargs='?', default=default_ana_type,
                      help='ana type (default={})'.format(default_ana_type))
  parser.add_argument('input_dir', nargs='?', default='root/all',
                      help='input dir')
  parser.add_argument('output_dir', nargs='?', default='root/dc',
                      help='output dir')
  parser.add_argument('-d', '--dry', action='store_true',
                      help='echo command')
  parser.add_argument('-f', '--force', action='store_true',
                      help='force overwrite')
  parser.add_argument('-n', '--no-check', action='store_true',
                      help='skip log check')
  parsed, unparsed = parser.parse_known_args()
  if parsed.module_number > 18 and parsed.module_number < 119:
    m = parsed.module_number - 19
    array = run_number.emulsion_2017[m]
  elif parsed.module_number > 0 and parsed.module_number < 119:
    m = parsed.module_number - 1
    array = run_number.emulsion_2016[m]
  else:
    quit()
  out_file = os.path.join(parsed.output_dir,
                          '{}_Mod{:03d}.root'
                          .format(parsed.ana_type,
                                  parsed.module_number))
  command = 'hadd ' if not parsed.force else 'hadd -f '
  command += out_file
  nerror = 0
  for r in array:
    head = '{}_{:05d}'.format(parsed.ana_type, r)
    if not parsed.no_check:
      log = os.path.join(default_log_dir, '{}.log'.format(head))
      if not os.path.isfile(log):
        print('mod{:03d} no such log: {}'.format(parsed.module_number, log))
        nerror += 1
    command += ' ' + os.path.join(parsed.input_dir, '{}.root'.format(head))
  if nerror == 0:
    if parsed.dry:
      pass
      #print(command)
    else:
      subprocess.call(command, shell=True)
