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
Chd|  LAW_USER                      src/usermodules1/law_user.F   
Chd|-- called by -----------
Chd|        LECMUSER08                    pub/userl1/lecmuser08.F       
Chd|        LECMUSER75                    pub/userl1/lecmuser75.F       
Chd|        LECMUSER76                    pub/userl1/lecmuser76.F       
Chd|        LECMUSER95                    pub/userl1/lecmuser95.F       
Chd|        LECMUSER79                    pub/userl1/lecmuser79.F       
Chd|        LECMUSER26                    pub/userl1/lecmuser26.F       
Chd|        LECMUSER16                    pub/userl1/lecmuser16.F       
Chd|        LECMUSER33                    pub/userl1/lecmuser33.F       
Chd|        LECMUSER46                    pub/userl1/lecmuser46.F       
Chd|        LECMUSER61                    pub/userl1/lecmuser61.F       
Chd|        LECMUSER58                    pub/userl1/lecmuser58.F       
Chd|        LECMUSER99                    pub/userl1/lecmuser99.F       
Chd|        LECMUSER86                    pub/userl1/lecmuser86.F       
Chd|        LECMUSER31                    pub/userl1/lecmuser31.F       
Chd|        LECMUSER04                    pub/userl1/lecmuser04.F       
Chd|        LECMUSER39                    pub/userl1/lecmuser39.F       
Chd|        LECMUSER98                    pub/userl1/lecmuser98.F       
Chd|        LECMUSER68                    pub/userl1/lecmuser68.F       
Chd|        LECMUSER01                    pub/userl1/lecmuser01.F       
Chd|        LECMUSER72                    pub/userl1/lecmuser72.F       
Chd|        LECMUSER92                    pub/userl1/lecmuser92.F       
Chd|        LECMUSER51                    pub/userl1/lecmuser51.F       
Chd|        LECMUSER42                    pub/userl1/lecmuser42.F       
Chd|        LECMUSER87                    pub/userl1/lecmuser87.F       
Chd|        LECMUSER38                    pub/userl1/lecmuser38.F       
Chd|        LECMUSER29                    pub/userl1/lecmuser29.F       
Chd|        LECMUSER54                    pub/userl1/lecmuser54.F       
Chd|        LECMUSER15                    pub/userl1/lecmuser15.F       
Chd|        LECMUSER25                    pub/userl1/lecmuser25.F       
Chd|        LECMUSER07                    pub/userl1/lecmuser07.F       
Chd|        LECMUSER12                    pub/userl1/lecmuser12.F       
Chd|        LECMUSER36                    pub/userl1/lecmuser36.F       
Chd|        LECMUSER22                    pub/userl1/lecmuser22.F       
Chd|        LECMUSER96                    pub/userl1/lecmuser96.F       
Chd|        LECMUSER49                    pub/userl1/lecmuser49.F       
Chd|        LECMUSER45                    pub/userl1/lecmuser45.F       
Chd|        LECMUSER70                    pub/userl1/lecmuser70.F       
Chd|        LECMUSER32                    pub/userl1/lecmuser32.F       
Chd|        LECMUSER80                    pub/userl1/lecmuser80.F       
Chd|        LECMUSER21                    pub/userl1/lecmuser21.F       
Chd|        LECMUSER30                    pub/userl1/lecmuser30.F       
Chd|        LECMUSER37                    pub/userl1/lecmuser37.F       
Chd|        LECMUSER41                    pub/userl1/lecmuser41.F       
Chd|        LECMUSER83                    pub/userl1/lecmuser83.F       
Chd|        LECMUSER64                    pub/userl1/lecmuser64.F       
Chd|        LECMUSER19                    pub/userl1/lecmuser19.F       
Chd|        LECMUSER71                    pub/userl1/lecmuser71.F       
Chd|        LECMUSER74                    pub/userl1/lecmuser74.F       
Chd|        LECMUSER35                    pub/userl1/lecmuser35.F       
Chd|        LECMUSER53                    pub/userl1/lecmuser53.F       
Chd|        LECMUSER84                    pub/userl1/lecmuser84.F       
Chd|        LECMUSER63                    pub/userl1/lecmuser63.F       
Chd|        LECMUSER48                    pub/userl1/lecmuser48.F       
Chd|        LECMUSER11                    pub/userl1/lecmuser11.F       
Chd|        LECMUSER67                    pub/userl1/lecmuser67.F       
Chd|        LECMUSER60                    pub/userl1/lecmuser60.F       
Chd|        LECMUSER06                    pub/userl1/lecmuser06.F       
Chd|        LECMUSER56                    pub/userl1/lecmuser56.F       
Chd|        LECMUSER28                    pub/userl1/lecmuser28.F       
Chd|        LECMAT                        src/mater1/lecmat.F           
Chd|        LECMUSER09                    pub/userl1/lecmuser09.F       
Chd|        LECMUSER50                    pub/userl1/lecmuser50.F       
Chd|        LECMUSER89                    pub/userl1/lecmuser89.F       
Chd|        LECMUSER57                    pub/userl1/lecmuser57.F       
Chd|        LECMUSER78                    pub/userl1/lecmuser78.F       
Chd|        LECMUSER93                    pub/userl1/lecmuser93.F       
Chd|        LECMUSER66                    pub/userl1/lecmuser66.F       
Chd|        LECMUSER44                    pub/userl1/lecmuser44.F       
Chd|        LECMUSER18                    pub/userl1/lecmuser18.F       
Chd|        LECMUSER24                    pub/userl1/lecmuser24.F       
Chd|        LECMUSER81                    pub/userl1/lecmuser81.F       
Chd|        LECMUSER62                    pub/userl1/lecmuser62.F       
Chd|        LECMUSER20                    pub/userl1/lecmuser20.F       
Chd|        LECMUSER85                    pub/userl1/lecmuser85.F       
Chd|        LECMUSER47                    pub/userl1/lecmuser47.F       
Chd|        LECMUSER73                    pub/userl1/lecmuser73.F       
Chd|        LECMUSER27                    pub/userl1/lecmuser27.F       
Chd|        LECMUSER55                    pub/userl1/lecmuser55.F       
Chd|        LECMUSER03                    pub/userl1/lecmuser03.F       
Chd|        LECMUSER34                    pub/userl1/lecmuser34.F       
Chd|        LECMUSER40                    pub/userl1/lecmuser40.F       
Chd|        LECMUSER13                    pub/userl1/lecmuser13.F       
Chd|        LECM99                        src/user1/lecm99.F            
Chd|        LECMUSER90                    pub/userl1/lecmuser90.F       
Chd|        LECMUSER59                    pub/userl1/lecmuser59.F       
Chd|        LECMUSER05                    pub/userl1/lecmuser05.F       
Chd|        LECMUSER69                    pub/userl1/lecmuser69.F       
Chd|        LECMUSER14                    pub/userl1/lecmuser14.F       
Chd|        LECMUSER88                    pub/userl1/lecmuser88.F       
Chd|        LECMUSER91                    pub/userl1/lecmuser91.F       
Chd|        LECMUSER97                    pub/userl1/lecmuser97.F       
Chd|        LECMUSER43                    pub/userl1/lecmuser43.F       
Chd|        LECMUSER77                    pub/userl1/lecmuser77.F       
Chd|        LECMUSER                      src/mater1/lecmuser.F         
Chd|        LECMUSER82                    pub/userl1/lecmuser82.F       
Chd|        LECMUSER52                    pub/userl1/lecmuser52.F       
Chd|        LECMUSER17                    pub/userl1/lecmuser17.F       
Chd|        LECMUSER02                    pub/userl1/lecmuser02.F       
Chd|        LECMUSER10                    pub/userl1/lecmuser10.F       
Chd|        LECMUSER23                    pub/userl1/lecmuser23.F       
Chd|        LECMUSER94                    pub/userl1/lecmuser94.F       
Chd|        LECMUSER65                    pub/userl1/lecmuser65.F       
Chd|-- calls ---------------
Chd|====================================================================
      MODULE LAW_USER
