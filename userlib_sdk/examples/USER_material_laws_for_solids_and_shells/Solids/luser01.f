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
C     This subroutine computes elastic stresses. 
C================================================================= 
      SUBROUTINE LUSER01 ( 
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    , 
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME , 
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     , 
     4     SIGY   ,PLA    ,USERBUF) 
C ----------------------------------------------------------------- 
      USE LAW_USERSO 
C 
C    INPUT DATA 
C 
      INTEGER NEL, NUPARAM, NUVAR,NGL(NEL) 
      DOUBLE PRECISION 
     .   TIME,TIMESTEP,UPARAM(NUPARAM), 
     .   RHO(NEL),VOLUME(NEL),EINT(NEL),      
     .   EPSPXX(NEL),EPSPYY(NEL),EPSPZZ(NEL), 
     .   EPSPXY(NEL),EPSPYZ(NEL),EPSPZX(NEL), 
     .   DEPSXX(NEL),DEPSYY(NEL),DEPSZZ(NEL), 
     .   DEPSXY(NEL),DEPSYZ(NEL),DEPSZX(NEL), 
     .   EPSXX(NEL) ,EPSYY(NEL) ,EPSZZ(NEL), 
     .   EPSXY(NEL) ,EPSYZ(NEL) ,EPSZX(NEL), 
     .   SIGOXX(NEL),SIGOYY(NEL),SIGOZZ(NEL), 
     .   SIGOXY(NEL),SIGOYZ(NEL),SIGOZX(NEL), 
     .   RHO0(NEL) 
C----------------------------------------------- 
C   O U T P U T   DATA 
C----------------------------------------------- 
      DOUBLE PRECISION 
     .    SOUNDSP(NEL),VISCMAX(NEL),   
     .    SIGNXX(NEL),SIGNYY(NEL),SIGNZZ(NEL), 
     .    SIGNXY(NEL),SIGNYZ(NEL),SIGNZX(NEL), 
     .    SIGVXX(NEL),SIGVYY(NEL),SIGVZZ(NEL), 
     .    SIGVXY(NEL),SIGVYZ(NEL),SIGVZX(NEL), 
     .    DPLA(NEL),TEMP(NEL) 
C----------------------------------------------- 
C   I N P U T   O U T P U T   A r g u m e n ts 
C----------------------------------------------- 
      DOUBLE PRECISION 
     .  UVAR(NEL,NUVAR), OFF(NEL),PLA(NEL), SIGY(NEL) 
C----------------------------------------------- 
      TYPE(ULAWINTBUF) :: USERBUF  
C----------------------------------------------- 
      INTEGER NPF(*), NFUNC, IFUNC(NFUNC),GET_U_CYCLE 
      DOUBLE PRECISION  FINTER ,TF(*) , DYDX
      EXTERNAL FINTER , WRITE_IOUT,GET_U_CYCLE
C        Y = FINTER(IFUNC(J),X,NPF,TF,DYDX) 
C        Y       : y = f(x) 
C        X       : x 
C        DYDX    : f’(x) = dy/dx 
C        IFUNC(J): FUNCTION INDEX 
C              J : FIRST(J=1), SECOND(J=2) .. FUNCTION USED FOR THIS LAW 
C        NPF,TF  : FUNCTION PARAMETER 
C ----------------------------------------------- 
C----------------------------------------------- 
C   L o c a l   V a r i a b l e s 
C----------------------------------------------- 
      INTEGER I,J,LEN,CYCL,DEBUG
      DOUBLE PRECISION  
     .   A11(NEL),A12(NEL),G(NEL) , E(NEL),NU

      CHARACTER*256 LINE
        
     
C----------------------------------------------- 
C     USER VARIABLES INITIALIZATION 
C----------------------------------------------- 
        CYCL      = GET_U_CYCLE()
        
