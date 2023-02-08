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
      SUBROUTINE ST_USERWIS(ROOTN ,ROOTLEN ,NUMNOD  ,ITAB    ,
     .                      X     ,V       ,VR      ,MASS    ,INER    ,
     .                      NUVAR ,NUVARI  ,UVAR    ,IUVAR )
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ST_USERWIS" :: ST_USERWIS
!DEC$ ATTRIBUTES REFERENCE :: ILAW,ROOTN,ROOTLEN,NUMNOD ,ITAB,X,V,VR,MASS,INER,NUVAR,NUVARI,UVAR,IUVAR 
#endif
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   I n p u t     A r g u m e n t s 
C-----------------------------------------------
      INTEGER ROOTLEN
      CHARACTER*80 ROOTN
C-----------------------------------------------
C   O u t P u t   A r g u m e n t s 
C-----------------------------------------------
      INTEGER NUMNOD, NUVAR ,NUVARI,ITAB(NUMNOD),IUVAR(*)
      my_real
     .   X(3,NUMNOD) ,V(3,NUMNOD),VR(3,NUMNOD),
     .   MASS(NUMNOD),INER(NUMNOD),UVAR(*)
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
        WRITE(CLAW,'(I4.4)') 1
        FILNAM  ='SI'//ROOTN(1:ROOTLEN)//'_'//CLAW//'.scr'
        LEN_FILNAM=LEN_TRIM(FILNAM)

      OPEN(UNIT=IIN,
     .     FORM='FORMATTED',
     .     FILE=FILNAM(1:LEN_FILNAM),
     .     ACTION='READ'
     .     )      

C Open the Output File
        WRITE(CLAW,'(I4.4)') 1
        FILNAM  ='SO'//ROOTN(1:ROOTLEN)//'_'//CLAW//'.scr'
        LEN_FILNAM=LEN_TRIM(FILNAM)

        OPEN(UNIT=31,FILE=FILNAM(1:LEN_FILNAM),
     .     FORM='FORMATTED')


        CALL USERWIS(IIN     ,IOUT    ,NUMNOD   ,ITAB    ,
     .               X       ,V       ,VR       ,MASS    ,INER    ,
     .               NUVAR   ,NUVARI  ,UVAR     ,IUVAR   )


      CLOSE (UNIT=IIN)
      CLOSE (UNIT=IOUT)


      END
