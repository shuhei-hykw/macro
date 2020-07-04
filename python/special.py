#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gROOT, gStyle, kRed, kBlue, kGray, TArrow,
                  TCanvas, TCut, TEllipse,
                  TF1, TFile, TGraph, TH1F, TH2F,
                  TLatex, TLine,
                  TMath, TPad, TTree)

draw_line = True
#xi->Scan("pKn:pKp:m2Kp+0.02:MissMass:MissP:chisqrKurama:resAngle:MeanDeXi:thetaXi:SSD2Flag", "runnum==2559&&evnum==535843", "")
target_line = [None, None]
#_______________________________________________________________________________
def draw_target_size(h, size):
  global target_line
  target_line[0] = TArrow(size[0], h.GetMaximum(),
                          size[0], 0, 0.02, '')
  target_line[1] = TArrow(size[1], h.GetMaximum(),
                          size[1], 0, 0.02, '')
  target_line[0].SetLineStyle(2)
  target_line[1].SetLineStyle(2)
  target_line[0].Draw()
  target_line[1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.SetBatch()
  root_file = 'root/v13/DstXiAna_All.root'
  # root_file = 'root/dc/DstXiAna_All.root'
  f1 = TFile.Open(root_file)
  t1 = f1.Get('xi')
  #t1.Scan("*", "runnum==2559&&evnum==535843", "")
  # t1.Scan("pKn:pKp:m2Kp+0.02:MissMass:MissP:chisqrKurama:resAngle:MeanDeXi:thetaXi:SSD2Flag", "runnum==2559&&evnum==535843", "")
  t1.Show(67462)
