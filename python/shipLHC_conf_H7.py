#!/usr/bin/env python
# -*- coding: latin-1 -*-

import ROOT,os
import shipunit as u
from ShipGeoConfig import ConfigRegistry
detectorList = []

def configure(run,ship_geo,Gfield=''):
# -----Create media-------------------------------------------------
 if hasattr(run,'SetMaterials'):  run.SetMaterials("media.geo")  # Materials
 
# -----Create geometry----------------------------------------------
 cave= ROOT.ShipCave("CAVE")
 cave.SetGeometryFileName("caveWithAir.geo")
 detectorList.append(cave)

 floor = ROOT.Floor()
 for parName in ship_geo.Floor:
    parValue = eval('ship_geo.Floor.'+parName)
    floor.SetConfPar("Floor/"+parName, parValue)
 detectorList.append(floor)
 
# EmulsionDet = ROOT.EmulsionDet("EmulsionDet",ROOT.kTRUE)
# for parName in ship_geo.EmulsionDet:
#    parValue = eval('ship_geo.EmulsionDet.'+parName)
#    EmulsionDet.SetConfPar("EmulsionDet/"+parName, parValue)
# detectorList.append(EmulsionDet)

 H7_Scifi = ROOT.H7_Scifi("H7_Scifi", ROOT.kTRUE)
 for parName in ship_geo.H7_Scifi:
    parValue = eval('ship_geo.H7_Scifi.'+parName)
    H7_Scifi.SetConfPar("H7_Scifi/"+parName, parValue)
 detectorList.append(H7_Scifi)

 H7_MuFilter = ROOT.H7_MuFilter("H7_MuFilter",ROOT.kTRUE)
 for parName in ship_geo.H7_MuFilter:
    parValue = eval('ship_geo.H7_MuFilter.'+parName)
    H7_MuFilter.SetConfPar("H7_MuFilter/"+parName, parValue)
 detectorList.append(H7_MuFilter)

 detElements = {}
 if hasattr(run,'SetMaterials'):  
  for x in detectorList:
    run.AddModule(x)
# return list of detector elements
  for x in run.GetListOfModules(): detElements[x.GetName()]=x
 else:
  for x in detectorList: detElements[x.GetName()]=x
 return detElements
