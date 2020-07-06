// -*- C++ -*-

#include <iostream>
#include <fstream>

#include <TApplication.h>
#include <TCanvas.h>
#include <TCut.h>
#include <TF1.h>
#include <TFile.h>
#include <TH1.h>
#include <TROOT.h>
#include <TString.h>
#include <TStyle.h>
#include <TText.h>
#include <TTimeStamp.h>
#include <TTree.h>

#include "DetectorID.hh"
#include "Utility.hh"

namespace
{
  enum eParticle { kPion, kKaon, nParticle };
}

//_____________________________________________________________________________
void
TFitBH1( void )
{
  std::cout << "Usage: TFitBH1.C(Int_t run_number)" << std::endl;
  gApplication->Terminate();
}

//_____________________________________________________________________________
void
TFitBH1( const Int_t run_number, Int_t p=kKaon )
{
  gROOT->Reset();
  gStyle->SetOptStat(1110);
  gStyle->SetOptFit();
  gStyle->SetStatX(.90);
  gStyle->SetStatY(.90);
  gStyle->SetStatW(.20);
  gStyle->SetStatH(.20);
  // Configuration
  const Int_t canvas_x = 1200, canvas_y = 800;
  const Int_t hmin = 300000, hmax = 500000;
  const Int_t hbin = ( hmax - hmin ) / 10;
  const Int_t width = 3000;
  const TString ana_type   = "Hodoscope";
  const TString ana_dir    = Form( "%s/k18analyzer/pro", std::getenv("HOME") );
  const TString root_dir   = Form( "%s/root/all", ana_dir.Data() );
  const TString param_dir  = Form( "%s/param/HDPRM", ana_dir.Data() );
  const TString param_file = Form( "%s/HodoParam_%05d",
				   param_dir.Data(), run_number );
  const TString fig_dir    = Form( "%s/fig/tune", ana_dir.Data() );
  const TString fig_file   = Form( "%s_%05d.pdf", __func__, run_number );
  const TString root_file  = Form( "run%05d_%s.root",
				   run_number, ana_type.Data() );
  TFile* file = new TFile( Form("%s/%s", root_dir.Data(), root_file.Data()) );
  TTree* tree = dynamic_cast<TTree*>( file->Get("tree") );
  const TString outname = Form( "%s/macro/output/tune/%s_%05d",
				ana_dir.Data(), __func__, run_number );
  std::ifstream infile( param_file );
  std::ofstream outfile( outname );
  std::cout << TString('=', 80) << std::endl
	    << "run_num    = " << run_number << std::endl
	    << "ana_type   = " << ana_type   << std::endl
	    << "ana_dir    = " << ana_dir    << std::endl
	    << "root_dir   = " << root_dir   << std::endl
	    << "root_file  = " << root_file  << std::endl
	    << "param_dir  = " << param_dir  << std::endl
	    << "param_file = " << param_file << std::endl
	    << "out_file   = " << outname    << std::endl
	    << "fig_dir    = " << fig_dir    << std::endl
	    << "fig_file   = " << fig_file   << std::endl
	    << TString('=', 80) << std::endl;
  enum e_AorT { kADC, kTDC,  kAorT };
  enum e_UorD { kUP,  kDOWN, kUorD };
  TString ud_str[kUorD]      = { "U", "D" };
  TString branch_name[kUorD] = { "bh1ut", "bh1dt" };
  TH1* h[kUorD][NumOfSegBH1];
  TF1* f[kUorD][NumOfSegBH1];
  for( Int_t ud=0; ud<kUorD; ++ud ){
    for( Int_t i=0; i<NumOfSegBH1; ++i ){
      h[ud][i] = new TH1D( Form( "%s_%d", branch_name[ud].Data(), i+1 ),
			   Form( "BH1 TDC %d%s", i+1, ud_str[ud].Data() ),
			   hbin, hmin, hmax );
    }
  }
  // Event loop
  const UInt_t MaxDepth = 16;
  Int_t    bh1nhits;
  Double_t bh1ut[NumOfSegBH1][MaxDepth];
  Double_t bh1dt[NumOfSegBH1][MaxDepth];
  tree->SetBranchAddress( "bh1nhits", &bh1nhits );
  tree->SetBranchAddress( "bh1ut", bh1ut );
  tree->SetBranchAddress( "bh1dt", bh1dt );
  tree->SetBranchStatus( "*", false );
  tree->SetBranchStatus( "bh1nhits", true );
  tree->SetBranchStatus( "bh1ut", true );
  tree->SetBranchStatus( "bh1dt", true );
  TCut cut1;
  for( UInt_t iev=0, nev=tree->GetEntries(); iev<nev; ++iev ){
    if( iev%10000 == 0 )
      std::cout << "Event number = " << iev << std::endl;
    tree->GetEntry( iev );
    for( UInt_t i=0; i<NumOfSegBH1; ++i ){
      // if( i==0 || i==1 || i==9 || i==10 ){
      // 	if( p==kPion ){
      // 	  cut1 += "trigflag[17]>0 && trigflag[13]>0";
      // 	  cut1 += "bact[0]>600 && bact[1]>600 && bh1nhits>0";
      // 	} else {
      // 	  cut1 += "bact[0]<=0 && bact[1]<=0 && bh1nhits==1";
      // 	}
      // } else {
      // 	if ( p==kPion ){
      // 	  cut1 += "trigflag[17]>0 && trigflag[13]>0";
      // 	  cut1 += "bact[0]>600 && bact[1]>600 && bh1nhits==1";
      // 	} else {
      // 	  cut1 += "bact[0]<=0 && bact[1]<=0 && bh1nhits==1";
      // 	}
      // }
      for( UInt_t m=0; m<MaxDepth; ++m ){
	if( bh1ut[i][m] > 0 )
	  h[kUP][i]->Fill( bh1ut[i][m] );
	if( bh1dt[i][m] > 0 )
	  h[kDOWN][i]->Fill( bh1dt[i][m] );
      }
    }
  }
  // Fitting
  TCanvas* c1 = new TCanvas( "c1","c1", canvas_x, canvas_y );
  c1->Divide(6, 4);
  std::cout << "- Start Fitting BH1 TDC" << std::endl;
  Bool_t   fit_ok[kUorD][NumOfSegBH1];
  Double_t param0[kUorD][NumOfSegBH1];
  Double_t param1[kUorD][NumOfSegBH1];
  for( Int_t ud=0; ud<kUorD; ++ud ){
    std::cout << "Seg\tMean\tSigma" << std::endl;
    for( Int_t i=0; i<NumOfSegBH1; ++i ){
      c1->cd( i + ud*(NumOfSegBH1+1) + 1 );
      if( h[ud][i]->Integral()==0 ) continue;
      TString fname = Form("fit_%s_%d", branch_name[ud].Data(), i);
      f[ud][i] = new TF1( fname, "gaus" );
      Double_t center = h[ud][i]->GetBinCenter( h[ud][i]->GetMaximumBin() );
      h[ud][i]->Fit( fname, "RQ", "", center-width, center+width );
      Double_t Const  = f[ud][i]->GetParameter(0);
      Double_t Mean   = f[ud][i]->GetParameter(1);
      Double_t Sigma  = f[ud][i]->GetParameter(2);
      for( Int_t ifit=0; ifit<3; ++ifit ){
	h[ud][i]->Fit( fname, "RQ", "", Mean-Sigma*2, Mean+Sigma*2 );
	Const  = f[ud][i]->GetParameter(0);
	Mean   = f[ud][i]->GetParameter(1);
	Sigma  = f[ud][i]->GetParameter(2);
      }
      param0[ud][i] = Mean;
      //param1[ud][i] = 0.035;
      fit_ok[ud][i] = ( Sigma < 5000. && h[ud][i]->Integral()>200 );
      // if( nentries<1e4 ) fit_ok[ud][i] = false;
      // if( nentries<1e5 ) fit_ok[ud][i] = false;
      TString str = fit_ok[ud][i] ? "OK" : "NG";
      Color_t col = fit_ok[ud][i] ? kBlue+1 : kRed+1;
      TText *t = NewTText();
      t->SetTextColor(col);
      t->DrawText( 0.640, 0.360, str );
      std::cout << std::setw(2) << i << ud_str[ud] << "\t"
		<< Mean << "\t" << Sigma << std::endl;
      h[ud][i]->GetXaxis()->SetRangeUser(Mean-10*Sigma, Mean+16*Sigma);
      c1->Update();
    }
  }
  c1->Print(Form("%s/%s", fig_dir.Data(), fig_file.Data()));
  // Make HodoParam
  TString line;
  if( !infile.is_open() ){
    std::cerr<<param_file<<" cannot open !"<<std::endl;
  }
  while( infile.good() && line.ReadLine(infile) ){
    //if(line[0]=='#'||line[0]==0) continue;
    Int_t    cid, plane, seg, at, ud;
    Double_t p0, p1, cp0, cp1;
    Char_t   buf1[1024];
    Char_t   buf2[1024];
    Char_t   buf3[1024];
    auto np = std::sscanf( line.Data(), "%d %d %d %d %d %lf %lf",
			   &cid, &plane, &seg, &at, &ud, &p0, &p1 );
    auto nc = std::sscanf( line.Data(), "%s %s %s",
			   buf1, buf2, buf3 );
    if( np == 7 && cid == DetIdBH1 && at == kTDC ){
      TString ok;
      if( fit_ok[ud][seg] && param0[ud][seg]!=0 ){
	cp0 = param0[ud][seg];
	ok = "";
      } else {
	cp0 = p0;
	ok = "*";
      }
      cp1 = p1;
      TString buf = Form( "%d\t%d\t%d\t%d\t%d\t%.3f\t%.10f",
			  cid, plane, seg, at, ud, cp0, cp1 );
      std::cout << buf << "\t" << ok << std::endl;
      outfile << buf << std::endl;
    } else if( np == 7
	       && ( cid == DetIdCFT || cid == DetIdBGO || cid == DetIdPiID ) ){
      ;
    } else if( nc == 3 && TString( buf2 ).Contains("file:") ){
      outfile << Form( "#  file: HodoParam_%05d\n", run_number );
    } else if( nc == 3 && TString( buf2 ).Contains("date:") ){
      outfile << Form( "#  date: %s\n", TTimeStamp().AsString("s") );
    } else if( nc == 3 && TString( buf2 ).Contains("note:") ){
      outfile << line << std::endl
	      << "#        " << __func__ << " ... done" << std::endl;
    } else if( nc == 3 && TString( buf2 ).Contains(__func__) ){
      ;
    } else {
      outfile << line << std::endl;
    }
  }
}
