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


Cf51e6 Nouvelle routine
Chd|====================================================================
Chd|  UINTBUF_MOD                   src/usermodules/uintbuf_mod.F 
Chd|-- called by -----------
Chd|        USERINT8                      pub/user/userint8.F           
Chd|        USERINT1                      pub/user/userint1.F           
Chd|        I2RUPT                        src/interf/int2rupt.F         
Chd|        USERINT7                      pub/user/userint7.F           
Chd|        USERINT6                      pub/user/userint6.F           
Chd|        USERINT5                      pub/user/userint5.F           
Chd|        USERINT4                      pub/user/userint4.F           
Chd|        RUPTINT2                      src/interf/ruptint2.F         
Chd|        USERINT3                      pub/user/userint3.F           
Chd|        USERINT9                      pub/user/userint9.F           
Chd|        USERINT2                      pub/user/userint2.F           
Chd|-- calls ---------------
Chd|====================================================================
      MODULE UINTBUF_MOD
C-----------------------------------------------
#include      "implicit_f.inc"
C-----------------------------------------------
C   D e r i v e d   T y p e   D e f i n i t i o n s
C-----------------------------------------------
      TYPE UINTBUF

	INTEGER ISLAVE
        my_real AREA
        my_real DT
        my_real DXN
        my_real DXT
        my_real SIGN
        my_real SIGT
        my_real RUPT
        my_real FACN
        my_real FACT
      END TYPE UINTBUF
C-----
C
      END MODULE UINTBUF_MOD
      
