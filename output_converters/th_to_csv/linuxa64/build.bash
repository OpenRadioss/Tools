#!/bin/bash

#
# check if exec directory exists, create if not
#
if [ ! -d ../../../exec ]
then
   mkdir ../../../exec
fi


 gcc -DLINUX -o ../../../exec/th_to_csv_linuxa64 ../src/th_to_csv.c

