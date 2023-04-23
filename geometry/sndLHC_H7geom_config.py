import ROOT as r
import shipunit as u
from ShipGeoConfig import AttrDict, ConfigRegistry


with ConfigRegistry.register_config("basic") as c:
# cave parameters
        c.cave = AttrDict(z=0*u.cm)

        # Antonia, 482000mm (FASER+2, P3) + 1017mm (DZ) + 245mm (centre emulsion),z=483262./10.*u.cm
        # centre emulsion now 326.2cm downstream from origin.
        #c.EmulsionDet = AttrDict(z=326.2*u.cm)
        #c.EmulsionDet.PassiveOption = 1 #0 makes emulsion volumes active, 1 makes all emulsion volumes passive
        #c.EmulsionDet.row = 2
        #c.EmulsionDet.col = 2
        #c.EmulsionDet.wall= 0
        #c.EmulsionDet.target = 0  #number of neutrino target volumes
        #c.EmulsionDet.n_plates = 0
        #c.EmulsionDet.EmTh = 0.0070 * u.cm
        #c.EmulsionDet.EmX = 19.2 * u.cm
        #c.EmulsionDet.EmY = 19.2 * u.cm
        #c.EmulsionDet.PBTh = 0.0175 * u.cm
        #c.EmulsionDet.PassiveTh = 0.1 * u.cm
        #c.EmulsionDet.EPlW = 2* c.EmulsionDet.EmTh + c.EmulsionDet.PBTh
        #c.EmulsionDet.AllPW = c.EmulsionDet.PassiveTh + c.EmulsionDet.EPlW

        #c.EmulsionDet.BrPackZ = 0.*u.cm
        #c.EmulsionDet.BrPackX = 2*0.05*u.cm
        #c.EmulsionDet.BrPackY = 2*0.05*u.cm
        #
        #c.EmulsionDet.BrX = c.EmulsionDet.EmX + c.EmulsionDet.BrPackX
        #c.EmulsionDet.BrY = c.EmulsionDet.EmY + c.EmulsionDet.BrPackY
        #c.EmulsionDet.BrZ = c.EmulsionDet.n_plates * c.EmulsionDet.AllPW + c.EmulsionDet.EPlW + c.EmulsionDet.BrPackZ

        #c.EmulsionDet.xdim = 42.2 *u.cm #external wall dimensions
        #c.EmulsionDet.ydim = 42.2 *u.cm
        #c.EmulsionDet.TotalWallZDim = 10.0 *u.cm #wall dimension along z, including border
        #c.EmulsionDet.WallXDim = 38.6 *u.cm #internal wall dimensions
        #c.EmulsionDet.WallYDim = 38.6 *u.cm
        #c.EmulsionDet.WallZDim = 8.15 *u.cm
        #c.EmulsionDet.WallZBorder_offset = 4.75 * u.mm
        #c.EmulsionDet.TTz = 3.0*u.cm
        #c.EmulsionDet.zdim = c.EmulsionDet.wall* c.EmulsionDet.TotalWallZDim + c.EmulsionDet.wall*c.EmulsionDet.TTz
        #c.EmulsionDet.ShiftX = -8.0*u.cm - c.EmulsionDet.xdim/2.
        #c.EmulsionDet.ShiftY = 15.5*u.cm + c.EmulsionDet.ydim/2.

        #c.EmulsionDet.startpos =  -25.4750 * u.cm + c.EmulsionDet.z
        #c.EmulsionDet.zC = c.EmulsionDet.startpos + c.EmulsionDet.zdim/2.
        #
        ## survey points in survey coordinate system!
        #c.EmulsionDet.Xpos0,c.EmulsionDet.Ypos0,c.EmulsionDet.Zpos0 = 5.74*u.cm, 288.89*u.cm, 16.63*u.cm
        #c.EmulsionDet.Xpos1,c.EmulsionDet.Ypos1,c.EmulsionDet.Zpos1 = 5.74*u.cm, 301.89*u.cm, 16.63*u.cm
        #c.EmulsionDet.Xpos2,c.EmulsionDet.Ypos2,c.EmulsionDet.Zpos2 = 5.74*u.cm, 314.89*u.cm, 16.63*u.cm
        #c.EmulsionDet.Xpos3,c.EmulsionDet.Ypos3,c.EmulsionDet.Zpos3 = 5.74*u.cm, 327.89*u.cm, 16.63*u.cm
        #c.EmulsionDet.Xpos4,c.EmulsionDet.Ypos4,c.EmulsionDet.Zpos4 = 5.74*u.cm, 340.89*u.cm, 16.63*u.cm

        #SciFi parameters
        c.H7_Scifi = AttrDict(z=0*u.cm)
        c.H7_Scifi.xdim = 13.0 * u.cm #sensitive only, real 13cm
        c.H7_Scifi.ydim = 13.0 * u.cm 
        c.H7_Scifi.zdim = 3*u.cm 
        c.H7_Scifi.DZ = 1 * u.cm 
        c.H7_Scifi.nmats = 1
        c.H7_Scifi.nscifi   = 0

        #SiPM parameters
        c.H7_Scifi.channel_width     = 0.25 *u.mm
        c.H7_Scifi.sipm_edge = 0.17*u.mm    # on both ends
        c.H7_Scifi.charr_gap = 0.2 *u.mm
        c.H7_Scifi.charr_width = 64 * c.H7_Scifi.channel_width
        c.H7_Scifi.sipm_diegap     = 0.06*u.mm
        c.H7_Scifi.SiPMarray_width = c.H7_Scifi.sipm_edge+c.H7_Scifi.charr_width+c.H7_Scifi.charr_gap+c.H7_Scifi.charr_width+c.H7_Scifi.sipm_edge
        c.H7_Scifi.nsipm_channels  = 128
        c.H7_Scifi.nsipm_mat             = 4
        c.H7_Scifi.nsipms = c.H7_Scifi.nsipm_mat *  c.H7_Scifi.nmats  # 12 per SciFi plane
        c.H7_Scifi.sipmarr_width  = c.H7_Scifi.charr_gap + 2.*c.H7_Scifi.charr_width
        c.H7_Scifi.firstChannelX = -19.528*u.cm  # to agree with SiPM positions of engineering design

        c.H7_Scifi.nfibers_shortrow = 471
        c.H7_Scifi.nfibers_longrow  = 472
        c.H7_Scifi.nfibers_z = 6
        
