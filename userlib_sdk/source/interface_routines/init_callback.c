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


#ifdef MYREAL4
#define my_real float
#endif

#ifdef MYREAL8
#define my_real  double
#endif


#ifdef _WIN64
#include <process.h>
#include <stdio.h>
#define _FCALL 

int (*get_u_numtable_p)(int * tid);
int _FCALL GET_U_NUMTABLE(int * tid){
 int res;
 res = get_u_numtable_p(tid);
 return res;
}
int get_u_numtable(int * tid){
 int res;
 res = get_u_numtable_p(tid);
 return res;
}


void (*get_u_table_p)(int * itable,my_real *XX, my_real *YY);
void _FCALL GET_U_TABLE(int * itable,my_real *XX, my_real *YY){
 get_u_table_p(itable,XX,YY);
}
void get_u_table(int * itable,my_real *XX, my_real *YY){
 get_u_table_p(itable,XX,YY);
}


void (*get_u_vtable_p)(int * itable, int * nel0, int * ipos,my_real *XX, my_real*YY, my_real *DYDX1);
void _FCALL GET_U_VTABLE(int * itable, int * nel0, int * ipos,my_real *XX, my_real*YY, my_real *DYDX1){
  get_u_vtable_p(itable,nel0,ipos,XX,YY,DYDX1);
}
void get_u_vtable(int * itable, int * nel0, int * ipos,my_real *XX, my_real*YY, my_real *DYDX1){
  get_u_vtable_p(itable,nel0,ipos,XX,YY,DYDX1);
}


void (*set_u_shlplas_p)(int *USRNEL,my_real *SIGY,my_real *ETSE);
void _FCALL SET_U_SHLPLAS(int *USRNEL,my_real *SIGY,my_real *ETSE){
 set_u_shlplas_p(USRNEL,SIGY,ETSE);
}
void set_u_shlplas(int *USRNEL,my_real *SIGY,my_real *ETSE){
 set_u_shlplas_p(USRNEL,SIGY,ETSE);
}


void (*set_u_solplas_p)(int *USRNEL,my_real *SIGY,my_real *PLA);
void _FCALL SET_U_SOLPLAS(int *USRNEL, my_real*SIGY, my_real*PLA){
 set_u_solplas_p(USRNEL,SIGY,PLA);
}
void set_u_solplas(int *USRNEL, my_real*SIGY, my_real*PLA){
 set_u_solplas_p(USRNEL,SIGY,PLA);
}


void (*usens_shift_ab_p)(my_real * sensor);
void _FCALL USENS_SHIFT_AB(my_real * sensor){
 usens_shift_ab_p(sensor);
}
void usens_shift_ab(my_real * sensor){
 usens_shift_ab_p(sensor);
}


void (*usens_shift_ba_p)(my_real * sensor);
void _FCALL USENS_SHIFT_BA(my_real * sensor){
 usens_shift_ba_p(sensor);
}
void usens_shift_ba(my_real * sensor){
 usens_shift_ba_p(sensor);
}


int (*get_u_numsens_p)(int * idsens);
int _FCALL GET_U_NUMSENS (int * idsens) {
 int res;
 res = get_u_numsens_p(idsens);
 return res;
}
int get_u_numsens (int * idsens) {
 int res;
 res = get_u_numsens_p(idsens);
 return res;
}


int (*get_u_sens_id_p)(int * idsens);
int _FCALL GET_U_SENS_ID (int * idsens){
 int res;
 res = get_u_sens_id_p(idsens);
 return res;
}
int get_u_sens_id(int * idsens){
 int res;
 res = get_u_sens_id_p(idsens);
 return res;
}


int (*set_u_sens_value_p)(int * nsens, int * ivar, my_real * var);
int _FCALL SET_U_SENS_VALUE(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = set_u_sens_value_p(nsens,ivar,var);
 return res;
}
int set_u_sens_value(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = set_u_sens_value_p(nsens,ivar,var);
 return res;
}


