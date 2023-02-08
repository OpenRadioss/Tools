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

#ifdef __GNUC__
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <fcntl.h>


#ifdef MYREAL4
#define my_real float
#endif

#ifdef MYREAL8
#define my_real  double
#endif


/*************/
/*  STARTER  */
/*************/


__declspec(dllexport) void __cdecl ST_LECG (int * igtyp,char * rootn,int* rootlen, int * nuvar,my_real * pargeo)
{
  st_lecg(igtyp,rootn,rootlen, nuvar,pargeo);
}

__declspec(dllexport) void  __cdecl  ST_LECGUSER (int * igtyp,char * rootn,int* rootlen, int * nuvar,my_real * pargeo)
{
   st_lecguser (igtyp,rootn,rootlen,nuvar,pargeo);
}

__declspec(dllexport) void  __cdecl  ST_LECM (int* ilaw ,char * rootn, int* rootlen,my_real* uparam ,int* maxuparam ,int* nuparam,int* nuvar,int* ifunc ,int* maxfunc ,int* mfunc ,my_real* parmat,int* unitab)
{
  st_lecm (ilaw ,rootn,rootlen,uparam ,maxuparam ,nuparam,nuvar,ifunc , maxfunc ,mfunc ,parmat,unitab);
}

__declspec(dllexport) void  __cdecl  ST_LECR (int* irupt ,char * rootn, int* rootlen,my_real* uparam ,int* maxuparam ,int* nuparam,int* nuvar,int* ifunc ,int* maxfunc ,int* mfunc ,int* id)
{
 st_lecr (irupt ,rootn, rootlen,uparam ,maxuparam ,nuparam,nuvar,ifunc ,maxfunc ,mfunc ,id);
}

__declspec(dllexport) void  __cdecl  ST_LECM99 (int * ilaw,char * rootn,int* rootlen, int * iuser_law,my_real * uparam , int * maxuparam, int * nuparam,int * nuvar, int * ifunc,int * maxfunc,int * nfunc, my_real * parmat)
{
 st_lecm99 (ilaw,rootn,rootlen,iuser_law,uparam ,maxuparam, nuparam,nuvar, ifunc,maxfunc, nfunc, parmat);
}

__declspec(dllexport) void  __cdecl  ST_LECSEN (int * typ,char * rootn,int* rootlen)
{
 st_lecsen (typ,rootn,rootlen);
}

__declspec(dllexport) void  __cdecl  ST_RINIUSER (int *igtyp,char * rootn,int* rootlen,int* nel,int* iprop,int * ix,my_real *xl,my_real *mass,my_real *xiner,my_real *stifn,my_real *stifr,my_real *vism  ,my_real *visr,my_real *uvar,int *nuvar)
{
 st_riniuser (igtyp,rootn,rootlen,nel,iprop,ix,xl,mass,xiner,stifn,stifr,vism  ,visr,uvar,nuvar);
}

__declspec(dllexport) void  __cdecl  ST_USERWIS (char * rootn,int* rootlen,int*numnod,int * itab,my_real *x ,my_real *v,my_real *vr,my_real *mass,my_real *iner,int *nuvar ,int *nuvari  ,my_real *uvar ,int *iuvar )
{
   st_userwis (rootn,rootlen,numnod,itab,x ,v,vr,mass,iner,nuvar ,nuvari  ,uvar ,iuvar );
}

__declspec(dllexport) void  __cdecl  ST_USERWIS_INI(char * rootn,int* rootlen,int*iuparam,int*numnod,int * itab,my_real *x ,my_real *v,my_real *vr,my_real *mass,my_real *iner,int *nuvar ,int *nuvari  ,my_real *uvar ,int *iuvar )
{
   st_userwis_ini( rootn, rootlen,iuparam,numnod, itab,x ,v,vr,mass,iner,nuvar ,nuvari ,uvar ,iuvar );
}

__declspec(dllexport) void  __cdecl  ST_SINIUSR ( int *ITYP,char *ROOTN,int *ROOTLEN,
    int *NEL	,int *NUVAR  ,int *IPROP  ,int *IMAT  ,int *SOLID_ID,my_real *TIME  ,my_real * TIMESTEP,
    my_real *EINT   ,my_real *VOL    ,my_real *UVAR   ,my_real *FR_WAVE,my_real *OFF    ,my_real *RHO    ,my_real *SIG    ,
    my_real *XX1    ,my_real *XX2    ,my_real *XX3    ,my_real *XX4    ,my_real *XX5    ,my_real *XX6    ,my_real *XX7    ,my_real *XX8    ,	 
    my_real *YY1    ,my_real *YY2    ,my_real *YY3    ,my_real *YY4    ,my_real *YY5    ,my_real *YY6    ,my_real *YY7    ,my_real *YY8    ,  
    my_real *ZZ1    ,my_real *ZZ2    ,my_real *ZZ3    ,my_real *ZZ4    ,my_real *ZZ5    ,my_real *ZZ6    ,my_real *ZZ7    ,my_real *ZZ8    ,
    my_real *UX1    ,my_real *UX2    ,my_real *UX3    ,my_real *UX4    ,my_real *UX5    ,my_real *UX6    ,my_real *UX7    ,my_real *UX8    ,
    my_real *UY1    ,my_real *UY2    ,my_real *UY3    ,my_real *UY4    ,my_real *UY5    ,my_real *UY6    ,my_real *UY7    ,my_real *UY8    ,
    my_real *UZ1    ,my_real *UZ2    ,my_real *UZ3    ,my_real *UZ4    ,my_real *UZ5    ,my_real *UZ6    ,my_real *UZ7    ,my_real *UZ8    ,
    my_real *VX1    ,my_real *VX2    ,my_real *VX3    ,my_real *VX4    ,my_real *VX5    ,my_real *VX6    ,my_real *VX7    ,my_real *VVX8    ,
    my_real *VY1    ,my_real *VY2    ,my_real *VY3    ,my_real *VY4    ,my_real *VY5    ,my_real *VY6    ,my_real *VY7    ,my_real *VVY8    ,
    my_real *VZ1    ,my_real *VZ2    ,my_real *VZ3    ,my_real *VZ4    ,my_real *VZ5    ,my_real *VZ6    ,my_real *VZ7    ,my_real *VVZ8    ,
    my_real *VRX1   ,my_real *VRX2   ,my_real *VRX3   ,my_real *VRX4   ,my_real *VRX5   ,my_real *VRX6   ,my_real *VRX7   ,my_real *VVRX8   ,
    my_real *VRY1   ,my_real *VRY2   ,my_real *VRY3   ,my_real *VRY4   ,my_real *VRY5   ,my_real *VRY6   ,my_real *VRY7   ,my_real *VVRY8   ,
    my_real *VRZ1   ,my_real *VRZ2   ,my_real *VRZ3   ,my_real *VRZ4   ,my_real *VRZ5   ,my_real *VRZ6   ,my_real *VRZ7   ,my_real *VVRZ8   ,
    my_real *FX1    ,my_real *FX2    ,my_real *FX3    ,my_real *FX4    ,my_real *FX5    ,my_real *FX6    ,my_real *FX7    ,my_real *VFX8    ,
    my_real *FY1    ,my_real *FY2    ,my_real *FY3    ,my_real *FY4    ,my_real *FY5    ,my_real *FY6    ,my_real *FY7    ,my_real *VFY8    ,
    my_real *FZ1    ,my_real *FZ2    ,my_real *FZ3    ,my_real *FZ4    ,my_real *FZ5    ,my_real *FZ6    ,my_real *FZ7    ,my_real *VFZ8    ,
    my_real *MX1    ,my_real *MX2    ,my_real *MX3    ,my_real *MX4    ,my_real *MX5    ,my_real *MX6    ,my_real *MX7    ,my_real *VMX8    ,
    my_real *MY1    ,my_real *MY2    ,my_real *MY3    ,my_real *MY4    ,my_real *MY5    ,my_real *MY6    ,my_real *MY7    ,my_real *MY8    ,
    my_real *MZ1    ,my_real *MZ2    ,my_real *MZ3    ,my_real *MZ4    ,my_real *MZ5    ,my_real *MZ6    ,my_real *MZ7    ,my_real *MZ8    ,
    my_real *STIFM  ,my_real *STIFR  ,my_real *VISCM  ,my_real *VISCR  )
{
  st_siniusr    ( ITYP, ROOTN, ROOTLEN,
                  NEL,NUVAR  ,IPROP  ,IMAT  ,SOLID_ID,TIME  ,TIMESTEP,
                  EINT   ,VOL    ,UVAR   ,FR_WAVE,OFF    ,RHO    ,SIG    ,
                  XX1    ,XX2    ,XX3    ,XX4    ,XX5    ,XX6    ,XX7    ,XX8    ,	 
                  YY1    ,YY2    ,YY3    ,YY4    ,YY5    ,YY6    ,YY7    ,YY8    ,  
                  ZZ1    ,ZZ2    ,ZZ3    ,ZZ4    ,ZZ5    ,ZZ6    ,ZZ7    ,ZZ8    ,
                  UX1    ,UX2    ,UX3    ,UX4    ,UX5    ,UX6    ,UX7    ,UX8    ,
                  UY1    ,UY2    ,UY3    ,UY4    ,UY5    ,UY6    ,UY7    ,UY8    ,
                  UZ1    ,UZ2    ,UZ3    ,UZ4    ,UZ5    ,UZ6    ,UZ7    ,UZ8    ,
                  VX1    ,VX2    ,VX3    ,VX4    ,VX5    ,VX6    ,VX7    ,VVX8    ,
                  VY1    ,VY2    ,VY3    ,VY4    ,VY5    ,VY6    ,VY7    ,VVY8    ,
                  VZ1    ,VZ2    ,VZ3    ,VZ4    ,VZ5    ,VZ6    ,VZ7    ,VVZ8    ,
                  VRX1   ,VRX2   ,VRX3   ,VRX4   ,VRX5   ,VRX6   ,VRX7   ,VVRX8   ,
                  VRY1   ,VRY2   ,VRY3   ,VRY4   ,VRY5   ,VRY6   ,VRY7   ,VVRY8   ,
                  VRZ1   ,VRZ2   ,VRZ3   ,VRZ4   ,VRZ5   ,VRZ6   ,VRZ7   ,VVRZ8   ,
                  FX1    ,FX2    ,FX3    ,FX4    ,FX5    ,FX6    ,FX7    ,VFX8    ,
                  FY1    ,FY2    ,FY3    ,FY4    ,FY5    ,FY6    ,FY7    ,VFY8    ,
                  FZ1    ,FZ2    ,FZ3    ,FZ4    ,FZ5    ,FZ6    ,FZ7    ,VFZ8    ,
                  MX1    ,MX2    ,MX3    ,MX4    ,MX5    ,MX6    ,MX7    ,VMX8    ,
                  MY1    ,MY2    ,MY3    ,MY4    ,MY5    ,MY6    ,MY7    ,MY8    ,
                  MZ1    ,MZ2    ,MZ3    ,MZ4    ,MZ5    ,MZ6    ,MZ7    ,MZ8    ,
                  STIFM  ,STIFR  ,VISCM  ,VISCR  );
}

