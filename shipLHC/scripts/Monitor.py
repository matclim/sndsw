#!/usr/bin/env python
import ROOT
import os,sys,subprocess
import time
import ctypes
from array import array
import rootUtils as ut
import shipunit as u
import SndlhcGeo

A,B=ROOT.TVector3(),ROOT.TVector3()
ROOT.gInterpreter.Declare("""
#include "MuFilterHit.h"
#include "AbsMeasurement.h"
#include "TrackPoint.h"

void fixRoot(MuFilterHit& aHit,std::vector<int>& key,std::vector<float>& value, bool mask) {
   std::map<int,float> m = aHit.GetAllSignals(false);
   std::map<int, float>::iterator it = m.begin();
   while (it != m.end())
    {
        key.push_back(it->first);
        value.push_back(it->second);
        it++;
    }
}
void fixRootT(MuFilterHit& aHit,std::vector<int>& key,std::vector<float>& value, bool mask) {
   std::map<int,float> m = aHit.GetAllTimes(false);
   std::map<int, float>::iterator it = m.begin();
   while (it != m.end())
    {
        key.push_back(it->first);
        value.push_back(it->second);
        it++;
    }
}
void fixRoot(MuFilterHit& aHit, std::vector<TString>& key,std::vector<float>& value, bool mask) {
   std::map<TString, float> m = aHit.SumOfSignals();
   std::map<TString, float>::iterator it = m.begin();
   while (it != m.end())
    {
        key.push_back(it->first);
        value.push_back(it->second);
        it++;
    }
}

void fixRoot(std::vector<genfit::TrackPoint*>& points, std::vector<int>& d,std::vector<int>& k, bool mask) {
      for(std::size_t i = 0; i < points.size(); ++i) {
        genfit::AbsMeasurement*  m = points[i]->getRawMeasurement();
        d.push_back( m->getDetId() );
        k.push_back( int(m->getHitId()/1000) );
    }
}
""")

Tkey  = ROOT.std.vector('TString')()
Ikey   = ROOT.std.vector('int')()
Value = ROOT.std.vector('float')()

class Monitoring():
   " set of monitor histograms "
   def __init__(self,options,FairTasks):
        self.options = options
        self.EventNumber = -1
# MuFilter mapping of planes and bars 
        self.systemAndPlanes  = {1:2,2:5,3:7}
        self.systemAndBars     = {1:7,2:10,3:60}
        self.systemAndChannels     = {1:[8,0],2:[6,2],3:[1,0]}
        self.sdict                     = {0:'Scifi',1:'Veto',2:'US',3:'DS'}

        self.freq      = 160.E6
        self.TDC2ns = 1E9/self.freq

        path     = options.path
        if path.find('eos')>0:
             path  = options.server+options.path
        if options.online:
             path = path.replace("raw_data","convertedData").replace("data/","")

# setup geometry
        if (options.geoFile).find('../')<0: self.snd_geo = SndlhcGeo.GeoInterface(path+options.geoFile)
        else:                                         self.snd_geo = SndlhcGeo.GeoInterface(options.geoFile[3:])
        self.MuFilter = self.snd_geo.modules['MuFilter']
        self.Scifi       = self.snd_geo.modules['Scifi']
        self.zPos = self.getAverageZpositions()

        self.h = {}   # histogram storage

        self.runNr   = str(options.runNumber).zfill(6)
# presenter file
        self.presenterFile = ROOT.TFile('run'+self.runNr+'.root','recreate')
        self.presenterFile.mkdir('scifi')
        self.presenterFile.mkdir('mufilter')
        self.presenterFile.mkdir('eventdisplay')
        self.FairTasks = {}
        for x in FairTasks:   #  keeps extended methods if from python class
                 self.FairTasks[x.GetName()] = x

# setup input
        if options.online:
            import ConvRawData
            options.chi2Max = 2000.
            options.saturationLimit  = 0.95
            options.stop = False
            options.withGeoFile = True
            self.converter = ConvRawData.ConvRawDataPY()
            self.converter.Init(options)
            self.options.online = self.converter
            self.eventTree = options.online.fSink.GetOutTree()
            for T in FairTasks:
               self.converter.run.AddTask(T)
               T.Init()
            # self.converter.run.Init()
            self.run = self.converter.run
            return
        else:
            partitions = 0
            if path.find('eos')>0:
                dirlist  = str( subprocess.check_output("xrdfs "+options.server+" ls "+options.path,shell=True) )