C     Input Data structure 
      SIGOXX(1:NEL) = USERBUF%SIGOXX(1:NEL) 
      SIGOYY(1:NEL) = USERBUF%SIGOYY(1:NEL) 
      SIGOZZ(1:NEL) = USERBUF%SIGOZZ(1:NEL) 
      SIGOXY(1:NEL) = USERBUF%SIGOXY(1:NEL)  
      SIGOYZ(1:NEL) = USERBUF%SIGOYZ(1:NEL)  
      SIGOZX(1:NEL) = USERBUF%SIGOZX(1:NEL) 
C        
      EPSPXX(1:NEL) = USERBUF%EPSPXX(1:NEL)       
      EPSPYY(1:NEL) = USERBUF%EPSPYY(1:NEL)  
      EPSPZZ(1:NEL) = USERBUF%EPSPZZ(1:NEL)     
      EPSPXY(1:NEL) = USERBUF%EPSPXY(1:NEL)     
      EPSPYZ(1:NEL) = USERBUF%EPSPYZ(1:NEL)     
      EPSPZX(1:NEL) = USERBUF%EPSPZX(1:NEL)  
C        
      EPSXX(1:NEL) = USERBUF%EPSXX(1:NEL)     
      EPSYY(1:NEL) = USERBUF%EPSYY(1:NEL)  
      EPSZZ(1:NEL) = USERBUF%EPSZZ(1:NEL)   
      EPSXY(1:NEL) = USERBUF%EPSXY(1:NEL)     
      EPSYZ(1:NEL) = USERBUF%EPSYZ(1:NEL)     
      EPSZX(1:NEL) = USERBUF%EPSZX(1:NEL) 
C        
      DEPSXX(1:NEL) = USERBUF%DEPSXX(1:NEL)     
      DEPSYY(1:NEL) = USERBUF%DEPSYY(1:NEL)  
      DEPSZZ(1:NEL) = USERBUF%DEPSZZ(1:NEL)    
      DEPSXY(1:NEL) = USERBUF%DEPSXY(1:NEL)     
      DEPSYZ(1:NEL) = USERBUF%DEPSYZ(1:NEL)     
      DEPSZX(1:NEL) = USERBUF%DEPSZX(1:NEL)  
C               
      SIGNXX(1:NEL) = USERBUF%SIGNXX(1:NEL)     
      SIGNYY(1:NEL) = USERBUF%SIGNYY(1:NEL) 
      SIGNZZ(1:NEL) = USERBUF%SIGNZZ(1:NEL) 
      SIGNXY(1:NEL) = USERBUF%SIGNXY(1:NEL)     
      SIGNYZ(1:NEL) = USERBUF%SIGNYZ(1:NEL)     
      SIGNZX(1:NEL) = USERBUF%SIGNZX(1:NEL)     
C 
      SIGVXX(1:NEL) = USERBUF%SIGVXX(1:NEL)     
      SIGVYY(1:NEL) = USERBUF%SIGVYY(1:NEL) 
      SIGVZZ(1:NEL) = USERBUF%SIGVZZ(1:NEL)   
      SIGVXY(1:NEL) = USERBUF%SIGVXY(1:NEL) 
      SIGVYZ(1:NEL) = USERBUF%SIGVYZ(1:NEL)     
      SIGVZX(1:NEL) = USERBUF%SIGVZX(1:NEL) 
      RHO0(1:NEL)   = USERBUF%RHO0(1:NEL) 
      DPLA(1:NEL)   = USERBUF%DPLA(1:NEL)  
C 
      TEMP(1:NEL)   = USERBUF%TEMP(1:NEL)
      
      NU            = UPARAM(4) 
      
      IF(NFUNC .EQ. 1)THEN
        DO I = 1,NEL
          E(I)      = FINTER(IFUNC(1),TEMP(I),NPF,TF,DYDX)
          A11(I)    = E(I) * (1.-NU) / (1.+NU) / (1.-2.*NU) 
          A12(I)    = E(I) * NU / (1.+NU) / (1.-2.*NU) 
          G(I)      = E(I) / 2. / (1.+NU) 
          UVAR(I,1) = E(I)
        ENDDO
      ELSE           
        A11(1:NEL)       = UPARAM(1) 
        A12(1:NEL)       = UPARAM(2) 
        G(1:NEL)         = UPARAM(3) 
      ENDIF  
      DEBUG = INT(UPARAM(4))
      IF (TIME.EQ.0.0) THEN
       DO I = 1,NEL 
        WRITE(LINE,'(A,I10)') "Entering material routine at time = 0.0 for El#",NGL(I)
        LEN = LEN_TRIM(LINE)             
        CALL WRITE_IOUT(LINE,LEN) 
        print *,'TIME = 0.0 element #',NGL(I)
       ENDDO
      ENDIF
       