int (*get_u_sens_value_p)(int * nsens, int * ivar, my_real * var);
int _FCALL GET_U_SENS_VALUE(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = get_u_sens_value_p(nsens,ivar,var);
 return res;
}
int get_u_sens_value(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = get_u_sens_value_p(nsens,ivar,var);
 return res;
}


int (*set_u_sens_maxvalue_p)(int * nsens, int * ivar, my_real * var);
int _FCALL SET_U_SENS_MAXVALUE(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = set_u_sens_maxvalue_p(nsens,ivar,var);
 return res;
}
int set_u_sens_maxvalue(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = set_u_sens_maxvalue_p(nsens,ivar,var);
 return res;
}


int (*get_u_sens_fpar_p)(int * nsens, int * ivar, my_real * var);
int _FCALL GET_U_SENS_FPAR(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = get_u_sens_fpar_p(nsens,ivar,var);
 return res;
}
int get_u_sens_fpar(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = get_u_sens_fpar_p(nsens,ivar,var);
 return res;
}

int (*get_u_sens_ipar_p)(int * nsens, int * ivar, my_real * var);
int _FCALL GET_U_SENS_IPAR(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = get_u_sens_ipar_p(nsens,ivar,var);
 return res;
}
int get_u_sens_ipar(int *nsens, int * ivar, my_real * var ) {
 int res;
 res = get_u_sens_ipar_p(nsens,ivar,var);
 return res;
}


int (*set_u_sens_acti_p)(int * nsens);
int _FCALL SET_U_SENS_ACTI(int *nsens) {
 int res;
 res = set_u_sens_acti_p(nsens);
 return res;
}
int set_u_sens_acti(int *nsens) {
 int res;
 res = set_u_sens_acti_p(nsens);
 return res;
}

int (*get_u_sens_acti_p)(int * nsens);
int _FCALL GET_U_SENS_ACTI(int *nsens) {
 int res;
 res = get_u_sens_acti_p(nsens);
 return res;
}
int get_u_sens_acti(int *nsens) {
 int res;
 res = get_u_sens_acti_p(nsens);
 return res;
}


my_real  (*get_u_sens_p)(int * usens);
my_real _FCALL GET_U_SENS(int *usens) {
 my_real res;
 res = get_u_sens_p(usens);
 return res;
}
my_real get_u_sens(int *usens) {
 my_real res;
 res = get_u_sens_p(usens);
 return res;
}


my_real  (*get_u_sens_delay_p)(int * usens);
my_real _FCALL GET_U_SENS_DELAY(int *usens) {
 my_real res;
 res = get_u_sens_delay_p(usens);
 return res;
}
my_real get_u_sens_delay(int *usens) {
 my_real res;
 res = get_u_sens_delay_p(usens);
 return res;
}


my_real  (*get_u_mat_p)(int * ivar,int * im);
my_real _FCALL GET_U_MAT(int *ivar, int * im) {
 my_real res;
 res = get_u_mat_p(ivar,im);
 return res;
}
my_real get_u_mat(int *ivar, int * im) {
 my_real res;
 res = get_u_mat_p(ivar,im);
 return res;
}


my_real  (*get_u_geo_p)(int * ivar,int * ip);
my_real _FCALL GET_U_GEO(int *ivar, int * ip) {
 my_real res;
 res = get_u_geo_p(ivar,ip);
 return res;
}
my_real get_u_geo(int *ivar, int * ip) {
 my_real res;
 res = get_u_geo_p(ivar,ip);
 return res;
}


int  (*get_u_pnu_p)(int * ivar,int * ip,int * k);
int _FCALL GET_U_PNU(int *ivar, int * ip,int * k) {
 int res;
 res = get_u_pnu_p(ivar,ip,k);
 return res;
}
int get_u_pnu(int *ivar, int * ip,int * k) {
 int res;
 res = get_u_pnu_p(ivar,ip,k);
 return res;
}


