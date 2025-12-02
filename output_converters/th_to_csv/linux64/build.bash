#!/bin/bash

#
# check if exec directory exists, create if not
#
if [ ! -d ../../../exec ]
then
   mkdir ../../../exec
fi


 gcc -DLINUX -o ../../../exec/th_to_csv_linux64_gf ../src/th_to_csv.c
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