# single file, before Feb'22
                data = "sndsw_raw_"+self.runNr+".root"
                if  dirlist.find(data)<0:
# check for partitions
                   dirlist  = str( subprocess.check_output("xrdfs "+options.server+" ls "+options.path+"run_"+self.runNr,shell=True) )
                   while 1>0:
                      data = "raw-"+ str(partitions).zfill(4)
                      if dirlist.find(data)>0:
                           partitions+=1
                      else: break
            else:
# check for partitions
                 data = "sndsw_raw_"+self.runNr+".root"
                 dirlist = os.listdir(options.path)
                 if  not data in dirlist:
                     dirlist  = os.listdir(options.path+"run_"+self.runNr)
                     for x in dirlist:
                         data = "raw-"+ str(partitions).zfill(4)
                         if x.find(data)>0:
                             partitions+=1

            if options.runNumber>0:
                eventChain = ROOT.TChain('rawConv')
                if partitions==0:
                   eventChain.Add(path+'sndsw_raw_'+str(options.runNumber).zfill(6)+'.root')
                else:
                   for p in range(partitions):
                       print(partitions,path+'run_'+self.runNr+'/sndsw_raw-'+str(p).zfill(4)+'.root')
                       eventChain.Add(path+'run_'+self.runNr+'/sndsw_raw-'+str(p).zfill(4)+'.root')
            else:
# for MC data
                f=ROOT.TFile.Open(options.fname)
                eventChain = f.cbmsim

            rc = eventChain.GetEvent(0)
# start FairRunAna
            self.run  = ROOT.FairRunAna()
            ioman = ROOT.FairRootManager.Instance()
            ioman.SetTreeName(eventChain.GetName())
            outFile = ROOT.TMemFile('dummy','CREATE')
            source = ROOT.FairFileSource(eventChain.GetCurrentFile())
            if partitions>0:
                  for p in range(1,partitions):
                       source.AddFile(path+'run_'+self.runNr+'/sndsw_raw-'+str(p).zfill(4)+'.root')
            self.run.SetSource(source)
            sink = ROOT.FairRootFileSink(outFile)
            self.run.SetSink(sink)

            for t in FairTasks: 
                self.run.AddTask(t)

#avoiding some error messages
            xrdb = ROOT.FairRuntimeDb.instance()
            xrdb.getContainer("FairBaseParSet").setStatic()
            xrdb.getContainer("FairGeoParSet").setStatic()

            self.run.Init()
            if partitions>0:  self.eventTree = ioman.GetInChain()
            else:                 self.eventTree = ioman.GetInTree()