int  (*get_u_mnu_p)(int * ivar,int * ip,int * k);
int _FCALL GET_U_MNU(int *ivar, int * ip,int * k) {
 int res;
 res = get_u_mnu_p(ivar,ip,k);
 return res;
}
int get_u_mnu(int *ivar, int * ip,int * k) {
 int res;
 res = get_u_mnu_p(ivar,ip,k);
 return res;
}


int  (*get_u_pid_p)(int * ip);
int _FCALL GET_U_PID(int * ip) {
 int res;
 res = get_u_pid_p(ip);
 return res;
}
int get_u_pid(int * ip) {
 int res;
 res = get_u_pid_p(ip);
 return res;
}


int  (*get_u_mid_p)(int * im);
int _FCALL GET_U_MID(int * im) {
 int res;
 res = get_u_mid_p(im);
 return res;
}
int get_u_mid(int * im) {
 int res;
 res = get_u_mid_p(im);
 return res;
}


int  (*get_u_m_p)(int * mid);
int _FCALL GET_U_M(int * mid) {
 int res;
 res = get_u_m_p(mid);
 return res;
}
int get_u_m(int * mid) {
 int res;
 res = get_u_m_p(mid);
 return res;
}


int  (*get_u_p_p)(int * pid);
int _FCALL GET_U_P(int * pid) {
 int res;
 res = get_u_p_p(pid);
 return res;
}
int get_u_p(int * pid) {
 int res;
 res = get_u_p_p(pid);
 return res;
}


int  (*get_u_proc_p)();
int _FCALL GET_U_PROC() {
 int res;
 res = get_u_proc_p();
 return res;
}
int get_u_proc() {
 int res;
 res = get_u_proc_p();
 return res;
}


int  (*get_u_task_p)();
int _FCALL GET_U_TASK() {
 int res;
 res = get_u_task_p();
 return res;
}
int get_u_task() {
 int res;
 res = get_u_task_p();
 return res;
}


int  (*get_u_func_n_p)(int * ifunc);
int _FCALL GET_U_FUNC_N(int * ifunc) {
 int res;
 res = get_u_func_n_p(ifunc);
 return res;
}
int get_u_fuunc_n(int * ifunc) {
 int res;
 res = get_u_func_n_p(ifunc);
 return res;
}


my_real  (*get_u_func_x_p)(int * ifunc,int * n);
my_real _FCALL GET_U_FUNC_X(int * ifunc,int *n) {
 my_real res;
 res = get_u_func_x_p(ifunc,n);
 return res;
}
my_real get_u_func_x(int * ifunc,int *n) {
 my_real res;
 res = get_u_func_x_p(ifunc,n);
 return res;
}


my_real  (*get_u_func_y_p)(int * ifunc,int * n);
my_real _FCALL GET_U_FUNC_Y(int * ifunc,int *n) {
 my_real res;
 res = get_u_func_y_p(ifunc,n);
 return res;
}
my_real get_u_func_y(int * ifunc,int *n) {
 my_real res;
 res = get_u_func_y_p(ifunc,n);
 return res;
}


my_real  (*get_u_func_p)(int * ifunc,my_real * XX, my_real * DERI);
my_real _FCALL GET_U_FUNC(int * ifunc,my_real *XX,my_real * DERI) {
 my_real res;
 res = get_u_func_p(ifunc,XX,DERI);
 return res;
}
my_real get_u_func(int * ifunc,my_real *XX,my_real * DERI) {
 my_real res;
 res = get_u_func_p(ifunc,XX,DERI);
 return res;
}


void  (*get_v_func_p)(int * ifunc,int * llt,my_real * xx, my_real * dydx,int * jpos);
void _FCALL GET_V_FUNC(int * ifunc,int * llt,my_real * xx, my_real * dydx,int * jpos) {
 get_v_func_p(ifunc,llt,xx, dydx,jpos);
}
void get_v_func(int * ifunc,int * llt,my_real * xx, my_real * dydx,int * jpos) {
 get_v_func_p(ifunc,llt,xx, dydx,jpos);
}


