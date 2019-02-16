#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import fwhm
import os

import EnvManager
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TFile, TH1F, TLatex, TLine)

#flag = 't0'
#flag = 'btof'
#flag = 'ub'
flag = 'ub2'

#ext = '.ps'
ext = '.pdf'

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
  root_file = os.path.join(EnvManager.root_dir,
                           'Hodoscope_{:05d}.root'.format(parsed.run_number))
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  f1 = TFile.Open(root_file)
  t1 = f1.Get('hodo')
  t1.SetBranchStatus('*', 0)
  t1.SetBranchStatus('trigflag', 1)
  t1.SetBranchStatus('nhBh1', 1)
  t1.SetBranchStatus('nhBh2', 1)
  t1.SetBranchStatus('tBh2', 1)
  t1.SetBranchStatus('btof', 1)
  t1.SetBranchStatus('nhBac', 1)
  c1 = TCanvas('c1', 'c1')
  #h1 = TH1F('h1', 'h1;Time-of-flight [ns];Counts [/50 ps]', 100, -2, 3)
  h1 = TH1F('h1', 'h1;[ns];Counts', 100, -2, 3)
  h12 = h1.Clone('h12')
  # h12.SetLineColor(ROOT.kRed+1)
  h2 = TH1F('h2', 'h2', 200, -5, 5)
  h3 = TH1F('h3', 'h3', 200, -5, 5)
  for i in range(t1.GetEntries()):
    # if i == 300000: break
    # if i == 300000: break
    t1.GetEntry(i)
    for i1 in range(t1.nhBh1):
      if t1.trigflag[5] > 0:
        h1.Fill(t1.btof[i1])
        if t1.nhBac == 0:
          h12.Fill(t1.btof[i1])
      if t1.trigflag[7] > 0:
        h2.Fill(t1.btof[i1])
        # h12.Fill(t1.btof[i1])
        for i2 in range(t1.nhBh2):
          h3.Fill(t1.tBh2[i2])
  h2.SetXTitle('Time-of-flight [ns]')
  h2.SetYTitle('Counts [/50 ps]')
  h3.SetXTitle('Timing BH2 [ns]')
  h3.SetYTitle('Counts [/50 ps]')
  # h2.SetLineColor(ROOT.kRed+1)
  # h1.Draw('')
  tex = TLatex()
  tex.SetTextFont(12)
  tex.SetTextSize(0.08)
  c1.SetLogy()
  '''btof'''
  h2.Draw()
  fig_file = EnvManager.fig_dir + '/dc/btof' + ext
  draw_cut_line(h2, [-2, 2])
  c1.Print(fig_file)
  print('print ' + fig_file)
  '''t0'''
  h3.Draw()
  fig_file = EnvManager.fig_dir + '/dc/t0' + ext
  draw_cut_line(h3, [-1, 1])
  c1.Print(fig_file)
  print('print ' + fig_file)
  c1.SetLogy(False)
  '''ub'''
  h1.Draw()
  fig_file = EnvManager.fig_dir + '/dc/btof_ub' + ext
  tex.DrawLatex(0.4, h1.GetMaximum()*0.9, 'K^{#minus}')
  tex.DrawLatex(1.2, h1.GetMaximum()*0.2, '#pi^{#minus}')
  c1.Print(fig_file)
  print('print ' + fig_file)
  '''ub2'''
  h12.Draw()
  fig_file = EnvManager.fig_dir + '/dc/btof_ub2' + ext
  tex.DrawLatex(0.4, h12.GetMaximum()*0.9, 'K^{#minus}')
  tex.DrawLatex(1.2, h12.GetMaximum()*0.2, '#pi^{#minus}')
  c1.Print(fig_file)
  print('print ' + fig_file)
