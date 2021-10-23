#!/usr/bin/env python3

# ~ https://dataportals.pangaea.de/bsrn/?q=LR0100

import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from pysolar.solar import *
import numpy as np
from scipy.special import lambertw
from libreria_clear_sky_models_panda import *


# get the number of the last line of header comment
def get_skip_pangaea( _filename ):
	skip_line = 0
	document = open( _filename , 'r+')
	with document as f:
		for line in f:
			skip_line += 1
			if "*/" in line:
				break
	document.close()

	''' import file as a panda object'''
	ds = pd.read_csv(_filename,
						sep='\t',
						lineterminator = "\n",
						skiprows= skip_line
					)
	return ds



def clear_minus_to_0(_col):
	if _col <0:
		_col = 0
	return _col



# get cenital angle
def theta_z_calculation( _col , _longitude, _latitude):
	col = Timestamp(_col, freq='MS').to_pydatetime()
	date = col.replace(tzinfo=datetime.timezone.utc)
	# ~ get_altitude(self.lat, self.lon, d)
	return ( 90-get_altitude(_latitude, _longitude, date) )



def check_if_value_is_in_range(_col, _max_std):
	std_col = _col
	max_std = _max_std

	if std_col<= max_std:
		return(1)
	return(0)



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



# get a and b parameter of SANCHEZ SEGuRA - PENA CRUZ K_n model
def compute_SSPCnormalDistribution_parameters(_theta_1, _DNI_1 , _theta_2 , _DNI_2, _Iext):
	''' y = a e**(b x**2)'''

	kt1 = 1 - _DNI_1 / _Iext
	kt2	= 1 - _DNI_2 / _Iext

	theta_z1 = _theta_1 * np.pi/180
	theta_z2 = _theta_2 * np.pi/180
	x1 = kt1 * np.sin(theta_z1)
	y1 = kt1 * np.cos(theta_z1)
	x2 = kt2 * np.sin(theta_z2)
	y2 = kt2 * np.cos(theta_z2)

	b =  np.real(  1/(x1**2-x2**2)*np.log(y1/y2) )
	a = y1 * (y1/y2)**(-x1**2/(x1**2-x2**2))
	# validation to obtain a real curve using a and b parametres
	sscp = compute_SSPC_using_a_b( theta_z1, a, b, 1000)

	# ~ print("sscp is: " , type(sscp) )
	# ~ print("sscp is nan: " , np.isnan(sscp) )
	# ~ print("sscp value: " , sscp)
	return ( a , b , sscp)



def compute_SSPC_using_a_b(_theta_z, a, b, _I_ext):
	theta_z1 = _theta_z * np.pi/180
	if _theta_z < 90:
		#productLogfunction
		w =  np.real(lambertw(-2*a**2*b*(np.tan(theta_z1))**2 ))
		x = 1 * (w)**0.5 /(2*-b)**0.5
		y = x /np.tan(theta_z1)
	else:
		x = 0
		y = 1
	kt = 1- (x**2 + y**2)**0.5
	if kt < 0:
		kt = 0
	SSPC = kt*_I_ext
	return (SSPC)