int  (*get_u_numfun_p)(int * idfun);
int _FCALL GET_U_NUMFUN(int * idfun) {
 int res;
 res = get_u_numfun_p(idfun);
 return res;
}
int get_u_numfun(int * idfun) {
 int res;
 res = get_u_numfun_p(idfun);
 return res;
}


int  (*get_u_fid_p)(int * ifun);
int _FCALL GET_U_FID(int * ifun) {
 int res;
 res = get_u_fid_p(ifun);
 return res;
}
int get_u_fid(int * ifun) {
 int res;
 res = get_u_fid_p(ifun);
 return res;
}


int  (*get_u_cycle_p)();
int _FCALL GET_U_CYCLE() {
 int res;
 res = get_u_cycle_p();
 return res;
}
int get_u_cycle() {
 int res;
 res = get_u_cycle_p();
 return res;
}


my_real  (*get_u_time_p)();
my_real _FCALL GET_U_TIME() {
 my_real res;
 res = get_u_time_p();
 return res;
}
my_real get_u_time() {
 my_real res;
 res = get_u_time_p();
 return res;
}


my_real  (*get_u_accel_p)(int * nacc, my_real * ax, my_real * ay, my_real * az);
my_real _FCALL GET_U_ACCEL(int * nacc, my_real * ax, my_real * ay, my_real * az) {
 my_real res;
 res = get_u_accel_p(nacc, ax, ay, az);
 return res;
}
my_real get_u_accel(int * nacc, my_real * ax, my_real * ay, my_real * az) {
 my_real res;
 res = get_u_accel_p(nacc, ax, ay, az);
 return res;
}


int  (*get_u_numacc_p)(int * idacc);
int _FCALL GET_U_NUMACC(int * idacc) {
 int res;
 res = get_u_numacc_p(idacc);
 return res;
}
int get_u_numacc(int * idacc) {
 int res;
 res = get_u_numacc_p(idacc);
 return res;
}


int  (*get_u_numnod_p)(int * iu);
int _FCALL GET_U_NUMNOD(int * iu) {
 int res;
 res = get_u_numnod_p(iu);
 return res;
}
int get_u_numnod(int * iu) {
 int res;
 res = get_u_numnod_p(iu);
 return res;
}


int  (*get_u_nod_x_p)(int * nod, my_real * x, my_real * y, my_real * z);
int _FCALL GET_U_NOD_X(int * nod, my_real * x, my_real * y, my_real * z) {
 int res;
 res = get_u_nod_x_p(nod, x, y, z);
 return res;
}
int get_u_nod_x(int * nod, my_real * x, my_real * y, my_real * z) {
 int res;
 res = get_u_nod_x_p(nod, x, y, z);
 return res;
}


int  (*get_u_nod_d_p)(int * nod, my_real * dx, my_real * dy, my_real * dz);
int _FCALL GET_U_NOD_D(int * nod, my_real * dx, my_real * dy, my_real * dz) {
 int res;
 res = get_u_nod_d_p(nod, dx, dy, dz);
 return res;
}
int get_u_nod_d(int * nod, my_real * dx, my_real * dy, my_real * dz) {
 int res;
 res = get_u_nod_d_p(nod, dx, dy, dz);
 return res;
}


int  (*get_u_nod_v_p)(int * nod, my_real * vx, my_real * vy, my_real * vz);
int _FCALL GET_U_NOD_V(int * nod, my_real * vx, my_real * vy, my_real * vz) {
 int res;
 res = get_u_nod_v_p(nod, vx, vy, vz);
 return res;
}
int get_u_nod_v(int * nod, my_real * vx, my_real * vy, my_real * vz) {
 int res;
 res = get_u_nod_v_p(nod, vx, vy, vz);
 return res;
}


