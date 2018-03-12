import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from math import floor,ceil
from mplcursors import cursor

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def plotAll(x,y,step,clearance_coeff):
    for j,item in enumerate(y):
        temp = 0
        maxInd = []
        for i in range(len(item)):
            if(i+1) < len(item):
                s1 = item[i+1] - item[i]
                if temp < s1:
                    temp = s1 

        for i in range(len(item)):
            if(i+1) < len(item):
                s1 = abs(item[i+1] - item[i])
                if temp == s1:
                    maxInd.append(str(i))

        print('Max difference between consecutive '+ y[j].name + ' :'+ str(temp)+ ' | Positions: '+ '-'.join(maxInd))

        
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    fig.subplots_adjust(right=0.75)

    lines = []
    lines.append(ax.plot(x, y[0])[0])
    ymin = min(y[0])
    ymax = max(y[0])
    yclearance = ceil((ymax-ymin)* clearance_coeff)
    ax.axis([x[0], x[step], ymin-yclearance, ymax+yclearance])
    ax.set_ylabel(y[0].name)
    ax.set_xlabel(x.name)
    axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='white')
    slider_max = len(x) - step - 1
    spos = Slider(axpos, 'Pos', 0, slider_max)

    if len(y) > 1:
        ax2 = ax.twinx()
        lines.append(ax2.plot(x,y[1],color='tab:red')[0])
        ymin = min(y[1])
        ymax = max(y[1])
        yclearance = ceil((ymax-ymin)* clearance_coeff)
        ax2.axis([x[0], x[step], ymin-yclearance, ymax+yclearance])
        ax2.set_ylabel(y[1].name)

    if len(y) > 2:    
        ax3 = ax.twinx()
        ax3.spines["right"].set_position(("axes", 1.1))
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        make_patch_spines_invisible(ax3)
        # Second, show the right spine.
        ax3.spines["right"].set_visible(True)
        lines.append(ax3.plot(x,y[2],color='tab:green')[0])
        ymin = min(y[2])
        ymax = max(y[2])
        yclearance = ceil((ymax-ymin)* clearance_coeff)
        ax3.axis([x[0], x[step], ymin-yclearance, ymax+yclearance])
        ax3.set_ylabel(y[2].name)

    if len(y) > 3:
        ax4 = ax.twinx()
        ax4.spines["right"].set_position(("axes", 1.2))
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        make_patch_spines_invisible(ax4)
        # Second, show the right spine.
        ax4.spines["right"].set_visible(True)
        lines.append(ax4.plot(x,y[3],color='tab:orange')[0])
        ymin = min(y[3])
        ymax = max(y[3])
        yclearance = ceil((ymax-ymin)* clearance_coeff)
        ax4.axis([x[0], x[step], ymin-yclearance, ymax+yclearance])
        ax4.set_ylabel(y[3].name)

    ax.legend(lines, [l.get_label() for l in lines])

    def update(val):
        pos = spos.val
        ymin = min(y[0][floor(pos):floor(pos)+step])
        ymax = max(y[0][floor(pos):floor(pos)+step])
        yclearance = ceil((ymax-ymin)*clearance_coeff)
        # ax.axis([x[floor(pos)], x[floor(pos)+step],ymin-yclearance ,ymax+yclearance])
        ax.axis([x[floor(pos)], x[floor(pos)+step], min(y[0]), max(y[0])])
        fig.canvas.draw_idle()

    spos.on_changed(update)
    cursor()
    plt.show()

def partialPlot(x,y,start,end,clearance_coeff):
    fig, ax = plt.subplots(figsize=(30, 10))
    plt.subplots_adjust(bottom=0.25)
    fig.subplots_adjust(right=0.75)

    lines = []
    lines.append(ax.plot(x, y[0])[0])
    ymin = min(y[0][start:end])
    ymax = max(y[0][start:end])
    yclearance = ceil((ymax-ymin)*clearance_coeff)
    ax.axis([x[start], x[end], ymin-yclearance, ymax+yclearance])
    ax.set_ylabel(y[0].name)
    ax.set_xlabel(x.name)
    # axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='white')
    # slider_max = len(x) - step - 1
    # spos = Slider(axpos, 'Pos', 0, slider_max)

    if len(y) > 1:
        ax2 = ax.twinx()
        lines.append(ax2.plot(x,y[1],color='tab:orange')[0])
        ymin = min(y[1][start:end])
        ymax = max(y[1][start:end])
        yclearance = ceil((ymax-ymin)*clearance_coeff)

        ax2.axis([x[start], x[end], ymin-yclearance, ymax+yclearance])
        ax2.set_ylabel(y[1].name)

    if len(y) > 2:    
        ax3 = ax.twinx()
        ax3.spines["right"].set_position(("axes", 1.1))
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        make_patch_spines_invisible(ax3)
        # Second, show the right spine.
        ax3.spines["right"].set_visible(True)
        lines.append(ax3.plot(x,y[2],color='tab:green')[0])
        ymin = min(y[2][start:end])
        ymax = max(y[2][start:end])
        yclearance = ceil((ymax-ymin)*clearance_coeff)
        ax3.axis([x[start], x[end], ymin-yclearance, ymax+yclearance])
        ax3.set_ylabel(y[2].name)

    if len(y) > 3:
        ax4 = ax.twinx()
        ax4.spines["right"].set_position(("axes", 1.2))
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        make_patch_spines_invisible(ax4)
        # Second, show the right spine.
        ax4.spines["right"].set_visible(True)
        lines.append(ax4.plot(x,y[3],color='tab:red')[0])
        ymin = min(y[3][start:end])
        ymax = max(y[3][start:end])
        yclearance = ceil((ymax-ymin)*clearance_coeff)
        ax4.axis([x[start], x[end], ymin-yclearance, ymax+yclearance])
        ax4.set_ylabel(y[3].name)

    ax.legend(lines, [l.get_label() for l in lines])
    cursor()
    plt.show()  



clearance_coeff = 0.05
fileName = sys.argv[1]

if 'xls' in fileName:
    df = pd.read_excel(fileName)
elif 'csv' in fileName:
    df = pd.read_csv(fileName)

x = df[sys.argv[2]]
x = pd.to_datetime(x) 

y = []
for i in sys.argv[3:-1]:
    y.append(df[i])

step = sys.argv[-1]
if '-' in step:
    start = int(step.split('-')[0])
    end = int(step.split('-')[1])
    partialPlot(x,y,start,end,clearance_coeff) 

else:
    step = int(sys.argv[-1])
    plotAll(x,y,step,clearance_coeff)
