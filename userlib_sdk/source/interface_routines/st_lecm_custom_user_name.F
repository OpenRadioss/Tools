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
Chd|  LECM99                        src/user1/lecm99.F            
Chd|-- called by -----------
Chd|        LECMUSER                      src/mater1/lecmuser.F         
Chd|-- calls ---------------
Chd|                                      src/usermodules1/law_user.F   
Chd|        LAW_USER                      src/usermodules1/law_user.F   
Chd|====================================================================
      SUBROUTINE ST_LECM_CUSTOM_USER_NAME(ILAW,ROOTN,ROOTLEN,IUSER_LAW,UPARAM ,MAXUPARAM,
     .                  NUPARAM,NUVAR,IFUNC    ,MAXFUNC,NFUNC    ,
     .                  PARMAT )
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ST_LECM_CUSTOM_USER_NAME" :: ST_LECM_CUSTOM_USER_NAME
!DEC$ ATTRIBUTES REFERENCE :: ILAW,ROOTN,ROOTLEN,IUSER_LAW,UPARAM,MAXUPARAM,NUPARAM,NUVAR,IFUNC,MAXFUNC,NFUNC ,PARMAT
#endif

      USE LAW_USER
      USE ST_ULAW
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C IIN      |  1      | I | R | INPUT FILE UNIT (D00 file) 
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
CIUSER_LAW /  1      | I | R |  USER MATERIAl NUMBER
C UPARAM   | NUPARAM | F | W | USER MATERIAL PARAMETER ARRAY
C MAXUPARAM|  1      | I | R | MAXIMUM SIZE OF UPARAM 
C NUPARAM  |  1      | I | W | SIZE OF UPARAM =< MAXUPARAM
C NUVAR    |  1      | I | W | NUMBER OF USER ELEMENT VARIABLES
C----------+---------+---+---+--------------------------------------------
C IFUNC    | NFUNC   | I | W | FUNCTION NUMBER ARRAY
C MAXFUNC  |  1      | I | R | MAXIMUM SIZE OF IFUNC
C NFUNC    |  1      | I | W | SIZE OF IFUNC =< MAXFUNC
C----------+---------+---+---+--------------------------------------------
C (STIFINT)|                 | Replaced by PARMAT(1)
C PARMAT   |  3      | F | W | 1)STIFNESS MODULUS FOR INTERFACE
C          |(in v31) |   |   |       (AND INITIAL TIME STEP COMPUTATION)
C          |         |   |   | 2)YOUNG MODULUS (only needed for shells)
C          |         |   |   | 3)POISSON'S RATIO (only needed for shells)
C          |         |   |   | 4... Possible future use
C----------+---------+---+---+--------------------------------------------
C
C     This subroutine read the user material parameters.
C     The material cards that are common for all materials
C     (card 1 to 7 in version 2.2) have previously been read.
C     The NUPARAM material datas have to bee stored in UPARAM array.
C     If some standard radioss functions (time function or 
C     x,y function) are needed, this NFUNC function numbers have to 
C     bee stored in IFUNC array.  
C-----------------------------------------------
C   C o m m o n   B l o c k s
C-----------------------------------------------
#ifndef ncharline
#define ncharline 500
#endif
#ifndef nchartitle
#define nchartitle 500
#endif
C-----------------------------------------------
C   D u m m y   A r g u m e n t s
C-----------------------------------------------
      INTEGER MAXUPARAM,NUPARAM,NUVAR,MAXFUNC,NFUNC,
     .        IFUNC(MAXFUNC),IUSER_LAW,ILAW,ROOTLEN
      my_real
     .    UPARAM(MAXUPARAM),PARMAT(*)

      CHARACTER*80 ROOTN
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      type(ULAWBUF) :: USERBUF2
      CHARACTER TITR*nchartitle

      INTEGER LENROOTN
      CHARACTER FILNAM*512,CLAW*4
      INTEGER LEN_FILNAM,IIN,IOUT
      IOUT=31
      IIN=30
C=====================================
C Open the Input File
      WRITE(CLAW,'(I4.4)')ILAW
      FILNAM  ='SI'//ROOTN(1:ROOTLEN)//'_'//CLAW//'.scr'
      LEN_FILNAM=LEN_TRIM(FILNAM)

      OPEN(UNIT=IIN,
     .     FORM='FORMATTED',
     .     FILE=FILNAM(1:LEN_FILNAM),
     .     ACTION='READ'
     .     )


C Open the Output File
        WRITE(CLAW,'(I4.4)')ILAW
        FILNAM  ='SO'//ROOTN(1:ROOTLEN)//'_'//CLAW//'.scr'
        LEN_FILNAM=LEN_TRIM(FILNAM)

        OPEN(UNIT=31,FILE=FILNAM(1:LEN_FILNAM),
     .     FORM='FORMATTED')

