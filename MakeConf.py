#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from array import array

import EnvManager
from ROOT import (gROOT, gStyle,
                  TCanvas, TGraph, TLatex,
                  kRed)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('src_number', type=int)
  parser.add_argument('dst_number', type=int)
  parsed, unpased = parser.parse_known_args()
  src = '{0}/analyzer_{1:05d}.conf'.format(EnvManager.conf_dir,
                                           parsed.src_number)
  dst = '{0}/analyzer_{1:05d}.conf'.format(EnvManager.conf_dir,
                                           parsed.dst_number)
  if os.path.exists(dst):
    print('{0} already exists'.format(dst))
    quit()
  buf = ''
  with open(src, 'r') as f:
    for line in f.read().split('\n'):
      if str(parsed.src_number) in line:
        buf += line.replace(str(parsed.src_number),
                            str(parsed.dst_number)) + '\n'
      else:
        buf += line + '\n'
    print(buf)
  with open(dst, 'w') as f:
    f.write(buf)