def main():
	# data
	save_document_name = "DB_.csv"

	''' ------------------------ '''
	filename_tl 	=	"Alert_TL.csv"		#Linke Turbidity coefficient data from soda
	path_base 		=	"ALE_radiation_"
	name_station 	=	"Alert"

	latitude	=	82.490000
	longitude	=	-62.420000
	elevation	=	127.0

	''' ------------------------ '''
	''' Reno's conditions'''
	max_std		= 	0.2		# max std permited inman
	max_M		=	75
	max_mean	=	75


	''' import linke turbidity data by months '''
	Tl_ds = get_tl_by_interpolation_soda( filename_tl )
	print('Tl_ds' , Tl_ds)

	ds = np.asarray([])
	for j in np.arange(2010 , 2020+1 , 1 ):
		for i in np.arange(1,12+1 , 1):
			if(i<10):
				path_df = path_base + str(j) + "-0" + str(i) + ".tab"
			else:
				path_df = path_base + str(j) + "-" + str(i) + ".tab"

			''' import data of pangaea '''
			try:
				if (ds.shape[0] == 0 ):
					ds = get_skip_pangaea( path_df )
				else:
					ds1 = get_skip_pangaea( path_df )
					ds = ds.append(ds1, ignore_index=True)
				print(path_df)
			except:
				r=1


	# Change time colum to format datetime
	ds["Date/Time"] =  pd.to_datetime(ds["Date/Time"], infer_datetime_format=True )
	ds['Time'] = ds["Date/Time"]

	# Ggt the number of days in the database
	qty_days = ( ds['Time'][ds.shape[0]-1] - ds['Time'][0] ).days +1
	print("Number of days to analyze: " , qty_days)

	day_analized = qty_days
	# define first and last time indetificator
	first_identificator = ds.iloc[0][0]
	last_identificator = ds.iloc[-1][0]

	''' set date/time as index '''
	ds = ds.set_index("Date/Time")

	# create a new objecto using only DNI value
	ds_dni = ds[['Time' , 'DIR [W/m**2]']]
	ds_dni.rename(columns = {"DIR [W/m**2]":'DNI'}, inplace = True)
	# cleaning  bad/inclomplete information by 0s
	ds_dni = ds_dni.fillna(0)

	# Change Negative irradiation to cero
	ds_dni['DNI'] = ds_dni['DNI'].apply(clear_minus_to_0)

	''' We create the colums to select a clear sky moment using a kernel of 10 x 1 centered '''
	# 1. Create filters which no use a clear sky model. Note: pysolar consume a lot of process
	ds_dni['mean'] = ds_dni['DNI'].rolling(10 , center=True).mean()
	ds_dni['s_t'] = ds_dni['DNI'].shift(1) - ds_dni['DNI']

	# to L (not used)
	ds_dni['L'] = ds_dni['s_t'].abs()
	ds_dni['L'] = ds_dni['L'].rolling(10 , center=True).sum()

	# Get rolling max value
	ds_dni['M'] = ds_dni['DNI'].rolling(10 , center=True).max()

	# to normalize standard deviation
	ds_dni['norm stdev'] = ds_dni['s_t'].rolling(10 , center=True).std()/ ds_dni['mean']

	ds_dni['stdev in range'] = ds_dni.apply(lambda x : check_if_value_is_in_range(x['norm stdev'], max_std) , axis=1 )
	ds_dni['clear sky'] = ds_dni['DNI'] * ds_dni['stdev in range']
	# eliminate the DNI that not is clear sky day filter by stdev

	# aprox 87% of informatios is eliminated
	print("Total data", ds_dni.shape)
	total_data_dowloaded = ds_dni.shape[0]
	ds_dni = ds_dni[ds_dni['clear sky'] > 0 ]

	# Creation of theta_z colum using pysolar, time colum and geografic location
	ds_dni['theta_z'] = ds_dni.apply( lambda  x : theta_z_calculation(x['Time'], longitude , latitude ) , axis=1)
	ds_dni = ds_dni[ds_dni['theta_z'] < 80 ]

	# Calculation of K_n model used as reference of clear sky day
	ds_dni['ESRA'] = ds_dni.apply( lambda x: ESRA_calculation_pandas(x['Time'], x['theta_z'], elevation , Tl_ds)  , axis=1) # elevation , Tl_ds , axis=1)

	ds_dni['mean'] 	=	( ds_dni['ESRA'] - ds_dni['mean'] )
	ds_dni['M'] 	=	( ds_dni['ESRA'] - ds_dni['M'] )
	
	ds_dni['mean'] 	=	ds_dni.apply(lambda x : check_if_value_is_in_range(x['mean'], max_mean) , axis=1 )
	ds_dni['M'] 	=	ds_dni.apply(lambda x : check_if_value_is_in_range(x['M'], max_M) , axis=1 )
	ds_dni['clear sky'] = ds_dni['DNI'] * ds_dni['mean'] * ds_dni['M']
	# eliminate the DNI that not is clear sky day filter by stdev

	# aprox 94.58% of informatios is eliminated
	ds_dni = ds_dni[ds_dni['clear sky'] > 0 ]
	total_data_used = ds_dni.shape[0]
	print("Data used:", total_data_used, "  " , total_data_used*100 /total_data_dowloaded,"%")
	# End filters

	''' Summary of important user data '''
	data_used_df = pd.DataFrame( {
							'Name'			:	[name_station],
							'Latitude'		:	[latitude],
							'Longitude'		:	[longitude] ,
							'Elevation'		:	[elevation] ,
							'Day analized'	:	[day_analized],
							'Total data'	:	[total_data_dowloaded] ,
							'CSI data'	:	[total_data_used]  #clear sky instants
							})
	
	data_used_df.to_csv("info_data_Recuperated.csv")



	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  #
	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  #
	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  #



	# Creating the first Dataframe using dictionary
	k_n_results = []

	#for iteration days
	for day_n_aux  in np.arange( qty_days ) :
		day_n = int(day_n_aux)
		start_day	=	first_identificator + datetime.timedelta(day_n)					+	datetime.timedelta( -longitude *0.5/180)
		end_day 	=	first_identificator + datetime.timedelta(day_n + 1-1/(24*60))	+	datetime.timedelta( -longitude *0.5/180)
		ds_dni_one_day =  ds_dni.loc[ start_day : end_day ]
		# check if data day exist
		if 	ds_dni_one_day.shape[0] > 1:
			print("Day analazing: " ,  start_day.date()  )
			ds_dni_one_day_aux = ds_dni_one_day

			# ----------------- SSPC k_n model ----------------- #
			# First_calculation of SSPC
			I_ext		= get_Ext_irradiance_pandas(ds_dni_one_day.iloc[0]['Time'] )
			theta_z_0	,	dni_0	=	25	, 	200
			theta_z_1	,	dni_1	=	37.5,	100

			# First a, b and sspc column
			a_sspc	,	 b_sspc , sscp	= compute_SSPCnormalDistribution_parameters(	theta_z_0 , dni_0 , theta_z_1 , dni_1 , I_ext)
			ds_dni_one_day_aux['SSPC'] 	= ds_dni_one_day.apply(lambda x : compute_SSPC_using_a_b( x['theta_z'], a_sspc , b_sspc , I_ext ),axis=1)

			# Definition of a an b coefficients [Diference between SSPC and DNI]
			ds_dni_one_day_aux['DNI - SSPC'] = ds_dni_one_day_aux['DNI'] - ds_dni_one_day_aux['SSPC']

			sspc_largest = ds_dni_one_day_aux.nlargest( ds_dni_one_day_aux.shape[0] , 'DNI - SSPC')
			theta_z_0 	=	sspc_largest.iloc[0]['theta_z']
			dni_0 		=	sspc_largest.iloc[0]['DNI']
			theta_z_1 	=	90
			dni_1 		=	0

			for i in np.arange(100):
				# get the 2 first largest DNI diference value
				decrement	=	0.1

				# define a y b sspc coefficients
				theta_z_1 	-=	decrement
				a_sspc_aux , b_sspc_aux , sscp= compute_SSPCnormalDistribution_parameters(	theta_z_0 , dni_0 , theta_z_1 , dni_1 , I_ext)

				if np.isnan(sscp) == False:
					a_sspc , b_sspc	=	a_sspc_aux , b_sspc_aux
					ds_dni_one_day_aux['SSPC'] = ds_dni_one_day_aux.apply(lambda x : compute_SSPC_using_a_b( x['theta_z'], a_sspc,b_sspc,I_ext),axis=1)
					ds_dni_one_day_aux['DNI - SSPC'] = ds_dni_one_day_aux['DNI'] - ds_dni_one_day_aux['SSPC']
					sspc_largest = ds_dni_one_day_aux.nlargest( ds_dni_one_day_aux.shape[0] , 'DNI - SSPC')

					if(dni_0 <= sspc_largest.iloc[0]['DNI']):
						theta_z_0 	=	sspc_largest.iloc[0]['theta_z']
						dni_0 		=	sspc_largest.iloc[0]['DNI']
					else:
						break

			sspc_largest = ds_dni_one_day_aux.nlargest( ds_dni_one_day_aux.shape[0] , 'DNI - SSPC')
			for k in np.arange(ds_dni_one_day_aux.shape[0]-1):
				# recalculate dots
				theta_z_1 	=	sspc_largest.iloc[k+1]['theta_z']
				dni_1 		=	sspc_largest.iloc[k+1]['DNI']
				a_sspc , b_sspc , sscp= compute_SSPCnormalDistribution_parameters(	theta_z_0 , dni_0 , theta_z_1 , dni_1 , I_ext)
				if np.isnan(sscp) == False and  a_sspc < 0.5 and  a_sspc > 0.1 and b_sspc < 0:

					ds_dni_one_day['SSPC'] =  ds_dni_one_day.apply(lambda x : compute_SSPC_using_a_b( x['theta_z'], a_sspc,b_sspc,I_ext),axis=1)
					ds_dni_one_day['DNI - SSPC'] = ds_dni_one_day['DNI'] - ds_dni_one_day['SSPC']

					''' Compute all clear sky models '''
					ds_dni_one_day['I_P'] 		=  ds_dni_one_day.apply(lambda x : Ineichen_Perez_calculation(I_ext, x['DNI'], elevation),axis=1)
					ds_dni_one_day['HLJ'] 		=  ds_dni_one_day.apply(lambda x : HLJ_calculation( I_ext , x['theta_z'] , elevation ),axis=1)
					ds_dni_one_day['Mghouchi'] 	=  ds_dni_one_day.apply(lambda x : El_Mghouchi_calculation( I_ext , x['theta_z'] , x['Time']),axis=1)
					ds_dni_one_day['Biga'] 		=  ds_dni_one_day.apply(lambda x : Biga_calculation(x['theta_z']),axis=1)
					ds_dni_one_day['FR1999'] 	=  ds_dni_one_day.apply(lambda x : FR1999_calculation( I_ext , x['theta_z'] , elevation ),axis=1)
					ds_dni_one_day['S1994'] 	=  ds_dni_one_day.apply(lambda x : S1994_calculation( I_ext , x['theta_z'] , elevation ),axis=1)
					ds_dni_one_day['DPP'] 		=  ds_dni_one_day.apply(lambda x : DPP_calculation(x['theta_z']),axis=1)
					ds_dni_one_day['M1976'] 	=  ds_dni_one_day.apply(lambda x : M1976_calculation( I_ext , x['theta_z'] ),axis=1)
					ds_dni_one_day['L1970'] 	=  ds_dni_one_day.apply(lambda x : L1970_calculation( I_ext , x['theta_z'] , elevation ),axis=1)
					ds_dni_one_day['Kasten'] 	=  ds_dni_one_day.apply(lambda x : Kasten_calculation(I_ext , x['theta_z'] , x['Time'] , elevation , Tl_ds) ,axis=1)
					ds_dni_one_day['SP1965'] 	=  ds_dni_one_day.apply(lambda x : SP1965_calculation( I_ext , x['theta_z']  ),axis=1)
					ds_dni_one_day['Hourwitz'] 	=  ds_dni_one_day.apply(lambda x : Hourwitz_calculation(  x['theta_z']  ),axis=1)
					break

			if a_sspc < 0.5 and  a_sspc > 0.1 and b_sspc < 0:
				''' statistical metrics '''
				t_l_a	=	T_L_by_a(elevation, a_sspc)
				pi = ds_dni_one_day['SSPC']
				oi = ds_dni_one_day['DNI']
				Om = oi.mean()
				Pm = pi.mean()
				N  = oi.shape[0]

				MBD		=	(100 / Om) * (pi - oi).mean() # Y. El Mghouchi
				MAPE	=	100 * ( ((pi - oi) / oi ).abs()).mean()
				RMSD 	= 	(100 / Om) * ( (pi - oi) ** 2 ).mean() ** 0.5
				MAD		=	(100 / Om) * ( (pi - oi).abs() ).mean()
				SD 		=	(100 / Om) * ( ((pi - oi)**2).sum()/ (N-2) )**0.5
				SBF		=	( (pi-Pm)*(oi-Om) ).sum() / ((oi-Om)**2).sum()
				U95		=	1.96  * (SD**2 + RMSD**2)**0.5
				TS		=	(  (N-1)*MBD**2 / (RMSD**2-MBD**2)    )**0.5
				NSE 	=	1 -  ( (pi-oi)**2 ).sum() / ((oi-Om)**2).sum()   #NSE is R2
				WIA		=	1 -  ( (pi-oi)**2 ).sum() / ( ( (pi-Om).abs() + (oi-Om).abs() )**2).sum()
				LCE		=	1 -  ( (pi - oi).abs() ).sum() /  ((oi-Om).abs() ).sum()

				# c charactristics
				# normalization of data
				pi_norm = (pi - pi.mean()) / (pi.max() - pi.min())
				oi_norm = (oi - oi.mean()) / (oi.max() - oi.min())

				Dn = (pi_norm - oi_norm).abs()
				N_2 = 0
				for i in np.arange(Dn.shape[0]-1):
					N_2 += 1

				Dc = 1.63 / N_2**0.5
				Ac_norm = Dc * ( pi_norm.max() - oi_norm.min() )
				Ac = Dc * ( pi.max() - pi.min() )

				Area_KSI 	= 0
				Area_OVER 	= 0
				
				# Trapezoidal Rule of Integration
				for i in np.arange(Dn.shape[0]-1):
					if Dn.index[i+1].minute - Dn.index[i].minute == 1:
						Area_KSI += ( Dn.iloc[i] + Dn.iloc[i+1] ) / 2
						if Dn.iloc[i]-Dc > 0  and Dn.iloc[i+1]-Dc > 0:
							Area_OVER += (Dn.iloc[i]-Dc + Dn.iloc[i+1]-Dc)/2

				KSI	= 	100/Ac * Area_KSI
				OVER=	100/Ac * Area_OVER
				CPI	=	(KSI + OVER + 2*RMSD) / 4 ## aaaa rmseeee

				KSI_norm	= 	100/Ac_norm * Area_KSI
				OVER_norm =	100/Ac_norm * Area_OVER
				CPI_norm	=	(KSI_norm + OVER_norm + 2*RMSD) / 4 ## aaaa rmseeee

				# RMSD calculation for other models
				ESRA 	= 	(100 / Om) * ( (ds_dni_one_day['ESRA'] 		- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				I_and_P = 	(100 / Om) * ( (ds_dni_one_day['I_P'] 		- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				HLJ 	= 	(100 / Om) * ( (ds_dni_one_day['HLJ'] 		- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				Mghouchi= 	(100 / Om) * ( (ds_dni_one_day['Mghouchi'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				Biga 	= 	(100 / Om) * ( (ds_dni_one_day['Biga'] 		- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				FR1999 	= 	(100 / Om) * ( (ds_dni_one_day['FR1999'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				S1994 	= 	(100 / Om) * ( (ds_dni_one_day['S1994'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				DPP 	= 	(100 / Om) * ( (ds_dni_one_day['DPP'] 		- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				M1976 	= 	(100 / Om) * ( (ds_dni_one_day['M1976'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				L1970 	= 	(100 / Om) * ( (ds_dni_one_day['L1970'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				Kasten 	= 	(100 / Om) * ( (ds_dni_one_day['Kasten'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				SP1965 	= 	(100 / Om) * ( (ds_dni_one_day['SP1965'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5
				Hourwitz= 	(100 / Om) * ( (ds_dni_one_day['Hourwitz'] 	- ds_dni_one_day['DNI']) ** 2 ).mean() ** .5


				# Creating of array to save in Dataframe using dictionary
				k_n_results_aux = {
							'Date'		:	start_day.date(),
							'I_ext'		:	I_ext ,
							'a'	:	a_sspc ,
							'b'	:	b_sspc ,
							'Tl_a'	:	t_l_a ,
							'SSPC_MBD'	:	MBD ,
							'SSPC_MAPD'	:	MAPE,
							'SSPC_RMSD'	:	RMSD ,
							'SSPC_MAD'	:	MAD ,
							'SSPC_SD'	:	SD ,
							'SSPC_NSE_o_R2'	:	NSE ,
							'SSPC_SBF'	:	SBF ,
							'SSPC_U95'	:	U95 ,
							'SSPC_TS'	:	TS ,
							'SSPC_WIA'	:	WIA ,
							'SSPC_LCE'	:	LCE ,
							'SSPC_KSI'	:	KSI ,
							'SSPC_OVER'	:	OVER ,
							'SSPC_CPI'	:	CPI ,

							'SSPC_KSI_norm'	:	KSI_norm ,
							'SSPC_OVER_norm':	OVER_norm ,
							'SSPC_CPI_norm'	:	CPI_norm ,

							# RMSD of other Kn models 
							'ESRA_RMSD'		:	ESRA ,
							'I&P_RMSD'		:	I_and_P ,
							'HLJ_RMSD'		:	HLJ ,
							'Mghouchi_RMSD'	:	Mghouchi ,
							'Biga_RMSD'		:	Biga ,
							'FR1999_RMSD'	:	FR1999 ,
							'S1994_RMSD'		:	S1994 ,
							'DPP_RMSD'		:	DPP ,
							'M1976_RMSD'		:	M1976 ,
							'L1970_RMSD'		:	L1970 ,
							'Kasten_RMSD'	:	Kasten ,
							'SP1965_RMSD'	:	SP1965 ,
							'Hourwitz_RMSD'	:	Hourwitz,
							'Om':	Om
							}

				k_n_results.append( k_n_results_aux	)

	df_k_n_results = pd.DataFrame( k_n_results ).round(4)
	df_k_n_results.to_csv(save_document_name)

	print(df_k_n_results)

if __name__ == '__main__':
	main()
