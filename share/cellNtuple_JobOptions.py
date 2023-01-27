import glob

# In order to run on 21.9 samples you need the following settings. These can be added in a preInclude.py file or pasted at the top of joboptions file.
from AthenaCommon.GlobalFlags import globalflags
globalflags.DataSource.set_Value_and_Lock("geant4")
DetDescrVersion="ATLAS-P2-ITK-23-00-03"
ConditionsTag="OFLCOND-MC15c-SDR-14-03"
globalflags.DetDescrVersion.set_Value_and_Lock(DetDescrVersion)
include("InDetSLHC_Example/preInclude.NoTRT_NoBCM_NoDBM.py")
include("InDetSLHC_Example/preInclude.SLHC_Setup.py")
include("InDetSLHC_Example/preInclude.SLHC_Setup_Strip_GMX.py")
include("InDetSLHC_Example/preInclude.SLHC_Calorimeter_mu200.py")


if not "FilesInput" in dir():
    FilesInput=glob.glob("../../mc15_14TeV/mc15_14TeV.600012.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.recon.AOD.e8185_s3770_s3773_r13644/*pool.root.1")
    
#Input file
#from PyUtils import AthFile
#import AthenaPoolCnvSvc.ReadAthenaPool                 #sets up reading of POOL files (e.g. xAODs)
#from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
#svcMgr.EventSelector.InputCollections=files
#athenaCommonFlags.FilesInput = svcMgr.EventSelector.InputCollections
#include( "RecExCommon/ContainerRemapping.py" )

jps.AthenaCommonFlags.FilesInput = FilesInput
#svcMgr.EventSelector.InputCollections=FilesInput


    
# Run over all events
#theApp.EvtMax=100

#jps.AthenaCommonFlags.AccessMode = "POOLAccess"
# Give path to input file.
#jps.AthenaCommonFlags.FilesInput = [ "path_to_input_file" ]

# Register the output files. The upper-case stream names are used in the code in GepOutputReader. The names of the ROOT files can be changed.
produceCaloCellsMap = False
produceHist = False
produceNtuples = True

if(produceCaloCellsMap):
    jps.AthenaCommonFlags.HistOutputs = ["STREAM_CALOMAP:CaloCellsMap.root"]
if(produceHist):
    jps.AthenaCommonFlags.HistOutputs = ["STREAM_HIST:myfile_hist.root"]
if(produceNtuples):
    jps.AthenaCommonFlags.HistOutputs = ["STREAM_TREE:myfile_tree.root"]

# Flags for ntuple information
getCellsInfo = True
getEventInfo = True

# Choose the algorithms to run
topoclAlgs=['Calo422', 'Calo420']
puSupprAlgs=['', 'SK']
jetAlgs=[]

svcMgr.THistSvc.MaxFileSize = -1 #disable check for perf improvement

# Add the respective sequences to the main sequence.
from AthenaCommon.AlgSequence import AlgSequence
athAlgSeq = AlgSequence()

from TrigL0GepPerf.L0GepSimulationSequence import setupL0GepSimulationSequence
setupL0GepSimulationSequence( topoclAlgs=topoclAlgs,
                              jetAlgs=jetAlgs,
                              puSupprAlgs=puSupprAlgs )

from GepOutputReader.GepOutputReaderSequence import setupGepOutputReaderSequence

setupGepOutputReaderSequence( produceCaloCellsMap=produceCaloCellsMap,
                              produceHist=produceHist,
                              produceNtuples=produceNtuples,
                              topoclAlgs=topoclAlgs,
                              jetAlgs=jetAlgs,
                              puSupprAlgs=puSupprAlgs,
                              getCellsInfo=getCellsInfo,
                              getEventInfo=getEventInfo )

# Set the detector information.
from RecExConfig import AutoConfiguration
AutoConfiguration.ConfigureSimulationOrRealData()
AutoConfiguration.ConfigureConditionsTag()
from AthenaCommon.DetFlags import DetFlags
DetFlags.all_setOff()
DetFlags.detdescr.Calo_setOn()
include("RecExCond/AllDet_detDescr.py")

# Reduce logging - but don't suppress messages
include("AthAnalysisBaseComps/SuppressLogging.py")
MessageSvc.defaultLimit = 9999999
MessageSvc.useColors = True
MessageSvc.Format = "% F%35W%S%7W%R%T %0W%M"

# Execution statistics
#from AthenaCommon.AppMgr import theAuditorSvc
#from GaudiAud.GaudiAudConf import ChronoAuditor
#theAuditorSvc += ChronoAuditor()
#theApp.AuditAlgorithms = True
