## About the results

	Para los siguientes ejemplos de resultados, se utilizara el archivo de audio “ook.wav”.
Ejecutando el archivo de programa “testing1.py”, se obtienen las siguientes graficas asociadas:

1. **Grafica Dominio Frecuencia**

	* Sin filtro
	![Grafica dominio frecuencia - sin filtro](https://github.com/redes-usach/redes-equipo-1/tree/master/resources/plots/ook(Freq Domain Plot).png)
	* Con filtro
	![Grafica dominio frecuencia - con filtro](https://github.com/redes-usach/redes-equipo-1/tree/master/resources/plots/ookFiltered(Freq Domain Plot).png)


	Resultados: Se puede apreciar como los valores de frecuencias mas altas son despreciadas por el filtro, dejando valores entre los 0 y 3000 Hz. Se puede observar que aproximadamente en los 2000 Hz, se encuentran los valores relevantes del audio, el resto siendo ruido en su mayoria.




2. **Grafica Dominio Tiempo**

	* Sin filtro
	![Grafica dominio tiempo - sin filtro](https://github.com/redes-usach/redes-equipo-1/tree/master/resources/plots/ook(Time Domain Plot).png)

	* Con filtro
	![Grafica dominio tiempo - con filtro](https://github.com/redes-usach/redes-equipo-1/tree/master/resources/plots/ookFiltered(Time Domain Plot).png)




3. **Grafica Espectrograma**


	* Sin filtro
	![Grafica espectrograma - sin filtro](https://github.com/redes-usach/redes-equipo-1/tree/master/resources/plots/ook(Spectogram).png)
	* Con filtro
	![Grafica espectrograma - con filtro](https://github.com/redes-usach/redes-equipo-1/tree/master/resources/plots/ookFiltered(Spectogram).png)

	Resultados: Al igual que en el grafico en el dominio de la frecuencia, se puede observar como el filtro obvia los valores de frecuencia mas altas. A su vez, se aprecia que los valores de mayor relevancia, del audio filtrado, se encuentran al rededor de los 2000 Hz (Al igual que en el grafico de dominio-frecuencia).
