# Create a library called "libMuonShieldBackground" which includes the source files given in
# the array .
# The extension is already found.  Any number of sources could be listed here.
include(CMakePrintHelpers)
cmake_print_variables(VMC_INCLUDE_DIRS)

if(EXISTS "$ENV{PYTHON_HOME}")
 set(PYTHON_LIBRARY $ENV{PYTHON_HOME}/lib)
 set(PYTHON_INCLUDE_DIR $ENV{PYTHON_HOME}/include/python2.7)
endif(EXISTS "$ENV{PYTHON_HOME}")
FIND_PACKAGE(Python3 COMPONENTS Development) 

set(INCLUDE_DIRECTORIES
${CMAKE_SOURCE_DIR}/muonShieldOptimization ${CMAKE_SOURCE_DIR}/veto ${CMAKE_SOURCE_DIR}/shipdata ${VMC_INCLUDE_DIRS} ${Python3_INCLUDE_DIRS}
)

include_directories( ${INCLUDE_DIRECTORIES}   ${FAIRROOT_INCLUDE_DIR} ${FairLogger_INCDIR} ${FMT_INCLUDE_DIR}
)
include_directories(SYSTEM ${SYSTEM_INCLUDE_DIRECTORIES})

cmake_print_variables(INCLUDE_DIRECTORIES)

set(LINK_DIRECTORIES
${ROOT_LIBRARY_DIR}
${FAIRROOT_LIBRARY_DIR}
)
 
link_directories( ${LINK_DIRECTORIES})

set(SRCS
exitHadronAbsorber.cxx
pyFairModule.cxx
simpleTarget.cxx
)

Set(HEADERS )
Set(LINKDEF muonShieldBackgroundLinkDef.h)
Set(LIBRARY_NAME ShipMuonShieldBackground)
Set(DEPENDENCIES Base GeoBase ParBase Geom Core)

GENERATE_LIBRARY()
