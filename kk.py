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
offset = 0.110
make_root = False

cut_line = []

#_______________________________________________________________________________
def draw_cut_line(h, cut):
  global cut_line
  ymax = -1e10
  for i, c in enumerate(cut):
    ymax = max(ymax, h.GetBinContent(h.FindBin(c)) +
               h.GetMaximum()*0.0)
  # if len(cut) == 2:
  #   ymax = 0
  for i, c in enumerate(cut):
    cut_line.append(TArrow(c, h.GetMaximum()*(0.05 if gPad.GetLogy() else 0.5),
                           c, ymax, 0.04, '>'))
    cut_line[-1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  # gROOT.Reset()
  gROOT.SetBatch()
  #EnvManager.Load()
  # parser = argparse.ArgumentParser()
  # parser.add_argument('run_number', type=int, help='run_number')
  # parsed, unpased = parser.parse_known_args()
  tex = TLatex()
  tex.SetTextFont(132)
  tex.SetTextSize(0.08)
  if make_root:
    hxy = TH2F('hxy', 'hxy', 100, -50, 50, 100, -50, 50)
    hzt = TH2F('hzt', 'hzt', 400, -200, 200, 450, 0, 45)
    hvx = TH1F('hvx', 'hvx', 200, -100, 100)
    hvy = TH1F('hvy', 'hvy', 200, -100, 100)
    hvz = TH1F('hvz', 'hvz', 200, -200, 200)
    hcd = TH1F('hcd', 'hcd', 300, 0, 30)
    hmm = TH1F('hmm', 'hmm; Missing mass [GeV/#font[12]{c}^{2}]', 800, 1, 1.8)
    hth = TH1F('hth', 'hth; Scattering angle [deg]', 180, 0, 90)
    hthz = TH2F('hthz', 'hthz;z-vertex [mm];Scattering angle [deg]', 200, -200, 200, 180, 0, 90)
    hmmw = hmm.Clone('hmmw')
    for r in range(100):
      root_file = os.path.join('root/dc/DstKKAna_Mod{:03d}.root'.format(r+19))
      print('reading', root_file)
      f1 = TFile.Open(root_file)
      t1 = f1.Get('kk')
      t1.SetBranchStatus('*', 0)
      t1.SetBranchStatus('trigflag', 1)
      t1.SetBranchStatus('ntKurama', 1)
      t1.SetBranchStatus('pKurama', 1)
      t1.SetBranchStatus('qKurama', 1)
      t1.SetBranchStatus('chisqrKurama', 1)
      t1.SetBranchStatus('stof', 1)
      t1.SetBranchStatus('path', 1)
      t1.SetBranchStatus('m2', 1)
      t1.SetBranchStatus('nKn', 1)
      t1.SetBranchStatus('nKp', 1)
      t1.SetBranchStatus('nKK', 1)
      t1.SetBranchStatus('theta', 1)
      t1.SetBranchStatus('closeDist', 1)
      t1.SetBranchStatus('vtx', 1)
      t1.SetBranchStatus('vty', 1)
      t1.SetBranchStatus('vtz', 1)
      t1.SetBranchStatus('MissMass', 1)
      t1.SetBranchStatus('theta', 1)
      for i in range(t1.GetEntries()):
        # if i == 1000: break
        t1.GetEntry(i)
        if t1.trigflag[7] > 0:
          for ikp in range(t1.nKp):
            if t1.chisqrKurama[ikp] > 20: continue
            if t1.qKurama[ikp] <= 0: continue
            # if t1.pKurama[ikp] < 0.9: continue
            if 1.5 < t1.pKurama[ikp]: continue
            ctime = t1.stof[ikp] + offset
            beta = t1.path[ikp]/ctime/TMath.C()*1e6
            cm2 = t1.pKurama[ikp]*t1.pKurama[ikp]*(1.-beta**2)/(beta**2)
            width = 3 * 0.038
            #if abs(t1.m2[ikp]-0.22) > 0.04*3: continue
            if abs(cm2-0.241) > width: continue
            for ikn in range(t1.nKn):
              ikk = ikn+ikp*t1.nKn
              hmmw.Fill(t1.MissMass[ikk])
              if 0.9 < t1.pKurama[ikp]:
                hvx.Fill(t1.vtx[ikk])
                hvy.Fill(t1.vty[ikk])
                hvz.Fill(t1.vtz[ikk])
                hxy.Fill(t1.vtx[ikk], t1.vty[ikk])
                hzt.Fill(t1.vtz[ikk], t1.theta[ikk])
                hcd.Fill(t1.closeDist[ikk])
                hmm.Fill(t1.MissMass[ikk])
                hth.Fill(t1.theta[ikk])
                hthz.Fill(t1.vtz[ikk], t1.theta[ikk])
    c1 = TCanvas()
    #hxy.Draw('col')
    # hz = hzt.ProjectionX()
    # hz.SetXTitle('z-vertex [mm]')
    # hz.SetYTitle('Counts [/mm]')
    # hz.Draw('')
    # cut = [-80, 80]
    # line1 = TArrow(cut[0], hz.GetMaximum()*0.5,
    #                cut[0], 0, 0.02, '>')
    # line2 = TArrow(cut[1], hz.GetMaximum()*0.5,
    #                cut[1], 0, 0.02, '>')
    # line1.Draw()
    # line2.Draw()
    # tex.DrawLatexNDC(0.23, 0.83, '(a)')
    # c1.Print(fig_file)
    '''vtx'''
    hvx.SetXTitle('x-vertex [mm]')
    hvx.SetYTitle('Counts [/mm]')
    hvx.Draw()
    cut = [-50, 50]
    line1 = TArrow(cut[0], hvx.GetMaximum()*0.5, cut[0], 0, 0.02, '>')
    line2 = TArrow(cut[1], hvx.GetMaximum()*0.5, cut[1], 0, 0.02, '>')
    line1.Draw()
    line2.Draw()
    cut = [-25, 25]
    line3 = TArrow(cut[0], hvx.GetMaximum(), cut[0], 0, 0.02, '')
    line4 = TArrow(cut[1], hvx.GetMaximum(), cut[1], 0, 0.02, '')
    # line3.SetLineWidth(2)
    # line4.SetLineWidth(2)
    line3.SetLineStyle(7)
    line4.SetLineStyle(7)
    line3.Draw()
    line4.Draw()
    tex.DrawLatexNDC(0.23, 0.83, '(a)')
    c1.Print('fig/dc/kk_vtx.ps')
    '''vty'''
    hvy.SetXTitle('y-vertex [mm]')
    hvy.SetYTitle('Counts [/mm]')
    hvy.Draw()
    cut = [-30, 30]
    line1 = TArrow(cut[0], hvy.GetMaximum()*0.5, cut[0], 0, 0.02, '>')
    line2 = TArrow(cut[1], hvy.GetMaximum()*0.5, cut[1], 0, 0.02, '>')
    line1.SetLineWidth(2)
    line2.SetLineWidth(2)
    line1.Draw()
    line2.Draw()
    cut = [-15, 15]
    line3 = TArrow(cut[0], hvy.GetMaximum(), cut[0], 0, 0.02, '')
    line4 = TArrow(cut[1], hvy.GetMaximum(), cut[1], 0, 0.02, '')
    line3.SetLineStyle(2)
    line4.SetLineStyle(2)
    line3.Draw()
    line4.Draw()
    tex.DrawLatexNDC(0.23, 0.83, '(b)')
    c1.Print('fig/dc/kk_vty.ps')
    '''vtz'''
    hvz.SetXTitle('z-vertex [mm]')
    hvz.SetYTitle('Counts [/2 mm]')
    hvz.Draw()
    cut = [-80, 80]
    line1 = TArrow(cut[0], hvz.GetMaximum()*0.5, cut[0], 0, 0.02, '>')
    line2 = TArrow(cut[1], hvz.GetMaximum()*0.5, cut[1], 0, 0.02, '>')
    line1.Draw()
    line2.Draw()
    cut = [-25, 25]
    line3 = TArrow(cut[0], hvz.GetMaximum(), cut[0], 0, 0.02, '')
    line4 = TArrow(cut[1], hvz.GetMaximum(), cut[1], 0, 0.02, '')
    line3.SetLineStyle(2)
    line4.SetLineStyle(2)
    line3.Draw()
    line4.Draw()
    tex.DrawLatexNDC(0.23, 0.83, '(c)')
    c1.Print('fig/dc/kk_vtz.ps')
    '''close'''
    hcd.SetXTitle('Closest distance [mm]')
    hcd.SetYTitle('Counts [/0.1 mm]')
    hcd.Draw()
    cut = 10
    line = TArrow(cut, hcd.GetMaximum()*0.5, cut, 0, 0.02, '>')
    line.Draw()
    tex.DrawLatexNDC(0.23, 0.83, '(d)')
    c1.Print('fig/dc/kk_close.ps')
    hmm.Draw()
    hth.Draw()
    hthz.Draw('col')
    c1.Print('fig/dc/kk_mm.ps')
    f1 = TFile('kk.root', 'recreate')
    f1.Add(hxy)
    f1.Add(hzt)
    f1.Add(hvx)
    f1.Add(hvy)
    f1.Add(hvz)
    f1.Add(hcd)
    f1.Add(hmm)
    f1.Add(hmmw)
    f1.Add(hth)
    f1.Add(hthz)
    f1.Write()
    f1.Close()
  else:
    f1 = TFile('kk.root')
    c1 = TCanvas()
    for n in ['xy', 'zt', 'vx', 'vy', 'vz', 'cd', 'mm', 'th', 'thz']:
      hname = 'h' + n
      h = f1.Get(hname)
      h.Draw()
      cut = ([[-50, 50], [-25, 25]] if n == 'vx' else
             [[-30, 30], [-15, 15]] if n == 'vy' else
             [[-80, 80], [-15, 15]] if n == 'vz' else
             [[10]] if n == 'cd' else
             None)
      label = ('(a)' if n == 'vx' else
               '(b)' if n == 'vy' else
               '(c)' if n == 'vz' else
               '(d)' if n == 'cd' else
               None)
      if cut is not None:
        tex.DrawLatexNDC(0.23, 0.83, label)
        draw_cut_line(h, cut[0])
        if n != 'cd':
          line3 = TArrow(cut[1][0], h.GetMaximum(), cut[1][0], 0, 0.02, '')
          line4 = TArrow(cut[1][1], h.GetMaximum(), cut[1][1], 0, 0.02, '')
          line3.SetLineStyle(7)
          line4.SetLineStyle(7)
          line3.Draw()
          line4.Draw()
      fig_name = 'fig/dc/kk_{}.ps'.format(n.replace('v', 'vt').replace('cd', 'close'))
      print(hname, fig_name)
      c1.Print(fig_name)
  print('done')
