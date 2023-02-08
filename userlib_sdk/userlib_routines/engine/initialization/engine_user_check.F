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
Chd|  ENGINE_USER_CHECK                                          
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|                                                         
Chd|====================================================================
        SUBROUTINE ENGINE_USER_CHECK(MY_RANK,TSTOP,NCYCLE,TT,MSTOP)
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENGINE_USER_CHECK" :: ENGINE_USER_CHECK
!DEC$ ATTRIBUTES REFERENCE :: MY_RANK,TSTOP,NCYCLE,TT,MSTOP
#endif
C -----------------------------------------------------------------
        IMPLICIT NONE
C-----------------------------------------------
C   I N P U T   A r g u m e n t s
C-----------------------------------------------
        INTEGER, INTENT(in) :: MY_RANK,NCYCLE
        INTEGER, INTENT(inout) :: MSTOP
        REAL(kind=8), INTENT(in) :: TSTOP,TT
!       integer MY_RANK  : input  - MPI_RANK id from MPI process MPI_RANK = [0:NSPMD-1]
!       integer NCYCLE  : input  - Current cycle number
!       integer MSTOP  : input-output  - Termination flag : if MSTOP is set to non zero value, Radioss terminates cycle, write restart & exits
!       real(kind=8) TSTOP : Total simulation time
!       real(kind=8) TT : Current simulation time
C-----------------------------------------------
        IF(MY_RANK ==0) THEN

          IF( MOD(NCYCLE,1000)==0) THEN
            WRITE(6,'(A)') 'HELLO WORLD ENGINE_USER_CHECK '
            MSTOP=2
          ENDIF
        ENDIF
C-----------------------------------------------
        END 
