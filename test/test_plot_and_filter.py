from lib import modulo_wav as  mw
from lib import generate_wav as gw
import os

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_PLOT_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "plots")
PATH_SOUND_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "audio_files")

def format_audio_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_SOUND_RESOURCES, path)
        return new_path
    return path

def format_plot_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_PLOT_RESOURCES, path)
        return new_path
    return path


## Obtaining data
filename = "ook.wav"
path = format_audio_path(filename)
samp_freq, data = mw.wavfile.read(path)
data, samp_points = mw.obtain_mono_data(data)

## Plotting signal domain
print("Now plotting, please wait")
fig1 = mw.plot_signal_time_domain(data, samp_points, samp_freq, holdplot=True)
fig2 = mw.plot_signal_frequency_domain(data,samp_freq,holdplot=True)
fig3 = mw.plot_signal_spectogram(data,samp_points,samp_freq, holdplot=True)

## Plotting filtered signal domain
filtered_data = mw.fir_filter_2(data, samp_freq, cutoff=4000)
fig4 = mw.plot_signal_time_domain(filtered_data, samp_points, samp_freq, holdplot=True)
fig5 = mw.plot_signal_frequency_domain(filtered_data,samp_freq,holdplot=True)
fig6 = mw.plot_signal_spectogram(filtered_data,samp_points,samp_freq, holdplot=True)


## Saving the plotted data
pathfig = format_plot_path("Time domain plot.png")
mw.save_plot_figure(fig1,path=pathfig)
print("Plot {} has ben saved".format(pathfig))

pathfig = format_plot_path("Frequency domain plot.png")
mw.save_plot_figure(fig2,path=pathfig)
print("Plot {} has ben saved".format(pathfig))

pathfig = format_plot_path("Spectogram plot.png")
mw.save_plot_figure(fig3,path=pathfig)
print("Plot {} has ben saved".format(pathfig))

pathfig = format_plot_path("Time domain plot (FILTERED).png")
mw.save_plot_figure(fig4,path=pathfig)
print("Plot {} has ben saved".format(pathfig))

pathfig = format_plot_path("Frequency domain plot (FILTERED).png")
mw.save_plot_figure(fig5,path=pathfig)
print("Plot {} has ben saved".format(pathfig))

pathfig = format_plot_path("Spectogram plot (FILTERED).png")
mw.save_plot_figure(fig6,path=pathfig)
print("Plot {} has ben saved".format(pathfig))

# De-comment if you want to plot on python
# plt.show()

### Saving filtered wav
filename = "filtered testing.wav"
path = format_audio_path(filename)
gw.make_wav(path, filtered_data, 44100)
print("Filtered wav {} has ben saved".format(path))
