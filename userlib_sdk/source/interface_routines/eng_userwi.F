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
      SUBROUTINE ENG_USERWI(ROOTN ,ROOTLEN ,
     1                           NUVAR  ,NUVARI ,NUMNOD ,
     2           NCYCLE ,LENWA  ,IUVAR  ,ITAB   ,TT     ,
     3           DT1    ,DT2    ,USREINT,EXWORK ,UVAR   ,
     4           D      ,X      ,V      ,VR     ,MASS   ,
     5           INER   ,STIFN  ,STIFR  ,A      ,AR     ,
     6           WA     )
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_USERWI" :: ENG_USERWI
!DEC$ ATTRIBUTES REFERENCE :: ROOTN ,ROOTLEN ,
     1                           NUVAR  ,NUVARI ,NUMNOD ,
     2           NCYCLE ,LENWA  ,IUVAR  ,ITAB   ,TT     ,
     3           DT1    ,DT2    ,USREINT,EXWORK ,UVAR   ,
     4           D      ,X      ,V      ,VR     ,MASS   ,
     5           INER   ,STIFN  ,STIFR  ,A      ,AR     ,
     6           WA    
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

      INTEGER 
     1  NUVAR   ,NUVARI,NUMNOD,NCYCLE  ,LENWA,
     2   IUVAR(NUVARI)  ,ITAB(NUMNOD)  
       DOUBLE PRECISION
     1   TT     ,DT1    ,DT2     ,USREINT,EXWORK  ,
     2   UVAR(NUVAR) ,D(3,NUMNOD) ,X(3,NUMNOD) ,V(3,NUMNOD) ,
     3   VR(3,NUMNOD) ,A(3,NUMNOD) ,AR(3,NUMNOD) ,MASS(NUMNOD) ,
     4   INER(NUMNOD) ,STIFN(NUMNOD) ,STIFR(NUMNOD),WA(LENWA)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
#ifndef ncharline
#define ncharline 500
#endif
      INTEGER LENROOTN,IIN,IOUT   
      CHARACTER FILNAM*512,CLAW*4,LINE*ncharline
      INTEGER LEN_FILNAM,LENLINE   
C-----------------------------------------------
      IOUT=31
      IIN=30


      OPEN(UNIT=IIN,
     .     FORM='FORMATTED',
     .     FILE=ROOTN(1:ROOTLEN),
     .     ACTION='READ'
     .     )      

C Open the Output File

      OPEN(UNIT=IOUT,STATUS='SCRATCH', FORM='FORMATTED')



      CALL USERWI(
     1           IIN    ,IOUT   ,NUVAR  ,NUVARI ,NUMNOD ,
     2           NCYCLE ,LENWA  ,IUVAR  ,ITAB   ,TT     ,
     3           DT1    ,DT2    ,USREINT,EXWORK ,UVAR   ,
     4           D      ,X      ,V      ,VR     ,MASS   ,
     5           INER   ,STIFN  ,STIFR  ,A      ,AR     ,
     6           WA     )

      REWIND(IOUT)
      DO WHILE(.TRUE.)
          READ(UNIT=IOUT,END=999,FMT='(A)')LINE    
          LENLINE=LEN_TRIM(LINE)
          CALL WRITE_IOUT(LINE,LENLINE)
      ENDDO
 999  CONTINUE 

      CLOSE (UNIT=IIN)
      CLOSE (UNIT=IOUT)

      END
