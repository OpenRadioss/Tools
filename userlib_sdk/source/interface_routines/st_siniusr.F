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
      SUBROUTINE ST_SINIUSR(IGTYP,ROOTN  ,ROOTLEN ,
     1 NEL  ,NUVAR,IPROP ,IMAT,SOLID_ID,
     2 EINT ,VOL  ,UVAR ,OFF,RHO  ,SIG  ,
     3 XX1  ,XX2  ,XX3  ,XX4  ,XX5  ,XX6  ,XX7  ,XX8 ,
     4 YY1  ,YY2  ,YY3  ,YY4  ,YY5  ,YY6  ,YY7  ,YY8 ,
     5 ZZ1  ,ZZ2  ,ZZ3  ,ZZ4  ,ZZ5  ,ZZ6  ,ZZ7  ,ZZ8 ,
     6 VX1  ,VX2  ,VX3  ,VX4  ,VX5  ,VX6  ,VX7  ,VX8 ,
     7 VY1  ,VY2  ,VY3  ,VY4  ,VY5  ,VY6  ,VY7  ,VY8 ,
     8 VZ1  ,VZ2  ,VZ3  ,VZ4  ,VZ5  ,VZ6  ,VZ7  ,VZ8 ,
     9 VRX1 ,VRX2 ,VRX3 ,VRX4 ,VRX5 ,VRX6 ,VRX7 ,VRX8 ,
     A VRY1 ,VRY2 ,VRY3 ,VRY4 ,VRY5 ,VRY6 ,VRY7 ,VRY8 ,
     B VRZ1 ,VRZ2 ,VRZ3 ,VRZ4 ,VRZ5 ,VRZ6 ,VRZ7 ,VRZ8 ,
     C MAS1 ,MAS2 ,MAS3 ,MAS4 ,MAS5 ,MAS6 ,MAS7 ,MAS8 ,
     D INN1 ,INN2 ,INN3 ,INN4 ,INN5 ,INN6 ,INN7 ,INN8 ,
     C STIFM,STIFR,VISCM,VISCR)
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ST_SINIUSR" :: ST_SINIUSR
!DEC$ ATTRIBUTES REFERENCE :: IGTYP,ROOTN  ,ROOTLEN ,
     1 NEL  ,NUVAR,IPROP ,IMAT,SOLID_ID,
     2 EINT ,VOL  ,UVAR ,OFF,RHO  ,SIG  ,
     3 XX1  ,XX2  ,XX3  ,XX4  ,XX5  ,XX6  ,XX7  ,XX8 ,
     4 YY1  ,YY2  ,YY3  ,YY4  ,YY5  ,YY6  ,YY7  ,YY8 ,
     5 ZZ1  ,ZZ2  ,ZZ3  ,ZZ4  ,ZZ5  ,ZZ6  ,ZZ7  ,ZZ8 ,
     6 VX1  ,VX2  ,VX3  ,VX4  ,VX5  ,VX6  ,VX7  ,VX8 ,
     7 VY1  ,VY2  ,VY3  ,VY4  ,VY5  ,VY6  ,VY7  ,VY8 ,
     8 VZ1  ,VZ2  ,VZ3  ,VZ4  ,VZ5  ,VZ6  ,VZ7  ,VZ8 ,
     9 VRX1 ,VRX2 ,VRX3 ,VRX4 ,VRX5 ,VRX6 ,VRX7 ,VRX8 ,
     A VRY1 ,VRY2 ,VRY3 ,VRY4 ,VRY5 ,VRY6 ,VRY7 ,VRY8 ,
     B VRZ1 ,VRZ2 ,VRZ3 ,VRZ4 ,VRZ5 ,VRZ6 ,VRZ7 ,VRZ8 ,
     C MAS1 ,MAS2 ,MAS3 ,MAS4 ,MAS5 ,MAS6 ,MAS7 ,MAS8 ,
     D INN1 ,INN2 ,INN3 ,INN4 ,INN5 ,INN6 ,INN7 ,INN8 ,
     C STIFM,STIFR,VISCM,VISCR
#endif
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"

