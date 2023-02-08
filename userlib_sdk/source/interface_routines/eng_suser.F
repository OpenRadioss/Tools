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
      SUBROUTINE ENG_SUSER(ITYP,
     1 NEL    ,NUVAR  ,IPROP  ,IMAT  ,SOLID_ID,TIME  ,TIMESTEP,
     2 EINT   ,VOL    ,UVAR   ,FR_WAVE,OFF    ,RHO    ,SIG    ,
     3 XX1    ,XX2    ,XX3    ,XX4    ,XX5    ,XX6    ,XX7    ,XX8    ,     
     4 YY1    ,YY2    ,YY3    ,YY4    ,YY5    ,YY6    ,YY7    ,YY8    ,  
     5 ZZ1    ,ZZ2    ,ZZ3    ,ZZ4    ,ZZ5    ,ZZ6    ,ZZ7    ,ZZ8    ,
     6 UX1    ,UX2    ,UX3    ,UX4    ,UX5    ,UX6    ,UX7    ,UX8    ,
     7 UY1    ,UY2    ,UY3    ,UY4    ,UY5    ,UY6    ,UY7    ,UY8    ,
     8 UZ1    ,UZ2    ,UZ3    ,UZ4    ,UZ5    ,UZ6    ,UZ7    ,UZ8    ,
     9 VX1    ,VX2    ,VX3    ,VX4    ,VX5    ,VX6    ,VX7    ,VX8    ,
     A VY1    ,VY2    ,VY3    ,VY4    ,VY5    ,VY6    ,VY7    ,VY8    ,
     B VZ1    ,VZ2    ,VZ3    ,VZ4    ,VZ5    ,VZ6    ,VZ7    ,VZ8    ,
     C VRX1   ,VRX2   ,VRX3   ,VRX4   ,VRX5   ,VRX6   ,VRX7   ,VRX8   ,
     D VRY1   ,VRY2   ,VRY3   ,VRY4   ,VRY5   ,VRY6   ,VRY7   ,VRY8   ,
     E VRZ1   ,VRZ2   ,VRZ3   ,VRZ4   ,VRZ5   ,VRZ6   ,VRZ7   ,VRZ8   ,
     F FX1    ,FX2    ,FX3    ,FX4    ,FX5    ,FX6    ,FX7    ,FX8    ,
     G FY1    ,FY2    ,FY3    ,FY4    ,FY5    ,FY6    ,FY7    ,FY8    ,
     H FZ1    ,FZ2    ,FZ3    ,FZ4    ,FZ5    ,FZ6    ,FZ7    ,FZ8    ,
     I MX1    ,MX2    ,MX3    ,MX4    ,MX5    ,MX6    ,MX7    ,MX8    ,
     J MY1    ,MY2    ,MY3    ,MY4    ,MY5    ,MY6    ,MY7    ,MY8    ,
     K MZ1    ,MZ2    ,MZ3    ,MZ4    ,MZ5    ,MZ6    ,MZ7    ,MZ8    ,
     L STIFM  ,STIFR  ,VISCM  ,VISCR  )

#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_SUSER" :: ENG_SUSER
!DEC$ ATTRIBUTES REFERENCE :: ITYP,
     1 NEL    ,NUVAR  ,IPROP  ,IMAT  ,SOLID_ID,TIME  ,TIMESTEP,
     2 EINT   ,VOL    ,UVAR   ,FR_WAVE,OFF    ,RHO    ,SIG    ,
     3 XX1    ,XX2    ,XX3    ,XX4    ,XX5    ,XX6    ,XX7    ,XX8    ,     
     4 YY1    ,YY2    ,YY3    ,YY4    ,YY5    ,YY6    ,YY7    ,YY8    ,  
     5 ZZ1    ,ZZ2    ,ZZ3    ,ZZ4    ,ZZ5    ,ZZ6    ,ZZ7    ,ZZ8    ,
     6 UX1    ,UX2    ,UX3    ,UX4    ,UX5    ,UX6    ,UX7    ,UX8    ,
     7 UY1    ,UY2    ,UY3    ,UY4    ,UY5    ,UY6    ,UY7    ,UY8    ,
     8 UZ1    ,UZ2    ,UZ3    ,UZ4    ,UZ5    ,UZ6    ,UZ7    ,UZ8    ,
     9 VX1    ,VX2    ,VX3    ,VX4    ,VX5    ,VX6    ,VX7    ,VX8    ,
     A VY1    ,VY2    ,VY3    ,VY4    ,VY5    ,VY6    ,VY7    ,VY8    ,
     B VZ1    ,VZ2    ,VZ3    ,VZ4    ,VZ5    ,VZ6    ,VZ7    ,VZ8    ,
     C VRX1   ,VRX2   ,VRX3   ,VRX4   ,VRX5   ,VRX6   ,VRX7   ,VRX8   ,
     D VRY1   ,VRY2   ,VRY3   ,VRY4   ,VRY5   ,VRY6   ,VRY7   ,VRY8   ,
     E VRZ1   ,VRZ2   ,VRZ3   ,VRZ4   ,VRZ5   ,VRZ6   ,VRZ7   ,VRZ8   ,
     F FX1    ,FX2    ,FX3    ,FX4    ,FX5    ,FX6    ,FX7    ,FX8    ,
     G FY1    ,FY2    ,FY3    ,FY4    ,FY5    ,FY6    ,FY7    ,FY8    ,
     H FZ1    ,FZ2    ,FZ3    ,FZ4    ,FZ5    ,FZ6    ,FZ7    ,FZ8    ,
     I MX1    ,MX2    ,MX3    ,MX4    ,MX5    ,MX6    ,MX7    ,MX8    ,
     J MY1    ,MY2    ,MY3    ,MY4    ,MY5    ,MY6    ,MY7    ,MY8    ,
     K MZ1    ,MZ2    ,MZ3    ,MZ4    ,MZ5    ,MZ6    ,MZ7    ,MZ8    ,
     L STIFM  ,STIFR  ,VISCM  ,VISCR
