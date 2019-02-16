#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import fwhm
import os

import EnvManager
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TFile, TH1F, TLatex, TLine)

draw_line = True

cut_line = [None, None]

#_______________________________________________________________________________
def draw_cut_line(h, cut):
  global cut_line
  ymax = -1e10
  for i, c in enumerate(cut):
    ymax = max(ymax, h.GetBinContent(h.FindBin(c))*2.5)
  if len(cut) == 2:
    ymax = 0
  for i, c in enumerate(cut):
    cut_line[i] = TArrow(c, h.GetMaximum()*(0.05 if gPad.GetLogy() else 0.5),
                         c, ymax, 0.04, '>')
    #cut_line[i].SetLineWidth(2)
    cut_line[i].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gROOT.SetBatch()
  gStyle.SetPalette(52) # grayscale
  ROOT.TColor.InvertPalette()
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='run_number')
  parsed, unpased = parser.parse_known_args()
  # root_file = os.path.join(EnvManager.root_dir,
  #                          'K18Tracking_{:05d}.root'.format(parsed.run_number))
  root_file = os.path.join('root/dc/run'
                           '{:05d}_Easiroc.root'.format(parsed.run_number))
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  bft_file = EnvManager.fig_dir + '/dc/bft_ctime.ps'
  f1 = TFile.Open(root_file)
  #t1 = f1.Get('k18track')
  t1 = f1.Get('ea0c')
  t1.SetBranchStatus('*', 0)
  t1.SetBranchStatus('trigflag', 1)
  t1.SetBranchStatus('bft_ncl', 1)
  t1.SetBranchStatus('bft_ctime', 1)
  c1 = TCanvas('c1', 'c1')
  hw = 15
  h1 = TH1F('h1', 'h1', 10*2*hw, -hw, hw)
  for i in range(t1.GetEntries()):
    t1.GetEntry(i)
    if t1.trigflag[7] > 0:
      for i1 in range(t1.bft_ncl):
        if abs(t1.bft_ctime[i1]) < hw:
          h1.Fill(t1.bft_ctime[i1])
  h1.SetXTitle('Timing BFT [ns]')
  h1.SetYTitle('Counts [/100 ps]')
  c1.SetLogy()
  h1.Draw('')
  # fwhm.FWHM(h1, factor=0.5)
  draw_cut_line(h1, [-4, 4])
  # tex = TLatex()
  # tex.SetTextFont(132)
  # tex.SetTextSize(0.08)
  # tex.DrawLatex(0.4, h1.GetMaximum()*0.9, 'K^{#minus}')
  # tex.DrawLatex(1.2, h1.GetMaximum()*0.2, '#pi^{#minus}')
  # h3.Draw()
  c1.Print(bft_file)
  print('done')
