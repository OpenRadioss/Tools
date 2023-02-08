# Copyright 1986-2022 Altair Engineering Inc.  
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#
# CMake project file for Radioss uselib sdk
# ------------------------------------------

cmake_minimum_required (VERSION 2.8)

project (userlib_sdk)

# Language settings & Compiler Settings
# -------------------------------------
enable_language (Fortran)
enable_language (C)

set(CMAKE_C_OUTPUT_EXTENSION_REPLACE 1)
set(CMAKE_Fortran_OUTPUT_EXTENSION_REPLACE 1)

# source files & include directories
# ----------------------------------

set (source_directory ${CMAKE_CURRENT_SOURCE_DIR})
set (include_directory "${CMAKE_CURRENT_SOURCE_DIR}/source/includes" )

#  Load compiler settings
# ------------------------

include (${source_directory}/Cmake_Compilers${cdir}/cmake_${arch}_${compiler}.txt)



# Includes directory list
# -----------------------
file(GLOB_RECURSE include_files ${source_directory}/*.h  ${source_directory}/*.inc)

set (include_dir_list "")
foreach (incfile ${include_files})
    get_filename_component(dir ${incfile} PATH)
    list (APPEND include_dir_list ${dir})
endforeach()
list(REMOVE_DUPLICATES include_dir_list)



#C source files
file(GLOB_RECURSE c_source_files ${source_directory}/*.c  ${source_directory}/../userlib_routines/*.c)
file(GLOB_RECURSE c_source_files_remove ${source_directory}/../userlib_routines/engine/initialization/*.c)
list(REMOVE_ITEM c_source_files ${c_source_files_remove})

#Fortran source files
file(GLOB_RECURSE fortran_source_files ${source_directory}/*.F  ${source_directory}/../userlib_routines/*.F)
file(GLOB_RECURSE f_source_files_remove ${source_directory}/../userlib_routines/engine/initialization/*.F)
list(REMOVE_ITEM fortran_source_files ${f_source_files_remove})



message (STATUS " " )
message (STATUS "arch: ${arch} ")
message (STATUS "Compiler: ${compiler} ")
message (STATUS "Precision: ${precision} ")
message (STATUS " " )
message (STATUS "Fortran Compiler: ${CMAKE_Fortran_COMPILER}" )
message (STATUS "C Compiler      : ${CMAKE_C_COMPILER}" )
message (STATUS " " )

#
# Clean up compiler Flags
# ------------------------

set (CMAKE_Fortran_FLAGS " " )
set (CMAKE_C_FLAGS " " )
set (CMAKE_CPP_FLAGS " " )
set (CMAKE_CXX_FLAGS " " )

set (CMAKE_Fortran_FLAGS_DEBUG " " )
set (CMAKE_Fortran_FLAGS_RELEASE " " )

set (CMAKE_C_FLAGS_DEBUG " " )
set (CMAKE_C_FLAGS_RELEASE " " )

set (CMAKE_CPP_FLAGS_DEBUG " " )
set (CMAKE_CPP_FLAGS_RELEASE " " )

set (CMAKE_CXX_FLAGS_DEBUG " " )
set (CMAKE_CXX_FLAGS_RELEASE " " )

#
# Set up compiler Flags
# ------------------------
set_source_files_properties( ${fortran_source_files}  PROPERTIES COMPILE_FLAGS "${Fortran_Compiler_flags}")
set_source_files_properties( ${c_source_files}  PROPERTIES COMPILE_FLAGS "${C_Compiler_flags}")


#add_library(hm_reader/libs_${arch}/libhm_reader_rd_${arch} STATIC ${cpp_source_files} )
add_library(${lib_suffix}raduser_${arch}${lib_prec}_${compiler} STATIC ${c_source_files} ${fortran_source_files} )
target_include_directories(${lib_suffix}raduser_${arch}${lib_prec}_${compiler} PRIVATE ${include_dir_list}  )



