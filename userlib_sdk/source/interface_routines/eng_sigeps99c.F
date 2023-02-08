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


Csm51i6 nouvelle lois utilisateurs.
Chd|====================================================================
Chd|  SIGEPS99C                     src/user/sigeps99c.F          
Chd|-- called by -----------
Chd|        MULAWC                        src/coque/mulawc.F            
Chd|-- calls ---------------
Chd|        LUSER01C                      pub/usersh/luser01c.F         
Chd|        LUSER02C                      pub/usersh/luser02c.F         
Chd|        LUSER03C                      pub/usersh/luser03c.F         
Chd|        LUSER04C                      pub/usersh/luser04c.F         
Chd|        LUSER05C                      pub/usersh/luser05c.F         
Chd|        LUSER06C                      pub/usersh/luser06c.F         
Chd|        LUSER07C                      pub/usersh/luser07c.F         
Chd|        LUSER08C                      pub/usersh/luser08c.F         
Chd|        LUSER09C                      pub/usersh/luser09c.F         
Chd|        LUSER10C                      pub/usersh/luser10c.F         
Chd|        LUSER11C                      pub/usersh/luser11c.F         
Chd|        LUSER12C                      pub/usersh/luser12c.F         
Chd|        LUSER13C                      pub/usersh/luser13c.F         
Chd|        LUSER14C                      pub/usersh/luser14c.F         
Chd|        LUSER15C                      pub/usersh/luser15c.F         
Chd|        LUSER16C                      pub/usersh/luser16c.F         
Chd|        LUSER17C                      pub/usersh/luser17c.F         
Chd|        LUSER18C                      pub/usersh/luser18c.F         
Chd|        LUSER19C                      pub/usersh/luser19c.F         
Chd|        LUSER20C                      pub/usersh/luser20c.F         
Chd|        LUSER21C                      pub/usersh/luser21c.F         
Chd|        LUSER22C                      pub/usersh/luser22c.F         
Chd|        LUSER23C                      pub/usersh/luser23c.F         
Chd|        LUSER24C                      pub/usersh/luser24c.F         
Chd|        LUSER25C                      pub/usersh/luser25c.F         
Chd|        LUSER26C                      pub/usersh/luser26c.F         
Chd|        LUSER27C                      pub/usersh/luser27c.F         
Chd|        LUSER28C                      pub/usersh/luser28c.F         
Chd|        LUSER29C                      pub/usersh/luser29c.F         
Chd|        LUSER30C                      pub/usersh/luser30c.F         
Chd|        LUSER31C                      pub/usersh/luser31c.F         
Chd|        LUSER32C                      pub/usersh/luser32c.F         
Chd|        LUSER33C                      pub/usersh/luser33c.F         
Chd|        LUSER34C                      pub/usersh/luser34c.F         
Chd|        LUSER35C                      pub/usersh/luser35c.F         
Chd|        LUSER36C                      pub/usersh/luser36c.F         
Chd|        LUSER37C                      pub/usersh/luser37c.F         
Chd|        LUSER38C                      pub/usersh/luser38c.F         
Chd|        LUSER39C                      pub/usersh/luser39c.F         
Chd|        LUSER40C                      pub/usersh/luser40c.F         
Chd|        LUSER41C                      pub/usersh/luser41c.F         
Chd|        LUSER42C                      pub/usersh/luser42c.F         
Chd|        LUSER43C                      pub/usersh/luser43c.F         
Chd|        LUSER44C                      pub/usersh/luser44c.F         
Chd|        LUSER45C                      pub/usersh/luser45c.F         
Chd|        LUSER46C                      pub/usersh/luser46c.F         
Chd|        LUSER47C                      pub/usersh/luser47c.F         
Chd|        LUSER48C                      pub/usersh/luser48c.F         
Chd|        LUSER49C                      pub/usersh/luser49c.F         
Chd|        LUSER50C                      pub/usersh/luser50c.F         
Chd|        LUSER51C                      pub/usersh/luser51c.F         
Chd|        LUSER52C                      pub/usersh/luser52c.F         
Chd|        LUSER53C                      pub/usersh/luser53c.F         
Chd|        LUSER54C                      pub/usersh/luser54c.F         
Chd|        LUSER55C                      pub/usersh/luser55c.F         
Chd|        LUSER56C                      pub/usersh/luser56c.F         
Chd|        LUSER57C                      pub/usersh/luser57c.F         
Chd|        LUSER58C                      pub/usersh/luser58c.F         
Chd|        LUSER59C                      pub/usersh/luser59c.F         
Chd|        LUSER60C                      pub/usersh/luser60c.F         
Chd|        LUSER61C                      pub/usersh/luser61c.F         
Chd|        LUSER62C                      pub/usersh/luser62c.F         
Chd|        LUSER63C                      pub/usersh/luser63c.F         
Chd|        LUSER64C                      pub/usersh/luser64c.F         
Chd|        LUSER65C                      pub/usersh/luser65c.F         
Chd|        LUSER66C                      pub/usersh/luser66c.F         
Chd|        LUSER67C                      pub/usersh/luser67c.F         
Chd|        LUSER68C                      pub/usersh/luser68c.F         
Chd|        LUSER69C                      pub/usersh/luser69c.F         
Chd|        LUSER70C                      pub/usersh/luser70c.F         
Chd|        LUSER71C                      pub/usersh/luser71c.F         
Chd|        LUSER72C                      pub/usersh/luser72c.F         
Chd|        LUSER73C                      pub/usersh/luser73c.F         
Chd|        LUSER74C                      pub/usersh/luser74c.F         
Chd|        LUSER75C                      pub/usersh/luser75c.F         
Chd|        LUSER76C                      pub/usersh/luser76c.F         
Chd|        LUSER77C                      pub/usersh/luser77c.F         
Chd|        LUSER78C                      pub/usersh/luser78c.F         
Chd|        LUSER79C                      pub/usersh/luser79c.F         
Chd|        LUSER80C                      pub/usersh/luser80c.F         
Chd|        LUSER81C                      pub/usersh/luser81c.F         
Chd|        LUSER82C                      pub/usersh/luser82c.F         
Chd|        LUSER83C                      pub/usersh/luser83c.F         
Chd|        LUSER84C                      pub/usersh/luser84c.F         
Chd|        LUSER85C                      pub/usersh/luser85c.F         
Chd|        LUSER86C                      pub/usersh/luser86c.F         
Chd|        LUSER87C                      pub/usersh/luser87c.F         
Chd|        LUSER88C                      pub/usersh/luser88c.F         
Chd|        LUSER89C                      pub/usersh/luser89c.F         
Chd|        LUSER90C                      pub/usersh/luser90c.F         
Chd|        LUSER91C                      pub/usersh/luser91c.F         
Chd|        LUSER92C                      pub/usersh/luser92c.F         
Chd|        LUSER93C                      pub/usersh/luser93c.F         
Chd|        LUSER94C                      pub/usersh/luser94c.F         
Chd|        LUSER95C                      pub/usersh/luser95c.F         
Chd|        LUSER96C                      pub/usersh/luser96c.F         
Chd|        LUSER97C                      pub/usersh/luser97c.F         
Chd|        LUSER98C                      pub/usersh/luser98c.F         
Chd|        LUSER99C                      pub/usersh/luser99c.F         
Chd|        LAW_USERSH                    src/usermodules/law_usersh.F  
Chd|====================================================================
      SUBROUTINE ENG_SIGEPS99C(
     1     NEL      ,NUPARAM ,NUVAR   ,ILAW_USER ,NFUNC  ,
     3     IFUNC    ,NPF     ,NGL    ,TF       ,TIME   ,
     3     TIMESTEP ,UPARAM  ,RHO    ,AREA      ,EINT   ,
     4     SHF      ,SOUNDSP ,VISCMAX ,PLA       ,UVAR   , 
     5     OFF      ,SIGY    )
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_SIGEPS99C" :: ENG_SIGEPS99C
!DEC$ ATTRIBUTES REFERENCE ::   NEL      ,NUPARAM ,NUVAR   ,ILAW_USER ,NFUNC  ,
     3     IFUNC    ,NPF     ,NGL    ,TF       ,TIME   ,
     3     TIMESTEP ,UPARAM  ,RHO    ,AREA      ,EINT   ,
     4     SHF      ,SOUNDSP ,VISCMAX ,PLA       ,UVAR   , 
     5     OFF      ,SIGY    
