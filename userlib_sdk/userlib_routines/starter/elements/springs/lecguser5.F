Copyright>
Copyright> Copyright (C) 1986-2023 Altair Engineering Inc.
Copyright>    
Copyright> Permission is hereby granted, free of charge, to any person obtaining 
Copyright> a copy of this software and associated documentation files (the "Software"), 
Copyright> to deal in the Software without restriction, including without limitation 
Copyright> the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
Copyright> sell copies of the Software, and to permit persons to whom the Software is 
Copyright> furnished to do so, subject to the following conditions:
Copyright> 
Copyright> The above copyright notice and this permission notice shall be included in all 
Copyright> copies or substantial portions of the Software.
Copyright> 
Copyright> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
Copyright> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
Copyright> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
Copyright> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
Copyright> WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
Copyright> IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Copyright>


Chd|====================================================================
Chd|  LECGUSER5                     src/user1/lecguser5.F         
Chd|-- called by -----------
Chd|        LECGUSER                      src/lectur1/lecguser.F        
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE LECGUSER5(IIN   ,IOUT  ,NUVAR ,PARGEO)
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C IIN      |  1      | I | R | INPUT FILE UNIT (D00 file) 
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
C NUVAR    |  1      | I | W | NUMBER OF USER ELEMENT VARIABLES
C----------+---------+---+---+--------------------------------------------
C PARGEO   |  *      | F | W | 1)SKEW NUMBER
C          |         |   |   | 2)STIFNESS FOR INTERFACE
C          |         |   |   | 3)FRONT WAVE OPTION
C          |         |   |   | 4)... not yet used
C----------+---------+---+---+--------------------------------------------
C
C     This subroutine read the user geometry parameters.
C
C     The geometry datas has to bee stored in radioss storage 
C     with the function SET_U_GEO(value_index,value). 
C
C     If some standard radioss functions (time function or 
C     x,y function) are used, this function IDs has to 
C     bee stored with the function SET_U_PNU(func_index,func_id,KFUNC).
C
C     If this property refers to a user material, this 
C     material IDs has to bee stored with the function 
C     SET_U_PNU(mat_index,mat_id,KMAT).
C
C     If this property refers to a user property, this 
C     sub-property IDs has to bee stored with the function 
C     SET_U_PNU(sub_prop_index,sub_prop_id,KMAT).
C
C     SET_U_GEO and SET_U_PNU return 0 if no error 
C     SET_U_GEO and SET_U_PNU return the maximum allowed index 
C     if index is larger than this maximum
C-----------------------------------------------
C   D u m m y   A r g u m e n t s
C-----------------------------------------------
      INTEGER IIN,IOUT,NUVAR
      my_real   
     .        PARGEO(*)
C-----------------------------------------------
C   E x t e r n a l   F u n c t i o n s
C-----------------------------------------------
      INTEGER SET_U_PNU,SET_U_GEO
C-----------------------------------------------
C   P a r a m e t e r s
C-----------------------------------------------
      INTEGER KFUNC,KMAT,KPROP
      PARAMETER (KFUNC=29)
      PARAMETER (KMAT=31)
      PARAMETER (KPROP=33)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
C=================================================================
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='USER PROPERTY'
        SIZE=LEN_TRIM(OPTION)
        WRITE(6,'(A)')
     .     '** ERROR IN USER LIBRARY SDK'
         WRITE(6,'(A,A)')
     .     ' OPTION : ',OPTION(1:SIZE)
        WRITE(6,'(A)')
     .     'USER INTERFACE OPTION USED, BUT NO USER INTERFACE ROUTINE IS FOUND IN SDK'

        CALL ARRET(2)
      END 

