#!/bin/bash

#
# check if exec directory exists, create if not
#
if [ ! -d ../../../exec ]
then
   mkdir ../../../exec
fi

 EXEC_DIR=$(cd ../../../exec && pwd)
 cd ..
 cargo build --release
 export BUILD_RETURN_CODE=$?
 if [ $BUILD_RETURN_CODE -ne 0 ]
 then
    echo " " 
    echo "Build failed"
    echo " " 
    exit $BUILD_RETURN_CODE
 fi

 cp target/release/anim_to_vtk "$EXEC_DIR/anim_to_vtk_linux64_gf"

 echo " " 
 echo "Build succeeded"
 echo " "
 exit 0
