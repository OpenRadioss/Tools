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
Chd|  F04LAWC                       src/user2/f04lawc.F           
Chd|-- called by -----------
Chd|        MULAWC                        src/coque/mulawc.F            
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE F04LAWC(
     1     NEL   ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC  ,NPF    ,
     2     TF    ,TIME   ,TIMESTEP,UPARAM  , NGL   ,IPT    ,
     3     NPT0  ,IPM    ,NPROPMI ,MAT   ,
     4     SIGNXX ,SIGNYY ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
     4     EPSPXX ,EPSPYY ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
     6     EPSXX  ,EPSYY  ,EPSXY   ,EPSYZ   ,EPSZX  ,
     7     PLA    ,DPLA   ,EPSP    ,UVAR    ,UEL    , 
     8     OFF    ,LENGTH ,AREA    ,BIDON3  ,BIDON4  ,BIDON5  )
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C-----------------------------------------------
C   G l o b a l   P a r a m e t e r s
C-----------------------------------------------
#include  "mvsiz_p.inc"
c#include "scr17_c.inc"
c#include "units_c.inc"
c#include  "comlock.inc"
c#include  "param_c.inc"
C---------+---------+---+---+--------------------------------------------
C VAR     | SIZE    |TYP| RW| DEFINITION
C---------+---------+---+---+--------------------------------------------
C NEL     |  1      | I | R | SIZE OF THE ELEMENT GROUP NEL 
C NUPARAM |  1      | I | R | SIZE OF THE USER PARAMETER ARRAY
C NUVAR   |  1      | I | R | NUMBER OF USER ELEMENT VARIABLES
C---------+---------+---+---+--------------------------------------------
C NFUNC   |  1      | I | R | NUMBER FUNCTION USED FOR THIS USER LAW
C IFUNC   | NFUNC   | I | R | FUNCTION INDEX 
C NPF     |  *      | I | R | FUNCTION ARRAY   
C NPT     |  1      | I | R | NUMBER OF LAYERS OR INTEGRATION POINTS   
C IPT     |  1      | I | R | LAYER OR INTEGRATION POINT NUMBER      
C TF      |  *      | F | R | FUNCTION ARRAY 
C NGL     | NEL     | I | R | ELEMEMT NUMBER
C---------+---------+---+---+--------------------------------------------
C TIME    |  1      | F | R | CURRENT TIME
C TIMESTEP|  1      | F | R | CURRENT TIME STEP
C UPARAM  | NUPARAM | F | R | USER MATERIAL PARAMETER ARRAY
C EPSPXX  | NEL     | F | R | STRAIN RATE XX
C EPSPYY  | NEL     | F | R | STRAIN RATE YY
C ...     |         |   |   |
C EPSXX   | NEL     | F | R | STRAIN XX
C EPSYY   | NEL     | F | R | STRAIN YY
C---------+---------+---+---+--------------------------------------------
C SIGNXX  | NEL     | F | W | NEW ELASTO PLASTIC STRESS XX
C SIGNYY  | NEL     | F | W | NEW ELASTO PLASTIC STRESS YY
C ...     |         |   |   |
C---------+---------+---+---+--------------------------------------------
C PLA     | NEL     | F |R/W| PLASTIC STRAIN
C UVAR    |NEL*NUVAR| F |R/W| USER ELEMENT VARIABLE ARRAY
C OFF     | NEL     | F |R/W| DELETED ELEMENT FLAG (=1. ON, =0. OFF)
C---------+---------+---+---+--------------------------------------------
C   I N P U T   A r g u m e n t s
C-----------------------------------------------
      INTEGER NEL, NUPARAM, NUVAR, NGL(NEL),MAT(NEL),NPROPMI,
     .  IPT,NPT0,IPM(NPROPMI,*)
      my_real 
     .   TIME,TIMESTEP(NEL),UPARAM(NUPARAM),DPLA(NEL),
     .   EPSP(NEL), PLA(NEL) ,LENGTH(NEL) ,AREA(NEL),
     .   EPSPXX(NEL),EPSPYY(NEL),EPSPXY(NEL),EPSPYZ(NEL),EPSPZX(NEL),
     .   EPSXX(NEL) ,EPSYY(NEL) ,EPSXY(NEL) ,EPSYZ(NEL) ,EPSZX(NEL),
     .   BIDON3  ,BIDON4  ,BIDON5    
