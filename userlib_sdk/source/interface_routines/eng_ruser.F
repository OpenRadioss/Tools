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
      SUBROUTINE ENG_RUSER(ITYP,
     1             NEL     ,IPROP   ,UVAR   ,NUVAR  ,
     2             FX      ,FY      ,FZ     ,XMOM   ,YMOM   ,
     3             ZMOM    ,E       ,OFF    ,STIFM  ,STIFR  ,
     4             VISCM   ,VISCR   ,MASS   ,XINER  ,DT     ,
     5             XL      ,VX      ,RY1    ,RZ1    ,RX     ,
     6             RY2     ,RZ2     ,FR_WAVE)
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_RUSER" :: ENG_RUSER
!DEC$ ATTRIBUTES REFERENCE :: ITYP,NEL,IPROP,UVAR,NUVAR,FX,FY,FZ,XMOM,YMOM,ZMOM,E,OFF,STIFM,STIFR,VISCM,VISCR,MASS,XINER,DT,XL,VX ,RY1,RZ1,RX,RY2,RZ2,FR_WAVE
#endif
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   I n p u t     A r g u m e n t s 
C-----------------------------------------------
      INTEGER ITYP
C-----------------------------------------------
      INTEGER NEL,NUVAR,IPROP,
     .        GET_U_PNU,GET_U_PID,GET_U_MID,GET_U_MNU,
     .        KFUNC,KMAT,KPROP,GET_U_PROC
      my_real
     .   UVAR(NUVAR,*),DT ,
     .   FX(*), FY(*), FZ(*), E(*), VX(*),MASS(*) ,XINER(*),
     .   RY1(*), RZ1(*), OFF(*), XMOM(*), YMOM(*),
     .   ZMOM(*), RX(*), RY2(*), RZ2(*),XL(*),
     .   STIFM(*) ,STIFR(*) , VISCM(*) ,VISCR(*) ,FR_WAVE(*)
C-----------------------------------------------
C   L o c a l   V a r i a b l e s
C-----------------------------------------------
#ifndef ncharline
#define ncharline 500
#endif
      INTEGER IOUT  , LENLINE,itsk
      CHARACTER LINE*ncharline
      INTEGER GET_U_TASK
      EXTERNAL GET_U_TASK
C-----------------------------------------------
C Open the Output File
        itsk=get_u_task()
        IOUT=31*10000+itsk
        OPEN(UNIT=IOUT,STATUS='SCRATCH', FORM='FORMATTED')

      IF (ITYP==29)THEN

       CALL RUSER29(NEL,IOUT   ,IPROP  ,UVAR   ,NUVAR  ,
     2              FX      ,FY      ,FZ     ,XMOM   ,YMOM   ,
     3              ZMOM    ,E       ,OFF    ,STIFM  ,STIFR  ,
     4              VISCM   ,VISCR   ,MASS   ,XINER  ,DT     ,
     5              XL      ,VX      ,RY1    ,RZ1    ,RX     ,
     6              RY2     ,RZ2     ,FR_WAVE ) 

      ELSEIF(ITYP==30)THEN

       CALL RUSER30(NEL,IOUT   ,IPROP  ,UVAR   ,NUVAR  ,
     2              FX      ,FY      ,FZ     ,XMOM   ,YMOM   ,
     3              ZMOM    ,E       ,OFF    ,STIFM  ,STIFR  ,
     4              VISCM   ,VISCR   ,MASS   ,XINER  ,DT     ,
     5              XL      ,VX      ,RY1    ,RZ1    ,RX     ,
     6              RY2     ,RZ2     ,FR_WAVE)

      ELSEIF(ITYP==31)THEN

       CALL RUSER31(NEL,IOUT   ,IPROP  ,UVAR   ,NUVAR  ,
     2              FX      ,FY      ,FZ     ,XMOM   ,YMOM   ,
     3              ZMOM    ,E       ,OFF    ,STIFM  ,STIFR  ,
     4              VISCM   ,VISCR   ,MASS   ,XINER  ,DT     ,
     5              XL      ,VX      ,RY1    ,RZ1    ,RX     ,
     6              RY2     ,RZ2     ,FR_WAVE)
 
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