__declspec(dllexport) void  __cdecl  ST_GET_USERBUF_VAR(int * id, char * title)
{
  st_get_userbuf_var(id,title);
}

/************/
/*  ENGINE  */
/************/

/* ------------ */
/* User Springs */
/* ------------ */
__declspec(dllexport) void  __cdecl  ENG_RUSER (int *ITYP, int *NEL     ,int *IPROP       ,my_real *UVAR   ,int *NUVAR  ,
    		 my_real *FX	  ,my_real *FY      ,my_real *FZ     ,my_real *XMOM   ,my_real *YMOM   ,
    		 my_real *ZMOM    ,my_real *E	    ,my_real *OFF    ,my_real *STIFM  ,my_real *STIFR  ,
    		 my_real *VISCM   ,my_real *VISCR   ,my_real *MASS   ,my_real *XINER  ,my_real *DT     ,
    		 my_real *XL	  ,my_real *VX      ,my_real *RY1    ,my_real *RZ1    ,my_real *RX     ,
    		 my_real *RY2	  ,my_real *RZ2     ,my_real *FR_WAVE) 
{
  eng_ruser (ITYP    , NEL    ,IPROP  ,UVAR   ,NUVAR  ,
    		 FX	     ,FY      ,FZ     ,XMOM   ,YMOM   ,
    		 ZMOM    ,E	      ,OFF    ,STIFM  ,STIFR  ,
    		 VISCM   ,VISCR   ,MASS   ,XINER  ,DT     ,
    		 XL	     ,VX      ,RY1    ,RZ1    ,RX     ,
    		 RY2	 ,RZ2     ,FR_WAVE) ;
}
             

/* ------------------------- */
/* User Law 29-30-31 Solids  */
/* ------------------------- */
__declspec(dllexport) void  __cdecl  ENG_SIGEPS (int* ilaw ,
      int *NEL ,int* NUPARAM ,int* NUVAR ,int* NFUNC ,int* IFUNC ,
      int* NPF ,my_real *TF  ,my_real *TIME , my_real *TIMESTEP, my_real *UPARAM ,my_real *RHO0 ,
      my_real *RHO ,my_real *VOLUME ,my_real *EINT ,my_real *EPSPXX ,my_real *EPSPYY ,my_real *EPSPZZ  ,
      my_real *EPSPXY  ,my_real *EPSPYZ  ,my_real *EPSPZX ,my_real *DEPSXX ,my_real *DEPSYY ,my_real *DEPSZZ  ,
      my_real *DEPSXY  ,my_real *DEPSYZ  ,my_real *DEPSZX ,my_real *EPSXX  ,my_real *EPSYY  ,my_real *EPSZZ   ,
      my_real *EPSXY   ,my_real *EPSYZ   ,my_real *EPSZX  ,
      my_real *IGOXX  ,my_real *SIGOYY ,my_real *SIGOZZ  ,my_real *SIGOXY  ,my_real *SIGOYZ  ,my_real *SIGOZX ,
      my_real *SIGNXX ,my_real *SIGNYY ,my_real *SIGNZZ  ,my_real *SIGNXY  ,my_real *SIGNYZ  ,my_real *SIGNZX ,
      my_real *SIGVXX ,my_real *SIGVYY ,my_real *SIGVZZ  ,my_real *SIGVXY  ,my_real *SIGVYZ  ,my_real *SIGVZX ,
      my_real *SOUNDSP,my_real *VISCMAX,my_real *UVAR    ,my_real *OFF     )
{
 eng_sigeps (ilaw ,
      NEL    ,NUPARAM ,NUVAR  ,NFUNC ,IFUNC ,
      NPF    ,TF      ,TIME   ,TIMESTEP,UPARAM ,RHO0 ,
      RHO    ,VOLUME  ,EINT   ,EPSPXX  ,EPSPYY ,EPSPZZ  ,
      EPSPXY ,EPSPYZ  ,EPSPZX ,DEPSXX  ,DEPSYY ,DEPSZZ  ,
      DEPSXY ,DEPSYZ  ,DEPSZX ,EPSXX   ,EPSYY  ,EPSZZ   ,
      EPSXY  ,EPSYZ   ,EPSZX  ,
      IGOXX  ,SIGOYY  ,SIGOZZ ,SIGOXY  ,SIGOYZ ,SIGOZX ,
      SIGNXX ,SIGNYY  ,SIGNZZ ,SIGNXY  ,SIGNYZ ,SIGNZX ,
      SIGVXX ,SIGVYY  ,SIGVZZ ,SIGVXY  ,SIGVYZ ,SIGVZX ,
      SOUNDSP,VISCMAX ,UVAR   ,OFF     );
}

/* ------------------------- */
/* User Law 29-30-31 Shells  */
/* ------------------------- */
__declspec(dllexport) void  __cdecl  ENG_SIGEPSC(int* ilaw ,
	  int* NEL ,int*NUPARAM ,int*NUVAR ,int*NFUNC ,int*IFUNC ,
      int*NPF  ,int*NPT     ,int*IPT   ,int*IFLAG ,
      my_real *TF ,my_real *TIME ,my_real *TIMESTEP , my_real *UPARAM , my_real *RHO0   ,
      my_real *AREA   ,my_real *EINT   ,my_real *THKLY   ,
      my_real *EPSPXX ,my_real *EPSPYY ,my_real *EPSPXY  ,my_real *EPSPYZ  ,my_real *EPSPZX ,
      my_real *DEPSXX ,my_real *DEPSYY ,my_real *DEPSXY  ,my_real *DEPSYZ  ,my_real *DEPSZX ,
      my_real *EPSXX  ,my_real *EPSYY  ,my_real *EPSXY   ,my_real *EPSYZ   ,my_real *EPSZX  ,
      my_real *SIGOXX ,my_real *SIGOYY ,my_real *SIGOXY  ,my_real *SIGOYZ  ,my_real *SIGOZX ,
      my_real *SIGNXX ,my_real *SIGNYY ,my_real *SIGNXY  ,my_real *SIGNYZ  ,my_real *SIGNZX ,
      my_real *SIGVXX ,my_real *SIGVYY ,my_real *SIGVXY  ,my_real *SIGVYZ  ,my_real *SIGVZX ,
      my_real *SOUNDSP,my_real *VISCMAX,my_real *THK     ,my_real *PLA     ,my_real *UVAR   ,
      my_real *OFF    ,int *NGL    ,int *SHF)
{

 eng_sigepsc(ilaw ,
	  NEL    ,NUPARAM,NUVAR   ,NFUNC ,IFUNC ,
      NPF    ,NPT    ,IPT     ,IFLAG ,
      TF     ,TIME   ,TIMESTEP,UPARAM , RHO0   ,
      AREA   ,EINT   ,THKLY   ,
      EPSPXX ,EPSPYY ,EPSPXY  ,EPSPYZ  ,EPSPZX ,
      DEPSXX ,DEPSYY ,DEPSXY  ,DEPSYZ  ,DEPSZX ,
      EPSXX  ,EPSYY  ,EPSXY   ,EPSYZ   ,EPSZX  ,
      SIGOXX ,SIGOYY ,SIGOXY  ,SIGOYZ  ,SIGOZX ,
      SIGNXX ,SIGNYY ,SIGNXY  ,SIGNYZ  ,SIGNZX ,
      SIGVXX ,SIGVYY ,SIGVXY  ,SIGVYZ  ,SIGVZX ,
      SOUNDSP,VISCMAX,THK     ,PLA     ,UVAR   ,
      OFF    ,NGL    ,SHF);
}

