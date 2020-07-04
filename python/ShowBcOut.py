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
  root_file = 'run{0:05d}_BcOutTracking.root'.format(parsed.run_number)
  fig_file = EnvManager.fig_dir + '/' + root_file.replace('.root', '.pdf')
  f1 = TFile.Open(EnvManager.root_dir + '/' + root_file)
  if f1 is None:
    quit()
  tree = f1.Get('bcout')
  if tree is None:
    quit()
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.Print(fig_file + '[')
  c1.Clear()
  c1.Divide(4,3)
  lname = ['BC3-X1', 'BC3-X2', 'BC3-V1', 'BC3-V2','BC3-U1', 'BC3-U2',
           'BC4-U1', 'BC4-U2', 'BC4-V1', 'BC4-V2','BC4-X1', 'BC4-X2']
  hlist = []
  # TDC
  for l in xrange(len(lname)):
    c1.cd(l + 1) #.SetGrid()
    h = f1.Get('h{}'.format(100*(l+1)+2))
    hlist.append(h)
    h.GetXaxis().SetRangeUser(200,500)
    h.Draw()
  c1.Print(fig_file)
  # Drift Time
  c1.Clear()
  c1.Divide(4,3)
  for l in xrange(len(lname)):
    c1.cd(l + 1) #.SetGrid()
    h = f1.Get('h{}'.format(100*(l+1)+3))
    hlist.append(h)
    #h.GetXaxis().SetRangeUser(200,500)
    h.Draw()
    h = f1.Get('h{}'.format(100*(l+1)+12))
    h.SetLineColor(kRed)
    h.Draw('same')
  c1.Print(fig_file)
  # Drift Length
  c1.Clear()
  c1.Divide(4,3)
  for l in xrange(len(lname)):
    c1.cd(l + 1) #.SetGrid()
    h = f1.Get('h{}'.format(100*(l+1)+4))
    hlist.append(h)
    #h.GetXaxis().SetRangeUser(200,500)
    h.Draw()
    h = f1.Get('h{}'.format(100*(l+1)+13))
    h.SetLineColor(kRed)
    h.Draw('same')
  c1.Print(fig_file)
  c1.Print(fig_file + ']')
