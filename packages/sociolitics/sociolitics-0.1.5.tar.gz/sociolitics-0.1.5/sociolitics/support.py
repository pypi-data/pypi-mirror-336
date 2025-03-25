# Copyright © 2024 Dmitry Pronin.
import numpy as np
from scipy.stats import entropy
from scipy.stats import rankdata
from sklearn.neighbors import NearestNeighbors
from scipy.linalg import norm
from scipy.spatial import distance_matrix


def find_similar(words, norm_related_freqs, target_freqs, n=10, metric=entropy):
    words = np.array(words)
    neigh = NearestNeighbors(metric=metric)
    neigh.fit(norm_related_freqs)
    indexes = neigh.kneighbors([target_freqs], n, return_distance=False)[0]
    return words[indexes]

# wordwise jsd 
def word_jsd(related_freqs, eps=10**(-10)):
    related_freqs = np.array(related_freqs)
    m = np.mean(related_freqs, axis=1)
    f1 = related_freqs[:, 0]
    f2 = related_freqs[:, 1]
    return np.sign(f2-f1) * (m*np.log2(1/(m+eps)) - 0.5*(f1*np.log2(1/(f1+eps)) + f2*np.log2(1/(f2+eps))))

# wordwise rank turbulence divergence
def word_rtd(related_freqs, alpha=1):
    related_freqs = np.array(related_freqs)
    f1 = related_freqs[:, 0]
    f2 = related_freqs[:, 1]
    # rank data
    x1 = 1+len(f1)-rankdata(f1)
    x1 = x1**-1
    x2 = 1+len(f2)-rankdata(f2)
    x2 = x2**-1
    # basic rank divergence
    divergence_elements = \
        (alpha+1)/alpha * \
        (np.abs(x1**alpha - x2**alpha))**(1/(alpha+1))
    # detect freqs > 0
    indices1 = f1>0
    indices2 = f2>0
    # normalization coeficient computation
    N1 = np.sum(indices1)
    N2 = np.sum(indices2)
    ranks1disjoint = N2 + N1/2;
    r1disjoint = 1/ranks1disjoint;
    ranks2disjoint = N1 + N2/2;
    r2disjoint = 1/ranks2disjoint;
    normalization = \
        (alpha+1)/alpha * \
        np.sum((np.abs(x1**alpha - r2disjoint**alpha))**(1/(alpha+1))) + \
        (alpha+1)/alpha * \
        np.sum((np.abs(r1disjoint**alpha - x2**alpha))**(1/(alpha+1)))
    # directional divergence
    return np.sign(x2-x1) * divergence_elements/normalization

# rankturbulence for distributions
def rankturbulence(f1, f2, axis=0, alpha=1):
    f1 = np.asarray(f1)
    f2 = np.asarray(f2)
    # rank data
    x1 = 1+f1.shape[axis]-rankdata(f1, axis=axis)
    x1 = x1**-1
    x2 = 1+f2.shape[axis]-rankdata(f2, axis=axis)
    x2 = x2**-1
    # basic rank divergence
    divergence_elements = \
        (alpha+1)/alpha * \
        (np.abs(x1**alpha - x2**alpha))**(1/(alpha+1))
    # detect freqs > 0
    indices1 = f1>0
    indices2 = f2>0
    # normalization coefficient computation
    N1 = np.sum(indices1, axis=axis, keepdims=True)
    N2 = np.sum(indices2, axis=axis, keepdims=True)
    ranks1disjoint = N2 + N1/2;
    r1disjoint = 1/ranks1disjoint;
    ranks2disjoint = N1 + N2/2;
    r2disjoint = 1/ranks2disjoint;
    normalization = \
        (alpha+1)/alpha * \
        np.sum((np.abs(x1**alpha - r2disjoint**alpha))**(1/(alpha+1)), axis=axis, keepdims=True) + \
        (alpha+1)/alpha * \
        np.sum((np.abs(r1disjoint**alpha - x2**alpha))**(1/(alpha+1)), axis=axis, keepdims=True)
    # base turbulence divergence
    # final formula with normalization
    return np.sum(divergence_elements/normalization, axis=axis)

def cosine_distance(a, b, axis=1, eps=10**(-10)):
    a = np.array(a)
    b = np.array(b)
    return 1-(np.sum(a*b, axis=axis)/(norm(a, axis=axis)*norm(b, axis=axis)+eps))

# Burrow's delta-distance matrix
def delta_distances(freq_matrix, top_n=300, eps=10**-10):
    # Use the top-n threshold
    freq_matrix = np.array(freq_matrix)[:top_n]
    rows, cols =  freq_matrix.shape
    delta_matrix = np.zeros((cols, cols))
    for row in range(rows):
        delta_matrix += 1/(np.std(freq_matrix[row])+eps) * distance_matrix(freq_matrix[row].reshape(-1, 1), 
                                                     freq_matrix[row].reshape(-1, 1))
    return delta_matrix

# Burrow's wordwise delta-distance
# f1 and f2 are parts of the freq_matrix
def word_delta(f1, f2, freq_matrix, top_n=300, eps=10**-10):
    freq_matrix = np.array(freq_matrix)[:top_n]
    f1 = np.array(f1)[:top_n]
    f2 = np.array(f2)[:top_n]
    # Reshaping for 1-D array
    if len(f1.shape) == 1:
        f1 = f1.reshape(-1, 1)
    if len(f2.shape) == 1:
        f2 = f2.reshape(-1, 1)
    # Calculating mean freqs for each group
    f1 = np.mean(f1, axis=1)
    f2 = np.mean(f2, axis=1)
    return  (f1-f2) / (np.std(freq_matrix, axis=1)+eps)

# Base for Novelity-Transcience analysis
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
