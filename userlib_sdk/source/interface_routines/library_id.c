//Copyright>
//Copyright> Copyright (C) 1986-2023 Altair Engineering Inc.
//Copyright>
//Copyright> Permission is hereby granted, free of charge, to any person obtaining 
//Copyright> a copy of this software and associated documentation files (the "Software"), 
//Copyright> to deal in the Software without restriction, including without limitation 
//Copyright> the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
//Copyright> sell copies of the Software, and to permit persons to whom the Software is 
//Copyright> furnished to do so, subject to the following conditions:
//Copyright> 
//Copyright> The above copyright notice and this permission notice shall be included in all 
//Copyright> copies or substantial portions of the Software.
//Copyright> 
//Copyright> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
//Copyright> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
//Copyright> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
//Copyright> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
//Copyright> WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
//Copyright> IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//Copyright>


#ifdef _WIN64
#include <process.h>
#endif

#include <stdio.h>
#define _FCALL 

#ifdef MYREAL4
#define my_real real
#endif

#ifdef MYREAL8
#define my_real  double
#endif

#ifdef GCC_COMP
#define TAG 2102011231  
#else
#define TAG 2102011230
#endif


#ifdef _WIN64  

  #ifdef __GNUC__
     __declspec(dllexport) void __cdecl userlib_id(int * version){
        *version=TAG;
     }
  
  #else
     __declspec(dllexport) void userlib_id(int * version){
     *version=TAG;
     }

  #endif
#else   // Linux flavors
   void userlib_id(int * version){
   *version=TAG;
   }    
#endif