C=====================================
C
C   New Use material Law
         IF(IUSER_LAW == 1) THEn
           CALL LECMUSER01(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                     NUVAR  ,IFUNC ,MAXFUNC,NFUNC    ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 2) THEN
           CALL LECMUSER02(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 3) THEN
           CALL LECMUSER03(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 4) THEN
           CALL LECMUSER04(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 5) THEN
           CALL LECMUSER05(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 6) THEN
           CALL LECMUSER06(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 7) THEN
           CALL LECMUSER07(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 8) THEN
           CALL LECMUSER08(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 9) THEN
           CALL LECMUSER09(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 10) THEN
           CALL LECMUSER10(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 11) THEN
           CALL LECMUSER11(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 12) THEN
           CALL LECMUSER12(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 13) THEN
           CALL LECMUSER13(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 14) THEN
           CALL LECMUSER14(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 15) THEN
           CALL LECMUSER15(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 16) THEN
           CALL LECMUSER16(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 17) THEN
           CALL LECMUSER17(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 18) THEN
           CALL LECMUSER18(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 19) THEN
           CALL LECMUSER19(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 20) THEN
           CALL LECMUSER20(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 21) THEn
           CALL LECMUSER21(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 22) THEN
           CALL LECMUSER22(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 23) THEN
           CALL LECMUSER23(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 24) THEN
           CALL LECMUSER24(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 25) THEN
           CALL LECMUSER25(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 26) THEN
           CALL LECMUSER26(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 27) THEN
           CALL LECMUSER27(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 28) THEN
           CALL LECMUSER28(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 29) THEN
           CALL LECMUSER29(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 30) THEn
           CALL LECMUSER30(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 31) THEN
           CALL LECMUSER31(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 32) THEN
           CALL LECMUSER32(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 33) THEN
           CALL LECMUSER33(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 34) THEN
           CALL LECMUSER34(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 35) THEN
           CALL LECMUSER35(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 36) THEN
           CALL LECMUSER36(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 37) THEN
           CALL LECMUSER37(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 38) THEN
           CALL LECMUSER38(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 39) THEN
           CALL LECMUSER39(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 40) THEN
           CALL LECMUSER40(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 41) THEN
           CALL LECMUSER41(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 42) THEN
           CALL LECMUSER42(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 43) THEN
           CALL LECMUSER43(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 44) THEN
           CALL LECMUSER44(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 45) THEN
           CALL LECMUSER45(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 46) THEN
           CALL LECMUSER46(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 47) THEN
           CALL LECMUSER47(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 48) THEN
           CALL LECMUSER48(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 49) THEN
           CALL LECMUSER49(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 50) THEN
           CALL LECMUSER50(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 51) THEn
           CALL LECMUSER51(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 52) THEN
           CALL LECMUSER52(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 53) THEN
           CALL LECMUSER53(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 54) THEN
           CALL LECMUSER54(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 55) THEN
           CALL LECMUSER55(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 56) THEN
           CALL LECMUSER56(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 57) THEN
           CALL LECMUSER57(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 58) THEN
           CALL LECMUSER58(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 59) THEN
           CALL LECMUSER59(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 60) THEn
           CALL LECMUSER60(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 61) THEN
           CALL LECMUSER61(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 62) THEN
           CALL LECMUSER62(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 63) THEN
           CALL LECMUSER63(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 64) THEN
           CALL LECMUSER64(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 65) THEN
           CALL LECMUSER65(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 66) THEN
           CALL LECMUSER66(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 67) THEN
           CALL LECMUSER67(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 68) THEN
           CALL LECMUSER68(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 69) THEN
           CALL LECMUSER69(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 70) THEN
           CALL LECMUSER70(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 71) THEN
           CALL LECMUSER71(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 72) THEN
           CALL LECMUSER72(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 73) THEN
           CALL LECMUSER73(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 74) THEN
           CALL LECMUSER74(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 75) THEN
           CALL LECMUSER75(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 76) THEN
           CALL LECMUSER76(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 77) THEN
           CALL LECMUSER77(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 78) THEN
           CALL LECMUSER78(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 79) THEN
           CALL LECMUSER79(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 80) THEN
           CALL LECMUSER80(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 81) THEN
           CALL LECMUSER81(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 82) THEN
           CALL LECMUSER82(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 83) THEN
           CALL LECMUSER83(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 84) THEN
           CALL LECMUSER84(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 85) THEN
           CALL LECMUSER85(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 86) THEN
           CALL LECMUSER86(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 87) THEN
           CALL LECMUSER87(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 88) THEN
           CALL LECMUSER88(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 89) THEN
           CALL LECMUSER89(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 90) THEN
           CALL LECMUSER90(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 91) THEN
           CALL LECMUSER91(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 92) THEN
           CALL LECMUSER92(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 93) THEN
           CALL LECMUSER93(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 94) THEN
           CALL LECMUSER94(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 95) THEN
           CALL LECMUSER95(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 96) THEN
           CALL LECMUSER96(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 97) THEN
           CALL LECMUSER97(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 98) THEN
           CALL LECMUSER98(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ELSEIF(IUSER_LAW == 99) THEN
           CALL LECMUSER99(IIN    ,IOUT ,UPARAM ,MAXUPARAM, NUPARAM,
     .                  NUVAR,IFUNC    ,MAXFUNC,NFUNC      ,PARMAT ,
     .                     USERBUF)
         ENDIF

      CLOSE (UNIT=IIN)
      CLOSE (UNIT=IOUT)


      RETURN
      END
