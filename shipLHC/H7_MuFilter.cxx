//
//  H7_MuFilter.cxx
//
//  by M.Climescu 
//

#include "H7_MuFilter.h"
#include "H7_MuFilterPoint.h"

#include "TGeoManager.h"
#include "TString.h"                    // for TString

#include "TClonesArray.h"
#include "TVirtualMC.h"

#include "TGeoBBox.h"
#include "TGeoMaterial.h"
#include "TGeoMedium.h"
#include "TGeoBBox.h"
#include "TGeoCompositeShape.h"

#include "TParticle.h"
#include "TParticlePDG.h"
#include "TParticleClassPDG.h"
#include "TVirtualMCStack.h"

#include "FairVolume.h"
#include "FairGeoVolume.h"
#include "FairGeoNode.h"
#include "FairRootManager.h"
#include "FairGeoLoader.h"
#include "FairGeoInterface.h"
#include "FairGeoTransform.h"
#include "FairGeoMedia.h"
#include "FairGeoMedium.h"
#include "FairGeoBuilder.h"
#include "FairRun.h"

#include "ShipDetectorList.h"
#include "ShipUnit.h"
#include "ShipStack.h"

#include <stddef.h>                     // for NULL
#include <iostream>                     // for operator<<, basic_ostream,etc
#include <string.h>
#include <cstring>

using std::cout;
using std::endl;
using std::to_string;
using std::string;
using namespace ShipUnit;

H7_MuFilter::H7_MuFilter()
: FairDetector("MuonFilter", "",kTRUE),
  fTrackID(-1),
fVolumeID(-1),
fPos(),
fMom(),
fTime(-1.),
fLength(-1.),
fELoss(-1),
fH7_MuFilterPointCollection(new TClonesArray("H7_MuFilterPoint"))
{
}

H7_MuFilter::H7_MuFilter(const char* name, Bool_t Active,const char* Title)
: FairDetector(name, true, kH7_MuFilter),
  fTrackID(-1),
fVolumeID(-1),
fPos(),
fMom(),
fTime(-1.),
fLength(-1.),
fELoss(-1),
fH7_MuFilterPointCollection(new TClonesArray("H7_MuFilterPoint"))
{
}

H7_MuFilter::~H7_MuFilter()
{
    if (fH7_MuFilterPointCollection) {
        fH7_MuFilterPointCollection->Delete();
        delete fH7_MuFilterPointCollection;
    }
}

void H7_MuFilter::Initialize()
{
	FairDetector::Initialize();
}

// -----  Private method InitMedium
Int_t H7_MuFilter::InitMedium(const char* name)
{
    static FairGeoLoader *geoLoad=FairGeoLoader::Instance();
    static FairGeoInterface *geoFace=geoLoad->getGeoInterface();
    static FairGeoMedia *media=geoFace->getMedia();
    static FairGeoBuilder *geoBuild=geoLoad->getGeoBuilder();

    FairGeoMedium *ShipMedium=media->getMedium(name);

    if (!ShipMedium)
    {
        Fatal("InitMedium","Material %s not defined in media file.", name);
        return -1111;
    }
    TGeoMedium* medium=gGeoManager->GetMedium(name);
    if (medium!=NULL)
        return ShipMedium->getMediumIndex();
    return geoBuild->createMedium(ShipMedium);
}

