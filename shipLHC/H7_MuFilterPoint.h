#ifndef H7_MUFILTERPOINT_H
#define H7_MUFILTERPOINT_H 1


#include "FairMCPoint.h"

#include "TObject.h"
#include "TVector3.h"

class H7_MuFilterPoint : public FairMCPoint
{

  public:

    /** Default constructor **/
    H7_MuFilterPoint();


    /** Constructor with arguments
     *@param trackID  Index of MCTrack
     *@param detID    Detector ID
     *@param pos      Ccoordinates at entrance to active volume [cm]
     *@param mom      Momentum of track at entrance [GeV]
     *@param tof      Time since event start [ns]
     *@param length   Track length since creation [cm]
     *@param eLoss    Energy deposit [GeV]
     **/

    
    H7_MuFilterPoint(Int_t trackID, Int_t detID, TVector3 pos, TVector3 mom,
		Double_t tof, Double_t length, Double_t eLoss, Int_t pdgCode);

    /** Destructor **/
    virtual ~H7_MuFilterPoint();

    /** Output to screen **/
    virtual void Print(const Option_t* opt) const;
    

    Int_t PdgCode() const {return fPdgCode;}

  private:


    Int_t fPdgCode;
    
    /** Copy constructor **/
    
    H7_MuFilterPoint(const H7_MuFilterPoint& point);
    H7_MuFilterPoint operator=(const H7_MuFilterPoint& point);

    ClassDef(H7_MuFilterPoint,1)

};

#endif