C-----------------------------------------------
C   O U T P U T   A r g u m e n t s
C-----------------------------------------------
c      my_real
c    
C-----------------------------------------------
C   I N P U T   O U T P U T   A r g u m e n t s 
C-----------------------------------------------
      my_real UVAR(NEL,NUVAR), OFF(NEL),
     .    SIGNXX(NEL),SIGNYY(NEL),UEL(NEL),
     .    SIGNXY(NEL),SIGNYZ(NEL),SIGNZX(NEL)

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
     .    JCT(MVSIZ),IR,IFAIL,JJ
      my_real EPSMAX(MVSIZ)

      my_real  ZERO,UN,QCINQ
C-----------------------------------------------
      ZERO=0.0
      UN=1.0
      QCINQ=4./5.
C-----------------------------------------------
C    Ex : deletion d'element sur criter epsmax
C-----------------------------------------------
      IR = 0
      DO I=1,NEL
       IFAIL  = IPM(111,MAT(I))
       IF(IFAIL.EQ.4) THEN 
        IR = IR + 1
        JCT(IR) = I
        IADBUF = IPM(114,MAT(I))  
        EPSMAX(I) = UPARAM(IADBUF)
        IFLAG(I)  = UPARAM(IADBUF + 1)
       ENDIF
      ENDDO
C-----------------------------------------------
C     USER VARIABLES INITIALIZATION
C-----------------------------------------------
      IF(TIME.EQ.ZERO)THEN
        DO JJ=1,IR
        I = JCT(JJ)
        UEL(I) = ZERO
         DO J=1,NUVAR
           UVAR(I,1)=ZERO
         ENDDO
        ENDDO 
      ENDIF
C----------------------------------------------- 
      IDEL=0
      IDEV=0
      DO J=1,IR
       I = JCT(J)
       IF(IFLAG(I).EQ.1)THEN
        IDEL=1
       ELSEIF(IFLAG(I).EQ.2)THEN
        IDEV =1
       END IF
      END DO
C...
      IF(IDEL.EQ.1)THEN
       NINDX=0  
       DO J =1,IR
        I = JCT(J)
        IF(IFLAG(I).EQ.1.AND.OFF(I).EQ.UN)THEN               
         IF(PLA(I).GE.EPSMAX(I)) THEN
          OFF(I)=QCINQ
          NINDX=NINDX+1
          INDX(NINDX)=I                 
         ENDIF
        ENDIF 
       ENDDO      
      ENDIF
Cc tensor set a zero   
      IF(IDEV.EQ.1)THEN
       NINDX=0  
       DO J =1,IR
        I= JCT(J)
        IF(IFLAG(I).EQ.2.AND.OFF(I).EQ.UN)THEN
         IF(PLA(I).GE.EPSMAX(I))THEN 
           SIGNXX(I) = ZERO
           SIGNYY(I) = ZERO
           SIGNXY(I) = ZERO
           SIGNYZ(I) = ZERO
           SIGNZX(I) = ZERO
           UEL(I) = UEL(I) + 1
           IF(INT(UEL(I)).EQ.NPT0) OFF(I) = QCINQ      
         ENDIF
        ENDIF  
       ENDDO
c       IF(NINDX.GT.0)THEN
c        DO J=1,NINDX
c#include "lockon.inc"
c         WRITE(IOUT, 2000) IPT,NGL(I)
c         WRITE(ISTDO,2100) IPT, NGL(I),TIME
c#include "lockoff.inc" 
c        END DO
c       END IF         
      ENDIF      
C------------------
c 2000 FORMAT(1X,' TENSOR STRESS OFF LAYER NUMBER',I10,
c     .'FOR ELEMENT SHELL NUMBER',I10,1X, 'SET TO ZERO')
c 2100 FORMAT(1X,' TENSOR STRESS OFF LAYER NUMBER',I10,
c     .'FOR ELEMENT SHELL NUMBER',I10,1X,'SET TO ZERO ',
c     .          ' AT TIME :',1PE20.13)
      RETURN
      END
