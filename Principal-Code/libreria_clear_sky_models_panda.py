#!/usr/bin/env python3
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
import datetime 
import matplotlib.pyplot as plt
from pysolar.solar import *
import numpy as np
from scipy.special import lambertw





''' Extraterrestial functions  implementations '''
def get_Ext_irradiance_pandas(_time ):
	# Calculed like: Worldwide performance assessment of 75 global clear-sky irradiance models using Principal Component Analysis
	day_time	= Timestamp(_time, freq='MS').to_pydatetime()
	N			= day_time.timetuple().tm_yday
	I_0 = 1361.2 # extaterrestrial solar irradiance [w/m2]
	c = np.pi/180
	c_360 = 360*(N-1)/365*c
	fac1 = 1.00011 + 0.034221* np.cos(c_360)
	fac2 = 0.00128 * np.sin(c_360) + 0.000719*np.cos(2*c_360)
	fac3 = 0.000077 * np.sin(2*c_360)

	I_ext = I_0 * ( fac1 + fac2 + fac3)
	return(I_ext)

'''	ESRA MODEL '''
# get ESRA value
def ESRA_calculation_pandas(_time , _theta_z ,  _altura, _Tl_ds): #,): # altitud modificar
	#get julian day and month number
	day_time	= Timestamp(_time, freq='MS').to_pydatetime()
	# ~ N			= day_time.timetuple().tm_yday
	month 		= day_time.strftime("%m")
	# ~ Bc -> DNI ESRA clear sky
	I_exp 		= 	get_Ext_irradiance_pandas( _time ) #1367  --- I_exp * epsilon 
	altitud 	= 	(90-_theta_z)*np.pi/180
	T_L 		=  _Tl_ds.loc[ int(month) ]['T_l'] # TL(AM2) is the Linke turbidity factor for an air mass equal to 2;
	''' relative optical air mass '''
	altura		=  _altura    #  347
	altura_h	= 8434.5
	p_p0		= np.exp(-altura/altura_h) 
	altitud_ref = 0.061359 * ( 0.1594 + 1.1230*altitud + 0.065656*altitud**2) / ( 1 + 28.9344*altitud + 277.3971*altitud**2) # sin 180 / pi , ya esta en rad
	altitud_true= altitud + altitud_ref
	aux 		= np.sin(altitud_true) + 0.50572 * (altitud_true*180/np.pi + 6.0995)**(-1.6364)
	m = p_p0 / aux    #relative optical air mass
	# ~ print(m)
	''' Rayleigh optical thickness '''
	if m <= 20:
		delta_r = 1 / (6.62960 + 1.75130*m-0.12020*m**2+0.00650*m**3-0.00013*m**4)
	else: 
		delta_r = 1 / (10.4+0.718*m)		
	if _theta_z >90 or _theta_z <0:
		Bc = 0
	else:
		Bc = I_exp  * np.exp(-0.8662 * T_L * m * delta_r ) # quitamos el sin(altitud) para corregir
	''' Original '''
	# ~ Bc = I_exp *np.sin(altitud) * np.exp(-0.8662 * T_L * m * delta_r )
	
	return(Bc ) #*np.cos(_theta_z*np.pi/180))


def T_L_by_a(_altura, _a): # altitud modificar	
	altitud 	= 	(90)*np.pi/180	
	''' relative optical air mass '''
	altura =  _altura    #  347
	altura_h = 8434.5
	p_p0 = np.exp(-altura/altura_h) 
	altitud_ref = 0.061359 * ( 0.1594 + 1.1230*altitud + 0.065656*altitud**2) / ( 1 + 28.9344*altitud + 277.3971*altitud**2) # sin 180 / pi , ya esta en rad
	altitud_true = altitud + altitud_ref
	aux = np.sin(altitud_true) + 0.50572 * (altitud_true*180/np.pi + 6.0995)**(-1.6364)
	m = p_p0 / aux    #relative optical air mass
	# ~ print(m)
	''' Rayleigh optical thickness '''
	if m <= 20:
		delta_r = 1 / (6.62960 + 1.75130*m-0.12020*m**2+0.00650*m**3-0.00013*m**4)
	else: 
		delta_r = 1 / (10.4+0.718*m)		
	T_L = np.log(1-_a) / (-0.8662 * m * delta_r )
	return(T_L)


