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


C================================================================= 
C     This subroutine reads the user material parameters. 
C================================================================= 
      SUBROUTINE LECMUSER01(IIN,IOUT,UPARAM,MAXUPARAM,NUPARAM, 
     .                NUVAR,IFUNC,MAXFUNC,NFUNC,STIFINT, 
     .                USERBUF) 
      USE LAW_USER 
C----------------------------------------------- 
C   I m p l i c i t   T y p e s 
C----------------------------------------------- 
      IMPLICIT NONE 
C----------------------------------------------- 
C   D u m m y   A r g u m e n t s 
C----------------------------------------------- 
      INTEGER IIN,IOUT,MAXUPARAM,NUPARAM,NUVAR,MAXFUNC,NFUNC, 
     .        IFUNC(MAXFUNC) 
      DOUBLE PRECISION   UPARAM(MAXUPARAM),STIFINT 
C----------------------------------------------- 
      TYPE(ULAWBUF) :: USERBUF  
C----------------------------------------------- 
C   L o c a l   V a r i a b l e s 
C----------------------------------------------- 
      DOUBLE PRECISION E,NU,A11,A12,A44 
      INTEGER DEBUG
C 
C====================================== 
C     ELASTIC LAW WITH SOLIDS 
C====================================== 
C 
C----------------------------------------------- 
C     INPUT FILE READING (USER DATA) 
C----------------------------------------------- 
      READ(IIN,'(2F20.0,I10)')E,NU,DEBUG
      A11 = E * (1.-NU) / (1.+NU) / (1.-2.*NU) 
      A12 = E * NU / (1.+NU) / (1.-2.*NU) 
      A44 = E / 2. / (1.+NU) 
C 
C----------------------------------------------- 
C     DATA CHECKING 
C----------------------------------------------- 
      IF(NU .LT. 0.0 .OR. NU .GE. 0.5)THEN 
        WRITE(IOUT,*)' ** ERROR : WRONG NU VALUE' 
        PRINT *,' ****** ERROR !!!  NU value out of range  !!!'
        call ARRET(0)
      ENDIF 
      
      NUPARAM = 4 
      
C----------------------------------------------- 
C     USER MATERIAL PARAMETERS DEFINITION   
C----------------------------------------------- 
C used in sigeps29 (solid 2d,3d) 
      UPARAM(1) = A11  
      UPARAM(2) = A12 
      UPARAM(3) = A44 
      UPARAM(4) = REAL(DEBUG) 

C 
C------------------------------------------------- 
C     NUMBER OF USER ELEMENT VARIABLES AND CURVES  
C------------------------------------------------- 
      NUVAR = 5 
      NFUNC = 0 
C 
C----------------------------------------------- 
C     USED FOR SOLIDS  
C----------------------------------------------- 
C used for interface (solid+shell) 
      STIFINT = A11 
C 
C------------------------------------------------- 
C     OUTPUT FILE PRINT  
C------------------------------------------------- 
      WRITE(IOUT,1000) 
      WRITE(IOUT,1100)E,NU 
C 
 1000 FORMAT( 
     & 5X,'  MY first ELASTIC USER LAW ',/,
     & 5X,'   compiled 2019.09.10 ',/,
     & 5X,'   with MinGW compiler ',/,
     & 5X,'        Marian         ',/,
     & 5X,'  -------------------  ',/,
     & 5X,'     only SOLIDS !!!   ',/, 
     & 5X,'  -------------------  ',//) 
 1100 FORMAT( 
     & 5X,'E . . . . . . . . . . . . . . . . . . .=',E12.4/ 
     & 5X,'NU. . . . . . . . . . . . . . . . . . .=',E12.4//) 
C 
C------------------------------------------------- 
      RETURN 
      END 