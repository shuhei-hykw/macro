#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess

import run_number

default_ana_type = 'DstXiAna'
default_log_dir = 'log'

#_______________________________________________________________________________
def get_bin_list(bin_dir='bin'):
  if os.path.isdir(bin_dir):
    return sorted(os.listdir(bin_dir))

#_______________________________________________________________________________
if __name__ == '__main__':
  bin_list = get_bin_list()
  for i, bin in enumerate(bin_list):
    print(i, bin)
  parser = argparse.ArgumentParser()
  parser.add_argument('bin_number', type=int, help='bin number')
  parser.add_argument('run_number', type=int, help='run number')
  parser.add_argument('root_dir', nargs='?', default='root/all',
                      help='root dir')
  parser.add_argument('log_dir', nargs='?', default='log',
                      help='log dir')
  parsed, unparsed = parser.parse_known_args()
  t = bin_list[parsed.bin_number]
  r = parsed.run_number
  root_file = os.path.join(parsed.root_dir, '{}_{:05d}.root'.format(t, r))
  log_file = os.path.join(parsed.log_dir, '{}_{:05d}.log'.format(t, r))
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
      pass
      # subprocess.call(command, shell=True)
