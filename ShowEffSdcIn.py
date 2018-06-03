#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import EnvManager
from ROOT import (gROOT, gStyle,
                  TCanvas, TCut, TFile, TH1F, TLatex)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  root_file = 'run{0:05d}_SdcInTracking.root'.format(parsed.run_number)
  fig_file = EnvManager.fig_dir + '/' + root_file.replace('.root', '_Eff.pdf')
  f1 = TFile.Open(EnvManager.root_dir + '/' + root_file)
  if f1 is None:
    quit()
  tree = f1.Get('sdcin')
  if tree is None:
    quit()
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.Print(fig_file + '[')
  h = TH1F('run{0:05d}'.format(parsed.run_number),
           'NTrack SdcIn', 10, 0, 10)
  tree.Project('run{0:05d}'.format(parsed.run_number),
               'ntrack', '')
  h.Draw()
  nof0 = h.GetBinContent(1)
  nall = h.GetEntries()
  eff = 1 - nof0 / nall
  text = TLatex()
  text.SetNDC()
  text.SetTextSize(0.08)
  text.DrawLatex(0.32, 0.35, 'tracking eff. {0:.3f}'.format(eff))
  print('track  {0:.3f}'.format(eff))
  c1.Print(fig_file)
  c1.Clear()
  c1.Divide(3,2)
  lname = ['SDC1-V1', 'SDC1-V2', 'SDC1-X1', 'SDC1-X2',
           'SDC1-U1', 'SDC1-U2']
  hlist = []
  for l in xrange(len(lname)):
    c1.cd(l + 1) #.SetGrid()
    name = 'h{}'.format(l + 1)
    title = 'Multiplicity {}'.format(lname[l])
    h = TH1F(name, title, 10, 0, 10)
    hlist.append(h)
    cut = TCut()
    for ll in xrange(8):
      if l == ll:
        continue
      cut += TCut('nhSdcIn[{}]>0'.format(ll))
    tree.Project(name, 'nhSdcIn[{}]'.format(l), cut.GetTitle())
    #tree.Project(name, 'nhit[{}]'.format(l))
    h.Draw()
    nof0 = h.GetBinContent(1)
    nall = h.GetEntries()
    eff = 1 - nof0 / nall
    text = TLatex()
    text.SetNDC()
    text.SetTextSize(0.08)
    text.DrawLatex(0.32, 0.35, 'plane eff. {0:.3f}'.format(eff))
    print('{0:2}  {1:.3f}'.format(l, eff))
  c1.Print(fig_file)
  c1.Print(fig_file + ']')
