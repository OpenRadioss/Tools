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
Chd|  ST_LECM                                                      
Chd|-- called by -----------
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE ENG_USERINT(IGTYP,
     1  NSN       ,II       ,PID      ,NUVAR     ,  
     2  UVAR  )
     
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_USERINT" :: ENG_USERINT
!DEC$ ATTRIBUTES REFERENCE :: IGTYP
     1          NSN       ,II       ,PID      ,NUVAR     ,  
     2          UVAR        
#endif

C-----------------------------------------------
C   M o d u l e s
C-----------------------------------------------
      USE UINTBUF_MOD
      USE UINTBUF_USE_MOD
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   I n p u t     A r g u m e n t s 
C-----------------------------------------------
      INTEGER ROOTLEN
      CHARACTER*80 ROOTN

      INTEGER 
     1 IGTYP, NSN, NUVAR   ,II,PID
       my_real
     1   UVAR(*) 
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
#ifndef ncharline
#define ncharline 500
#endif
      INTEGER LENROOTN,IOUT,LENLINE,itsk
      CHARACTER FILNAM*512,CLAW*4,LINE*ncharline
      INTEGER LEN_FILNAM
      INTEGER GET_U_TASK
      EXTERNAL GET_U_TASK
C-----------------------------------------------
C Open the Output File
        itsk=get_u_task()
        IOUT=31*10000+itsk

      OPEN(UNIT=IOUT,STATUS='SCRATCH', FORM='FORMATTED')



           IF (IGTYP == 29) THEN                                        
             CALL USERINT1(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 30) THEN                                    
             CALL USERINT2(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 31) THEN                                    
             CALL USERINT3(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 37) THEN                                    
             CALL USERINT4(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 38) THEN                                    
             CALL USERINT5(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 39) THEN                                    
             CALL USERINT6(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 40) THEN                                    
             CALL USERINT7(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 41) THEN                                    
             CALL USERINT8(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )                                 
           ELSEIF (IGTYP == 42) THEN                                    
             CALL USERINT9(                                             
     .            NSN       ,II       ,IOUT     ,PID      ,NUVAR     ,  
     .            UVAR,UINTBUF_VAR  )
           ENDIF                                                        

      REWIND(IOUT)
      DO WHILE(.TRUE.)
          READ(UNIT=IOUT,END=999,FMT='(A)')LINE    
          LENLINE=LEN_TRIM(LINE)
          CALL WRITE_IOUT(LINE,LENLINE)
      ENDDO
 999  CONTINUE 
      CLOSE (UNIT=IOUT)

      END