void H7_MuFilter::ConstructGeometry()
{
	TGeoVolume *top=gGeoManager->FindVolumeFast("Detector");
	if(!top)  LOG(ERROR) << "no Detector volume found " ;

	//Materials 

	InitMedium("iron");
	TGeoMedium *Fe =gGeoManager->GetMedium("iron");
	InitMedium("aluminium");
	TGeoMedium *Al =gGeoManager->GetMedium("aluminium");
	InitMedium("polyvinyltoluene");
	TGeoMedium *Scint =gGeoManager->GetMedium("polyvinyltoluene");
	InitMedium("Concrete");
	TGeoMedium *concrete = gGeoManager->GetMedium("Concrete");

	Float_t nSiPMs[3];             //  number of SiPMs per side
	Float_t nSides[3];             //  number of sides readout
	nSiPMs[0] = conf_ints["H7_MuFilter/VetonSiPMs"];
	nSiPMs[1] = conf_ints["H7_MuFilter/UpstreamnSiPMs"];
	nSiPMs[2] = conf_ints["H7_MuFilter/DownstreamnSiPMs"];
	nSides[0]  = conf_ints["H7_MuFilter/VetonSides"];
	nSides[1]  = conf_ints["H7_MuFilter/DownstreamnSides"];
	nSides[2]  = conf_ints["H7_MuFilter/UpstreamnSides"];

	Int_t fNUpstreamPlanes = conf_ints["H7_MuFilter/NUpstreamPlanes"]; // Number of planes
	Int_t fNUpstreamBars = conf_ints["H7_MuFilter/NUpstreamBars"]; // Number of staggered bars
	Int_t fNDownstreamPlanes =  conf_ints["H7_MuFilter/NDownstreamPlanes"]; // Number of planes
	Int_t fNDownstreamBars =  conf_ints["H7_MuFilter/NDownstreamBars"]; // Number of staggered bars
	Double_t fDownstreamBarX_ver = conf_floats["H7_MuFilter/DownstreamBarX_ver"]; // Staggered bars of upstream section, vertical bars for x measurement
	Double_t fDownstreamBarY_ver = conf_floats["H7_MuFilter/DownstreamBarY_ver"];
	Double_t fDownstreamBarZ_ver = conf_floats["H7_MuFilter/DownstreamBarZ_ver"];
	Double_t fDS4ZGap = conf_floats["H7_MuFilter/DS4ZGap"];

	// position of left bottom edges in survey coordinate system converted to physicist friendly coordinate system
	std::map<int, TVector3 > edge_Veto;
	edge_Veto[1] = TVector3( -conf_floats["H7_MuFilter/Veto1Dx"],conf_floats["H7_MuFilter/Veto1Dz"],conf_floats["H7_MuFilter/Veto1Dy"]) ;
	edge_Veto[2] = TVector3( -conf_floats["H7_MuFilter/Veto2Dx"],conf_floats["H7_MuFilter/Veto2Dz"],conf_floats["H7_MuFilter/Veto2Dy"]) ;
	std::map<int, TVector3 > edge_Iron;
	std::map<int, TVector3 > edge_H7_MuFilter;
	for (int i=1;i<10;i++){
		string si = to_string(i);
		edge_Iron[i] = TVector3( -conf_floats["H7_MuFilter/Iron"+si+"Dx"],conf_floats["H7_MuFilter/Iron"+si+"Dz"],conf_floats["H7_MuFilter/Iron"+si+"Dy"]);
		edge_H7_MuFilter[i]  = TVector3( -conf_floats["H7_MuFilter/Muon"+si+"Dx"],conf_floats["H7_MuFilter/Muon"+si+"Dz"],conf_floats["H7_MuFilter/Muon"+si+"Dy"]);
	}
	// system alignment parameters
	Double_t fVetoShiftX   = conf_floats["H7_MuFilter/VetoShiftX"];
	Double_t fVetoShiftY   = conf_floats["H7_MuFilter/VetoShiftY"];
	Double_t fVetoShiftZ   = conf_floats["H7_MuFilter/VetoShiftZ"];
	Double_t fShiftX     = conf_floats["H7_MuFilter/ShiftX"];
	Double_t fShiftY     = conf_floats["H7_MuFilter/ShiftY"];
	Double_t fShiftZ     = conf_floats["H7_MuFilter/ShiftZ"];

	TVector3 displacement;

	Int_t fNVetoPlanes       = conf_ints["H7_MuFilter/NVetoPlanes"]; //Moved here because needed for later
	//Definition of the box containing veto planes //Not needed for TBSND23
	/*TGeoVolumeAssembly *volVeto = new TGeoVolumeAssembly("volVeto");
	
	//Veto Planes
	Double_t fVetoBarX     = conf_floats["H7_MuFilter/VetoBarX"]; // Veto Bar dimensions
	Double_t fVetoBarY     = conf_floats["H7_MuFilter/VetoBarY"];
	Double_t fVetoBarZ     = conf_floats["H7_MuFilter/VetoBarZ"];
	Double_t fVetoBarGap     = conf_floats["H7_MuFilter/VetoBarGap"];
	Int_t fNVetoBars          = conf_ints["H7_MuFilter/NVetoBars"];
	Double_t fSupportBoxVW = conf_floats["H7_MuFilter/SupportBoxVW"]; // SupportBox dimensions
	// local position of bottom horizontal bar to survey edge
	TVector3 LocBarVeto = TVector3(-conf_floats["H7_MuFilter/VETOLocX"], conf_floats["H7_MuFilter/VETOLocZ"],conf_floats["H7_MuFilter/VETOLocY"]);

	TVector3 VetoBox1 = TVector3(-conf_floats["H7_MuFilter/VETOBoxX1"],conf_floats["H7_MuFilter/VETOBoxZ1"],conf_floats["H7_MuFilter/VETOBoxY1"]); // bottom front left
	TVector3 VetoBox2 = TVector3(-conf_floats["H7_MuFilter/VETOBoxX2"],conf_floats["H7_MuFilter/VETOBoxZ2"],conf_floats["H7_MuFilter/VETOBoxY2"]); // top back right
	TVector3 VetoBoxDim = TVector3( VetoBox1.X()-VetoBox2.X(), VetoBox2.Y()-VetoBox1.Y(), VetoBox2.Z()-VetoBox1.Z() ) ;
	// support box
	TGeoBBox  *supVetoBoxInner  = new TGeoBBox("supVetoBoxI",VetoBoxDim.X()/2,VetoBoxDim.Y()/2,VetoBoxDim.Z()/2);
	TGeoBBox  *supVetoBoxOuter = new TGeoBBox("supVetoBoxO",VetoBoxDim.X()/2+fSupportBoxVW,VetoBoxDim.Y()/2+fSupportBoxVW,VetoBoxDim.Z()/2+fSupportBoxVW);
	TGeoCompositeShape *subVetoBoxShape = new TGeoCompositeShape("subVetoBoxShape", "supVetoBoxO-supVetoBoxI");
	TGeoVolume *subVetoBox = new TGeoVolume("subVetoBox", subVetoBoxShape, Al);     
	subVetoBox->SetLineColor(kGray+1);

	//Veto bars
	TGeoVolume *volVetoBar = gGeoManager->MakeBox("volVetoBar",Scint,fVetoBarX/2., fVetoBarY/2., fVetoBarZ/2.);

	volVetoBar->SetLineColor(kRed-3);
	AddSensitiveVolume(volVetoBar);

	//adding veto planes //not needed for TBSND23
	
	TGeoVolume* volVetoPlane;
	for (int iplane=0; iplane < fNVetoPlanes; iplane++){
	  
	  string name = "volVetoPlane_"+to_string(iplane);
	  volVetoPlane = new TGeoVolumeAssembly(name.c_str());

	  displacement = edge_Veto[iplane+1] + LocBarVeto + TVector3(-fVetoBarX/2, 0, 0);
	  volVeto->AddNode(volVetoPlane,iplane,
				new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
	 //  VETOBox1 = bottom front left
	  displacement = edge_Veto[iplane+1] +VetoBox1 + TVector3(-VetoBoxDim.X()/2,VetoBoxDim.Y()/2,VetoBoxDim.Z()/2);
	  volVeto->AddNode(subVetoBox,iplane,
		new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));

	  displacement = TVector3(0, 0, 0);
	  for (Int_t ibar = 0; ibar < fNVetoBars; ibar++){
	    Double_t dy_bar =  (fVetoBarY + fVetoBarGap)*ibar; 
	    volVetoPlane->AddNode(volVetoBar, 1e+4+iplane*1e+3+ibar,
				new TGeoTranslation(displacement.X(),displacement.Y()+dy_bar,displacement.Z()));
	  }
	}
	
		//adding to detector volume
	top->AddNode(volVeto, 1,new TGeoTranslation(fVetoShiftX,fVetoShiftY,fVetoShiftZ)) ;


	
	


	*/
	//*****************************************UPSTREAM SECTION*********************************//

		//Definition of the box containing Fe Blocks + Timing Detector planes 
	TGeoVolumeAssembly *volH7_MuFilter = new TGeoVolumeAssembly("volH7_MuFilter");
	
	//Iron blocks volume definition
	Double_t fFeBlockX = conf_floats["H7_MuFilter/FeX"]; // Passive Iron blocks dimensions
	Double_t fFeBlockY = conf_floats["H7_MuFilter/FeY"];
	Double_t fFeBlockZ = conf_floats["H7_MuFilter/FeZ"];
	Double_t fFeBlockEndX = conf_floats["H7_MuFilter/FeEndX"]; // last Iron block dimensions
	Double_t fFeBlockEndY = conf_floats["H7_MuFilter/FeEndY"];
	Double_t fFeBlockEndZ = conf_floats["H7_MuFilter/FeEndZ"];
	Double_t fFeBlockBotX = conf_floats["H7_MuFilter/FeBotX"]; // bottom Iron block dimensions
	Double_t fFeBlockBotY = conf_floats["H7_MuFilter/FeBotY"];
	Double_t fFeBlockBotZ = conf_floats["H7_MuFilter/FeBotZ"];
	Double_t fSupportBoxW = conf_floats["H7_MuFilter/SupportBoxW"]; // SupportBox dimensions



	TVector3 DSBox1 = TVector3(-conf_floats["H7_MuFilter/DSBoxX1"],conf_floats["H7_MuFilter/DSBoxZ1"],conf_floats["H7_MuFilter/DSBoxY1"]); // bottom front left
	TVector3 DSBox2 = TVector3(-conf_floats["H7_MuFilter/DSBoxX2"],conf_floats["H7_MuFilter/DSBoxZ2"],conf_floats["H7_MuFilter/DSBoxY2"]); // top back right
	TVector3 DSBoxDim = TVector3( DSBox1.X()-DSBox2.X(), DSBox2.Y()-DSBox1.Y(), DSBox2.Z()-DSBox1.Z() ) ;
	TVector3 USBox1 = TVector3(-conf_floats["H7_MuFilter/DSBoxX1"],conf_floats["H7_MuFilter/DSBoxZ1"],conf_floats["H7_MuFilter/USBoxY1"]); // bottom front left
	TVector3 USBox2 = TVector3(-conf_floats["H7_MuFilter/DSBoxX2"],conf_floats["H7_MuFilter/DSBoxZ2"],conf_floats["H7_MuFilter/USBoxY2"]); // top back right
	TVector3 USBoxDim = TVector3( USBox1.X()-USBox2.X(), USBox2.Y()-USBox1.Y(), USBox2.Z()-USBox1.Z() ) ;

	//Iron blocks volume definition
	TGeoVolume *volFeBlock = gGeoManager->MakeBox("volFeBlock",Fe,fFeBlockX/2, fFeBlockY/2, fFeBlockZ/2); 
	//volFeBlock->SetLineColor(kGreen-4);
	volFeBlock->SetLineColor(kGreen-4);
	TGeoVolume *volFeBlockEnd = gGeoManager->MakeBox("volFeBlockEnd",Fe,fFeBlockEndX/2, fFeBlockEndY/2, fFeBlockEndZ/2);
	//volFeBlockEnd->SetLineColor(kGreen-4);
	volFeBlockEnd->SetLineColor(kYellow);
	TGeoVolume *volBlockBot = gGeoManager->MakeBox("volBlockBot",concrete,fFeBlockBotX/2, fFeBlockBotY/2, fFeBlockBotZ/2);
	//volBlockBot->SetLineColor(kGreen-4);
	volBlockBot->SetLineColor(kOrange);

	// support box
	TGeoBBox  *supDSBoxInner  = new TGeoBBox("supDSBoxI",DSBoxDim.X()/2,DSBoxDim.Y()/2,DSBoxDim.Z()/2);
	TGeoBBox  *supDSBoxOuter = new TGeoBBox("supDSBoxO",DSBoxDim.X()/2+fSupportBoxW,DSBoxDim.Y()/2+fSupportBoxW,DSBoxDim.Z()/2+fSupportBoxW);
	TGeoCompositeShape *subDSBoxShape = new TGeoCompositeShape("subDSBoxShape", "supDSBoxO-supDSBoxI");
	TGeoVolume *subDSBox = new TGeoVolume("subDSBox", subDSBoxShape, Al);     
	subDSBox->SetLineColor(kGray+1);
	TGeoBBox  *supUSBoxInner  = new TGeoBBox("supUSBoxI",USBoxDim.X()/2,USBoxDim.Y()/2,USBoxDim.Z()/2);
	TGeoBBox  *supUSBoxOuter = new TGeoBBox("supUSBoxO",USBoxDim.X()/2+fSupportBoxW,USBoxDim.Y()/2+fSupportBoxW,USBoxDim.Z()/2+fSupportBoxW);
	TGeoCompositeShape *subUSBoxShape = new TGeoCompositeShape("subUSBoxShape", "supUSBoxO-supUSBoxI");
	TGeoVolume *subUSBox = new TGeoVolume("subUSBox", subUSBoxShape, Al);     
	subUSBox->SetLineColor(kGray+1);

	top->AddNode(volH7_MuFilter,1,new TGeoTranslation(fShiftX,fShiftY,fShiftZ ));

	Double_t dy = 0;
	Double_t dz = 0;
	//Upstream Detector planes definition
	Double_t fUpstreamDetZ =  conf_floats["H7_MuFilter/UpstreamDetZ"];
	// local position of bottom horizontal bar to survey edge
	TVector3 LocBarUS = TVector3(
		-conf_floats["H7_MuFilter/DSHLocX"],
		conf_floats["H7_MuFilter/DSHLocZ"] - conf_floats["H7_MuFilter/DownstreamBarY"]/2 + conf_floats["H7_MuFilter/UpstreamBarY"]/2,
		conf_floats["H7_MuFilter/DSHLocY"]);

	TGeoVolume* volUpstreamDet;
	Double_t fUpstreamBarX = conf_floats["H7_MuFilter/UpstreamBarX"]; //Staggered bars of upstream section
	Double_t fUpstreamBarY = conf_floats["H7_MuFilter/UpstreamBarY"];
	Double_t fUpstreamBarZ = conf_floats["H7_MuFilter/UpstreamBarZ"];
	Double_t fUpstreamBarGap = conf_floats["H7_MuFilter/UpstreamBarGap"];

	//H7 Scintillator dimensions
	Double_t fTargetScintillatorX = conf_floats["H7_MuFilter/TScintX"]; 
	Double_t fTargetScintillatorY = conf_floats["H7_MuFilter/TScintY"];
	Double_t fTargetScintillatorZ = conf_floats["H7_MuFilter/TScintZ"];

	//H7 Segmented Target Thicknesses
	Double_t fTargetThick1 = conf_floats["H7_MuFilter/H7_TT1"]; 
	Double_t fTargetThick2 = conf_floats["H7_MuFilter/H7_TT2"];
	Double_t fTargetThick3 = conf_floats["H7_MuFilter/H7_TT3"];
	
	//H7 Beam Counter Parameters
	Double_t fBC_rad = conf_floats["H7_MuFilter/H7_BC_Scint_rad"];
	Double_t fBC_thick = conf_floats["H7_MuFilter/H7_BC_Scint_thick"];
	Double_t fBC_ScintX = conf_floats["H7_MuFilter/H7_BC_ScintX"];
	Double_t fBC_ScintY = conf_floats["H7_MuFilter/H7_BC_ScintY"];
	Double_t fBC_ScintZ = conf_floats["H7_MuFilter/H7_BC_ScintZ"];

	//adding staggered bars, first part, only 11 bars, (single stations, readout on both ends)
	TGeoVolume *volMuUpstreamBar = gGeoManager->MakeBox("volMuUpstreamBar",Scint,fUpstreamBarX/2, fUpstreamBarY/2, fUpstreamBarZ/2);
	volMuUpstreamBar->SetLineColor(kBlue+2);
	AddSensitiveVolume(volMuUpstreamBar);
	for(Int_t l=0; l<fNUpstreamPlanes; l++)
	{
	  string name = "volMuUpstreamDet_"+std::to_string(l);
	  volUpstreamDet = new TGeoVolumeAssembly(name.c_str());

	  displacement = edge_Iron[l+1] - TVector3(fFeBlockX/2,-fFeBlockY/2,-fFeBlockZ/2);
	  volH7_MuFilter->AddNode(volFeBlock,l,new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
// place for H8 mockup target 20cm in front of US1
// 	Gap between Divided Target and first upstream iron plate[US1]: 20cm
	//Target: between end of Iron target and scintillator 0.76cm
	//gap between first scint and iron plate is 0.74cm
	  if (edge_Iron[9][2] <0.1 && l==0) {
//		TGeoVolume *volFeTarget[3] = {gGeoManager->MakeBox("volScintTarget0",Fe,80./2, 60./2, 16.77/2/2),
//					      gGeoManager->MakeBox("volScintTarget1",Fe,80./2, 60./2, 16.77/2/2),
//					      gGeoManager->MakeBox("volScintTarget2",Fe,80./2, 60./2, (29.5-16.77)/2)};

//Segmentation in 3
/*		TGeoVolume *volFeTarget[3] = {gGeoManager->MakeBox("volScintTarget0",Fe,80./2, 60./2, fTargetThick1),
					      gGeoManager->MakeBox("volScintTarget1",Fe,80./2, 60./2, fTargetThick2),
					      gGeoManager->MakeBox("volScintTarget2",Fe,80./2, 60./2, fTargetThick3)};

		volFeTarget[0]->SetLineColor(kGreen-4);
		volFeTarget[1]->SetLineColor(kGreen-4);
		volFeTarget[2]->SetLineColor(kGreen-4);
	//	AddSensitiveVolume(volFeTarget[0]);
	//	AddSensitiveVolume(volFeTarget[1]);
	//	AddSensitiveVolume(volFeTarget[2]);
		displacement = edge_Iron[l+1] - TVector3(80/2,-60/2,29.5/2+fFeBlockZ+3*fTargetScintillatorZ);
		volH7_MuFilter->AddNode(volFeTarget[0],1,
                                    new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
		volH7_MuFilter->AddNode(volFeTarget[1],1,
                                    new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()+29.5/3+2.5));
		volH7_MuFilter->AddNode(volFeTarget[2],1,
                                    new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()+2*(29.5/3+2.5)));
	//}
	  displacement = edge_H7_MuFilter[l+1]+LocBarUS + TVector3(-fUpstreamBarX/2, 0, 0);
	  volH7_MuFilter->AddNode(volUpstreamDet,fNVetoPlanes+l,
                                    new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
*/
		
		TGeoVolume *volFeTarget[100];

		displacement = edge_Iron[l+1] - TVector3(80/2,-60/2,29.5/2+fFeBlockZ+3*fTargetScintillatorZ);
		for(int element=0;element<100;element++){
			volFeTarget[element]=gGeoManager->MakeBox(Form("volScintTarget%d",element),Fe,80./2, 60./2,29.5/100/2),
			volFeTarget[element]->SetLineColor(kGreen-4);
			AddSensitiveVolume(volFeTarget[element]);
			volH7_MuFilter->AddNode(volFeTarget[element],100+element,
                                    new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()+element*(29.5/100/*+2.5*/)));
		}
		}
	  displacement = edge_H7_MuFilter[l+1]+LocBarUS + TVector3(-fUpstreamBarX/2, 0, 0);
	  volH7_MuFilter->AddNode(volUpstreamDet,fNVetoPlanes+l,
                                    new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));




	 //  USBox1 = bottom front left
	  displacement = edge_H7_MuFilter[l+1] +USBox1 + TVector3(-USBoxDim.X()/2,USBoxDim.Y()/2,USBoxDim.Z()/2);
	  volH7_MuFilter->AddNode(subUSBox,l+fNVetoPlanes,
		new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));

	  displacement = TVector3(0, 0, 0);
	  for (Int_t ibar = 0; ibar < fNUpstreamBars; ibar++){
	    Double_t dy_bar =  (fUpstreamBarY + fUpstreamBarGap)*ibar; 
	    volUpstreamDet->AddNode(volMuUpstreamBar,2e+4+l*1e+3+ibar,
				new TGeoTranslation(displacement.X(),displacement.Y()+conf_floats["H7_MuFilter/USOffZ"+to_string(l+1)]+dy_bar,displacement.Z()));
	  }

	}

	//*************************************DOWNSTREAM (high granularity) SECTION*****************//

    // first loop, adding detector main boxes
	TGeoVolume* volDownstreamDet;

	// local position of bottom horizontal bar to survey edge
	TVector3 LocBarH = TVector3(-conf_floats["H7_MuFilter/DSHLocX"],conf_floats["H7_MuFilter/DSHLocZ"],conf_floats["H7_MuFilter/DSHLocY"]);
	// local position of l left vertical bar to survey edge
	TVector3 LocBarV = TVector3(-conf_floats["H7_MuFilter/DSVLocX"],conf_floats["H7_MuFilter/DSVLocZ"],conf_floats["H7_MuFilter/DSVLocY"]);

	Double_t fDownstreamBarX = conf_floats["H7_MuFilter/DownstreamBarX"]; // Staggered bars of upstream section
	Double_t fDownstreamBarY = conf_floats["H7_MuFilter/DownstreamBarY"];
	Double_t fDownstreamBarZ = conf_floats["H7_MuFilter/DownstreamBarZ"];
	Double_t fDownstreamBarGap = conf_floats["H7_MuFilter/DownstreamBarGap"];
	
	TGeoVolume *volMuDownstreamBar_hor = gGeoManager->MakeBox("volMuDownstreamBar_hor",Scint,fDownstreamBarX/2, fDownstreamBarY/2, fDownstreamBarZ/2);
	volMuDownstreamBar_hor->SetLineColor(kAzure+7);
	AddSensitiveVolume(volMuDownstreamBar_hor);

	//vertical bars, for x measurement
	TGeoVolume *volMuDownstreamBar_ver = gGeoManager->MakeBox("volMuDownstreamBar_ver",Scint,fDownstreamBarX_ver/2, fDownstreamBarY_ver/2, fDownstreamBarZ/2);
	volMuDownstreamBar_ver->SetLineColor(kViolet-2);
	AddSensitiveVolume(volMuDownstreamBar_ver);

	for(Int_t l=0; l<fNDownstreamPlanes; l++)
	{
	// add iron blocks
	//temp if (l<fNDownstreamPlanes-1){
		displacement = edge_Iron[l+fNUpstreamPlanes+1] - TVector3(fFeBlockX/2,-fFeBlockY/2,-fFeBlockZ/2);
		volH7_MuFilter->AddNode(volFeBlock,l+fNUpstreamPlanes+fNVetoPlanes,
				new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
	/*temp	}else if (edge_Iron[9][2] >0.1) {
// more iron
		displacement = edge_Iron[l+fNUpstreamPlanes+1]  - TVector3(fFeBlockEndX/2,-fFeBlockEndY/2,-fFeBlockEndZ/2);
		volH7_MuFilter->AddNode(volFeBlockEnd,1,
				new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
		displacement = edge_Iron[l+fNUpstreamPlanes+1]  - TVector3(fFeBlockBotX/2-10.0, fFeBlockBotY/2,fFeBlockBotZ/2-fFeBlockEndZ);
		volH7_MuFilter->AddNode(volBlockBot,1,
				new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
	}
	*/
	// add detectors
	string name = "volMuDownstreamDet_"+std::to_string(l);
	volDownstreamDet = new TGeoVolumeAssembly(name.c_str());
	displacement = edge_H7_MuFilter[l+fNUpstreamPlanes+1] + LocBarH + TVector3(-fDownstreamBarX/2, 0,0);
	
	volH7_MuFilter->AddNode(volDownstreamDet,l+fNUpstreamPlanes+fNVetoPlanes,
				new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));

	//adding bars within each detector box
	if (l!=fNDownstreamPlanes-1) {
		displacement = TVector3(0, 0,0);
		for (Int_t ibar = 0; ibar < fNDownstreamBars; ibar++){
	                 //adding horizontal bars for y
			Double_t dy_bar = (fDownstreamBarY + fDownstreamBarGap)*ibar;
		    	volDownstreamDet->AddNode(volMuDownstreamBar_hor,3e+4+l*1e+3+ibar,
				new TGeoTranslation(displacement.X(),displacement.Y()+dy_bar,displacement.Z()));
			}
		}
	 //  DSBox1 = bottom front left
	displacement = edge_H7_MuFilter[l+fNUpstreamPlanes+1] +DSBox1 +
			TVector3(-DSBoxDim.X()/2,DSBoxDim.Y()/2,DSBoxDim.Z()/2);
		volH7_MuFilter->AddNode(subDSBox,l+fNUpstreamPlanes+fNVetoPlanes,
		new TGeoTranslation(displacement.X(),displacement.Y(),displacement.Z()));
	//adding vertical bars for x
	displacement = LocBarV + TVector3(0, -fDownstreamBarY_ver/2,0) - LocBarH - TVector3(-fDownstreamBarX/2, 0,0);
	for (Int_t i_vbar = 0; i_vbar<fNDownstreamBars; i_vbar++) {
		Double_t dx_bar = (fDownstreamBarX_ver+ fDownstreamBarGap)*i_vbar;
		Int_t i_vbar_rev  = fNDownstreamBars-1-i_vbar;
		volDownstreamDet->AddNode(volMuDownstreamBar_ver,3e+4+l*1e+3+i_vbar_rev+60,
				new TGeoTranslation(displacement.X()+dx_bar,displacement.Y(),displacement.Z())); 
 		// Andrew added a 60 here to make each horizontal + vertical sub-plane contain bars given detIDs as one plane. So the first bar in the vert. sub plane is the 60th etc. 
			}
	}

	//****************************************BEAM COUNTER**************************************//
	
	TGeoVolumeAssembly *volH7_BeamCounter = new TGeoVolumeAssembly("volH7_MuFilter");
	TGeoVolume *volBeamCounterScintillator=gGeoManager->MakeTube("BeamCounterPlasticScintillator",Scint,0,fBC_rad,fBC_thick);
	volBeamCounterScintillator->SetLineColor(kRed);
	AddSensitiveVolume(volBeamCounterScintillator);
	volH7_BeamCounter->AddNode(volBeamCounterScintillator,15000,new TGeoTranslation(fBC_ScintX,fBC_ScintY,fBC_ScintZ));
	top->AddNode(volH7_BeamCounter, 1,new TGeoTranslation(0,0,0)) ;

}

