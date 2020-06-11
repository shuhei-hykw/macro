#!/usr/bin/env python
# -*- coding: utf-8 -*-

import array
import argparse
import fwhm
import numpy
import os

import EnvManager

p0 = [353309.,
      356212.,
      353711.,
      351882.,
      353079.,
      353895.,
      354534.,
      354827.]

gate = 200

#_______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='run_number')
  parsed, unpased = parser.parse_known_args()
  import ROOT
  ROOT.gROOT.SetBatch()
  EnvManager.Load()
  root_file = os.path.join(EnvManager.root_dir,
               'run{:05d}_Hodoscope.root'.format(parsed.run_number))
  #root_file = 'tmp.root'
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  fig_file = EnvManager.fig_dir + '/TFitBH2_{}.pdf'.format(parsed.run_number)
  file1 = ROOT.TFile.Open(root_file)
  t1 = file1.Get('tree')
  t1.SetBranchStatus('*', 0)
  t1.SetBranchStatus('trigflag', 1)
  t1.SetBranchStatus('bh2ut', 1)
  t1.SetBranchStatus('bh2dt', 1)
  #t1.SetBranchAddress('bh2dt', bh2dt)
  harray = []
  for i in range(8):
    harray.append(ROOT.TH1F('h_dt_{}'.format(i+1),
                            'h_dt_{};TDC;Counts'.format(i+1),
                            50000, 0., 1000000.))
    harray.append(ROOT.TH1F('h_dt_{}_single'.format(i+1),
                            'h_dt_{}_single;TDC;Counts'.format(i+1),
                            50000, 0., 1000000.))
  for i in range(t1.GetEntries()):
    t1.GetEntry(i)
    # if i == 200000: break
    #if t1.trigflag[7] > 0:
    # bh2ut = numpy.reshape(t1.bh2ut, (8, 16))
    bh2dt = numpy.reshape(t1.bh2dt, (8, 16))
    nhbh2 = 0
    for i_bh2 in range(8):
      for i_multi in range(16):
        # ut = bh2ut[i_bh2][i_multi]
        dt = bh2dt[i_bh2][i_multi]
        if dt < 0:
          continue
        harray[2*i_bh2  ].Fill(dt)
        if abs(dt - p0[i_bh2]) < gate:
          nhbh2 += 1
    if nhbh2 == 1:
      for i_bh2 in range(8):
        for i_multi in range(16):
          # ut = bh2ut[i_bh2][i_multi]
          dt = bh2dt[i_bh2][i_multi]
          if dt < 0:
            continue
          harray[2*i_bh2+1].Fill(dt)
  c1 = ROOT.TCanvas('c1', 'c1')
  c1.Divide(4, 2)
  tex = ROOT.TLatex()
  tex.SetNDC()
  tex.SetTextSize(0.13)
  for i in range(8):
    c1.cd(i+1)
    h1 = harray[2*i]
    f1 = ROOT.TF1('f1', 'gaus', 0., 1000000.)
    f1.SetLineWidth(1)
    p = h1.GetBinCenter(h1.GetMaximumBin())
    w = 100
    for ifit in range(3):
      h1.Fit('f1', 'Q', '', p-2*w, p+2*w)
      p = f1.GetParameter(1)
      w = f1.GetParameter(2)
      if w < 100:
        w = 100
    print(f1.GetParameter(1))
    h1.GetXaxis().SetRangeUser(p-8*w, p+14*w)
    tex.DrawLatex(0.6, 0.22, '{:.1f}'.format(f1.GetParameter(2)))
  c1.Print(fig_file + '(')
  for i in range(8):
    c1.cd(i+1)
    h1 = harray[2*i+1]
    f1 = ROOT.TF1('f1', 'gaus', 0., 1000000.)
    f1.SetLineWidth(1)
    p = h1.GetBinCenter(h1.GetMaximumBin())
    w = 100
    for ifit in range(3):
      h1.Fit('f1', 'Q', '', p-2*w, p+2*w)
      p = f1.GetParameter(1)
      w = f1.GetParameter(2)
      if w < 100:
        w = 100
    print(f1.GetParameter(1))
    h1.GetXaxis().SetRangeUser(p-8*w, p+14*w)
    tex.DrawLatex(0.6, 0.22, '{:.1f}'.format(f1.GetParameter(2)))
  c1.Print(fig_file + ')')
  print('done')
