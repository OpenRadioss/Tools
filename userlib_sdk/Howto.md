# How to build the userlib_sdk

The userlib_sdk must be compiled to generate the sdk library
The SDK exists for linux X86-64, Windows X86-6 and Linux ARMv8-a.

The Supported compiler are:

* On Linux X86-64 : gcc/Gfortran, Intel OneAPI and Intel Compilers prior to OneAPI
* On Windows X86-64 : Intel OneAPI, Intel COmpilers prior to OneAPI, and MinGW (gcc/gfortran porting for Windows).
* On Linux ARM architectures : Armflang and gcc/gfortran

Main build script is _build_script.bash_

           ./build_script.bash
          
           userlib_sdk build script
           -------------------------
          
           Use with arguments :
           -arch=[linux64|linuxa64|win64]
           -compiler=[armflang|gfortran|intel]
                      Defaults :
                        linux64  : gfortran
                        win64    : oneapi
                        linuxa64 : gfortran
           -prec=[dp|sp]
                        set precision - dp (default) |sp

           -verbose : Build verbose mode.
           -clean : delete build


Following page describes how to build the userlib_sdk on the various platforms and compilers.

* [Linux X86-64 and gfortran](#linux-x64-gfortran)
* [Linux X86-64 and Intel OneAPI](#linux-x64-intel-oneapi)
* [Windows X86-64 and Intel OneAPI](#windows-x64-intel-oneapi)
* [Windows X86-64 and MinGW/Gfortran](#windows-x64-mingw-gfortran)
* [Linux ARM-64 and Arm Compilers](#linux-arm64-arm-compilers)
* [Linux ARM-64 and Gfortran](#linux-arm64-gfortran)

## Userlib SDK for linux X86-64

### linux x64 gfortran

#### System and compiler installation

Linux system with glibc version 2.17 or higher:

    * CentOS/RHEL 7, CentOS Stream 8, RHEL 8, Rocky Linux 8, Rocky Linux 9
    * Ubuntu 20.0.4 or higher
    * Windows Subsystem for Linux: OpenRadioss works with WSL/WSL2 Ubuntu 20.04 LTS, WSL2 Ubuntu 22.x

#### Compiler and development tools

You will need GCC/Gfortran version 8 or higher, Cmake version 2.8 or higher, and GNU make.

Install as sudo or root

    * RHEL 7

          yum install devtoolset-8
          yum install make
          yum install cmake

    To enable the devtoolset-8, you can run scl enable devtoolset-8 bash

    * RHEL 8, CentOS Stream 8

         dnf install gcc
         dnf install gcc-gfortran
         dnf install gcc-c++
         dnf install make
         dnf install cmake

    * Ubuntu

         apt-get update
         apt-get upgrade
         apt-get install build-essential
         apt-get install gfortran
         apt-get install cmake

#### How to build userlib_sdk

   * clone the source code from the OpenRadioss_userlib_sdk repository or your fork

         git clone git@github.com:OpenRadioss/OpenRadioss_userlib_sdk.git

   * run `./build_script.bash` :
   
         ./build_script.bash -arch=linux64 -compiler=gfortran

  * Libraries and modules are copied in: 
 
         userlib_sdk/linux64_gfortran

### Linux x64 Intel oneAPI

#### System and compiler installation

Linux system with glibc version 2.17 or higher:

    * CentOS/RHEL 7, CentOS Stream 8, RHEL 8, Rocky Linux 8, Rocky Linux 9
    * Ubuntu 20.0.4 or higher
    * Windows Subsystem for Linux: OpenRadioss works with WSL/WSL2 Ubuntu 20.04 LTS, WSL2 Ubuntu 22.x

#### Compiler and development tools

You will need Cmake version 2.8 or higher, and GNU make.

Install cmake & make as sudo or root

    * RHEL 7, CentOS Stream 8
    
          yum install make
          yum install cmake

    * Ubuntu

         apt-get update
         apt-get upgrade
         apt-get install build-essential
         apt-get install cmake

Download and Install Intel oneAPI for Linux from Intel Web page:

* Visit one API Base Toolkit Download page: [oneAPI Base Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit-download.html)
* Visit one API HPC Toolkit Download page: [oneAPI HPC Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/hpc-toolkit-download.html)

Load the compiler variables :

         call [Path to OneAPI]/compiler/latest/env/vars.sh
         
#### How to build userlib_sdk

   * clone the source code from the OpenRadioss_userlib_sdk repository or your fork

         git clone git@github.com:OpenRadioss/OpenRadioss_userlib_sdk.git

   * apply `./build_script.bash`:
   
         ./build_script.bash -arch=linux64 -compiler=oneapi

  * Libraries and modules are copied in: 
  
         userlib_sdk/linux64_oneapi


## Userlib SDK for Windows X86-64

### Windows x64 Intel oneAPI

#### Compiler Environment

OpenRadioss was tested with oneAPI 2022.3.1 + Visual Studio 2019. Cygwin is used to build OpenRadioss. 
Issues have been found with earlier oneAPI releases. It is not recommended to use previous versions.

This chapter explains how to setup 

1. Intel OneAPI requires Visual Studio Community, Enterprise or Professional Edition installed.
   For all prerequisites, see [here](https://www.intel.com/content/www/us/en/developer/articles/system-requirements/intel-oneapi-base-toolkit-system-requirements.html)
    
2. Download one API Base Toolkit and one API HPC Toolkit

    * Visit one API Base Toolkit Download page: [oneAPI Base Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit-download.html)
    * Visit one API HPC Toolkit Download page: [oneAPI HPC Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/hpc-toolkit-download.html)

3. Install Toolkits

   Minimum required packages are 
   
* In the Base Toolkit: Intel DPC++/C++, Intel Math Kernel Library
* In the HPC Toolkit: Intel Intel® oneAPI DPC++/C++ Compiler, Intel® Fortran Compiler, Intel® MPI Library

Choose the default directory to install Intel oneAPI

4. Install Git 

* Install Git for Windows from : [https://git-scm.com/downloads](https://git-scm.com/downloads)
The Git Bash tool is not need, but can be installed.


5. Install Cygwin

* Download setup-x86-64 setup from : https://www.cygwin.com/install.html
  Direct access is : [setup-x86_64.exe](https://www.cygwin.com/setup-x86_64.exe)
   * execute setup-x86_64.exe
   * Choose in Download Source : 'Install from Internet'  
   * In cygwin Install Directory : Choose Cygwin directory. 
         It is recommended to use the Default directory
   * In Local Download Directory, Choose the download directory
   * In Internet Connexion : Choose System parameters
   * In Download site menu : choose the repository server nearest to your location.
   * In the Package Menu : 
       * Choose make
       * **Do not install git, cmake and ssh from cygwin : 
               cygwin Git does not support LFS, native Git installation will be used.
               cmake is shipped with Visual Studio 
               and ssh is shipped with git**
   * Next will install the packages.

* Post installation task must de done :

   * In cygwin, /bin/link.exe program conflicts with Visual Studio. 
   * Rename it to avoid issues :

         Launch cygwin
         in the shell : move /bin/link.exe in /bin/link_cygwin.exe :
         mv /bin/link.exe in /bin/link_cygwin.exe 


**Notes**
Cygwin is a Unix environment for Windows, all Unix tools are accessible.
* Windows directories are accessible in /cygdrive/[c|d]
* There is a user home directory in cygwin

6. Create a build environment with Intel oneAPI, git and cygwin

Cygwin can be launched with following Batch script : 

         @echo off
         rem c:
         call "C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
         chdir C:\cygwin64\bin
         bash --login -i


7. Setup git in Cygwin

This paragraph permits to to setup Git in Cygwin and use it with GitHub as in a Linux shell.
Launch cygwin build environment and apply the git configuration :


* Add in Git global environment the autocrlf flag

            git config --global core.autocrlf true
	    
* Create the ssh key & set it in GitHub

            ssh-keygen -t rsa
  
  **Note: Accept all defaults, Standard directory, no passphrase**

* Copy the new generated ssh key in cygwin home directory
  As a workaround to used git in cygwin, copy the ssh key in cygwin home directory 
  ssh keys are found in : /cygdrive/c/Users/[Windows User]/.ssh

            cp -r /cygdrive/c/Users/[Windows User]/.ssh /home/[cygwin_user]/

* Set your git parameters as in [CONTRIBUTING.md](./CONTRIBUTING.md)

#### How to build userlib_sdk

Those tasks must be made in the created cygwin environment:

   * clone the source code from the OpenRadioss_userlib_sdk repository or your fork

         git clone git@github.com:OpenRadioss/OpenRadioss_userlib_sdk.git

   * run `./build_script.bash`:
   
         ./build_script.bash -arch=win64 -compiler=oneapi

  * Libraries and modules are copied in : 
  
         userlib_sdk/win64_oneapi

### windows x64 mingw gfortran

#### Compiler Environment

MinGW is a native GNU gcc/gfortran port for Windows. Cygwin will be used to build the SDK

For more information, please visit [https://www.mingw-w64.org](https://www.mingw-w64.org)

1. Installing MinGW compiler

   * Download the Release binaries on GitHub : [https://github.com/niXman/mingw-builds-binaries/releases](https://github.com/niXman/mingw-builds-binaries/releases)
   * Choose the package with x86-64-[GCC Bersion]-win32-seh-rt-[rev].7z
   * Create a MinGW directory in C:\MinGW
   * Unpack the 7Zip file in C:\MinGW

2.  Install Git 

    Install Git for Windows from : [https://git-scm.com/downloads](https://git-scm.com/downloads)
    The Git Bash tool is not need, but can be installed.

3. Install CMake

    cmake is shipped with Visual Studio SDK. This task can be skipped if Visual Studio is already installed : 

    * Download and install cmake from [here](https://cmake.org/download/)
    
4. Install Cygwin
    
    * Download setup-x86-64 setup from [here](https://www.cygwin.com/install.html)
  Direct access is : [setup-x86_64.exe](https://www.cygwin.com/setup-x86_64.exe)
   * execute setup-x86_64.exe
   * Choose in Download Source: 'Install from Internet'  
   * In cygwin Install Directory: Choose Cygwin directory. 
         It is recommended to use the Default directory
   * In Local Download Directory, Choose the download directory
   * In Internet connection: Choose System parameters
   * In Download site menu: choose the repository server nearest to your location.
   * In the Package Menu: 
       * Choose make
       * **Do not install git, cmake and ssh from cygwin : 
               cygwin Git does not support LFS, native Git installation will be used.
               cmake is a native install or shipeed with Visual Studio
               and ssh is shipped with git**
   * Next will install the packages.

* Post installation task must be done :

   * In cygwin, /bin/link.exe program conflicts with Visual Studio. 
   * Rename it to avoid issues :

         Launch cygwin
         in the shell: move /bin/link.exe in /bin/link_cygwin.exe :
         mv /bin/link.exe in /bin/link_cygwin.exe 


**Notes**
Cygwin is a Unix environment for Windows, all Unix tools are accessible.
* Windows directories are accessible in /cygdrive/[c|d]
* There is a user home directory in cygwin
    
5. Create a build environment with Intel oneAPI, git and cygwin

   Cygwin can be launched with following Batch script : 

         @echo off
         
	 rem add Path to MinGw 
	 set PATH=C:\MinGW\mingw64\bin;%PATH%
	 
	 rem add path to cmake
	 set PATH=C:\[Path to Cmake]\bin;%PATH%
	 
         chdir C:\cygwin64\bin
         bash --login -i


6. Setup git in Cygwin

   This paragraph permits to to setup Git in Cygwin and use it with GitHub as in a Linux shell.
   Launch cygwin build environment and apply the git configuration :


   * Add in Git global environment the autocrlf flag

            git config --global core.autocrlf true
	    
   * Create the ssh key & set it in GitHub

            ssh-keygen -t rsa
  
     **Note: Accept all defaults, Standard directory, no passphrase**

   * Copy the new generated ssh key in cygwin home directory
     As a workaround to used git in cygwin, copy the ssh key in cygwin home directory 
     ssh keys are found in : /cygdrive/c/Users/[Windows User]/.ssh

            cp -r /cygdrive/c/Users/[Windows User]/.ssh /home/[cygwin_user]/
 
   * Set your git parameters as in [CONTRIBUTING.md](./CONTRIBUTING.md)

#### How to build userlib_sdk

   * clone the source code from the OpenRadioss_userlib_sdk repository or your fork

         git clone git@github.com:OpenRadioss/OpenRadioss_userlib_sdk.git

   * apply `./build_script.bash`:
   
         ./build_script.bash -arch=win64 -compiler=gfortran

  * Libraries and modules are copied in: 
  
         userlib_sdk/win64-gfortran


## Userlib SDK for Linux ARM 64

### Linux arm64 arm compilers

#### System and compiler installation

Linux system with glibc version 2.17 or higher:

    * CentOS/RHEL 7, CentOS Stream 8, RHEL 8, Rocky Linux 8, Rocky Linux 9
    * Ubuntu 20.0.4 or higher

#### Compiler and development tools

1. Install cmake & make as sudo or root

    * RHEL 7, CentOS Stream 8
    
          yum install make
          yum install cmake
	  
    * Ubuntu

         apt-get update
         apt-get upgrade
         apt-get install build-essential
         apt-get install cmake

2. Install ArmFlang & ArmClang 

   See [ARM Installation Guide](https://developer.arm.com/documentation/102621/0100)
   
#### How to build userlib_sdk

   * clone the source code from the OpenRadioss_userlib_sdk repository or your fork

         git clone git@github.com:OpenRadioss/OpenRadioss_userlib_sdk.git

   * apply `./build_script.bash`:
   
         ./build_script.bash -arch=linuxa64 -compiler=armflang

  * Libraries and modules are copied in : 
  
         userlib_sdk/linuxa64_armflang


### Linux arm64 gfortran

#### System and compiler installation

Linux system with glibc version 2.17 or higher:

    * CentOS/RHEL 7, CentOS Stream 8, RHEL 8, Rocky Linux 8, Rocky Linux 9
    * Ubuntu 20.0.4 or higher

#### Compiler and development tools

You will need GCC/Gfortran version 8 or higher, Cmake version 2.8 or higher, and GNU make.

Install as sudo or root

    * RHEL 7
    
          yum install devtoolset-8
          yum install make
          yum install cmake

    To enable the devtoolset-8, you can run scl enable devtoolset-8 bash

    * RHEL 8, CentOS Stream 8

         dnf install gcc
         dnf install gcc-gfortran
         dnf install gcc-c++
         dnf install make
         dnf install cmake

    * Ubuntu

         apt-get update
         apt-get upgrade
         apt-get install build-essential
         apt-get install gfortran
         apt-get install cmake

#### How to build userlib_sdk

   * clone the source code from the OpenRadioss_userlib_sdk repository or your fork

         git clone git@github.com:OpenRadioss/OpenRadioss_userlib_sdk.git

   * apply `./build_script.bash`:
   
         ./build_script.bash -arch=linuxa64 -compiler=gfortran

  * Libraries and modules are copied in: 
  
         userlib_sdk/linuxa64-gfortran


