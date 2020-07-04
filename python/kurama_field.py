#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import EnvManager
import ROOT
from ROOT import (gROOT, gStyle, gPad, kGray, kRed,
                  TBox, TCanvas, TCut, TFile, TGraph,
                  TH2F, TLatex, TLine, TMath)

#wide_mode = True
wide_mode = False

#_______________________________________________________________________________
def show_central_field(field_map):
  print(field_map)
  g1 = TGraph()
  with open(field_map, 'r') as f:
    for l in f:
      columns = l.split()
      if (float(columns[0]) == 0 and
          float(columns[1]) == 0):
        print(columns)
        g1.SetPoint(g1.GetN(),
                    float(columns[2])*10,
                    TMath.Abs(float(columns[4])))
  c1 = TCanvas('c1', 'c1', 767, 474)
  gPad.SetTopMargin(0.2)
  # g1.SetMarkerStyle(8)
  g1.GetXaxis().SetTitle('Position [mm]')
  g1.GetYaxis().SetTitle('Magnetic field [T]')
  zrange = 1200 if wide_mode else 1000
  g1.GetYaxis().SetRangeUser(0.0, 0.75)
  g1.GetXaxis().SetLimits(-zrange, zrange)
  g1.Draw('AC')
  tex = TLatex()
  tex.SetTextAlign(22)
  tex.SetTextFont(132)
  tsize = 0.04
  tex.SetTextSize(tsize)
  y = [0.8, 0.9]
  bb = []
  zz = [[0, 400, 'pole'], [-800, 50, 'end guard'], [800, 50, 'end guard']]
  for z in zz:
    b1 = TBox(z[0]-z[1], y[0], z[0]+z[1], y[1])
    b1.SetFillColor(kGray)
    b1.Draw('l')
    bb.append(b1)
    tex.DrawLatex(z[0], y[1]-0.1-tsize/2, z[2])
  # y = [0.90, 0.95]
  zz = [[-1064.2, 15, 'target'],
        [-1041.215+10, 10, 'Emulsion'],
        [-850-70-35, 35, 'PVAC FAC'],
        [-850-35, 35, ''],
        [-635.4675, 24, 'SDC1'],
        [-387.25, 4, 'SCH'],
        [884.6, 16, 'SDC2'],
        ]
  for i, z in enumerate(zz):
    if z[0] < -zrange:
      continue
    b2 = TBox(z[0]-z[1], y[0], z[0]+z[1], y[1])
    b2.SetFillColor(0)
    b2.Draw('l')
    bb.append(b2)
    offset = tsize/2+0.01 #(i%2)*(-0.12)+0.01
    tex.DrawLatex(z[0], y[1]+offset, z[2])
  c1.Print('fig/dc/kurama_by.ps')

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gROOT.SetBatch()
  gStyle.SetPalette(52)
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('field_map', help='root_file')
  parsed, unpased = parser.parse_known_args()
  show_central_field(parsed.field_map)
