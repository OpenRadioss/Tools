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


Csm51i6 Nouvelle routine
Chd|====================================================================
Chd|  LAW_USERSO                    src/usermodules/law_userso.F  
Chd|-- called by -----------
Chd|        LUSER15                       pub/userso/luser15.F          
Chd|        LUSER77                       pub/userso/luser77.F          
Chd|        LUSER54                       pub/userso/luser54.F          
Chd|        LUSER02                       pub/userso/luser02.F          
Chd|        LUSER20                       pub/userso/luser20.F          
Chd|        LUSER89                       pub/userso/luser89.F          
Chd|        LUSER26                       pub/userso/luser26.F          
Chd|        LUSER78                       pub/userso/luser78.F          
Chd|        LUSER67                       pub/userso/luser67.F          
Chd|        LUSER82                       pub/userso/luser82.F          
Chd|        LUSER80                       pub/userso/luser80.F          
Chd|        MULAW                         src/matera/mulaw.F            
Chd|        LUSER43                       pub/userso/luser43.F          
Chd|        LUSER23                       pub/userso/luser23.F          
Chd|        LUSER49                       pub/userso/luser49.F          
Chd|        LUSER14                       pub/userso/luser14.F          
Chd|        LUSER08                       pub/userso/luser08.F          
Chd|        LUSER03                       pub/userso/luser03.F          
Chd|        LUSER90                       pub/userso/luser90.F          
Chd|        LUSER97                       pub/userso/luser97.F          
Chd|        LUSER42                       pub/userso/luser42.F          
Chd|        LUSER60                       pub/userso/luser60.F          
Chd|        LUSER32                       pub/userso/luser32.F          
Chd|        LUSER85                       pub/userso/luser85.F          
Chd|        LUSER29                       pub/userso/luser29.F          
Chd|        LUSER75                       pub/userso/luser75.F          
Chd|        LUSER59                       pub/userso/luser59.F          
Chd|        LUSER13                       pub/userso/luser13.F          
Chd|        LUSER24                       pub/userso/luser24.F          
Chd|        LUSER46                       pub/userso/luser46.F          
Chd|        LUSER98                       pub/userso/luser98.F          
Chd|        LUSER69                       pub/userso/luser69.F          
Chd|        LUSER38                       pub/userso/luser38.F          
Chd|        LUSER09                       pub/userso/luser09.F          
Chd|        LUSER87                       pub/userso/luser87.F          
Chd|        LUSER76                       pub/userso/luser76.F          
Chd|        LUSER64                       pub/userso/luser64.F          
Chd|        LUSER86                       pub/userso/luser86.F          
Chd|        LUSER53                       pub/userso/luser53.F          
Chd|        LUSER45                       pub/userso/luser45.F          
Chd|        LUSER73                       pub/userso/luser73.F          
Chd|        LUSER62                       pub/userso/luser62.F          
Chd|        LUSER37                       pub/userso/luser37.F          
Chd|        LUSER12                       pub/userso/luser12.F          
Chd|        LUSER44                       pub/userso/luser44.F          
Chd|        LUSER88                       pub/userso/luser88.F          
Chd|        LUSER06                       pub/userso/luser06.F          
Chd|        LUSER01                       pub/userso/luser01.F          
Chd|        LUSER10                       pub/userso/luser10.F          
Chd|        LUSER07                       pub/userso/luser07.F          
Chd|        LUSER74                       pub/userso/luser74.F          
Chd|        LUSER63                       pub/userso/luser63.F          
Chd|        LUSER95                       pub/userso/luser95.F          
Chd|        LUSER93                       pub/userso/luser93.F          
Chd|        LUSER36                       pub/userso/luser36.F          
Chd|        LUSER79                       pub/userso/luser79.F          
Chd|        LUSER11                       pub/userso/luser11.F          
Chd|        LUSER57                       pub/userso/luser57.F          
Chd|        LUSER83                       pub/userso/luser83.F          
Chd|        LUSER66                       pub/userso/luser66.F          
Chd|        LUSER33                       pub/userso/luser33.F          
Chd|        LUSER50                       pub/userso/luser50.F          
Chd|        LUSER61                       pub/userso/luser61.F          
Chd|        LUSER96                       pub/userso/luser96.F          
Chd|        LUSER18                       pub/userso/luser18.F          
Chd|        LUSER94                       pub/userso/luser94.F          
Chd|        LUSER04                       pub/userso/luser04.F          
Chd|        LUSER51                       pub/userso/luser51.F          
Chd|        LUSER35                       pub/userso/luser35.F          
Chd|        LUSER30                       pub/userso/luser30.F          
Chd|        LUSER52                       pub/userso/luser52.F          
Chd|        LUSER70                       pub/userso/luser70.F          
Chd|        LUSER19                       pub/userso/luser19.F          
Chd|        LUSER71                       pub/userso/luser71.F          
Chd|        LUSER58                       pub/userso/luser58.F          
Chd|        LUSER21                       pub/userso/luser21.F          
Chd|        LUSER84                       pub/userso/luser84.F          
Chd|        LUSER27                       pub/userso/luser27.F          
Chd|        LUSER48                       pub/userso/luser48.F          
Chd|        LUSER65                       pub/userso/luser65.F          
Chd|        LUSER34                       pub/userso/luser34.F          
Chd|        LUSER91                       pub/userso/luser91.F          
Chd|        LUSER05                       pub/userso/luser05.F          
Chd|        LUSER31                       pub/userso/luser31.F          
Chd|        LUSER41                       pub/userso/luser41.F          
Chd|        LUSER22                       pub/userso/luser22.F          
Chd|        LUSER55                       pub/userso/luser55.F          
Chd|        LUSER28                       pub/userso/luser28.F          
Chd|        LUSER72                       pub/userso/luser72.F          
Chd|        SIGEPS99                      src/user/sigeps99.F           
Chd|        LUSER40                       pub/userso/luser40.F          
Chd|        LUSER56                       pub/userso/luser56.F          
Chd|        LUSER16                       pub/userso/luser16.F          
Chd|        LUSER25                       pub/userso/luser25.F          
Chd|        LUSER81                       pub/userso/luser81.F          
Chd|        LUSER92                       pub/userso/luser92.F          
Chd|        LUSER99                       pub/userso/luser99.F          
Chd|        LUSER39                       pub/userso/luser39.F          
Chd|        LUSER68                       pub/userso/luser68.F          
Chd|        LUSER47                       pub/userso/luser47.F          
Chd|        LUSER17                       pub/userso/luser17.F          
Chd|-- calls ---------------
Chd|====================================================================
      MODULE LAW_USERSO