# Guido: Fibre mat total width 500um less wide than 4 SiPM arrays mounted on a single bar, therefore 32.6mm x 4 -0.5=129.9mm 
        c.H7_Scifi.scifimat_width = (c.H7_Scifi.SiPMarray_width+c.H7_Scifi.sipm_diegap)*c.H7_Scifi.nsipm_mat -0.5*u.mm
        c.H7_Scifi.scifimat_length = c.H7_Scifi.ydim
        c.H7_Scifi.scifimat_z = 0.135 *u.cm
        c.H7_Scifi.epoxymat_z = 0.17 *u.cm
        c.H7_Scifi.scifimat_gap = 0.05 *u.cm
        
        c.H7_Scifi.fiber_length = c.H7_Scifi.scifimat_length
        c.H7_Scifi.scintcore_rmax = 0.011 *u.cm  
        c.H7_Scifi.clad1_rmax = 0.01175 *u.cm    
        c.H7_Scifi.clad2_rmax = 0.0125 *u.cm

        c.H7_Scifi.horizontal_pitch = 0.0275 *u.cm
        c.H7_Scifi.vertical_pitch = 0.021 *u.cm
        c.H7_Scifi.rowlong_offset = 0.035 *u.cm 
        c.H7_Scifi.rowshort_offset = 0.0215 *u.cm 

        c.H7_Scifi.carbonfiber_z = 0.02 *u.cm
        c.H7_Scifi.honeycomb_z = 0.5 *u.cm
       
        c.H7_Scifi.plastbar_x = 1.5 *u.cm
        c.H7_Scifi.plastbar_y = c.H7_Scifi.ydim
        c.H7_Scifi.plastbar_z = 0.195 *u.cm

        c.H7_Scifi.scifi_separation = 10*u.cm 
	#Candidate for z position 
        c.H7_Scifi.offset_z = - 100*u.cm  #SciFi starts at the end of the first ECC
       
        c.H7_Scifi.timeResol = 150.*u.picosecond

        # absolute edge point positions in survey coordinate system
        #c.H7_MuFilter.H7_BC_ScintX      = -33.08*u.cm
        #c.H7_MuFilter.H7_BC_ScintY      = 29.15*u.cm
