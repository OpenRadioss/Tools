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
Chd|  ST_GET_USERBUF_VAR                        src/user1/lecm99.F            
Chd|-- called by -----------
Chd|        LECMUSER                      src/mater1/lecmuser.F         
Chd|-- calls ---------------
Chd|====================================================================
      SUBROUTINE ENG_GET_UINTBUF_VAR(ISLAVE, AREA, DT,DXN,DXT,SIGN,SIGT,
     *                              RUPT, FACN, FACT )
#ifdef _WIN64
!DEC$ ATTRIBUTES DLLEXPORT, DECORATE, ALIAS : "ENG_GET_UINTBUF_VAR" :: ENG_GET_UINTBUF_VAR
!DEC$ ATTRIBUTES REFERENCE :: ISLAVE, AREA, DT,DXN,DXT,SIGN,SIGT,RUPT, FACN, FACT 
#endif
C-----------------------------------------------
      USE UINTBUF_USE_MOD
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   D u m m y   A r g u m e n t s
C-----------------------------------------------
	INTEGER ISLAVE
        my_real AREA, DT, DXN, DXT, SIGN, SIGT,
     *          RUPT,FACN,FACT

         UINTBUF_VAR%ISLAVE = ISLAVE
         UINTBUF_VAR%AREA   = AREA
         UINTBUF_VAR%DT     = DT
         UINTBUF_VAR%DXN    = DXN
         UINTBUF_VAR%DXT    = DXT
         UINTBUF_VAR%SIGN   = SIGN
         UINTBUF_VAR%SIGT   = SIGT
         UINTBUF_VAR%RUPT   = RUPT
         UINTBUF_VAR%FACN   = FACN
         UINTBUF_VAR%FACT   = FACT
      END
