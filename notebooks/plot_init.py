# load libraries and set plot parameters
import matplotlib

MM_TO_INCH = 1./25.4
label_size = 8
font_size = 7
legend_size = 7
tiny = 6
small = 7
regular = 8
large = 10
axis_lw = 0.6
plot_lw = 1.5

def figsize_mm(width, height=None, aspect=4/3):
    if height is None:
        height = width/aspect
    return width*MM_TO_INCH, height*MM_TO_INCH

# figure sizes in mm
figsizes = {'single': figsize_mm(84),
            '1.5': figsize_mm(129),
            'double': figsize_mm(174)}

params = {'savefig.dpi': 1000,
          'figure.dpi': 1000,
          'figure.figsize': figsizes['single'],
          'font.size': regular,
          'axes.labelsize': regular,
          'axes.titlesize': regular,
          'axes.linewidth': axis_lw,
#           'text.fontsize': small,
          'xtick.labelsize': tiny,
          'ytick.labelsize': tiny,
          'font.family': 'serif',
          'mathtext.fontset': "dejavuserif",
          'legend.fontsize': legend_size,
#           'lines.markersize': 8,
#           'grid.linewidth': 0.2,
#           'grid.linestyle': '--',
#           'legend.framealpha': 1,
#           'legend.frameon': True
         }

matplotlib.rcParams.update(params)
