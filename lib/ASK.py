import numpy as np
import matplotlib.pyplot as plt

def ASK_Modulation(code):
	dim = 1000
	Vx = []
	for i in range (1,len(code)):
		f = np.ones(dim)
		x = f * code[i]
		Vx = np.concatenate((Vx,x))
	plt.subplot(3,1,1)
	plt.plot(Vx)

	dim2 = len(Vx)
	t = np.linspace(0,5,dim2)
	frec = 5
	plt.subplot(3,1,2)
	Am = 2
	w1 = Am * np.pi * frec * t
	Signal = np.cos(w1)
	plt.plot(t,Signal)
	plt.subplot(3,1,3)
	mult = (Vx*Signal)
	plt.plot(t,mult)
	plt.show()

Enter = [0,	0,1,1,0,1,1,0,0,1,0,1,1,1,1,1,1,1] #Ejemplo de informacion a enviar
ASK_Modulation(Enter)