C --- Trial stress 
C          
      DO I = 1,NEL 

      SIGNXX(I)=SIGOXX(I) + A11(I)*DEPSXX(I) + A12(I)*(DEPSYY(I) + DEPSZZ(I)) 
      SIGNYY(I)=SIGOYY(I) + A11(I)*DEPSYY(I) + A12(I)*(DEPSXX(I) + DEPSZZ(I)) 
      SIGNZZ(I)=SIGOZZ(I) + A11(I)*DEPSZZ(I) + A12(I)*(DEPSYY(I) + DEPSXX(I)) 
      SIGNXY(I)=SIGOXY(I) + G(I)*DEPSXY(I) 
      SIGNYZ(I)=SIGOYZ(I) + G(I)*DEPSYZ(I) 
      SIGNZX(I)=SIGOZX(I) + G(I)*DEPSZX(I) 
      PRINT *,' Element #',NGL(I),' hat SIGNXX  =',SIGNXX(I)
      PRINT *,' Element #',NGL(I),' hat SIGNYY=',SIGNYY(I)
      PRINT *,' Element #',NGL(I),' hat SIGNZZ=',SIGNZZ(I)
      PRINT *,' Element #',NGL(I),' hat SIGNXY=',SIGNXY(I)
      PRINT *,' Element #',NGL(I),' hat SIGNYZ=',SIGNYZ(I)
      PRINT *,' Element #',NGL(I),' hat SIGNZX=',SIGNZX(I)
      
c!      SIGNXX(I)= SIGNZZ / SIGNYY(I)
      
      IF(CYCL .GT. DEBUG)THEN
c!      IF((CYCL/10) == (REAL(CYCL)/10))THEN
       WRITE(LINE,'(A,I10,A,F8.3,A,I10)') " Element Nr. ",NGL(I)," STRESS SIGNZZ =",SIGNZZ(I)," Cycle =",CYCL
       LEN = LEN_TRIM(LINE)
       CALL WRITE_IOUT(LINE,LEN)
      ENDIF
      
C sound velocity  
      SOUNDSP(I) = SQRT(A11(I)/RHO0(I)) 
      VISCMAX(I) = ZERO     
      ENDDO  
      
C     Outp data structure 
      USERBUF%SIGNXX(1:NEL) = SIGNXX(1:NEL) 
      USERBUF%SIGNYY(1:NEL) = SIGNYY(1:NEL) 
      USERBUF%SIGNZZ(1:NEL) = SIGNZZ(1:NEL) 
      USERBUF%SIGNXY(1:NEL) = SIGNXY(1:NEL) 
      USERBUF%SIGNYZ(1:NEL) = SIGNYZ(1:NEL) 
      USERBUF%SIGNZX(1:NEL) = SIGNZX(1:NEL) 
C 
      USERBUF%SIGVXX(1:NEL) = SIGVXX(1:NEL) 
      USERBUF%SIGVYY(1:NEL) = SIGVYY(1:NEL) 
      USERBUF%SIGVZZ(1:NEL) = SIGVZZ(1:NEL) 
      USERBUF%SIGVXY(1:NEL) = SIGVXY(1:NEL) 
      USERBUF%SIGVYZ(1:NEL) = SIGVYZ(1:NEL) 
      USERBUF%SIGVZX(1:NEL) = SIGVZX(1:NEL)  
      USERBUF%DPLA(1:NEL)   =  DPLA(1:NEL)  
      RETURN
      END	  