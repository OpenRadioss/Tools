# INP to Rad converter

## Description

This Python script converts .inp format to Radioss (.rad) format.
It can be used as a standalone tool or as a plugin to the [OpenRadioss gui tool](https://github.com/OpenRadioss/Tools/tree/main/openradioss_gui).
It is provided “as is”, and should be considered as 'beta' today, but has been successfully tested on a wide range of explicit models and already supports most commonly used element formulations, material laws, loadings and boundary conditions.
Through provision of this tool, we hope to further enhance the accessibility of OpenRadioss by enabling the use of open-source pre-processors supporting the .inp format such as PrePoMax. “ (I put a link to Prepomax)

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
