# Copyright © 2024 Dmitry Pronin.

import re
import numpy as np
from pandas import DataFrame, concat
from scipy.stats import rankdata
from sklearn.feature_extraction.text import CountVectorizer


class DAR:
    # TODO: write exceptions!
    def __init__(self):
        self.keys = []
        self.counts = []
        self.arrays = []
        self.period_names = []
        self.period_lens = []

    def __getitem__(self, key):
        if type(key) not in (list, tuple):
            dar = DAR()
            idx = np.where(self.keys==key)
            dar.counts = [self.counts[idx].flatten()[0]]
            dar.keys = [key]
            dar.period_names = self.period_names
            dar.arrays = self.arrays[:, idx].flatten().tolist()
            return dar
        else:
            dar.period_names = self.period_names
            for k in key:
                dar = DAR()
                idx = np.where(self.keys==k)
                dar.counts.append(self.counts[idx].flatten()[0])
                dar.keys.append(k)
                dar.arrays.append(self.arrays[:, idx].flatten().tolist())
            return dar

    def fit(self, corpus, mode, period_names=None, token_pattern=r'(?u)\b\w+\b', **vectorizer_args):
        if period_names == None:
            period_names = [str(i) for i in range(len(corpus))]
        # fitting of BOW vectorizer
        vectorizer = CountVectorizer(token_pattern=token_pattern, **vectorizer_args)
        vectors = vectorizer.fit_transform(corpus)
        # vectorize function returns relative frequencies and counts
        self.keys = vectorizer.get_feature_names_out()
        self.counts = vectors.sum(axis=0).A.ravel()
        self.period_names = period_names
        self.period_lens = np.array([len(re.findall(pattern=token_pattern, string=period)) for period in corpus])
        self.arrays = vectors.A
        perform_dar_mode(self, mode)

    def sort(self):
        sorted_indices = sorted(range(len(self.period_names)), key=lambda x: self.period_names[x])
        self.period_names = [self.period_names[i] for i in sorted_indices]
        self.period_lens = [self.period_lens[i] for i in sorted_indices]
        self.arrays = [self.arrays[i] for i in sorted_indices]
        
    def to_pandas(self):
        df = DataFrame(columns=['Count', 'Word', *self.period_names])
        df['Count'] = self.counts
        df['Word'] = self.keys
        for i, period in enumerate(self.period_names):
            df[period] = self.arrays[i]
        return df

# make any DAR from count mode DAR
def perform_dar_mode(dar, mode):
    if mode == 'count':
        pass
    elif mode == 'freq':
        dar.arrays = dar.arrays / dar.period_lens.reshape(-1, 1)
    elif mode == 'proba':
        freqs = dar.arrays / dar.period_lens.reshape(-1, 1)
        dar.arrays = freqs / freqs.sum(axis=0)
    elif mode == 'rank':
        dar.arrays = 1+len(dar.keys) - rankdata(dar.arrays, axis=1)
    elif mode == 'delta':
        dar.arrays = dar.arrays / dar.period_lens.reshape(-1, 1)
        dar.arrays = dar.arrays / (np.std(dar.arrays, axis=0))
    elif mode == 'zscore':
        dar.arrays = dar.arrays / dar.period_lens.reshape(-1, 1)
        dar.arrays = (dar.arrays-np.mean(dar.arrays, axis=0)) / (np.std(dar.arrays, axis=0))
    else:
        raise Exception("Invalid mode!")

# make one DAR from a list of dars
# !!! input DAR should be in count mode!!!
def merge_dars(dar_list, mode):
    merged_dar = DAR()
    dfs = []
    len_dfs = []
    for dar in dar_list:
        dfs.append(dar.to_pandas())
        len_dfs.append(DataFrame({'period_names': dar.period_names,
                                  'period_lens': dar.period_lens}))
    concated = concat(dfs, sort=False).fillna(0)
    concated_lens = concat(len_dfs, sort=False).fillna(0)
    concated = concated.groupby(by='Word').sum().reset_index()
    concated_lens = concated_lens.groupby(by='period_names').sum().reset_index()
    merged_dar.counts = concated['Count'].values
    merged_dar.keys = concated['Word'].values
    cols = concated.columns[2:]
    merged_dar.arrays = concated[cols].values.T
    merged_dar.period_names = cols.values
    merged_dar.period_lens = concated_lens['period_lens'].values
    perform_dar_mode(merged_dar, mode=mode)
    return merged_dar