int  (*get_u_nod_a_p)(int * nod, my_real * ax, my_real * ay, my_real * az);
int _FCALL GET_U_NOD_A(int * nod, my_real * ax, my_real * ay, my_real * az) {
 int res;
 res = get_u_nod_a_p(nod, ax, ay, az);
 return res;
}
int get_u_nod_a(int * nod, my_real * ax, my_real * ay, my_real * az) {
 int res;
 res = get_u_nod_a_p(nod, ax, ay, az);
 return res;
}


int  (*get_u_skew_p)(int * idskw, int * n1,int* n2, int* n3, my_real * vect);
int _FCALL GET_U_SKEW(int * idskw, int * n1,int* n2, int* n3, my_real * vect) {
 int res;
 res = get_u_skew_p(idskw,n1, n2, n3, vect);
 return res;
}
int get_u_skew(int * idskw, int * n1,int* n2, int* n3, my_real * vect) {
 int res;
 res = get_u_skew_p(idskw,n1, n2, n3, vect);
 return res;
}


my_real  (*get_u_uvar_p)(int * iel, int * ilayer,int* ivar, int* nuvar);
my_real _FCALL GET_U_UVAR(int * iel, int * ilayer,int* ivar, int* nuvar) {
 my_real res;
 res = get_u_uvar_p(iel,ilayer,ivar,nuvar);
 return res;
}
my_real get_u_var(int * iel, int * ilayer,int* ivar, int* nuvar) {
 my_real res;
 res = get_u_uvar_p(iel,ilayer,ivar,nuvar);
 return res;
}


void  (*set_spring_elnum_p)(int * jft, int * jlt,int* ixr);
void _FCALL SET_SPRING_ELNUM(int * jft, int * jlt,int* ixr) {
 set_spring_elnum_p(jft,jlt,ixr);
}
void set_spring_elnum(int * jft, int * jlt,int* ixr) {
 set_spring_elnum_p(jft,jlt,ixr);
}


int  (*get_spring_elnum_p)(int * iel);
int _FCALL GET_SPRING_ELNUM(int * iel) {
 int res;
 res = get_spring_elnum_p(iel);
 return res;
}
int get_spring_elnum(int * iel) {
 int res;
 res = get_spring_elnum_p(iel);
 return res;
}


int  (*set_u_geo_p)(int *ivar,my_real *a);
int _FCALL SET_U_GEO(int *ivar,my_real *a) {
 int res;
 res = set_u_geo_p(ivar,a);
 return res;
}
int set_u_geo(int *ivar,my_real *a) {
 int res;
 res = set_u_geo_p(ivar,a);
 return res;
}


int  (*set_u_pnu_p)(int * ivar,int * ip,int * k);
int _FCALL SET_U_PNU(int *ivar, int * ip,int * k) {
 int res;
 res = set_u_pnu_p(ivar,ip,k);
 return res;
}
int set_u_pnu(int *ivar, int * ip,int * k) {
 int res;
 res = set_u_pnu_p(ivar,ip,k);
 return res;
}


int  (*reset_u_geo_p)(int * ivar,int * ip,my_real * a);
int _FCALL RESET_U_GEO(int *ivar, int * ip,my_real * a) {
 int res;
 res = reset_u_geo_p(ivar,ip,a);
 return res;
}
int reset_u_geo(int *ivar, int * ip,my_real * a) {
 int res;
 res = reset_u_geo_p(ivar,ip,a);
 return res;
}


my_real  (*get_u_func_deri_p)(int * ifunc);
my_real _FCALL GET_U_FUNC_DERI(int * ifunc) {
 my_real res;
 res = get_u_func_deri_p(ifunc);
 return res;
}
my_real get_u_func_deri(int * ifunc) {
 my_real res;
 res = get_u_func_deri_p(ifunc);
 return res;
}


