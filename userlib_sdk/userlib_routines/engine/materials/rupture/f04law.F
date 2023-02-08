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
Chd|  F04LAW                        src/user2/f04law.F            
Chd|-- called by -----------
Chd|        MULAW                         src/matera/mulaw.F            
Chd|        MULAW8                        src/matera/mulaw8.F           
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE F04LAW (
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,
     2     NPF    ,TF     ,TIME   ,TIMESTEP ,UPARAM  ,
     3     NGL    ,IPM    ,NPROPMI,MAT,IDEL7NOK,
     4     EPSPXX ,EPSPYY ,EPSPZZ  ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
     5     EPSXX  ,EPSYY  ,EPSZZ   ,EPSXY   ,EPSYZ   ,EPSZX  ,
     6     SIGNXX ,SIGNYY ,SIGNZZ  ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
     7     PLA    ,DPLA    ,EPSP   ,UVAR    ,OFF     ,
     8     BIDON1  ,BIDON2   ,BIDON3  ,BIDON4  ,BIDON5 )
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C---------+---------+---+---+--------------------------------------------
C VAR     | SIZE    |TYP| RW| DEFINITION
C---------+---------+---+---+--------------------------------------------
C NEL     |  1      | I | R | SIZE OF THE ELEMENT GROUP NEL 
C NUPARAM |  1      | I | R | SIZE OF THE USER PARAMETER ARRAY
C NUVAR   |  1      | I | R | NUMBER OF FAILURE ELEMENT VARIABLES
C---------+---------+---+---+--------------------------------------------
C NFUNC   |  1      | I | R | NUMBER FUNCTION USED FOR THIS USER LAW
C IFUNC   | NFUNC   | I | R | FUNCTION INDEX 
C NPF     |  *      | I | R | FUNCTION ARRAY   
C TF      |  *      | F | R | FUNCTION ARRAY 
C---------+---------+---+---+--------------------------------------------
C TIME    |  1      | F | R | CURRENT TIME
C TIMESTEP|  1      | F | R | CURRENT TIME STEP
C UPARAM  | NUPARAM | F | R | USER FAILURE PARAMETER ARRAY
C---------+---------+---+---+--------------------------------------------
C SIGNXX  | NEL     | F | W | NEW ELASTO PLASTIC STRESS XX
C SIGNYY  | NEL     | F | W | NEW ELASTO PLASTIC STRESS YY
C ...     |         |   |   |
C ...     |         |   |   |
C---------+---------+---+---+--------------------------------------------
C UVAR    |NEL*NUVAR| F |R/W| USER ELEMENT VARIABLE ARRAY
C OFF     | NEL     | F |R/W| DELETED ELEMENT FLAG (=1. ON, =0. OFF)
C---------+---------+---+---+--------------------------------------------
#include "mvsiz_p.inc"
c#include "scr17_c.inc"
c#include "units_c.inc"
c#include "comlock.inc"
c#include "param_c.inc"
C-----------------------------------------------
C   I N P U T   A r g u m e n t s
C-----------------------------------------------
C
      INTEGER NEL, NUPARAM,NPROPMI, NUVAR,NGL(NEL),IPM(NPROPMI,*),
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
C   O U T P U T   A r g u m e n t s
C-----------------------------------------------
cc      my_real
 
C-----------------------------------------------
C   I N P U T   O U T P U T   A r g u m e n t s 
C-----------------------------------------------
      my_real 
     .  UVAR(NEL,NUVAR), OFF(NEL),
     .   SIGNXX(NEL),SIGNYY(NEL),SIGNZZ(NEL),
     .   SIGNXY(NEL),SIGNYZ(NEL),SIGNZX(NEL)
C-----------------------------------------------
C   VARIABLES FOR FUNCTION INTERPOLATION 
C-----------------------------------------------
      INTEGER NPF(*), NFUNC, IFUNC(NFUNC)
      my_real FINTER ,TF(*)
      EXTERNAL FINTER
C        Y = FINTER(IFUNC(J),X,NPF,TF,DYDX)
C        Y       : y = f(x)
C        X       : x
C        DYDX    : f'(x) = dy/dx
C        IFUNC(J): FUNCTION INDEX
C              J : FIRST(J=1), SECOND(J=2) .. FUNCTION USED FOR THIS LAW
C        NPF,TF  : FUNCTION PARAMETER
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER I,J,IDEL,IDEV,IFLAG(MVSIZ),INDX(MVSIZ),IADBUF,NINDX,
     .        NINDEX,INDEX(MVSIZ),IR,IFAIL,JST(MVSIZ),JJ
      my_real EPSMAX(MVSIZ),P

      my_real  ZERO,UN,QCINQ