def ESRA_calculation_puntos(_I_exp, _theta_z, _altura, _T_L): # altitud modificar
	''' Validating nine clear sky radiation models in Australia '''
	''' 
		On the clear sky model of the ESRA - European Solar
		Radiation Atlas with respect to the Heliosat method
		Christelle Rigollier, Olivier Bauer, Lucien Wald
	'''
	# ~ Bc -> DNI ESRA clear sky
	I_exp 		= 	_I_exp #1367  --- I_exp * epsilon 
	altitud 	= 	(90-_theta_z)*np.pi/180	
	T_L= _T_L# TL(AM2) is the Linke turbidity factor for an air mass equal to 2;
	''' relative optical air mass '''
	altura =  _altura    #  347
	altura_h = 8434.5
	p_p0 = np.exp(-altura/altura_h) 
	altitud_ref = 0.061359 * ( 0.1594 + 1.1230*altitud + 0.065656*altitud**2) / ( 1 + 28.9344*altitud + 277.3971*altitud**2) # sin 180 / pi , ya esta en rad
	altitud_true = altitud + altitud_ref
	aux = np.sin(altitud_true) + 0.50572 * (altitud_true*180/np.pi + 6.0995)**(-1.6364)
	m = p_p0 / aux    #relative optical air mass
	# ~ print(m)
	''' Rayleigh optical thickness '''
	if m <= 20:
		delta_r = 1 / (6.62960 + 1.75130*m-0.12020*m**2+0.00650*m**3-0.00013*m**4)
	else: 
		delta_r = 1 / (10.4+0.718*m)		
	Bc = I_exp  * np.exp(-0.8662 * T_L * m * delta_r ) # quitamos el sin(altitud) para corregir
	''' Original '''
	# ~ Bc = I_exp *np.sin(altitud) * np.exp(-0.8662 * T_L * m * delta_r )
	return(Bc)


# get t_l by soda data base
def get_skip_tl_by_soda( _filename_tl ):
	skip_line = 0
	document = open( _filename_tl , 'r+') 
	with document as f:
		for line in f:
			if "Month;Tl" in line:
				break
			skip_line += 1
	document.close()
	''' import file as a panda object'''
	soda_tl = pd.read_csv(_filename_tl, 
						sep=';', 
						lineterminator = "\n",
						skiprows= skip_line
					)
	soda_tl.rename(columns = {"# Month":'Month' , 'Tl 2010' : 'T_l'}, inplace = True)
	soda_tl = soda_tl.set_index('Month')
	return soda_tl


# get t_l by soda data base
def get_tl_by_interpolation_soda( _filename_tl ):
	soda_tl = pd.read_csv(_filename_tl, 
						sep=',', 
						lineterminator = "\n"
					)
	soda_tl.rename(columns = {"Month":'Month' , 'T_L' : 'T_l'}, inplace = True)
	soda_tl = soda_tl.set_index('Month')
	return soda_tl


'''
Ineichen, Pierre
Perez, Richard

"A new airmass independent formulation for the linke turbidity coefficient"

'''




def Ineichen_Perez_calculation(_I_ext, _Bn, _altura):  
	I_ext	= 	_I_ext 
	Bn = _Bn
	altura = _altura
	
	AM = 2
	T_lk = np.log(I_ext / Bn )*(9.4+0.9* AM)/AM
	f_h1 = np.exp(-altura /8000)
	b = 0.664+0.163/f_h1
	
	Bc = b*I_ext* np.exp(-0.09 * AM *(T_lk-1))
	
	return(Bc)

def HLJ_calculation( _I_ext , _theta_z , _altitude ):
	I_ext	= 	_I_ext 
	theta_z = _theta_z*np.pi/180
	A = _altitude/1000
	
	
	a0 	= 0.2538 - 0.0063*(6 - A)**2
	a1 	= 0.7678 + 0.0010*(6.5-A)**2
	k	=	0.249+0.081*(2.5-A)**2
	
	tau = a0 + a1 * np.exp (-k *1/np.cos(theta_z))
	Bn = tau*I_ext
	return(Bn)



def yearDayFunction_aux(_time):
	day_time	= Timestamp(_time, freq='MS').to_pydatetime()
	N			= day_time.timetuple().tm_yday
	return(N)


