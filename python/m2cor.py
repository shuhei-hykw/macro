#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TF1, TFile, TH1F, TH2F,
                  TLatex, TLine,
                  TMath, TPad)

draw_line = True

kaon_mass = 0.493677
#offset = 0.101484
offset = 0.110

flag = 2

tex = TLatex()
tex.SetTextAlign(21)
tex.SetTextFont(132)
tex.SetTextSize(0.06)

cut_line = []

#_______________________________________________________________________________
def draw_cut_line(h, cut):
  global cut_line
  ymax = -1e10
  for i, c in enumerate(cut):
    ymax = max(ymax, h.GetBinContent(h.FindBin(c)) +
               h.GetMaximum()*(0.02 if len(cut_line) == 0 else 0.3))
  if len(cut) == 2:
    ymax = 0
  for i, c in enumerate(cut):
    cut_line.append(TArrow(c, h.GetMaximum()*(0.05 if gPad.GetLogy() else 0.5),
                           c, ymax, 0.04 if len(cut_line) < 2 else 0.025, '>'))
    cut_line[-1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  # gROOT.Reset()
  gROOT.SetBatch()
  # gStyle.SetPalette(52) # grayscale
  # ROOT.TColor.InvertPalette()
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  if flag == 1:
    parser.add_argument('run_number', type=int, help='run_number')
    parsed, unpased = parser.parse_known_args()
    root_file = os.path.join('root/dc/run{:05d}_KuramaTracking.root'.format(parsed.run_number))
    fig_file = EnvManager.fig_dir + '/dc/m2cor.ps'
    f1 = TFile.Open(root_file)
    t1 = f1.Get('kurama')
    h1 = TH2F('h1', 'h1;Squared mass [(GeV/#font[12]{c}^{2})^{2}]; Momentum [GeV/#font[12]{c}]',
              280, -0.2, 1.2, 220, 0.4, 1.8)
    h2 = TH1F('h2', 'h2;Time', 100, 0., 100.)
    h3 = TH1F('h3', 'h2;dTime', 100, -1., 1.)
    h4 = h1.Clone('h4')
    h5 = TH2F('h5', 'h5;TOF ADC [arb. unit];Squared mass [(GeV/#font[12]{c}^{2})^{2}]',
              450, 0, 4.5, 280, -0.2, 1.2)
    h6 = h5.Clone('h6')
    t1.SetBranchStatus('*', 0)
    t1.SetBranchStatus('trigflag', 1)
    t1.SetBranchStatus('ntKurama', 1)
    t1.SetBranchStatus('pKurama', 1)
    t1.SetBranchStatus('qKurama', 1)
    t1.SetBranchStatus('chisqrKurama', 1)
    t1.SetBranchStatus('path', 1)
    t1.SetBranchStatus('beta', 1)
    t1.SetBranchStatus('cstof', 1)
    t1.SetBranchStatus('m2', 1)
    t1.SetBranchStatus('tofsegKurama', 1)
    t1.SetBranchStatus('nhTof', 1)
    t1.SetBranchStatus('TofSeg', 1)
    t1.SetBranchStatus('deTof', 1)
    for i in range(t1.GetEntries()):
      t1.GetEntry(i)
      if t1.trigflag[7] > 0:
        for j in range(t1.ntKurama):
          if (t1.chisqrKurama[j] < 20 and
              t1.qKurama[j] > 0):
            h1.Fill(t1.m2[j], t1.pKurama[j])
            ctime = t1.cstof[j] + offset
            beta = t1.path[j]/ctime/TMath.C()*1e6
            cm2 = t1.pKurama[j]*t1.pKurama[j]*(1.-beta**2)/(beta**2)
            if(0.9 < t1.pKurama[j] and
               t1.pKurama[j] < 1.5):
              h4.Fill(cm2, t1.pKurama[j])
              for itof in range(t1.nhTof):
                if t1.tofsegKurama[j] == t1.TofSeg[itof]:
                  h5.Fill(t1.deTof[itof], t1.m2[j])
                  h6.Fill(t1.deTof[itof], cm2)
            if (abs(t1.m2[j]-0.22) < 0.04 and
                0.9 < t1.pKurama[j] and
                t1.pKurama[j] < 1.5):
              calc_time = (t1.path[j] * TMath.Sqrt(kaon_mass**2+t1.pKurama[j]**2) /
                           t1.pKurama[j] / TMath.C() * 1e6)
              h2.Fill(t1.cstof[j])
              h3.Fill(t1.cstof[j]-calc_time)
    c1 = TCanvas()
    #
    h1.Draw('col')
    h2.Draw()
    h3.Fit('gaus', '', '', -0.2, 0.1)
    hx = h4.ProjectionX().Clone('h4_px')
    hx.SetYTitle('Counts [/0.05 (GeV/#font[12]{c}^{2})^{2}]')
    # c1.cd().SetLogy()
    hx.Draw()
    tmp = TFile('m2.root', 'recreate')
    tmp.Add(h4)
    tmp.Add(hx)
    tmp.Add(h5)
    tmp.Add(h6)
    tmp.Write()
    tmp.Close()
    c1.Print(fig_file)
    # hx.GetXaxis().SetRangeUser(0,0.6)
    # ff = TF1('ff', 'gaus+pol0(3)')
    # ff.SetParameter(0, 100)
    # ff.SetParameter(1, 0.493)
    # ff.SetParameter(2, 0.040)
    # ff.SetParameter(3, 5)
    # hx.Fit('ff', '', '', 0.16, 0.32)
    # c1.cd().SetLogz()
    # h5.Draw('col')
    # c1.Print('fig/dc/tofde.ps')
    print(fig_file)
  if flag == 2:
    root_file = 'm2.root'
    f1 = TFile(root_file)
    hx = f1.Get('h4_px')
    c1 = TCanvas()
    #c1.cd().SetLogy()
    hx.RebinX(2)
    #hx.GetXaxis().SetRangeUser(-0.08,1.2)
    hx.SetXTitle('Squared mass [(GeV/#font[12]{c}^{2})^{2}]')
    hx.SetYTitle('Counts [/0.01 (GeV/#font[12]{c}^{2})^{2}]')
    hx.Draw()
    #width = 3. * 0.0364
    width = 3. * 0.038
    cut = [0.241-width, 0.241+width]
    draw_cut_line(hx, cut)
    tex.DrawLatex(0.135**2, hx.GetMaximum()*0.1, '#font[12]{#pi^{#plus}}')
    tex.DrawLatex(0.493**2, hx.GetMaximum()*0.1, '#font[12]{K^{#plus}}')
    tex.DrawLatex(0.99**2, hx.GetMaximum()*0.86, '#font[12]{p}')
    pad = TPad('pad', 'pad', 0.2, 0.4, 0.63, 0.92)
    pad.cd()#.SetLogy()
    hx2 = hx.Clone('hx2')
    hx2.SetXTitle('[(GeV/#font[12]{c}^{2})^{2}]')
    hx2.SetYTitle('')
    hx2.GetXaxis().SetRangeUser(0.02, 0.5)
    hx2.GetYaxis().SetRangeUser(0, hx2.GetMaximum()*1.1)
    hx2.Draw()
    draw_cut_line(hx2, cut)
    c1.cd()
    pad.Draw()
    c1.Print('fig/dc/m2cor_px.ps')
    c1.Clear()
    c1.cd().SetLogz()
    hde = f1.Get('h6')
    #hde.GetXaxis().SetRangeUser()
    hde.RebinX(5)
    hde.RebinY(4)
    #hde.GetYaxis().SetRangeUser(-0.2, 0.6)
    hde.Draw('colz')
    c1.Print('fig/dc/tofde.ps')
