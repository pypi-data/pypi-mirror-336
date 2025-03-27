//Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
//Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
void c_unwrap(int lenperimeter, int * flatperimeter, int gridsize, double *amp, double *phase, int *mask, double pi, double twopi);
void c_cpu_idft_code(double*aperturereal,double*apertureimag,double*l,double*m,double*rebeam,double*imbeam,double*x,double*y,int Nx,int Nl);
void c_cpu_dft_code(double*aperturereal,double*apertureimag,double*l,double*m,double*rebeam,double*imbeam,double*x,double*y,int Nx,int Nl);
