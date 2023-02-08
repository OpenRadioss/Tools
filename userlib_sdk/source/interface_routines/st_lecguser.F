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
Chd|  ST_LECM                                                      
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE ST_LECGUSER(IGTYP,ROOTN,ROOTLEN,NUVAR,PARGEO)
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ST_LECGUSER" :: ST_LECGUSER
!DEC$ ATTRIBUTES REFERENCE :: IGTYP,ROOTN,ROOTLEN,NUVAR,PARGEO
#endif
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   I n p u t     A r g u m e n t s 
C-----------------------------------------------
      INTEGER IGTYP,NUVAR,ROOTLEN
      CHARACTER*80 ROOTN
      my_real
     .   PARGEO(*)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER LENROOTN,IIN,IOUT   
      CHARACTER FILNAM*512,CLAW*4
      INTEGER LEN_FILNAM
C-----------------------------------------------
#ifndef ncharline
#define ncharline 500
#endif
      IOUT=31
      IIN=30

C Open the Input File
      WRITE(CLAW,'(I4.4)')IGTYP
      FILNAM  ='SI'//ROOTN(1:ROOTLEN)//'_'//CLAW//'.scr' 
      LEN_FILNAM=LEN_TRIM(FILNAM)     

      OPEN(UNIT=IIN,
     .     FORM='FORMATTED',
     .     FILE=FILNAM(1:LEN_FILNAM),
     .     ACTION='READ'
     .     )      

C Open the Output File
        WRITE(CLAW,'(I4.4)')IGTYP
        FILNAM  ='SO'//ROOTN(1:ROOTLEN)//'_'//CLAW//'.scr'
        LEN_FILNAM=LEN_TRIM(FILNAM)

        OPEN(UNIT=31,FILE=FILNAM(1:LEN_FILNAM),
     .     FORM='FORMATTED')

      IF (IGTYP==29)THEN
        CALL  LECGUSER1(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==30)THEN
        CALL  LECGUSER2(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==31)THEN
        CALL  LECGUSER3(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==37)THEN
        CALL  LECGUSER4(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==38)THEN
        CALL  LECGUSER5(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==39)THEN
        CALL  LECGUSER6(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==40)THEN
        CALL  LECGUSER7(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==41)THEN
        CALL  LECGUSER8(IIN  ,IOUT ,NUVAR,PARGEO)
      ELSEIF(IGTYP==42)THEN
        CALL  LECGUSER9(IIN  ,IOUT ,NUVAR,PARGEO)
      ENDIF

      CLOSE (UNIT=IIN)
      CLOSE (UNIT=IOUT)


      END
