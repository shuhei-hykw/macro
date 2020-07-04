#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import EnvManager
from ROOT import (gROOT, gStyle, kRed,
                  TCanvas, TCut, TFile, TH1F, TLatex)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  root_file = 'run{0:05d}_Easiroc.root'.format(parsed.run_number)
  fig_file = EnvManager.fig_dir + '/' + root_file.replace('.root', '.pdf')
  f1 = TFile.Open(EnvManager.root_dir + '/' + root_file)
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.Clear()
  c1.Divide(4, 4)
  # hid_list = [10008, 10009, 20004, 20014, 30008, 40008, 50008,
  #             60008, 70008, 80008, 90008, 100008, 110008, 120008,
  #             130008]
  hid_list = [20004, 20014]
  for i, hid in enumerate(hid_list):
    c1.cd(i + 1 if i < 7 else i + 2) #.SetGrid()
    h = f1.Get('h{}'.format(hid))
    p = h.GetBinCenter(h.GetMaximumBin())
    w = 10
    h.Fit('gaus', '', '', p-w, p+w)
  c1.Print(fig_file)
