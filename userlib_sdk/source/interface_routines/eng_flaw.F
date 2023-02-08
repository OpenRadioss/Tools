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
      SUBROUTINE ENG_FLAW(IRUP,
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,
     2     NPF    ,TF     ,TIME   ,TIMESTEP ,UPARAM  ,
     3     NGL    ,IPM    ,NPROPMI,MAT,IDEL7NOK,
     4     EPSPXX ,EPSPYY ,EPSPZZ  ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
     5     EPSXX  ,EPSYY  ,EPSZZ   ,EPSXY   ,EPSYZ   ,EPSZX  ,
     6     SIGNXX ,SIGNYY ,SIGNZZ  ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
     7     PLA    ,DPLA    ,EPSP   ,UVAR    ,OFF     ,
     8     BIDON1  ,BIDON2   ,BIDON3  ,BIDON4  ,BIDON5        )
C-----------------------------------------------
C   E X P O R T   I N   D L L 
C-----------------------------------------------

#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_FLAW" :: ENG_FLAW
!DEC$ ATTRIBUTES REFERENCE :: IRUP,
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,
     2     NPF    ,TF     ,TIME   ,TIMESTEP ,UPARAM  ,
     3     NGL    ,IPM    ,NPROPMI,MAT,IDEL7NOK,
     4     EPSPXX ,EPSPYY ,EPSPZZ  ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
     5     EPSXX  ,EPSYY  ,EPSZZ   ,EPSXY   ,EPSYZ   ,EPSZX  ,
     6     SIGNXX ,SIGNYY ,SIGNZZ  ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
     7     PLA    ,DPLA    ,EPSP   ,UVAR    ,OFF     ,
     8     BIDON1  ,BIDON2   ,BIDON3  ,BIDON4  ,BIDON5 
#endif
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   I n p u t     A r g u m e n t s 
C-----------------------------------------------
      INTEGER IRUP,NEL, NUPARAM,NPROPMI, NUVAR,NGL(NEL),IPM(NPROPMI,*),
     .        MAT(NEL),IDEL7NOK
      my_real 
     .   TIME,TIMESTEP,UPARAM(NUPARAM),
     .   DPLA(NEL),EPSP(NEL),PLA(NEL),
     .   EPSPXX(NEL),EPSPYY(NEL),EPSPZZ(NEL),
     .   EPSPXY(NEL),EPSPYZ(NEL),EPSPZX(NEL),
     .   EPSXX(NEL) ,EPSYY(NEL) ,EPSZZ(NEL) ,
     .   EPSXY(NEL) ,EPSYZ(NEL) ,EPSZX(NEL) ,
     .   BIDON1 ,BIDON2 ,BIDON3 ,BIDON4 ,BIDON5
C-----------------------------------------------
C   O u t P u t   A r g u m e n t s 
C-----------------------------------------------
C-----------------------------------------------
C   I N P U T   O U T P U T   A r g u m e n t s
C-----------------------------------------------
      my_real 
     .  UVAR(NEL,NUVAR), OFF(NEL),
     .   SIGNXX(NEL),SIGNYY(NEL),SIGNZZ(NEL),
     .   SIGNXY(NEL),SIGNYZ(NEL),SIGNZX(NEL)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER LENROOTN,IIN,IOUT   
      CHARACTER FILNAM*512,CLAW*4
      INTEGER LEN_FILNAM
C-----------------------------------------------
C   VARIABLES FOR FUNCTION INTERPOLATION
C-----------------------------------------------
      INTEGER NPF(*), NFUNC, IFUNC(NFUNC)
      my_real FINTER ,TF(*)
      EXTERNAL FINTER
C-----------------------------------------------

      IF (IRUP==4)THEN
        CALL F04LAW (
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,
     2     NPF    ,TF     ,TIME   ,TIMESTEP ,UPARAM  ,
     3     NGL    ,IPM    ,NPROPMI,MAT,IDEL7NOK,
     4     EPSPXX ,EPSPYY ,EPSPZZ  ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
     5     EPSXX  ,EPSYY  ,EPSZZ   ,EPSXY   ,EPSYZ   ,EPSZX  ,
     6     SIGNXX ,SIGNYY ,SIGNZZ  ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
     7     PLA    ,DPLA    ,EPSP   ,UVAR    ,OFF     ,
     8     BIDON1  ,BIDON2   ,BIDON3  ,BIDON4  ,BIDON5 )

      ELSEIF(IRUP==5)THEN
        CALL F05LAW (
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,
     2     NPF    ,TF     ,TIME   ,TIMESTEP ,UPARAM  ,
     3     NGL    ,IPM    ,NPROPMI,MAT,IDEL7NOK,
     4     EPSPXX ,EPSPYY ,EPSPZZ  ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
     5     EPSXX  ,EPSYY  ,EPSZZ   ,EPSXY   ,EPSYZ   ,EPSZX  ,
     6     SIGNXX ,SIGNYY ,SIGNZZ  ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
     7     PLA    ,DPLA    ,EPSP   ,UVAR    ,OFF     ,
     8     BIDON1  ,BIDON2   ,BIDON3  ,BIDON4  ,BIDON5 )

      ELSEIF(IRUP==6)THEN
        CALL F06LAW (
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,
     2     NPF    ,TF     ,TIME   ,TIMESTEP ,UPARAM  ,
     3     NGL    ,IPM    ,NPROPMI,MAT,IDEL7NOK,
     4     EPSPXX ,EPSPYY ,EPSPZZ  ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
     5     EPSXX  ,EPSYY  ,EPSZZ   ,EPSXY   ,EPSYZ   ,EPSZX  ,
     6     SIGNXX ,SIGNYY ,SIGNZZ  ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
     7     PLA    ,DPLA    ,EPSP   ,UVAR    ,OFF     ,
     8     BIDON1  ,BIDON2   ,BIDON3  ,BIDON4  ,BIDON5 )

      ENDIF


      END