/* ----------------------- */
/* User Law Rupture BRICK  */
/* ----------------------- */
__declspec(dllexport) void  __cdecl  ENG_FLAW (int*IRUP,
     	  int*NEL    ,int*NUPARAM,int*NUVAR   ,int*NFUNC   ,int*IFUNC   ,
     	  int*NPF    ,my_real *TF     ,my_real *TIME   ,my_real *TIMESTEP ,my_real *UPARAM  ,
     	  int*NGL    ,int*IPM	 ,int*NPROPMI,int*MAT,int*IDEL7NOK,
     	  my_real *EPSPXX ,my_real *EPSPYY ,my_real *EPSPZZ ,my_real *EPSPXY,my_real *EPSPYZ,my_real *EPSPZX ,
     	  my_real *EPSXX  ,my_real *EPSYY  ,my_real *EPSZZ  ,my_real *EPSXY ,my_real *EPSYZ ,my_real *EPSZX  ,
     	  my_real *SIGNXX ,my_real *SIGNYY ,my_real *SIGNZZ ,my_real *SIGNXY,my_real *SIGNYZ,my_real *SIGNZX ,
     	  my_real *PLA    ,my_real *DPLA   ,my_real *EPSP   ,my_real *UVAR  ,my_real *OFF   ,
     	  my_real *BIDON1 ,my_real *BIDON2 ,my_real *BIDON3 ,my_real *BIDON4,my_real *BIDON5)
{
      eng_flaw (IRUP,
     	  NEL    ,NUPARAM,NUVAR  ,NFUNC   ,IFUNC   ,
     	  NPF    ,TF     ,TIME   ,TIMESTEP ,UPARAM  ,
     	  NGL    ,IPM	 ,NPROPMI,MAT,IDEL7NOK,
     	  EPSPXX ,EPSPYY ,EPSPZZ ,EPSPXY,EPSPYZ,EPSPZX ,
     	  EPSXX  ,EPSYY  ,EPSZZ  ,EPSXY ,EPSYZ ,EPSZX  ,
     	  SIGNXX ,SIGNYY ,SIGNZZ ,SIGNXY,SIGNYZ,SIGNZX ,
     	  PLA    ,DPLA   ,EPSP   ,UVAR  ,OFF   ,
     	  BIDON1 ,BIDON2 ,BIDON3 ,BIDON4,BIDON5);
}

/* ------------------------ */
/* User Law Rupture SHELL  */
/* ------------------------ */
__declspec(dllexport) void  __cdecl  ENG_FLAWC( int *IRUP,
   	int *NEL   ,int *NUPARAM,int *NUVAR   ,int *NFUNC   ,int *IFUNC  ,int *NPF    ,
   	my_real *TF    ,my_real *TIME	,my_real *TIMESTEP,my_real *UPARAM  , int *NGL   ,int *IPT    ,
   	int *NPT0  ,int *IPM	,int *NPROPMI ,int *MAT   ,
   	my_real *SIGNXX ,my_real *SIGNYY ,my_real *SIGNXY  ,my_real *SIGNYZ  ,my_real *SIGNZX ,
   	my_real *EPSPXX ,my_real *EPSPYY ,my_real *EPSPXY  ,my_real *EPSPYZ  ,my_real *EPSPZX ,
   	my_real *EPSXX  ,my_real *EPSYY  ,my_real *EPSXY   ,my_real *EPSYZ   ,my_real *EPSZX  ,
   	my_real *PLA	,my_real *DPLA   ,my_real *EPSP    ,my_real *UVAR    ,my_real *UEL    , 
   	my_real *OFF	,my_real *BIDON1  ,my_real *BIDON2   ,my_real *BIDON3  ,my_real *BIDON4  ,my_real *BIDON5   )
{
  eng_flawc( IRUP,
   	NEL    ,NUPARAM   ,NUVAR     ,NFUNC   ,IFUNC  ,NPF    ,
   	TF     ,TIME	  ,TIMESTEP  ,UPARAM  ,NGL    ,IPT    ,
   	NPT0   ,IPM	      ,NPROPMI   ,MAT     ,
   	SIGNXX ,SIGNYY    ,SIGNXY    ,SIGNYZ  ,SIGNZX ,
   	EPSPXX ,EPSPYY    ,EPSPXY    ,EPSPYZ  ,EPSPZX ,
   	EPSXX  ,EPSYY     ,EPSXY     ,EPSYZ   ,EPSZX  ,
   	PLA	   ,DPLA      ,EPSP      ,UVAR    ,UEL    , 
   	OFF	   ,BIDON1    ,BIDON2    ,BIDON3  ,BIDON4  ,BIDON5   );
}


/* ---------------------------- */
/* User Laws sigeps99c (Shells) */
/* ---------------------------- */
__declspec(dllexport) void  __cdecl  ENG_SIGEPS99C(int*NEL      ,int*NUPARAM ,int*NUVAR   ,int*ILAW_USER ,int*NFUNC  ,
    	 int*IFUNC    ,int *NPF     ,int*NGL    ,my_real *TF       ,my_real *TIME   ,
    	 my_real *TIMESTEP ,my_real *UPARAM  ,my_real *RHO    ,my_real *AREA	  ,my_real *EINT   ,
    	 my_real *SHF	   ,my_real *SOUNDSP ,my_real *VISCMAX ,my_real *PLA	   ,my_real *UVAR   , 
    	 my_real *OFF	   ,my_real *SIGY  )
{
 eng_sigeps99c( NEL      ,NUPARAM ,NUVAR   ,ILAW_USER ,NFUNC  ,
    	        IFUNC    ,NPF     ,NGL     ,TF        ,TIME   ,
    	        TIMESTEP ,UPARAM  ,RHO     ,AREA	  ,EINT   ,
    	        SHF	     ,SOUNDSP ,VISCMAX ,PLA	      ,UVAR   , 
    	        OFF	     ,SIGY  );
}

/* ------------------------------- */
/* User Law sigeps99c get variables */
/* ------------------------------- */
__declspec(dllexport) void  __cdecl  ENG_GET_LAWC_USER_VAR ( int*NCYCLE, int*IMAT, int*ILAYER, int*NPTA, int*IFLAG,
     				my_real* R11,	 my_real*R12,    my_real*R13,    my_real*R21,    my_real*R22,
     				my_real* R23,	 my_real*R31,    my_real*R32,    my_real*R33,    my_real*SIGOXX,
     				my_real* SIGOYY, my_real*SIGOXY, my_real*SIGOYZ, my_real*SIGOZX, my_real*EPSPXX,
     				my_real* EPSPYY, my_real*EPSPXY, my_real*EPSPYZ, my_real*EPSPZX, my_real*EPSXX,
     				my_real* EPSYY,  my_real*EPSXY,  my_real*EPSYZ,  my_real*EPSZX,  my_real*DEPSXX,
     				my_real* DEPSYY, my_real*DEPSXY, my_real*DEPSYZ, my_real*DEPSZX, my_real*THKLYL,	  
     				my_real* THKN,   my_real*SIGNXX, my_real*SIGNYY, my_real*SIGNXY, my_real*SIGNYZ,
     				my_real* SIGNZX, my_real*SIGVXX, my_real*SIGVYY, my_real*SIGVXY, my_real*SIGVYZ,
     				my_real* SIGVZX, my_real*DPLA ){
                    
                     eng_get_lawc_user_var( 
                            NCYCLE, IMAT,   ILAYER, NPTA, IFLAG,
     			   	        R11,	R12,    R13,    R21,    R22,
     				        R23,	R31,    R32,    R33,    SIGOXX,
     				        SIGOYY, SIGOXY, SIGOYZ, SIGOZX, EPSPXX,
     				        EPSPYY, EPSPXY, EPSPYZ, EPSPZX, EPSXX,
     				        EPSYY,  EPSXY,  EPSYZ,  EPSZX,  DEPSXX,
     				        DEPSYY, DEPSXY, DEPSYZ, DEPSZX, THKLYL,	  
     				        THKN,   SIGNXX, SIGNYY, SIGNXY, SIGNYZ,
     				        SIGNZX, SIGVXX, SIGVYY, SIGVXY, SIGVYZ,
     				        SIGVZX, DPLA );
                    }