#        c.H7_Scifi.Xpos0,c.H7_Scifi.Ypos0,c.H7_Scifi.Zpos0 = 4.34*u.cm, 298.94*u.cm, 15.22*u.cm
#        c.H7_Scifi.Xpos1,c.H7_Scifi.Ypos1,c.H7_Scifi.Zpos1 = 4.34*u.cm, 311.94*u.cm, 15.22*u.cm
#        c.H7_Scifi.Xpos2,c.H7_Scifi.Ypos2,c.H7_Scifi.Zpos2 = 4.34*u.cm, 324.94*u.cm, 15.22*u.cm
        c.H7_Scifi.Xpos0,c.H7_Scifi.Ypos0,c.H7_Scifi.Zpos0 = -33.08*u.cm, 29.15*u.cm, 20*u.cm
        c.H7_Scifi.Xpos1,c.H7_Scifi.Ypos1,c.H7_Scifi.Zpos1 = -33.08*u.cm, 29.15*u.cm, 25*u.cm
        c.H7_Scifi.Xpos2,c.H7_Scifi.Ypos2,c.H7_Scifi.Zpos2 = -33.08*u.cm, 29.15*u.cm, 30*u.cm

# H7_Scifi technical drawing, distance from first channel on vertical / horizontal plane to edge point  225,225,0, xy plane z perpendicularc.H7_Scifi.ydim
        c.H7_Scifi.EdgeAX, c.H7_Scifi.EdgeAY, c.H7_Scifi.EdgeAZ =  225*u.mm, 225*u.mm, 0*u.mm

        c.H7_Scifi.FirstChannelVX,c.H7_Scifi.FirstChannelVY,c.H7_Scifi.FirstChannelVZ = -195.28*u.mm, -200.0*u.mm, -12.92*u.mm

        c.H7_Scifi.FirstChannelHX,c.H7_Scifi.FirstChannelHY,c.H7_Scifi.FirstChannelHZ = -200.0*u.mm, -195.28*u.mm, -7.07*u.mm

# Local H7_Scifi position of first channel on a vertical scifi plane in software
        c.H7_Scifi.LfirstChannelVX,c.H7_Scifi.LfirstChannelVY,c.H7_Scifi.LfirstChannelVZ = -195.135*u.mm, 195.0*u.mm, 11.85*u.mm   # sipm on top

