#!/usr/bin/env python2

from __future__ import print_function

import argparse
import datetime
import numpy
import os
import ROOT

work_dir = '.'
#epics_dir = 'epics'
epics_dir = '/group/had/sks/E40/JPARC2020Feb/E40SubData2020Feb/epics_2020feb'
#epics_dir = '/group/had/sks/E07/KURAMA2017Apr/epics_e07_2017'
#epics_dir = '/group/had/sks/E07/KURAMA2016Jun/epics_e07_2016'

data_dir = '/group/had/sks/E40/JPARC2020Feb/e40_2020feb'
#data_dir = '/group/had/sks/E07/KURAMA2017Jun/e07_2017'
#data_dir = '/group/had/sks/E07/KURAMA2016Apr/e07_2016'

magnet_name = [
  'KURAMA_Field', 'D4_Field',
  'D1', 'Q1', 'Q2', 'D2', 'Q3', 'O1', 'Q4', 'S1',
  'CM1', 'CM2', 'S2', 'Q5', 'Q6', 'D3', 'Q7', 'O2', 'S3',
  'CM3', 'CM4', 'S4', 'Q8', 'O3', 'Q9',
  'Q10', 'Q11', 'D4', 'D4s', 'Q12', 'Q13']

#______________________________________________________________________________
def make_magnet_param(run_number, skip_empty=True):
  ''' make magnet parameter '''
  output_file = os.path.join(work_dir, 'tool/MatrixMaker/K18MagnetParam',
                             'K18MagParam_{:05d}.txt'.format(run_number))
  recorder_log = os.path.join(data_dir, 'recorder.log')
  print('output_file =', output_file)
  print('recorder_log =', recorder_log)
  # Run Start/End Time
  month_start = None
  date_start = None
  hms_start = None
  year_start = None
  month_end = None
  date_end = None
  hms_end = None
  year_end = None
  with open(recorder_log, 'r') as f:
    for line in f.readlines():
      column = line.split()
      if (len(column) != 20 or
          column[0] != 'RUN' or
          int(column[1]) != run_number):
        continue
      print(line)
      month_start = column[4]
      date_start = int(column[5])
      hms_start = column[6]
      year_start = int(column[7])
      month_end = column[10]
      date_end = int(column[11])
      hms_end = column[12]
      year_end = int(column[13])
  if (month_start is None or hms_start is None or
      month_end is None or hms_end is None):
    return
  start = '{}-{}-{} {}'.format(year_start, month_start, date_start, hms_start)
  end = '{}-{}-{} {}'.format(year_end, month_end, date_end, hms_end)
  rec_start = datetime.datetime.strptime(start, '%Y-%b-%d %H:%M:%S')
  rec_end = datetime.datetime.strptime(end, '%Y-%b-%d %H:%M:%S')
  # Epics
  magnet_val = [[] for x in magnet_name]
  for ir, e in enumerate(sorted(os.listdir(epics_dir))):
    if '.root' not in e:
      continue
    epics_end = datetime.datetime.strptime(e[9:24], '%Y%m%d_%H%M%S')
    epics_start = epics_end - datetime.timedelta(hours=4)
    if rec_start > epics_end or rec_end < epics_start:
      continue
    tfile = ROOT.TFile.Open(os.path.join(epics_dir, e))
    tree = tfile.Get('tree')
    tree.SetBranchStatus('*', False)
    tree.SetBranchStatus('HDDAQ_RUNNUMBER', True)
    tree.SetBranchStatus('KURAMA_Field', True)
    tree.SetBranchStatus('D4_Field', True)
    tree.SetBranchStatus('ALine_K18D1_CMON', True)
    tree.SetBranchStatus('K18_Q1_CMON', True)
    tree.SetBranchStatus('K18_Q2_CMON', True)
    tree.SetBranchStatus('K18_D2_CMON', True)
    tree.SetBranchStatus('K18_Q3_CMON', True)
    tree.SetBranchStatus('K18_O1_CMON', True)
    tree.SetBranchStatus('K18_Q4_CMON', True)
    tree.SetBranchStatus('K18_S1_CMON', True)
    tree.SetBranchStatus('K18_CM1_CMON', True)
    tree.SetBranchStatus('K18_CM2_CMON', True)
    tree.SetBranchStatus('K18_S2_CMON', True)
    tree.SetBranchStatus('K18_Q5_CMON', True)
    tree.SetBranchStatus('K18_Q6_CMON', True)
    tree.SetBranchStatus('K18_D3_CMON', True)
    tree.SetBranchStatus('K18_Q7_CMON', True)
    tree.SetBranchStatus('K18_O2_CMON', True)
    tree.SetBranchStatus('K18_S3_CMON', True)
    tree.SetBranchStatus('K18_CM3_CMON', True)
    tree.SetBranchStatus('K18_CM4_CMON', True)
    tree.SetBranchStatus('K18_S4_CMON', True)
    tree.SetBranchStatus('K18_Q8_CMON', True)
    tree.SetBranchStatus('K18_O3_CMON', True)
    tree.SetBranchStatus('K18_Q9_CMON', True)
    tree.SetBranchStatus('K18_Q10_CMON', True)
    tree.SetBranchStatus('K18_Q11_CMON', True)
    tree.SetBranchStatus('K18_D4_CMON', True)
    tree.SetBranchStatus('K18_D4s_CMON', True)
    tree.SetBranchStatus('K18_Q12_CMON', True)
    tree.SetBranchStatus('K18_Q13_CMON', True)
    n_entries = tree.GetEntries()
    for iev in range(n_entries):
      tree.GetEntry(iev)
      if int(tree.HDDAQ_RUNNUMBER) != run_number:
        continue
      val = []
      val.append(tree.KURAMA_Field)
      val.append(tree.D4_Field)
      val.append(tree.ALine_K18D1_CMON)
      val.append(tree.K18_Q1_CMON)
      val.append(tree.K18_Q2_CMON)
      val.append(tree.K18_D2_CMON)
      val.append(tree.K18_Q3_CMON)
      val.append(tree.K18_O1_CMON)
      val.append(tree.K18_Q4_CMON)
      val.append(tree.K18_S1_CMON)
      val.append(tree.K18_CM1_CMON)
      val.append(tree.K18_CM2_CMON)
      val.append(tree.K18_S2_CMON)
      val.append(tree.K18_Q5_CMON)
      val.append(tree.K18_Q6_CMON)
      val.append(tree.K18_D3_CMON)
      val.append(tree.K18_Q7_CMON)
      val.append(tree.K18_O2_CMON)
      val.append(tree.K18_S3_CMON)
      val.append(tree.K18_CM3_CMON)
      val.append(tree.K18_CM4_CMON)
      val.append(tree.K18_S4_CMON)
      val.append(tree.K18_Q8_CMON)
      val.append(tree.K18_O3_CMON)
      val.append(tree.K18_Q9_CMON)
      val.append(tree.K18_Q10_CMON)
      val.append(tree.K18_Q11_CMON)
      val.append(tree.K18_D4_CMON)
      val.append(tree.K18_D4s_CMON)
      val.append(tree.K18_Q12_CMON)
      val.append(tree.K18_Q13_CMON)
      for i, v in enumerate(val):
        if skip_empty and (v == -999999.999 or v == -999.9 or
                           (-0.0001 < v and v < 0.0001) ):
          continue
        # print(i, magnet_name[i], v)
        magnet_val[i].append(v)
  with open(output_file, 'w') as f:
    if len(magnet_val[1]) == 0:
      magnet_val[1].append(0)
    pK18 = 0.299792*numpy.mean(magnet_val[1])*4.;
    buf = '{:<20s}{:>13.8f}'.format('pK18', pK18)
    print(buf)
    f.write(buf + '\n')
    for i, m in enumerate(magnet_val):
      if len(m) == 0:
        m.append(0)
      buf = ('{:<20s}{:>13.8f}  {:>13.10f} {:3d}'
             .format(magnet_name[i], numpy.mean(m), numpy.std(m), len(m)))
      print(buf)
      f.write(buf + '\n')

#______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='run_number')
  parsed, unparsed = parser.parse_known_args()
  try:
    if parsed.run_number > 0:
      make_magnet_param(parsed.run_number)
    else:
      for i in range(8452, 8480):
        make_magnet_param(i)
  except KeyboardInterrupt as err:
    print(err)