/* --------------------------------- */
/* User Law sigeps99c get variables 2*/
/* --------------------------------- */
__declspec(dllexport) void  __cdecl ENG_GET_LAWC_USER_VAR_2(
         my_real* VAR01,int *SIZVAR01,my_real* VAR02,int *SIZVAR02,
         my_real* VAR03,int *SIZVAR03,my_real* VAR04,int *SIZVAR04,my_real* VAR05,int *SIZVAR05,my_real* VAR06,int * SIZVAR06,
         my_real* VAR07,int *SIZVAR07,my_real* VAR08,int *SIZVAR08,my_real* VAR09,int *SIZVAR09,my_real* VAR10,int * SIZVAR10,
         my_real* VAR11,int *SIZVAR11,my_real* VAR12,int *SIZVAR12,my_real* VAR13,int *SIZVAR13,my_real* VAR14,int * SIZVAR14,
         my_real* VAR15,int *SIZVAR15,my_real* VAR16,int *SIZVAR16,my_real* VAR17,int *SIZVAR17,my_real* VAR18,int * SIZVAR18,    
         my_real* VAR19,int *SIZVAR19,my_real* VAR20,int *SIZVAR20,my_real* VAR21,int *SIZVAR21,my_real* VAR22,int * SIZVAR22,
         my_real* VAR23,int *SIZVAR23,my_real* VAR24,int *SIZVAR24,my_real* VAR25,int *SIZVAR25,my_real* VAR26,int * SIZVAR26,    
         my_real* VAR27,int *SIZVAR27,my_real* VAR28,int *SIZVAR28,my_real* VAR29,int *SIZVAR29,my_real* VAR30,int * SIZVAR30,
         my_real* VAR31,int *SIZVAR31,my_real* VAR32,int *SIZVAR32,my_real* VAR33,int *SIZVAR33,my_real* VAR34,int * SIZVAR34,    
         my_real* VAR35,int *SIZVAR35,my_real* VAR36,int *SIZVAR36,my_real* VAR37,int *SIZVAR37,my_real* VAR38,int * SIZVAR38,
         my_real* VAR39,int *SIZVAR39,my_real* VAR40,int *SIZVAR40,my_real* VAR41,int *SIZVAR41,my_real* VAR42,int * SIZVAR42,    
         my_real* VAR43,int *SIZVAR43,my_real* VAR44,int *SIZVAR44,my_real* VAR45,int *SIZVAR45,my_real* VAR46,int * SIZVAR46,
         my_real* VAR47,int *SIZVAR47,my_real* VAR48,int *SIZVAR48,my_real* VAR49,int *SIZVAR49,my_real* VAR50,int * SIZVAR50,    
         my_real* VAR51,int *SIZVAR51,my_real* VAR52,int *SIZVAR52,my_real* VAR53,int *SIZVAR53,my_real* VAR54,int * SIZVAR54,
         my_real* VAR55,int *SIZVAR55,my_real* VAR56,int *SIZVAR56,my_real* VAR57,int *SIZVAR57,my_real* VAR58,int * SIZVAR58,    
         my_real* VAR59,int *SIZVAR59,my_real* VAR60,int *SIZVAR60,my_real* VAR61,int *SIZVAR61,my_real* VAR62,int * SIZVAR62,
         my_real* VAR63,int *SIZVAR63,my_real* VAR64,int *SIZVAR64,my_real* VAR65,int *SIZVAR65,my_real* VAR66,int * SIZVAR66,    
         my_real* VAR67,int *SIZVAR67,my_real* VAR68,int *SIZVAR68,my_real* VAR69,int *SIZVAR69,my_real* VAR70,int * SIZVAR70,
         my_real* VAR71,int *SIZVAR72,my_real* VAR73,int *SIZVAR73,my_real* VAR74,int *SIZVAR74,my_real* VAR75,int * SIZVAR75,
         my_real* VAR76,int *SIZVAR76,my_real* VAR77,int *SIZVAR77,my_real* VAR78,int *SIZVAR78,my_real* VAR79,int * SIZVAR79,
         my_real* VAR80,int *SIZVAR80,my_real* VAR81,int *SIZVAR81,my_real* VAR82,int *SIZVAR82,my_real* VAR83,int * SIZVAR83,    
         my_real* VAR84,int *SIZVAR84,my_real* VAR85,int *SIZVAR85,my_real* VAR86,int *SIZVAR86,my_real* VAR87,int * SIZVAR87,
         my_real* VAR88,int *SIZVAR88,my_real* VAR89,int *SIZVAR89,my_real* VAR90,int *SIZVAR90,my_real* VAR91,int * SIZVAR91,    
         my_real* VAR92,int *SIZVAR92,my_real* VAR93,int *SIZVAR93,my_real* VAR94,int *SIZVAR94,my_real* VAR95,int * SIZVAR95,
         my_real* VAR96,int *SIZVAR96,my_real* VAR97,int *SIZVAR97,my_real* VAR98,int *SIZVAR98,my_real* VAR99,int * SIZVAR99){
         
             eng_get_lawc_user_var_2(    VAR01,SIZVAR01,VAR02,SIZVAR02,
         VAR03,SIZVAR03, VAR04,SIZVAR04, VAR05,SIZVAR05,VAR06,SIZVAR06,
         VAR07,SIZVAR07, VAR08,SIZVAR08, VAR09,SIZVAR09,VAR10,SIZVAR10,
         VAR11,SIZVAR11, VAR12,SIZVAR12, VAR13,SIZVAR13,VAR14,SIZVAR14,
         VAR15,SIZVAR15, VAR16,SIZVAR16, VAR17,SIZVAR17,VAR18,SIZVAR18,    
         VAR19,SIZVAR19, VAR20,SIZVAR20, VAR21,SIZVAR21,VAR22,SIZVAR22,
         VAR23,SIZVAR23, VAR24,SIZVAR24, VAR25,SIZVAR25,VAR26,SIZVAR26,    
         VAR27,SIZVAR27, VAR28,SIZVAR28, VAR29,SIZVAR29,VAR30,SIZVAR30,
         VAR31,SIZVAR31, VAR32,SIZVAR32, VAR33,SIZVAR33,VAR34,SIZVAR34,    
         VAR35,SIZVAR35, VAR36,SIZVAR36, VAR37,SIZVAR37,VAR38,SIZVAR38,
         VAR39,SIZVAR39, VAR40,SIZVAR40, VAR41,SIZVAR41,VAR42,SIZVAR42,    
         VAR43,SIZVAR43, VAR44,SIZVAR44, VAR45,SIZVAR45,VAR46,SIZVAR46,
         VAR47,SIZVAR47, VAR48,SIZVAR48, VAR49,SIZVAR49,VAR50,SIZVAR50,    
         VAR51,SIZVAR51, VAR52,SIZVAR52, VAR53,SIZVAR53,VAR54,SIZVAR54,
         VAR55,SIZVAR55, VAR56,SIZVAR56, VAR57,SIZVAR57,VAR58,SIZVAR58,    
         VAR59,SIZVAR59, VAR60,SIZVAR60, VAR61,SIZVAR61,VAR62,SIZVAR62,
         VAR63,SIZVAR63, VAR64,SIZVAR64, VAR65,SIZVAR65,VAR66,SIZVAR66,    
         VAR67,SIZVAR67, VAR68,SIZVAR68, VAR69,SIZVAR69,VAR70,SIZVAR70,
         VAR71,SIZVAR72, VAR73,SIZVAR73, VAR74,SIZVAR74,VAR75,SIZVAR75,
         VAR76,SIZVAR76, VAR77,SIZVAR77, VAR78,SIZVAR78,VAR79,SIZVAR79,
         VAR80,SIZVAR80, VAR81,SIZVAR81, VAR82,SIZVAR82,VAR83,SIZVAR83,    
         VAR84,SIZVAR84, VAR85,SIZVAR85, VAR86,SIZVAR86,VAR87,SIZVAR87,
         VAR88,SIZVAR88, VAR89,SIZVAR89, VAR90,SIZVAR90,VAR91,SIZVAR91,    
         VAR92,SIZVAR92, VAR93,SIZVAR93, VAR94,SIZVAR94,VAR95,SIZVAR95,
         VAR96,SIZVAR96, VAR97,SIZVAR97, VAR98,SIZVAR98,VAR99,SIZVAR99);

         }
/* ----------------------------------- */
/* User Law sigeps99 copy back results */
/* ----------------------------------- */
__declspec(dllexport) void  __cdecl ENG_SET_LAWC_USER_VAR (
                    my_real*SIGNXX,  my_real*SIGNYY, my_real*SIGNXY, my_real* SIGNYZ,  my_real*SIGNZX,
     				my_real* SIGVXX, my_real*SIGVYY, my_real*SIGVXY, my_real*SIGVYZ,   my_real*SIGVZX,
     				my_real* DPLA,   my_real*ETSE,   my_real* THKN ) {
                    
                    eng_set_lawc_user_var ( SIGNXX,  SIGNYY, SIGNXY, SIGNYZ,  SIGNZX,
     				SIGVXX, SIGVYY, SIGVXY, SIGVYZ, SIGVZX,
     				DPLA,   ETSE,   THKN );
                    
                    }