Bool_t  H7_MuFilter::ProcessHits(FairVolume* vol)
{
	/** This method is called from the MC stepping */
	//Set parameters at entrance of volume. Reset ELoss.
	if ( gMC->IsTrackEntering() ) 
	{
		fELoss  = 0.;
		fTime   = gMC->TrackTime() * 1.0e09;
		fLength = gMC->TrackLength();
		gMC->TrackPosition(fPos);
		gMC->TrackMomentum(fMom);
	}
	// Sum energy loss for all steps in the active volume
	fELoss += gMC->Edep();

	// Create H7_MuFilterPoint at exit of active volume
	if ( gMC->IsTrackExiting()    ||
			gMC->IsTrackStop()       || 
			gMC->IsTrackDisappeared()   ) {
		fTrackID  = gMC->GetStack()->GetCurrentTrackNumber();
		gMC->CurrentVolID(fVolumeID);

		if (fELoss == 0. ) { return kFALSE; }
		TParticle* p=gMC->GetStack()->GetCurrentTrack();
		Int_t pdgCode = p->GetPdgCode();

		TLorentzVector Pos; 
		gMC->TrackPosition(Pos); 
		Double_t xmean = (fPos.X()+Pos.X())/2. ;
		Double_t ymean = (fPos.Y()+Pos.Y())/2. ;
		Double_t zmean = (fPos.Z()+Pos.Z())/2. ;


		AddHit(fTrackID,fVolumeID, TVector3(xmean, ymean,  zmean),
				TVector3(fMom.Px(), fMom.Py(), fMom.Pz()), fTime, fLength,
				fELoss, pdgCode);

		// Increment number of muon det points in TParticle
		ShipStack* stack = (ShipStack*) gMC->GetStack();
		stack->AddPoint(kH7_MuFilter);
	}   

	return kTRUE;
}

