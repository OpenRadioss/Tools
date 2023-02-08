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


C
Chd|====================================================================
Chd|  LUSER01C                                                    
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|        LAW_USERSH                                                  
Chd|====================================================================
      SUBROUTINE LUSER59C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO0   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,USERBUF)
C ----------------------------------------
      USE LAW_USERSH
C --------------------------------------------
#include "implicit_f.inc"
C --------------------------------------------
      INTEGER  NEL,NUVAR,NUPARAM,NGL(NEL)
      DOUBLE PRECISION
     .   TIME,PLA(NEL), UVAR(NEL,NUVAR),UPARAM(NUPARAM),
     .   TIMESTEP(NEL), AREA(NEL),OFF(NEL),VISCMAX(NEL),
     .   EINT(2,NEL), SHF(NEL), SOUNDSP(NEL),RHO0(NEL),
     .   SIGY(NEL)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER  NPT, IPT,IFLAG
       DOUBLE PRECISION 
     .   THKLYL(MVSIZ),THKN(MVSIZ),
     .   EPSPXX(MVSIZ),EPSPYY(MVSIZ),
     .   EPSPXY(MVSIZ),EPSPYZ(MVSIZ),EPSPZX(MVSIZ),
     .   DEPSXX(MVSIZ),DEPSYY(MVSIZ),
     .   DEPSXY(MVSIZ),DEPSYZ(MVSIZ),DEPSZX(MVSIZ),
     .   EPSXX(MVSIZ) ,EPSYY(MVSIZ) ,
     .   EPSXY(MVSIZ) ,EPSYZ(MVSIZ) ,EPSZX(MVSIZ) ,
     .   SIGOXX(MVSIZ),SIGOYY(MVSIZ),
     .   SIGOXY(MVSIZ),SIGOYZ(MVSIZ),SIGOZX(MVSIZ)
C-----------------------------------------------
C   O U T P U T   A r g u m e n t s
C-----------------------------------------------
      DOUBLE PRECISION
     .    SIGNXX(MVSIZ),SIGNYY(MVSIZ),
     .    SIGNXY(MVSIZ),SIGNYZ(MVSIZ),SIGNZX(MVSIZ),
     .    SIGVXX(MVSIZ),SIGVYY(MVSIZ),
     .    SIGVXY(MVSIZ),SIGVYZ(MVSIZ),SIGVZX(MVSIZ),
     .    DPLA(MVSIZ),ETSE(MVSIZ)
C-----------------------------------------------
      TYPE(ULAWCINTBUF) :: USERBUF
C----------------------------------------------- 
C   VARIABLES FOR FUNCTION INTERPOLATION 
C-----------------------------------------------
      INTEGER NFUNC, IFUNC(NFUNC),NPF(*)
      DOUBLE PRECISION   FINTER ,TF(*)
      EXTERNAL FINTER
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='/MAT/USER59 - SHELL '
        SIZE=LEN_TRIM(OPTION)
        WRITE(6,'(A)')
     .     '** ERROR IN USER LIBRARY SDK'
         WRITE(6,'(A,A)')
     .     ' OPTION : ',OPTION(1:SIZE)
        WRITE(6,'(A)')
     .     'USER INTERFACE OPTION USED, BUT NO USER INTERFACE ROUTINE IS FOUND IN SDK'

        CALL ARRET(2)
      END 
C----------------------------------------------- 