__declspec(dllexport) void  __cdecl ENG_SET_LAWC_USER_VAR_2 (    my_real* VAR01,int*SIZVAR01,my_real* VAR02,int*SIZVAR02,
         my_real* VAR03,int*SIZVAR03,my_real* VAR04,int*SIZVAR04,my_real* VAR05,int*SIZVAR05,my_real* VAR06,int*SIZVAR06,
         my_real* VAR07,int*SIZVAR07,my_real* VAR08,int*SIZVAR08,my_real* VAR09,int*SIZVAR09,my_real* VAR10,int*SIZVAR10,
         my_real* VAR11,int*SIZVAR11,my_real* VAR12,int*SIZVAR12,my_real* VAR13,int*SIZVAR13,my_real* VAR14,int*SIZVAR14,
         my_real* VAR15,int*SIZVAR15,my_real* VAR16,int*SIZVAR16,my_real* VAR17,int*SIZVAR17,my_real* VAR18,int*SIZVAR18,    
         my_real* VAR19,int*SIZVAR19,my_real* VAR20,int*SIZVAR20,my_real* VAR21,int*SIZVAR21,my_real* VAR22,int*SIZVAR22,
         my_real* VAR23,int*SIZVAR23,my_real* VAR24,int*SIZVAR24,my_real* VAR25,int*SIZVAR25,my_real* VAR26,int*SIZVAR26,    
         my_real* VAR27,int*SIZVAR27,my_real* VAR28,int*SIZVAR28,my_real* VAR29,int*SIZVAR29,my_real* VAR30,int*SIZVAR30,
         my_real* VAR31,int*SIZVAR31,my_real* VAR32,int*SIZVAR32,my_real* VAR33,int*SIZVAR33,my_real* VAR34,int*SIZVAR34,    
         my_real* VAR35,int*SIZVAR35,my_real* VAR36,int*SIZVAR36,my_real* VAR37,int*SIZVAR37,my_real* VAR38,int*SIZVAR38,
         my_real* VAR39,int*SIZVAR39,my_real* VAR40,int*SIZVAR40,my_real* VAR41,int*SIZVAR41,my_real* VAR42,int*SIZVAR42,    
         my_real* VAR43,int*SIZVAR43,my_real* VAR44,int*SIZVAR44,my_real* VAR45,int*SIZVAR45,my_real* VAR46,int*SIZVAR46,
         my_real* VAR47,int*SIZVAR47,my_real* VAR48,int*SIZVAR48,my_real* VAR49,int*SIZVAR49,my_real* VAR50,int*SIZVAR50,    
         my_real* VAR51,int*SIZVAR51,my_real* VAR52,int*SIZVAR52,my_real* VAR53,int*SIZVAR53,my_real* VAR54,int*SIZVAR54,
         my_real* VAR55,int*SIZVAR55,my_real* VAR56,int*SIZVAR56,my_real* VAR57,int*SIZVAR57,my_real* VAR58,int*SIZVAR58,    
         my_real* VAR59,int*SIZVAR59,my_real* VAR60,int*SIZVAR60,my_real* VAR61,int*SIZVAR61,my_real* VAR62,int*SIZVAR62,
         my_real* VAR63,int*SIZVAR63,my_real* VAR64,int*SIZVAR64,my_real* VAR65,int*SIZVAR65,my_real* VAR66,int*SIZVAR66,    
         my_real* VAR67,int*SIZVAR67,my_real* VAR68,int*SIZVAR68,my_real* VAR69,int*SIZVAR69,my_real* VAR70,int*SIZVAR70,
         my_real* VAR71,int*SIZVAR72,my_real* VAR73,int*SIZVAR73,my_real* VAR74,int*SIZVAR74,my_real* VAR75,int*SIZVAR75,
         my_real* VAR76,int*SIZVAR76,my_real* VAR77,int*SIZVAR77,my_real* VAR78,int*SIZVAR78,my_real* VAR79,int*SIZVAR79,
         my_real* VAR80,int*SIZVAR80,my_real* VAR81,int*SIZVAR81,my_real* VAR82,int*SIZVAR82,my_real* VAR83,int*SIZVAR83,    
         my_real* VAR84,int*SIZVAR84,my_real* VAR85,int*SIZVAR85,my_real* VAR86,int*SIZVAR86,my_real* VAR87,int*SIZVAR87,
         my_real* VAR88,int*SIZVAR88,my_real* VAR89,int*SIZVAR89,my_real* VAR90,int*SIZVAR90,my_real* VAR91,int*SIZVAR91,    
         my_real* VAR92,int*SIZVAR92,my_real* VAR93,int*SIZVAR93,my_real* VAR94,int*SIZVAR94,my_real* VAR95,int*SIZVAR95,
         my_real* VAR96,int*SIZVAR96,my_real* VAR97,int*SIZVAR97,my_real* VAR98,int*SIZVAR98,my_real* VAR99,int*SIZVAR99){
         
          eng_set_lawc_user_var_2   (     VAR01,SIZVAR01, VAR02,SIZVAR02,
          VAR03,SIZVAR03, VAR04,SIZVAR04, VAR05,SIZVAR05, VAR06,SIZVAR06,
          VAR07,SIZVAR07, VAR08,SIZVAR08, VAR09,SIZVAR09, VAR10,SIZVAR10,
          VAR11,SIZVAR11, VAR12,SIZVAR12, VAR13,SIZVAR13, VAR14,SIZVAR14,
          VAR15,SIZVAR15, VAR16,SIZVAR16, VAR17,SIZVAR17, VAR18,SIZVAR18,    
          VAR19,SIZVAR19, VAR20,SIZVAR20, VAR21,SIZVAR21, VAR22,SIZVAR22,
          VAR23,SIZVAR23, VAR24,SIZVAR24, VAR25,SIZVAR25, VAR26,SIZVAR26,    
          VAR27,SIZVAR27, VAR28,SIZVAR28, VAR29,SIZVAR29, VAR30,SIZVAR30,
          VAR31,SIZVAR31, VAR32,SIZVAR32, VAR33,SIZVAR33, VAR34,SIZVAR34,    
          VAR35,SIZVAR35, VAR36,SIZVAR36, VAR37,SIZVAR37, VAR38,SIZVAR38,
          VAR39,SIZVAR39, VAR40,SIZVAR40, VAR41,SIZVAR41, VAR42,SIZVAR42,    
          VAR43,SIZVAR43, VAR44,SIZVAR44, VAR45,SIZVAR45, VAR46,SIZVAR46,
          VAR47,SIZVAR47, VAR48,SIZVAR48, VAR49,SIZVAR49, VAR50,SIZVAR50,    
          VAR51,SIZVAR51, VAR52,SIZVAR52, VAR53,SIZVAR53, VAR54,SIZVAR54,
          VAR55,SIZVAR55, VAR56,SIZVAR56, VAR57,SIZVAR57, VAR58,SIZVAR58,    
          VAR59,SIZVAR59, VAR60,SIZVAR60, VAR61,SIZVAR61, VAR62,SIZVAR62,
          VAR63,SIZVAR63, VAR64,SIZVAR64, VAR65,SIZVAR65, VAR66,SIZVAR66,    
          VAR67,SIZVAR67, VAR68,SIZVAR68, VAR69,SIZVAR69, VAR70,SIZVAR70,
          VAR71,SIZVAR72, VAR73,SIZVAR73, VAR74,SIZVAR74, VAR75,SIZVAR75,
          VAR76,SIZVAR76, VAR77,SIZVAR77, VAR78,SIZVAR78, VAR79,SIZVAR79,
          VAR80,SIZVAR80, VAR81,SIZVAR81, VAR82,SIZVAR82, VAR83,SIZVAR83,    
          VAR84,SIZVAR84, VAR85,SIZVAR85, VAR86,SIZVAR86, VAR87,SIZVAR87,
          VAR88,SIZVAR88, VAR89,SIZVAR89, VAR90,SIZVAR90, VAR91,SIZVAR91,    
          VAR92,SIZVAR92, VAR93,SIZVAR93, VAR94,SIZVAR94, VAR95,SIZVAR95,
          VAR96,SIZVAR96, VAR97,SIZVAR97, VAR98,SIZVAR98, VAR99,SIZVAR99);

         
         }

/* ---------------------------- */
/* User Laws sigeps99  (Solids) */
/* ---------------------------- */
__declspec(dllexport) void  __cdecl ENG_SIGEPS99(
    	 int*NEL	 ,int*NUPARAM     ,int*NUVAR      ,int*ILAW_USER  ,int*NFUNC   ,
    	 int*IFUNC       ,int*NPF	  ,my_real*TF	  ,my_real*TIME   ,my_real*TIMESTEP,
    	 my_real*UPARAM  ,my_real*RHO	  ,my_real*VOLUME ,my_real*EINT   ,int*NGL    ,
    	 my_real*SOUNDSP ,my_real*VISCMAX ,my_real*UVAR   ,my_real*OFF	  ,my_real*SIGY   ,
    	 my_real*PLA  ){
         
         eng_sigeps99(
    	 NEL	 ,NUPARAM ,NUVAR  ,ILAW_USER  ,NFUNC   ,
    	 IFUNC   ,NPF	  ,TF	  ,TIME       ,TIMESTEP,
    	 UPARAM  ,RHO	  ,VOLUME ,EINT       ,NGL    ,
    	 SOUNDSP ,VISCMAX ,UVAR   ,OFF	      ,SIGY   ,
    	 PLA  );
         }

