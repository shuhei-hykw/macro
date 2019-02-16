#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import sys
from array import array

import EnvManager
import utility
from ROOT import (gROOT, gStyle,
                  TCanvas, TGraph, TLatex,
                  kRed)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('src_num', type=int, nargs='?', default=57,
                      help='run number of source')
  parser.add_argument('dst_num', type=int)
  parsed, unpased = parser.parse_known_args()
  src_num = '{0:05d}'.format(parsed.src_num)
  dst_num = '{0:05d}'.format(parsed.dst_num)
  src = '{0}/analyzer_{1}.conf'.format(EnvManager.conf_dir,
                                       src_num)
  dst = '{0}/analyzer_{1}.conf'.format(EnvManager.conf_dir,
                                       dst_num)
  if os.path.exists(dst):
    utility.ExitFailure('{0} already exists'.format(dst))
  buf = ''
  if not os.path.isfile(src):
    utility.ExitFailure('No such file: ' + src)
  with open(src, 'r') as f:
    for line in f.read().split('\n'):
      if src_num in line:
        buf += line.replace(src_num, dst_num) + '\n'
      else:
        buf += line + '\n'
    # print(buf)
  with open(dst, 'w') as f:
    f.write(buf)
  for l in buf.split('\n'):
    p = l.split()
    if len(p)<2 or '#' in p[0] or not 'param' in p[1]:
      continue
    if os.path.isfile(p[1]):
      pass
    else:
      shutil.copy2(p[1].replace(dst_num, src_num), p[1])
      print('copy ' + p[1])
