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
Chd|  SIGEPS99                      src/user/sigeps99.F           
Chd|-- called by -----------
Chd|        MULAW                         src/matera/mulaw.F            
Chd|-- calls ---------------
Chd|        LUSER01                       pub/userso/luser01.F          
Chd|        LUSER02                       pub/userso/luser02.F          
Chd|        LUSER03                       pub/userso/luser03.F          
Chd|        LUSER04                       pub/userso/luser04.F          
Chd|        LUSER05                       pub/userso/luser05.F          
Chd|        LUSER06                       pub/userso/luser06.F          
Chd|        LUSER07                       pub/userso/luser07.F          
Chd|        LUSER08                       pub/userso/luser08.F          
Chd|        LUSER09                       pub/userso/luser09.F          
Chd|        LUSER10                       pub/userso/luser10.F          
Chd|        LUSER11                       pub/userso/luser11.F          
Chd|        LUSER12                       pub/userso/luser12.F          
Chd|        LUSER13                       pub/userso/luser13.F          
Chd|        LUSER14                       pub/userso/luser14.F          
Chd|        LUSER15                       pub/userso/luser15.F          
Chd|        LUSER16                       pub/userso/luser16.F          
Chd|        LUSER17                       pub/userso/luser17.F          
Chd|        LUSER18                       pub/userso/luser18.F          
Chd|        LUSER19                       pub/userso/luser19.F          
Chd|        LUSER20                       pub/userso/luser20.F          
Chd|        LUSER21                       pub/userso/luser21.F          
Chd|        LUSER22                       pub/userso/luser22.F          
Chd|        LUSER23                       pub/userso/luser23.F          
Chd|        LUSER24                       pub/userso/luser24.F          
Chd|        LUSER25                       pub/userso/luser25.F          
Chd|        LUSER26                       pub/userso/luser26.F          
Chd|        LUSER27                       pub/userso/luser27.F          
Chd|        LUSER28                       pub/userso/luser28.F          
Chd|        LUSER29                       pub/userso/luser29.F          
Chd|        LUSER30                       pub/userso/luser30.F          
Chd|        LUSER31                       pub/userso/luser31.F          
Chd|        LUSER32                       pub/userso/luser32.F          
Chd|        LUSER33                       pub/userso/luser33.F          
Chd|        LUSER34                       pub/userso/luser34.F          
Chd|        LUSER35                       pub/userso/luser35.F          
Chd|        LUSER36                       pub/userso/luser36.F          
Chd|        LUSER37                       pub/userso/luser37.F          
Chd|        LUSER38                       pub/userso/luser38.F          
Chd|        LUSER39                       pub/userso/luser39.F          
Chd|        LUSER40                       pub/userso/luser40.F          
Chd|        LUSER41                       pub/userso/luser41.F          
Chd|        LUSER42                       pub/userso/luser42.F          
Chd|        LUSER43                       pub/userso/luser43.F          
Chd|        LUSER44                       pub/userso/luser44.F          
Chd|        LUSER45                       pub/userso/luser45.F          
Chd|        LUSER46                       pub/userso/luser46.F          
Chd|        LUSER47                       pub/userso/luser47.F          
Chd|        LUSER48                       pub/userso/luser48.F          
Chd|        LUSER49                       pub/userso/luser49.F          
Chd|        LUSER50                       pub/userso/luser50.F          
Chd|        LUSER51                       pub/userso/luser51.F          
Chd|        LUSER52                       pub/userso/luser52.F          
Chd|        LUSER53                       pub/userso/luser53.F          
Chd|        LUSER54                       pub/userso/luser54.F          
Chd|        LUSER55                       pub/userso/luser55.F          
Chd|        LUSER56                       pub/userso/luser56.F          
Chd|        LUSER57                       pub/userso/luser57.F          
Chd|        LUSER58                       pub/userso/luser58.F          
Chd|        LUSER59                       pub/userso/luser59.F          
Chd|        LUSER60                       pub/userso/luser60.F          
Chd|        LUSER61                       pub/userso/luser61.F          
Chd|        LUSER62                       pub/userso/luser62.F          
Chd|        LUSER63                       pub/userso/luser63.F          
Chd|        LUSER64                       pub/userso/luser64.F          
Chd|        LUSER65                       pub/userso/luser65.F          
Chd|        LUSER66                       pub/userso/luser66.F          
Chd|        LUSER67                       pub/userso/luser67.F          
Chd|        LUSER68                       pub/userso/luser68.F          
Chd|        LUSER69                       pub/userso/luser69.F          
Chd|        LUSER70                       pub/userso/luser70.F          
Chd|        LUSER71                       pub/userso/luser71.F          
Chd|        LUSER72                       pub/userso/luser72.F          
Chd|        LUSER73                       pub/userso/luser73.F          
Chd|        LUSER74                       pub/userso/luser74.F          
Chd|        LUSER75                       pub/userso/luser75.F          
Chd|        LUSER76                       pub/userso/luser76.F          
Chd|        LUSER77                       pub/userso/luser77.F          
Chd|        LUSER78                       pub/userso/luser78.F          
Chd|        LUSER79                       pub/userso/luser79.F          
Chd|        LUSER80                       pub/userso/luser80.F          
Chd|        LUSER81                       pub/userso/luser81.F          
Chd|        LUSER82                       pub/userso/luser82.F          
Chd|        LUSER83                       pub/userso/luser83.F          
Chd|        LUSER84                       pub/userso/luser84.F          
Chd|        LUSER85                       pub/userso/luser85.F          
Chd|        LUSER86                       pub/userso/luser86.F          
Chd|        LUSER87                       pub/userso/luser87.F          
Chd|        LUSER88                       pub/userso/luser88.F          
Chd|        LUSER89                       pub/userso/luser89.F          
Chd|        LUSER90                       pub/userso/luser90.F          
Chd|        LUSER91                       pub/userso/luser91.F          
Chd|        LUSER92                       pub/userso/luser92.F          
Chd|        LUSER93                       pub/userso/luser93.F          
Chd|        LUSER94                       pub/userso/luser94.F          
Chd|        LUSER95                       pub/userso/luser95.F          
Chd|        LUSER96                       pub/userso/luser96.F          
Chd|        LUSER97                       pub/userso/luser97.F          
Chd|        LUSER98                       pub/userso/luser98.F          
Chd|        LUSER99                       pub/userso/luser99.F          
Chd|        LAW_USERSO                    src/usermodules/law_userso.F  
Chd|====================================================================
      SUBROUTINE ENG_SIGEPS99 (
     1     NEL    ,NUPARAM ,NUVAR  ,ILAW_USER  ,NFUNC   ,
     2     IFUNC  ,NPF     ,TF     ,TIME       ,TIMESTEP,
     3     UPARAM ,RHO     ,VOLUME ,EINT       ,NGL    ,
     4     SOUNDSP,VISCMAX ,UVAR   ,OFF        ,SIGY   ,
     5     PLA   )

