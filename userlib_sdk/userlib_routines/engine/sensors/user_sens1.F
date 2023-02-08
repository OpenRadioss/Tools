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
Chd|  USER_SENS1                                                  
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|        GET_U_FUNC                                                  
Chd|        GET_U_NUMFUN                                                
Chd|        GET_U_NUMSENS                                               
Chd|        GET_U_SENS_IPAR                                             
Chd|        GET_U_SENS_VALUE                                            
Chd|        SET_U_SENS_VALUE                                            
Chd|====================================================================
      SUBROUTINE USER_SENS1(ID)
C----------+---------+---+---+--------------------------------------------
C VAR      | SIZE    |TYP| RW| DEFINITION
C----------+---------+---+---+--------------------------------------------
C ID       |  1      | I | R | SENSOR ID
C=========================================================================
C RADIOSS DATABASE ACCESS FUNCTIONS
C------  to get a sensor number 
C      INTEGER NUM = GET_U_NUMSENS(ID)
C              ID  = SENSOR ID
C              NUM = SENSOR NUMBER
C------ to retrieve a float sensor parameter
C      INTEGER IERR =  GET_U_SENS_FPAR(IVAR, VAR)
C              IVAR  = float   VARIABLE INDEX
C              VAR   = integer VALUE
C------ to retrieve an intenger sensor parameter
C      INTEGER IERR =  GET_U_SENS_IPAR(IVAR, VAR)
C              IVAR  = integer VARIABLE INDEX
C              VAR   = integer VALUE
C------ to write a variable to a sensor buffer (float)
C      INTEGER IERR =  SET_U_SENS_VALUE(NSENS,IVAR,VAR)
C              NSENS = integer SENSOR NUMBER
C              IVAR  = integer BUFFER INDEX
C              VAR   = float   VALUE
C------ to read a variable from a sensor buffer (float)
C      INTEGER IERR =  GET_U_SENS_VALUE(NSENS,IVAR,VAR)
C              NSENS = integer SENSOR NUMBER
C              IVAR  = integer BUFFER INDEX
C              VAR   = float   VALUE
C------ to activate a sensor using radioss flag
C      INTEGER IERR = SET_U_SENS_ACTI(NSENS)
C             NSENS = integer SENSOR NUMBER
C------ to check radioss activation status of a sensor
C      FLOAT   DTIME = GET_U_SENS_ACTI(NSENS)
C             DTIME  = float TIME DELAY SINCE FIRST ACTIVATION 
C                     (actif <=> DTIME > 0)
C             NSENS = integer SENSOR NUMBER
C====   to check current time
C	FLOAT  TIME = GET_U_TIME
C------ to check current cycle
C	INTEGER NCYC = GET_U_CYCLE
C====   to access accelerometer values
C 	INTEGER IERR = GET_U_ACCEL(NACC, AX,AY,AZ)
C              AX,AY,AZ = float acceleration components
C              NACC = integer accelerator number,
C              IDACC= integer accelerator ID, and
C	       NACC = GET_U_NUMACC(IDACC)
C====   to access nodal values
C 	INTEGER IERR = GET_U_NOD_X(NOD, X,Y,Z)
C 	INTEGER IERR = GET_U_NOD_D(NOD, DX,DY,DZ)
C 	INTEGER IERR = GET_U_NOD_V(NOD, VX,VY,VZ)
C 	INTEGER IERR = GET_U_NOD_A(NOD, AX,AY,AZ)
C              X, Y, Z  = float nodal coordinates
C              DX,DY,DZ = float nodal displacements
C              AX,AY,AZ = float nodal velocities
C              AX,AY,AZ = float nodal accelerations
C              NOD = integer node number 
C              NID = integer node ID, and
C              NOD = GET_U_NUMNOD(ID)	
C====   to access Radioss functions
C	FLOAT Y = GET_U_FUNC(IFUNC, X, DERI)
C              Y    = float ordinate
C              X    = float abscissa
C              DERI  = float Y/X
C              IFUNC = integer function number 
C              IDFUN = integer function ID, and
C 	INTEGER IFUNC = GET_U_NUMFUN(IDFUN)
C-----------------------------------------------
C    MAXIMUM NUMBER OF USER SENSOR VARIABLES = 100 
C=========================================================================
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include      "implicit_f.inc"
C----------------------------------------------------------
C   D u m m y   A r g u m e n t s   a n d   F u n c t i o n
C----------------------------------------------------------
      INTEGER ID, IDFUN, NFUN
      INTEGER GET_U_NUMSENS,GET_U_SENS_IPAR, GET_U_SENS_FPAR,
     .        GET_U_SENS_VALUE,SET_U_SENS_VALUE,SET_U_SENS_ACTI,
     .        GET_U_NUMACC,GET_U_ACCEL,GET_U_NUMNOD,GET_U_NOD_X,
     .        GET_U_NOD_D,GET_U_NOD_V,GET_U_NOD_A,GET_U_CYCLE,
     .        GET_U_NUMFUN,GET_U_FID
      my_real GET_U_TIME,GET_U_SENS_ACTI,GET_U_FUNC
      EXTERNAL GET_U_SENS_IPAR,GET_U_SENS_FPAR,
     .         GET_U_SENS_VALUE,SET_U_SENS_VALUE,
     .         GET_U_SENS_ACTI,SET_U_SENS_ACTI,GET_U_NUMSENS,
     .         GET_U_NUMACC,GET_U_ACCEL,GET_U_NOD_X,
     .         GET_U_NUMNOD,GET_U_NOD_D,GET_U_NOD_V,GET_U_NOD_A,
     .         GET_U_NUMFUN,GET_U_FID,GET_U_TIME,GET_U_CYCLE
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
      INTEGER IERR, NSENS
      my_real
     .   DY1,DY2,DY, DZ1,DZ2,DZ, SY, SZ, DERI
      my_real
     .   UNDEMI
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='USER SENSOR'
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
