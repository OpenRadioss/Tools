#!/bin/bash

#
# check if exec directory exists, create if not
#
if [ ! -d ../../../exec ]
then
   mkdir ../../../exec
fi


 g++ -DLINUX -o ../../../exec/anim_to_vtk_linux64_gf ../src/anim_to_vtk.cpp
 export BUILD_RETURN_CODE=$?
 if [ $BUILD_RETURN_CODE -ne 0 ]
 then
    echo " " 
    echo "Build failed"
    echo " " 
    rm -f *.o
    exit $BUILD_RETURN_CODE
 fi

 echo " " 
 echo "Build succeeded"
 echo " "
 rm -f *.o
 exit 0
