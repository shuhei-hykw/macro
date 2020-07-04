// -*- C++ -*-

#include <TH1.h>
#include <TH2.h>
#include <TString.h>

//_____________________________________________________________________
// Utility Functions

//_____________________________________________________________________
TH1*
NewTH1( TString name, TString title,
	Int_t xbin, Double_t xmin, Double_t xmax,
	Color_t c=kBlue+1, Width_t w=2 )
{
  TH1 *h = new TH1F(name, title, xbin, xmin, xmax);
  h->SetLineColor(c);
  h->SetLineWidth(w);
  return h;
}

//_____________________________________________________________________
TH1*
NewTH2( TString name, TString title,
	Int_t xbin, Double_t xmin, Double_t xmax,
	Int_t ybin, Double_t ymin, Double_t ymax,
	Color_t c=kBlue+1, Width_t w=2 )
{
  TH1 *h = new TH2F(name, title, xbin, xmin, xmax, ybin, ymin, ymax);
  h->SetLineColor(c);
  h->SetLineWidth(w);
  return h;
}

//_____________________________________________________________________
TText*
NewTText( Float_t tsize=0.080, Font_t tfont=42, Color_t tcolor=kBlue+1 )
{
  TText *t = new TText;
  t->SetNDC();
  t->SetTextSize(tsize);
  t->SetTextFont(tfont);
  t->SetTextColor(tcolor);
  return t;
}
