import numpy as np
import jax.numpy as jnp
from classy import Class
from .glquad import GLQuad
from .wignerd import *
from .new_remote_spectra import *
from scipy import special
from scipy.interpolate import interp1d, interp2d
import ipdb

class test_operation:
    def __init__(self, *args):
        self.a = args[0]
        self.b = args[1]

    def operation(self, c):
        return (self.a + self.b)*c


class pSZ_ps():
    def __init__(self, A_s, n_s, Omega_b, Omega_c, h, tau, w, wa, Omega_K):
        """
        Cosmological parameters container

        Attributes:
        Omega_b (float): Baryon density parameter
        Omega_c (float): Cold dark matter density parameter
        h (float): Dimensionless Hubble parameter (H0/100 km/s/Mpc)
        """
        self.A_s = A_s
        self.n_s = n_s
        self.Omega_b = Omega_b
        self.Omega_c = Omega_c
        self.h = h
        self.tau = tau
        self.w = w
        self.wa = wa
        self.Omega_K = Omega_K
        self.common_settings = {
            'h':self.h,
            'omega_b':self.Omega_b*self.h**2,
            'omega_cdm':self.Omega_c*self.h**2,
            'A_s': self.A_s*1e-9,
            'n_s': self.n_s,
            'tau_reio':self.tau,
            'output':'mPk',
            'P_k_max_1/Mpc':15,
            'gauge':'newtonian'
        }

        self.M = Class()
        self.M.set(self.common_settings)
        self.M.set({'z_pk':1000})
        self.M.compute()


    def CLEE_psz0(self, lmax, k=None, Pk_pri=None, Chi_low=1, Chi_re=9000, Chi_grid_num=100):
        L = np.arange(0, lmax+1, 1)
        T_list = [Transfer_E(k, L, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h, self.tau, Chi_low=Chi_low, Chi_re=Chi_re, Chi_grid_num=Chi_grid_num)]

        return CL_bins(T_list, T_list, L, k=k, Pk_pri=Pk_pri)[0]


    def CLdd_eff_oneChi(self, L, Chi, for_cross=False):
        """
        CLdd_eff(Chi)
        """
        if not isinstance(L, np.ndarray):
            L = np.array([L])
        CL = np.zeros(len(L), dtype=np.complex64)

        Z = zfromchi(Chi, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        a = az(Z)
        sigma_ne = sigma_nez(Z, self.Omega_b, self.h)
        # ipdb.set_trace()
        if for_cross:
            CL = a*sigma_ne*self.M.get_pk_all((L+1/2)/np.array(Chi), Z)
        else:
            CL = a**2*sigma_ne**2*self.M.get_pk_all((L+1/2)/np.array(Chi), Z)
        return CL[0]

    def CLdd_eff_Chi1Chi2(self, L, Chi1, Chi2, k=None):
        """
        CLDD_eff(Chi1, Chi2)
        """
        if not isinstance(L, np.ndarray):
            L = np.array([L])

        Z1 = zfromchi(Chi1, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        a1 = az(Z1)
        sigma_ne1 = sigma_nez(Z1, self.Omega_b, self.h)

        Z2 = zfromchi(Chi1, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        a2 = az(Z2)
        sigma_ne2 = sigma_nez(Z2, self.Omega_b, self.h)

        CL = np.zeros(len(L), dtype=np.complex64)
        Integrand = np.zeros((len(k), len(L)), dtype=np.complex64)
        k_broad = np.broadcast_to(k, (len(L), len(k))).transpose()
        L_broad = np.broadcast_to(L, (len(k), len(L)))

        Integrand = (k_broad**2)/(2*np.pi)**3* a1*a2*sigma_ne1*sigma_ne2*(4*np.pi)**2*special.spherical_jn(L_broad, k_broad*Chi1)*special.spherical_jn(L_broad, k_broad*Chi2)*np.sqrt(self.M.get_pk_all(k_broad, Z1[0])*self.M.get_pk_all(k_broad, Z2[0]))

        CL = np.real(integrate.simps(Integrand, k, axis=0))
        return CL



    def CLqq_oneChi(self, L, Chi, k=None, Pk_pri=None):
        """
        CLqq(Chi, Chi')
        """
        if not isinstance(L, np.ndarray):
            L = np.array([L])
        CL = np.zeros(len(L), dtype=np.complex64)
        k_broad = np.broadcast_to(k, (len(L), len(k))).transpose()
        Pk_pri_broad = np.broadcast_to(Pk_pri, (len(L), len(k))).transpose()
        Integrand = np.zeros((len(k), len(L)), dtype=np.complex64)

        Z = zfromchi(Chi, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        T = Transfer_psz_redshift(k, L, Z[0], self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)

        Integrand = (k_broad**2)/(2*np.pi)**3*Pk_pri_broad*np.conj(T)*T
        CL = np.real(integrate.simps(Integrand, k, axis=0))

        return CL

    def CLqq_Chi1Chi2(self, L, Chi1, Chi2, k=None, Pk_pri=None):
        """
        CLqq(Chi, Chi')
        """
        if not isinstance(L, np.ndarray):
            L = np.array([L])
        CL = np.zeros(len(L), dtype=np.complex64)
        k_broad = np.broadcast_to(k, (len(L), len(k))).transpose()
        Pk_pri_broad = np.broadcast_to(Pk_pri, (len(L), len(k))).transpose()
        Integrand = np.zeros((len(k), len(L)), dtype=np.complex64)

        Z1 = zfromchi(Chi1, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        T1 = Transfer_psz_redshift(k, L, Z1[0], self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)


        Z2 = zfromchi(Chi2, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        T2 = Transfer_psz_redshift(k, L, Z2[0], self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)

        Integrand = (k_broad**2)/(2*np.pi)**3*Pk_pri_broad*np.conj(T1)*T2

        CL = np.real(integrate.simps(Integrand, k, axis=0))
        return CL


    def CLee_psz1_oneChi(self, lmax, l1min, l1max, l2min, l2max, Chi, k=None, Pk_pri=None):
        """
        CLee_psz_1(Chi)
        Attributes:
        k:
        Pk_pri: primordial scalar perturbation power spectrum
        """
        l = jnp.arange(0, lmax+1)
        glq = GLQuad(int((3*lmax+1)/2))

        # l1 = jnp.arange(0, l1max+1)
        l1 = np.arange(0, l1max+1)
        l2 = np.arange(0, l2max+1)

        # ipdb.set_trace()
        Z = zfromchi(Chi, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        Cl1 = self.M.get_pk_all((l+1/2)/np.array(Chi), Z)[0]
        Cl2 = self.CLqq_oneChi(l2, Chi, k=k, Pk_pri=Pk_pri)

        # ipdb.set_trace()
        zeta_00 = glq.cf_from_cl(0, 0, Cl1, lmin=l1min, lmax=l1max, prefactor=True)
        zeta_m2m2 = glq.cf_from_cl(-2, -2, Cl2, lmin=l2min, lmax=l2max, prefactor=True)
        zeta_p2m2 = glq.cf_from_cl(2, -2, Cl2, lmin=l2min, lmax=l2max, prefactor=True)

        A = glq.cl_from_cf(2, 2, zeta_00 * zeta_m2m2, lmax=lmax)
        B = glq.cl_from_cf(-2, 2, zeta_00 * zeta_p2m2, lmax=lmax)

        return np.pi*(A + B)



    def geL_oneChi(self, lmax, l1min, l1max, l2min, l2max, Chi):
        """
        geL(chi)
        """
        l = jnp.arange(0, lmax+1)
        glq = GLQuad(int((3*lmax+1)/2))

        # l1 = jnp.arange(0, l1max+1)
        l1 = np.arange(0, l1max+1)
        l2 = np.arange(0, l2max+1)

        # ipdb.set_trace()
        Z = zfromchi(Chi, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        Cl1 = self.M.get_pk_all((l+1/2)/np.array(Chi), Z)[0]
        Cl2 = np.ones(l2max+1)

        zeta_00 = glq.cf_from_cl(0, 0, Cl1, lmin=l1min, lmax=l1max, prefactor=True)
        zeta_m2m2 = glq.cf_from_cl(-2, -2, Cl2, lmin=l2min, lmax=l2max, prefactor=True)
        zeta_p2m2 = glq.cf_from_cl(2, -2, Cl2, lmin=l2min, lmax=l2max, prefactor=True)

        A = glq.cl_from_cf(2, 2, zeta_00 * zeta_m2m2, lmax=lmax)
        B = glq.cl_from_cf(-2, 2, zeta_00 * zeta_p2m2, lmax=lmax)

        return np.pi*(A + B)



    def GeL(self, lmax, l1min, l1max, l2min, l2max, z_low=None, z_high=None, Chi_grid_num=50):

        Chi_grid = np.linspace(chifromz(z_low, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h), chifromz(z_high, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h), Chi_grid_num)

        ipdb.set_trace()

        Z_grid = zfromchi(Chi_grid, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        a_grid = az(Z_grid)
        sigma_ne_grid = sigma_nez(Z_grid, self.Omega_b, self.h)

        Integrand = np.zeros((lmax+1, len(Chi_grid)), dtype=np.complex64)
        Gl = np.zeros((lmax+1, len(Chi_grid)))

        print("calculating GeL")
        for i in np.arange(len(Chi_grid)):
            Integrand[:, i] = 1/Chi_grid[i]*a_grid[i]*sigma_ne_grid[i]*self.geL_oneChi(lmax, l1min, l1max, l2min, l2max, Chi_grid[i])

        Gl = np.sqrt(6)/10*integrate.simps(Integrand, Chi_grid, axis=-1).real
        return Gl



    def CLee_psz1_Chi1Chi2(self, lmax, l1min, l1max, l2min, l2max, Chi1, Chi2,  k=None, Pk_pri=None):

        l = jnp.arange(0, lmax+1)
        glq = GLQuad(int((3*lmax+1)/2))

        # l1 = jnp.arange(0, l1max+1)
        l1 = np.arange(0, l1max+1)
        l2 = np.arange(0, l2max+1)

        # ipdb.set_trace()
        Cl1 = self.CLdd_eff_Chi1Chi2(l1, Chi1, Chi2, k=k)
        Cl2 = self.CLqq_Chi1Chi2(l2, Chi1, Chi2, k=k, Pk_pri=Pk_pri)

        f1 = Cl1
        f2 = Cl2
        # ipdb.set_trace()
        zeta_00 = glq.cf_from_cl(0, 0, f1, lmin=l1min, lmax=l1max, prefactor=True)
        zeta_m2m2 = glq.cf_from_cl(-2, -2, f2, lmin=l2min, lmax=l2max, prefactor=True)
        zeta_p2m2 = glq.cf_from_cl(2, -2, f2, lmin=l2min, lmax=l2max, prefactor=True)

        A = glq.cl_from_cf(2, 2, zeta_00 * zeta_m2m2, lmax=lmax)
        B = glq.cl_from_cf(-2, 2, zeta_00 * zeta_p2m2, lmax=lmax)

        return np.pi*(A + B)



    def CLbb_psz1_oneChi(self, lmax, l1min, l1max, l2min, l2max, Chi, k=None, Pk_pri=None):
        """
        CLbb_psz_1(Chi)
        """
        l = jnp.arange(0, lmax+1)
        glq = GLQuad(int((3*lmax+1)/2))

        # l1 = jnp.arange(0, l1max+1)
        l1 = np.arange(0, l1max+1)
        l2 = np.arange(0, l2max+1)

        # ipdb.set_trace()
        # Cl1 = self.CLdd_eff_oneChi(l1, Chi)
        Z = zfromchi(Chi, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        Cl1 = self.M.get_pk_all((l+1/2)/np.array(Chi), Z)[0]
        Cl2 = self.CLqq_oneChi(l2, Chi, k=k, Pk_pri=Pk_pri)

        # ipdb.set_trace()
        zeta_00 = glq.cf_from_cl(0, 0, Cl1, lmin=l1min, lmax=l1max, prefactor=True)
        zeta_m2m2 = glq.cf_from_cl(-2, -2, Cl2, lmin=l2min, lmax=l2max, prefactor=True)
        zeta_p2m2 = glq.cf_from_cl(2, -2, Cl2, lmin=l2min, lmax=l2max, prefactor=True)

        A = glq.cl_from_cf(2, 2, zeta_00 * zeta_m2m2, lmax=lmax)
        B = glq.cl_from_cf(-2, 2, zeta_00 * zeta_p2m2, lmax=lmax)

        return np.pi*(A - B)


    def CLEE_psz1(self, lmax, l1min, l1max, l2min, l2max, k=None, Pk_pri=None, Chi_low=1000, Chi_re=9000, Chi_grid_num=100):

        Chi_grid = np.linspace(Chi_low, Chi_re, Chi_grid_num)
        Z_grid = zfromchi(Chi_grid, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        a_grid = az(Z_grid)
        sigma_ne_grid = sigma_nez(Z_grid, self.Omega_b, self.h)

        Integrand = np.zeros((lmax+1, len(Chi_grid)), dtype=np.complex64)
        Cl = np.zeros((lmax+1, len(Chi_grid)))

        print("calculating CLEE_pSZ1")
        for i in np.arange(len(Chi_grid)):
            Integrand[:, i] = 1/Chi_grid[i]**2*a_grid[i]**2*sigma_ne_grid[i]**2*self.CLee_psz1_oneChi(lmax, l1min, l1max, l2min, l2max, Chi_grid[i], k=k, Pk_pri=Pk_pri)

        Cl = 6/100*integrate.simps(Integrand, Chi_grid, axis=-1).real
        return Cl


    def CLBB_psz1(self, lmax, l1min, l1max, l2min, l2max, k=None, Pk_pri=None, Chi_low=1000, Chi_re=9000, Chi_grid_num=100):


        Chi_grid = np.linspace(Chi_low, Chi_re, Chi_grid_num)
        Z_grid = zfromchi(Chi_grid, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        a_grid = az(Z_grid)
        sigma_ne_grid = sigma_nez(Z_grid, self.Omega_b, self.h)

        Integrand = np.zeros((lmax+1, len(Chi_grid)), dtype=np.complex64)
        Cl = np.zeros((lmax+1, len(Chi_grid)))

        print("calculating CLBB_pSZ1")
        for i in np.arange(len(Chi_grid)):
            Integrand[:, i] = 1/Chi_grid[i]**2*a_grid[i]**2*sigma_ne_grid[i]**2*self.CLbb_psz1_oneChi(lmax, l1min, l1max, l2min, l2max, Chi_grid[i], k=k, Pk_pri=Pk_pri)

        Cl = 6/100*integrate.simps(Integrand, Chi_grid, axis=-1).real
        return Cl



    def CLEE_psz1_accurate(self, lmax, l1min, l1max, l2min, l2max, k=None, Pk_pri=None, Chi_low=1000, Chi_re=9000, Chi_grid_num=100):
        Chi_grid = np.linspace(Chi_low, Chi_re, Chi_grid_num)

        Cl = np.zeros((lmax+1, len(Chi_grid), len(Chi_grid)))

        Integrand = np.zeros((lmax+1, len(Chi_grid), len(Chi_grid)), dtype=np.complex64)
        print("calculating CLEE_pSZ1_accurate")
        for i in np.arange(len(Chi_grid)):
            for j in np.arange(len(Chi_grid)):
                print(i, j)
                Integrand[:, i, j] = self.CLee_psz1_Chi1Chi2(lmax, l1min, l1max, l2min, l2max, Chi_grid[i], Chi_grid[j], k=k, Pk_pri=Pk_pri)

        Cl = integrate.simps(Integrand, Chi_grid, axis=-1).real
        Cl = integrate.simps(Cl, Chi_grid, axis=-1).real

        return Cl
