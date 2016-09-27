import matplotlib.pyplot as plt
from lib import modulo_wav as mw

### Testing:

## Obtaining data
filename = "ook.wav"
path = mw.format_wav_path(filename)
samp_freq, data = mw.wavfile.read(path)
data, samp_points = mw.obtain_mono_data(data)
print("sdffasdf<-")
#mw.play_wav_file("nya")

## Plotting data
print("Now plotting, please wait")
fig1 = mw.plot_signal_time_domain(data, samp_points, samp_freq, holdplot=True)
fig2 = mw.plot_signal_frequency_domain(data,samp_freq,holdplot=True)
fig3 = mw.plot_signal_spectogram(data,samp_points,samp_freq, holdplot=True)
mw.save_plot_figure(fig1,filename=filename, title=" (Time Domain Plot)")
print("A plot has been saved on resources/plot/{} (Time Domain Plot).png".format(filename.replace(".wav","")))
mw.save_plot_figure(fig2,filename=filename, title="(Freq Domain Plot)")
print("A plot has been saved on resources/plot/{} (Freq Domain Plot).png".format(filename.replace(".wav","")))
mw.save_plot_figure(fig3,filename=filename, title="(Spectogram)")
print("A plot has been saved on resources/plot/{} (Spectogran).png".format(filename.replace(".wav","")))




## Filtering data
filtered_data = mw.fir_filter(data, samp_freq)
fig4 = mw.plot_signal_time_domain(data, samp_points, samp_freq, holdplot=True)
fig5 = mw.plot_signal_frequency_domain(filtered_data,samp_freq,holdplot=True)
fig6 = mw.plot_signal_spectogram(filtered_data,samp_points,samp_freq, holdplot=True)

mw.save_plot_figure(fig4,filename=filename, title="Filtered (Time Domain Plot)")
print("A plot has been saved on resources/plot/{} Filtered (Time Domain Plot).png".format(filename.replace(".wav","")))
mw.save_plot_figure(fig5,filename=filename, title="Filtered (Freq Domain Plot)")
print("A plot has been saved on resources/plot/{} Filtered (Freq Domain Plot).png".format(filename.replace(".wav","")))
mw.save_plot_figure(fig6,filename=filename, title="Filtered (Spectogram)")
print("A plot has been saved on resources/plot/{} Filtered (Spectogran).png".format(filename.replace(".wav","")))

# De-comment you want to plot on python
# plt.show()

##Save Filtered wav
mw.write_wav_file(filename.replace(".wav","_filtered.wav"),filtered_data,samp_freq)
print("The filtered wavfile has been saved on resources/sound_files/{}".format(filename.replace(".wav","_filtered.wav")))

