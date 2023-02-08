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
Chd|  LECM30                                                      
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE LECM30(IIN  ,IOUT ,UPARAM ,MAXUPARAM,NUPARAM,
     .                  NUVAR,IFUNC,MAXFUNC,NFUNC    ,PARMAT,
     .                  UNITAB )
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
      IMPLICIT NONE
C-----------------------------------------------
C   D u m m y   A r g u m e n t s
C-----------------------------------------------
      INTEGER IIN,IOUT,MAXUPARAM,NUPARAM,NUVAR,MAXFUNC,NFUNC,
     .        IFUNC(MAXFUNC),UNITAB(*)
      DOUBLE PRECISION   UPARAM(MAXUPARAM),PARMAT(*)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
C----------------------------------------------- 
      CHARACTER OPTION*256
      INTEGER SIZE
C----------------------------------------------- 
        OPTION='/MAT/USER2'
        SIZE=LEN_TRIM(OPTION)
        WRITE(6,'(A)')
     .     '** ERROR IN USER LIBRARY SDK'
         WRITE(6,'(A,A)')
     .     ' OPTION : ',OPTION(1:SIZE)
        WRITE(6,'(A)')
     .     'USER INTERFACE OPTION USED, BUT NO USER INTERFACE ROUTINE IS FOUND IN SDK'

        CALL ARRET(2)
      END 