int  (*set_u_sens_ipar_p)(int * ivar,int * var);
int _FCALL SET_U_SENS_IPAR(int *ivar, int * var) {
 int res;
 res = set_u_sens_ipar_p(ivar,var);
 return res;
}
int set_u_sens_ipar(int *ivar, int * var) {
 int res;
 res = set_u_sens_ipar_p(ivar,var);
 return res;
}


int  (*set_u_sens_fpar_p)(int * ivar,my_real * var);
int _FCALL SET_U_SENS_FPAR(int *ivar, my_real * var) {
 int res;
 res = set_u_sens_fpar_p(ivar,var);
 return res;
}
int set_u_sens_fpar(int *ivar, my_real * var) {
 int res;
 res = set_u_sens_fpar_p(ivar,var);
 return res;
}


my_real (*finter_p)(int *ifunc ,my_real *XX , int *NPF ,my_real *TF ,my_real *DERI);

my_real _FCALL FINTER(int *ifunc ,my_real * XX ,int* NPF ,my_real *TF ,my_real *DERI){
  my_real result;
  result = finter_p(ifunc ,  XX,  NPF, TF, DERI);
  return result;
}
my_real finter(int *ifunc ,my_real * XX ,int* NPF ,my_real *TF ,my_real *DERI){
  my_real result;
  result = finter_p(ifunc ,  XX,  NPF, TF, DERI);
  return result;
}


void (*write_iout_p)(char * line,int* len);
void _FCALL WRITE_IOUT(char* line,int *len) {
   write_iout_p(line,len);
}
void write_iout(char* line,int *len) {
   write_iout_p(line,len);
}

void (*set_dd_mat_weight_p)(my_real *mat_weight1pt,my_real *mat_weight5pt,int * elem_type);

void _FCALL SET_DD_MAT_WEIGHT(my_real * MAT_WEIGHT1PT,my_real * MAT_WEIGHT5PT,int * elem_type){
   set_dd_mat_weight_p(MAT_WEIGHT1PT,MAT_WEIGHT5PT,elem_type);
}
void set_dd_mat_weight(my_real *MAT_WEIGHT1PT,my_real *MAT_WEIGHT5PT,int * elem_type){
   set_dd_mat_weight_p(MAT_WEIGHT1PT,MAT_WEIGHT5PT,elem_type);
}

void (*uelt_spmd_additional_node_p)(int * nodid);

void _FCALL UELT_SPMD_ADDITIONAL_NODE(int * NODID){
  uelt_spmd_additional_node_p(NODID);
}
void uelt_spmd_additional_node(int * NODID){
  uelt_spmd_additional_node_p(NODID);
}

void (*arret_p)(int * mode);
void _FCALL ARRET(int * mode){  arret_p(mode);}
void _FCALL arret(int * mode){  arret_p(mode);}


int (*set_u_sens_deacti_p)(int * nsens);
int _FCALL SET_U_SENS_DEACTI(int *nsens) {
 int res;
 res = set_u_sens_deacti_p(nsens);
 return res;
}
int set_u_sens_deacti(int *nsens) {
 int res;
 res = set_u_sens_deacti_p(nsens);
 return res;
}

void (*get_table_value_p)(int * itable,my_real *XX, int * XXDIM, my_real *YY);
void _FCALL GET_TABLE_VALUE(int * itable,my_real *XX, int * XXDIM,my_real *YY){
 get_table_value_p(itable,XX,XXDIM,YY);
}
void get_table_value(int * itable,my_real *XX, int * XXDIM, my_real *YY){
 get_table_value_p(itable,XX,XXDIM,YY);
}