void H7_MuFilter::EndOfEvent()
{
    fH7_MuFilterPointCollection->Clear();
}


void H7_MuFilter::Register()
{

    /** This will create a branch in the output tree called
 *      H7_MuFilterPoint, setting the last parameter to kFALSE means:
 *           this collection will not be written to the file, it will exist
 *                only during the simulation.
 *                     */

    FairRootManager::Instance()->Register("H7_MuFilterPoint", "H7_MuFilter",
                                          fH7_MuFilterPointCollection, kTRUE);
}

TClonesArray* H7_MuFilter::GetCollection(Int_t iColl) const
{
    if (iColl == 0) { return fH7_MuFilterPointCollection; }
    else { return NULL; }
}

void H7_MuFilter::Reset()
{
    fH7_MuFilterPointCollection->Clear();
}


H7_MuFilterPoint* H7_MuFilter::AddHit(Int_t trackID,Int_t detID,
                           TVector3 pos, TVector3 mom,
                           Double_t time, Double_t length,
                            Double_t eLoss, Int_t pdgCode)
{
    TClonesArray& clref = *fH7_MuFilterPointCollection;
    Int_t size = clref.GetEntriesFast();
    return new(clref[size]) H7_MuFilterPoint(trackID,detID, pos, mom,
                                        time, length, eLoss, pdgCode);
}