__declspec(dllexport) void  __cdecl ENG_GET_LAW_USER_VAR(  int*NCYCLE, int*IMAT, int*IPTR, int*IPTS, int*IPTT,
    	                       my_real*UR11,my_real*R12, my_real*R13, my_real*R21, my_real*R22, my_real*R23,  my_real*R31,
    	                       my_real*UR32,my_real*R33, my_real*SO1, my_real*SO2, my_real*SO3, my_real*SO4,  my_real*SO5,
    	                       my_real*SO6, my_real*EP1, my_real*EP2, my_real*EP3, my_real*EP4, my_real*EP5,  my_real*EP6,
    	                       my_real*ES1, my_real*ES2, my_real*ES3, my_real*ES4, my_real*ES5, my_real*ES6,  my_real*DE1,
    	                       my_real*DE2, my_real*DE3, my_real*DE4, my_real*DE5, my_real*DE6, my_real*RHO0, my_real*S1,
    	                       my_real*S2,  my_real*S3,  my_real*S4,  my_real*S5,  my_real*S6,  my_real*SV1,  my_real*SV2,
    			               my_real*SV3, my_real*SV4, my_real*SV5, my_real*SV6 ){
                               
                               eng_get_law_user_var(  NCYCLE, IMAT, IPTR, IPTS, IPTT,
    	                       UR11,R12, R13, R21, R22, R23,  R31,
    	                       UR32,R33, SO1, SO2, SO3, SO4,  SO5,
    	                       SO6, EP1, EP2, EP3, EP4, EP5,  EP6,
    	                       ES1, ES2, ES3, ES4, ES5, ES6,  DE1,
    	                       DE2, DE3, DE4, DE5, DE6, RHO0, S1,
    	                       S2,  S3,  S4,  S5,  S6,  SV1,  SV2,
    			               SV3, SV4, SV5, SV6 );
                               }

                               
__declspec(dllexport) void  __cdecl ENG_GET_LAW_USER_VAR_2     ( my_real*FPSXX,int *SIZFPSXX,my_real*FPSYY,int *SIZFPSYY,
         my_real*FPSZZ,int *SIZFPSZZ,my_real*FPSXY,int *SIZFPSXY,my_real*FPSYZ,int *SIZFPSYZ,my_real*FPSZX,int *SIZFPSZX,
         my_real*FPSYX,int *SIZFPSYX,my_real*FPSZY,int *SIZFPSZY,my_real*FPSXZ,int *SIZFPSXZ,my_real*VAR10,int *SIZVAR10,
         my_real*VAR11,int *SIZVAR11,my_real*VAR12,int *SIZVAR12,my_real*VAR13,int *SIZVAR13,my_real*VAR14,int *SIZVAR14,
         my_real*VAR15,int *SIZVAR15,my_real*VAR16,int *SIZVAR16,my_real*VAR17,int *SIZVAR17,my_real*VAR18,int *SIZVAR18,    
         my_real*VAR19,int *SIZVAR19,my_real*VAR20,int *SIZVAR20,my_real*VAR21,int *SIZVAR21,my_real*VAR22,int *SIZVAR22,
         my_real*VAR23,int *SIZVAR23,my_real*VAR24,int *SIZVAR24,my_real*VAR25,int *SIZVAR25,my_real*VAR26,int *SIZVAR26,    
         my_real*VAR27,int *SIZVAR27,my_real*VAR28,int *SIZVAR28,my_real*VAR29,int *SIZVAR29,my_real*VAR30,int *SIZVAR30,
         my_real*VAR31,int *SIZVAR31,my_real*VAR32,int *SIZVAR32,my_real*VAR33,int *SIZVAR33,my_real*VAR34,int *SIZVAR34,    
         my_real*VAR35,int *SIZVAR35,my_real*VAR36,int *SIZVAR36,my_real*VAR37,int *SIZVAR37,my_real*VAR38,int *SIZVAR38,
         my_real*VAR39,int *SIZVAR39,my_real*VAR40,int *SIZVAR40,my_real*VAR41,int *SIZVAR41,my_real*VAR42,int *SIZVAR42,    
         my_real*VAR43,int *SIZVAR43,my_real*VAR44,int *SIZVAR44,my_real*VAR45,int *SIZVAR45,my_real*VAR46,int *SIZVAR46,
         my_real*VAR47,int *SIZVAR47,my_real*VAR48,int *SIZVAR48,my_real*VAR49,int *SIZVAR49,my_real*VAR50,int *SIZVAR50,    
         my_real*VAR51,int *SIZVAR51,my_real*VAR52,int *SIZVAR52,my_real*VAR53,int *SIZVAR53,my_real*VAR54,int *SIZVAR54,
         my_real*VAR55,int *SIZVAR55,my_real*VAR56,int *SIZVAR56,my_real*VAR57,int *SIZVAR57,my_real*VAR58,int *SIZVAR58,    
         my_real*VAR59,int *SIZVAR59,my_real*VAR60,int *SIZVAR60,my_real*VAR61,int *SIZVAR61,my_real*VAR62,int *SIZVAR62,
         my_real*VAR63,int *SIZVAR63,my_real*VAR64,int *SIZVAR64,my_real*VAR65,int *SIZVAR65,my_real*VAR66,int *SIZVAR66,    
         my_real*VAR67,int *SIZVAR67,my_real*VAR68,int *SIZVAR68,my_real*VAR69,int *SIZVAR69,my_real*VAR70,int *SIZVAR70,
         my_real*VAR71,int *SIZVAR72,my_real*VAR73,int *SIZVAR73,my_real*VAR74,int *SIZVAR74,my_real*VAR75,int *SIZVAR75,
         my_real*VAR76,int *SIZVAR76,my_real*VAR77,int *SIZVAR77,my_real*VAR78,int *SIZVAR78,my_real*VAR79,int *SIZVAR79,
         my_real*VAR80,int *SIZVAR80,my_real*VAR81,int *SIZVAR81,my_real*VAR82,int *SIZVAR82,my_real*VAR83,int *SIZVAR83,    
         my_real*VAR84,int *SIZVAR84,my_real*VAR85,int *SIZVAR85,my_real*VAR86,int *SIZVAR86,my_real*VAR87,int *SIZVAR87,
         my_real*VAR88,int *SIZVAR88,my_real*VAR89,int *SIZVAR89,my_real*VAR90,int *SIZVAR90,my_real*VAR91,int *SIZVAR91,    
         my_real*VAR92,int *SIZVAR92,my_real*VAR93,int *SIZVAR93,my_real*VAR94,int *SIZVAR94,my_real*VAR95,int *SIZVAR95,
         my_real*VAR96,int *SIZVAR96,my_real*VAR97,int *SIZVAR97,my_real*VAR98,int *SIZVAR98,my_real*VAR99,int *SIZVAR99){
         
         eng_get_law_user_var_2    (   FPSXX,SIZFPSXX,FPSYY,SIZFPSYY,
         FPSZZ,SIZFPSZZ,FPSXY,SIZFPSXY,FPSYZ,SIZFPSYZ,FPSZX,SIZFPSZX,
         FPSYX,SIZFPSYX,FPSZY,SIZFPSZY,FPSXZ,SIZFPSXZ,VAR10,SIZVAR10,
         VAR11,SIZVAR11,VAR12,SIZVAR12,VAR13,SIZVAR13,VAR14,SIZVAR14,
         VAR15,SIZVAR15,VAR16,SIZVAR16,VAR17,SIZVAR17,VAR18,SIZVAR18,    
         VAR19,SIZVAR19,VAR20,SIZVAR20,VAR21,SIZVAR21,VAR22,SIZVAR22,
         VAR23,SIZVAR23,VAR24,SIZVAR24,VAR25,SIZVAR25,VAR26,SIZVAR26,    
         VAR27,SIZVAR27,VAR28,SIZVAR28,VAR29,SIZVAR29,VAR30,SIZVAR30,
         VAR31,SIZVAR31,VAR32,SIZVAR32,VAR33,SIZVAR33,VAR34,SIZVAR34,    
         VAR35,SIZVAR35,VAR36,SIZVAR36,VAR37,SIZVAR37,VAR38,SIZVAR38,
         VAR39,SIZVAR39,VAR40,SIZVAR40,VAR41,SIZVAR41,VAR42,SIZVAR42,    
         VAR43,SIZVAR43,VAR44,SIZVAR44,VAR45,SIZVAR45,VAR46,SIZVAR46,
         VAR47,SIZVAR47,VAR48,SIZVAR48,VAR49,SIZVAR49,VAR50,SIZVAR50,    
         VAR51,SIZVAR51,VAR52,SIZVAR52,VAR53,SIZVAR53,VAR54,SIZVAR54,
         VAR55,SIZVAR55,VAR56,SIZVAR56,VAR57,SIZVAR57,VAR58,SIZVAR58,    
         VAR59,SIZVAR59,VAR60,SIZVAR60,VAR61,SIZVAR61,VAR62,SIZVAR62,
         VAR63,SIZVAR63,VAR64,SIZVAR64,VAR65,SIZVAR65,VAR66,SIZVAR66,    
         VAR67,SIZVAR67,VAR68,SIZVAR68,VAR69,SIZVAR69,VAR70,SIZVAR70,
         VAR71,SIZVAR72,VAR73,SIZVAR73,VAR74,SIZVAR74,VAR75,SIZVAR75,
         VAR76,SIZVAR76,VAR77,SIZVAR77,VAR78,SIZVAR78,VAR79,SIZVAR79,
         VAR80,SIZVAR80,VAR81,SIZVAR81,VAR82,SIZVAR82,VAR83,SIZVAR83,    
         VAR84,SIZVAR84,VAR85,SIZVAR85,VAR86,SIZVAR86,VAR87,SIZVAR87,
         VAR88,SIZVAR88,VAR89,SIZVAR89,VAR90,SIZVAR90,VAR91,SIZVAR91,    
         VAR92,SIZVAR92,VAR93,SIZVAR93,VAR94,SIZVAR94,VAR95,SIZVAR95,
         VAR96,SIZVAR96,VAR97,SIZVAR97,VAR98,SIZVAR98,VAR99,SIZVAR99);
   
         }

         
