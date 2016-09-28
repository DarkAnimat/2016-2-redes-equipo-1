## About the code

El presente codigo se compone de multiples archivos python, los cuales se dividen en: archivo principal (main.py) y archivos de funciones (los cuales se explicaran a continuacion).

1.- Archivo principal:
	En "main", simplemente se importa el archivo "testing1.py", para realizar las pruebas de filtros, y generar las graficas.


2.- Archivos de funciones:
	 
2.1.- modulo_wav.py:
	Contiene funciones asociadas al manejo de archivos de sonido, filtrar y graficar señales. Estas incluyen obtener el "Wave Object" asociado a un archivo de sonido (en modo lectura o escritura), reproducir "wavefiles" asociados a un archivo de sonido, grabar un "wavefile" por una cantidad de segundos, escribir datos y audio sobre un "wavefile", plotear señales en el dominio del tiempo y frecuencia asi como espectrogramas. Tambien se encuentra en este archivo la funcion de filtro "FIR", la cual aplica aquel filtro a una señal.

2.2.- spectrogram.py:
	Plotea el espectrograma de una onda.

2.3.- testing1.py:
	Importando las funciones del archivo "modulo_wav.py", esta parte del programa se encarga de plotear todos los graficos asociados a un archivo de sonido ingresado. "testing1.py" sera usado como el archivo de prueba para todas las funcionalidades de la primera etapa del proyecto.