C-----------------------------------------------
C   I n p u t     A r g u m e n t s 
C-----------------------------------------------
      INTEGER NEL,NUVAR,IPROP,IMAT,SOLID_ID(*)
      my_real
     .   UVAR(NEL,NUVAR),
     .   STIFM(*) ,STIFR(*) , VISCM(*) ,VISCR(*) ,
     .   OFF(*) ,EINT(*) , RHO(*) ,VOL(*) ,SIG(6,*),
     2 XX1(*),XX2(*),XX3(*),XX4(*),XX5(*),XX6(*),XX7(*),XX8(*),
     3 YY1(*),YY2(*),YY3(*),YY4(*),YY5(*),YY6(*),YY7(*),YY8(*),
     4 ZZ1(*),ZZ2(*),ZZ3(*),ZZ4(*),ZZ5(*),ZZ6(*),ZZ7(*),ZZ8(*),
     5 VX1(*),VX2(*),VX3(*),VX4(*),VX5(*),VX6(*),VX7(*),VX8(*),
     6 VY1(*),VY2(*),VY3(*),VY4(*),VY5(*),VY6(*),VY7(*),VY8(*),
     7 VZ1(*),VZ2(*),VZ3(*),VZ4(*),VZ5(*),VZ6(*),VZ7(*),VZ8(*),
     8 VRX1(*),VRX2(*),VRX3(*),VRX4(*),VRX5(*),VRX6(*),VRX7(*),VRX8(*),
     9 VRY1(*),VRY2(*),VRY3(*),VRY4(*),VRY5(*),VRY6(*),VRY7(*),VRY8(*),
     A VRZ1(*),VRZ2(*),VRZ3(*),VRZ4(*),VRZ5(*),VRZ6(*),VRZ7(*),VRZ8(*),
     C MAS1(*),MAS2(*),MAS3(*),MAS4(*),MAS5(*),MAS6(*),MAS7(*),MAS8(*),
     D INN1(*),INN2(*),INN3(*),INN4(*),INN5(*),INN6(*),INN7(*),INN8(*)
C-----------------------------------------------
      INTEGER IGTYP,ROOTLEN
      CHARACTER*80 ROOTN
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER LENROOTN,IOUT   
      CHARACTER FILNAM*512,CLAW*4
      INTEGER LEN_FILNAM
C-----------------------------------------------
#ifndef ncharline
#define ncharline 500
#endif
      IOUT=31