void H7_MuFilter::GetLocalPosition(Int_t fDetectorID, TVector3& vLeft, TVector3& vRight)
{
  GetPosition(fDetectorID, vLeft, vRight);
  TGeoNavigator* nav = gGeoManager->GetCurrentNavigator();
  TString path = nav->GetPath();
  TString loc( path(0, path.Last('/') ) );
  nav->cd(loc);
  Double_t A[3] = {vLeft.X(),vLeft.Y(),vLeft.Z()};
  Double_t B[3] = {vRight.X(),vRight.Y(),vRight.Z()};
  Double_t locA[3] = {0,0,0};
  Double_t locB[3] = {0,0,0};
  nav->MasterToLocal(A, locA);   nav->MasterToLocal(B, locB);
  vLeft.SetXYZ(locA[0],locA[1],locA[2]);
  vRight.SetXYZ(locB[0],locB[1],locB[2]);
}

Float_t H7_MuFilter::GetCorrectedTime(Int_t fDetectorID, Int_t channel, Double_t rawTime, Double_t L){
/* expect time in u.ns  and  path length to sipm u.cm */
/* calibration implemented only for DS! */
/* channel 0 left or top, channel 1 right */
	if (fDetectorID<30000){
 		LOG(ERROR) << "not yet implemented for Veto and DS, no correction applied" ;
		return rawTime;
	}
	Float_t cor = rawTime;
	int l = (fDetectorID-30000)/1000;
	int ichannel60 = fDetectorID%1000;
	int p;
	if (channel==0 && ichannel60<30 ){p=0+l*6;}
	if (channel==0 && ichannel60>29 && ichannel60<60 ){p=1+l*6;}
	if (channel==1 && ichannel60<30 ){p=2+l*6;}
	if (channel==1 && ichannel60>29 && ichannel60<60 ){p=3+l*6;}
	if (channel==0 && ichannel60>59 && ichannel60<90 ){p=4+l*6;}
	if (channel==0 && ichannel60>89 && ichannel60<120 ){p=5+l*6;}
	if (l==3){p-=4;}
	if (ichannel60>59) {ichannel60-=60;}
	// DS time alignment first order
	if (ichannel60<30){cor += conf_floats["H7_MuFilter/DSTcorslope"]*(ichannel60-15);}
	else{              cor -= conf_floats["H7_MuFilter/DSTcorslope"]*(ichannel60-45);}
	string si = to_string(p);
	cor -= conf_floats["H7_MuFilter/DSTcorC"+si];
	cor -= L/conf_floats["H7_MuFilter/DsPropSpeed"];
	return cor;
}

