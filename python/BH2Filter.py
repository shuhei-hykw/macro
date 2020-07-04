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
  root_file = 'run{:05d}_BcOutTracking.root'.format(run_number)
  fig_file = os.path.join(EnvManager.fig_dir, 'BH2Filter_{:05d}.pdf'
                          .format(run_number))
  f1 = ROOT.TFile.Open(os.path.join(EnvManager.root_dir, root_file))
  if f1 == None:
    return
  c1 = ROOT.TCanvas('c1', 'c1', 1000, 800)
  c1.Print(fig_file + '[')
  c1.Divide(4,3)
  for i in range(3):
    for l in xrange(12):
      c1.cd(l+1)
      if i == 1:
        ROOT.gPad.SetLogz()
      hid = 100*(l + 1) + 51
      h = f1.Get('h{}'.format(hid))
      # h.__class__ = TH1
      h.SetStats(0)
      if h == None:
        continue
      h.Draw('colz')
    c1.Print(fig_file)
  c1.Print(fig_file + ']')

#_______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  try:
    process(parsed.run_number)
  except:
    print(sys.exc_info())
