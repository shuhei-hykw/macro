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
TFitBAC( void )
{
  std::cout << "Usage: TFitBAC.C(Int_t run_number)" << std::endl;
  gApplication->Terminate();
}

//_____________________________________________________________________________
void
TFitBAC( const Int_t run_number, Int_t p=kKaon )
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
  const Int_t hmin = 200000, hmax = 400000;
  const Int_t hbin = ( hmax - hmin ) / 20;
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
  TString branch_name = "bact";
  TH1* h[NumOfSegBAC];
  TF1* f[NumOfSegBAC];
  for( Int_t i=0; i<NumOfSegBAC; ++i ){
    h[i] = new TH1D( Form( "%s_%d", branch_name.Data(), i+1 ),
		     Form( "BAC TDC %d", i+1 ),
		     hbin, hmin, hmax );
  }
  // Event loop
  const UInt_t MaxDepth = 16;
  Int_t    bacnhits;
  Double_t bact[NumOfSegBAC][MaxDepth];
  tree->SetBranchAddress( "bacnhits", &bacnhits );
  tree->SetBranchAddress( "bact", bact );
  tree->SetBranchStatus( "*", false );
  tree->SetBranchStatus( "bacnhits", true );
  tree->SetBranchStatus( "bact", true );
  TCut cut1;
  for( UInt_t iev=0, nev=tree->GetEntries(); iev<nev; ++iev ){
    if( iev%10000 == 0 )
      std::cout << "Event number = " << iev << std::endl;
    tree->GetEntry( iev );
    for( UInt_t i=0; i<NumOfSegBAC; ++i ){
      // if( i==0 || i==1 || i==9 || i==10 ){
      // 	if( p==kPion ){
      // 	  cut1 += "trigflag[17]>0 && trigflag[13]>0";
      // 	  cut1 += "bact[0]>600 && bact[1]>600 && bacnhits>0";
      // 	} else {
      // 	  cut1 += "bact[0]<=0 && bact[1]<=0 && bacnhits==1";
      // 	}
      // } else {
      // 	if ( p==kPion ){
      // 	  cut1 += "trigflag[17]>0 && trigflag[13]>0";
      // 	  cut1 += "bact[0]>600 && bact[1]>600 && bacnhits==1";
      // 	} else {
      // 	  cut1 += "bact[0]<=0 && bact[1]<=0 && bacnhits==1";
      // 	}
      // }
      for( UInt_t m=0; m<MaxDepth; ++m ){
	if( bact[i][m] > 0 ) h[i]->Fill( bact[i][m] );
      }
    }
  }
  // Fitting
  TCanvas* c1 = new TCanvas( "c1","c1", canvas_x, canvas_y );
  // c1->Divide(6, 4);
  std::cout << "- Start Fitting BAC TDC" << std::endl;
  Bool_t   fit_ok[NumOfSegBAC];
  Double_t param0[NumOfSegBAC];
  Double_t param1[NumOfSegBAC];
  std::cout << "Seg\tMean\tSigma" << std::endl;
  for( Int_t i=0; i<NumOfSegBAC; ++i ){
    c1->cd( i + 1 );
    if( h[i]->Integral()==0 ) continue;
    TString fname = Form("fit_%s_%d", branch_name.Data(), i);
    f[i] = new TF1( fname, "gaus" );
    Double_t center = h[i]->GetBinCenter( h[i]->GetMaximumBin() );
    h[i]->Fit( fname, "RQ", "", center-width, center+width );
    Double_t Const  = f[i]->GetParameter(0);
    Double_t Mean   = f[i]->GetParameter(1);
    Double_t Sigma  = f[i]->GetParameter(2);
    for( Int_t ifit=0; ifit<3; ++ifit ){
      h[i]->Fit( fname, "RQ", "", Mean-Sigma*2, Mean+Sigma*2 );
      Const  = f[i]->GetParameter(0);
      Mean   = f[i]->GetParameter(1);
      Sigma  = f[i]->GetParameter(2);
    }
    param0[i] = Mean;
    fit_ok[i] = ( Sigma < 5000. && h[i]->Integral()>200 );
    // if( nentries<1e4 ) fit_ok[i] = false;
    // if( nentries<1e5 ) fit_ok[i] = false;
    TString str = fit_ok[i] ? "OK" : "NG";
    Color_t col = fit_ok[i] ? kBlue+1 : kRed+1;
    TText *t = NewTText();
    t->SetTextColor(col);
    t->DrawText( 0.640, 0.360, str );
    std::cout << std::setw(2) << i << "\t"
	      << Mean << "\t" << Sigma << std::endl;
    h[i]->GetXaxis()->SetRangeUser(Mean-10*Sigma, Mean+16*Sigma);
    c1->Update();
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
    if( np == 7 && cid == DetIdBAC && at == kTDC ){
      TString ok;
      if( fit_ok[seg] && param0[seg]!=0 ){
	cp0 = param0[seg];
	ok = "";
      } else {
	cp0 = p0;
	ok = "*";
      }
      // cp1 = p1;
      cp1 = -0.0009390020;
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
      TTimeStamp s;
      s.Add( -TTimeStamp::GetZoneOffset() );
      outfile << Form( "#  date: %s\n", s.AsString("s") );
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