C-----------------------------------------------
C   D e r i v e d   T y p e   D e f i n i t i o n s
C-----------------------------------------------
C-----------------------------------------------
C   I m p l i c i t   T y p e s
C-----------------------------------------------
C-----------------------------------------------
C   G l o b a l   P a r a m e t e r s
C-----------------------------------------------
C---------+---------+---+---+--------------------------------------------
C VAR     | SIZE    |TYP| RW| DEFINITION
C---------+---------+---+---+--------------------------------------------
C IMAT    |     1   | I | R | MATERIAL ID
C---------+---------+---+---+--------------------------------------------
C NAME    |   100   | C | R | MATERIAL NAME
C---------+---------+---+---+--------------------------------------------
C ...     |         |   |   |
C---------+---------+---+---+--------------------------------------------
C---------+---------+---+---+--------------------------------------------
C
      TYPE ULAWBUF
C-----------------------------------------------
C   I N P U T   A r g u m e n t s
C-----------------------------------------------
C integer
        INTEGER   ID
C character
        CHARACTER NAME*500
C-----------------------------------------------
C   O U T P U T   A r g u m e n t s
C-----------------------------------------------
C
C-----------------------------------------------
       END TYPE ULAWBUF

C-----------------------------------------------
C   I N P U T   O U T P U T   A r g u m e n t s
C-----------------------------------------------
      END MODULE LAW_USER

