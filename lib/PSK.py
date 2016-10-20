import numpy as np
import matplotlib.pyplot as plt

def PSK_Modulation(code):
	dim = 1000
	Vx = []
	Di = []
	for i in range(1,len(code)):
		f = np.ones(dim)
		x = f * code[i]
		Vx = np.concatenate((Vx,x))
	plt.subplot(4,1,1)
	plt.plot(Vx)
	dim2 = len(Vx)
	t = np.linspace(0,5,dim2)
	frec1 = 2
	plt.subplot(4,1,2)
	w1 = 2 * np.pi * frec1 * t
	signal1 = np.cos(w1)
	plt.plot(t,signal1)
	
	frec2 = 2
	plt.subplot(4,1,3)
	w2 = 2 * np.pi * frec2 * t
	signal2 = np.sin(w2)
	plt.plot(t,signal2)
	plt.subplot(4,1,4)
	
	SignalPSK = ((signal2*Vx) - (signal1*Vx) + (signal1))
	plt.plot(t,SignalPSK)	

	plt.show()

Enter = [0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1]
PSK_Modulation(Enter)