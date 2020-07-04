#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy
import run_number

import ROOT

#_______________________________________________________________________________
if __name__ == '__main__':
  ROOT.gROOT.SetBatch()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  #   //////////////////// Configuration
  #   // for 2015
  #   // const Double_t zEmulsion = 1178.;
  #   // const Double_t zSSD2     = 1200.;
  #   // for 2016
  #   // const Double_t zEmulsion = 1897.50; // from VO
  #   // for 2017
  zEmulsion = -1041.215 #; // from KURAMA
  ana_type  = "SsdTracking"
  #   const Int_t canvas_x = 800, canvas_y = 600;
  #   const Int_t NbinTheta = 200, NbinDe = 200;
  MinX = -30.
  MaxX =  30.
  NbinX = int(MaxX - MinX)
  MinY = -30.
  MaxY =  30.
  NbinY = int(MaxY - MinY)
  MinU = -0.8
  MaxU =  0.8
  NbinU = int(MaxU - MinU)
  MinV = -0.8
  MaxV =  0.8
  NbinV = int(MaxV - MinV)
  MinTheta = 0.
  MaxTheta = 90.
  NbinTheta = int(MaxTheta - MinTheta)*10
  MinDe    = 0.
  MaxDe    = 4.0e4
  NbinDe = int(MaxDe - MinDe)/100
  root_file = 'root/all/SsdTracking_{:05d}.root'.format(parsed.run_number)
  f1 = ROOT.TFile.Open(root_file)
  t1 = f1.Get('ssd');
  hxy = ROOT.TH2F('hxy', 'Emulsion XY',
	          NbinX, MinX, MaxX, NbinY, MinY, MaxY)
  hxy.SetXTitle("Horizontal position [mm]")
  hxy.SetYTitle("Vertical position [mm]")
  hnt1 = ROOT.TH1F('hnt1', 'ntrack [Raw]', 1000, 0, 1000)
  hnt2 = ROOT.TH1F('hnt2', 'ntrack [Cut]', 1000, 0, 1000)
  htheta = ROOT.TH1F('htheta', 'Theta',
                     NbinTheta, MinTheta, MaxTheta)
  hde = ROOT.TH1F('hde', 'dE',
                  NbinDe, MinDe, MaxDe)
  htde = ROOT.TH2F('htde', 'dE%Theta',
	           NbinTheta, MinTheta, MaxTheta,
                   NbinDe, MinDe, MaxDe)
  #   TH2F *huv = new TH2F("huv", "UV Emulsion", NbinU, MinU, MaxU, NbinV, MinV, MaxV);
  #   TH2F *hxu = new TH2F("hxu", "XU Emulsion", NbinX, MinX, MaxX, NbinU, MinU, MaxU);
  #   TH2F *hyv = new TH2F("hyv", "YV Emulsion", NbinY, MinY, MaxY, NbinV, MinV, MaxV);

  #   TH2F *h_theta_de = new TH2F("h_theta_de", "Theta%dE Emulsion",
  # 			      NbinTheta, MinTheta, MaxTheta, NbinDe, MinDe, MaxDe);

  #   htrack->SetLineColor(kBlue);

  #   const Int_t NumOfSegTrig =   32;
  #   const Int_t MaxHits      = 1000;
  #   const Int_t NumOfLayer   =    4;
  #   const Int_t NumOfSegSSD  = 1536;
  #   std::vector<Double_t> vxpos;
  #   std::vector<Double_t> vypos;

  #   ofs << "#\n# " << emul_file << "\n#\n";
  #   ofs << "# Event\tTrack\tdxdz\tdydz\tx\ty\txEM\tyEM\tE0\tE1\tE2\tE3" << std::endl;
  t1.SetBranchStatus('*', 0)
  t1.SetBranchStatus('ntPbar', 1)
  t1.SetBranchStatus('x0Pbar', 1)
  t1.SetBranchStatus('y0Pbar', 1)
  t1.SetBranchStatus('u0Pbar', 1)
  t1.SetBranchStatus('v0Pbar', 1)
  t1.SetBranchStatus('thetaPbar', 1)
  t1.SetBranchStatus('dePbar', 1)
  # t1.SetBranchStatus('xpos', 1)
  # t1.SetBranchStatus('ypos', 1)
  for ievent in range(t1.GetEntries()):
    t1.GetEntry(ievent)
    dePbar = numpy.reshape(t1.dePbar, (4, 1000))
    hnt1.Fill(t1.ntPbar)
    nt = 0
    for it in range(t1.ntPbar):
      x = t1.x0Pbar[it] + t1.u0Pbar[it] * zEmulsion
      y = t1.y0Pbar[it] + t1.v0Pbar[it] * zEmulsion
      u = t1.u0Pbar[it]
      v = t1.v0Pbar[it]
      theta = t1.thetaPbar[it];
      de = numpy.average([dePbar[0][it],
                          dePbar[1][it],
                          dePbar[2][it],
                          dePbar[3][it]])
      htheta.Fill(theta)
      hde.Fill(de)
      htde.Fill(theta, de)
      if theta > 75.:
        continue;
      nt += 1
      hxy.Fill(x, y)
    hnt2.Fill(nt)
  c1 = ROOT.TCanvas()
  print(hxy.GetEntries())
  hxy.Draw('colz')
  c1.Print('fig/dc/pbar_xy.ps')
  hnt1.GetXaxis().SetRangeUser(0, 10)
  hnt1.Draw()
  hnt2.SetLineColor(ROOT.kRed)
  hnt2.Draw('same')
  c1.Print('fig/dc/pbar_nt.ps')
