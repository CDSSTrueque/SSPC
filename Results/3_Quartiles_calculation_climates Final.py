#!/usr/bin/env python3
# ~ https://dataportals.pangaea.de/bsrn/?q=LR0100

import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
import datetime
import math
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from pysolar.solar import *
import numpy as np
from scipy.special import lambertw
import matplotlib.pyplot as plt # importando matplotlib
import seaborn as sns # importando seaborn
import io


from matplotlib import rc
rc('font', family='serif')




def main():
	
	
	

	# data
	save_document_name = "DB_.csv"

	# download statistical results 
	filename = "statistical_results_compilation.csv"
	df = pd.read_csv(filename, encoding = 'unicode_escape', engine ='python')
	
	# ~ print(df.head())
	
	''' Filter data frame by weather''' 
	df_A =  df[df['Weather'] == 'A']
	df_B =  df[df['Weather'] == 'B']
	df_C =  df[df['Weather'] == 'C']
	df_D =  df[df['Weather'] == 'D']
	df_E =  df[df['Weather'] == 'E']
	# ~ print(df_A)
	
	
		
	
	
	

	

	'''------------------------------------'''
	''' Class A and B statistical metrics  '''
	'''------------------------------------'''
	data_A = [	
				df_A['SSPC_MBD'],		df_A['SSPC_RMSD'],	df_A['SSPC_MAPD'],	df_A['SSPC_MAD'],	df_A['SSPC_SBF'],
			]
	data_B = [	
				df_B['SSPC_MBD'],		df_B['SSPC_RMSD'],	df_B['SSPC_MAPD'],	df_B['SSPC_MAD'],	df_B['SSPC_SBF'],
			]
	data_C = [	
				df_C['SSPC_MBD'],		df_C['SSPC_RMSD'],	df_C['SSPC_MAPD'],	df_C['SSPC_MAD'],	df_C['SSPC_SBF'],
			]
	data_D = [	
				df_D['SSPC_MBD'],		df_D['SSPC_RMSD'],	df_D['SSPC_MAPD'],	df_D['SSPC_MAD'],	df_D['SSPC_SBF'],
			]
	data_E = [	
				df_E['SSPC_MBD'],		df_E['SSPC_RMSD'],	df_E['SSPC_MAPD'],	df_E['SSPC_MAD'],	df_E['SSPC_SBF'],
			]
	data_G = [	
				df['SSPC_MBD'],		df['SSPC_RMSD'],		df['SSPC_MAPD'],	df['SSPC_MAD'], 	df['SSPC_SBF'],
			]
	
	
	
	fig = plt.figure(1, figsize=(6, 3))
	ax = plt.gca()
	line_width = 2
	c = "blue"		
	r = 1
	m = 7
	boxes0 = ax.boxplot(data_G, positions=[r , r+m , r+2*m , r+3*m	, r+4*m ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'',''
							],
				capprops=dict(color=c, linewidth = line_width), whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ), medianprops=dict(color='red', linewidth = line_width),patch_artist=True, boxprops=dict(facecolor=c )
			)
	
	
	
	c = "green"	
	r = 2
	boxes1 = ax.boxplot(data_A, positions=[r , r+m , r+2*m , r+3*m	, r+4*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' ,'' ,'' ,'',''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "purple"		
	r = 3
	boxes2 = ax.boxplot(data_B, positions=[r , r+m , r+2*m , r+3*m	, r+4*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'MBD' , 'RMSD' ,'MAPD' ,'MAD', 'SBF'
							],
							
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)
	c = "black"		
	r = 4
	boxes3 = ax.boxplot(data_C, positions=[r , r+m , r+2*m , r+3*m	, r+4*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'',''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "gray"		
	r = 5
	boxes4 = ax.boxplot(data_D, positions=[r , r+m , r+2*m , r+3*m	, r+4*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'',''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "orange"		
	r = 6
	boxes5 = ax.boxplot(data_E, positions=[r , r+m , r+2*m , r+3*m	, r+4*m ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'',''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)				
	
	plt.legend([boxes0["boxes"][0], boxes1["boxes"][0], boxes2["boxes"][0], boxes3["boxes"][0], boxes4["boxes"][0], boxes5["boxes"][0]], ['Global','Equatorial', 'Arid', 'Temperate' , 'Cold' , 'Polar'], loc='upper right')
	ax.set_ylabel("Difference [$\\%$]", fontsize=14,color='black' ,  usetex=True)
	ax.grid(True)
	plt.xticks(fontsize=12 ,  usetex=True),plt.yticks(fontsize=12 ,  usetex=True)
	plt.tight_layout()
	fig.savefig('Class_a_b_metrics_1.pdf')
	plt.show()



	''' second  '''
	
	# ~ ,'SBF' ,'NSE' ,'WIA' ,'LCE' 
	
	data_A_2 = [	
					df_A['SSPC_NSE_o_R2'],	df_A['SSPC_WIA'],	df_A['SSPC_LCE'] 
			]
	data_B_2 = [	
				df_B['SSPC_NSE_o_R2'],	df_B['SSPC_WIA'],	df_B['SSPC_LCE'] 
			]
	data_C_2 = [	
				df_C['SSPC_NSE_o_R2'],	df_C['SSPC_WIA'],	df_C['SSPC_LCE'] 
			]
	data_D_2 = [	
				df_D['SSPC_NSE_o_R2'],	df_D['SSPC_WIA'],	df_D['SSPC_LCE'] 
			]
	data_E_2 = [	
				df_E['SSPC_NSE_o_R2'],	df_E['SSPC_WIA'],	df_E['SSPC_LCE'] 
			]
	data_G_2 = [	
				df['SSPC_NSE_o_R2'],df['SSPC_WIA'],	df['SSPC_LCE'] 
			]
	
	fig = plt.figure(1, figsize=(6, 3))
	ax = plt.gca()
	line_width = 2
	c = "blue"		
	r = 1
	boxes0 = ax.boxplot(data_G_2, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								 '' ,'' ,''
							],
				capprops=dict(color=c, linewidth = line_width), whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ), medianprops=dict(color='red', linewidth = line_width),patch_artist=True, boxprops=dict(facecolor=c )
			)
	
	
	
	c = "green"	
	r = 2
	boxes1 = ax.boxplot(data_A_2, positions=[r , r+m , r+2*m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' ,'' ,''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "purple"		
	r = 3
	boxes2 = ax.boxplot(data_B_2, positions=[r , r+m , r+2*m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'NSE' ,'WIA' ,'LCE' 
							],
							
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)
	c = "black"		
	r = 4
	boxes3 = ax.boxplot(data_C_2, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' ,'' ,''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "gray"		
	r = 5
	boxes4 = ax.boxplot(data_D_2, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								 '' ,'' ,''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "orange"		
	r = 6
	boxes5 = ax.boxplot(data_E_2, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								 '' ,'' ,''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)				
	
	plt.legend([boxes0["boxes"][0], boxes1["boxes"][0], boxes2["boxes"][0], boxes3["boxes"][0], boxes4["boxes"][0], boxes5["boxes"][0]], ['Global','Equatorial', 'Arid', 'Temperate' , 'Cold' , 'Polar'], loc='lower right')
	ax.set_ylabel("Difference", fontsize=14,color='black' ,  usetex=True)
	ax.grid(True)
	plt.xticks(fontsize=12 ,  usetex=True),plt.yticks(fontsize=12 ,  usetex=True)
	plt.tight_layout()
	fig.savefig('Class_a_b_metrics_2.pdf')
	plt.show()


	
	''' third  '''
		
	data_A_3 = [	
				df_A['SSPC_U95'],	df_A['SSPC_TS']
			]
	data_B_3 = [	
				df_B['SSPC_U95'],	df_B['SSPC_TS']
			]
	data_C_3 = [	
				df_C['SSPC_U95'],	df_C['SSPC_TS']
			]
	data_D_3 = [	
				df_D['SSPC_U95'],	df_D['SSPC_TS']
			]
	data_E_3 = [	
				df_E['SSPC_U95'],	df_E['SSPC_TS']
			]
	data_G_3 = [	
				df['SSPC_U95'],	df['SSPC_TS']
			]
				
	fig = plt.figure(1, figsize=(3, 3))
	ax = plt.gca()
	line_width = 2
	c = "blue"		
	r = 1
	boxes0 = ax.boxplot(data_G_3, positions=[r , r+m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' 
							],
				capprops=dict(color=c, linewidth = line_width), whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ), medianprops=dict(color='red', linewidth = line_width),patch_artist=True, boxprops=dict(facecolor=c )
			)
	
	c = "green"	
	r = 2
	boxes1 = ax.boxplot(data_A_3, positions=[r , r+m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' ,'' 
								],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "purple"		
	r = 3
	boxes2 = ax.boxplot(data_B_3, positions=[r , r+m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'U95' ,'TS'  
							],
							
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)
	c = "black"		
	r = 4
	boxes3 = ax.boxplot(data_C_3, positions=[r , r+m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' 
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "gray"		
	r = 5
	boxes4 = ax.boxplot(data_D_3, positions=[r , r+m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' 
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "orange"		
	r = 6
	boxes5 = ax.boxplot(data_E_3, positions=[r , r+m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' 
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)				
	
	plt.legend([boxes0["boxes"][0], boxes1["boxes"][0], boxes2["boxes"][0], boxes3["boxes"][0], boxes4["boxes"][0], boxes5["boxes"][0]], ['Global','Equatorial', 'Arid', 'Temperate' , 'Cold' , 'Polar'], loc='upper right')
	ax.set_ylabel("Difference [$\\%$]", fontsize=14,color='black' ,  usetex=True)
	ax.grid(True)
	plt.xticks(fontsize=12 ,  usetex=True),plt.yticks(fontsize=12 ,  usetex=True)
	plt.tight_layout()
	fig.savefig('Class_a_b_metrics_3.pdf')
	plt.show()







	'''------------------------------------'''
	''' Class c statistical metrics '''
	'''------------------------------------'''

	data_A_3 = [	
				df_A['SSPC_KSI_norm'],	df_A['SSPC_OVER_norm'], df_A['SSPC_CPI_norm'],
			]
	data_B_3 = [	
				df_B['SSPC_KSI_norm'],	df_B['SSPC_OVER_norm'], df_B['SSPC_CPI_norm'],
			]
	data_C_3 = [	
				df_C['SSPC_KSI_norm'],	df_C['SSPC_OVER_norm'], df_C['SSPC_CPI_norm'],
			]
	data_D_3 = [	
				df_D['SSPC_KSI_norm'],	df_D['SSPC_OVER_norm'], df_D['SSPC_CPI_norm'],
			]
	data_E_3 = [	
				df_E['SSPC_KSI_norm'],	df_E['SSPC_OVER_norm'], df_E['SSPC_CPI_norm'],
			]
	data_G_3 = [	
				df['SSPC_KSI_norm'],	df['SSPC_OVER_norm'], df['SSPC_CPI_norm'],
			]
				
	fig = plt.figure(1, figsize=(3, 3))
	ax = plt.gca()
	line_width = 2
	c = "blue"		
	r = 1
	boxes0 = ax.boxplot(data_G_3, positions=[r , r+m  , r+2*m ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,''
							],
				capprops=dict(color=c, linewidth = line_width), whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ), medianprops=dict(color='red', linewidth = line_width),patch_artist=True, boxprops=dict(facecolor=c )
			)
	
	c = "green"	
	r = 2
	boxes1 = ax.boxplot(data_A_3, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' ,'' ,''
								],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "purple"		
	r = 3
	boxes2 = ax.boxplot(data_B_3, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'KSI' ,'OVER' , 'CPI' 
							],
							
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)
	c = "black"		
	r = 4
	boxes3 = ax.boxplot(data_C_3, positions=[r , r+m, r+2*m   ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "gray"		
	r = 5
	boxes4 = ax.boxplot(data_D_3, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "orange"		
	r = 6
	boxes5 = ax.boxplot(data_E_3, positions=[r , r+m , r+2*m  ], #showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "black","markersize": "5" },
							labels=[	
								'' , '' ,''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)				
	
	plt.legend([boxes0["boxes"][0], boxes1["boxes"][0], boxes2["boxes"][0], boxes3["boxes"][0], boxes4["boxes"][0], boxes5["boxes"][0]], ['Global','Equatorial', 'Arid', 'Temperate' , 'Cold' , 'Polar'], loc='upper right')
	ax.set_ylabel("Difference [$\\%$]", fontsize=14,color='black' ,  usetex=True)
	ax.grid(True)
	plt.xticks(fontsize=12 ,  usetex=True),plt.yticks(fontsize=12 ,  usetex=True)
	plt.tight_layout()
	fig.savefig('Class_c_metrics.pdf')
	plt.show()		


	'''------------------------------------'''
	''' RMSD comparison '''
	'''------------------------------------'''
	
	data_A = [	
				df_A['SSPC_RMSD'],	df_A['Biga_RMSD'], 	df_A['DPP_RMSD'], 		df_A['Mghouchi_RMSD'],	df_A['ESRA_RMSD'],
				df_A['FR1999_RMSD'],df_A['HLJ_RMSD'],	df_A['Hourwitz_RMSD'],	df_A['I&P_RMSD'],		df_A['Kasten_RMSD'], 
				df_A['L1970_RMSD'],	df_A['M1976_RMSD'],	df_A['SP1965_RMSD'],	df_A['S1994_RMSD']									
			]
	data_B = [	
				df_B['SSPC_RMSD'],	df_B['Biga_RMSD'], 	df_B['DPP_RMSD'], 		df_B['Mghouchi_RMSD'],	df_B['ESRA_RMSD'],
				df_B['FR1999_RMSD'],df_B['HLJ_RMSD'],	df_B['Hourwitz_RMSD'],	df_B['I&P_RMSD'],		df_B['Kasten_RMSD'], 
				df_B['L1970_RMSD'],	df_B['M1976_RMSD'],	df_B['SP1965_RMSD'],	df_B['S1994_RMSD']
			]
	data_C = [	
				df_C['SSPC_RMSD'],	df_C['Biga_RMSD'], 	df_C['DPP_RMSD'], 		df_C['Mghouchi_RMSD'],	df_C['ESRA_RMSD'],
				df_C['FR1999_RMSD'],df_C['HLJ_RMSD'],	df_C['Hourwitz_RMSD'],	df_C['I&P_RMSD'],		df_C['Kasten_RMSD'], 
				df_C['L1970_RMSD'],	df_C['M1976_RMSD'],	df_C['SP1965_RMSD'],	df_C['S1994_RMSD']
			]
	data_D = [	
				df_D['SSPC_RMSD'],	df_D['Biga_RMSD'], 	df_D['DPP_RMSD'], 		df_D['Mghouchi_RMSD'],	df_D['ESRA_RMSD'],
				df_D['FR1999_RMSD'],df_D['HLJ_RMSD'],	df_D['Hourwitz_RMSD'],	df_D['I&P_RMSD'],		df_D['Kasten_RMSD'], 
				df_D['L1970_RMSD'],	df_D['M1976_RMSD'],	df_D['SP1965_RMSD'],	df_D['S1994_RMSD']
			]
	data_E = [	
				df_E['SSPC_RMSD'],	df_E['Biga_RMSD'], 	df_E['DPP_RMSD'], 		df_E['Mghouchi_RMSD'],	df_E['ESRA_RMSD'],
				df_E['FR1999_RMSD'],df_E['HLJ_RMSD'],	df_E['Hourwitz_RMSD'],	df_E['I&P_RMSD'],		df_E['Kasten_RMSD'], 
				df_E['L1970_RMSD'],	df_E['M1976_RMSD'],	df_E['SP1965_RMSD'],	df_E['S1994_RMSD']
			]
	data_G = [	
				
				df['SSPC_RMSD'],	df['Biga_RMSD'], 	df['DPP_RMSD'], 		df['Mghouchi_RMSD'],	df['ESRA_RMSD'],
				df['FR1999_RMSD'],	df['HLJ_RMSD'],		df['Hourwitz_RMSD'],	df['I&P_RMSD'],			df['Kasten_RMSD'], 
				df['L1970_RMSD'],	df['M1976_RMSD'],	df['SP1965_RMSD'],		df['S1994_RMSD']
			]
	
	df_rmsd_A = pd.DataFrame(data_A).mean(axis=1)
	df_rmsd_B = pd.DataFrame(data_B).mean(axis=1)
	df_rmsd_C = pd.DataFrame(data_C).mean(axis=1)
	df_rmsd_D = pd.DataFrame(data_D).mean(axis=1)
	df_rmsd_E = pd.DataFrame(data_E).mean(axis=1)
	df_rmsd_G = pd.DataFrame(data_G).mean(axis=1)
	
	
	global_mean = pd.concat([df_rmsd_G, df_rmsd_A , df_rmsd_B,
						df_rmsd_C, df_rmsd_D , df_rmsd_E	], axis=1).round(2)
	
	
	global_mean = global_mean.rename(columns={ 	0 :'G',
										1 :'A',
										2 :'B',
										3 :'C',
										4 :'D',
										5 :'E'})#.T	
	
	global_mean.to_csv("mean_of_climate_classes.csv")
	
	print(global_mean)
	
	
	
	# ~ fig = plt.figure(1, figsize=(14, 6))
	fig = plt.figure(1, figsize=(12, 5))
	ax = plt.gca()
	line_width = 2
	c = "blue"		
	r = 1
	m = 10
	boxes0 = ax.boxplot(data_G, positions=[r , r+m , r+2*m , r+3*m , r+4*m , r+5*m , r+6*m , r+7*m , r+8*m , r+9*m , r+10*m , r+11*m , r+12*m , r+13*m  ], showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "red","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'', '' , '' ,'' ,'', '' , '' ,'' ,'','' , '' 
							],
				capprops=dict(color=c, linewidth = line_width), whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ), medianprops=dict(color='red', linewidth = line_width),patch_artist=True, boxprops=dict(facecolor=c )
			)
	
	
	
	c = "green"	
	r = 2
	boxes1 = ax.boxplot(data_A, positions=[r , r+m , r+2*m , r+3*m , r+4*m , r+5*m , r+6*m , r+7*m , r+8*m , r+9*m , r+10*m , r+11*m , r+12*m , r+13*m ], showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "red","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'', '' , '' ,'' ,'', '' , '' ,'' ,'','' , ''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	c = "purple"		
	r = 3
	boxes2 = ax.boxplot(data_B, positions=[r , r+m , r+2*m , r+3*m , r+4*m , r+5*m , r+6*m , r+7*m , r+8*m , r+9*m , r+10*m , r+11*m , r+12*m , r+13*m ], showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "red","markersize": "5" },
							labels=[
								
								'SSPC',		'Biga',		'DPP',		'El Mghouchi',		'ESRA',	
								'FR1999',	'HLJ',		'Hourwitz', 'I$\\&$P', 			'Kasten',
								'L1970', 	'M1976',	'SP1965', 	'S1994'
							],
							
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)
	c = "black"		
	r = 4
	boxes3 = ax.boxplot(data_C, positions=[r , r+m , r+2*m , r+3*m , r+4*m , r+5*m , r+6*m , r+7*m , r+8*m , r+9*m , r+10*m , r+11*m , r+12*m , r+13*m  ], showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "red","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'', '' , '' ,'' ,'', '' , '' ,'' ,'','' , ''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)	
	
	c = "gray"		
	r = 5
	boxes4 = ax.boxplot(data_D, positions=[r , r+m , r+2*m , r+3*m , r+4*m , r+5*m , r+6*m , r+7*m , r+8*m , r+9*m , r+10*m , r+11*m , r+12*m , r+13*m   ], showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "red","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'', '' , '' ,'' ,'', '' , '' ,'' ,'','' , ''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)		
	
	c = "orange"		
	r = 6
	boxes5 = ax.boxplot(data_E, positions=[r , r+m , r+2*m , r+3*m , r+4*m , r+5*m , r+6*m , r+7*m , r+8*m , r+9*m , r+10*m , r+11*m , r+12*m , r+13*m  ], showfliers=False,
							showmeans = True ,
							meanprops={"marker": "o","markerfacecolor": "white","markeredgecolor": "red","markersize": "5" },
							labels=[	
								'' , '' ,'' ,'', '' , '' ,'' ,'', '' , '' ,'' ,'','' , ''
							],
				capprops=dict(color=c, linewidth = line_width),whiskerprops=dict(color=c, linewidth = line_width),flierprops=dict(color=c, markeredgecolor=c ),medianprops=dict(color='red', linewidth = line_width),patch_artist=True,boxprops=dict(facecolor=c )
			)				
	
	plt.legend([boxes0["boxes"][0], boxes1["boxes"][0], boxes2["boxes"][0], boxes3["boxes"][0], boxes4["boxes"][0], boxes5["boxes"][0]], ['Global','Equatorial', 'Arid', 'Temperate' , 'Cold' , 'Polar'], loc='upper left')
	ax.set_ylabel("RMSD [$\\%$]", fontsize=14,color='k' ,  usetex=True)
	ax.grid(True)
	plt.xlim((-2,140))
	plt.xticks(fontsize=12 ,  usetex=True),plt.yticks(fontsize=12 ,  usetex=True)
	plt.tight_layout()
	fig.savefig('RMSD_comparison.pdf')
	plt.show()
	
	
	
	
	


if __name__ == '__main__':
	main()
