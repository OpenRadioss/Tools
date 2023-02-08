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

echo " "
echo " "
echo "*********************************************"
echo "** Generating Radioss Dynamic user library **"
echo "**            linux64 oneapi               **"
echo "**                                         **"
echo "*********************************************"
echo " "

if [ "$#" == 0 ];then
  echo " "
  echo "Script Usage:"
  echo " "
  echo "build_userlib.bash starter=\"Starter source files\" engine=\"Engine Source files\" [Optional Arguments]"
  echo " "
  echo "[Optional Arguments]"
  echo " "
  echo "library=\"Additional static Library\""
  echo "outfile=\"Optional library name\""
  echo " "
  echo "-free   : Source files are in Fortran 90 Free Format"
  echo "-addflag \"Additional Compiling Arguments\" - Advanced Users Only"
  echo "-link_flags \"Additional Linking Arguments\" - Advanced Users Only"
  echo " "
  echo "----"
  echo " "
  echo " "
  exit 1
fi

libpath=$RAD_USERLIB_SDK_PATH/$RAD_USERLIB_ARCH

got_starter=0
got_engine=0
got_static_lib=0
got_outfile=0
got_free=0
got_addflag=0
got_link_flags=0

for var in "$@"
do
    arg=`echo $var|awk -F '=' '{print $1}'`
    if [ "$arg" == "starter" ]
    then
      starter_files=`echo $var|awk -F '=' '{print $2}'`
      got_starter=1
    fi

    arg=`echo $var|awk -F '=' '{print $1}'`
    if [ "$arg" == "engine" ]
    then
      engine_files=`echo $var|awk -F '=' '{print $2}'`
      got_engine=1
    fi

    arg=`echo $var|awk -F '=' '{print $1}'`
    if [ "$arg" == "library" ]
    then
      static_library=`echo $var|awk -F '=' '{print $2}'`
      got_static_lib=1
    fi

    arg=`echo $var|awk -F '=' '{print $1}'`
    if [ "$arg" == "outfile" ]
    then
      outfile=`echo $var|awk -F '=' '{print $2}'`
      got_outfile=1
    fi

    arg=`echo $var|awk -F '=' '{print $1}'`
    if [ "$arg" == "addflag" ]
    then
      addfl=`echo $var|awk -F '=' '{print $2}'`
      got_addflag=1
    fi

    arg=`echo $var|awk -F '=' '{print $1}'`
    if [ "$arg" == "link_flags" ]
    then
      linkfl=`echo $var|awk -F '=' '{print $2}'`
      got_link_flags=1
    fi

    arg=`echo $var|awk '{print $1}'`
    if [ "$arg" == "-free" ]
    then
      got_free=1
    fi

done

if [ $got_outfile == 1 ]
then
   outlib=../$outfile
   outnam=$outfile
else
   outlib=../libraduser_linux64.so
   outnam=libraduser_linux64.so
fi

if [ $got_free == 1 ]
then
   free_flag=" -free "
else
   free_flag=" "
fi

if [ $got_addflag == 1 ]
then
   addflag=$addfl
else
   addflag=" "
fi

if [ $got_link_flags == 1 ]
then
   link_flags=$linkfl
else
   link_flags=" "
fi

# ----------------------------------------------------------
# Check environment variables 
# if they are wrong, the static interface library could not be found
# ----------------------------------------------------------
if [ ! -f $libpath/libraduser_linux64_oneapi.a ]
then
echo "*** Error : " 
echo " "
echo $libpath/libraduser_linux64_oneapi.a 
echo " "
echo "not found"
echo " "
echo " "
echo "Check environment variables:"
echo " "
echo "RAD_USERLIB_SDK_PATH"
echo "RAD_USERLIB_ARCH"
echo " "
echo " "
exit 0
fi

mkdir _obj_linux64_$$

if [ $got_starter == 1 ]
then
  cp $starter_files _obj_linux64_$$
fi

if [ $got_engine == 1 ]
then
  cp $engine_files _obj_linux64_$$
fi


#Verify if an additional statical library was set

if [ $got_static_lib == 1 ]
then
     cp $static_library _obj_linux64_$$ 
     static_libname=`echo $static_library|awk -F '/' '{print $NF}'`
     echo " " 
     echo "adding $static_libname in library"
     echo "---------------------------------"
     echo " " 
fi

cd  _obj_linux64_$$


ar -x $libpath/libraduser_linux64_oneapi.a

#extract statical library
if [ $got_static_lib == 1 ]
then
  for lib in $static_libname
  do
   if [ -f $lib ]
   then
     echo extracting $lib
     ar -x $lib
   fi
  done
fi


if [ $got_starter == 1 ]
then
echo " " 
echo " " 
echo " Compiling: " $starter_files
echo "-----------"
echo " "
  ifx $free_flag -module $libpath $addflag -fPIC  -axsse3 -O2  -fp-model precise -ftz -extend-source -qopenmp -assume buffered_io -DMYREAL8 -DR8 -c $starter_files
fi

if [ $got_engine == 1 ]
then
  echo " " 
  echo " " 
  echo "Compiling: " $engine_files
  echo "----------"
  echo " "
  ifx $free_flag -module $libpath $addflag -fPIC  -axSSE3,COMMON-AVX512 -no-fma -O3 -fp-model precise -align array64byte -fimf-use-svml=true -qopenmp -ftz  -extend-source -assume buffered_io -DMYREAL8 -DR8 -c $engine_files
fi



echo " "
echo " "
echo "Creating library: " $outnam
echo "-----------------"
echo " "

if [ "$INTEL_LIBRARY_PATH" = "" ]
then

ifx  $addflag -fPIC -shared  -static-intel -qopenmp-link=static -axsse3 -O2  -fp-model precise -ftz -o $outlib *.o $link_flags -lifcoremt_pic

else

ar -x  $INTEL_LIBRARY_PATH/libifcoremt_pic.a
ifx  $addflag -fPIC -shared -static-intel -qopenmp-link=static -axSSE3,COMMON-AVX512 -no-fma -O3 -fp-model precise -align array64byte -fimf-use-svml=true -qopenmp -ftz  -extend-source -assume buffered_io -o $outlib  *.o  $link_flags 

fi 

cd ..
rm -rf  _obj_linux64_$$

echo " "
echo " "
echo "Done"
echo "----"
echo " "
echo " "
