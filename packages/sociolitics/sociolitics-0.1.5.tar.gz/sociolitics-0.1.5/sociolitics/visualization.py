# Copyright © 2024 Dmitry Pronin.
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import rankdata

import seaborn as sns
import plotly.express as px
from matplotlib import pyplot as plt


def word_dateplot(wordlist, freqs, dates, mode, window_relation=10, 
                  sensitivity=-1, **plot_args):
    plt.figure(figsize=(10, 5), dpi=150)
    if mode == 'freq':
        ytitle = "Частотность (ipm)"
        freqs = freqs*10**6 # to ipm
    if mode == 'rank':
        ytitle = "Ранг"
        plt.yscale('log')
        plt.gca().invert_yaxis()
    if sensitivity == -1:
        for i in range(len(wordlist)):
            plt.plot_date(dates, freqs[i], fmt='-', label=wordlist[i], **plot_args)
    else:
        window_size = len(freqs[0])//window_relation + 2
        for i in range(len(wordlist)):
            plt.plot_date(dates, savgol_filter(freqs[i], window_size, sensitivity, deriv=0), 
                           fmt='-', label=wordlist[i], **plot_args)
    plt.xticks(rotation=90);
    plt.legend(title='Термин')
    plt.grid()
    plt.ylabel(ytitle);

# only for DAR with shape nx2
def specificity_shift(words, norm_related_freqs, colors=['C0', 'C1'], orientation='horizontal'):
    norm_related_freqs = np.array(norm_related_freqs)
    if orientation=='horizontal':
        #fig, ax = plt.subplots(figsize=(8, len(words)/4+0.5), dpi=150)
        plt.subplots(figsize=(8, len(words)/4+0.5), dpi=150)
        sns.barplot(x=-norm_related_freqs[:, 0], y=words, orient=orientation, dodge=True, color=colors[0])
        sns.barplot(x=norm_related_freqs[:, 1], y=words, orient=orientation, dodge=True, color=colors[1])
        plt.xlabel('Типичность')
        ticks = np.array([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
        plt.xticks(ticks, np.abs(ticks.astype(np.float16)))
        plt.xlim([-1, 1])
        plt.ylabel('')
    if orientation=='vertical':
        #fig, ax = plt.subplots(figsize=(len(words)/4+0.5, 8), dpi=150)
        plt.subplots(figsize=(len(words)/4+0.5, 8), dpi=150)
        sns.barplot(y=-norm_related_freqs[:, 0], x=words, orient=orientation, dodge=True, color=colors[0])
        sns.barplot(y=norm_related_freqs[: ,1], x=words, orient=orientation, dodge=True, color=colors[1])
        plt.ylabel('Типичность')
        ticks = np.array([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
        plt.yticks(ticks, np.abs(ticks.astype(np.float16)))
        plt.ylim([-1, 1])
        plt.xlabel('')
        plt.xticks(rotation=90)
    
# only for DAR with shape nx2
def word_shift(words, divergences, xlabel='Сдвиг'):
    divergences = np.array(divergences)
    plt.figure(figsize=(8, len(words)/4), dpi=150)
    ax = sns.barplot(x=divergences, y=words, color='grey')
    plt.setp(ax.patches, linewidth=0)
    plt.ylabel('')
    plt.yticks([])
    plt.xlabel(xlabel)
    xlim = 1.3*np.abs(divergences).max()
    plt.xlim(-xlim, xlim)
    for patch in np.where(divergences>0)[0]:
        ax.patches[patch].set_facecolor('C0')
    for patch in np.where(divergences<0)[0]:
        ax.patches[patch].set_facecolor('C1')
    ax.bar_label(ax.containers[0], words)
    plt.show()

def word_phase_portrait(related_freqs, period_names=None, eps=10**(-10), window_relation=10, 
                        sensitivity=1, annotation_step=None):
    related_freqs = np.array(related_freqs)
    if period_names == None:
        period_names = [str(i) for i in range(len(related_freqs))]
    if annotation_step == None:
        annotation_step = len(related_freqs)//10
    window_size = len(related_freqs)//window_relation + 2
    savgol = savgol_filter(related_freqs, window_size, sensitivity, deriv=0)
    savgol_deriv = savgol_filter(savgol_filter(related_freqs/(eps+sum(related_freqs)), window_size,
                                                sensitivity, deriv=1), window_size, 1, deriv=0)
    cmap = plt.cm.autumn
    colors = [cmap(i / float(len(related_freqs))) for i in range(len(related_freqs))]
    plt.figure(figsize=(8, 8), dpi=150)
    plt.plot(savgol_deriv, savgol, color='black', zorder=0)
    plt.scatter(savgol_deriv, savgol, color=colors, zorder=1)
    plt.scatter(savgol_deriv[0], savgol[0], color='black', zorder=2)
    for i in range(0, len(period_names), annotation_step):
        plt.annotate(period_names[i], (savgol_deriv[i], savgol[i]))
    plt.xlabel('Сила тренда')
    plt.ylabel('Относительная частота')
    plt.grid()


def corpus_map(words, related_freqs, start=0, stop=None, eps=10**(-10), window_relation=10):
    related_freqs = np.array(related_freqs)
    size = related_freqs.shape[0]
    window_size = related_freqs.shape[1]//window_relation + 2
    # Noise reduction
    savgol_freq = savgol_filter(related_freqs, window_size, 1, deriv=0)
    # Normalization of derivative + noise reduction
    savgol_deriv = savgol_filter(savgol_filter(related_freqs/(eps+np.sum(related_freqs, axis=1).reshape(-1, 1)), 
                                                window_size, 1, deriv=1), window_size, 1, deriv=0)
    # Rank by freq and derivative
    freq_mean = np.mean(savgol_freq[:, start:stop], axis=1)
    savgol_freq_rank = 1+len(freq_mean)-rankdata(freq_mean, axis=0).T
    deriv_mean = np.mean(savgol_deriv[:, start:stop], axis=1)
    savgol_deriv_rank = 1+len(deriv_mean)-rankdata(deriv_mean, axis=0).T
    plot_dict = {'Термин': words, 
             'Ранг частоты': savgol_freq_rank, 
             'Ранг тренда' : savgol_deriv_rank}
    fig = px.scatter(plot_dict, x = 'Ранг тренда', y = 'Ранг частоты', hover_name='Термин')
    fig.update_layout(width=700, height=700, 
                hoverlabel=dict(bgcolor="white"),
                xaxis_autorange="reversed",
                yaxis_autorange="reversed")
    fig.show()