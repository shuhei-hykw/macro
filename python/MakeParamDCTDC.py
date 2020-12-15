#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import EnvManager

from ROOT import gROOT

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()

# // enum e_argv
# //   {
# //     k_process,
# //     k_ana_type,
# //     k_run_number,
# //     k_argc
# //   };

# // Config conf;

# // int LayerOffset;
# // int MinLayer;
# // int MaxLayer;
# // std::vector<int>    MaxWire;
# // std::vector<double> MaxDriftLength;
# // std::vector<double> MaxDriftTime;
# // std::vector<double> MaxFitDriftTime;
# // std::vector<double> XTFitOffset;
# // std::vector<double> FitWidth;

# // ///////////////////////////////////////////////////////////////////////
# // int
# // main( int argc, char **argv )
# // {

# //   gROOT->SetBatch(kTRUE);
# //   gErrorIgnoreLevel = kFatal; // suppress Print, Info, Warning and Error
# //   gStyle->SetOptStat(1111110);
# //   gStyle->SetStatW(.4);
# //   gStyle->SetStatH(.25);

# //   std::string process = basename( argv[k_process] );
# //   if( argc!=k_argc ){
# //     std::cout << "#D Usage: " << process
# // 	      << " [ana type]"
# // 	      << " [run number]"        << std::endl
# // 	      << "ana_type: 0) BcIn   " << std::endl
# // 	      << "          1) BcOut  " << std::endl
# // 	      << "          2) SdcIn  " << std::endl
# // 	      << "          3) SdcOut " << std::endl;
# //     return EXIT_FAILURE;
# //   }

# //   conf.run_number = std::strtol( argv[k_run_number], NULL, 0 );
# //   int i_ana_type  = std::strtol( argv[k_ana_type],   NULL, 0 );
# //   switch( i_ana_type ){
# //   case k_BcIn:   InitBcIn();   break;
# //   case k_BcOut:  InitBcOut();  break;
# //   case k_SdcIn:  InitSdcIn();  break;
# //   case k_SdcOut: InitSdcOut(); break;
# //   default: break;
# //   }

# //   //////////////////// Configuration
# //   conf.param_file = Form("%s/DCTDC/DCTdcCalib_%05d",
# // 			 conf.param_dir.Data(), conf.run_number);
# //   conf.pic_file   = Form("%s/dctdc/DCTdcCalib_%s_%05d.pdf",
# // 			 conf.pic_dir.Data(),
# // 			 conf.ana_type.Data(),
# // 			 conf.run_number);
# //   conf.root_file = Form("%s/%sTracking_%05d.root",
# // 			conf.root_dir.Data(),
# // 			conf.ana_type.Data(),
# // 			conf.run_number);
# //   conf.out_file  = Form("%s/dctdc/DCTdcCalib_%s_%05d",
# // 			conf.out_dir.Data(),
# // 			conf.ana_type.Data(),
# // 			conf.run_number);

# //   TFile *file = new TFile( conf.root_file );
# //   if(!file->IsOpen()){
# //     std::cout << Form("#E %s(): can't open root file: %s",
# // 		      __func__, basename( conf.root_file.Data() ) ) <<std::endl;
# //     return EXIT_FAILURE;
# //   }

# //   std::ifstream ifs( conf.param_file.Data() );
# //   if(!ifs.is_open()){
# //     std::cerr<<Form("#E %s(): can't open param file: %s",
# // 		    __func__, basename(conf.param_file.Data()))<<std::endl;
# //     return EXIT_FAILURE;
# //   }

# //   std::ofstream ofs(conf.out_file.Data());
# //   if(!ofs.is_open()) {
# //     std::cerr<<Form("#E %s(): can't open output file: %s",
# // 		    __func__, basename(conf.out_file.Data()))<<std::endl;
# //     return EXIT_FAILURE;
# //   }

# //   conf.Print();

# //   int x_devide = 4, y_devide = 4;
# //   //if(conf.ana_type=="SdcOut"){ x_devide = 6; y_devide = 6; }
# //   TCanvas *c1       = new TCanvas("c1", "c1", 1000, 1000);
# //   TF1     *fit_func = new TF1("fit_func", t0_func, 600, 700, 4);
# //   TLine    fit_line;
# //   fit_line.SetLineColor(kGreen);

