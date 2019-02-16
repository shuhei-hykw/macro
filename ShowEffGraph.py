#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from array import array

import EnvManager
from ROOT import (gROOT, gStyle,
                  TCanvas, TGraph, TLatex,
                  kRed)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  EnvManager.Load()
  # parser = argparse.ArgumentParser()
  # parser.add_argument('summary_txt')
  # parsed, unpased = parser.parse_known_args()
  fig_file = EnvManager.fig_dir + '/ShowEffGraph.pdf'
  vth1 = array('d')
  eff1 = array('d')
  vth2 = array('d')
  eff2 = array('d')
  for s in [238, 288, 338, 388]:
    vth1.append(s)
  for e in [0.381, 0.361, 0.328, 0.296]:
    eff1.append(e)
  for s in [288, 338, 388]:
    vth2.append(s)
  for e in [0.425, 0.439, 0.437]:
    eff2.append(e)
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.SetGrid()
  g1 = TGraph(len(vth1), vth1, eff1)
  g2 = TGraph(len(vth2), vth2, eff2)
  g1.SetMarkerSize(2)
  g2.SetMarkerSize(2)
  g1.SetMarkerStyle(8)
  g2.SetMarkerStyle(8)
  g2.SetMarkerColor(kRed)
  g1.GetYaxis().SetRangeUser(0,0.5)
  g1.GetXaxis().SetTitle('SDC3-Vth')
  g1.SetTitle('SdcOutTracking Efficiency')
  g1.Draw("AP")
  g2.Draw("P")
  c1.Print(fig_file)