C Open the Output File
        WRITE(CLAW,'(I4.4)')IGTYP
        FILNAM  ='SO'//ROOTN(1:ROOTLEN)//'_'//CLAW//'.scr'
        LEN_FILNAM=LEN_TRIM(FILNAM)

        OPEN(UNIT=31,FILE=FILNAM(1:LEN_FILNAM),
     .     FORM='FORMATTED')

      IF (IGTYP==29)THEN
        CALL SINI29(
     1     NEL  ,NUVAR,IOUT ,IPROP ,IMAT,SOLID_ID,
     2     EINT ,VOL  ,UVAR ,OFF,RHO  ,SIG  ,
     3     XX1  ,XX2  ,XX3  ,XX4  ,XX5  ,XX6  ,XX7  ,XX8 ,
     4     YY1  ,YY2  ,YY3  ,YY4  ,YY5  ,YY6  ,YY7  ,YY8 ,
     5     ZZ1  ,ZZ2  ,ZZ3  ,ZZ4  ,ZZ5  ,ZZ6  ,ZZ7  ,ZZ8 ,
     6     VX1  ,VX2  ,VX3  ,VX4  ,VX5  ,VX6  ,VX7  ,VX8 ,
     7     VY1  ,VY2  ,VY3  ,VY4  ,VY5  ,VY6  ,VY7  ,VY8 ,
     8     VZ1  ,VZ2  ,VZ3  ,VZ4  ,VZ5  ,VZ6  ,VZ7  ,VZ8 ,
     9     VRX1 ,VRX2 ,VRX3 ,VRX4 ,VRX5 ,VRX6 ,VRX7 ,VRX8 ,
     A     VRY1 ,VRY2 ,VRY3 ,VRY4 ,VRY5 ,VRY6 ,VRY7 ,VRY8 ,
     B     VRZ1 ,VRZ2 ,VRZ3 ,VRZ4 ,VRZ5 ,VRZ6 ,VRZ7 ,VRZ8 ,
     C     MAS1 ,MAS2 ,MAS3 ,MAS4 ,MAS5 ,MAS6 ,MAS7 ,MAS8 ,
     D     INN1 ,INN2 ,INN3 ,INN4 ,INN5 ,INN6 ,INN7 ,INN8 ,
     C     STIFM,STIFR,VISCM,VISCR)

      ELSEIF(IGTYP==30)THEN
        CALL SINI30(
     1     NEL  ,NUVAR,IOUT ,IPROP ,IMAT,SOLID_ID,
     2     EINT ,VOL  ,UVAR ,OFF,RHO  ,SIG  ,
     3     XX1  ,XX2  ,XX3  ,XX4  ,XX5  ,XX6  ,XX7  ,XX8 ,
     4     YY1  ,YY2  ,YY3  ,YY4  ,YY5  ,YY6  ,YY7  ,YY8 ,
     5     ZZ1  ,ZZ2  ,ZZ3  ,ZZ4  ,ZZ5  ,ZZ6  ,ZZ7  ,ZZ8 ,
     6     VX1  ,VX2  ,VX3  ,VX4  ,VX5  ,VX6  ,VX7  ,VX8 ,
     7     VY1  ,VY2  ,VY3  ,VY4  ,VY5  ,VY6  ,VY7  ,VY8 ,
     8     VZ1  ,VZ2  ,VZ3  ,VZ4  ,VZ5  ,VZ6  ,VZ7  ,VZ8 ,
     9     VRX1 ,VRX2 ,VRX3 ,VRX4 ,VRX5 ,VRX6 ,VRX7 ,VRX8 ,
     A     VRY1 ,VRY2 ,VRY3 ,VRY4 ,VRY5 ,VRY6 ,VRY7 ,VRY8 ,
     B     VRZ1 ,VRZ2 ,VRZ3 ,VRZ4 ,VRZ5 ,VRZ6 ,VRZ7 ,VRZ8 ,
     C     MAS1 ,MAS2 ,MAS3 ,MAS4 ,MAS5 ,MAS6 ,MAS7 ,MAS8 ,
     D     INN1 ,INN2 ,INN3 ,INN4 ,INN5 ,INN6 ,INN7 ,INN8 ,
     C     STIFM,STIFR,VISCM,VISCR)

      ELSEIF(IGTYP==31)THEN
        CALL SINI31(
     1     NEL  ,NUVAR,IOUT ,IPROP ,IMAT,SOLID_ID,
     2     EINT ,VOL  ,UVAR ,OFF,RHO  ,SIG  ,
     3     XX1  ,XX2  ,XX3  ,XX4  ,XX5  ,XX6  ,XX7  ,XX8 ,
     4     YY1  ,YY2  ,YY3  ,YY4  ,YY5  ,YY6  ,YY7  ,YY8 ,
     5     ZZ1  ,ZZ2  ,ZZ3  ,ZZ4  ,ZZ5  ,ZZ6  ,ZZ7  ,ZZ8 ,
     6     VX1  ,VX2  ,VX3  ,VX4  ,VX5  ,VX6  ,VX7  ,VX8 ,
     7     VY1  ,VY2  ,VY3  ,VY4  ,VY5  ,VY6  ,VY7  ,VY8 ,
     8     VZ1  ,VZ2  ,VZ3  ,VZ4  ,VZ5  ,VZ6  ,VZ7  ,VZ8 ,
     9     VRX1 ,VRX2 ,VRX3 ,VRX4 ,VRX5 ,VRX6 ,VRX7 ,VRX8 ,
     A     VRY1 ,VRY2 ,VRY3 ,VRY4 ,VRY5 ,VRY6 ,VRY7 ,VRY8 ,
     B     VRZ1 ,VRZ2 ,VRZ3 ,VRZ4 ,VRZ5 ,VRZ6 ,VRZ7 ,VRZ8 ,
     C     MAS1 ,MAS2 ,MAS3 ,MAS4 ,MAS5 ,MAS6 ,MAS7 ,MAS8 ,
     D     INN1 ,INN2 ,INN3 ,INN4 ,INN5 ,INN6 ,INN7 ,INN8 ,
     C     STIFM,STIFR,VISCM,VISCR)

      ENDIF


      CLOSE (UNIT=IOUT)


      END
