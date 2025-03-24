#gather all config parameters here
import numpy as np

################ red shift binning

z_max = 5.0 #highest redshift.
z_min = 0.2 #lowest redshift.

E_estim_signal_lmax = 100
T_estim_signal_lmax = 1000
psz_estim_signal_lmax = 1000

ksz_estim_signal_lmax = 100
N_bins = 4 #number of red shift bins, uniform in conformal distance.

transfer_integrand_sampling = 1000

################ halomodel

use_halomodel = True #set false to speed up. if false, the bias is taken as z+1 and eg Pgg= b^2 P_mm_camb.
gasprofile = 'AGN' #only used if use_halomodel=True
A_electron = 1  # This parameter interpolates between Pk of electrons and Pk of dark matter. It serves to test dependence on fiducial model of electrons. 1 is full electron model.
halomassfunction = 'Tinker'
mdef = 'm200d'

################ LSS

lss_shot_noise = True
LSSexperiment = 'LSST' #can be 'ngalsMpc3Fixed' or 'LSST'  #if not fixed, this selects the HODthreshold for a given experiment. Must be implemented in galaxies.py.
ngalsMpc3Fixed = 0.01 #only used when LSSexperiment='ngalsMpc3Fixed' and use_halomodel = True
sigma_photo_z = 0.05 #0.05
galaxy_selection = 'all' # This can be 'red', 'blue', or 'all' galaxies,
                         # or 'off' for constant biases in fig. 1 of 1505.07596.
rmax = 25.3
sigma_cal = 1e-4 # variance of photometric calibration erros (as appearing in arXiv:1709.08661)

dndz = None
unwisecolour = 'blue'

################ cosmological parameters

As = 2.2
Omega_m = 0.31
Omega_b = 0.049
Omega_c=Omega_m-Omega_b
Omega_r_h2 = 4.15 * 10**-5
mnu = 0.06

h = 0.68
H0 = h * 100
ns = 0.965

ombh2 = Omega_b*h**2
omch2=Omega_c*h**2

Omega_r = 9.236 * 10**-5
Omega_K = 0.0
w = -1.0
wa = 0.0
zdec = 1090 # Redshift at decoupling
adec = 1 / (1 + zdec) # Scale factor at decoupling
tau = 0.06 # Optical depth to reionization
T_CMB = 2.725*10.**6. # muK
fNL = 0.0
delta_collapse = 1.686 # Linearized collapse threshold


################ Tracers from camb

camb_tracers = ['pCMB']

################ CMB experimental noise

#CMB noise
cmb_experimental_noise = True #set false to switch it off
beamArcmin_T = 1.0 # S4
noiseTuKArcmin_T = 1.0 # 1.5 S4
beamArcmin_pol = 1.0
noiseTuKArcmin_pol = 1.0 #1.5

################ k sampling for direct transfer integration

# k_min = -5  #logscale
# k_max = 1.4  #logscale
# kaux = np.append(np.logspace(k_min, -3, 200),np.logspace(-2.99, k_max, 10000))


# ################ k sampling for direct transfer integration
# k_min = 0.0001
# k_max = 0.001
# kaux = np.linspace(k_min, k_max, 200)

k_min = -5  #logscale
k_max = -1.9  #logscale
k_res = 200

# pivot scale
k0 = 0.05

if k_max<=-3:
    kaux = np.logspace(k_min, k_max, k_res)
else:
    kaux = np.append(np.logspace(k_min, -3, 200),np.logspace(-2.99, k_max, 10000))

log_kmax = -2
log_kmin = -5
k_res = 1000
ks_hm = np.logspace(log_kmin,log_kmax,num=k_res)     #k-sampling
zs_hm = np.logspace(-2,np.log10(6),150) #z-sampling

k0 = 0.05


###CIB info
CIB_model = 'Websky'

################ Cleaning tags
cleaning_mode = 'SO'
cleaning_frequencies = {'Planck' : np.array([30,44,70,100,143,217,353,545,857]), 'SO' : np.array([27,39,93,145,225,280]), 'DoubleSO' : np.round(np.concatenate([np.linspace(10,120,10),np.linspace(125,165,8),np.logspace(np.log10(177),np.log10(1500),20)]),0)[1:-1:3]}
