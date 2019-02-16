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
  root_file = 'run{0:05d}_SdcOutTracking.root'.format(parsed.run_number)
  fig_file = EnvManager.fig_dir + '/' + root_file.replace('.root', '_Eff.pdf')
  f1 = TFile.Open(EnvManager.root_dir + '/' + root_file)
  if f1 is None:
    quit()
  tree = f1.Get('sdcout')
  if tree is None:
    quit()
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.Print(fig_file + '[')
  h = TH1F('run{0:05d}'.format(parsed.run_number),
           'NTrack SdcOut', 10, 0, 10)
  tree.Project('run{0:05d}'.format(parsed.run_number),
               'ntrack', '')
  h.Draw()
  nof0 = h.GetBinContent(1)
  nof1 = h.GetBinContent(2)
  nall = h.GetEntries()
  eff = 1 - nof0 / nall
  single = nof1 / (nall - nof0)
  text = TLatex()
  text.SetNDC()
  text.SetTextSize(0.08)
  text.DrawLatex(0.32, 0.35, 'tracking eff. {0:.3f}'.format(eff))
  print('track  {0:.3f} : single/all {1:.3f}'.format(eff, single))
  c1.Print(fig_file)
  c1.Clear()
  c1.Divide(4,2)
  lname = ['SDC2-X1', 'SDC2-X2', 'SDC2-Y1', 'SDC2-Y2',
           'SDC3-Y1', 'SDC3-Y2', 'SDC3-X1', 'SDC3-X2']
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
      cut += TCut('nhit[{}]>0'.format(ll))
    tree.Project(name, 'nhit[{}]'.format(l), cut.GetTitle())
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