#endif
C ----------------------------------------
      USE LAW_USERSH_VAR
#include "implicit_f.inc"
C --------------------------------------------
      INTEGER  NEL,NUVAR,NUPARAM,NGL(NEL),ILAW_USER
      my_real
     .   TIME,PLA(NEL), UVAR(NUVAR,NEL),UPARAM(NUPARAM),
     .   TIMESTEP(NEL), AREA(NEL),OFF(NEL),VISCMAX(NEL),
     .   EINT(2,NEL), SHF(NEL), SOUNDSP(NEL),RHO(NEL),
     .   SIGY(NEL)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER ITASK,GET_U_TASK
C-----------------------------------------------
C     USER VARIABLES INITIALIZATION
C----------------------------------------------- 
C-----------------------------------------------
C   VARIABLES FOR FUNCTION INTERPOLATION 
C-----------------------------------------------
      INTEGER NFUNC, IFUNC(NFUNC),NPF(*)
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
C     USER VARIABLES INITIALIZATION
C-----------------------------------------------        
         ITASK=MAX(GET_U_TASK(),1)
         
      IF(ILAW_USER == 1) THEN
        CALL LUSER01C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 2) THEN
        CALL LUSER02C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 3) THEN
        CALL LUSER03C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 4) THEN
        CALL LUSER04C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 5) THEN
        CALL LUSER05C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 6) THEN
        CALL LUSER06C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 7) THEN
        CALL LUSER07C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 8) THEN
        CALL LUSER08C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 9) THEN
        CALL LUSER09C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 10) THEN
        CALL LUSER10C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 11) THEN
        CALL LUSER11C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 12) THEN
        CALL LUSER12C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 13) THEN
        CALL LUSER13C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 14) THEN
        CALL LUSER14C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 15) THEN
        CALL LUSER15C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 16) THEN
        CALL LUSER16C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 17) THEN
        CALL LUSER17C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 18) THEN
        CALL LUSER18C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 19) THEN
        CALL LUSER19C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 20) THEN
        CALL LUSER20C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 21) THEn
        CALL LUSER21C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 22) THEN
        CALL LUSER22C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 23) THEN
        CALL LUSER23C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 24) THEN
        CALL LUSER24C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 25) THEN
        CALL LUSER25C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 26) THEN
        CALL LUSER26C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 27) THEN
        CALL LUSER27C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 28) THEN
        CALL LUSER28C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 29) THEN
        CALL LUSER29C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 30) THEn
        CALL LUSER30C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 31) THEN
        CALL LUSER31C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 32) THEN
        CALL LUSER32C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 33) THEN
        CALL LUSER33C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 34) THEN
        CALL LUSER34C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 35) THEN
        CALL LUSER35C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 36) THEN
        CALL LUSER36C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 37) THEN
        CALL LUSER37C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 38) THEN
        CALL LUSER38C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 39) THEN
        CALL LUSER39C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 40) THEN
        CALL LUSER40C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 41) THEN
        CALL LUSER41C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 42) THEN
        CALL LUSER42C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 43) THEN
        CALL LUSER43C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 44) THEN
        CALL LUSER44C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 45) THEN
        CALL LUSER45C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 46) THEN
        CALL LUSER46C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 47) THEN
        CALL LUSER47C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 48) THEN
        CALL LUSER48C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 49) THEN
        CALL LUSER49C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 50) THEN
        CALL LUSER50C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 51) THEn
        CALL LUSER51C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 52) THEN
        CALL LUSER52C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 53) THEN
        CALL LUSER53C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 54) THEN
        CALL LUSER54C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 55) THEN
        CALL LUSER55C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 56) THEN
        CALL LUSER56C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 57) THEN
        CALL LUSER57C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 58) THEN
        CALL LUSER58C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 59) THEN
        CALL LUSER59C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 60) THEn
        CALL LUSER60C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 61) THEN
        CALL LUSER61C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 62) THEN
        CALL LUSER62C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 63) THEN
        CALL LUSER63C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 64) THEN
        CALL LUSER64C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 65) THEN
        CALL LUSER65C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 66) THEN
        CALL LUSER66C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 67) THEN
        CALL LUSER67C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 68) THEN
        CALL LUSER68C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 69) THEN
        CALL LUSER69C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 70) THEN
        CALL LUSER70C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 71) THEN
        CALL LUSER71C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 72) THEN
        CALL LUSER72C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 73) THEN
        CALL LUSER73C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 74) THEN
        CALL LUSER74C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 75) THEN
        CALL LUSER75C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 76) THEN
        CALL LUSER76C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 77) THEN
        CALL LUSER77C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 78) THEN
        CALL LUSER78C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 79) THEN
        CALL LUSER79C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 80) THEN
        CALL LUSER80C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 81) THEN
        CALL LUSER81C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 82) THEN
        CALL LUSER82C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 83) THEN
        CALL LUSER83C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 84) THEN
        CALL LUSER84C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 85) THEN
        CALL LUSER85C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 86) THEN
        CALL LUSER86C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 87) THEN
        CALL LUSER87C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 88) THEN
        CALL LUSER88C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 89) THEN
        CALL LUSER89C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 90) THEN
        CALL LUSER90C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 91) THEN
        CALL LUSER91C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 92) THEN
        CALL LUSER92C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 93) THEN
        CALL LUSER93C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 94) THEN
        CALL LUSER94C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 95) THEN
        CALL LUSER95C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 96) THEN
        CALL LUSER96C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 97) THEN
        CALL LUSER97C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 98) THEN
        CALL LUSER98C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    , NGL   , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO   ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   , OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ELSEIF(ILAW_USER == 99) THEN
        CALL LUSER99C(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC  ,IFUNC    ,
     2     NPF    ,NGL    , TF     ,TIME   ,TIMESTEP ,
     3     UPARAM ,RHO    ,AREA    ,EINT   ,SHF      ,
     4     SOUNDSP,VISCMAX ,PLA    ,UVAR   ,OFF     ,
     5     SIGY   ,ULAWCVAR_ARRAY(ITASK))
      ENDIF
      RETURN
      END
