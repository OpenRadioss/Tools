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
Chd|  RINIUSR1                      src/user1/riniusr1.F          
Chd|-- called by -----------
Chd|        RINIT3                        src/ressor1/rinit3.F          
Chd|-- calls ---------------
Chd|        RINI29                        pub/user1/rini29.F            
Chd|====================================================================
      SUBROUTINE RINIUSR1(NEL   ,IOUT   ,IPROP ,
     3                    IX    ,XL     ,MASS  ,XINER  ,STIFM ,
     4                    STIFR ,VISCM  ,VISCR ,UVAR   ,NUVAR )
C-------------------------------------------------------------------------
C     This subroutine initialize springs using user properties.
C-------------------------------------------------------------------------
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
C IPROP    |  1      | I | R | PROPERTY NUMBER
C----------+---------+---+---+--------------------------------------------
C IX       | 3*NEL   | I | R | SPRING CONNECTIVITY
C                            | IX(1,I) NODE 1 ID
C                            | IX(2,I) NODE 2 ID
C                            | IX(3,I) OPTIONNAL NODE 3 ID
C                            | IX(4,I) SPRING ID
C XL       |   NEL   | F | R | ELEMENT LENGTH
C----------+---------+---+---+--------------------------------------------
C MASS     |   NEL   | F | W | ELEMENT MASS
C XINER    |   NEL   | F | W | ELEMENT INERTIA (SPHERICAL)
C STIFM    |   NEL   | F | W | ELEMENT STIFNESS (TIME STEP)
C STIFR    |   NEL   | F | W | ELEMENT ROTATION STIFNESS (TIME STEP)
C VISCM    |   NEL   | F | W | ELEMENT VISCOSITY (TIME STEP)
C VISCR    |   NEL   | F | W | ELEMENT ROTATION VISCOSITY (TIME STEP)
C----------+---------+---+---+--------------------------------------------
C UVAR     |NUVAR*NEL| F | W | USER ELEMENT VARIABLES
C NUVAR    |  1      | I | R | NUMBER OF USER ELEMENT VARIABLES
C----------+---------+---+---+--------------------------------------------
C-------------------------------------------------------------------------
C FUNCTION 
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
C my_real PARAMI = GET_U_GEO(I,IP)
C         I     :     PARAMETER INDEX(1 for first parameter,...)
C         IP    :     PROPERTY NUMBER
C         THIS FUNCTION RETURN THE USER GEOMETRY PARAMETERS 
C-------------------------------------------------------------------------
C my_real PARAMI = GET_U_MAT(I,IM)
C         I     :     PARAMETER INDEX(1 for first parameter,...)
C         IM    :     MATERIAL NUMBER
C         THIS FUNCTION RETURN THE USER MATERIAL PARAMETERS 
C         NOTE: GET_U_MAT(0,IMAT) RETURN THE DENSITY
C-------------------------------------------------------------------------
C INTEGER MID = GET_U_PID(IP)
C         IP    :     PROPERTY NUMBER
C         THIS FUNCTION RETURN THE USER PROPERTY ID CORRESPONDING TO
C         USER PROPERTY NUMBER IP. 
C-------------------------------------------------------------------------
C INTEGER PID = GET_U_MID(IM)
C         IM   :     MATERIAL NUMBER
C         THIS FUNCTION RETURN THE USER MATERIAL ID CORRESPONDING TO
C         USER MATERIAL NUMBER IM. 
C-------------------------------------------------------------------------
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------------------------------------------------------
C   D u m m y   A r g u m e n t s   a n d   F u n c t i o n
C----------------------------------------------------------
      INTEGER IOUT,NUVAR,NEL,IPROP,   
     .        IX(4,NEL) ,
     .        GET_U_PNU,GET_U_PID,GET_U_MID,GET_U_MNU,
     .        KFUNC,KMAT,KPROP
      my_real 
     .        XL(NEL) ,MASS(NEL) ,XINER(NEL) ,STIFM(NEL) ,
     .        STIFR(NEL),VISCM(NEL) ,VISCR(NEL),UVAR(NUVAR,*),
     .        GET_U_MAT,GET_U_GEO
      EXTERNAL GET_U_PNU,GET_U_MNU,GET_U_MAT,GET_U_GEO,GET_U_PID,
     .         GET_U_MID
      PARAMETER (KFUNC=29)
      PARAMETER (KMAT=31)
      PARAMETER (KPROP=33)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
C=================================================================
C     EXAMPLE : ELASTIC BEAM DEFINED WITH 1 USER PROPERTY
C               REFERING 2 USER PROPERTIES (ONE FOR EACH BEAM END)
C               EACH SECONDARY USER PROPERTY DEFINES BEAM GEOMETRY
C               AND REFERS TO ONE USER MATERIAL.
C=================================================================
      CALL RINI29(NEL   ,IOUT   ,IPROP ,
     .            IX    ,XL     ,MASS  ,XINER  ,STIFM ,
     .            STIFR ,VISCM  ,VISCR ,UVAR   ,NUVAR )
C-----------------------------------------------
      RETURN
      END
