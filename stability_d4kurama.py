#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2016
#D4     : mean=1.50199e+00, rms=1.21513e-04, fluc.=8.09011e-05
#KURAMA : mean=7.62362e-01, rms=3.29230e-04, fluc.=4.31856e-04

# 2017
# D4     : mean=1.51077e+00, rms=1.60421e-04, fluc.=1.06185e-04
# KURAMA : mean=7.62203e-01, rms=2.43267e-04, fluc.=3.19163e-04

import argparse
import calendar
import datetime
import os
import sys
import time

import ROOT

import run_number

#_______________________________________________________________________________
months = {}
for i ,v in enumerate(calendar.month_abbr):
  months[v] = i

#_______________________________________________________________________________
def get_run_time(recorder_log, run_number):
  '''Get Run Start/End Time'''
  record = None
  with open(recorder_log, 'r') as f:
    for line in f:
      columns = line.split()
      if len(columns) > 1 and columns[1] == str(run_number):
        record = columns
        break
  if record is None:
    return None
  start = int('{}{:02d}{:02d}{}'.format(record[7], int(months[record[4]]),
                                    int(record[5]), record[6].replace(':', '')))
  stop = int('{}{:02d}{:02d}{}'.format(record[13], int(months[record[10]]),
                                   int(record[11]), record[12].replace(':', '')))
  return [start, stop]

#_______________________________________________________________________________
def get_epics_data(root_dir, run_time):
  file_list = []
  data_list = []
  for r in sorted(os.listdir(root_dir)):
    root_file = os.path.join(root_dir, r)
    if not '.root' in r:
      continue
    r = r.replace('k18epics', '')
    r = r.replace('.root', '')
    r = int(r.replace('_', ''))
    if run_time[0] < r:
      file_list.append(root_file)
      if run_time[1] < r:
        break
  print(run_time)
  for r in file_list:
    f1 = ROOT.TFile.Open(r)
    tree = f1.Get("tree");
    nentries = tree.GetEntries()
    for i in range(nentries):
      tree.GetEntry(i);
      unixtime = tree.UnixTime - 4*3600
      stamp = datetime.datetime.fromtimestamp(unixtime)
      datatime = int('{}{:02d}{:02d}{:02d}{:02d}{:02d}'
                     .format(stamp.year, stamp.month, stamp.day,
                             stamp.hour, stamp.minute, stamp.second))
      if datatime < run_time[0] or run_time[1] < datatime:
        continue
      data_list.append([run_time, unixtime, tree.D4_Field, tree.KURAMA_Field])
  return data_list

#_______________________________________________________________________________
def show():
  c1 = ROOT.TCanvas('c1', 'c1', 1600, 600)
  c2 = ROOT.TCanvas('c2', 'c2', 1600, 600)
  c1.Divide(2, 1)
  c2.Divide(2, 1)
  tex = ROOT.TLatex()
  tex.SetNDC()
  tex.SetTextFont(132)
  tex.SetTextSize(0.1)
  for year in [2016, 2017]:
    root_dir = ('/group/had/sks/E07/KURAMA{}{}/epics_e07_{}'
                .format(year, 'Jun' if year == 2016 else 'Apr', year))
    data_dir = 'e07_{}'.format(year);
    recorder_log = os.path.join(data_dir, 'recorder.log')
    if not os.path.isfile(recorder_log):
      return
    if year == 2016:
      run_array = run_number.emulsion_2016
    else:
      run_array = run_number.emulsion_2017
    data_array = []
    for mod in run_array:
      for run in mod:
        run_time = get_run_time(recorder_log, run)
        epics_data = get_epics_data(root_dir, run_time)
        data_array.append(epics_data)
    if year == 2016:
      h1 = ROOT.TH2F('h1' + str(year), 'D4 Field',
                     250, 0, 250000,
                     50, 1.501, 1.503)
      h2 = ROOT.TH2F('h2' + str(year), 'Kurama Field',
                     250, 0, 250000,
                     50, 0.7618, 0.7638)
      h3 = ROOT.TH1F('h3' + str(year), 'D4 Field',
                     100, 1.501, 1.503)
      h4 = ROOT.TH1F('h4' + str(year), 'Kurama Field',
                     100, 0.760, 0.7640)
    else:
      h1 = ROOT.TH2F('h1' + str(year), 'D4 Field',
                     250, 0, 2000000,
                     50, 1.510, 1.512)
      h2 = ROOT.TH2F('h2' + str(year), 'Kurama Field',
                     250, 0, 2000000,
                     50, 0.7612, 0.7632)
      h3 = ROOT.TH1F('h3' + str(year), 'D4 Field',
                     100, 1.510, 1.512)
      h4 = ROOT.TH1F('h4' + str(year), 'Kurama Field',
                     100, 0.760, 0.7640)
    h1.GetXaxis().SetTitle('Run time [s]')
    h1.GetYaxis().SetTitle('Magnetic field [T]')
    h2.GetXaxis().SetTitle('Run time [s]')
    h2.GetYaxis().SetTitle('Magnetic field [T]')
    h3.GetXaxis().SetTitle('Magnetic field [T]')
    h4.GetXaxis().SetTitle('Magnetic field [T]')
    total_run_time = 0
    prev_time = 0
    for d in data_array:
      for p in d:
        if abs(p[2]) < 0.1:
          continue
        diff = p[1] - prev_time
        if diff > 60:
          diff = 0
        prev_time = p[1]
        total_run_time += diff
        h1.Fill(total_run_time, abs(p[2]))
        h2.Fill(total_run_time, abs(p[3]))
        h3.Fill(abs(p[2]))
        h4.Fill(abs(p[3]))
    if year == 2016:
      c1.cd(1)
      h1_2016 = h1.Clone()
      h1_2016.__class__ = ROOT.TH2F
      h1_2016.Draw('box')
      tex.DrawLatex(0.75, 0.75, '(a)')
      c2.cd(1)
      h2_2016 = h2.Clone()
      h2_2016.__class__ = ROOT.TH2F
      h2_2016.Draw('box')
      tex.DrawLatex(0.75, 0.75, '(a)')
    else:
      c1.cd(2)
      h1.Draw('box')
      tex.DrawLatex(0.75, 0.75, '(b)')
      c2.cd(2)
      h2.Draw('box')
      tex.DrawLatex(0.75, 0.75, '(b)')
    # h3.Draw()
    # print('D4     : mean={:.5e}, rms={:.5e}, fluc.={:.5e}'
    #       .format(h3.GetMean(), h3.GetRMS(), h3.GetRMS()/h3.GetMean()))
    # c1.Print('fig/dc/d4_{}.ps'.format(year))
    # h4.Draw()
    # print('KURAMA : mean={:.5e}, rms={:.5e}, fluc.={:.5e}'
    #       .format(h4.GetMean(), h4.GetRMS(), h4.GetRMS()/h4.GetMean()))
    # c1.Print('fig/dc/kurama_{}.ps'.format(year))
  c1.Print('fig/dc/d4_field.ps')
  c2.Print('fig/dc/kurama_field.ps')

#_______________________________________________________________________________
if __name__ == '__main__':
  ROOT.gROOT.SetBatch()
  try:
    show()
  except:
    print(sys.exc_info()[1])