# //   const int hist_id = 0;
# //   // 0 : raw TDC
# //   // 1000 : drift time before tracking
# //   // 5000 : drift time after tracking

# //   std::vector<double>         t0[MaxLayer-MinLayer+1];
# //   std::vector<std::string> fitok[MaxLayer-MinLayer+1];
# //   for(int layer=0; layer<MaxLayer-MinLayer+1; layer++){
# //     int plane = layer + LayerOffset;
# //     switch(layer){
# //     case  0: case  1: case  2: case  3: case  4: case  5:
# //     case  6: case  7: case  8: case  9: case 10: case 11:
# //       break;
# //     default:
# //       std::cerr<<Form("#E T0Fit%s(): invalid layer: %d",
# // 		      conf.ana_type.Data(), layer)<<std::endl;
# //       return EXIT_FAILURE;
# //     }
# //     double t0_init = t0_default[i_ana_type-1][layer];
# //     double t0_ave  = 0.;
# //     int n_fitok    = 0;
# //     //std::cout<<"WireId\t#event\tt0(fit)\tt0\tstatus"<<std::endl;
# //     for (int i=0; i<MaxWire[layer]; i++) {
# //       //std::cout<<Form("#D layer: %d  wire: %d", layer, i)<<std::endl;
# //       int pad = i%(x_devide*y_devide) +1;
# //       if( pad==1 ){
# // 	c1->Clear();
# // 	c1->Divide(x_devide, y_devide);
# //       }
# //       c1->cd(pad)->SetGrid();
# //       const TString& hist_name = Form("h%d", (layer+1)*10000 + hist_id + i+1);
# //       TH1F *h1 = (TH1F *)file->Get( hist_name );
# //       //h1->GetXaxis()->SetRangeUser( hmin, hmax );
# //       //h1->RebinX(4);
# //       double width = FitWidth[layer];
# //       if( i_ana_type==k_SdcOut )
# // 	h1->GetXaxis()->SetRangeUser( t0_init-width*2.2, t0_init+width*2.8 );
# //       else
# // 	h1->GetXaxis()->SetRangeUser( t0_init-width*1.2, t0_init+width*1.8 );

# //       h1->Draw();

# //       double t0_integral = h1->Integral( 0, hmax );
# //       double t0_mean     = t0_integral / 10.;

# //       fit_func->SetLineStyle(2);
# //       fit_func->SetParameter(0, t0_mean);
# //       fit_func->SetParameter(1, t0_init);
# //       fit_func->SetParameter(2, -1.); // TDC : -1, drift time : 1
# //       fit_func->SetParameter(3, 0.);
# //       if(t0_mean != 0){
# // 	h1->Fit("fit_func","Q","", t0_init-width , t0_init+width);
# //       }
# //       double mean    = fit_func->GetParameter(k_mean);
# //       double sigma   = fit_func->GetParameter(k_sigma);
# //       double e_mean  = fit_func->GetParError(k_mean);
# //       double e_sigma = fit_func->GetParError(k_sigma);
# //       double chi2    = fit_func->GetChisquare();
# //       int    fit_ev  = h1->Integral(t0_init-width, t0_init+width, "width");

# //       double e_t0 = 0.;
# //       if( true
# // 	  && abs(mean-t0_init)<max_diff_mean
# // 	  && e_mean<max_error_mean
# // 	  //&& fit_ev>min_event_num
# // 	  ){
# // 	if( i_ana_type==k_SdcOut )
# // 	  h1->GetXaxis()->SetRangeUser( mean-width*2.2, mean+width*2.8 );
# // 	else
# // 	  h1->GetXaxis()->SetRangeUser( mean-width*1.2, mean+width*1.8 );

# // 	t0[layer].push_back(mean);
# // 	e_t0 = e_mean;
# // 	fitok[layer].push_back("*");
# // 	fit_line.DrawLine(t0[layer][i], 0, t0[layer][i], h1->GetMaximum()*1.05);
# // 	//if(i>15&&i<48)
# // 	t0_ave += t0[layer][i];
# // 	n_fitok++;
# //       }else{
# // 	t0[layer].push_back(t0_init);
# // 	fitok[layer].push_back("");
# //       }

# //       TPaveText *pt = new TPaveText(0.5, 0.42, 0.88, 0.52, "NB NDC");
# //       pt->SetTextSize(0.07);
# //       pt->SetFillColor(0);
# //       pt->AddText(Form("%s%.2f(%.0f)",
# // 		       fitok[layer][i].c_str(), t0[layer][i], e_t0*pow(10.,2)));
# //       pt->Draw();

