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
Chd|  USERWI                                                      
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE USERWI(
     1           IIN    ,IOUT   ,NUVAR  ,NUVARI ,NUMNOD ,
     2           NCYCLE ,LENWA  ,IUVAR  ,ITAB   ,TT     ,
     3           DT1    ,DT2    ,USREINT,EXWORK ,UVAR   ,
     4           D      ,X      ,V      ,VR     ,MASS   ,
     5           INER   ,STIFN  ,STIFR  ,A      ,AR     ,
     6           WA     )
C-------------------------------------------------------------------------
C     Global user window subroutine (compute forces and moments).
C-------------------------------------------------------------------------
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C IIN      |  1      | I | R | INPUT FILE UNIT (D00 file) 
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
C NUVAR    |  1      | I | R | SIZE OF USER REAL ARRAY
C NUVARI   |  1      | I | R | SIZE OF USER INTEGER ARRAY
C NUMNOD   |  1      | I | R | NUMBER OF NODES
C NCYCLE   |  1      | I | R | CURRENT NCYCLE
C----------+---------+---+---+--------------------------------------------
C IUVAR    | NUVARI  | I |R/W| USER INTEGER ARRAY
C----------+---------+---+---+--------------------------------------------
C ITAB     | NUMNOD  | I | R | USER NODE ID  
C----------+---------+---+---+--------------------------------------------
C TT       |  1      | F | R | CURRENT TIME
C DT1      |  1      | F | R | PREVIOUS TIME STEP
C DT2      |  1      | F | W | USER STABLE TIME STEP
C USREINT  |  1      | F |R/W| USER INTERNAL ENERGY
C EXWORK   |  1      | F |R/W| EXTERNAL WORK
C----------+---------+---+---+--------------------------------------------
C UVAR     | NUVAR   | F |R/W| USER INTEGER ARRAY
C----------+---------+---+---+--------------------------------------------
C D        |3,NUMNOD | F | R | X,Y,Z DISPLACEMENTS
C X        |3,NUMNOD | F | R | X,Y,Z COORDINATES
C V        |3,NUMNOD | F | R | X,Y,Z VELOCITIES
C VR       |3,NUMNOD | F | R | XX,YY,ZZ ROTATIONAL VELOCITIES
C MASS     | NUMNOD  | F | R | NODAL MASS
C INER     | NUMNOD  | F | R | NODAL SHERICAL INERTIA
C----------+---------+---+---+--------------------------------------------
C STIFN    | NUMNOD  | F |R/W| NODAL EQUIVALENT STIFNESS FOR NODAL TIME STEP
C STIFR    | NUMNOD  | F |R/W| NODAL ROTATIONAL STIFNESS FOR NODAL TIME STEP
C A        |3,NUMNOD | F |R/W| X,Y,Z FORCES
C AR       |3,NUMNOD | F |R/W| XX,YY,ZZ MOMENTS
C----------+---------+---+---+--------------------------------------------
C WA       | LENWA   | F | - | WORKING AREA 
C                            | (non saved data from one call to next one)
C----------+---------+---+---+--------------------------------------------
C-------------------------------------------------------------------------
C FUNCTION TO ACCESS USER'S PROPERTIES AND MATERIALS
C-------------------------------------------------------------------------
C INTEGER IP = GET_U_P(PID)
C         INTEGER PID     :     property ID
C         THIS FUNCTION RETURN PROPERTY NUMBER. 
C-------------------------------------------------------------------------
C INTEGER PID = GET_U_PID(IP)
C         IP    :     PROPERTY NUMBER
C         THIS FUNCTION RETURN THE USER PROPERTY ID CORRESPONDING TO
C         USER PROPERTY NUMBER IP. 
C-------------------------------------------------------------------------
C DOUBLE PRECISION PARAMI = GET_U_GEO(I,IP)
C         I     :     PARAMETER INDEX(1 for first parameter,...)
C         IP    :     PROPERTY NUMBER
C         THIS FUNCTION RETURN THE USER GEOMETRY PARAMETERS 
C-------------------------------------------------------------------------
C INTEGER IM = GET_U_M(MID)
C         INTEGER MID     :     MATERIAL ID
C         THIS FUNCTION RETURN MATERIAL NUMBER. 
C-------------------------------------------------------------------------
C INTEGER MID = GET_U_MID(IM)
C         IM   :     MATERIAL NUMBER
C         THIS FUNCTION RETURN THE USER MATERIAL ID CORRESPONDING TO
C         USER MATERIAL NUMBER IM. 
C-------------------------------------------------------------------------
C DOUBLE PRECISION PARAMI = GET_U_MAT(I,IM)
C         I     :     PARAMETER INDEX(1 for first parameter,...)
C         IM    :     MATERIAL NUMBER
C         THIS FUNCTION RETURN THE USER MATERIAL PARAMETERS 
C         NOTE: GET_U_MAT(0,IMAT) RETURN THE DENSITY
C-------------------------------------------------------------------------
C INTEGER II = GET_U_PNU(I,IP,KK)
C         IFUNCI = GET_U_PNU(I,IP,KFUNC)
C         IPROPI = GET_U_PNU(I,IP,KPROP)
C         IMATI = GET_U_PNU(I,IP,KMAT)
C         I     :     VARIABLE INDEX(1 for first variable,...)
C         IP    :     PROPERTY NUMBER
C         KK    :     PARAMETER KFUNC,KMAT,KPROP
C         THIS FUNCTION RETURN THE USER STORED FUNCTION(IF KK=KFUNC), 
C         MATERIAL(IF KK=KMAT) OR PROPERTY(IF KK=KPROP) NUMBERS. 
C         SEE LECG29 FOR CORRESPONDING ID STORAGE.
C-------------------------------------------------------------------------
C INTEGER IFUNCI = GET_U_MNU(I,IM,KFUNC)
C         I     :     VARIABLE INDEX(1 for first function)
C         IM    :     MATERIAL NUMBER
C         KFUNC :     ONLY FUNCTION ARE YET AVAILABLE.
C         THIS FUNCTION RETURN THE USER STORED FUNCTION NUMBERS(function 
C         refered by users materials).
C         SEE LECM29 FOR CORRESPONDING ID STORAGE.
C-------------------------------------------------------------------------
C-------------------------------------------------------------------------
C DOUBLE PRECISION Y = GET_U_FUNC(IFUNC,X,DYDX)
C         IFUNC :     function number obtained by 
C                     IFUNC = GET_U_MNU(I,IM,KFUNC) or 
C                     IFUNC = GET_U_PNU(I,IP,KFUNC)
C         X     :     X value
C         DYDX  :     slope dY/dX
C         THIS FUNCTION RETURN Y(X)
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
      IMPLICIT NONE
