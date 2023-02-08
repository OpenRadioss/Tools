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
Chd|  LUSER01                                                     
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|        LAW_USERSO                                                  
Chd|====================================================================
      SUBROUTINE LUSER67(
     1     NEL    ,NUPARAM,NUVAR   ,NFUNC   ,IFUNC   ,NPF    ,
     2     TF     ,TIME   ,TIMESTEP,UPARAM  ,RHO     ,VOLUME ,
     3     EINT   ,NGL    ,SOUNDSP ,VISCMAX ,UVAR    ,OFF     ,
     4     SIGY   ,PLA    ,USERBUF)
C -----------------------------------------------------------------
        USE LAW_USERSO
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
C
      INTEGER NEL, NUPARAM, NUVAR,NGL(NEL)
      DOUBLE PRECISION
     .   TIME,TIMESTEP,UPARAM(NUPARAM),
     .   RHO(NEL),VOLUME(NEL),EINT(NEL),     
     .   EPSPXX(MVSIZ),EPSPYY(MVSIZ),EPSPZZ(MVSIZ),
     .   EPSPXY(MVSIZ),EPSPYZ(MVSIZ),EPSPZX(MVSIZ),
     .   DEPSXX(MVSIZ),DEPSYY(MVSIZ),DEPSZZ(MVSIZ),
     .   DEPSXY(MVSIZ),DEPSYZ(MVSIZ),DEPSZX(MVSIZ),
     .   EPSXX(MVSIZ) ,EPSYY(MVSIZ) ,EPSZZ(MVSIZ),
     .   EPSXY(MVSIZ) ,EPSYZ(MVSIZ) ,EPSZX(MVSIZ),
     .   SIGOXX(MVSIZ),SIGOYY(MVSIZ),SIGOZZ(MVSIZ),
     .   SIGOXY(MVSIZ),SIGOYZ(MVSIZ),SIGOZX(MVSIZ),
     .   RHO0(MVSIZ)
C-----------------------------------------------
C   O U T P U T   A r g u m e n t s
C-----------------------------------------------
      DOUBLE PRECISION
     .    SOUNDSP(NEL),VISCMAX(NEL),  
     .    SIGNXX(MVSIZ),SIGNYY(MVSIZ),SIGNZZ(MVSIZ),
     .    SIGNXY(MVSIZ),SIGNYZ(MVSIZ),SIGNZX(MVSIZ),
     .    SIGVXX(MVSIZ),SIGVYY(MVSIZ),SIGVZZ(MVSIZ),
     .    SIGVXY(MVSIZ),SIGVYZ(MVSIZ),SIGVZX(MVSIZ),
     .    DPLA(MVSIZ)
C-----------------------------------------------
C   I N P U T   O U T P U T   A r g u m e n t s 
C-----------------------------------------------
      DOUBLE PRECISION
     .  UVAR(NEL,NUVAR), OFF(NEL),PLA(NEL), SIGY(NEL)
C-----------------------------------------------
      TYPE(ULAWINTBUF) :: USERBUF 
C-----------------------------------------------
      INTEGER NPF(*), NFUNC, IFUNC(NFUNC)
      DOUBLE PRECISION
     .  FINTER ,TF(*)
      EXTERNAL FINTER
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='/MAT/USER67 - SOLID '
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
