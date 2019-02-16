#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import EnvManager
import ROOT
from ROOT import (gROOT, gStyle, kRed, kBlue,
                  TCanvas, TCut, TFile, TH2F, TLatex, TLine)

draw_line = True

#_______________________________________________________________________________
if __name__ == '__main__':
  # gROOT.Reset()
  gROOT.SetBatch()
  # gStyle.SetPalette(52) # grayscale
  # ROOT.TColor.InvertPalette()
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  fig_file = EnvManager.fig_dir + '/dc/matrix.pdf'
  if parsed.run_number < 1000:
    root_file = 'HUL_{0:05d}.root'.format(parsed.run_number)
    f1 = TFile.Open(EnvManager.root_dir + '/' + root_file)
    t1 = f1.Get('hul')
  else:
    kk_file = 'DstKKAna_{0:05d}.root'.format(parsed.run_number)
    ea0c_file = 'Easiroc_{0:05d}.root'.format(parsed.run_number)
    f1 = TFile.Open(EnvManager.root_dir + '/' + kk_file)
    f2 = TFile.Open(EnvManager.root_dir + '/' + ea0c_file)
    t1 = f1.Get('kk')
    t2 = f2.Get('ea0c')
    t1.AddFriend( t2 )
  c1 = TCanvas('c1', 'c1')
  h = TH2F('h', 'h', 64, 0, 64, 24, 0, 24)
  h2d = TH2F('h2d', 'h2d', 64, 1, 65, 24, 1, 25)
  h3d = TH2F('h3d', 'h3d', 64, 1, 65, 24, 1, 25)
  matrix2d_param = EnvManager.param_dir + '/MATRIX/matrix2d_pattern_20170418.txt'
  matrix3d_param = EnvManager.param_dir + '/MATRIX/matrix3d_pattern_veto_20170418.txt'
  #matrix_param = EnvManager.param_dir + '/MATRIX/matrix3d_pattern_veto_20170412.txt'
  target_fbh = 8
  with open(matrix2d_param, 'r') as f:
    matrix2d = []
    element = []
    for line in f:
      c = line.split()
      if len(c) != 2 or '#' in c[0]: continue
      element.append(int(c[1]))
      h2d.Fill(len(element), len(matrix2d)+1, int(c[1]))
      if c[0] == 'CH63':
        matrix2d.append(element)
        print(element)
        element = []
  h2d.SetLineColor(2)
  # h2d.Draw('box')
  with open(matrix3d_param, 'r') as f:
    matrix3d = []
    element = []
    for line in f:
      c = line.split()
      if len(c) != 2: continue
      fbh = int(target_fbh*2 + 1)
      element.append(float(c[1][fbh]))
      # h.Fill(len(element), len(matrix3d), float(c[1][fbh]))
      if c[0] == 'CH63':
        matrix3d.append(element)
        element = []
  if parsed.run_number < 1000:
    for i in xrange(t1.GetEntries()):
      # if i == 100000: break
      t1.GetEntry(i)
      if t1.trigflag[7] <= 0: continue
      # if t1.hultof_nhits != 1: continue
      # if t1.hulsch_nhits != 1: continue
      for itof in xrange(t1.hultof_nhits):
        for isch in xrange(t1.hulsch_nhits):
          h.Fill(t1.hulsch_hitpat[isch]-1, t1.hultof_hitpat[itof]-1)
    #t1.Project('h', 'hul.hultof_hitpat-1:hul.hulsch_hitpat-1')
  else:
    for i in range(t1.GetEntries()):
      # if i == 1000: break
      if i%10000 == 0:
        print(i, t1.GetEntries())
      t1.GetEntry(i)
      if t1.trigflag[7] <= 0: continue
      for itof in xrange(t1.nhTof):
        for isch in xrange(t1.sch_nhits):
          h.Fill(t1.sch_hitpat[isch], t1.TofSeg[itof]-1)
    #t1.Project('h', 'kk.TofSeg[0]-1:ea0c.sch_hitpat[0]')
  # t1.Project('h', 'kk.TofSeg[0]:ea0c.sch_hitpat[0]',
  #            'kk.trigflag[5]>0 && ea0c.fbh_hitpat[0]=={}'.format(int(target_fbh)))
  h.SetXTitle('SCH segment')
  h.SetYTitle('TOF segment')
  # h.SetZTitle('Counts')
  #h.Draw('box')
  h.Draw('colz')
  line2d = TLine()
  line2d.SetLineColor(kRed+1)
  line2d.SetLineWidth(4)
  line3d = TLine()
  line3d.SetLineColor(kBlue+1)
  line3d.SetLineWidth(4)
  if draw_line:
    for i in range(24):
      left2d = -1
      right2d = -1
      for j in range(64):
        if left2d < 0 and matrix2d[i][j] > 0:
          left2d = j
        if left2d > 0 and right2d < 0 and matrix2d[i][j] == 0:
          right2d = j
      line2d.DrawLine(left2d, i, left2d, i+1)
      line2d.DrawLine(right2d, i, right2d, i+1)
      for j in range(64):
        if j > 0 and matrix3d[i][j-1] != matrix3d[i][j]:
          line3d.DrawLine(j, i, j, i+1)
    for i in range(64):
      up2d = -1
      down2d = -1
      for j in range(24):
        if down2d < 0 and matrix2d[j][i] > 0:
          down2d = j
        if down2d >= 0 and up2d < 0 and matrix2d[j][i] == 0:
          up2d = j
      if up2d < 0 and down2d > 0: up2d = 24
      if up2d >= 0:
        line2d.DrawLine(i, up2d, i+1, up2d)
      if down2d >= 0:
        line2d.DrawLine(i, down2d, i+1, down2d)
      up3d = -1
      down3d = -1
      for j in range(24):
        if down3d * matrix3d[j][i] < 0:
          down3d = j
        if down3d >= 0 and up3d < 0 and matrix3d[j][i] == 0:
          up3d = j
      if up3d < 0 and down3d > 0: up3d = 24
      if up3d >= 0:
        line3d.DrawLine(i, up3d, i+1, up3d)
      if down3d >= 0:
        line3d.DrawLine(i, down3d, i+1, down3d)
  c1.SetLogz()
  c1.Print(fig_file)
  print('done')
