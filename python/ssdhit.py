#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, kGray, TArrow,
                  TCanvas, TCut, TF1, TFile, TH1F, TLatex, TLine, TPad)

#flag = 'at'
flag = 'de'
#flag = 'time'
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
    ymax = max(ymax, h.GetBinContent(h.FindBin(c))*2.5)
  # if len(cut) == 2:
  ymax = 0
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
  if flag == 'at':
    root_file = os.path.join('root/dc/run{:05d}_SsdHit_woFilter.root'
                             .format(parsed.run_number))
  else:
    root_file = os.path.join('root/dc/run{:05d}_SsdHit.root'
                             .format(parsed.run_number))
    root_file = os.path.join('root/dc/run{:05d}_SsdHit_woFilter.root'
                             .format(parsed.run_number))
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  f1 = TFile.Open(root_file)
  if flag == 'at':
    tdc_file = [EnvManager.fig_dir + '/dc/ssd1at.ps']
    hname = ['h33018']
    for i, h in enumerate(hname):
      h1 = f1.Get(h)
      c1 = TCanvas()
      pad_size = 1
      pad = TPad('pad', 'pad', 0., 0., pad_size, pad_size)
      # pad.SetTopMargin(0.)
      # pad.SetRightMargin(0.)
      pad.Draw()
      if pad_size < 1.0:
        pad_top = TPad('pad_top', 'pad_top', 0., pad_size, pad_size, 1.0)
        pad_right = TPad('pad_right', 'pad_right', pad_size, 0., 1.0, pad_size)
        pad_top.Draw()
        pad_right.Draw()
      rebin = 1
      h1.RebinX(rebin)
      h1.RebinY(rebin)
      hstyle.set_style(h1)
      h1.SetXTitle('Cluster #DeltaE [arb. unit]')
      h1.SetYTitle('Cluster timing [ns]')
      h1.GetYaxis().SetRangeUser(0, 200)
      pad.cd()
      h1.Draw('colz')
      cut = [2500]
      line1 = TArrow(cut[0], 200, cut[0], 0, 0, '')
      line1.Draw()
      cut = [60, 120]
      line2 = TArrow(-1000, cut[0], 50000, cut[0], 0, '')
      line3 = TArrow(-1000, cut[1], 50000, cut[1], 0, '')
      line2.Draw()
      line3.Draw()
      if pad_size < 1.0:
        hx = h1.ProjectionX()
        hy = h1.ProjectionY()
        # hx.SetFillColor(kGray)
        pad_top.cd()
        hx.Draw('bar')
        pad_right.cd()
        hy.Draw('hbar')
      gPad.SetRightMargin(0.145)
      h1.SetZTitle('Counts')
      h1.GetZaxis().SetLabelSize(0.04)
      h1.GetZaxis().SetTitleSize(0.05)
      c1.Print(tdc_file[i])
      print(tdc_file[i])
  elif flag == 'de':
    tdc_file = EnvManager.fig_dir + '/dc/ssd1de.ps'
    tree = f1.Get('ssd')
    tree.SetBranchStatus('*', 0)
    tree.SetBranchStatus('ssd1y1ncl', 1)
    tree.SetBranchStatus('ssd1y1clde', 1)
    h1 = TH1F('h1', 'h1;Cluster #DeltaE [arb. unit];Counts', 250, 0.0, 4.0e4)
    h2 = h1.Clone('h2')
    l = 'ssd1y1'
    for i in range(tree.GetEntries()):
      tree.GetEntry(i)
      for j in range(tree.ssd1y1ncl):
        h1.Fill(tree.ssd1y1clde[j])
        if tree.ssd1y1ncl == 1 and tree.ssd1y1clde[j] > 2500:
          h2.Fill(tree.ssd1y1clde[j])
    # tree.Project('h1', '{}clde'.format(l), '0<{}clde && {}clde<5e4'.format(l, l))
    # tree.Project('h2', '{}clde'.format(l), '{}clde>2500&&abs({}cltime-90)<30'.format(l, l))
    #tree.Project('h2', 'ssd1x0clde/1e4', 'ssd1x1ncl==1&&ssd1y0ncl==1&&ssd1y1ncl==1')
    c1 = TCanvas()
    h1.GetXaxis().SetNdivisions(505)
    # h1.Draw()
    # h2.Draw('same')
    h2.Draw()
    # draw_cut_line(h1, [2500])
    # h2.Draw('same')
    # #h2.Draw()
    # h2.SetFillColor(ROOT.kGray)
    c1.RedrawAxis()
    c1.Print(tdc_file)
    print(tdc_file)
  elif flag == 'time':
    fig_file = EnvManager.fig_dir + '/dc/ssdtime.ps'
    tree = f1.Get('ssd')
    h1 = TH1F('h1', 'h1;Cluster time [ns];Counts [/ns]', 180, 0.0, 180.0)
    h2 = TH1F('h2', 'h2;Cluster time [ns];Counts [/ns]', 180, 0.0, 180.0)
    tree.Project('h1', 'ssd1x0cltime', '')
    tree.Project('h2', 'ssd1x0cltime', 'ssd1x0clde>2500&&abs(ssd1x0cltime-90)<30')
    h2.SetFillColor(ROOT.kGray)
    # h2.SetFillStyle(3344)
    # h1 = f1.Get('h{}'.format(44014))
    # h2 = f1.Get('h{}'.format(44014))
    c1 = TCanvas()
    # fwhm.FWHM(h1, 0.2, verbose=True)
    h1.Draw('')
    h2.Draw('same')
    c1.RedrawAxis()
    c1.Print(fig_file)
    print(fig_file)
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
    h1.SetLineColor(1)
    hh = h1.Clone()
    #h1.GetXaxis().SetRangeUser(0, 100)
    # h1.GetYaxis().SetTitleOffset(1.6)
    h1.SetXTitle('#chi^{2}')
    h1.SetYTitle('Counts [/0.1]')
    cut = 20
    line = TArrow(cut, h1.GetMaximum()*0.5, cut, 0, 0.02, '>')
    h1.Draw()
    line.Draw()
    pad = TPad('pad', 'pad', 0.48, 0.4, 0.88, 0.92)
    pad.cd().SetLogy()
    hh.GetYaxis().SetRangeUser(1, hh.GetMaximum()*2.05)
    hh.Draw()
    line.DrawArrow(cut, h1.GetMaximum()*0.01,
                   cut, h1.GetMaximum()*0.0005, 0.02, '>')
    c1.cd()
    pad.Draw()
    c1.Modified()
    c1.Update()
    c1.Print(tdc_file)
    print(tdc_file)
  elif flag == 'eff':
    t1 = f1.Get('ssd')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    h1 = TH1F('h1', 'h1', 10, 0, 10)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if t1.trigflag[7] <= 0:
        continue
      n = 0
      # for j in range(t1.ntrack):
      #   if t1.chisqr[j] < 20.:
      #     n += 1
      h1.Fill(n)
    nall = h1.GetEntries()
    n0 = h1.GetBinContent(1)
    n1 = h1.GetBinContent(2)
    print('eff = {}'.format(1-n0/nall))
    print('s/a = {}'.format(n1/(nall-n0)))
  print('done')