C-----------------------------------------------
      ZERO=0.0
      UN=1.0
      QCINQ=4./5.
C--------------------------------------------------------------
C       ex : deletion d'element sur critere epsmax
C
      IR = 0
      DO I=1,NEL
        IFAIL = IPM(111,MAT(I))
        IF(IFAIL.EQ.4)THEN 
         IADBUF = IPM(114,MAT(I))
         EPSMAX(I) = UPARAM(IADBUF)
         IFLAG(I) = NINT(UPARAM(IADBUF+2))
         IR = IR + 1
         JST(IR) = I
        ENDIF 
      ENDDO
C-----------------------------------------------
C     USER VARIABLES INITIALIZATION
C-----------------------------------------------
      IF(TIME.EQ.ZERO)THEN
       DO JJ=1,IR
        I = JST(JJ)
        DO J=1,NUVAR       
          UVAR(I,J)= ZERO
        ENDDO
       ENDDO   
      ENDIF   
Cc
      IDEL=0
      IDEV=0
      DO J=1,IR
        I = JST(J)
        IF(IFLAG(I).EQ.1)THEN
         IDEL=1
        ELSEIF(IFLAG(I).EQ.2)THEN
         IDEV =1
        END IF
      END DO
C...
      IF(IDEL.EQ.1)THEN
        DO J=1,IR
          I = JST(J)
          IF(OFF(I).LT.0.1) OFF(I)=0.0
          IF(OFF(I).LT.1.0) OFF(I)=OFF(I)*0.8
        END DO
      END IF
C      
      IF(IDEL.EQ.1)THEN
       NINDX=0  
       DO J=1,IR
        I = JST(J)
        IF(IFLAG(I).EQ.1.AND.OFF(I).EQ.UN)THEN     
         IF(PLA(I).GE.EPSMAX(I)) THEN
          OFF(I)=QCINQ
c          NINDX=NINDX+1
c          INDX(NINDX)=I
          IDEL7NOK = 1                  
         ENDIF
        ENDIF 
       ENDDO
c       IF(NINDX.GT.0)THEN
c        DO J=1,NINDX
c#include "lockon.inc"
c         WRITE(IOUT, 1000) NGL(INDX(J))
c         WRITE(ISTDO,1100) NGL(INDX(J)),TIME
c#include "lockoff.inc"
c        END DO
c       END IF         
       ENDIF
Cc deviatoric will be vanished      
      IF(IDEV.EQ.1)THEN
       NINDX=0 
       NINDEX = 0 
       DO J=1,IR
        I = JST(J) 
        IF(IFLAG(I).EQ.2.AND.OFF(I).EQ.UN)THEN 
         IF(PLA(I).GE.EPSMAX(I))THEN          
c           NINDX=NINDX+1
c           INDX(NINDX)=I
           SIGNXX(I) =   P
           SIGNYY(I) =   P
           SIGNZZ(I) =   P
           SIGNXY(I) = ZERO
           SIGNYZ(I) = ZERO
           SIGNZX(I) = ZERO
                            
          ENDIF
        ENDIF  
       ENDDO
c       IF(NINDX.GT.0)THEN
c        DO J=1,NINDX
c         I = INDX(J)
c#include "lockon.inc"
c         WRITE(IOUT, 2000) NGL(I)
c         WRITE(ISTDO,2100) NGL(I),TIME
c#include "lockoff.inc"
c        END DO
c       END IF           
      ENDIF      
C-----------------------------------------------
c 1000 FORMAT(1X,'DELETE SOLID ELEMENT NUMBER ',I10)
c 1100 FORMAT(1X,'DELETE SOLID ELEMENT NUMBER ',I10,
c     .          ' AT TIME :',1PE20.13)
cCC     
c 2000 FORMAT(1X,' DEVIATORIC STRESS WILL BE VANISHED',I10)
c 2100 FORMAT(1X,' DEVIATORIC STRESS WILL BE VANISHED',I10,
c     .          ' AT TIME :',1PE20.13)
      RETURN
      END
