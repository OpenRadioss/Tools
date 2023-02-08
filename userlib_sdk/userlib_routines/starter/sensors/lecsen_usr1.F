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
Chd|  LECSEN_USR1                                                 
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|        SET_U_SENS_IPAR                                             
Chd|====================================================================
      SUBROUTINE LECSEN_USR1(IIN,IOUT)
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C IIN      |  1      | I | R | INPUT FILE UNIT  (D00 file) 
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
C----------+---------+---+---+--------------------------------------------
C    MAXIMUM INTEGER PARAMETER NUMBER = 12 
C    MAXIMUM FLOAT   PARAMETER NUMBER = 20 
C-----------------------------------------------
C     This subroutine read the user sensor parameters.
C     The data has to be stored in sensor parameter buffers using functions:
C 
C     SET_U_SENS_FPAR(fpar_index,value) - for float  parameter values, and
C     SET_U_SENS_IPAR(ipar_index,value) - for integer  parameter values
C       where fpar_index and ipar_index are varable indexes 
C	in respective buffers
C     These functions return an integer flag ierr=-1 if the sensor number 
C     is not valid, ierr=MAXPAR if the maximum parameter number is exceeded,
C     and ierr=0 if no errror.
C---  Radioss functions access (*** VERSION 44 AND HIGHER ONLY)
C	FLOAT Y = GET_U_FUNC(IFUNC, X, DERI)
C              Y    = float ordinate
C              X    = float abscissa
C              DERI  = float Y/X
C              IFUNC = integer function number 
C              IDFUN = integer function ID, where
C 	INTEGER IFUNC = GET_U_NUMFUN(IDFUN)
C-----------------------------------------------
C   D u m m y   A r g u m e n t s
C-----------------------------------------------
      INTEGER IIN, IOUT
      INTEGER SET_U_SENS_IPAR
      my_real SET_U_SENS_FPAR
      EXTERNAL SET_U_SENS_IPAR,SET_U_SENS_FPAR
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER IERROR, IDFUN
C=================================================================
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='USER SENSOR'
        SIZE=LEN_TRIM(OPTION)
        WRITE(6,'(A)')
     .     '** ERROR IN USER LIBRARY SDK'
         WRITE(6,'(A,A)')
     .     ' OPTION : ',OPTION(1:SIZE)
        WRITE(6,'(A)')
     .     'USER INTERFACE OPTION USED, BUT NO USER INTERFACE ROUTINE IS FOUND IN SDK'

        CALL ARRET(2)
      END 