#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_SIGEPS99" :: ENG_SIGEPS99
!DEC$ ATTRIBUTES REFERENCE ::    NEL    ,NUPARAM ,NUVAR  ,ILAW_USER  ,NFUNC   ,
     2     IFUNC  ,NPF     ,TF     ,TIME       ,TIMESTEP,
     3     UPARAM ,RHO     ,VOLUME ,EINT       ,NGL    ,
     4     SOUNDSP,VISCMAX ,UVAR   ,OFF        ,SIGY   ,
     5     PLA 
#endif
C -----------------------------------------------------------------

        USE LAW_USERSO_VAR
#include "implicit_f.inc"
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
C TF      |  *      | F | R | FUNCTION ARRAY 
C---------+---------+---+---+--------------------------------------------
C TIME    |  1      | F | R | CURRENT TIME
C TIMESTEP|  1      | F | R | CURRENT TIME STEP
C UPARAM  | NUPARAM | F | R | USER MATERIAL PARAMETER ARRAY
C RHO0    | NEL     | F | R | INITIAL DENSITY
C RHO     | NEL     | F | R | DENSITY
C VOLUME  | NEL     | F | R | VOLUME
C EINT    | NEL     | F | R | TOTAL INTERNAL ENERGY
C---------+---------+---+---+--------------------------------------------
C UVAR    |NEL*NUVAR| F |R/W| USER ELEMENT VARIABLE ARRAY
C OFF     | NEL     | F |R/W| DELETED ELEMENT FLAG (=1. ON, =0. OFF)
C---------+---------+---+---+--------------------------------------------
C-----------------------------------------------
C   I N P U T   A r g u m e n t s
C-----------------------------------------------
      INTEGER NEL, NUPARAM, NUVAR,NGL(NEL),ILAW_USER
      my_real
     .   TIME,TIMESTEP,UPARAM(NUPARAM),
     .   RHO(NEL),VOLUME(NEL),EINT(NEL)
C-----------------------------------------------
C   O U T P U T   A r g u m e n t s
C-----------------------------------------------
      my_real
     .    SOUNDSP(NEL),VISCMAX(NEL)
C-----------------------------------------------
C   I N P U T   O U T P U T   A r g u m e n t s 
C-----------------------------------------------
      my_real
     .  UVAR(NEL,NUVAR), OFF(NEL),PLA(NEL), SIGY(NEL) ,RHO0(NEL)
C-----------------------------------------------
C   VARIABLES FOR FUNCTION INTERPOLATION 
C-----------------------------------------------
      INTEGER NPF(*), NFUNC, IFUNC(NFUNC),ITASK,
     .   GET_U_TASK
      my_real
     .  FINTER ,TF(*)
      EXTERNAL FINTER,GET_U_TASK
C        Y = FINTER(IFUNC(J),X,NPF,TF,DYDX)
C        Y       : y = f(x)
C        X       : x
C        DYDX    : f'(x) = dy/dx
C        IFUNC(J): FUNCTION INDEX
C              J : FIRST(J=1), SECOND(J=2) .. FUNCTION USED FOR THIS LAW
C        NPF,TF  : FUNCTION PARAMETER
C-----------------------------------------------        
         ITASK=MAX(GET_U_TASK(),1)