# Local H7_Scifi position of last channel (=first channel on technical drawing) on a horizontal scifi plane in software
        c.H7_Scifi.LfirstChannelHX,c.H7_Scifi.LfirstChannelHY,c.H7_Scifi.LfirstChannelHZ = -195.0*u.mm, 195.178*u.mm,  6.25*u.mm  # sipm on the right side direction away from IP1

 # relative mat alignments
        c.H7_Scifi.LocM100,c.H7_Scifi.LocM101,c.H7_Scifi.LocM102 =  0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM110,c.H7_Scifi.LocM111,c.H7_Scifi.LocM112=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM200,c.H7_Scifi.LocM201,c.H7_Scifi.LocM202=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM210,c.H7_Scifi.LocM211,c.H7_Scifi.LocM212 =  0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM300,c.H7_Scifi.LocM301,c.H7_Scifi.LocM302=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM310,c.H7_Scifi.LocM311,c.H7_Scifi.LocM312=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM400,c.H7_Scifi.LocM401,c.H7_Scifi.LocM402 =  0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM410,c.H7_Scifi.LocM411,c.H7_Scifi.LocM412=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM500,c.H7_Scifi.LocM501,c.H7_Scifi.LocM502=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM510,c.H7_Scifi.LocM511,c.H7_Scifi.LocM512=   0.0*u.um,     0.0*u.um,          0.0*u.um

        c.H7_MuFilter = AttrDict(z=0*u.cm)
        #coordinates in local gravity based system
        c.H7_MuFilter.Veto1Dx,c.H7_MuFilter.Veto1Dy,c.H7_MuFilter.Veto1Dz = 44.5*u.mm,    2798*u.mm, 185.9*u.mm
        c.H7_MuFilter.Veto2Dx,c.H7_MuFilter.Veto2Dy,c.H7_MuFilter.Veto2Dz = 44.5*u.mm,    2839*u.mm, 165.9*u.mm
        c.H7_MuFilter.Iron1Dx, c.H7_MuFilter.Iron1Dy, c.H7_MuFilter.Iron1Dz = -24.2*u.mm, 3579.6*u.mm, 146.6*u.mm
        # US1
        c.H7_MuFilter.Muon1Dx,c.H7_MuFilter.Muon1Dy,c.H7_MuFilter.Muon1Dz = -47.1*u.mm, 3760.2*u.mm, 146.6*u.mm
        c.H7_MuFilter.Iron2Dx,  c.H7_MuFilter.Iron2Dy,   c.H7_MuFilter.Iron2Dz   = -24.2*u.mm,  3804.6*u.mm, 136.6*u.mm
        # US2
        c.H7_MuFilter.Muon2Dx,c.H7_MuFilter.Muon2Dy,c.H7_MuFilter.Muon2Dz = -47.1*u.mm, 3985.2*u.mm, 136.6*u.mm
        c.H7_MuFilter.Iron3Dx,  c.H7_MuFilter.Iron3Dy,   c.H7_MuFilter.Iron3Dz    = -24.2*u.mm, 4029.6*u.mm, 126.6*u.mm
        # US3
        c.H7_MuFilter.Muon3Dx,c.H7_MuFilter.Muon3Dy,c.H7_MuFilter.Muon3Dz = -47.1*u.mm, 4210.2*u.mm, 126.6*u.mm
        c.H7_MuFilter.Iron4Dx,  c.H7_MuFilter.Iron4Dy,   c.H7_MuFilter.Iron4Dz    = -24.2*u.mm, 4254.6*u.mm, 116.7*u.mm
        # US4
        c.H7_MuFilter.Muon4Dx,c.H7_MuFilter.Muon4Dy,c.H7_MuFilter.Muon4Dz = -47.1*u.mm, 4435.2*u.mm, 116.7*u.mm
        c.H7_MuFilter.Iron5Dx,   c.H7_MuFilter.Iron5Dy,  c.H7_MuFilter.Iron5Dz    = -24.2*u.mm, 4479.6*u.mm, 127.7*u.mm    # 0 +225.0mm 0
        # US5
        c.H7_MuFilter.Muon5Dx,c.H7_MuFilter.Muon5Dy,c.H7_MuFilter.Muon5Dz = -47.1*u.mm, 4660.2*u.mm, 127.7*u.mm
        c.H7_MuFilter.Iron6Dx,   c.H7_MuFilter.Iron6Dy,  c.H7_MuFilter.Iron6Dz    = -24.2*u.mm, 4704.6*u.mm,127.7*u.mm     # 0 +225.0mm 0
        # DS1
        c.H7_MuFilter.Muon6Dx,c.H7_MuFilter.Muon6Dy,c.H7_MuFilter.Muon6Dz = -47.1*u.mm, 4884.9*u.mm, 127.7*u.mm
        c.H7_MuFilter.Iron7Dx,   c.H7_MuFilter.Iron7Dy,  c.H7_MuFilter.Iron7Dz    = -24.2*u.mm, 4943.6*u.mm, 127.7*u.mm       # 0 +239.0mm 0
        # DS2
        c.H7_MuFilter.Muon7Dx,c.H7_MuFilter.Muon7Dy,c.H7_MuFilter.Muon7Dz = -47.1*u.mm, 5123.9*u.mm, 127.7*u.mm
        c.H7_MuFilter.Iron8Dx,   c.H7_MuFilter.Iron8Dy,  c.H7_MuFilter.Iron8Dz    = -24.2*u.mm, 5183.9*u.mm, 127.7*u.mm        # 0 +240.3mm 0 
        # DS3
        c.H7_MuFilter.Muon8Dx,c.H7_MuFilter.Muon8Dy,c.H7_MuFilter.Muon8Dz = -4.7*u.mm, 5383.7*u.mm, 127.7*u.mm

        c.H7_MuFilter.DS4ZGap = 8.82*u.cm
        # DS4V
        c.H7_MuFilter.Muon9Dx,c.H7_MuFilter.Muon9Dy,c.H7_MuFilter.Muon9Dz = -4.7*u.mm,    5383.7*u.mm + c.H7_MuFilter.DS4ZGap, 127.7*u.mm
        c.H7_MuFilter.Iron9Dx,  c.H7_MuFilter.Iron9Dy,   c.H7_MuFilter.Iron9Dz    = 175.8*u.mm, 5529.7*u.mm, 127.7*u.mm

        # relation between edge and bottom bar for VETO
        c.H7_MuFilter.VETOLocX,c.H7_MuFilter.VETOLocY,c.H7_MuFilter.VETOLocZ = 20.0*u.mm,20.0*u.mm,46.7*u.mm

        # relation between edge and bottom bar for US and DS
        c.H7_MuFilter.DSHLocX,c.H7_MuFilter.DSHLocY,c.H7_MuFilter.DSHLocZ      = 10.5*u.mm, 32.0*u.mm, 11.1*u.mm
        # relation between edge and right bar
        c.H7_MuFilter.DSVLocX,c.H7_MuFilter.DSVLocY,c.H7_MuFilter.DSVLocZ       = 623.0*u.mm, 47.0*u.mm, 641.3*u.mm

        # offsets in Z of first US bar 
        c.H7_MuFilter.USOffZ1 = 4.35*u.mm
        c.H7_MuFilter.USOffZ2 = 5.0*u.mm
        c.H7_MuFilter.USOffZ3 = 4.2*u.mm
        c.H7_MuFilter.USOffZ4 = 5.21*u.mm
        c.H7_MuFilter.USOffZ5 = 4.74*u.mm

        #Veto station parameters
        c.H7_MuFilter.VetonSiPMs = 8
        c.H7_MuFilter.VetonSides  = 2
        c.H7_MuFilter.NVetoPlanes = 2
        c.H7_MuFilter.NVetoBars    = 7

        c.H7_MuFilter.VetoBarX,c.H7_MuFilter.VetoBarY,c.H7_MuFilter.VetoBarZ = 42 *u.cm, 6 * u.cm, 1 * u.cm
        c.H7_MuFilter.VetoBarGap = 2*30*u.um  # wrapping material

        c.H7_MuFilter.FeX,c.H7_MuFilter.FeY,c.H7_MuFilter.FeZ                  = 80*u.cm, 60*u.cm, 20*u.cm
        c.H7_MuFilter.FeEndX,c.H7_MuFilter.FeEndY,c.H7_MuFilter.FeEndZ = 40*u.cm, 40*u.cm, 20*u.cm
        c.H7_MuFilter.FeBotX,c.H7_MuFilter.FeBotY,c.H7_MuFilter.FeBotZ   = 80*u.cm,   9*u.cm, 40*u.cm

        c.H7_MuFilter.UpstreamDetZ = 2.6*u.cm
        c.H7_MuFilter.UpstreamnSiPMs = 8
        c.H7_MuFilter.UpstreamnSides = 2
        c.H7_MuFilter.NUpstreamPlanes = 5
        c.H7_MuFilter.DownstreamDetZ = 3.9*u.cm
        c.H7_MuFilter.DownstreamnSiPMs = 1
        c.H7_MuFilter.DownstreamnSides = 2   # only for horizontal, vertical only one side
        c.H7_MuFilter.NDownstreamPlanes = 1
        #upstream bars configuration
        c.H7_MuFilter.NUpstreamBars = 10
        c.H7_MuFilter.UpstreamBarX,c.H7_MuFilter.UpstreamBarY,c.H7_MuFilter.UpstreamBarZ = 82.525*u.cm, 6.0*u.cm, 1.0*u.cm
        c.H7_MuFilter.UpstreamBarGap = 0.1*u.mm

        #downstream bars configuration
        c.H7_MuFilter.NDownstreamBars = 60 #n.d.r. both for x and y in this case
        c.H7_MuFilter.DownstreamBarX,c.H7_MuFilter.DownstreamBarY,c.H7_MuFilter.DownstreamBarZ = 82.525*u.cm, 1*u.cm, 1*u.cm
        c.H7_MuFilter.DownstreamBarGap = 0.1*u.mm
        c.H7_MuFilter.DownstreamBarX_ver,c.H7_MuFilter.DownstreamBarY_ver,c.H7_MuFilter.DownstreamBarZ_ver = 1*u.cm, 63.525*u.cm, 1*u.cm

        # DS and US support box, inner, Z pointing upward
        c.H7_MuFilter.SupportBoxD  = 0.5*u.mm  # empty space between bars and box
        c.H7_MuFilter.SupportBoxW = 2*u.mm
        c.H7_MuFilter.DSBoxX1        = c.H7_MuFilter.DSHLocX - c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.DSBoxX2        = c.H7_MuFilter.DSHLocX + c.H7_MuFilter.DownstreamBarX + c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.DSBoxZ1        = c.H7_MuFilter.DSHLocZ - c.H7_MuFilter.DownstreamBarY/2 - c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.DSBoxZ2        = c.H7_MuFilter.DSVLocZ + c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.DSBoxY1        = c.H7_MuFilter.DSHLocY - c.H7_MuFilter.DownstreamBarZ/2 - c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.DSBoxY2        = c.H7_MuFilter.DSVLocY + c.H7_MuFilter.DownstreamBarZ/2 + c.H7_MuFilter.SupportBoxD

        c.H7_MuFilter.USBoxY1        = c.H7_MuFilter.DSHLocY - c.H7_MuFilter.DownstreamBarZ/2 - c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.USBoxY2        = c.H7_MuFilter.DSHLocY + c.H7_MuFilter.DownstreamBarZ/2 + c.H7_MuFilter.SupportBoxD

        c.H7_MuFilter.H7_Tthick=Tthick*u.cm
        
        #Slice thicknesses
        c.H7_MuFilter.H7_TT1=c.H7_MuFilter.H7_Tthick/3
        c.H7_MuFilter.H7_TT2=c.H7_MuFilter.H7_Tthick/3
        c.H7_MuFilter.H7_TT3=c.H7_MuFilter.H7_Tthick/3

	#Segmented Target SciFit thickness
        c.H7_MuFilter.TScintX=0
        c.H7_MuFilter.TScintY=0
        c.H7_MuFilter.TScintZ=0

	#Beam counter Parameters

        c.H7_MuFilter.H7_BC_Scint_rad   = 5*u.mm
        c.H7_MuFilter.H7_BC_Scint_thick = 5*u.mm
        c.H7_MuFilter.H7_BC_ScintX      = -33.08*u.cm
        c.H7_MuFilter.H7_BC_ScintY      = 29.15*u.cm
        #for Tthick=29.5
        #c.H7_MuFilter.H7_BC_ScintZ      = 45.705*u.cm
        #c.H7_MuFilter.H7_BC_ScintZ      = 75.205-c.H7_MuFilter.H7_Tthick
        c.H7_MuFilter.H7_BC_ScintZ      = 0 

       # VETO support box
        c.H7_MuFilter.SupportBoxVW = 4*u.mm
        c.H7_MuFilter.VETOBoxX1        = c.H7_MuFilter.VETOLocX - c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.VETOBoxX2        = c.H7_MuFilter.VETOLocX + c.H7_MuFilter.VetoBarX + c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.VETOBoxZ1        = c.H7_MuFilter.VETOLocZ - c.H7_MuFilter.VetoBarY/2 - c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.VETOBoxZ2        = c.H7_MuFilter.VETOLocZ + (c.H7_MuFilter.NVetoBars-1)*(c.H7_MuFilter.VetoBarY+c.H7_MuFilter.VetoBarGap) + c.H7_MuFilter.VetoBarY/2 + c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.VETOBoxY1        = c.H7_MuFilter.VETOLocY - c.H7_MuFilter.VetoBarZ/2 - c.H7_MuFilter.SupportBoxD
        c.H7_MuFilter.VETOBoxY2        = c.H7_MuFilter.VETOLocY + c.H7_MuFilter.VetoBarZ/2 + c.H7_MuFilter.SupportBoxD

       #digitization parameters
        c.H7_MuFilter.DsAttenuationLength   =  350 * u.cm                #  values between 300 cm and 400cm observed for H6 testbeam
        c.H7_MuFilter.DsTAttenuationLength =  700 * u.cm                # top readout with mirror on bottom
        c.H7_MuFilter.VandUpAttenuationLength = 999 * u.cm        # no significante attenuation observed for H6 testbeam
        c.H7_MuFilter.VandUpSiPMcalibrationL    = 25.*1000.       # 1.65 MeV = 41 qcd 
        c.H7_MuFilter.VandUpSiPMcalibrationS    = 25.*1000.
        c.H7_MuFilter.DsSiPMcalibration             = 25.*1000.
        c.H7_MuFilter.timeResol = 150.*u.picosecond
        c.H7_MuFilter.VandUpPropSpeed    = 12.5*u.cm/u.nanosecond
        c.H7_MuFilter.DsPropSpeed        = 14.3*u.cm/u.nanosecond

        c.Floor = AttrDict(z=48000.*u.cm) # to place tunnel in SND_@LHC coordinate system
        c.Floor.DX = 1.0*u.cm 
        c.Floor.DY = -4.5*u.cm #  subtract 4.5cm to avoid overlaps 
        c.Floor.DZ = 0.

