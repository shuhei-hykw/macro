#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TF1, TFile, TGaxis, TH1F, TLatex, TLine, TPad)

#flag = 'tdc'
flag = 'dldt'
#flag = 'residual'
#flag = 'chisqr'
#flag = 'eff'
draw_line = True

cut_line = []

#_______________________________________________________________________________
def draw_cut_line(h, cut):
  global cut_line
  ymax = -1e10
  for i, c in enumerate(cut):
    ymax = max(ymax, h.GetBinContent(h.FindBin(c)) +
               h.GetMaximum()*0.02)
  # if len(cut) == 2:
  #   ymax = 0
  for i, c in enumerate(cut):
    cut_line.append(TArrow(c, h.GetMaximum()*(0.05 if gPad.GetLogy() else 0.5),
                           c, ymax, 0.04, '>'))
    cut_line[-1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gROOT.SetBatch()
  gStyle.SetPalette(52) # grayscale
  # ROOT.TColor.InvertPalette()
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='run_number')
  parsed, unpased = parser.parse_known_args()
  if flag == 'tdc':
    root_file = os.path.join('root/dc/run{:05d}_BcOutTracking_woTDCCut.root'.format(parsed.run_number))
  else:
    root_file = os.path.join('root/dc/run{:05d}_BcOutTracking.root'.format(parsed.run_number))
  # if flag == 'residual':
  # else:
  #   root_file = os.path.join('root/all/'
  #                            'BcOutTracking_{:05d}.root'.format(parsed.run_number))
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  f1 = TFile.Open(root_file)
  tex = TLatex()
  tex.SetTextFont(132)
  tex.SetTextSize(0.08)
  if flag == 'tdc':
    tdc_file = [EnvManager.fig_dir + '/dc/bc3tdc.ps',
                EnvManager.fig_dir + '/dc/bc4tdc.ps']
    hname = ['h602', 'h1102']
    for i, h in enumerate(hname):
      h1 = f1.Get(h)
      c1 = TCanvas()
      h1.SetLineColor(1)
      h1.GetXaxis().SetRangeUser(580, 750)
      #h1.GetXaxis().SetRangeUser(450, 850)
      h1.SetXTitle('TDC [ch]')
      h1.SetYTitle('Counts [/ch]')
      hstyle.set_style(h1)
      h1.Draw('')
      draw_cut_line(h1, [630, 700])
      tex.DrawLatexNDC(0.23, 0.83, '(a)')
      c1.Print(tdc_file[i])
      print(tdc_file[i])
  elif flag == 'dldt':
    layers = [6, 11]
    drift_param = ('param/DCDRFT/DCDriftParam_{:05d}'
                   .format(parsed.run_number))
    func = {}
    with open(drift_param, 'r') as f:
      for l in f:
        columns = l.split()
        if len(columns) < 10:
          continue
        p = []
        for i in range(6):
          p.append(float(columns[i+4]))
        func[columns[0]] = p
    print(func)
    fig_file = [EnvManager.fig_dir + '/dc/bc3dldt.ps',
                EnvManager.fig_dir + '/dc/bc4dldt.ps']
    for i, l in enumerate(layers):
      h1 = f1.Get('h{}'.format(l*100+19))
      c1 = TCanvas()
      drft = TF1('drft', 'pol6', 0, 30)
      drft.SetLineColor(0)
      #drft.SetLineWidth()
      for j, p in enumerate(func[str(l+112)]):
        drft.SetParameter(j, p)
      drft.FixParameter(0, 0.0)
      h1.GetXaxis().SetRangeUser(-5, 35)
      h1.GetYaxis().SetRangeUser(-1.8, 1.8)
      h1.SetXTitle('Drift time [ns]')
      h1.SetYTitle('Drift length [mm]')
      h1.SetZTitle('Counts')
      hstyle.set_style(h1)
      gPad.SetRightMargin(0.145)
      h1.GetZaxis().SetLabelSize(0.04)
      h1.GetZaxis().SetTitleSize(0.05)
      h1.Draw('colz')
      # drft.Draw('same')
      #h1.Fit('drft', '', 'colz', 0, 35)
      #drft.Draw('same')
      tex.DrawLatexNDC(0.23, 0.83, '(b)')
      c1.Print(fig_file[i])
      print(fig_file[i])
  elif flag == 'residual':
    tdc_file = [EnvManager.fig_dir + '/dc/bc3res.ps',
                EnvManager.fig_dir + '/dc/bc4res.ps']
    for i in range(12):
      h1 = f1.Get('h{}'.format((i+1)*100+15))
      c1 = TCanvas()
      h1.SetLineColor(1)
      # h1.GetXaxis().SetRangeUser(580, 750)
      h1.GetYaxis().SetTitleOffset(1.6)
      h1.SetXTitle('Residual of hit position [mm]')
      h1.SetYTitle('Counts [/0.1 mm]')
      fwhm.FWHM(h1, 0.5)
      h1.Draw('')
      if i == 5:
        c1.Print(tdc_file[0])
        print(tdc_file[0])
      if i == 10:
        c1.Print(tdc_file[1])
        print(tdc_file[1])
  elif flag == 'chisqr':
    tdc_file = EnvManager.fig_dir + '/dc/bcoutchisqr.ps'
    h1 = f1.Get('h12')
    c1 = TCanvas()
    hstyle.set_style(h1)
    hh = h1.Clone()
    #h1.GetXaxis().SetRangeUser(0, 100)
    # h1.GetYaxis().SetTitleOffset(1.6)
    h1.SetXTitle('Reduced #chi^{2}')
    h1.SetYTitle('Counts [/0.1]')
    h1.Draw()
    draw_cut_line(h1, [20])
    pad = TPad('pad', 'pad', 0.48, 0.4, 0.88, 0.92)
    pad.cd().SetLogy()
    hh.GetYaxis().SetRangeUser(1, hh.GetMaximum()*2.05)
    hh.Draw()
    draw_cut_line(hh, [20])
    c1.cd()
    pad.Draw()
    c1.Modified()
    c1.Update()
    c1.Print(tdc_file)
    print(tdc_file)
  elif flag == 'eff':
    t1 = f1.Get('bcout')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('ntrack', 1)
    t1.SetBranchStatus('chisqr', 1)
    h1 = TH1F('h1', 'h1', 10, 0, 10)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if t1.trigflag[7] <= 0:
        continue
      n = 0
      for j in range(t1.ntrack):
        if t1.chisqr[j] < 20.:
          n += 1
      h1.Fill(n)
    nall = h1.GetEntries()
    n0 = h1.GetBinContent(1)
    n1 = h1.GetBinContent(2)
    print('eff = {}'.format(1-n0/nall))
    print('s/a = {}'.format(n1/(nall-n0)))
  print('done')
