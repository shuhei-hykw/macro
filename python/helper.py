#!/usr/bin/env python2

import sys
import ROOT

harray = dict()

#______________________________________________________________________________
def HB1(i, title, nbinx, xlow, xhigh, xtitle='', ytitle=''):
  if i<0:
    sys.stderr.write('HB1() invalid HistId : {}\n'.format(i))
    sys.exit(1)
  if i in harray:
    sys.stderr.write('HB1() h{}({}) already exists\n'
                     .format(i, harray[i].GetTitle()))
    sys.exit(1)
  harray[i] = ROOT.TH1D('h{}'.format(i), title, nbinx, xlow, xhigh)
  harray[i].SetXTitle(xtitle)
  harray[i].SetYTitle(ytitle)
  return harray[i]

#______________________________________________________________________________
def HB2(i, title, nbinx, xlow, xhigh, nbiny, ylow, yhigh,
        xtitle='', ytitle=''):
  if i<0:
    sys.stderr.write('HB2() invalid HistId : {}\n'.format(i))
    sys.exit(1)
  if i in harray:
    sys.stderr.write('HB2() h{}({}) already exists\n'
                     .format(i, harray[i].GetTitle()))
    sys.exit(1)
  harray[i] = ROOT.TH2D('h{}'.format(i), title,
                        nbinx, xlow, xhigh, nbiny, ylow, yhigh)
  harray[i].SetXTitle(xtitle)
  harray[i].SetYTitle(ytitle)
  return harray[i]

#______________________________________________________________________________
def HF1( i, x ):
  if i not in harray:
    sys.stderr.write('HF1() h{}({}) does not exist\n'
                     .format(i, harray[i].GetTitle()))
    sys.exit(1)
  else:
    harray[i].Fill( x )

#______________________________________________________________________________
def HF2( i, x, y ):
  if i not in harray:
    sys.stderr.write('HF2() h{}({}) does not exist\n'
                     .format(i, harray[i].GetTitle()))
    sys.exit(1)
  else:
    harray[i].Fill( x, y )

#______________________________________________________________________________
def HGet( i ):
  if i not in harray:
    sys.stderr.write('HGet() h{} does not exist\n'.format(i))
    return None
  else:
    return harray[i]

#   //___________________________________________________________________
#   inline void
#   HB1( int i, const TString& title,
#        int nbinx, double xlow, double xhigh )
#   {
#     HB1( i, title.Data(), nbinx, xlow, xhigh );
#   }

#   //___________________________________________________________________
#   inline void
#   HB2( int i, const char *title,
#        int nbinx, double xlow, double xhigh,
#        int nbiny, double ylow, double yhigh )
#   {
#     if( i<0 || MaxHist<=i )
#       throw std::out_of_range( Form("HB2() invalid HistId : %d/%d", i, MaxHist) );
#     if( h[i] ){
# #if ThrowError
#       throw std::invalid_argument( Form("h%d (%s) is already exist", i, title) );
# #endif
# #if OverWrite
#       delete h[i];
#       h[i] = 0;
# #endif
#     }
#     h[i] = new TH2F( Form("h%d", i), title,
# 		     nbinx, xlow, xhigh,
# 		     nbiny, ylow, yhigh );
#   }

#   //___________________________________________________________________
#   inline void
#   HB2( int i, const TString& title,
#        int nbinx, double xlow, double xhigh,
#        int nbiny, double ylow, double yhigh )
#   {
#     HB2( i, title.Data(), nbinx, xlow, xhigh, nbiny, ylow, yhigh );
#   }

#   //_____________________________________________________________________
#   inline void
#   HBProf( int i, const char *title,
# 	  int nbinx, double xlow, double xhigh,
# 	  double ylow, double yhigh )
#   {
#     if( i<0 || MaxHist<=i )
#       throw std::out_of_range( Form("HBProf() invalid HistId : %d/%d", i, MaxHist) );
#     if( h[i] ){
# #if ThrowError
#       throw std::invalid_argument( Form("h%d (%s) is already exist", i, title) );
# #endif
# #if OverWrite
#       delete h[i];
#       h[i] = 0;
# #endif
#     }
#     h[i] = new TProfile( Form("h%d", i), title,
# 			 nbinx, xlow, xhigh, ylow, yhigh );
#   }


#   //___________________________________________________________________
#   inline void
#   HF2( int i, double x, double y )
#   {
#     if( i<0 || MaxHist<=i )
#       throw std::out_of_range( Form("HF2() invalid HistId : %d/%d", i, MaxHist) );
#     if( h[i] ) h[i]->Fill( x, y );
#   }

#   //___________________________________________________________________
#   inline void
#   HFProf( int i, double x, double y )
#   {
#     if( i<0 || MaxHist<=i )
#       throw std::out_of_range( Form("HFProf() invalid HistId : %d/%d", i, MaxHist) );
#     if( h[i] ) h[i]->Fill( x, y );
#   }

#   //_____________________________________________________________________
#   inline void
#   HBTree( const char *name, const char *title )
#   {
#     if( tree ){
# #if ThrowError
#       throw std::invalid_argument( Form("%s (%s) is already exist", name, title) );
# #endif
# #if OverWrite
#       delete tree;
#       tree = 0;
# #endif
#     }
#     tree = new TTree( name, title );
#   }

#   //_____________________________________________________________________
#   inline void
#   HPrint( const std::string& arg="" )
#   {
#     hddaq::cout << "#D [root::HPrint()] " << arg << std::endl;
#     TList* list = gDirectory->GetList();
# #if 0
#     int count = 0;
#     TIter itr( list );
#     while( itr.Next() && ++count ){
#       const TString& name( (*itr)->GetName() );
#       hddaq::cout << " " << std::setw(8) << std::left << name;
#       if( count%10==0 ) hddaq::cout << std::endl;
#     }
#     hddaq::cout << std::endl;
# #endif
#     hddaq::cout << " NObject : " << list->GetEntries() << std::endl;
#   }

# }

# #endif
