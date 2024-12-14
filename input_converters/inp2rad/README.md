# INP to Rad converter

## Description

This Python script converts .inp format to Radioss (.rad) format.
It can be used as a standalone tool or as a plugin to the [OpenRadioss gui tool](https://github.com/OpenRadioss/Tools/tree/main/openradioss_gui).
It is provided “as is”, and should be considered as 'beta' today, but has been successfully tested on a wide range of explicit models and already supports most commonly used element formulations, material laws, loadings and boundary conditions.
Through provision of this tool, we hope to further enhance the accessibility of OpenRadioss by enabling the use of open-source pre-processors supporting the .inp format such as [PrePoMax](https://prepomax.fs.um.si).

## Installation

You need to have a python3 installation on Linux or Windows.

* On ***Windows*** : check [python.org](https://www.python.org/) web site to install Python
* On ***Linux***, install python from your OS Repository.

  * On RedHat, CentOS, Rocky Linux

          dnf install python3
          dnf install python3-tkinter

  * On Debian, Ubuntu

          apt-get install python3
          apt install python3-tk

  install the pyinstaller package

  * On Linux as root

          pip3 install pyinstaller
  
  * On Windows

          pip install pyinstaller

Apply the command:

* On ***Windows*** launch

        install.bat

* On ***Linux*** launch as root

        install.sh

This will install the inp2rad.py into Python library collection and inp2rad[.exe] into execution directory


## Supported .inp keywords and Syntax

The convertor aims to support .inp format with a good degree of flexibility, case, spacing and most special characters should be ok, use of ELSET, NSET names inside other ELSET, NSET is supported

Supported keywords: (not all sub-options necessarily supported):

*AMPLITUDE (only TABULAR, default form)

*BOUNDARY (default, SPC type and TYPE=DISPLACEMENT, TYPE=VELOCITY)

*BOUNDARY condition mappings ENCASTR, PINNED, XSYMM, YSYMM, ZSYMM
    
*CLOAD

*COHESIVE SECTION

*CONTACT

*CONTACT PAIR

*CONTACT PROPERTY ASSIGNMENT

*COUPLING, *DISTRIBUTING or *KINEMATIC

*DENSITY

*DISTRIBUTING

*DISTRIBUTING COUPLING

*DLOAD (only GRAV type)

*ELEMENT, *TYPE= 
  
         DCOUP3D
       
         CONN3D2, (RIGID or HINGE)
  
         S3
         
         S3R
         
         M3D3
  
         R3D3
  
         S4
         
         S4R
         
         R3D4
         
         M3D4R
         
         C3D4
         
         C3D6
         
         COH3D6
         
         SC6R
         
         SC8R
         
         C3D8
         
         C3D8I
  
         COH3D8
         
         C3D8R
         
         C3D10
         
         C3D10M

*ELSET, ELSET (GENERATE supported)

*FRICTION

*HYPERELASTIC (MOONEY-RIVLIN, OGDEN forms only)

*HYPERFOAM

*INITIAL CONDITIONS (VELOCITY only)

*KINEMATIC

*KINEMATIC COUPLING

*MASS

*MATERIAL

*MEMBRANE SECTION

*MPC (generates spring beams)

*NODE

*NSET, NSET (GENERATE supported)

*PLASTIC

*RIGID BODY

*SHELL SECTION

*SOLID SECTION

*SURFACE, TYPE=ELEMENT or TYPE=NODE

*TIE

*SURFACE, TYPE=NODE

*SURFACE INTERACTION

*SURFACE INTERACTION, NAME=RADIOSS_GENERAL (special usecase to ease PrePoMax usage, existence of this will result in a global general contact)

*SYSTEM

*UNIAXIAL TEST DATA
