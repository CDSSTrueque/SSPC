

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



def interpolacion_mapa_linke(T_L):
	
	# 1 - 2
	x1 , y1 = 64 , 1
	x2 , y2 = 94 , 2 
	if T_L <= x2 :
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b 
		
	# 2 - 3
	x1 , y1 = 94 , 2
	x2 , y2 = 112 , 3 
	if T_L <= x2 and T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b 
	# 3 - 4
	x1 , y1 = 112 , 3
	x2 , y2 = 127 , 4 
	if T_L <= x2 and T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b  
	# 4 - 5
	x1 , y1 = 127 , 4
	x2 , y2 = 133 , 5 
	if T_L <= x2 and T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b 
	# 5 - 6
	x1 , y1 = 133 , 5
	x2 , y2 = 147 , 6 
	if T_L <= x2 and T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b  
	# 6 - 7
	x1 , y1 = 147 , 6
	x2 , y2 = 162 , 7 
	if T_L <= x2 and T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b 
	# 7 - 8
	x1 , y1 = 162 , 7
	x2 , y2 = 175 , 8 
	if T_L <= x2 and T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b 
	# 8 - 9
	x1 , y1 = 175 , 8
	x2 , y2 = 194 , 9 
	if T_L <= x2 and T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b 
	# 9 - 10
	x1 , y1 = 194 , 8
	x2 , y2 = 210 , 10 
	if  T_L > x1:
		m = (y1 - y2) / ( x1 - x2)
		b = y1 - m * x1
		return m*T_L + b 
	
def get_TL_from_image(name_image, latitude , longitude):
	
	
	img_gray = cv2.imread(name_image, cv2.IMREAD_GRAYSCALE)
	
	# Center image
	x0 , y0 = 512 , 377
	# Coefficiente de conversion pixel / grados
	x1_pos , y1_pos = 299 , 235
	x1_neg , y1_neg = 299 , 236
	
	x_ang_pos = ( x0 - x1_pos ) / 100
	y_ang_pos = ( y0 - y1_pos ) / 40
	
	x_ang_neg = ( x0 - x1_neg ) / 100
	y_ang_neg = ( y0 - y1_neg ) / 40
	
	
	plt.plot( x0 - 50 * x_ang_pos , y0 - 20 * y_ang_pos ,'o',markersize=5)
	plt.plot( x0 + 50 * x_ang_neg , y0 + 20 * y_ang_neg ,'o',markersize=5)
	
	
	if latitude <= 0:
		y = y0 - latitude*y_ang_neg
	else:
		y = y0 - latitude*y_ang_pos
	
	if longitude  <= 0:
		x = x0 + longitude*x_ang_neg
	else:
		x = x0 + longitude*x_ang_pos
		
	
	
	
	y = round(y)
	x = round(x)
	
	pixel_value = img_gray[y,x]
	pix_lim = 100
	if pixel_value < pix_lim:
		return pixel_value
	else:
		pixel_qty = 0
		pixel_value = 0
		
		ctr = 0
		for pix_lim in np.arange(120,200):
			for q in np.arange(1,7):			
				for j in np.arange(-q,q+1,1):
					for i in np.arange(-q,q+1,1):
						r = img_gray[y+j,x+i]
						if r < pix_lim:
							pixel_value += r
							pixel_qty += 1
				if pixel_qty != 0 :
					ctr = 1
					break
			if ctr != 0 :
				break
				
		
		if pixel_qty == 0:
			return( img_gray[y,x] )
		
		return( pixel_value / pixel_qty )
	
	


def main():	

	filename = 'solarimetric_stations_localization.csv'
	
	ds = pd.read_csv(filename)
	
	for i in np.arange(ds.shape[0]):
		name_loc	=	ds.iloc[i , 0]
		print(name_loc)
		latitude	=	ds.iloc[i , 1]
		longitude	=	ds.iloc[i , 2]
		
		monthly_TL = pd.DataFrame( {
					'Month' : [1 , 2 , 3 , 4 , 5 , 6 ,  7 , 8 , 9 , 10 , 11 , 12 ] ,
					'Month Letters' : ['Jan' , 'Feb' , 'Mar' , 'Apr' , 'May' , 'Jun' ,  'Jul' , 'Aug' , 'Sep' , 'Oct' , 'Nov' , 'Dec' ] ,
					'T_L'	:	[	interpolacion_mapa_linke(get_TL_from_image("Tl2010_Jan.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Feb.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Mar.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Apr.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_May.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Jun.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Jul.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Aug.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Sep.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Oct.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Nov.png", latitude , longitude))	,
									interpolacion_mapa_linke(get_TL_from_image("Tl2010_Dec.png", latitude , longitude))	]
					} ).round(1)
		
		
		
		monthly_TL.to_csv(name_loc + "_TL.csv")
	



if __name__ == '__main__':
	main()


