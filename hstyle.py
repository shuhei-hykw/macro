#!/usr/bin/env python
## -*- coding: utf-8 -*-

import ROOT

#_______________________________________________________________________________
def set_style(h, myfont=42):
  h.SetLineColor(1)
  h.SetLabelFont(myfont, 'xyz')
  h.SetTitleFont(myfont, 'xyz')
  h.SetLabelSize(0.045, 'xyz')
  h.SetTitleSize(0.055, 'xyz')
#  h.SetOptTitle(0)
#  h.SetOptStat(0)