void (*get_vtable_value_p)(int * itable, int * nel0, int * ipos,my_real *XX, int *XXDIM, my_real*YY, my_real *DYDX1);
void   _FCALL GET_VTABLE_VALUE(int * itable, int * nel0, int * ipos,my_real *XX, int *XXDIM, my_real*YY, my_real *DYDX1){
  get_vtable_value_p(itable,nel0,ipos,XX,XXDIM,YY,DYDX1);
}
void get_vtable_value(int * itable, int * nel0, int * ipos,my_real *XX,int *XXDIM, my_real*YY, my_real *DYDX1){
  get_vtable_value_p(itable,nel0,ipos,XX,XXDIM,YY,DYDX1);
}

void (*mat_solid_get_nod_x_p) (my_real USER_X);
void  _FCALL  MAT_SOLID_GET_NOD_X(my_real USER_X){
    mat_solid_get_nod_x_p(USER_X);
}
void  mat_solid_get_nod_x(my_real USER_X){
    mat_solid_get_nod_x_p(USER_X);
}


void (*mat_solid_get_nod_v_p) (my_real USER_V);
void  _FCALL  MAT_SOLID_GET_NOD_V(my_real USER_V){
    mat_solid_get_nod_v_p(USER_V);
}
void  mat_solid_get_nod_v(my_real USER_V){
    mat_solid_get_nod_v_p(USER_V);
}


void (*userwindow_get_a_p) (double A_BUF);
void  _FCALL  USERWINDOW_GET_A(double A_BUF){
    userwindow_get_a_p(A_BUF);
}
void  userwindow_get_a(double A_BUF){
    userwindow_get_a_p(A_BUF);
}


void (*userwindow_get_ar_p) (double AR_BUF);
void  _FCALL  USERWINDOW_GET_AR(double AR_BUF){
    userwindow_get_ar_p(AR_BUF);
}
void  userwindow_get_ar(double AR_BUF){
    userwindow_get_ar_p(AR_BUF);
}


void (*rad_umat_open_p) (char * filename,int * length,int * result);

void _FCALL RAD_UMAT_OPEN (char * filename,int * length,int * result){
   rad_umat_open_p (filename,length,result);
}


void (*rad_umat_input_read_p) (char * line,int * len,int *size_read );
void _FCALL RAD_UMAT_INPUT_READ(char * line,int * len,int *size_read ){
  printf("read\n");
  rad_umat_input_read_p( line,len,size_read );
}

void (*rad_umat_input_rewind_p)();
void _FCALL RAD_UMAT_INPUT_REWIND(){
  rad_umat_input_rewind_p();
}

void (*rad_umat_close_input_p)();
void  _FCALL RAD_UMAT_CLOSE_INPUT(){
    rad_umat_close_input_p();
}

int (*set_u_sens_spmd_node_list_p)(int * var, int * ivar);
int _FCALL SET_U_SENS_SPMD_NODE_LIST(int * var, int * ivar){
  int res ;
  res = set_u_sens_spmd_node_list_p(var, ivar);
  return res ;
}

void (*get_table_value_dydx_p)(int *ITABLE, double *XX, double *XXDIM, double *YY, double *DYDX);
void  _FCALL GET_TABLE_VALUE_DYDX(int *ITABLE, double *XX, double *XXDIM, double *YY, double *DYDX){
    get_table_value_dydx_p(ITABLE, XX, XXDIM, YY, DYDX);
}

void (*set_user_window_nodes_p)(int *USERNODS, int * NUMBER_NODES);
void  _FCALL SET_USER_WINDOW_NODES(int *USERNODS, int *NUMBER_USERNODS){
         set_user_window_nodes_p(USERNODS, NUMBER_USERNODS);
}

void (*get_user_window_nodes_p)(int *INTERNAL_ID,int *USER_ID);
void  _FCALL GET_USER_WINDOW_NODES(int *INTERNAL_ID,int *USER_ID){
         get_user_window_nodes_p(INTERNAL_ID,USER_ID);
}


