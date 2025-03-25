# Copyright © 2024 Dmitry Pronin.
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

from scipy.signal import savgol_filter
from scipy.stats import rankdata
from scipy.stats import linregress

from scipy.spatial.distance import jensenshannon


def word_dateplot(wordlist, freqs, dates, mode, window_relation=10, 
                  sensitivity=-1, html_name=None):
    fig = go.Figure()
    if mode == 'freq':
        ytitle = "Частота (ipm)"
        freqs = np.array(freqs*10**6).astype(int) # to ipm
    if mode == 'rank':
        ytitle = "Ранг"
    if sensitivity == -1:
        for i in range(len(wordlist)):
            fig.add_trace(go.Scatter(x = dates, y = freqs[i], name=wordlist[i], mode='lines'))
    else:
        window_size = len(freqs[0])//window_relation + 2
        for i in range(len(wordlist)):
            fig.add_trace(go.Scatter(x = dates, 
                                     y = savgol_filter(freqs[i], window_size, sensitivity, deriv=0), 
                                     name=wordlist[i], mode='lines'))
    if mode == 'rank':
        fig.update_layout(yaxis_type="log", yaxis_autorange="reversed")
    fig.update_layout(xaxis_title="Дата",
                    yaxis_title=ytitle,
                    hoverlabel=dict(bgcolor="white"), 
                    hovermode="x unified",
                    xaxis=dict(tickformat='%d.%m.%Y'))
    fig.show()
    if html_name:
        fig.write_html(html_name)


def corr_heatmap(wordlist, freqs, html_name=None):
    deltas = freqs[:, 1:] - freqs[:, :-1]
    fig = go.Figure(data=
                    go.Heatmap(x=wordlist, y=wordlist, z=np.corrcoef(deltas),
                                    hovertemplate="Слово x: %{x}<br>" +
                                                "Слово y: %{y}<br>" +
                                                "Корреляция: %{z}<br>" +
                                                "<extra></extra>"))
    fig.layout.height = 500
    fig.layout.width = 500
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(hoverlabel=dict(bgcolor="white"))
    fig.show()
    if html_name:
        fig.write_html(html_name)



def corpus_map(words, counts, related_freqs, html_name=None, return_dict=False):
    related_freqs = np.array(related_freqs)
    # Noise reduction
    freq_rank = 1+len(counts)-rankdata(counts)
    num_rows, num_cols  = related_freqs.shape
    x = np.arange(num_cols)
    trends = []
    for i in range(num_rows):
        y = related_freqs[i] / related_freqs[i].max()
        trends.append(linregress(x, y).slope)
    sliceline = 1+len(trends)-np.searchsorted(trends, 0, side='right')
    trend_rank = 1+len(trends)-rankdata(trends)
    # Normalization of derivative + noise reduction
    # Rank by freq and derivative
    sorted_indices = sorted(range(len(trend_rank)), key=lambda x: trend_rank[x])
    words = [words[i] for i in sorted_indices]
    trend_rank = [trend_rank[i] for i in sorted_indices]
    freq_rank = [freq_rank[i] for i in sorted_indices]
    trends = [trends[i] for i in sorted_indices]
    plot_dict = {'Термин': words, 
             'Ранг частотности': freq_rank, 
             'Ранг тренда' : trend_rank,
             'Наклон': trends}
    fig = px.scatter(plot_dict, x = 'Ранг тренда', y = 'Ранг частотности', hover_name='Термин')
    fig.add_vline(x=sliceline, line_width=1, line_dash="dash", line_color="gray")
    fig.update_layout(width=700, height=700, 
                hoverlabel=dict(bgcolor="white"),
                xaxis_autorange="reversed",
                yaxis_autorange="reversed")
    fig.show()
    if html_name:
        fig.write_html(html_name)
    if return_dict:
        return plot_dict



