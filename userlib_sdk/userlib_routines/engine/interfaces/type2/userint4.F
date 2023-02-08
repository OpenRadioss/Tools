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
Chd|  USERINT4                                                    
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|        GET_U_FUNC                                                  
Chd|        GET_U_PNU                                                   
Chd|        GET_U_TIME                                                  
Chd|        UINTBUF_MOD                                                 
Chd|====================================================================
      SUBROUTINE USERINT4(
     1             NSL     ,ISL     ,IOUT    ,IPROP  ,NUVAR  ,
     2             UVAR    ,USERBUF )
C-----------------------------------------------
C   M o d u l e s
C-----------------------------------------------
      USE UINTBUF_MOD
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C NSL      |  1      | I | R | NUMBER OF SLAVE NODES
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L00 file)
C IPROP    |  1      | I | R | PROPERTY NUMBER
C NUVAR    |  1      | I | R | NUMBER OF USER VARIABLES
C UVAR     |NUVAR    | F |R/W| USER SLAVE NODE VARIABLES
C USERBUF  |         | F |R/W| SLAVE NODE DATA STRUCTURE
C----------+---------+---+---+--------------------------------------------
C-------------------------------------------------------------------------
C EXTERNAL FUNCTIONS :
C-------------------------------------------------------------------------
C INTEGER II = GET_U_PNU(I,IP,KK)
C         IFUNI = GET_U_PNU(I,IP,KFUNC)
C         IPROPI = GET_U_PNU(I,IP,KFUNC)
C         IMATI  = GET_U_PNU(I,IP,KMAT)
C         I     :     VARIABLE INDEX(1 for first variable,...)
C         IP    :     PROPERTY NUMBER
C         KK    :     PARAMETER KFUNC,KMAT,KPROP
C         THIS FUNCTION RETURN THE USER STORED FUNCTION(IF KK=KFUNC), 
C         MATERIAL(IF KK=KMAT) OR PROPERTY(IF KK=KPROP) NUMBER. 
C         SEE LECG29 FOR CORRESPONDING ID STORAGE.
C-------------------------------------------------------------------------
C INTEGER IFUNI = GET_U_MNU(I,IM,KFUNC)
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
C         NOTE: IF(IP==IPROP) UPARAG(I) == GET_U_GEO(I,IPROP)
C         see lecg30 for storage
C-------------------------------------------------------------------------
C my_real PARAMI = GET_U_MAT(I,IM)
C         I     :     PARAMETER INDEX(1 for first parameter,...)
C         IM    :     MATERIAL NUMBER
C         THIS FUNCTION RETURN THE USER MATERIAL PARAMETERS 
C         NOTE: GET_U_MAT(0,IMAT) RETURN THE DENSITY
C         see lecm29,30,31 for storage
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
C my_real Y = GET_U_FUNC(IFUN,X,DXDY)
C         IFUN :     function number obtained by 
C                     IFUN = GET_U_MNU(I,IM,KFUNC) or IFUN = GET_U_PNU(I,IP,KFUNC)
C         X     :     X value
C         DXDY  :     slope dX/dY
C         THIS FUNCTION RETURN Y(X)
C=======================================================================
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------------------------------------------------------
C   D u m m y   A r g u m e n t s   a n d   F u n c t i o n
C----------------------------------------------------------
      my_real, DIMENSION(*)  :: UVAR
      type(UINTBUF) :: USERBUF
      INTEGER  NSL,ISL,IOUT,NUVAR,IPROP
C-----------------------------------------------
C   E x t e r n a l   F u n c t i o n s
C-----------------------------------------------
      INTEGER  GET_U_CYCLE,GET_U_NUMFUN,
     .   GET_U_MNU,GET_U_PNU,GET_U_MID,GET_U_PID
      my_real
     .   GET_U_TIME,GET_U_MAT,GET_U_GEO,GET_U_FUNC
C-----------------------------------------------
C   P a r a m e t e r s
C-----------------------------------------------
      INTEGER KFUNC,KMAT,KPROP
      PARAMETER (KFUNC=29)
      PARAMETER (KMAT=31)
      PARAMETER (KPROP=33)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER  IERROR,IMOD,IFUNN,IFUNT,IFUNS,IDEBUG,IFILTR,IRUPT,ISLAV
      my_real
     .   DTIM,SIGN,SIGT,SIGN1,SIGT1,AREA,DFSIGN,DFSIGT,DSIG,
     .   SIGNMAX,SIGTMAX,DNMAX,DTMAX,FACN,FACT,TIME,
     .   SCAL_F,SCAL_D,SCAL_SR,SSR,ALPHA,DERI,DIS_N,DIS_T
      my_real
     .   ZERO,UN,EM20
C=======================================================================
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='INTERFACE TYPE2 FAILURE MODEL'
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

