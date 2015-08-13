#!/usr/bin/env python

                            ##### This programme calculates de Teff and luminosity of the stars #####

### To run this, you should have:

###     Standard values (Kenyon and Hartmann 1995, Pecaut and Mamajet or other).
###     To calculate the Teff, you should know: the spectral type (SPT) in number.
###     To calculate the luminosity, you should know: the spectral type (SPT) in number, V magnitud, the extinction (AV) and the distance.

import numpy as np
import scipy
import scipy.interpolate
import matplotlib.pyplot as plt


                                    ##### Upload the data of the standard values #####

### Table of Kenyon and Hartmann 1995
tabla_KH  =  scipy.genfromtxt('/Users/aliceperez/Documents/Maestria/TESIS/Modelos/CODE/Teff_Lum/KH95B2.txt',comments='#',dtype= 'S')

Spt     =   tabla_KH[:,0].astype(float)
Teff    =   tabla_KH[:,1].astype(float)
BC      =   tabla_KH[:,2].astype(float)


### Table of Pecaut and Mamajet
tabla_PM = np.loadtxt('/Users/aliceperez/Documents/Maestria/TESIS/Modelos/CODE/Teff_Lum/Pecaut_Mamajek_5to30myr2.txt',  skiprows=1)

Spt     =   tabla_PM[:,0].astype(float)
Teff    =   tabla_PM[:,1].astype(float)
BC      =   tabla_PM[:,11].astype(float)


### Table with the data of the target
data = scipy.genfromtxt('/Users/aliceperez/Documents/Maestria/TESIS/Modelos/CODE/Teff_Lum/test2.txt',comments='#',dtype= 'S')

Star        =   data[:,0]                       # Name of the target
RA          =   data[:,1].astype(float)         # RA
DEC         =   data[:,2].astype(float)         # DEC
Spt_obj     =   data[:,3].astype(float)         # Spectral typy
V           =   data[:,4].astype(float)         # V magnitud
J           =   data[:,5].astype(float)         # J magnitud
d           =   data[:,6].astype(float)         # Distance of the cluster
Av          =   data[:,7].astype(float)         # Extinction


                           ############## Calculation of the Teff  ############

In_Teff     =   scipy.interpolate.UnivariateSpline(Spt,Teff,k=3,s=0)
Teff_s      =   In_Teff(Spt_obj)                                         # Teff in Kelvin.
TEFF        =   np.log10 (Teff_s)                                        # Log of the Teff

Tmax        =   In_Teff(Spt_obj - 2)
T1          =   np.log10(Tmax)
Tmin        =   In_Teff(Spt_obj + 2)
T2          =   np.log10(Tmin)

Err_s       =   Tmax - Tmin                                              # Error of the Teff


                            ############## Calculation of the Luminosity  ############

Inter_BC    =   scipy.interpolate.UnivariateSpline(Spt,BC,k=3,s=0)
BC_s        =   Inter_BC(Spt_obj)
Lsun        =   3.839e26

                        ##############  Absolute and bolometric Magnitude ##############

### V Absolute Magnitude
Mv          =   V + 5 - 5*(np.log10(d)) - Av
Mbol        =   Mv + BC_s

### J Absolute Magnitude
Mj          =   J + 5 - 5*(np.log10(d)) - 0.29*Av           #Aj/Av = 0.29 (Cardelli, Clayton and Mathis 1989)
Mbol        =   Mj + BC_s

            ############## Calculation of the luminosity in function of the Lsun: L = Log L*/Lsun ##############

L           =   ((-Mbol+4.74)/2.5)              # Log of the luminosity
LUM         =   10**(L)                         # Luminosity


                        ##############  To save the data ##############

### Estimate with V magnitud
file= open('TEFF_LUM_.txt','w')
file.write('#RA\t' 'DEC\t' 'Star\t' 'Spt_obj\t' 'Teff_s\t' 'Err_s\t' 'TEFF\t'  ' Mv\t' 'Mbol\t' 'L\t' ' LUM\t' 'Av\n')

for i in range(len(Teff_s)):
    file.write("%8f %9f %9s %3f %3f %3f %3f %3f %3f %3f %3e %3f\n" % (RA[i], DEC[i], Star[i], Spt_obj[i], Teff_s[i], Err_s[i], TEFF[i], Mv[i], Mbol[i], L[i], LUM[i], Av[i]))

file.close()

### Estimate with J magnitud
file= open('TEFF_LUM_.txt','w')
file.write('#RA\t' 'DEC\t' 'Star\t' 'Spt_obj\t' 'Teff_s\t' 'Err_s\t' 'TEFF\t'  ' Mj\t' 'Mbol\t' 'L\t' ' LUM\t' 'Av\n')

for i in range(len(Teff_s)):
    file.write("%8f %9f %9s %3f %3f %3f %3f %3f %3f %3f %3e %3f\n" % (RA[i], DEC[i], Star[i], Spt_obj[i], Teff_s[i], Err_s[i], TEFF[i], Mj[i], Mbol[i], L[i], LUM[i], Av[i]))

file.close()