C
         IF(ILAW_USER == 1) THEN
           CALL LUSER01(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 2) THEN
           CALL LUSER02(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 3) THEN
           CALL LUSER03(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 4) THEN
           CALL LUSER04(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 5) THEN
           CALL LUSER05(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 6) THEN
           CALL LUSER06(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 7) THEN
           CALL LUSER07(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 8) THEN
           CALL LUSER08(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 9) THEN
           CALL LUSER09(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 10) THEn
           CALL LUSER10(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 11) THEN
           CALL LUSER11(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 12) THEN
           CALL LUSER12(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 13) THEN
           CALL LUSER13(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 14) THEN
           CALL LUSER14(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 15) THEN
           CALL LUSER15(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 16) THEN
           CALL LUSER16(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 17) THEN
           CALL LUSER17(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 18) THEN
           CALL LUSER18(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 19) THEN
           CALL LUSER19(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 20) THEN
           CALL LUSER20(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 21) THEn
           CALL LUSER21(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 22) THEN
           CALL LUSER22(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 23) THEN
           CALL LUSER23(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 24) THEN
           CALL LUSER24(
     1        NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2        TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO0    ,RHO    ,
     3        VOLUME ,EINT   ,NGL ,
     4        SOUNDSP,VISCMAX,UVAR    ,OFF     ,SIGY  , PLA)
         ELSEIF(ILAW_USER == 25) THEN
           CALL LUSER25(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 26) THEN
           CALL LUSER26(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 27) THEN
           CALL LUSER27(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 28) THEN
           CALL LUSER28(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 29) THEN
           CALL LUSER29(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 30) THEn
           CALL LUSER30(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 31) THEN
           CALL LUSER31(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 32) THEN
           CALL LUSER32(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 33) THEN
           CALL LUSER33(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 34) THEN
           CALL LUSER34(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 35) THEN
           CALL LUSER35(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 36) THEN
           CALL LUSER36(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 37) THEN
           CALL LUSER37(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 38) THEN
           CALL LUSER38(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 39) THEN
           CALL LUSER39(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 40) THEN
           CALL LUSER40(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 41) THEN
           CALL LUSER41(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 42) THEN
           CALL LUSER42(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 43) THEN
           CALL LUSER43(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 44) THEN
           CALL LUSER44(
     1        NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2        TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO0    ,RHO    ,
     3        VOLUME ,EINT   ,NGL ,
     4        SOUNDSP,VISCMAX,UVAR    ,OFF     ,SIGY  , PLA)
         ELSEIF(ILAW_USER == 45) THEN
           CALL LUSER45(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 46) THEN
           CALL LUSER46(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 47) THEN
           CALL LUSER47(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 48) THEN
           CALL LUSER48(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 49) THEN
           CALL LUSER49(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 50) THEN
           CALL LUSER50(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 51) THEn
           CALL LUSER51(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 52) THEN
           CALL LUSER52(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 53) THEN
           CALL LUSER53(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 54) THEN
           CALL LUSER54(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 55) THEN
           CALL LUSER55(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 56) THEN
           CALL LUSER56(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 57) THEN
           CALL LUSER57(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 58) THEN
           CALL LUSER58(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 59) THEN
           CALL LUSER59(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 60) THEn
           CALL LUSER60(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 61) THEN
           CALL LUSER61(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 62) THEN
           CALL LUSER62(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 63) THEN
           CALL LUSER63(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 64) THEN
           CALL LUSER64(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 65) THEN
           CALL LUSER65(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 66) THEN
           CALL LUSER66(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 67) THEN
           CALL LUSER67(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 68) THEN
           CALL LUSER68(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 69) THEN
           CALL LUSER69(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 70) THEN
           CALL LUSER70(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 71) THEN
           CALL LUSER71(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 72) THEN
           CALL LUSER72(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 73) THEN
           CALL LUSER73(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 74) THEN
           CALL LUSER74(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 75) THEN
           CALL LUSER75(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 76) THEN
           CALL LUSER76(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 77) THEN
           CALL LUSER77(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 78) THEN
           CALL LUSER78(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 79) THEN
           CALL LUSER79(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 80) THEN
           CALL LUSER80(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 81) THEN
           CALL LUSER81(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 82) THEN
           CALL LUSER82(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 83) THEN
           CALL LUSER83(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 84) THEN
           CALL LUSER84(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 85) THEN
           CALL LUSER85(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 86) THEN
           CALL LUSER86(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 87) THEN
           CALL LUSER87(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 88) THEN
           CALL LUSER88(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 89) THEN
           CALL LUSER89(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 90) THEN
           CALL LUSER90(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 91) THEN
           CALL LUSER91(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 92) THEN
           CALL LUSER92(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 93) THEN
           CALL LUSER93(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 94) THEN
           CALL LUSER94(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 95) THEN
           CALL LUSER95(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 96) THEN
           CALL LUSER96(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 97) THEN
           CALL LUSER97(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 98) THEN
           CALL LUSER98(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ELSEIF(ILAW_USER == 99) THEN
           CALL LUSER99(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY  , PLA , ULAWVAR_ARRAY(ITASK))
         ENDIF
C         
      RETURN
      END