C-----------------------------------------------
C   D e r i v e d   T y p e   D e f i n i t i o n s
C-----------------------------------------------
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
#include "implicit_f.inc"
C-----------------------------------------------
C   G l o b a l   P a r a m e t e r s
C-----------------------------------------------
#include      "mvsiz_p.inc"
C---------+---------+---+---+--------------------------------------------
C VAR     | SIZE    |TYP| RW| DEFINITION
C---------+---------+---+---+--------------------------------------------
C IPT     |  1      | I | R | LAYER OR INTEGRATION POINT NUMBER   
C IFLAG   |  *      | I | R | GEOMETRICAL FLAGS   
C---------+---------+---+---+--------------------------------------------
C EPSPXX  | NEL     | F | R | STRAIN RATE XX
C EPSPYY  | NEL     | F | R | STRAIN RATE YY
C ...     |         |   |   |
C DEPSXX  | NEL     | F | R | STRAIN INCREMENT XX
C DEPSYY  | NEL     | F | R | STRAIN INCREMENT YY
C ...     |         |   |   |
C EPSXX   | NEL     | F | R | STRAIN XX
C EPSYY   | NEL     | F | R | STRAIN YY
C ...     |         |   |   |
C SIGOXX  | NEL     | F | R | OLD ELASTO PLASTIC STRESS XX 
C SIGOYY  | NEL     | F | R | OLD ELASTO PLASTIC STRESS YY
C ...     |         |   |   |    
C---------+---------+---+---+--------------------------------------------
C SIGNXX  | NEL     | F | W | NEW ELASTO PLASTIC STRESS XX
C SIGNYY  | NEL     | F | W | NEW ELASTO PLASTIC STRESS YY
C ...     |         |   |   |
C SIGVXX  | NEL     | F | W | VISCOUS STRESS XX
C SIGVYY  | NEL     | F | W | VISCOUS STRESS YY
C ...     |         |   |   |
C---------+---------+---+---+--------------------------------------------
C DPLA    | NEL     | F |R/W| INCREMENTAL PLASTIC STRAIN
C---------+---------+---+---+--------------------------------------------
C
      TYPE ULAWINTBUF
      