#endif
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   I n p u t     A r g u m e n t s 
C-----------------------------------------------
      INTEGER ITYP
C-----------------------------------------------
      INTEGER NEL,NUVAR,IPROP,IMAT,SOLID_ID(*)
      my_real
     .   TIME,TIMESTEP,UVAR(NEL,NUVAR),
     .   STIFM(*) ,STIFR(*) , VISCM(*) ,VISCR(*) ,FR_WAVE(*),
     .   OFF(*) ,EINT(*) , RHO(*) ,VOL(*) ,SIG(6,*),
     2 XX1(*),XX2(*),XX3(*),XX4(*),XX5(*),XX6(*),XX7(*),XX8(*),
     3 YY1(*),YY2(*),YY3(*),YY4(*),YY5(*),YY6(*),YY7(*),YY8(*),
     4 ZZ1(*),ZZ2(*),ZZ3(*),ZZ4(*),ZZ5(*),ZZ6(*),ZZ7(*),ZZ8(*),
     2 UX1(*),UX2(*),UX3(*),UX4(*),UX5(*),UX6(*),UX7(*),UX8(*),
     3 UY1(*),UY2(*),UY3(*),UY4(*),UY5(*),UY6(*),UY7(*),UY8(*),
     4 UZ1(*),UZ2(*),UZ3(*),UZ4(*),UZ5(*),UZ6(*),UZ7(*),UZ8(*),
     5 VX1(*),VX2(*),VX3(*),VX4(*),VX5(*),VX6(*),VX7(*),VX8(*),
     6 VY1(*),VY2(*),VY3(*),VY4(*),VY5(*),VY6(*),VY7(*),VY8(*),
     7 VZ1(*),VZ2(*),VZ3(*),VZ4(*),VZ5(*),VZ6(*),VZ7(*),VZ8(*),
     8 VRX1(*),VRX2(*),VRX3(*),VRX4(*),VRX5(*),VRX6(*),VRX7(*),VRX8(*),
     9 VRY1(*),VRY2(*),VRY3(*),VRY4(*),VRY5(*),VRY6(*),VRY7(*),VRY8(*),
     A VRZ1(*),VRZ2(*),VRZ3(*),VRZ4(*),VRZ5(*),VRZ6(*),VRZ7(*),VRZ8(*),
     B FX1(*),FX2(*),FX3(*),FX4(*),FX5(*),FX6(*),FX7(*),FX8(*),
     C FY1(*),FY2(*),FY3(*),FY4(*),FY5(*),FY6(*),FY7(*),FY8(*),
     D FZ1(*),FZ2(*),FZ3(*),FZ4(*),FZ5(*),FZ6(*),FZ7(*),FZ8(*),
     E MX1(*),MX2(*),MX3(*),MX4(*),MX5(*),MX6(*),MX7(*),MX8(*),
     F MY1(*),MY2(*),MY3(*),MY4(*),MY5(*),MY6(*),MY7(*),MY8(*),
     G MZ1(*),MZ2(*),MZ3(*),MZ4(*),MZ5(*),MZ6(*),MZ7(*),MZ8(*)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
#ifndef ncharline
#define ncharline 500
#endif
      INTEGER IOUT,LENLINE,itsk
      CHARACTER LINE*ncharline
      INTEGER GET_U_TASK
      EXTERNAL GET_U_TASK
C-----------------------------------------------
C Open the Output File
        itsk=get_u_task()
        IOUT=31*10000+itsk

