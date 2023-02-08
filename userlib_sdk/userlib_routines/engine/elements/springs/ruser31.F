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
Chd|  RUSER31                                                     
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|        GET_V_FUNC                                                  
Chd|        GET_U_PNU                                                   
Chd|====================================================================
      SUBROUTINE RUSER31(NEL,IOUT   ,IPROP  ,UVAR   ,NUVAR  ,
     2             FX      ,FY      ,FZ     ,XMOM   ,YMOM   ,
     3             ZMOM    ,E       ,OFF    ,STIFM  ,STIFR  ,
     4             VISCM   ,VISCR   ,MASS   ,XINER  ,DT     ,
     5             XL      ,VX      ,RY1    ,RZ1    ,RX     ,
     6             RY2     ,RZ2     ,FR_WAVE)
C-------------------------------------------------------------------------
C     This subroutine compute springs forces and moments.
C-------------------------------------------------------------------------
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
C IPROP    |  1      | I | R | PROPERTY NUMBER
C----------+---------+---+---+--------------------------------------------
C XL       |   NEL   | F | R | ELEMENT LENGTH
C----------+---------+---+---+--------------------------------------------
C UVAR     |NUVAR*NEL| F |R/W| USER ELEMENT VARIABLES
C NUVAR    |  1      | I | R | NUMBER OF USER ELEMENT VARIABLES
C----------+---------+---+---+--------------------------------------------
C-------------------------------------------------------------------------
C FUNCTION 
C-------------------------------------------------------------------------
C INTEGER II = GET_U_PNU(I,IP,KK)
C         IFUNCI = GET_U_PNU(I,IP,KFUNC)
C         IPROPI = GET_U_PNU(I,IP,KFUNC)
C         IMATI  = GET_U_PNU(I,IP,KMAT)
C         I     :     VARIABLE INDEX(1 for first variable,...)
C         IP    :     PROPERTY NUMBER
C         KK    :     PARAMETER KFUNC,KMAT,KPROP
C         THIS FUNCTION RETURN THE USER STORED FUNCTION(IF KK=KFUNC), 
C         MATERIAL(IF KK=KMAT) OR PROPERTY(IF KK=KPROP) NUMBER. 
C         SEE LECG29 FOR CORRESPONDING ID STORAGE.
C-------------------------------------------------------------------------
C INTEGER IFUNCI = GET_U_MNU(I,IM,KFUNC)
C         I     :     VARIABLE INDEX(1 for first function)
C         IM    :     MATERIAL NUMBER
C         KFUNC :     ONLY FUNCTION ARE YET AVAILABLE.
C         THIS FUNCTION RETURN THE USER STORED FUNCTION NUMBER(function 
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
C INTEGER PID = GET_U_PID(IP)
C         IP    :     PROPERTY NUMBER
C         THIS FUNCTION RETURN THE USER PROPERTY ID CORRESPONDING TO
C         USER PROPERTY NUMBER IP. 
C-------------------------------------------------------------------------
C INTEGER MID = GET_U_MID(IM)
C         IM   :     MATERIAL NUMBER
C         THIS FUNCTION RETURN THE USER MATERIAL ID CORRESPONDING TO
C         USER MATERIAL NUMBER IM. 
C-------------------------------------------------------------------------
C my_real Y = GET_U_FUNC(IFUNC,X,DYDX)
C         IFUNC :     function number obtained by 
C                     IFUNC = GET_U_MNU(I,IM,KFUNC) or IFUNC = GET_U_PNU(I,IP,KFUNC)
C         X     :     X value
C         DYDX  :     slope dY/dX
C         THIS FUNCTION RETURN Y(X)
C-------------------------------------------------------------------------
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------------------------------------------------------
C   D u m m y   A r g u m e n t s   a n d   F u n c t i o n
C----------------------------------------------------------
      INTEGER IOUT,NEL,NUVAR,IPROP,ICO,
     .        GET_U_PNU,GET_U_PID,GET_U_MID,GET_U_MNU,
     .        KFUNC,KMAT,KPROP
      my_real
     .   UVAR(NUVAR,*),DT ,
     .   FX(*), FY(*), FZ(*), E(*), VX(*),MASS(*) ,XINER(*),
     .   RY1(*), RZ1(*), OFF(*), XMOM(*), YMOM(*),
     .   ZMOM(*), RX(*), RY2(*), RZ2(*),XL(*),
     .   STIFM(*) ,STIFR(*) , VISCM(*) ,VISCR(*) ,FR_WAVE(*) ,
     .   GET_U_MAT, GET_U_GEO, GET_U_FUNC
      EXTERNAL GET_U_MNU,GET_U_PNU,GET_U_MID,GET_U_PID,
     .         GET_U_MAT,GET_U_GEO, GET_U_FUNC
      PARAMETER (KFUNC=29)
      PARAMETER (KMAT=31)
      PARAMETER (KPROP=33)
C=================================================================
C
C     EXAMPLE 3 : Elastoplastic truss defined with 1 user property.
C                 
C               
C=================================================================
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER I,ID1,ID2,ID10,ID20,
     .        IFUN_XP,IFUN_XMI,IFUN_XXPI,IFUN_XXMI,IFUN_YY1PI,
     .        IFUN_YY1MI,IFUN_YY2PI,IFUN_YY2MI,IFUN_ZZ1PI,
     .        IFUN_ZZ1MI,IFUN_ZZ2PI,IFUN_ZZ2MI,
     .        IFUN_XMR,IFUN_XXPR,IFUN_XXMR,IFUN_YY1PR,
     .        IFUN_YY1MR,IFUN_YY2PR,IFUN_YY2MR,IFUN_ZZ1PR,
     .        IFUN_ZZ1MR,IFUN_ZZ2PR,IFUN_ZZ2MR
      INTEGER IFUNXM(NEL),IFUNXXM(NEL),IFUNYY1M(NEL),
     .        IFUNZZ1M(NEL),IFUNYY2M(NEL),IFUNZZ2M(NEL),
     .        IFUNXP(NEL),IFUNXXP(NEL),IFUNYY1P(NEL),
     .        IFUNZZ1P(NEL),IFUNYY2P(NEL),IFUNZZ2P(NEL),
     .        JPOSXM(NEL),JPOSXXM(NEL),JPOSYY1M(NEL),
     .        JPOSZZ1M(NEL),JPOSYY2M(NEL),JPOSZZ2M(NEL),
     .        JPOSXP(NEL),JPOSXXP(NEL),JPOSYY1P(NEL),
     .        JPOSZZ1P(NEL),JPOSYY2P(NEL),JPOSZZ2P(NEL)
      my_real 
     .        DYDX(NEL),
     .        X(NEL),FXM(NEL),FXP(NEL),
     .        XX(NEL),FXXM(NEL),FXXP(NEL),
     .        YY1(NEL),FYY1M(NEL),FYY1P(NEL),
     .        ZZ1(NEL),FZZ1M(NEL),FZZ1P(NEL),
     .        YY2(NEL),FYY2M(NEL),FYY2P(NEL),
     .        ZZ2(NEL),FZZ2M(NEL),FZZ2P(NEL),ULENG(NEL),
     .        MY1(NEL),MY2(NEL),MZ1(NEL),MZ2(NEL),
     .        XLIMG,XLIM,XXLIM,YY1LIM,YY2LIM,ZZ1LIM,ZZ2LIM,
     .        K11,K44,K55,K66,K5B,K6C,LENG2,LENG,ULENG0,R,AX,AY,AZ,
     .        A,B,D,FF1,FF2,R1,MM,FF
      my_real
     .        ZERO,UNDEMI,UN,EM20,DEUX
Csm45a2     .        EM20,UN,ZERO
Csm45a2      DATA EM20/1.E-20/,UN/1./,ZERO/0.0/
C-----------------------------------------------
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='USER SPRING PROPERTY '
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

