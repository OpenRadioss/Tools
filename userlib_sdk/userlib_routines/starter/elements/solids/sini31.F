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


C============================================================
C If you are using a C precompiler (cpp) or a fortran compiler compatible
C with cpp,
C uncomment nex line on CRAY 
C#define my_real REAL
C
C or next one on other computers
C#define my_real DOUBLEPRECISION
C 
C in other cases replace "my_real" by REAL or DOUBLEPRECISION 
C at each occurence
C
C comment the line #include      "implicit_f.inc"
Cgw41p nouvelles routines
Chd|====================================================================
Chd|  SINI31                                                      
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE SINI31(
     1 NEL  ,NUVAR,IOUT ,IPROP ,IMAT,SOLID_ID,
     2 EINT ,VOL  ,UVAR ,OFF,RHO  ,SIG  ,
     3 XX1  ,XX2  ,XX3  ,XX4  ,XX5  ,XX6  ,XX7  ,XX8 ,
     4 YY1  ,YY2  ,YY3  ,YY4  ,YY5  ,YY6  ,YY7  ,YY8 ,
     5 ZZ1  ,ZZ2  ,ZZ3  ,ZZ4  ,ZZ5  ,ZZ6  ,ZZ7  ,ZZ8 ,
     6 VX1  ,VX2  ,VX3  ,VX4  ,VX5  ,VX6  ,VX7  ,VX8 ,
     7 VY1  ,VY2  ,VY3  ,VY4  ,VY5  ,VY6  ,VY7  ,VY8 ,
     8 VZ1  ,VZ2  ,VZ3  ,VZ4  ,VZ5  ,VZ6  ,VZ7  ,VZ8 ,
     9 VRX1 ,VRX2 ,VRX3 ,VRX4 ,VRX5 ,VRX6 ,VRX7 ,VRX8 ,
     A VRY1 ,VRY2 ,VRY3 ,VRY4 ,VRY5 ,VRY6 ,VRY7 ,VRY8 ,
     B VRZ1 ,VRZ2 ,VRZ3 ,VRZ4 ,VRZ5 ,VRZ6 ,VRZ7 ,VRZ8 ,
     C MAS1 ,MAS2 ,MAS3 ,MAS4 ,MAS5 ,MAS6 ,MAS7 ,MAS8 ,
     D INN1 ,INN2 ,INN3 ,INN4 ,INN5 ,INN6 ,INN7 ,INN8 ,
     C STIFM,STIFR,VISCM,VISCR)