# for H6 / H8 testbeam and commissioning
        c.Floor.z = 0   # no tunnel, no slope
        c.H7_MuFilter.Iron9Dy = 0*u.mm # move iron blocks at the end out of the way
# scifi ed 46cm behind the iron block of second DS station and lifted by 10-15 cm.
# equal move H7_MuFilter in front of target and lower by 10-15cm, from 289 to 538+46, delta = -295
        c.H7_MuFilter.ShiftX =   4.5*u.cm
        c.H7_MuFilter.ShiftY =   -15.5*u.cm
        c.H7_MuFilter.ShiftZ = -275.0*u.cm            # -295cm was 20cm too much
# for H6eto  placed directly in front of first US
        c.H7_MuFilter.VetoShiftZ = 70*u.cm + c.H7_MuFilter.ShiftZ
        c.H7_MuFilter.VetoShiftX = -13.5*u.cm
        c.H7_MuFilter.VetoShiftY = -17.7*u.cm
# fine astements
        c.H7_MuFilter.Muon8Dx = -4.7*u.mm - 4*u.cm
        c.H7_MuFilter.Muon7Dx = -47.1*u.mm + 0.74*u.cm
        c.H7_MuFilter.Muon1Dz = 146.6*u.mm - 2.3*u.cm
        c.H7_MuFilter.Muon2Dz = 136.6*u.mm - 1.5*u.cm
        c.H7_MuFilter.Muon5Dz = 127.7*u.mm + 0.25*u.cm
        c.H7_MuFilter.Muon7Dz = 127.7*u.mm + 0.25*u.cm
        c.H7_MuFilter.Muon8Dz = 127.7*u.mm + 0.56*u.cm