__declspec(dllexport) void  __cdecl ENG_SET_LAW_USER_VAR (  
                               my_real*S1,  my_real*S2,   my_real*S3,  my_real*S4,  my_real*S5,  my_real*S6,
                               my_real*SV1, my_real*SV2,  my_real*SV3, my_real*SV4, my_real*SV5, my_real*SV6,
                               my_real*DPLA ){
                               
                               eng_set_law_user_var (  
                               S1,  S2,   S3,  S4,  S5,  S6,
                               SV1, SV2,  SV3, SV4, SV5, SV6,
                               DPLA );
                               }

__declspec(dllexport) void  __cdecl  ENG_SET_LAW_USER_VAR_2 (   my_real*VAR01,int *SIZVAR01,my_real*VAR02,int *SIZVAR02,
         my_real*VAR03,int *SIZVAR03,my_real*VAR04,int *SIZVAR04,my_real*VAR05,int *SIZVAR05,my_real*VAR06,int *SIZVAR06,
         my_real*VAR07,int *SIZVAR07,my_real*VAR08,int *SIZVAR08,my_real*VAR09,int *SIZVAR09,my_real*VAR10,int *SIZVAR10,
         my_real*VAR11,int *SIZVAR11,my_real*VAR12,int *SIZVAR12,my_real*VAR13,int *SIZVAR13,my_real*VAR14,int *SIZVAR14,
         my_real*VAR15,int *SIZVAR15,my_real*VAR16,int *SIZVAR16,my_real*VAR17,int *SIZVAR17,my_real*VAR18,int *SIZVAR18,    
         my_real*VAR19,int *SIZVAR19,my_real*VAR20,int *SIZVAR20,my_real*VAR21,int *SIZVAR21,my_real*VAR22,int *SIZVAR22,
         my_real*VAR23,int *SIZVAR23,my_real*VAR24,int *SIZVAR24,my_real*VAR25,int *SIZVAR25,my_real*VAR26,int *SIZVAR26,    
         my_real*VAR27,int *SIZVAR27,my_real*VAR28,int *SIZVAR28,my_real*VAR29,int *SIZVAR29,my_real*VAR30,int *SIZVAR30,
         my_real*VAR31,int *SIZVAR31,my_real*VAR32,int *SIZVAR32,my_real*VAR33,int *SIZVAR33,my_real*VAR34,int *SIZVAR34,    
         my_real*VAR35,int *SIZVAR35,my_real*VAR36,int *SIZVAR36,my_real*VAR37,int *SIZVAR37,my_real*VAR38,int *SIZVAR38,
         my_real*VAR39,int *SIZVAR39,my_real*VAR40,int *SIZVAR40,my_real*VAR41,int *SIZVAR41,my_real*VAR42,int *SIZVAR42,    
         my_real*VAR43,int *SIZVAR43,my_real*VAR44,int *SIZVAR44,my_real*VAR45,int *SIZVAR45,my_real*VAR46,int *SIZVAR46,
         my_real*VAR47,int *SIZVAR47,my_real*VAR48,int *SIZVAR48,my_real*VAR49,int *SIZVAR49,my_real*VAR50,int *SIZVAR50,    
         my_real*VAR51,int *SIZVAR51,my_real*VAR52,int *SIZVAR52,my_real*VAR53,int *SIZVAR53,my_real*VAR54,int *SIZVAR54,
         my_real*VAR55,int *SIZVAR55,my_real*VAR56,int *SIZVAR56,my_real*VAR57,int *SIZVAR57,my_real*VAR58,int *SIZVAR58,    
         my_real*VAR59,int *SIZVAR59,my_real*VAR60,int *SIZVAR60,my_real*VAR61,int *SIZVAR61,my_real*VAR62,int *SIZVAR62,
         my_real*VAR63,int *SIZVAR63,my_real*VAR64,int *SIZVAR64,my_real*VAR65,int *SIZVAR65,my_real*VAR66,int *SIZVAR66,    
         my_real*VAR67,int *SIZVAR67,my_real*VAR68,int *SIZVAR68,my_real*VAR69,int *SIZVAR69,my_real*VAR70,int *SIZVAR70,
         my_real*VAR71,int *SIZVAR72,my_real*VAR73,int *SIZVAR73,my_real*VAR74,int *SIZVAR74,my_real*VAR75,int *SIZVAR75,
         my_real*VAR76,int *SIZVAR76,my_real*VAR77,int *SIZVAR77,my_real*VAR78,int *SIZVAR78,my_real*VAR79,int *SIZVAR79,
         my_real*VAR80,int *SIZVAR80,my_real*VAR81,int *SIZVAR81,my_real*VAR82,int *SIZVAR82,my_real*VAR83,int *SIZVAR83,    
         my_real*VAR84,int *SIZVAR84,my_real*VAR85,int *SIZVAR85,my_real*VAR86,int *SIZVAR86,my_real*VAR87,int *SIZVAR87,
         my_real*VAR88,int *SIZVAR88,my_real*VAR89,int *SIZVAR89,my_real*VAR90,int *SIZVAR90,my_real*VAR91,int *SIZVAR91,    
         my_real*VAR92,int *SIZVAR92,my_real*VAR93,int *SIZVAR93,my_real*VAR94,int *SIZVAR94,my_real*VAR95,int *SIZVAR95,
         my_real*VAR96,int *SIZVAR96,my_real*VAR97,int *SIZVAR97,my_real*VAR98,int *SIZVAR98,my_real*VAR99,int *SIZVAR99){


              eng_set_law_user_var_2 ( VAR01,SIZVAR01,VAR02,SIZVAR02,
         VAR03,SIZVAR03,VAR04,SIZVAR04,VAR05,SIZVAR05,VAR06,SIZVAR06,
         VAR07,SIZVAR07,VAR08,SIZVAR08,VAR09,SIZVAR09,VAR10,SIZVAR10,
         VAR11,SIZVAR11,VAR12,SIZVAR12,VAR13,SIZVAR13,VAR14,SIZVAR14,
         VAR15,SIZVAR15,VAR16,SIZVAR16,VAR17,SIZVAR17,VAR18,SIZVAR18,    
         VAR19,SIZVAR19,VAR20,SIZVAR20,VAR21,SIZVAR21,VAR22,SIZVAR22,
         VAR23,SIZVAR23,VAR24,SIZVAR24,VAR25,SIZVAR25,VAR26,SIZVAR26,    
         VAR27,SIZVAR27,VAR28,SIZVAR28,VAR29,SIZVAR29,VAR30,SIZVAR30,
         VAR31,SIZVAR31,VAR32,SIZVAR32,VAR33,SIZVAR33,VAR34,SIZVAR34,    
         VAR35,SIZVAR35,VAR36,SIZVAR36,VAR37,SIZVAR37,VAR38,SIZVAR38,
         VAR39,SIZVAR39,VAR40,SIZVAR40,VAR41,SIZVAR41,VAR42,SIZVAR42,    
         VAR43,SIZVAR43,VAR44,SIZVAR44,VAR45,SIZVAR45,VAR46,SIZVAR46,
         VAR47,SIZVAR47,VAR48,SIZVAR48,VAR49,SIZVAR49,VAR50,SIZVAR50,    
         VAR51,SIZVAR51,VAR52,SIZVAR52,VAR53,SIZVAR53,VAR54,SIZVAR54,
         VAR55,SIZVAR55,VAR56,SIZVAR56,VAR57,SIZVAR57,VAR58,SIZVAR58,    
         VAR59,SIZVAR59,VAR60,SIZVAR60,VAR61,SIZVAR61,VAR62,SIZVAR62,
         VAR63,SIZVAR63,VAR64,SIZVAR64,VAR65,SIZVAR65,VAR66,SIZVAR66,    
         VAR67,SIZVAR67,VAR68,SIZVAR68,VAR69,SIZVAR69,VAR70,SIZVAR70,
         VAR71,SIZVAR72,VAR73,SIZVAR73,VAR74,SIZVAR74,VAR75,SIZVAR75,
         VAR76,SIZVAR76,VAR77,SIZVAR77,VAR78,SIZVAR78,VAR79,SIZVAR79,
         VAR80,SIZVAR80,VAR81,SIZVAR81,VAR82,SIZVAR82,VAR83,SIZVAR83,    
         VAR84,SIZVAR84,VAR85,SIZVAR85,VAR86,SIZVAR86,VAR87,SIZVAR87,
         VAR88,SIZVAR88,VAR89,SIZVAR89,VAR90,SIZVAR90,VAR91,SIZVAR91,    
         VAR92,SIZVAR92,VAR93,SIZVAR93,VAR94,SIZVAR94,VAR95,SIZVAR95,
         VAR96,SIZVAR96,VAR97,SIZVAR97,VAR98,SIZVAR98,VAR99,SIZVAR99);         
         }