#       hx->Fill( x );
#       hy->Fill( y );
#       hu->Fill( u );
#       hv->Fill( v );
#       hxy->Fill( x, y );
#       huv->Fill( u, v );
#       hxu->Fill( x, u );
#       hyv->Fill( y, v );

#       Double_t de =
# 	0.25*( dePbar[0][it]+dePbar[1][it]+dePbar[2][it]+dePbar[3][it] );
#       h_theta_de->Fill( theta, de );

#       ofs << std::fixed
# 	  << std::setprecision(3)
# 	  << i << "\t" << it << "\t"
# 	  << u << "\t" << v << "\t" << x << "\t" << y << "\t"
# 	  << xpos << "\t" << ypos << "\t"
# 	  << std::setprecision(1)
# 	  << dePbar[0][it] << "\t"
# 	  << dePbar[1][it] << "\t"
# 	  << dePbar[2][it] << "\t"
# 	  << dePbar[3][it] << std::endl;
#       ntrack++;

#     }
#     htrack->Fill( ntPbar );
#   }

#   {
#     Double_t x = TMath::Mean( vxpos.begin(), vxpos.end() );
#     Double_t y = TMath::Mean( vypos.begin(), vypos.end() );
#     TString pos;
#     if( x>0. && y>0. ) pos = "LU";
#     if( x<0. && y>0. ) pos = "RU";
#     if( x>0. && y<0. ) pos = "LD";
#     if( x<0. && y<0. ) pos = "RD";
#     hxy->SetTitle( Form( "Run# %05d  ( %.3lf, %.3lf ) "+pos, runnum, x, y ) );
#   }

#   {
#     c1->cd(1); hx->Draw();
#     c1->cd(2); hy->Draw();
#     c1->cd(3); hxy->Draw("colz");
#     c1->cd(4); hu->Draw();
#     c1->cd(5); hv->Draw();
#     c1->cd(6); huv->Draw("colz");
#     c1->cd(7); hxu->Draw("colz");
#     c1->cd(8); hyv->Draw("colz");
#     c1->cd(9); h_theta_de->Draw("colz");
#   }

#   c2->cd();
#   hxy->GetYaxis()->SetRangeUser( -30., 30. );
#   hxy->Draw("colz");

#   c2->Print( pic_dir+"/"+pic_file );
# }
