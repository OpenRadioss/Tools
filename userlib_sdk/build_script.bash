#!/bin/bash

# Copyright>  Copyright 1986-2023 Altair Engineering Inc.  
# Copyright> 
# Copyright>  Permission is hereby granted, free of charge, to any person obtaining 
# Copyright>  a copy of this software and associated documentation files (the "Software"), 
# Copyright>  to deal in the Software without restriction, including without limitation 
# Copyright>  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# Copyright>  sell copies of the Software, and to permit persons to whom the Software is 
# Copyright>  furnished to do so, subject to the following conditions:
# Copyright> 
# Copyright>  The above copyright notice and this permission notice shall be included in all 
# Copyright>  copies or substantial portions of the Software.
# Copyright> 
# Copyright>  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# Copyright>  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# Copyright>  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# Copyright>  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIAsBILITY, 
# Copyright>  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
# Copyright>  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

function my_help()
{
  echo " " 
  echo " userlib_sdk build script "
  echo " -------------------------"
  echo " " 
  echo " Use with arguments : "
  echo " -arch=[linux64|linuxa64|win64]"
  echo " -compiler=[armflang|gfortran|intel]"
  echo "            Defaults :"
  echo "              linux64  : gfortran"
  echo "              win64    : oneapi"
  echo "              linuxa64 : gfortran"
  echo " -prec=[dp|sp] "
  echo "              set precision - dp (default) |sp "
  echo " " 
  echo " -verbose : Build verbose mode."
  echo " -clean : delete build"
  echo " " 
  echo " " 
}

# -----------------------------
# Parse command line arguments
# -----------------------------
arch='none'
prec=dp
suffix=''
got_compiler=0
got_arch=0
clean=0
verbose=''

number_of_arguments=$#

if [ $number_of_arguments = 0 ]
then

  my_help
  exit 1

else

   for var in "$@"
   do
       arg=`echo $var|awk -F '=' '{print $1}'`
       if [ "$arg" == "-arch" ]
       then
         arch=`echo $var|awk -F '=' '{print $2}'`
         got_arch=1
       fi

       if [ "$arg" == "-compiler" ]
       then
         compiler=`echo $var|awk -F '=' '{print $2}'`
         got_compiler=1
       fi
       
       if [ "$arg" == "-prec" ]
       then
         prec=`echo $var|awk -F '=' '{print $2}'`
         if [ ${prec} = 'sp' ]
         then
           suffix=_sp
         fi
       fi

       if [ "$arg" == "-clean" ]
       then
         clean=1
       fi
       
       if [ "$arg" == "-verbose" ]
       then
         verbose='VERBOSE=1'
       fi

   done

  if [ $got_arch = '0' ]
  then
     echo " Error : "
     echo " ------  "
     echo " Specify -arch option"
     echo " " 
     echo " " 
     my_help
     exit 1
  fi


  if [ $got_compiler = 0 ]
  then
     if [ $arch == "win64" ]
     then
       compiler=oneapi
     fi
     
     if [ $arch == "linux64" ]
     then
       compiler=gfortran
     fi
     
     if [ $arch = 'linuxa64' ]
     then
       compiler=gfortran
     fi
  fi

   echo " " 
   echo " Build Radioss(TM) Userlib SDK"
   echo " ------------------------------"
   echo " Build Arguments :"
   echo " arch=            " $arch
   echo " compiler=        " $compiler
   echo " " 
fi

# Library extention 

if [ "$arch" == "win64" ] && [ "$compiler" != "gfortran" ]
then
  lib=.lib
else
  lib=.a
fi
echo $LIB_EXT

# build & object directory
build_directory=cbuild_${arch}_${compiler}${suffix}
sdk_directory=${arch}${suffix}_${compiler}

# clean option
if [ $clean = 1 ]
then
   if [ -d ${build_directory} ]
   then
     echo "Clean ${build_directory} directory"
     rm -rf ./${build_directory}
   else
     echo "Clean ${build_directory} directory requested but not found"
   fi
   echo " " 
   exit 0
fi

# create build directory
if [ ! -d ${build_directory} ] 
then
   mkdir ${build_directory}
fi

cd $build_directory

if [ $arch = "win64" ]
then
  cmake -G "Unix Makefiles" -Darch=${arch} -Dcompiler=${compiler} -Dprecision=${prec} ../source
else
  cmake -Darch=${arch} -Dcompiler=${compiler} -Dprecision=${prec} ../source
fi

make ${verbose}

cp libraduser_${arch}${suffix}_${compiler}${lib} *.mod ../userlib_sdk/${sdk_directory}

cd ..



echo " " 
echo " Done"
echo " ----" 
echo " " 

