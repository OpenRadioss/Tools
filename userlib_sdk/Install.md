# How to use the userlib_sdk

The Userlib SDK permits to create a Radioss user library using user code

## Develop the User code.

  * Visit the Altair Radioss Help for the interface explanation : [Radioss User Subroutine help](https://2022.help.altair.com/2022.1/hwsolvers/rad/topics/solvers/rad/introduction_user_code_r.htm)
  * Have a look at the examples provides in this repository : [Examples](https://github.com/OpenRadioss/userlib_sdk/tree/main/examples)

## Choose your platform and Compiler. 

  * The SDK must be compiled for this platform. See [How to Build the userlib_sdk](HOWTO.md) section.
  * The compiler must be installed and functional. The compiler used to build the SDK should be used to generate the user library. 

**Note:** the build scripts for Windows are made in Batch format. A cmd Shell is sufficient. Cygwin, cmake and make are not needed for this task. 

## Environment variables setting

Two Variables must be set: `RAD_USERLIB_SDK_PATH` and `RAD_USERLIB_ARCH`
* `RAD_USERLIB_SDK_PATH` to userlib_sdk root
* `RAD_USERLIB_ARCH` to Arch and compiler.

Under Linux / bash shell

      export RAD_USERLIB_SDK_PATH=[Root to dsk]/userlib_sdk
      export RAD_USERLIB_ARCH=[platform]_[compiler]
      
Under Windows / CMD.exe shell

      set RAD_USERLIB_SDK_PATH=[Root to dsk]\userlib_sdk
      set RAD_USERLIB_ARCH=[platform]_[compiler]
      
## Apply the build_script with user Routines

Help is displayed when script is executed without arguments 

Under Linux 

      $RAD_USERLIB_SDK_PATH/$RAD_USERLIB_ARCH/build_userlib.bash
      
      *********************************************
      ** Generating Radioss Dynamic user library **
      **            linux64 gfortran             **
      **                                         **
      *********************************************
      
      
      Script Usage:

      build_userlib.bash starter="Starter source files" engine="Engine Source files" [Optional Arguments]

      [Optional Arguments]

      library="Additional static Library"
      outfile="Optional library name"

      -free   : Source files are in Fortran 90 Free Format
      -addflag "Additional Compiling Arguments" - Advanced Users Only
      -link_flags "Additional Linking Arguments" - Advanced Users Only

      ----


Under Windows

      %RAD_USERLIB_SDK_PATH%\%RAD_USERLIB_ARCH%\build_userlib.bat

      *********************************************
      ** Generating Radioss Dynamic User Library **
      **            Win64 oneapi                 **
      **                                         **
      *********************************************
      
      
      Script Usage:
      
      build_userlib_win64.bat /STARTER "Starter source files" /ENGINE "Engine Source files " [Optional Argument]
      
      [Optional Argument]
      
      /LIBRARY "additional static Library"
      /OUTFILE "Library_name"
      
      /FREE  : Source code is in Fortran 90 Free Format
      /ADDFLAG "Additional compiler Flags" : Additional compiler flags to set
      /LINK_FLAGS "Additional link flags"  : add link Flags like library files to link with.
      
      
      Done
      ----


The Default name of the library is libraduser_linux64.so for Linux X64, libraduser_linuxa64.so for Linux Arm64 and libraduser_win64.dll for Windows.


## Executing with OpenRadioss
    
### Using environment variable : RAD_USERLIB_LIBPATH and default library name
    
   * Under Linux : 
     
      export RAD_USERLIB_LIBPATH=[Path to library]
      
   OpenRadioss will find  libraduser_linux64.so library in the folder.
    
   * under Windows / cmd.exe

     set RAD_USERLIB_LIBPATH=[Path to library]
     
### Using -dylib OpenRadioss command line argument
  
   Command line argument permits to git an other name to the library:
   
     [Path to starter]/starter_linux64 -dylib [path to mylib]/mylib.so -i [Starter input] -np [#MPI domains]

## Usage example

   Generate user library with material law routine lecmuser01.f and luser01c.f :
   
   * Linux example


         $RAD_USERLIB_SDK_PATH/$RAD_USERLIB_ARCH/build_userlib.bash starter="lecmuser01.f engine="luser01c.f"
         
         *********************************************
         ** Generating Radioss Dynamic user library **
         **            linux64 gfortran             **
         **                                         **
         *********************************************
         
         
         
         Compiling:  lecmuser01.f
         -----------
         
         
         
         Compiling:  luser01c.f
         ----------



         Creating library:  libraduser_linux64.so
         -----------------
         

         
         Done
         ----


   * Windows example

         %RAD_USERLIB_SDK_PATH%\%RAD_USERLIB_ARCH%\build_userlib.bat /STARTER "lecmuser01.f" /ENGINE "luser01c.f"
         
         D:\Work\Userlib_sdk\Law99_shell>echo off
         
         
         *********************************************
         ** Generating Radioss Dynamic User Library **
         **            Win64 oneapi                 **
         **                                         **
         *********************************************
         
         
         
         Preparing Library
         -----------------
         
         
         
         
         Compiling: lecmuser01.f
         ----------

         lecmuser01.f
         
         
         
         Compiling: luser01c.f
         ----------
         
         luser01c.f
         
         
         
         Creating library: libraduser_win64.dll
         ----------------
         
            Création de la bibliothèque libraduser_win64.lib et de l'objet libraduser_win64.exp

         Done
         ----





      
