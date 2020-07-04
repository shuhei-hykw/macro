#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TF1, TFile, TH1F, TLatex, TLine, TPad)

#flag = 'tdc'
flag = 'dldt'
#flag = 'residual'
#flag = 'chisqr'
#flag = 'eff'
#flag = 'tof'
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
    root_file = os.path.join('root/dc/run{:05d}_SdcOutTracking_woTDCCut.root'.format(parsed.run_number))
  elif flag == 'eff':
    root_file = os.path.join('root/all/DstKKAna_{:05d}.root'.format(parsed.run_number))
  elif flag == 'tof':
    root_file = os.path.join('root/dc/run{:05d}_SdcOutTracking_woTOF.root'.format(parsed.run_number))
  else:
    root_file = os.path.join('root/all/SdcOutTracking_{:05d}.root'.format(parsed.run_number))
    #    root_file = os.path.join('root/dc/run{:05d}_SdcInTracking.root'.format(parsed.run_number))
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
    tdc_file = [EnvManager.fig_dir + '/dc/sdc2tdc.ps',
                EnvManager.fig_dir + '/dc/sdc3tdc.ps']
    hname = ['h102', 'h802']
    for i, h in enumerate(hname):
      h1 = f1.Get(h)
      c1 = TCanvas()
      h1.SetLineColor(1)
      if i == 0:
        h1.GetXaxis().SetRangeUser(500, 1000)
        cut = [640, 890]
        label = '(a)'
      else:
        h1.GetXaxis().SetRangeUser(300, 1000)
        cut = [450, 890]
        label = '(c)'
      h1.SetXTitle('TDC [ch]')
      h1.SetYTitle('Counts [/ch]')
      hstyle.set_style(h1)
      h1.Draw('')
      draw_cut_line(h1, cut)
      tex.DrawLatexNDC(0.23, 0.83, label)
      c1.Print(tdc_file[i])
      print(tdc_file[i])
  elif flag == 'dldt':
    layers = [4, 5]
    fig_file = [EnvManager.fig_dir + '/dc/sdc2dldt.ps',
                EnvManager.fig_dir + '/dc/sdc3dldt.ps']
    for i, l in enumerate(layers):
      h1 = f1.Get('h{}'.format(l*100+19))
      c1 = TCanvas()
      if i == 0:
        h1.GetXaxis().SetRangeUser(-20, 130)
        h1.GetYaxis().SetRangeUser(-6, 6)
        label = '(b)'
      else:
        h1.GetXaxis().SetRangeUser(-20, 260)
        h1.GetYaxis().SetRangeUser(-12, 12)
        label = '(d)'
      h1.SetXTitle('Drift time [ns]')
      h1.SetYTitle('Drift length [mm]')
      #h1.SetYTitle('Hit position [mm]')
      hstyle.set_style(h1)
      h1.Draw('colz')
      tex.DrawLatexNDC(0.23, 0.83, label)
      gPad.SetRightMargin(0.145)
      h1.SetZTitle('Counts')
      h1.GetZaxis().SetLabelSize(0.04)
      h1.GetZaxis().SetTitleSize(0.05)
      c1.Print(fig_file[i])
      print(fig_file[i])
  elif flag == 'residual':
    tdc_file = [EnvManager.fig_dir + '/dc/sdc1res.ps']
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
    tdc_file = EnvManager.fig_dir + '/dc/sdcoutchisqr.ps'
    t1 = f1.Get('sdcout')
    #h1 = f1.Get('h12')
    h1 = TH1F('h1', 'h1', 500, 0, 50)
    t1.Project('h1', 'chisqr[]', '')
    c1 = TCanvas()
    # hh = h1.Clone()
    #h1.GetXaxis().SetRangeUser(0, 100)
    # h1.GetYaxis().SetTitleOffset(1.6)
    h1.SetXTitle('Reduced #chi^{2}')
    h1.SetYTitle('Counts [/0.1]')
    # cut = 20
    # line = TArrow(cut, h1.GetMaximum()*0.5, cut, 0, 0.02, '>')
    h1.Draw()
    # line.Draw()
    # pad = TPad('pad', 'pad', 0.48, 0.4, 0.88, 0.92)
    # pad.cd().SetLogy()
    # hh.GetYaxis().SetRangeUser(1, hh.GetMaximum()*2.05)
    # hh.Draw()
    # line.DrawArrow(cut, h1.GetMaximum()*0.01,
    #                cut, h1.GetMaximum()*0.0005, 0.02, '>')
    # c1.cd()
    # pad.Draw()
    # c1.Modified()
    # c1.Update()
    c1.Print(tdc_file)
    print(tdc_file)
  elif flag == 'eff':
    t1 = f1.Get('kk')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('nhFbh', 1)
    t1.SetBranchStatus('nhSch', 1)
    t1.SetBranchStatus('ntBcOut', 1)
    t1.SetBranchStatus('ntSdcIn', 1)
    t1.SetBranchStatus('ntSdcOut', 1)
    h1 = TH1F('h1', 'h1', 10, 0, 10)
    h2 = TH1F('h2', 'h2', 10, 0, 10)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if (t1.nhFbh > 0 and
          t1.nhSch > 0 and
          t1.ntBcOut > 0 and
          t1.ntSdcIn > 0 ):
        if t1.trigflag[7] > 0:
          h1.Fill(t1.ntSdcOut)
        if t1.trigflag[5] > 0:
          h2.Fill(t1.ntSdcOut)
    nall = h1.GetEntries()
    n0 = h1.GetBinContent(1)
    n1 = h1.GetBinContent(2)
    print('(K,K)')
    print('eff = {}'.format(1-n0/nall))
    print('s/a = {}'.format(n1/(nall-n0)))
    nall = h2.GetEntries()
    n0 = h2.GetBinContent(1)
    n1 = h2.GetBinContent(2)
    print('(ub,ub)')
    print('eff = {}'.format(1-n0/nall))
    print('s/a = {}'.format(n1/(nall-n0)))
  elif flag == 'tof':
    pdf_file = EnvManager.fig_dir + '/dc/sdcouttof.ps'
    t1 = f1.Get('sdcout')
    h1 = f1.Get('h41')
    h2 = f1.Get('h42')
    c1 = TCanvas()
    # h1.SetXTitle('#chi^{2}')
    # h1.SetYTitle('Counts [/0.1]')
    # cut = 20
    # line = TArrow(cut, h1.GetMaximum()*0.5, cut, 0, 0.02, '>')
    hstyle.set_style(h2)
    h2.SetXTitle('y-position [mm]')
    h2.SetYTitle('#Delta t [ns]')
    h2.RebinX(4)
    h2.RebinY(4)
    h2.Draw('col')
    c1.Print(pdf_file)
    print(pdf_file)
  print('done')
