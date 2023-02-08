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
Chd|  ENGINE_USER_INITIALIZE                                                     
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|                                                         
Chd|====================================================================
        SUBROUTINE ENGINE_USER_INITIALIZE( NSPMD, NTHREAD, MY_RANK)
C -----------------------------------------------------------------
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENGINE_USER_INITIALIZE" :: ENGINE_USER_INITIALIZE
!DEC$ ATTRIBUTES REFERENCE :: NSPMD, NTHREAD,MY_RANK
#endif
        IMPLICIT NONE
C-----------------------------------------------
C   I N P U T   A r g u m e n t s
C-----------------------------------------------
        INTEGER, INTENT(IN) :: NSPMD,NTHREAD,MY_RANK
!       integer NSPMD    : input  - Number of MPI domains from Radioss Job
!       integer NTHREADS : input  - Number of Threads from Radioss Job
!       integer MY_RANK  : input  - MPI_RANK id from MPI process MPI_RANK = [0:NSPMD-1]
C-----------------------------------------------
        WRITE(6,'(A)') 'HELLO WORLD /ENGINE_USER_INITIALIZE'
C-----------------------------------------------
        END 
