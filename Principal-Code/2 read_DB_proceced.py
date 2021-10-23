#!/usr/bin/env python3

# ~ https://dataportals.pangaea.de/bsrn/?q=LR0100

import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
import datetime 
import matplotlib.pyplot as plt
from pysolar.solar import *
import numpy as np
from scipy.special import lambertw
from libreria_clear_sky_models_panda import *
from matplotlib import rc
rc('text', usetex=True)
rc('font', family='serif')




def check_month(_time):
	day_time	= Timestamp(_time, freq='MS').to_pydatetime()
	month 		= day_time.strftime("%m")
	return(int(month) ) 



def main():	
	# data
	filename = "DB_.csv"
	file_rmse_save = "data_results_.csv"
	file_tl_save = "TL_from_a_monthly_.csv"
	
	ds = pd.read_csv(filename)
	d_recuperated = pd.read_csv('info_data_Recuperated.csv')
	
	
	# Change time colum to format datetime
	ds["Date"] =  pd.to_datetime(ds["Date"], infer_datetime_format=True )
	ds['Time'] = ds["Date"]
	ds.pop('Unnamed: 0')
	''' set date/time as index '''
	ds = ds.set_index("Date")
	print(ds)
	
	ds['month'] = ds.apply(lambda x: check_month(x['Time']) , axis =1 )	
	tl_mean = pd.DataFrame( {
				'Jan'	:	[	ds['Tl_a'][ds['month'] == 1].mean()	],
				'Feb'	:	[	ds['Tl_a'][ds['month'] == 2].mean()	],
				'Mar'	:	[	ds['Tl_a'][ds['month'] == 3].mean()	],
				'Apr'	:	[	ds['Tl_a'][ds['month'] == 4].mean()	],
				'May'	:	[	ds['Tl_a'][ds['month'] == 5].mean()	],
				'June'	:	[	ds['Tl_a'][ds['month'] == 6].mean()	],
				'July'	:	[	ds['Tl_a'][ds['month'] == 7].mean()	],
				'Aug'	:	[	ds['Tl_a'][ds['month'] == 8].mean()	],
				'Sept'	:	[	ds['Tl_a'][ds['month'] == 9].mean()	],
				'Oct'	:	[	ds['Tl_a'][ds['month'] == 10].mean()],
				'Nov'	:	[	ds['Tl_a'][ds['month'] == 11].mean()],
				'Dec'	:	[	ds['Tl_a'][ds['month'] == 12].mean()]
				} ).T.round(4)
	
	tl_mean.to_csv(file_tl_save)
	print("tl_mean", tl_mean)
			
	# Creating of array to save in Dataframe using dictionary
	data_results = ds[[	'SSPC_MBD' , 'SSPC_MAPD' ,'SSPC_RMSD','SSPC_MAD','SSPC_SD',
						'SSPC_NSE_o_R2','SSPC_SBF','SSPC_U95','SSPC_TS','SSPC_WIA',
						'SSPC_LCE','SSPC_KSI','SSPC_OVER','SSPC_CPI','SSPC_KSI_norm',
						'SSPC_OVER_norm','SSPC_CPI_norm',
						
						'ESRA_RMSD',
						'I&P_RMSD','HLJ_RMSD',
						'Mghouchi_RMSD','Biga_RMSD','FR1999_RMSD','S1994_RMSD',
						'DPP_RMSD','M1976_RMSD','L1970_RMSD','Kasten_RMSD',
						'SP1965_RMSD','Hourwitz_RMSD', 'Om']].mean().round(2)
	
	data_to_save = pd.DataFrame( {
							'Name'			:	[d_recuperated.iloc[0,1]],
							'Latitude'		:	[d_recuperated.iloc[0,2]],
							'Longitude'		:	[d_recuperated.iloc[0,3]] ,
							'Elevation'		:	[d_recuperated.iloc[0,4]] ,
							'Analized days'	:	[d_recuperated.iloc[0,5]],
							'Total data'	:	[d_recuperated.iloc[0,6]] ,				
							'CSI data'		:	[d_recuperated.iloc[0,7]] , #clear sky instants
							
							'SSPC_MBD'	:	[data_results[0]], 
							'SSPC_MAPD'	:	[data_results[1]],
							'SSPC_MAD' 	:	[data_results[3]],
							'SSPC_RMSD'	:	[data_results[2]],
							'SSPC_SD':	[data_results[4]],
							'SSPC_NSE_o_R2'	:	[data_results[5]],
							'SSPC_SBF':	[data_results[6]],
							'SSPC_U95' :	[data_results[7]],
							'SSPC_TS' 	:	[data_results[8]],
							'SSPC_WIA'	:	[data_results[9]],
							'SSPC_LCE' :	[data_results[10]],
							'SSPC_KSI':	[data_results[11]],
							'SSPC_OVER':	[data_results[12]],
							'SSPC_CPI':	[data_results[13]],
							'SSPC_KSI_norm':	[data_results[14]],
							'SSPC_OVER_norm':	[data_results[15]],
							'SSPC_CPI_norm':	[data_results[16]],
							
							
							'ESRA_RMSD'	:	[data_results[17]], 
							'I&P_RMSD':	[data_results[18]],
							'HLJ_RMSD'	:	[data_results[19]],
							'Mghouchi_RMSD':	[data_results[20]],
							'Biga_RMSD' :	[data_results[21]],
							'FR1999_RMSD' 	:	[data_results[22]],
							'S1994_RMSD'	:	[data_results[23]],
							'DPP_RMSD' :	[data_results[24]],
							'M1976_RMSD':	[data_results[25]],
							'L1970_RMSD':	[data_results[26]],
							'Kasten_RMSD':	[data_results[27]],
							'SP1965_RMSD'	:	[data_results[28]], 
							'Hourwitz_RMSD'	:	[data_results[29]],
							#'Om'	:	[data_results[30]]
							})
	data_to_save.to_csv(file_rmse_save)
	print(data_to_save)

if __name__ == '__main__':
	main()