/* ------------ */
/* User springs */
/* ------------ */
__declspec(dllexport) void  __cdecl  ENG_SUSER(int*ITYP,
      int*NEL	 ,int*NUVAR   ,int*IPROP  ,int*IMAT  ,int*SOLID_ID,my_real *TIME  ,my_real *TIMESTEP,
      my_real *EINT   ,my_real *VOL    ,my_real *UVAR   ,my_real *FR_WAVE,my_real *OFF    ,my_real *RHO    ,my_real *SIG    ,
      my_real *XX1    ,my_real *XX2    ,my_real *XX3    ,my_real *XX4    ,my_real *XX5    ,my_real *XX6    ,my_real *XX7    ,my_real *XX8    ,     
      my_real *YY1    ,my_real *YY2    ,my_real *YY3    ,my_real *YY4    ,my_real *YY5    ,my_real *YY6    ,my_real *YY7    ,my_real *YY8    ,  
      my_real *ZZ1    ,my_real *ZZ2    ,my_real *ZZ3    ,my_real *ZZ4    ,my_real *ZZ5    ,my_real *ZZ6    ,my_real *ZZ7    ,my_real *ZZ8    ,
      my_real *UX1    ,my_real *UX2    ,my_real *UX3    ,my_real *UX4    ,my_real *UX5    ,my_real *UX6    ,my_real *UX7    ,my_real *UX8    ,
      my_real *UY1    ,my_real *UY2    ,my_real *UY3    ,my_real *UY4    ,my_real *UY5    ,my_real *UY6    ,my_real *UY7    ,my_real *UY8    ,
      my_real *UZ1    ,my_real *UZ2    ,my_real *UZ3    ,my_real *UZ4    ,my_real *UZ5    ,my_real *UZ6    ,my_real *UZ7    ,my_real *UZ8    ,
      my_real *VX1    ,my_real *VX2    ,my_real *VX3    ,my_real *VX4    ,my_real *VX5    ,my_real *VX6    ,my_real *VX7    ,my_real *VX8    ,
      my_real *VY1    ,my_real *VY2    ,my_real *VY3    ,my_real *VY4    ,my_real *VY5    ,my_real *VY6    ,my_real *VY7    ,my_real *VY8    ,
      my_real *VZ1    ,my_real *VZ2    ,my_real *VZ3    ,my_real *VZ4    ,my_real *VZ5    ,my_real *VZ6    ,my_real *VZ7    ,my_real *VZ8    ,
      my_real *VRX1   ,my_real *VRX2   ,my_real *VRX3   ,my_real *VRX4   ,my_real *VRX5   ,my_real *VRX6   ,my_real *VRX7   ,my_real *VRX8   ,
      my_real *VRY1   ,my_real *VRY2   ,my_real *VRY3   ,my_real *VRY4   ,my_real *VRY5   ,my_real *VRY6   ,my_real *VRY7   ,my_real *VRY8   ,
      my_real *VRZ1   ,my_real *VRZ2   ,my_real *VRZ3   ,my_real *VRZ4   ,my_real *VRZ5   ,my_real *VRZ6   ,my_real *VRZ7   ,my_real *VRZ8   ,
      my_real *FX1    ,my_real *FX2    ,my_real *FX3    ,my_real *FX4    ,my_real *FX5    ,my_real *FX6    ,my_real *FX7    ,my_real *FX8    ,
      my_real *FY1    ,my_real *FY2    ,my_real *FY3    ,my_real *FY4    ,my_real *FY5    ,my_real *FY6    ,my_real *FY7    ,my_real *FY8    ,
      my_real *FZ1    ,my_real *FZ2    ,my_real *FZ3    ,my_real *FZ4    ,my_real *FZ5    ,my_real *FZ6    ,my_real *FZ7    ,my_real *FZ8    ,
      my_real * MX1    ,my_real *MX2   ,my_real *MX3    ,my_real *MX4    ,my_real *MX5    ,my_real *MX6    ,my_real *MX7    ,my_real *MX8    ,
      my_real *MY1    ,my_real *MY2    ,my_real *MY3    ,my_real *MY4    ,my_real *MY5    ,my_real *MY6    ,my_real *MY7    ,my_real *MY8    ,
      my_real *MZ1    ,my_real *MZ2    ,my_real *MZ3    ,my_real *MZ4    ,my_real *MZ5    ,my_real *MZ6    ,my_real *MZ7    ,my_real *MZ8    ,
      my_real *STIFM  ,my_real *STIFR  ,my_real *VISCM  ,my_real *VISCR  ){

     eng_suser(ITYP,
      NEL	 ,NUVAR  ,IPROP  ,IMAT  ,SOLID_ID,TIME  ,TIMESTEP,
      EINT   ,VOL    ,UVAR   ,FR_WAVE,OFF    ,RHO    ,SIG    ,
      XX1    ,XX2    ,XX3    ,XX4    ,XX5    ,XX6    ,XX7    ,XX8    ,     
      YY1    ,YY2    ,YY3    ,YY4    ,YY5    ,YY6    ,YY7    ,YY8    ,  
      ZZ1    ,ZZ2    ,ZZ3    ,ZZ4    ,ZZ5    ,ZZ6    ,ZZ7    ,ZZ8    ,
      UX1    ,UX2    ,UX3    ,UX4    ,UX5    ,UX6    ,UX7    ,UX8    ,
      UY1    ,UY2    ,UY3    ,UY4    ,UY5    ,UY6    ,UY7    ,UY8    ,
      UZ1    ,UZ2    ,UZ3    ,UZ4    ,UZ5    ,UZ6    ,UZ7    ,UZ8    ,
      VX1    ,VX2    ,VX3    ,VX4    ,VX5    ,VX6    ,VX7    ,VX8    ,
      VY1    ,VY2    ,VY3    ,VY4    ,VY5    ,VY6    ,VY7    ,VY8    ,
      VZ1    ,VZ2    ,VZ3    ,VZ4    ,VZ5    ,VZ6    ,VZ7    ,VZ8    ,
      VRX1   ,VRX2   ,VRX3   ,VRX4   ,VRX5   ,VRX6   ,VRX7   ,VRX8   ,
      VRY1   ,VRY2   ,VRY3   ,VRY4   ,VRY5   ,VRY6   ,VRY7   ,VRY8   ,
      VRZ1   ,VRZ2   ,VRZ3   ,VRZ4   ,VRZ5   ,VRZ6   ,VRZ7   ,VRZ8   ,
      FX1    ,FX2    ,FX3    ,FX4    ,FX5    ,FX6    ,FX7    ,FX8    ,
      FY1    ,FY2    ,FY3    ,FY4    ,FY5    ,FY6    ,FY7    ,FY8    ,
      FZ1    ,FZ2    ,FZ3    ,FZ4    ,FZ5    ,FZ6    ,FZ7    ,FZ8    ,
      MX1    ,MX2    ,MX3    ,MX4    ,MX5    ,MX6    ,MX7    ,MX8    ,
      MY1    ,MY2    ,MY3    ,MY4    ,MY5    ,MY6    ,MY7    ,MY8    ,
      MZ1    ,MZ2    ,MZ3    ,MZ4    ,MZ5    ,MZ6    ,MZ7    ,MZ8    ,
      STIFM  ,STIFR  ,VISCM  ,VISCR  );
      }
/* ------------------------- */
/* T2 INTERFACE USER RUPTURE */
/* ------------------------- */
__declspec(dllexport) void  __cdecl ENG_USERINT(int *IGTYP, int *NSN ,int *II ,int *PID ,int *NUVAR ,my_real * UVAR  ){
        eng_userint(IGTYP, NSN  ,II  ,PID  ,NUVAR,  UVAR  );
  }

__declspec(dllexport) void  __cdecl ENG_GET_UINTBUF_VAR(int *ISLAVE, my_real *AREA, my_real *DT,my_real *DXN,my_real *DXT,my_real *SIGN,my_real *SIGT,
                           my_real *RUPT, my_real *FACN, my_real *FACT ){
                             eng_get_uintbuf_var (ISLAVE, AREA, DT, DXN, DXT, SIGN, SIGT,
                                                    RUPT, FACN, FACT );
}                           
                           
__declspec(dllexport) void  __cdecl ENG_USERWI(
            char *ROOTN ,int *ROOTLEN ,
     		int *NUVAR  ,int *NUVARI ,int *NUMNOD ,
     		int *NCYCLE ,int *LENWA  ,int *IUVAR  ,int *ITAB   ,my_real *TT     ,
     		my_real *DT1	,my_real *DT2	 ,my_real *USREINT,my_real *EXWORK ,my_real *UVAR   ,
     		my_real *D	,my_real *X	 ,my_real *V	  ,my_real *VR     ,my_real *MASS   ,
     		my_real *INER	,my_real *STIFN  ,my_real *STIFR  ,my_real *A	   ,my_real *AR     ,
     		my_real *WA	){
              eng_userwi (ROOTN  ,ROOTLEN ,
     		              NUVAR  ,NUVARI  ,NUMNOD ,
     		              NCYCLE ,LENWA   ,IUVAR  ,ITAB   ,TT     ,
     		              DT1    ,DT2     ,USREINT,EXWORK ,UVAR   ,
     		              D      ,X       ,V      ,VR     ,MASS   ,
     		              INER	 ,STIFN   ,STIFR  ,A      ,AR     ,
     		              WA  );
        }
        

__declspec(dllexport) void  __cdecl ENG_USER_SENS(int *TYP,int *ID) {
           eng_user_sens (TYP,ID);
         }

#endif

#endif