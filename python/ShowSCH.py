#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager as env
from ROOT import (gROOT, gStyle, kRed,
                  TCanvas, TCut, TFile, TH1F, TLatex)

myname = os.path.basename(__file__).replace('.py', '')

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  env.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  env.ana_type = 'Easiroc'
  env.root_file = ('{0}/run{1:05d}_{2}.root'
                   .format(env.root_dir, parsed.run_number, env.ana_type))
  env.fig_file = ('{0}/{1}_{2:05d}.pdf'
                  .format(env.fig_dir, myname, parsed.run_number))
  f = TFile.Open(env.root_file)
  if f is None:
    quit()
  tree = f.Get('ea0c')
  if tree is None:
    quit()
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.Print(env.fig_file + '[')
  hid = [20001, 20101]
  for i in xrange(len(hid)):
    c1.Clear()
    c1.Divide(2, 2)
    for j in xrange(4):
      c1.cd(j + 1)
      h = gROOT.FindObject('h{}'.format(hid[i] + j))
      if j == 0:
        h.GetXaxis().SetRangeUser(0, 10)
      if i==0 and j == 2:
        h.GetXaxis().SetRangeUser(500, 1000)
      h.Draw()
    c1.Print(env.fig_file)

  hid = [20005, 20105]
  for i in xrange(len(hid)):
    c1.Clear()
    c1.Divide(1, 2)
    for j in xrange(2):
      c1.cd(j + 1)
      h = gROOT.FindObject('h{}'.format(hid[i] + j))
      h.Draw('colz')
    c1.Print(env.fig_file)

  c1.Print(env.fig_file + ']')