C Open the Output File
      OPEN(UNIT=IOUT,STATUS='SCRATCH', FORM='FORMATTED')

      IF (ITYP==29)THEN

       CALL SUSER29(
     1 NEL    ,NUVAR  ,IOUT   ,IPROP  ,IMAT  ,SOLID_ID,TIME  ,TIMESTEP,
     2 EINT   ,VOL    ,UVAR   ,FR_WAVE,OFF    ,RHO    ,SIG    ,
     3 XX1    ,XX2    ,XX3    ,XX4    ,XX5    ,XX6    ,XX7    ,XX8    ,     
     4 YY1    ,YY2    ,YY3    ,YY4    ,YY5    ,YY6    ,YY7    ,YY8    ,  
     5 ZZ1    ,ZZ2    ,ZZ3    ,ZZ4    ,ZZ5    ,ZZ6    ,ZZ7    ,ZZ8    ,
     6 UX1    ,UX2    ,UX3    ,UX4    ,UX5    ,UX6    ,UX7    ,UX8    ,
     7 UY1    ,UY2    ,UY3    ,UY4    ,UY5    ,UY6    ,UY7    ,UY8    ,
     8 UZ1    ,UZ2    ,UZ3    ,UZ4    ,UZ5    ,UZ6    ,UZ7    ,UZ8    ,
     9 VX1    ,VX2    ,VX3    ,VX4    ,VX5    ,VX6    ,VX7    ,VX8    ,
     A VY1    ,VY2    ,VY3    ,VY4    ,VY5    ,VY6    ,VY7    ,VY8    ,
     B VZ1    ,VZ2    ,VZ3    ,VZ4    ,VZ5    ,VZ6    ,VZ7    ,VZ8    ,
     C VRX1   ,VRX2   ,VRX3   ,VRX4   ,VRX5   ,VRX6   ,VRX7   ,VRX8   ,
     D VRY1   ,VRY2   ,VRY3   ,VRY4   ,VRY5   ,VRY6   ,VRY7   ,VRY8   ,
     E VRZ1   ,VRZ2   ,VRZ3   ,VRZ4   ,VRZ5   ,VRZ6   ,VRZ7   ,VRZ8   ,
     F FX1    ,FX2    ,FX3    ,FX4    ,FX5    ,FX6    ,FX7    ,FX8    ,
     G FY1    ,FY2    ,FY3    ,FY4    ,FY5    ,FY6    ,FY7    ,FY8    ,
     H FZ1    ,FZ2    ,FZ3    ,FZ4    ,FZ5    ,FZ6    ,FZ7    ,FZ8    ,
     I MX1    ,MX2    ,MX3    ,MX4    ,MX5    ,MX6    ,MX7    ,MX8    ,
     J MY1    ,MY2    ,MY3    ,MY4    ,MY5    ,MY6    ,MY7    ,MY8    ,
     K MZ1    ,MZ2    ,MZ3    ,MZ4    ,MZ5    ,MZ6    ,MZ7    ,MZ8    ,
     L STIFM  ,STIFR  ,VISCM  ,VISCR  )
     
      ELSEIF(ITYP==30)THEN

       CALL SUSER30(
     1 NEL    ,NUVAR  ,IOUT   ,IPROP  ,IMAT  ,SOLID_ID,TIME  ,TIMESTEP,
     2 EINT   ,VOL    ,UVAR   ,FR_WAVE,OFF    ,RHO    ,SIG    ,
     3 XX1    ,XX2    ,XX3    ,XX4    ,XX5    ,XX6    ,XX7    ,XX8    ,     
     4 YY1    ,YY2    ,YY3    ,YY4    ,YY5    ,YY6    ,YY7    ,YY8    ,  
     5 ZZ1    ,ZZ2    ,ZZ3    ,ZZ4    ,ZZ5    ,ZZ6    ,ZZ7    ,ZZ8    ,
     6 UX1    ,UX2    ,UX3    ,UX4    ,UX5    ,UX6    ,UX7    ,UX8    ,
     7 UY1    ,UY2    ,UY3    ,UY4    ,UY5    ,UY6    ,UY7    ,UY8    ,
     8 UZ1    ,UZ2    ,UZ3    ,UZ4    ,UZ5    ,UZ6    ,UZ7    ,UZ8    ,
     9 VX1    ,VX2    ,VX3    ,VX4    ,VX5    ,VX6    ,VX7    ,VX8    ,
     A VY1    ,VY2    ,VY3    ,VY4    ,VY5    ,VY6    ,VY7    ,VY8    ,
     B VZ1    ,VZ2    ,VZ3    ,VZ4    ,VZ5    ,VZ6    ,VZ7    ,VZ8    ,
     C VRX1   ,VRX2   ,VRX3   ,VRX4   ,VRX5   ,VRX6   ,VRX7   ,VRX8   ,
     D VRY1   ,VRY2   ,VRY3   ,VRY4   ,VRY5   ,VRY6   ,VRY7   ,VRY8   ,
     E VRZ1   ,VRZ2   ,VRZ3   ,VRZ4   ,VRZ5   ,VRZ6   ,VRZ7   ,VRZ8   ,
     F FX1    ,FX2    ,FX3    ,FX4    ,FX5    ,FX6    ,FX7    ,FX8    ,
     G FY1    ,FY2    ,FY3    ,FY4    ,FY5    ,FY6    ,FY7    ,FY8    ,
     H FZ1    ,FZ2    ,FZ3    ,FZ4    ,FZ5    ,FZ6    ,FZ7    ,FZ8    ,
     I MX1    ,MX2    ,MX3    ,MX4    ,MX5    ,MX6    ,MX7    ,MX8    ,
     J MY1    ,MY2    ,MY3    ,MY4    ,MY5    ,MY6    ,MY7    ,MY8    ,
     K MZ1    ,MZ2    ,MZ3    ,MZ4    ,MZ5    ,MZ6    ,MZ7    ,MZ8    ,
     L STIFM  ,STIFR  ,VISCM  ,VISCR  )

      ELSEIF(ITYP==31)THEN

       CALL SUSER31(
     1 NEL    ,NUVAR  ,IOUT   ,IPROP  ,IMAT  ,SOLID_ID,TIME  ,TIMESTEP,
     2 EINT   ,VOL    ,UVAR   ,FR_WAVE,OFF    ,RHO    ,SIG    ,
     3 XX1    ,XX2    ,XX3    ,XX4    ,XX5    ,XX6    ,XX7    ,XX8    ,     
     4 YY1    ,YY2    ,YY3    ,YY4    ,YY5    ,YY6    ,YY7    ,YY8    ,  
     5 ZZ1    ,ZZ2    ,ZZ3    ,ZZ4    ,ZZ5    ,ZZ6    ,ZZ7    ,ZZ8    ,
     6 UX1    ,UX2    ,UX3    ,UX4    ,UX5    ,UX6    ,UX7    ,UX8    ,
     7 UY1    ,UY2    ,UY3    ,UY4    ,UY5    ,UY6    ,UY7    ,UY8    ,
     8 UZ1    ,UZ2    ,UZ3    ,UZ4    ,UZ5    ,UZ6    ,UZ7    ,UZ8    ,
     9 VX1    ,VX2    ,VX3    ,VX4    ,VX5    ,VX6    ,VX7    ,VX8    ,
     A VY1    ,VY2    ,VY3    ,VY4    ,VY5    ,VY6    ,VY7    ,VY8    ,
     B VZ1    ,VZ2    ,VZ3    ,VZ4    ,VZ5    ,VZ6    ,VZ7    ,VZ8    ,
     C VRX1   ,VRX2   ,VRX3   ,VRX4   ,VRX5   ,VRX6   ,VRX7   ,VRX8   ,
     D VRY1   ,VRY2   ,VRY3   ,VRY4   ,VRY5   ,VRY6   ,VRY7   ,VRY8   ,
     E VRZ1   ,VRZ2   ,VRZ3   ,VRZ4   ,VRZ5   ,VRZ6   ,VRZ7   ,VRZ8   ,
     F FX1    ,FX2    ,FX3    ,FX4    ,FX5    ,FX6    ,FX7    ,FX8    ,
     G FY1    ,FY2    ,FY3    ,FY4    ,FY5    ,FY6    ,FY7    ,FY8    ,
     H FZ1    ,FZ2    ,FZ3    ,FZ4    ,FZ5    ,FZ6    ,FZ7    ,FZ8    ,
     I MX1    ,MX2    ,MX3    ,MX4    ,MX5    ,MX6    ,MX7    ,MX8    ,
     J MY1    ,MY2    ,MY3    ,MY4    ,MY5    ,MY6    ,MY7    ,MY8    ,
     K MZ1    ,MZ2    ,MZ3    ,MZ4    ,MZ5    ,MZ6    ,MZ7    ,MZ8    ,
     L STIFM  ,STIFR  ,VISCM  ,VISCR  )
 
      ENDIF

      REWIND(IOUT)
      DO WHILE(.TRUE.)
          READ(UNIT=IOUT,END=999,FMT='(A)')LINE    
          LENLINE=LEN_TRIM(LINE)
          CALL WRITE_IOUT(LINE,LENLINE)
      ENDDO
 999  CONTINUE 
      CLOSE (UNIT=IOUT)


      END