void H7_MuFilter::GetPosition(Int_t fDetectorID, TVector3& vLeft, TVector3& vRight)
{

  int subsystem     = floor(fDetectorID/10000);
  int plane             = floor(fDetectorID/1000) - 10*subsystem;
  int bar_number   = fDetectorID%1000;

  TString path = "/cave_1/Detector_0/";
  TString barName;
  Float_t shift;
  switch(subsystem) {
  
  case 1: 
      path+="volVeto_1/volVetoPlane_"+std::to_string(plane)+"_"+std::to_string(plane);
      barName = "/volVetoBar_";
      shift = conf_floats["H7_MuFilter/Veto"+std::to_string(plane+1)+"ShiftY"];
      break;
  case 2: 
      path+="volH7_MuFilter_1/volMuUpstreamDet_"+std::to_string(plane)+"_"+std::to_string(plane+2);
      barName = "/volMuUpstreamBar_";
      shift = conf_floats["H7_MuFilter/US"+std::to_string(plane+1)+"ShiftY"];
      break;
  case 3: 
      path+="volH7_MuFilter_1/volMuDownstreamDet_"+std::to_string(plane)+"_"+std::to_string(plane+7);
      barName = "/volMuDownstreamBar_";
      if (bar_number<60){
           barName+="hor_";
           shift = conf_floats["H7_MuFilter/DS"+std::to_string(plane+1)+"ShiftY"];
      }
      else{
           barName+="ver_";
           shift = conf_floats["H7_MuFilter/DS"+std::to_string(plane+1)+"ShiftX"];
      }
      break;
  }
  path += barName+std::to_string(fDetectorID);

  TGeoNavigator* nav = gGeoManager->GetCurrentNavigator();
  nav->cd(path);
  LOG(DEBUG) <<path<<" "<<fDetectorID<<" "<<subsystem<<" "<<bar_number;
  TGeoNode* W = nav->GetCurrentNode();
  TGeoBBox* S = dynamic_cast<TGeoBBox*>(W->GetVolume()->GetShape());

  if (subsystem == 3 and bar_number >59){  // vertical bars
      Double_t top[3] = {shift,S->GetDY(), 0};
      Double_t bot[3] = {shift,-S->GetDY(),0};
      Double_t Gtop[3],Gbot[3];
      nav->LocalToMaster(top, Gtop);   nav->LocalToMaster(bot, Gbot);
      vLeft.SetXYZ(Gtop[0],Gtop[1],Gtop[2]);
      vRight.SetXYZ(Gbot[0],Gbot[1],Gbot[2]);
    }
    else {     // horizontal bars
      Double_t posXend[3] = {S->GetDX(),shift,0};
      Double_t negXend[3] = {-S->GetDX(),shift,0};
      Double_t GposXend[3],GnegXend[3];
      nav->LocalToMaster(posXend, GposXend);   nav->LocalToMaster(negXend, GnegXend);
      vLeft.SetXYZ(GposXend[0],GposXend[1],GposXend[2]);
      vRight.SetXYZ(GnegXend[0],GnegXend[1],GnegXend[2]);
    }
}

   Int_t H7_MuFilter::GetnSiPMs(Int_t detID){
       int subsystem     = floor(detID/10000)-1;
       if (subsystem==0){return conf_ints["H7_MuFilter/VetonSiPMs"];}
       if (subsystem==1){return conf_ints["H7_MuFilter/UpstreamnSiPMs"];}
       return conf_ints["H7_MuFilter/DownstreamnSiPMs"];

   }
   Int_t H7_MuFilter::GetnSides(Int_t detID){
       int subsystem     = floor(detID/10000)-1;
       if (subsystem==0){return conf_ints["H7_MuFilter/VetonSides"];}
       if (subsystem==1){return conf_ints["H7_MuFilter/UpstreamnSides"];}
       return conf_ints["H7_MuFilter/DownstreamnSides"];
  }
ClassImp(H7_MuFilter)