# //       // std::cout<<Form("%d\t%d\t%d\t%.2f\t%.2f",
# //       // 		      layer, i, fit_ev, mean, t0[layer][i])
# //       // 	       <<"\t"<<fitok[layer][i]<<std::endl;

# //       bool open_flag  = ( layer == 0 && i+1 == pad );
# //       bool close_flag = ( layer == MaxLayer-MinLayer && i+1 == MaxWire[layer] );
# //       if( pad==x_devide*y_devide ){
# // 	if( open_flag )
# // 	  c1->Print(Form("%s(", conf.pic_file.Data()));
# // 	else
# // 	  c1->Print(Form("%s", conf.pic_file.Data()));
# //       }
# //       if( close_flag )
# // 	c1->Print(Form("%s)", conf.pic_file.Data()));
# //     }//for(i)
# //     std::cout<<Form("#D %s(): layer#%02d ", __func__, layer+1)
# // 	     <<Form("fit ok = %d/%d\tt0 average = %.2f",
# // 		    n_fitok, MaxWire[layer], t0_ave/n_fitok)<<std::endl;
# //   }//for(layer)
# //   //////////////////// Make Param
# //   std::cout<<Form("#D %s(): create %s", __func__, conf.out_file.Data())<<std::endl;
# //   //std::cout<<"PlId\tWireId\tp1\tp0\tstatus"<<std::endl;
# //   std::string line;
# //   while( ifs.good() && std::getline(ifs,line) ){
# //     char buf[1024];
# //     int PlId, WireId;
# //     double p1, p0;
# //     if( line[0]=='#' || line.empty() ||
# // 	sscanf(line.c_str(), "%d\t%d\t%lf\t%lf", &PlId, &WireId, &p1, &p0) != 4 ){
# //       ofs<<line<<std::endl;
# //       continue;
# //     }
# //     double cp1 = p1;
# //     double cp0 = p0;
# //     ////////// BcOut
# //     switch(PlId){
# //     case 113: case 114: case 115: case 116: case 117: case 118:
# //     case 119: case 120: case 121: case 122: case 123: case 124:
# //       if(conf.ana_type!="BcOut"){
# // 	ofs<<line<<std::endl;
# // 	break;
# //       }
# //       cp0 = -1.*t0[PlId-LayerOffset][WireId-1]*cp1;
# //       sprintf(buf, "%d\t%d\t%.3f\t%.3f", PlId, WireId, cp1, cp0);
# //       //std::cout<<buf<<"\t"<<fitok[PlId-LayerOffset][WireId-1]<<std::endl;
# //       ofs<<buf<<std::endl;
# //       break;
# //     case 1: case 2: case 3: case 4: case 5: case 6:
# //       if(conf.ana_type!="SdcIn"){
# // 	ofs<<line<<std::endl;
# // 	break;
# //       }
# //       cp0 = -1.*t0[PlId-LayerOffset][WireId-1]*cp1;
# //       sprintf(buf, "%d\t%d\t%.3f\t%.3f", PlId, WireId, cp1, cp0);
# //       //std::cout<<buf<<"\t"<<fitok[PlId-LayerOffset][WireId-1]<<std::endl;
# //       ofs<<buf<<std::endl;
# //       break;
# //     case 31: case 32: case 33: case 34:
# //     case 35: case 36: case 37: case 38:
# //       if(conf.ana_type!="SdcOut"){
# // 	ofs<<line<<std::endl;
# // 	break;
# //       }
# //       cp0 = -1.*t0[PlId-LayerOffset][WireId-1]*cp1;
# //       sprintf(buf, "%d\t%d\t%.5f\t%.3f", PlId, WireId, cp1, cp0);
# //       //std::cout<<buf<<"\t"<<fitok[PlId-LayerOffset][WireId-1]<<std::endl;
# //       ofs<<buf<<std::endl;
# //       break;
# //     default:
# //       ofs<<line<<std::endl;
# //       break;
# //     }
# //   }

# //   return EXIT_SUCCESS;
# // }

