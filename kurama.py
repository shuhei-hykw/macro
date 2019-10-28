#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, kGray, TArrow,
                  TCanvas, TCut, TF1, TFile, TH1F, TH2F,
                  TLatex, TLine,
                  TMath, TPad)

#flag = 'p'
#flag = 'stof'
flag = 'tofde'
#flag = 'm'
#flag = 'm2'
#flag = 'm2p'
#flag = 'residual'
#flag = 'chisqr'
#flag = 'eff'
#draw_line = True

ext = '.ps'
#ext = '.pdf'

cut_line = []

#_______________________________________________________________________________
def draw_cut_line(h, cut):
  global cut_line
  ymax = -1e10
  for i, c in enumerate(cut):
    ymax = max(ymax, h.GetBinContent(h.FindBin(c))*1.1)
  if len(cut) == 2:
    ymax = 0
  for i, c in enumerate(cut):
    cut_line.append(TArrow(c, h.GetMaximum()*(0.05 if gPad.GetLogy() else 0.5),
                           c, ymax, 0.04, '>'))
    cut_line[-1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  # gROOT.Reset()
  gROOT.SetBatch()
  # gStyle.SetPalette(52) # grayscale
  # ROOT.TColor.InvertPalette()
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, nargs='?',
                      default=2738, help='run_number')
  parsed, unpased = parser.parse_known_args()
  if flag == 'tdc':
    root_file = os.path.join('root/dc/run{:05d}_SdcOutTracking_woTDCCut.root'.format(parsed.run_number))
  # elif flag == 'm2':
  #   root_file = os.path.join('root/DstKKAna_Mod100.root')
  elif flag == 'eff':
    root_file = os.path.join('root/all/DstKKAna_{:05d}.root'.format(parsed.run_number))
  else:
    root_file = os.path.join('root/dc/run{:05d}_KuramaTracking.root'.format(parsed.run_number))
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
  if flag == 'p':
    t1 = f1.Get('kurama')
    h1 = TH1F('h1', 'h1;Momentum [GeV/#font[12]{c}];Counts [/ 20 MeV/#font[12]{c}]', 250/2, 0, 2.5)
    h2 = h1.Clone('h2')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('pKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    t1.SetBranchStatus('m2', 1)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if t1.trigflag[7] > 0:
        for j in range(t1.ntKurama):
          if t1.chisqrKurama[j] < 30:
            h1.Fill(t1.pKurama[j])
            if abs(t1.m2[j]-0.22) < 0.04*3 and t1.qKurama[j] > 0:
              h2.Fill(t1.pKurama[j])
    c1 = TCanvas()
    h2.Draw()
    draw_cut_line(h2, [0.9, 1.5])
    tex.DrawLatexNDC(0.23, 0.83, '(b)')
    c1.Print(EnvManager.fig_dir + '/dc/kuramap2' + ext)
    h1.Draw()
    c1.Print(EnvManager.fig_dir + '/dc/kuramap1' + ext)
    h2.SetFillColor(kGray)
    h2.Draw('same')
    c1.RedrawAxis()
    # c1.SetLogy()
    tex.DrawLatex(1.1, h2.GetMaximum()*2, '#font[12]{K^{#plus}}')
    tex.DrawLatexNDC(0.23, 0.83, '(a)')
    c1.Print(EnvManager.fig_dir + '/dc/kuramap0' + ext)
  elif flag == 'm':
    t1 = f1.Get('kurama')
    h1 = TH1F('h1', 'h1', 300, -0.8, 2.2)
    h1.SetXTitle('Mass #times Charge [GeV/#font[12]{c}^{2}]')
    h1.SetYTitle('Counts [/0.01 GeV/#font[12]{c}^{2}]')
    h2 = h1.Clone('h2')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('pKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    t1.SetBranchStatus('m2', 1)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if t1.trigflag[7] > 0:
        for j in range(t1.ntKurama):
          if t1.chisqrKurama[j] < 30:
          #if t1.chisqrKurama[j] < 200:
            h1.Fill(t1.qKurama[j] * TMath.Sqrt(t1.m2[j]))
            if 0.9 < t1.pKurama[j] and t1.pKurama[j] < 1.5:
              h2.Fill(t1.qKurama[j] * TMath.Sqrt(t1.m2[j]))
    c1 = TCanvas()
    c1.cd().SetLogy()
    h1.Draw()
    tex.SetTextAlign(21)
    tex.DrawLatex(-0.45, h1.GetMaximum()*0.05, '#font[12]{K^{#minus}}')
    tex.DrawLatex(-0.135, h1.GetMaximum()*0.05, '#pi^{#minus}')
    tex.DrawLatex(0.45, h1.GetMaximum()*0.05, '#font[12]{K^{+}}')
    tex.DrawLatex(0.135, h1.GetMaximum()*0.05, '#pi^{+}')
    tex.DrawLatex(1.1, h1.GetMaximum()*0.5, '#font[12]{p}')
    tex.DrawLatex(1.83, h1.GetMaximum()*0.05, '#font[12]{d}')
    fig_file = EnvManager.fig_dir + '/dc/kuramam2' + ext
    c1.Print(fig_file)
    h2.SetFillColor(kGray)
    h2.Draw('same')
    c1.RedrawAxis()
    fig_file = EnvManager.fig_dir + '/dc/kuramam2c' + ext
    c1.Print(fig_file)
    print(fig_file)
  elif flag == 'm2':
    fig_file = EnvManager.fig_dir + '/dc/kuramam2cut' + ext
    t1 = f1.Get('kurama')
    h1 = TH1F('h1', 'h1', 100, 0., 1.)
    h1.SetXTitle('Mass [GeV/#font[12]{c}^{2}]')
    h1.SetYTitle('Counts [/0.01 GeV/#font[12]{c}^{2}]')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('pKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    t1.SetBranchStatus('m2', 1)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if t1.trigflag[7] > 0:
        for j in range(t1.ntKurama):
          if t1.chisqrKurama[j] < 20:
          #if t1.chisqrKurama[j] < 200:
            if 0.9 < t1.pKurama[j] and t1.pKurama[j] < 1.5:
              h1.Fill(TMath.Sqrt(t1.m2[j]))
    c1 = TCanvas()
    h1.GetXaxis().SetRangeUser(0.2, 0.8)
    h1.Draw()
    c1.Print(fig_file)
    print(fig_file)
  elif flag == 'm2p':
    t1 = f1.Get('kurama')
    h1 = TH1F('h1', 'h1', 300, -0.8, 2.2)
    h2 = TH2F('h2', 'h2', 300, -0.8, 2.2, 250, 0, 2.5)
    h3 = TH2F('h3', 'h3;Mass #times Charge [GeV/#font[12]{c}^{2}];Momentum [GeV/#font[12]{c}]',
              100, -0.8, 2.2, 100, -0.1, 2.5)
              #100, -0.2, 0.7, 100, 0.2, 2.2)
    h1.SetXTitle('Mass #times Charge [GeV/#font[12]{c}^{2}]')
    h1.SetYTitle('Counts [/0.01 GeV/#font[12]{c}^{2}]')
    h2.SetXTitle('Mass #times Charge [GeV/#font[12]{c}^{2}]')
    h2.SetYTitle('Momentum [GeV/#font[12]{c}]')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('pKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    t1.SetBranchStatus('m2', 1)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      #if i == 200000: break
      if t1.trigflag[7] > 0:
        for j in range(t1.ntKurama):
          if t1.chisqrKurama[j] < 30:
          #if t1.chisqrKurama[j] < 200:
            # if 0.9 < t1.pKurama[j] and t1.pKurama[j] < 1.5:
            h1.Fill(t1.qKurama[j] * TMath.Sqrt(t1.m2[j]))
            h2.Fill(t1.qKurama[j] * TMath.Sqrt(t1.m2[j]),
                    t1.pKurama[j])
            h3.Fill(ROOT.TMath.Sqrt(t1.m2[j])*t1.qKurama[j], t1.pKurama[j])
    c1 = TCanvas()
    # ph = 0.8
    # p1 = TPad('p1', 'p1', 0, ph, 1, 1)
    # p1.SetBottomMargin(0)
    # p1.Draw()
    # p2 = TPad('p2', 'p2', 0, 0, 1, ph)
    # p2.SetTopMargin(0)
    # p2.Draw()
    # h2.GetYaxis().SetRangeUser(0.21,2.3)
    # p2.cd().SetLogz()
    # h2.Draw('col')
    # p1.cd().SetLogy()
    # h2.RebinX(2)
    # h2.RebinY(2)
    # h2.Draw('col')
    h3.Draw('colz')
    tex.SetTextAlign(21)
    ypos = 0.05
    tex.DrawLatex(-0.45, ypos, '#font[12]{K^{#minus}}')
    tex.DrawLatex(-0.135, ypos, '#pi^{#minus}')
    tex.DrawLatex(0.45, ypos, '#font[12]{K^{+}}')
    tex.DrawLatex(0.135, ypos, '#pi^{+}')
    tex.DrawLatex(0.938, ypos, '#font[12]{p}')
    tex.DrawLatex(1.83, ypos, '#font[12]{d}')
    c1.cd().SetLogz()
    fig_file = EnvManager.fig_dir + '/dc/kuramam2p' + ext
    # c1.Print(fig_file)
    # fig_file = EnvManager.fig_dir + '/dc/kuramam2pz' + ext
    gPad.SetRightMargin(0.12)
    #h3.SetZTitle('Counts')
    h3.GetZaxis().SetLabelSize(0.04)
    h3.GetZaxis().SetTitleOffset(0.7)
    h3.GetZaxis().SetTitleSize(0.05)
    c1.Print(fig_file)
    print(fig_file)
  elif flag == 'chisqr':
    tdc_file = EnvManager.fig_dir + '/dc/kuramachisqr' + ext
    t1 = f1.Get('kurama')
    #h1 = f1.Get('h12')
    h1 = TH1F('h1', 'h1;Reduced #chi^{2};Counts [/0.1]', 1000, 0, 100)
    h1w = h1.Clone('h1w')
    h2 = h1.Clone('h2')
    h1s = h1.Clone('h1s')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('ntSdcIn', 1)
    t1.SetBranchStatus('ntSdcOut', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      for j in range(t1.ntKurama):
        if t1.trigflag[7] > 0 and t1.qKurama[j] > 0:
          h1.Fill(t1.chisqrKurama[j])
          h1w.Fill(t1.chisqrKurama[j])
          if t1.ntKurama == 1:
            h1s.Fill(t1.chisqrKurama[j])
        if t1.trigflag[5] > 0:
          h2.Fill(t1.chisqrKurama[j])
    c1 = TCanvas()
    # hh = h1.Clone()
    #h1.GetXaxis().SetRangeUser(0, 100)
    # h1.GetYaxis().SetTitleOffset(1.6)
    for h in [h1, h2]:
      h.Print()
      print('mean   = {}'.format(h.GetMean()))
      print('stddev = {}'.format(h.GetStdDev()))
      print('peak   = {}'.format(h.GetBinCenter(h.GetMaximumBin())))
    # h1.SetXTitle('#chi^{2}')
    # h1.SetYTitle('Counts [/0.1]')
    h1.Draw()
    draw_cut_line(h1, [30])
    # line.Draw()
    # pad = TPad('pad', 'pad', 0.48, 0.4, 0.88, 0.92)
    # pad.cd().SetLogy()
    # h1w.Draw()
    # if cut > 100:
    #   line.DrawArrow(cut, h1.GetMaximum(),
    #                  cut, h1.GetMaximum()*0.03, 0.02, '>')
    # c1.cd()
    # # pad.Draw()
    # if cut < 100:
    #   line.DrawArrow(cut, h1.GetMaximum()*0.5,
    #                  cut, h1.GetMaximum()*0, 0.02, '>')
    # c1.Modified()
    # c1.Update()
    c1.Print(tdc_file)
    print(tdc_file)
  elif flag == 'tofde':
    tdc_file = EnvManager.fig_dir + '/dc/tofde' + ext
    t1 = f1.Get('kurama')
    h1 = TH2F('h1', 'h1;TOF #DeltaE;Squared mass [GeV/#font[42]{c}^{2}]',
              100, 0, 6, 100, -0.2, 1.2)
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('nhTof', 1)
    t1.SetBranchStatus('deTof', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    t1.SetBranchStatus('m2', 1)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if t1.ntKurama != 1 or t1.nhTof != 1:
        continue
      h1.Fill(t1.deTof[0], t1.m2[0])
    c1 = TCanvas()
    h1.Draw('colz')
    #draw_cut_line(h1, [30])
    c1.Print(tdc_file)
    print(tdc_file)
  elif flag == 'eff':
    #t1 = f1.Get('kurama')
    t1 = f1.Get('kk')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('nhFbh', 1)
    t1.SetBranchStatus('nhSch', 1)
    t1.SetBranchStatus('ntBcOut', 1)
    t1.SetBranchStatus('ntSdcIn', 1)
    t1.SetBranchStatus('ntSdcOut', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    h1 = TH1F('h1', 'h1', 10, 0, 10)
    h2 = TH1F('h2', 'h2', 10, 0, 10)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if (t1.nhFbh > 0 and
          t1.nhSch > 0 and
          t1.ntBcOut > 0 and
          t1.ntSdcIn > 0 and
          t1.ntSdcOut > 0):
        n = 0
        for j in range(t1.ntKurama):
          if t1.chisqrKurama[j] > 30: continue
          # if t1.chisqrKurama[j] > 200: continue
          n += 1
        if t1.trigflag[7] > 0:
          h1.Fill(n)
        if t1.trigflag[5] > 0:
          h2.Fill(n)
    for h in [h1, h2]:
      nall = h.GetEntries()
      n0 = h.GetBinContent(1)
      n1 = h.GetBinContent(2)
      h.Print()
      print('eff = {}'.format(1-n0/nall))
      print('s/a = {}'.format(n1/(nall-n0)))
  print('done')