C----------------------------------------------------------
C   D u m m y   A r g u m e n t s   a n d   F u n c t i o n
C----------------------------------------------------------
      INTEGER 
     1   IIN    ,IOUT   ,NUVAR   ,NUVARI,NUMNOD,NCYCLE  ,LENWA,
     2   IUVAR(NUVARI)  ,ITAB(NUMNOD)  
       DOUBLE PRECISION
     1   TT     ,DT1    ,DT2     ,USREINT,EXWORK  ,
     2   UVAR(NUVAR) ,D(3,NUMNOD) ,X(3,NUMNOD) ,V(3,NUMNOD) ,
     3   VR(3,NUMNOD) ,A(3,NUMNOD) ,AR(3,NUMNOD) ,MASS(NUMNOD) ,
     4   INER(NUMNOD) ,STIFN(NUMNOD) ,STIFR(NUMNOD),WA(LENWA)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
C=======================================================================
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='USER WINDOW'
        SIZE=LEN_TRIM(OPTION)
        WRITE(6,'(A)')
     .     '** ERROR IN USER LIBRARY SDK'
         WRITE(6,'(A,A)')
     .     ' OPTION : ',OPTION(1:SIZE)
        WRITE(6,'(A)')
     .     'USER INTERFACE OPTION USED, BUT NO USER INTERFACE ROUTINE IS FOUND IN SDK'

        CALL ARRET(2)
      END 

