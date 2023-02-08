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
Chd|  LECR04                        src/user2/lecr04.F            
Chd|-- called by -----------
Chd|        LECFAIL                       src/mater1/lecfail.F          
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE LECR04(IIN  ,IOUT ,UPARAM ,MAXUPARAM,NUPARAM,
     .                  NUVAR,IFUNC,MAXFUNC,NFUNC,ID)
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C IIN      |  1      | I | R | INPUT FILE UNIT (D00 file) 
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
C UPARAM   | NUPARAM | F | W | USER FAILURE MODEL PARAMETER ARRAY
C MAXUPARAM|  1      | I | R | MAXIMUM SIZE OF UPARAM 
C NUPARAM  |  1      | I | W | SIZE OF UPARAM =< MAXUPARAM
C NUVAR    |  1      | I | W | NUMBER OF USER  VARIABLES
C----------+---------+---+---+--------------------------------------------
C IFUNC    | NFUNC   | I | W | FUNCTION NUMBER ARRAY
C MAXFUNC  |  1      | I | R | MAXIMUM SIZE OF IFUNC
C NFUNC    |  1      | I | W | SIZE OF IFUNC =< MAXFUNC
C----------+---------+---+---+--------------------------------------------
C-----------------------------------------------
C   D u m m y   A r g u m e n t s
C-----------------------------------------------
      INTEGER IIN,IOUT,MAXUPARAM,NUPARAM,NUVAR,MAXFUNC,NFUNC,
     .        IFUNC(MAXFUNC),ID
      my_real   UPARAM(MAXUPARAM)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER ISHELL, ISOLID
      my_real EPSMAX
      my_real EP30
      CHARACTER*50 FMT_F_2I
C======================================
      EP30=1.E30
      FMT_F_2I = "(F20.0,2I10)"
C======================================
C
C     EXEMPLE : critere en epsmax
C
C======================================
C
      READ(IIN,FMT_F_2I)epsmax,ISHELL,ISOLID
      IF(EPSMAX.EQ.0)EPSMAX=EP30
      IF(ISHELL.EQ.0)ISHELL=1
      IF(ISOLID.EQ.0)ISOLID=1
      UPARAM(1) = EPSMAX
      UPARAM(2) = ISHELL
      UPARAM(3) = ISOLID
      NUPARAM = 3
      NUVAR = 0
C
      NFUNC = 0
       WRITE(IOUT, 1000)EPSMAX
C for shell      
      IF(ISHELL.EQ.1)THEN
        WRITE(IOUT, 1100)
      ELSEIF(ISHELL.EQ.2)THEN
        WRITE(IOUT, 1200)
      ENDIF
c for solid      
      IF(ISOLID.EQ.1)THEN
        WRITE(IOUT, 2100)
      ELSEIF(ISOLID.EQ.2)THEN
        WRITE(IOUT, 2200)
      ENDIF         
 1000 FORMAT(
     & 5X,40H        PARAMETER                       ,/,
     & 5X,40H  -----------------------------         ,/,
     & 5X,'MAX PLASTIC DEFORMATION        .. . . . . =',E12.4//)
 1100 FORMAT(
     & 5X,'   SHELL ELEMENT DELETION ') 
 2100 FORMAT(
     & 5X,'   SOLID ELEMENT  DELETION ') 

 1200 FORMAT(
     & 5X,'    SHELL TENSOR STRESS OF LAYER WILL BE VANISHED ')    
 2200 FORMAT(
     & 5X,'    DEVIATORIC STRESS WILL BE VANISHED ')    

      RETURN
      END
