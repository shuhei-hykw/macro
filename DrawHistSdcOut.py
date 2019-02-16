#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import EnvManager
from ROOT import (gROOT, gStyle,
                  TCanvas, TCut, TFile, TH1F)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('root_file', help='root_file')
  parsed, unpased = parser.parse_known_args()
  f1 = TFile.Open(parsed.root_file)
  if f1 is None:
    quit()
  tree = f1.Get('sdcout')
  if tree is None:
    quit()
  c1 = TCanvas()
  c1.Divide(4,2)
  hlist = []
  for l in xrange(8):
    c1.cd(l + 1).SetGrid()
    name = 'h{}'.format((l + 1) * 100 + 2)
    h = gROOT.FindObject(name)
    hlist.append(h)
    h.Draw()
  c1.Print('tmp.pdf')