__declspec(dllexport) void set_callback ( void ** callback_array)
{
  finter_p              = callback_array[ 0];
  get_u_numtable_p      = callback_array[ 1];
  get_u_table_p         = callback_array[ 2];
  get_u_vtable_p        = callback_array[ 3];
  set_u_shlplas_p       = callback_array[ 4];
  set_u_solplas_p       = callback_array[ 5];
  usens_shift_ab_p      = callback_array[ 6];
  usens_shift_ba_p      = callback_array[ 7];
  get_u_numsens_p       = callback_array[ 8];
  get_u_sens_id_p       = callback_array[ 9];
  set_u_sens_value_p    = callback_array[10];
  get_u_sens_value_p    = callback_array[11];
  set_u_sens_maxvalue_p = callback_array[12];
  get_u_sens_fpar_p     = callback_array[13];
  get_u_sens_ipar_p     = callback_array[14];
  set_u_sens_acti_p     = callback_array[15];
  get_u_sens_acti_p     = callback_array[16];
  get_u_sens_p          = callback_array[17];
  get_u_sens_delay_p    = callback_array[18];
  get_u_mat_p           = callback_array[19];
  get_u_geo_p           = callback_array[20];
  get_u_pnu_p           = callback_array[21];
  get_u_mnu_p           = callback_array[22];
  get_u_pid_p           = callback_array[23];
  get_u_mid_p           = callback_array[24];
  get_u_m_p             = callback_array[25]; 
  get_u_p_p             = callback_array[26]; 
  get_u_proc_p          = callback_array[27]; 
  get_u_task_p          = callback_array[28]; 
  get_u_func_n_p        = callback_array[29]; 
  get_u_func_x_p        = callback_array[30]; 
  get_u_func_y_p        = callback_array[31]; 
  get_u_func_p          = callback_array[32]; 
  get_v_func_p          = callback_array[33]; 
  get_u_numfun_p        = callback_array[34]; 
  get_u_fid_p           = callback_array[35]; 
  get_u_cycle_p         = callback_array[36]; 
  get_u_time_p          = callback_array[37]; 
  get_u_accel_p         = callback_array[38]; 
  get_u_numacc_p        = callback_array[39];
  get_u_numnod_p        = callback_array[40];
  get_u_nod_x_p         = callback_array[41];
  get_u_nod_d_p         = callback_array[42];
  get_u_nod_v_p         = callback_array[43];
  get_u_nod_a_p         = callback_array[44];
  get_u_skew_p          = callback_array[45];
  get_u_uvar_p          = callback_array[46]; 
  set_spring_elnum_p    = callback_array[47]; 
  get_spring_elnum_p    = callback_array[48]; 
  set_u_geo_p           = callback_array[49]; 
  set_u_pnu_p           = callback_array[50]; 
  reset_u_geo_p         = callback_array[51]; 
  get_u_func_deri_p     = callback_array[52]; 
  set_u_sens_ipar_p     = callback_array[53]; 
  set_u_sens_fpar_p     = callback_array[54];
  write_iout_p          = callback_array[55];
  set_dd_mat_weight_p   = callback_array[56];
  uelt_spmd_additional_node_p = callback_array[57];
  arret_p               = callback_array[58];
  set_u_sens_deacti_p   = callback_array[59];
  get_table_value_p     = callback_array[60];
  get_vtable_value_p    = callback_array[61];
  mat_solid_get_nod_x_p = callback_array[62];
  mat_solid_get_nod_v_p = callback_array[63]; 
  userwindow_get_a_p    = callback_array[64];
  userwindow_get_ar_p   = callback_array[65];
  rad_umat_open_p       = callback_array[66];
  rad_umat_input_read_p = callback_array[67];
  rad_umat_input_rewind_p = callback_array[68];
  rad_umat_close_input_p = callback_array[69];
  set_u_sens_spmd_node_list_p = callback_array[70];
  get_table_value_dydx_p  = callback_array[71];
  set_user_window_nodes_p = callback_array[72];
  get_user_window_nodes_p = callback_array[73];
}

#elif 1
void set_callback ( void ** callback_array)
{

}
#endif