C integer
        INTEGER  NCYCLE
        INTEGER  ID
        INTEGER  IPTR
        INTEGER  IPTS
        INTEGER  IPTT
C floating
        my_real R11(MVSIZ)
        my_real R12(MVSIZ)
        my_real R13(MVSIZ)
C
        my_real R21(MVSIZ)
        my_real R22(MVSIZ)
        my_real R23(MVSIZ)
C
        my_real R31(MVSIZ)
        my_real R32(MVSIZ)
        my_real R33(MVSIZ)
C
C
        my_real EPSPXX(MVSIZ)
        my_real EPSPYY(MVSIZ)
        my_real EPSPZZ(MVSIZ)
        my_real EPSPXY(MVSIZ)
        my_real EPSPYZ(MVSIZ)
        my_real EPSPZX(MVSIZ)
c
        my_real EPSXX(MVSIZ)
        my_real EPSYY(MVSIZ)
        my_real EPSZZ(MVSIZ)
        my_real EPSXY(MVSIZ)
        my_real EPSYZ(MVSIZ)
        my_real EPSZX(MVSIZ)
C------- when Ismstr=10 we input [F]
        my_real FPSXX(MVSIZ)
        my_real FPSYY(MVSIZ)
        my_real FPSZZ(MVSIZ)
        my_real FPSXY(MVSIZ)
        my_real FPSYZ(MVSIZ)
        my_real FPSZX(MVSIZ)
        my_real FPSYX(MVSIZ)
        my_real FPSZY(MVSIZ)
        my_real FPSXZ(MVSIZ)
C	
        my_real UPSXX(MVSIZ)
        my_real UPSYY(MVSIZ)
        my_real UPSZZ(MVSIZ)
        my_real UPSXY(MVSIZ)
        my_real UPSYZ(MVSIZ)
        my_real UPSXZ(MVSIZ)
C
        my_real DEPSXX(MVSIZ)
        my_real DEPSYY(MVSIZ)
        my_real DEPSZZ(MVSIZ)
        my_real DEPSXY(MVSIZ)
        my_real DEPSYZ(MVSIZ)
        my_real DEPSZX(MVSIZ)
C
        my_real SIGOXX(MVSIZ)
        my_real SIGOYY(MVSIZ)
        my_real SIGOZZ(MVSIZ)
        my_real SIGOXY(MVSIZ)
        my_real SIGOYZ(MVSIZ)
        my_real SIGOZX(MVSIZ)
        
        my_real RHO0(MVSIZ)
        my_real TEMP(MVSIZ)      ! temperature
C-----------------------------------------------
C   O U T P U T   A r g u m e n t s
C----------------------------------------------- 
        my_real SIGNXX(MVSIZ)
        my_real SIGNYY(MVSIZ)
        my_real SIGNZZ(MVSIZ)
        my_real SIGNXY(MVSIZ)
        my_real SIGNYZ(MVSIZ)
        my_real SIGNZX(MVSIZ)
C  
        my_real SIGVXX(MVSIZ)
        my_real SIGVYY(MVSIZ)
        my_real SIGVZZ(MVSIZ)
        my_real SIGVXY(MVSIZ)
        my_real SIGVYZ(MVSIZ)
        my_real SIGVZX(MVSIZ)
    
        my_real DPLA(MVSIZ)
      
       END TYPE ULAWINTBUF
C-----------------------------------------------
C   I N P U T   O U T P U T   A r g u m e n t s 
C-----------------------------------------------
      END MODULE LAW_USERSO
      