C-------------------------------------------------------------------------
C     This subroutine compute user 8 nodes solids forces and moments.
C-------------------------------------------------------------------------
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C NEL      |  1      | I | R | NUMBER OF ELEMENTS IN CURRENT GROUP
C NUVAR    |  1      | I | R | NUMBER OF USER ELEMENT VARIABLES
C IOUT     |  1      | I | R | OUTPUT FILE UNIT (L01 file)
C IPROP    |  1      | I | R | PROPERTY NUMBER
C IMAT     |  1      | I | R | MATERIAL NUMBER
C SOLID_ID |  NEL    | I | R | SOLID ELEMENT ID
C----------+---------+---+---+--------------------------------------------
C EINT     |  NEL    | F | W | TOTAL INTERNAL ENERGY at t=0
C----------+---------+---+---+--------------------------------------------
C VOL      |  NEL    | F |R/W| INITIAL VOLUME 
C          |         |   |   | incoming value is computed with 1 integration
C          |         |   |   | point, this value can be recomputed
C UVAR     |NEL*NUVAR| F |R/W| USER ELEMENT VARIABLES
C          |         |   |   | NUVAR IS DEFINED IN LECG29 (not in LECMAT29)
C FR_WAVE  |  NEL    | F |R/W| COMMUNICATION ARRAY TO ELEMENTS CONNECTED
C          |         |   |   | TO COMMON NODES
C----------+---------+---+---+--------------------------------------------
C OFF      |  NEL    | F |R/W| DELETE FLAG (=1. ON =0. OFF)
C RHO      |  NEL    | F |R/W| DENSITY (material law)
C SIG      | 6*NEL   | F |R/W| STRESS TENSOR SX,SY,SZ,SXY,SYZ,SZX
C          |         |   |   | initial value 
C----------+---------+---+---+--------------------------------------------
C XX1      |   NEL   | F | R | X COORDINATE NODE 1 in global frame
C YY1      |   NEL   | F | R | Y COORDINATE NODE 1 in global frame
C ZZ1      |   NEL   | F | R | Z COORDINATE NODE 1 in global frame
C XX2..ZZ8 |   NEL   | F | R | SAME FOR NODE 2 TO 8
C VX1      |   NEL   | F | R | X VELOCITY NODE 1,glob f
C VY1      |   NEL   | F | R | Y VELOCITY NODE 1,glob f
C VZ1      |   NEL   | F | R | Z VELOCITY NODE 1,glob f
C VRX1     |   NEL   | F | R | X ROTATIONAL VELOCITY NODE 1 ...
C VRY1     |   NEL   | F | R | Y ROTATIONAL VELOCITY NODE 1 ...
C VRZ1     |   NEL   | F | R | Z ROTATIONAL VELOCITY NODE 1 ...
C-------------------------------------------------------------------------
C MAS1     |   NEL   | F | W | MASS NODE 1
C MAS2.MAS8|   NEL   | F | W | SAME FOR NODE 2 TO 8
C INN1     |   NEL   | F | W | INERTIA NODE 1
C INN2.INN8|   NEL   | F | W | SAME FOR NODE 2 TO 8
C STIFM    |   NEL   | F | W | TRANSLATIONAL STIFNESS OVERESTIMATION
C STIFR    |   NEL   | F | W | ROTATIONAL STIFNESS OVERESTIMATION
C VISCM    |   NEL   | F | W | TRANSLATIONAL VISCOSITY OVERESTIMATION
C VISCR    |   NEL   | F | W | ROTATIONAL VISCOSITY OVERESTIMATION
C          |         |   |   | STIFM,STIFR,VISCM,VISCR are used to compute
C          |         |   |   | element or nodal time step.in Radioss Starter 
C-------------------------------------------------------------------------
C AVAILABLE FUNCTION 
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
C my_real Y = GET_U_FUNC(IFUNC,X,DXDY)
C         IFUNC :     function number obtained by 
C                     IFUNC = GET_U_MNU(I,IM,KFUNC) or IFUNC = GET_U_PNU(I,IP,KFUNC)
C         X     :     X value
C         DXDY  :     slope dX/dY
C         THIS FUNCTION RETURN Y(X)
C-------------------------------------------------------------------------
C-------------------------------------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------------------------------------------------------
C   D u m m y   A r g u m e n t s  
C----------------------------------------------------------
      INTEGER NEL,NUVAR,IOUT,IPROP,IMAT,SOLID_ID(*)
      my_real
     .   UVAR(NEL,NUVAR),
     .   STIFM(*) ,STIFR(*) , VISCM(*) ,VISCR(*) ,
     .   OFF(*) ,EINT(*) , RHO(*) ,VOL(*) ,SIG(6,*),
     2 XX1(*),XX2(*),XX3(*),XX4(*),XX5(*),XX6(*),XX7(*),XX8(*),
     3 YY1(*),YY2(*),YY3(*),YY4(*),YY5(*),YY6(*),YY7(*),YY8(*),
     4 ZZ1(*),ZZ2(*),ZZ3(*),ZZ4(*),ZZ5(*),ZZ6(*),ZZ7(*),ZZ8(*),
     5 VX1(*),VX2(*),VX3(*),VX4(*),VX5(*),VX6(*),VX7(*),VX8(*),
     6 VY1(*),VY2(*),VY3(*),VY4(*),VY5(*),VY6(*),VY7(*),VY8(*),
     7 VZ1(*),VZ2(*),VZ3(*),VZ4(*),VZ5(*),VZ6(*),VZ7(*),VZ8(*),
     8 VRX1(*),VRX2(*),VRX3(*),VRX4(*),VRX5(*),VRX6(*),VRX7(*),VRX8(*),
     9 VRY1(*),VRY2(*),VRY3(*),VRY4(*),VRY5(*),VRY6(*),VRY7(*),VRY8(*),
     A VRZ1(*),VRZ2(*),VRZ3(*),VRZ4(*),VRZ5(*),VRZ6(*),VRZ7(*),VRZ8(*),
     C MAS1(*),MAS2(*),MAS3(*),MAS4(*),MAS5(*),MAS6(*),MAS7(*),MAS8(*),
     D INN1(*),INN2(*),INN3(*),INN4(*),INN5(*),INN6(*),INN7(*),INN8(*)
C----------------------------------------------------------
C   E x t e r n a l  F u n c t i o n
C----------------------------------------------------------
      INTEGER  GET_U_PNU,GET_U_PID,GET_U_MID,GET_U_MNU
      my_real
     .   GET_U_MAT, GET_U_GEO, GET_U_FUNC
      EXTERNAL GET_U_MNU,GET_U_PNU,GET_U_MID,GET_U_PID,
     .         GET_U_MAT,GET_U_GEO, GET_U_FUNC
      INTEGER  KFUNC,KMAT,KPROP
      PARAMETER (KFUNC=29)
      PARAMETER (KMAT=31)
      PARAMETER (KPROP=33)
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='USER SOLID INITIALIZATION'
        SIZE=LEN_TRIM(OPTION)
        WRITE(6,'(A)')
     .     '** ERROR IN USER LIBRARY SDK'
         WRITE(6,'(A,A)')
     .     ' OPTION : ',OPTION(1:SIZE)
        WRITE(6,'(A)')
     .     'USER INTERFACE OPTION USED, BUT NO USER INTERFACE ROUTINE IS FOUND IN SDK'

        CALL ARRET(2)
      END 

