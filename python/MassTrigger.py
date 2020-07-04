#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import EnvManager

#_______________________________________________________________________________
def process(run_number):
  ''' process '''
  import ROOT
  EnvManager.Load()
  print('run{:05d} '.format(run_number) + '_' * 60)
  root_file = 'run{:05d}_MassTrigger.root'.format(run_number)
  fig_file = os.path.join(EnvManager.fig_dir, 'MassTrigger_{:05d}.pdf'
                          .format(run_number))
  f1 = ROOT.TFile.Open(os.path.join(EnvManager.root_dir, root_file))
  if f1 == None:
    return
  t1 = f1.Get('mst')
  if t1 == None:
    return
  n_entries = t1.GetEntries()
  get_entry = t1.GetEntry
  for i in range(n_entries):
    get_entry(i)

  c1 = ROOT.TCanvas('c1', 'c1', 1000, 800)
  c1.Print(fig_file + '[')
  c1.Divide(4,3)
  c1.Print(fig_file + ']')
  ROOT.TPython.Prompt()

#_______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  try:
    process(parsed.run_number)
  except:
    print(sys.exc_info())
