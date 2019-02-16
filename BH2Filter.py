#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import EnvManager
from ROOT import (gROOT, gStyle,
                  TCanvas, TCut, TFile, TH1, TH1F, TLatex)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gStyle.SetOptStat(0)
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  root_file = 'run{0:05d}_BcOutTracking.root'.format(parsed.run_number)
  fig_file = ('{0}/BH2Filter_{1:05d}.pdf'
              .format(EnvManager.fig_dir, parsed.run_number))
  f1 = TFile.Open(EnvManager.root_dir + '/' + root_file)
  if f1 is None:
    quit()
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.Print(fig_file + '[')
  c1.Divide(4,3)
  for l in xrange(12):
    c1.cd(l+1)
    hid = 100*(l + 1) + 8
    h = f1.Get('h{}'.format(hid))
    h.__class__ = TH1
    h.SetStats(0)
    h.Draw('colz')
  c1.Print(fig_file)
  c1.Clear()
  c1.Divide(4,2)
  for l in xrange(12):
    for seg in xrange(8):
      c1.cd(seg+1)
      hid = 10000*(l + 1) + 8000 + seg + 1
      h = gROOT.FindObject('h{}'.format(hid))
      h.SetStats(0)
      h.Draw('colz')
    c1.Print(fig_file)
  c1.Print(fig_file + ']')
