//Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
//Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
#include <math.h>
void c_unwrap(int lenperimeter, int * flatperimeter, int gridsize, double *amp, double *phase, int *mask, double pi, double twopi)
{
    while(lenperimeter)
    {
        double maxamp=-1.0;
        int ijmaxamp=0;
        lenperimeter--;
        int ijp=flatperimeter[lenperimeter];
        int neigh[4]={ijp-1,ijp+1,ijp-gridsize,ijp+gridsize};
        for (int ineigh=0;ineigh<4;ineigh++)
        {
            int ijneigh=neigh[ineigh];
            if (mask[ijneigh]==2)
            {
                if (amp[ijneigh]>maxamp)
                {
                    maxamp=amp[ijneigh];
                    ijmaxamp=ijneigh;
                }
            }else if (mask[ijneigh]==0)
            {
                int iper,jper;
                for (iper=0;iper<lenperimeter && amp[ijneigh]>amp[flatperimeter[iper]];iper++);
                for (jper=lenperimeter;jper>iper;jper--)
                    flatperimeter[jper]=flatperimeter[jper-1];
                flatperimeter[iper]=ijneigh;
                mask[ijneigh]=3;
                lenperimeter++;
            }
        }
        mask[ijp]=2;
        double dd=phase[ijp]-phase[ijmaxamp];
        if (fabs(dd)>=pi)
        {
            double ddmod=(dd-floor((dd+pi)/twopi)*twopi);
            if ((ddmod==-pi)&&(dd>0.0))
                ddmod=pi;
            phase[ijp]+=ddmod-dd;
        }
    }
}

void c_cpu_idft_code(double*aperturereal,double*apertureimag,double*l,double*m,double*rebeam,double*imbeam,double*x,double*y,int Nx,int Nl)
{
        int nxy=Nx;
        int nlm=Nl;
        for (int ilm=0;ilm<nlm;ilm++)
        {
            double beamr=0.0;
            double beami=0.0;
            double lilm=l[ilm];
            double milm=m[ilm];
            for (int idx=0;idx<nxy;idx++)
            {
                double theta=-(x[idx]*lilm+y[idx]*milm);
                double costheta=cos(theta);
                double sintheta=sin(theta);
                beamr+=aperturereal[idx]*costheta-apertureimag[idx]*sintheta;
                beami+=aperturereal[idx]*sintheta+apertureimag[idx]*costheta;
            }
            rebeam[ilm]=beamr/(double)nxy;
            imbeam[ilm]=beami/(double)nxy;
        }
}

void c_cpu_dft_code(double*aperturereal,double*apertureimag,double*l,double*m,double*rebeam,double*imbeam,double*x,double*y,int Nx,int Nl)
{
        int nxy=Nx;
        int nlm=Nl;
        for (int idx=0;idx<nxy;idx++)
        {
            double apr=0.0;
            double api=0.0;
            double xidx=x[idx];
            double yidx=y[idx];
            for (int ilm=0;ilm<nlm;ilm++)
            {
                double theta=(xidx*l[ilm]+yidx*m[ilm]);
                double costheta=cos(theta);
                double sintheta=sin(theta);
                apr+=rebeam[ilm]*costheta-imbeam[ilm]*sintheta;
                api+=rebeam[ilm]*sintheta+imbeam[ilm]*costheta;
            }
            aperturereal[idx]=apr;
            apertureimag[idx]=api;
        }
}