def El_Mghouchi_calculation(_I_ext , _theta_z , _vec_date):
	
	I_ext	= 	_I_ext #1367 
	theta_z = _theta_z*np.pi/180
	j = yearDayFunction_aux (_vec_date)
	T = 0.769 - 0.01 *np.sin(0.986*(j+284) *np.pi/180)
	C_t = 1 +0.034*np.cos(( j-2) *np.pi/180)
	
	
	Bn = I_ext * C_t * T * np.exp(-0.13 / np.cos(theta_z) ) * np.cos(theta_z) 
	return(Bn)





def Biga_calculation(_theta_z):
	theta_z = _theta_z*np.pi/180
	
	c= 0.93 #1.05 #
	I = 926* (np.cos(theta_z))**0.29
	D = 125 * (np.cos(theta_z))**0.40
	
	E = D /(c*np.cos(theta_z)) + I
	return(I)  #puede ser I

''' Clear sky irradiance models: areviwe of seventy models '''
def FR1999_calculation(_I_ext , _theta_z , _altitude): 
	I_ext	= 	_I_ext
	theta_z = _theta_z*np.pi/180
	A = _altitude
	
	k = np.exp(1.18*10**(-4) * A -1.638*10**(-9)*A**2 ) / np.cos(theta_z)
	
	Bn = I_ext	*0.5**k
	
	return (Bn)
	
def S1994_calculation(_I_ext , _theta_z , _altitude): 
	I_ext	= 	_I_ext
	theta_z = _theta_z*np.pi/180
	A = _altitude/1000
	
	k = 1- np.exp(-36 / np.pi * (np.pi/2 - theta_z))
	Bn = I_ext * ( (1-0.14*A)*np.exp(-0.357/ (np.cos(theta_z)**0.678) + 0.14*A*k) )

	return (Bn)


def DPP_calculation( _theta_z): 
	theta_z = _theta_z*np.pi/180
	
	B0 = 950 * (1 - np.exp(-0.075*(90 - _theta_z ))) * np.cos(theta_z)
	
	return(B0)

def M1976_calculation(_I_ext , _theta_z): 
	I_ext	= 	_I_ext
	theta_z = _theta_z*np.pi/180
	
	Bn = I_ext * 0.7**(1/np.cos(theta_z))**0.678
	return (Bn)

def L1970_calculation(_I_ext , _theta_z , _altitude): 
	I_ext	= 	_I_ext
	theta_z = _theta_z*np.pi/180
	A = _altitude/1000
	
	Bn = I_ext *( (1-0.14*A) *0.7**(1/np.cos(theta_z))**0.678 + 0.14*A)
	return (Bn)


def Kasten_calculation(_I_ext , _theta_z , _time , _altitude , _Tl_ds ): 
	
	#get julian day and month number
	day_time	= Timestamp(_time, freq='MS').to_pydatetime()
	# ~ N			= day_time.timetuple().tm_yday
	month 		= day_time.strftime("%m")
	I_ext	= 	_I_ext
	theta_z = _theta_z*np.pi/180
	A = _altitude/1000
	T_L 		=  _Tl_ds.loc[ int(month) ]['T_l'] # TL(AM2) is the Linke turbidity factor for an air mass equal to 2;
	
	
	altitud 	= 	(90-_theta_z)*np.pi/180
	''' relative optical air mass '''
	altura =  _altitude    #  347
	altura_h = 8434.5
	p_p0 = np.exp(-altura/altura_h) 	
	altitud_ref = 0.061359 * ( 0.1594 + 1.1230*altitud + 0.065656*altitud**2) / ( 1 + 28.9344*altitud + 277.3971*altitud**2) # sin 180 / pi , ya esta en rad
	altitud_true = altitud + altitud_ref
	aux = np.sin(altitud_true) + 0.50572 * (altitud_true*180/np.pi + 6.0995)**(-1.6364)
	airMass = p_p0 / aux    #relative optical air mass
	
	Bn = I_ext *( 0.664 + 0.163/np.exp(-A/8000) ) * np.exp(-0.09*airMass*(T_L-1))
	return (Bn)
	
	
def SP1965_calculation(_I_ext , _theta_z):
	I_ext	= 	_I_ext
	theta_z = _theta_z*np.pi/180
	
	Bn = 1.842* I_ext/2 *np.cos(theta_z)/(0.3135 + np.cos(theta_z))
	return (Bn)	
	
	
def Hourwitz_calculation( _theta_z):
	theta_z = _theta_z*np.pi/180
	
	Bn = 1098*np.exp(-0.057/np.cos(theta_z))
	return (Bn)	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


