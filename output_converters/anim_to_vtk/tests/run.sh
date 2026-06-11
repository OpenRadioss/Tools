#!/bin/bash
#legacy conversion using 
#find all *A0* files and convert them to vtk format using the anim_to_vtk_linux64_gf executable
#list_of_files=$(find . -name "*A0*") #wrong because of ./ in the name
rm *.vtk
list_of_files=$(ls *A0*) #correct because it only lists the file name without the path
for i in $list_of_files
do
~/OpenRadioss/exec/anim_to_vtk_linux64_gf $i > ref_${i}.vtk 
done
time /home/laurent/Tools/output_converters/anim_to_vtk/target/release/anim_to_vtk *A0* --legacy

#compare the two sets of vtk files using the diff command
echo "Comparing the two sets of vtk files, diffs:"
for i in $list_of_files
do
	echo "Comparing ref_${i}.vtk and ${i%.A0*}.vtk"
	diff -w ref_${i}.vtk ${i}.vtk
done