# add scifi cluster
            self.clusScifi   = ROOT.TClonesArray("sndCluster")
            self.clusScifiBranch    = self.eventTree.Branch("Cluster_Scifi",self.clusScifi,32000,1)
   def updateSource(self,fname):
   # only needed in auto mode
      self.converter.fiN = ROOT.TFile.Open(fname)
      newEntries = M.converter.fiN.event.GetEntries()
      if newEntries>nLast:
         nStart = max(nLast,newEntries-options.Nlast)
         nLast = newEntries
         for b in M.converter.fiN.GetListOfKeys():
            name = b.GetName()
            if name.find('board')!=0: continue
            M.converter.boards[name]=M.converter.fiN.Get(name)

   def makeScifiCluster(self):
      self.clusScifi.Delete()
      index = 0
      hitDict = {}
      for k in range(self.eventTree.Digi_ScifiHits.GetEntries()):
          d = self.eventTree.Digi_ScifiHits[k]
          if not d.isValid(): continue 
          hitDict[d.GetDetectorID()] = k
      hitList = list(hitDict.keys())
      if len(hitList)>0:
          hitList.sort()
          tmp = [ hitList[0] ]
          cprev = hitList[0]
          ncl = 0
          last = len(hitList)-1
          hitlist = ROOT.std.vector("sndScifiHit*")()
          for i in range(len(hitList)):
               if i==0 and len(hitList)>1: continue
               c=hitList[i]
               neighbour = False
               if (c-cprev)==1:    # does not account for neighbours across sipms
                     neighbour = True
                     tmp.append(c)
               if not neighbour  or c==hitList[last]:
                    first = tmp[0]
                    N = len(tmp)
                    hitlist.clear()
                    for aHit in tmp: hitlist.push_back( self.eventTree.Digi_ScifiHits[hitDict[aHit]])
                    aCluster = ROOT.sndCluster(first,N,hitlist,self.Scifi,False)
                    if  self.clusScifi.GetSize() == index: self.clusScifi.Expand(index+10)
                    self.clusScifi[index]=aCluster
                    index+=1
                    if c!=hitList[last]:
                         ncl+=1
                         tmp = [c]
                    elif not neighbour :   # save last channel
                         hitlist.clear()
                         hitlist.push_back( self.eventTree.Digi_ScifiHits[hitDict[c]])
                         aCluster = ROOT.sndCluster(c,1,hitlist,self.Scifi,False)
                         self.clusScifi[index]=aCluster
                         index+=1
               cprev = c

   def GetEvent(self,n):
      if self.options.online:
            self.options.online.executeEvent(n)
            self.eventTree = self.options.online.sTree
      else: 
            self.eventTree.GetEvent(n)
            self.makeScifiCluster()
      self.EventNumber = n
      return self.eventTree

   def publishRootFile(self):
   # try to copy root file with TCanvas to EOS
       self.presenterFile.Close()
       try:
            rc = os.system("xrdcp -f "+self.presenterFile.GetName()+"  "+os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/online")
       except:
            print("copy of root file failed. Token expired?")
       self.presenterFile = ROOT.TFile('run'+self.runNr+'.root','update')

   def updateHtml(self):
      rc = os.system("xrdcp -f "+os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/online.html  . ")
      old = open("online.html")
      oldL = old.readlines()
      old.close()
      tmp = open("tmp.html",'w')
      found = False
      for L in oldL:
           if not L.find(self.runNr)<0: return
           if L.find("https://snd-lhc-monitoring.web.cern.ch/online")>0 and not found:
              r = str(self.options.runNumber)
              Lnew = '            <li> <a href="https://snd-lhc-monitoring.web.cern.ch/online/run.html?file=run'+self.runNr+'.root">run '+r+'</a> \n'
              tmp.write(Lnew)
              found = True
           tmp.write(L)
      tmp.close()
      os.system('cp tmp.html online.html')
      try:
            rc = os.system("xrdcp online.html  "+os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/")
      except:
            print("copy of html failed. Token expired?")
   def systemAndOrientation(self,s,plane):
      if s==1 or s==2: return "horizontal"
      if plane%2==1 or plane == 6: return "vertical"
      return "horizontal"

   def getAverageZpositions(self):
      zPos={'MuFilter':{},'Scifi':{}}
      for s in self.systemAndPlanes:
          for plane in range(self.systemAndPlanes[s]):
             bar = 4
             p = plane
             if s==3 and (plane%2==0 or plane==7): 
                bar = 90
                p = plane//2
             elif s==3 and plane%2==1:
                bar = 30
                p = plane//2
             self.MuFilter.GetPosition(s*10000+p*1000+bar,A,B)
             zPos['MuFilter'][s*10+plane] = (A.Z()+B.Z())/2.
      for s in range(1,6):
         mat   = 2
         sipm = 1
         channel = 64
         for o in range(2):
             self.Scifi.GetPosition(channel+1000*sipm+10000*mat+100000*o+1000000*s,A,B)
             zPos['Scifi'][s*10+o] = (A.Z()+B.Z())/2.
      return zPos

   def smallSiPMchannel(self,i):
      if i==2 or i==5 or i==10 or i==13: return True
      else: return False

#  Scifi specific code
   def Scifi_xPos(self,detID):
        orientation = (detID//100000)%10
        nStation = 2*(detID//1000000-1)+orientation
        mat   = (detID%100000)//10000
        X = detID%1000+(detID%10000)//1000*128
        return [nStation,mat,X]   # even numbers are Y (horizontal plane), odd numbers X (vertical plane)

# decode MuFilter detID
   def MuFilter_PlaneBars(self,detID):
         s = detID//10000
         l  = (detID%10000)//1000  # plane number
         bar = (detID%1000)
         if s>2:
             l=2*l
             if bar>59:
                  bar=bar-60
                  if l<6: l+=1
         return {'station':s,'plane':l,'bar':bar}

   def map2Dict(self,aHit,T='GetAllSignals',mask=True):
      if T=="SumOfSignals":
         key = Tkey
      elif T=="GetAllSignals" or T=="GetAllTimes":
         key = Ikey
      else: 
           print('use case not known',T)
           1/0
      key.clear()
      Value.clear()
      if T=="GetAllTimes": ROOT.fixRootT(aHit,key,Value,mask)
      else:                         ROOT.fixRoot(aHit,key,Value,mask)
      theDict = {}
      for k in range(key.size()):
          if T=="SumOfSignals": theDict[key[k].Data()] = Value[k]
          else: theDict[key[k]] = Value[k]
      return theDict

   def fit_langau(self,hist,o,bmin,bmax,opt=''):
      if opt == 2:
         params = {0:'Width(scale)',1:'mostProbable',2:'norm',3:'sigma',4:'N2'}
         F = ROOT.TF1('langau',langaufun,0,200,len(params))
      else:
         params = {0:'Width(scale)',1:'mostProbable',2:'norm',3:'sigma'}
         F = ROOT.TF1('langau',twoLangaufun,0,200,len(params))
      for p in params: F.SetParName(p,params[p])
      rc = hist.Fit('landau','S'+o,'',bmin,bmax)
      res = rc.Get()
      if not res: return res
      F.SetParameter(2,res.Parameter(0))
      F.SetParameter(1,res.Parameter(1))
      F.SetParameter(0,res.Parameter(2))
      F.SetParameter(3,res.Parameter(2))
      F.SetParameter(4,0)
      F.SetParLimits(0,0,100)
      F.SetParLimits(1,0,100)
      F.SetParLimits(3,0,10)
      rc = hist.Fit(F,'S'+o,'',bmin,bmax)
      res = rc.Get()
      return res

   def twoLangaufun(self,x,par):
      N1 = self.langaufun(x,par)
      par2 = [par[0],par[1]*2,par[4],par[3]]
      N2 = self.langaufun(x,par2)
      return N1+abs(N2)

   def  langaufun(self,x,par):
   #Fit parameters:
   #par[0]=Width (scale) parameter of Landau density
   #par[1]=Most Probable (MP, location) parameter of Landau density
   #par[2]=Total area (integral -inf to inf, normalization constant)
   #par[3]=Width (sigma) of convoluted Gaussian function
   #
   #In the Landau distribution (represented by the CERNLIB approximation),
   #the maximum is located at x=-0.22278298 with the location parameter=0.
   #This shift is corrected within this function, so that the actual
   #maximum is identical to the MP parameter.
#
      # Numeric constants
      invsq2pi = 0.3989422804014   # (2 pi)^(-1/2)
      mpshift  = -0.22278298       # Landau maximum location
#
      # Control constants
      np = 100.0      # number of convolution steps
      sc =   5.0      # convolution extends to +-sc Gaussian sigmas
#
      # Variables
      summe = 0.0
#
      # MP shift correction
      mpc = par[1] - mpshift * par[0]
#
      # Range of convolution integral
      xlow = max(0,x[0] - sc * par[3])
      xupp = x[0] + sc * par[3]
#
      step = (xupp-xlow) / np
#
      # Convolution integral of Landau and Gaussian by sum
      i=1.0
      if par[0]==0 or par[3]==0: return 9999
      while i<=np/2:
         i+=1
         xx = xlow + (i-.5) * step
         fland = ROOT.TMath.Landau(xx,mpc,par[0]) / par[0]
         summe += fland * ROOT.TMath.Gaus(x[0],xx,par[3])
#
         xx = xupp - (i-.5) * step
         fland = ROOT.TMath.Landau(xx,mpc,par[0]) / par[0]
         summe += fland * ROOT.TMath.Gaus(x[0],xx,par[3])
#
      return (par[2] * step * summe * invsq2pi / par[3])

   def myPrint(self,tc,name,subdir='',withRootFile=True):
     srun = 'run'+str(self.options.runNumber)
     tc.Update()
     if withRootFile:
         self.presenterFile.cd(subdir)
         tc.Write()
     else:
         if not os.path.isdir(srun): os.system('mkdir '+srun)
         pname = srun+'/'+name+'-'+srun
         tc.Print(pname+'.png')
         tc.Print(pname+'.pdf')