# // //_____________________________________________________________________________
# // void
# // InitBcIn()
# // {
# //   //static const std::string funcname("["+__func__+"()]");
# //   std::cerr << "#E " << __func__ << "()]"
# // 	    << " current version doesn't support BcIn" << std::endl;
# //   std::exit(EXIT_FAILURE);
# //   conf.ana_type = "BcIn";
# //   // LayerOffset = 101;
# // }

# // //_____________________________________________________________________________
# // void
# // InitBcOut()
# // {
# //   LayerOffset = 113;
# //   MaxWire.clear();
# //   MaxDriftLength.clear();
# //   XTFitOffset.clear();
# //   MinLayer = BeginLayerBcOut;
# //   MaxLayer = EndLayerBcOut;
# //   for(int i=0; i<NumOfPlaneBC3; i++){
# //     MaxWire.push_back( NumOfWireBC3 );
# //     MaxDriftLength.push_back( MaxDriftLengthBC3 );
# //     MaxDriftTime.push_back( MaxDriftTimeBC3 );
# //     MaxFitDriftTime.push_back( MaxDriftTimeBC3 );
# //     XTFitOffset.push_back( XTFitOffsetBC3 );
# //     FitWidth.push_back( FitWidthBC3 );
# //   }
# //   for(int i=0; i<NumOfPlaneBC4; i++){
# //     MaxWire.push_back( NumOfWireBC4 );
# //     MaxDriftLength.push_back( MaxDriftLengthBC4 );
# //     MaxDriftTime.push_back( MaxDriftTimeBC4 );
# //     MaxFitDriftTime.push_back( MaxDriftTimeBC4 );
# //     XTFitOffset.push_back( XTFitOffsetBC4 );
# //     FitWidth.push_back( FitWidthBC4 );
# //   }
# //   conf.ana_type = "BcOut";
# //   std::cout<<Form("#D %s(): initialized", __func__)<<std::endl;
# // }

# // //_____________________________________________________________________________
# // void
# // InitSdcIn()
# // {
# //   LayerOffset = 1;
# //   MaxWire.clear();
# //   MaxDriftLength.clear();
# //   XTFitOffset.clear();
# //   MinLayer = BeginLayerSdcIn;
# //   MaxLayer = EndLayerSdcIn;
# //   for( int i=0; i<NumOfPlaneSDC1; ++i ){
# //     MaxWire.push_back( NumOfWireSDC1 );
# //     MaxDriftLength.push_back( MaxDriftLengthSDC1 );
# //     MaxDriftTime.push_back( MaxDriftTimeSDC1 );
# //     MaxFitDriftTime.push_back( MaxDriftTimeSDC1 );
# //     FitWidth.push_back( FitWidthSDC1 );
# //   }
# //   conf.ana_type = "SdcIn";
# //   std::cout<<Form("#D %s(): initialized", __func__)<<std::endl;
# // }

# // //_____________________________________________________________________________
# // void
# // InitSdcOut( void )
# // {
# //   LayerOffset = 31;
# //   MaxWire.clear(); MaxDriftLength.clear();
# //   MinLayer = BeginLayerSdcOut;
# //   MaxLayer = EndLayerSdcOut;
# //   XTFitOffset.clear();
# //   for( int i=0; i<NumOfPlaneSDC2; ++i ){
# //     MaxWire.push_back( NumOfWireSDC2 );
# //     MaxDriftLength.push_back( MaxDriftLengthSDC2 );
# //     MaxDriftTime.push_back( MaxDriftTimeSDC2 );
# //     MaxFitDriftTime.push_back( MaxDriftTimeSDC2 );
# //     FitWidth.push_back( FitWidthSDC2 );
# //   }
# //   for( int i=0; i<NumOfPlaneSDC3;++i ){
# //     if( i==0 || i==1 )
# //       MaxWire.push_back( NumOfWireSDC3Y );
# //     if( i==2 || i==3 )
# //       MaxWire.push_back( NumOfWireSDC3X );
# //     MaxDriftLength.push_back( MaxDriftLengthSDC3 );
# //     MaxDriftTime.push_back( MaxDriftTimeSDC3 );
# //     MaxFitDriftTime.push_back( MaxDriftTimeSDC3 );
# //     FitWidth.push_back( FitWidthSDC3 );
# //   }
# //   conf.ana_type = "SdcOut";
# //   std::cout<<Form("#D %s(): initialized", __func__)<<std::endl;
# // }

# // //_____________________________________________________________________________
# // void
# // Print()
# // {

# // }