def word_turbulence(words, freq_x, freq_y, 
                    name_x='Распределение x', name_y='Распределение y', 
                    html_name=None):
    rank_x = 1+len(freq_x)-rankdata(freq_x)
    rank_y = 1+len(freq_y)-rankdata(freq_y)
    plot_dict = {'Термин': words, 
             f'Ранг: {name_x}': rank_x, 
             f'Ранг: {name_y}': rank_y}
    fig = px.scatter(plot_dict, x = f'Ранг: {name_x}', y = f'Ранг: {name_y}', hover_name='Термин')
    fig.update_layout(width=700, height=700, 
                hoverlabel=dict(bgcolor="white"),
                xaxis_type="log",
                xaxis_autorange="reversed",
                yaxis_type="log",
                yaxis_autorange="reversed")
    fig.show()
    if html_name:
        fig.write_html(html_name)


def SNT_plot(sources_dar, space_dar, source_period, metric, window_size=6, html_name=None):
    def SNT(sources_dar, space_dar, source_period, metric, window_size=6):
        sources_df = sources_dar.to_pandas()
        space_df = space_dar.to_pandas()
        new_df = sources_df.merge(space_df, on='Word')
        sources_df = new_df[sources_dar.period_names]
        space_df = new_df[space_dar.period_names]
        date_quants = space_dar.period_names #space_df.columns[1:]
        start = source_period[0]
        stop = source_period[-1]
        start_index = list(date_quants).index(start)
        stop_index = list(date_quants).index(stop)
        left_win = start_index-window_size
        right_win = stop_index+window_size+1
        if left_win < 0 or right_win > len(date_quants):
            raise Exception('Invalid source period for selected window size!')
        else:
            dist_matrix = []
            for source in sources_df.columns:
                source_dists = []
                for q in date_quants[left_win:right_win]:
                    source_dists.append(metric(space_df[q], sources_df[source]))
                dist_matrix.append(source_dists)
            dist_matrix = np.array(dist_matrix)
            novelity = np.sum(dist_matrix[:, :window_size], axis=1)/window_size
            transience = np.sum(dist_matrix[:, -window_size:], axis=1)/window_size
            return novelity, transience, dist_matrix
    snt = SNT(sources_dar, space_dar, source_period=source_period, metric=metric, window_size=window_size)
    plot_dict = {'Источник': sources_dar.period_names, 
                 'Новизна': snt[0], 
                 'Консерватизм' : snt[1]}
    fig = px.scatter(plot_dict, x = 'Новизна', y = 'Консерватизм', hover_name='Источник')
    fig.update_layout(width=700, height=700, 
                hoverlabel=dict(bgcolor="white"))
    fig.update_layout(xaxis_type="log", yaxis_type="log")
    fig.show()
    if html_name:
        fig.write_html(html_name)


# for date ordered systems
def homogeneity_map(value_matrix1, value_matrix2, ticks1, ticks2, metric=jensenshannon, html_name=None, **metric_args):
    value_matrix1 = np.array(value_matrix1).T
    value_matrix2 = np.array(value_matrix2).T
    dist_matrix_dict = {}
    for i in range(len(ticks1)):
        date = ticks1[i]
        dist_matrix_dict[date] = []
        for j in range(len(ticks2)):
            dist_matrix_dict[date].append(metric(value_matrix1[i], value_matrix2[j], **metric_args))
    fig = go.Figure(data=
                    go.Heatmap(x=ticks1, y=ticks2, z=list(dist_matrix_dict.values()),
                                    hovertemplate="x: %{x}<br>" +
                                                "y: %{y}<br>" +
                                                "Расхождение: %{z}<br>" +
                                                "<extra></extra>"))
    fig.layout.height = 1000
    fig.layout.width = 1000
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(hoverlabel=dict(bgcolor="white"), 
                    xaxis=dict(tickformat='%d.%m.%Y'),
                    yaxis=dict(tickformat='%d.%m.%Y'),
                    yaxis_scaleanchor="x")
    fig.show()
    if html_name:
        fig.write_html(html_name)