# from tk alignment
        #c.H7_Scifi.Zpos0+=  20.00  *u.cm
        #c.H7_Scifi.Xpos0+=  -1177.09  *u.um
        #c.H7_Scifi.Zpos1+=  25.00  *u.cm
        #c.H7_Scifi.Xpos1+=  -810.00  *u.um
        #c.H7_Scifi.Zpos2+=   30.00  *u.cm
        #c.H7_Scifi.Xpos2+=  1602.8  *u.um
        #c.H7_Scifi.Zpos3+=  162.62  *u.um
        #c.H7_Scifi.Xpos3+=  -322.53  *u.um
        #c.H7_Scifi.Zpos4+=  229.08  *u.um
        #c.H7_Scifi.Xpos4+= -122.04  *u.um
# relatimat alignments
        c.H7_Scifi.LocM100,c.H7_Scifi.LocM101,c.H7_Scifi.LocM102 =  0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM110,c.H7_Scifi.LocM111,c.H7_Scifi.LocM112=   14.91*u.um, -29.82*u.um,     14.91*u.um
        c.H7_Scifi.LocM200,c.H7_Scifi.LocM201,c.H7_Scifi.LocM202=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM210,c.H7_Scifi.LocM211,c.H7_Scifi.LocM212 =  0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM300,c.H7_Scifi.LocM301,c.H7_Scifi.LocM302=   0.0*u.um,     0.0*u.um,          0.0*u.um
        c.H7_Scifi.LocM310,c.H7_Scifi.LocM311,c.H7_Scifi.LocM312=   30.80*u.um, -61.61*u.um,     30.80*u.um
        c.H7_Scifi.LocM400,c.H7_Scifi.LocM401,c.H7_Scifi.LocM402 = -65.64*u.um, -37.62*u.um,     103.25*u.um
        c.H7_Scifi.LocM410,c.H7_Scifi.LocM411,c.H7_Scifi.LocM412=  -1.49*u.um,    24.0*u.um,      -22.52*u.um
        c.H7_Scifi.LocM500,c.H7_Scifi.LocM501,c.H7_Scifi.LocM502=  -0.08*u.um,   -46.78*u.um,      46.86*u.um
        c.H7_Scifi.LocM510,c.H7_Scifi.LocM511,c.H7_Scifi.LocM512=  -230.92*u.um, 292.28*u.um,   -61.36*u.um

