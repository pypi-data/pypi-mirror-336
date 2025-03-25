# Copyright © 2024 Dmitry Pronin.
import numpy as np
from scipy.sparse import csr_matrix
from scipy.linalg import orthogonal_procrustes
from scipy.spatial.distance import cosine

from pandas import DataFrame

from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.extmath import randomized_svd

# Word Embedder
class WE:
    def __init__(self):
        self.X0c = []
        self.vocab = []
        self.unique_0 = []

    def fit(self, string: str,  context_size: int, 
            mode, zero_diag=True, pmi_threshold=0.1, 
            gamma=0.5, eps=10**-10, **vectorizer_args):
        # Support function for pmi matrix
        def pmi(matrix, positive=True):
            col_totals = matrix.sum(axis=0)
            total = col_totals.sum()
            row_totals = matrix.sum(axis=1)
            expected = np.outer(row_totals, col_totals) / (total+eps)
            matrix = matrix / (expected+eps)
            # Silence distracting warnings about log(0):
            with np.errstate(divide='ignore'):
                matrix = np.log(matrix)
            matrix[np.isinf(matrix)] = 0.0
            matrix[np.isnan(matrix)] = 0.0  # log(0) = 0
            if positive:
                matrix[matrix < pmi_threshold] = 0.0
            return matrix
        # Fit function
        # check_model = CountVectorizer(**vectorizer_args)
        # check_matrix = check_model
        word_windows = []
        words = string.split()
        for i in range(len(words)-context_size):
            word_windows.append(' '.join(words[i:i+context_size]))
        count_model = CountVectorizer(**vectorizer_args) # default unigram model
        count_model.fit([string])
        X0 = count_model.transform(word_windows)
        self.X0c = (X0.T * X0)
        self.vocab = count_model.get_feature_names_out()
        # Save these words (their vectors are useless)
        if zero_diag:
            self.X0c.setdiag(0)
        if mode == 'proba':
            self.X0c = self.X0c / (np.sum(self.X0c, axis=0)+eps)
        if mode == 'ppmi':
            self.X0c = pmi(self.X0c)
        if mode == 'svd':
            self.X0c = csr_matrix(pmi(self.X0c))
            # making of truncatedSVD
            U0, Sigma0, _ = randomized_svd(self.X0c, 
                              n_components=300,
                              n_iter=5,
                              random_state=42)
            self.X0c = U0 @ np.diag(Sigma0)**gamma

    def find_similar(self, word, n=10, metric=cosine, return_distance=False):
        idx = np.where(self.vocab==word)[0]
        neigh = NearestNeighbors(metric=metric)
        neigh.fit(self.X0c)
        indexes = neigh.kneighbors([self.X0c[idx].tolist()[0]], n, return_distance=return_distance)[0]
        return self.vocab[indexes]
    
    # only for not-svd mode
    def find_collocations(self, word, n=10):
        idx = np.where(self.vocab==word)[0]
        row = self.X0c[idx].A[0]
        sorted_indices = np.argsort(row)[::-1]
        return self.vocab[sorted_indices[:n]]

# Diachronic Word Embedder
class DiWE:
    def __init__(self):
        self.X0c = []
        self.X1c = []
        self.vocab = []
        self.unique_0 = []
        self.unique_1 = []
        self.divergences = []

    def fit(self, string1: str, string2: str,  context_size: int, 
            mode, zero_diag=True, unique_threshold=30, pmi_threshold=0.1, 
            gamma=0.5, eps=10**-10, **vectorizer_args):
        # Support function for pmi matrix
        def pmi(matrix, positive=True):
            col_totals = matrix.sum(axis=0)
            total = col_totals.sum()
            row_totals = matrix.sum(axis=1)
            expected = np.outer(row_totals, col_totals) / (total+eps)
            matrix = matrix / (expected+eps)
            # Silence distracting warnings about log(0):
            with np.errstate(divide='ignore'):
                matrix = np.log(matrix)
            matrix[np.isinf(matrix)] = 0.0
            matrix[np.isnan(matrix)] = 0.0  # log(0) = 0
            if positive:
                matrix[matrix < pmi_threshold] = 0.0
            return matrix
        # Fit function
        # check_model = CountVectorizer(**vectorizer_args)
        # check_matrix = check_model
        tagret_word_windows = []
        target = [string1, string2]
        for c in target:
            word_windows = []
            words = c.split()
            for i in range(len(words)-context_size):
                word_windows.append(' '.join(words[i:i+context_size]))
            tagret_word_windows.append(word_windows)
        count_model = CountVectorizer(**vectorizer_args) # default unigram model
        count_model.fit(target)
        X0 = count_model.transform(tagret_word_windows[0])
        X1 = count_model.transform(tagret_word_windows[1])
        self.X0c = (X0.T * X0)
        self.X1c = (X1.T * X1)
        self.vocab = count_model.get_feature_names_out()
        # Check near-unique words for each matrix
        diagX0 = np.diag(self.X0c.todense())
        diagX1 = np.diag(self.X1c.todense())
        idx_X0 = diagX1 < unique_threshold
        idx_X1 = diagX0 < unique_threshold
        # Save these words (their vectors are useless)
        self.unique_0 = self.vocab[idx_X0]
        self.unique_1 = self.vocab[idx_X1]
        # Select not union for new vocab
        bool_ = ~((idx_X0)|(idx_X1))
        self.vocab = self.vocab[bool_]
        self.X0c = csr_matrix(self.X0c[np.ix_(bool_, bool_)])
        self.X1c = csr_matrix(self.X1c[np.ix_(bool_, bool_)])
        if zero_diag:
            self.X0c.setdiag(0)
            self.X1c.setdiag(0)
        if mode == 'proba':
            self.X0c = self.X0c / (np.sum(self.X0c, axis=0)+eps)
            self.X1c = self.X1c / (np.sum(self.X1c, axis=0)+eps)
        if mode == 'ppmi':
            self.X0c = pmi(self.X0c)
            self.X1c = pmi(self.X1c)
        if mode == 'svd':
            self.X0c = csr_matrix(pmi(self.X0c))
            self.X1c = csr_matrix(pmi(self.X1c))
            # making of truncatedSVD
            U0, Sigma0, _ = randomized_svd(self.X0c, 
                              n_components=300,
                              n_iter=5,
                              random_state=42)
            self.X0c = U0 @ np.diag(Sigma0)**gamma
            U1, Sigma1, _ = randomized_svd(self.X1c, 
                              n_components=300,
                              n_iter=5,
                              random_state=42)
            self.X1c = U1 @ np.diag(Sigma1)**gamma
            # ortogonal aligning of X0c to X1c for further computations
            R, _ = orthogonal_procrustes(self.X0c, self.X1c)
            self.X0c = self.X0c @ R
            # Select unique words:
            self.X0c[np.abs(self.X0c) < eps] = 0


    def find_similar(self, word, key_space, value_space, n=10, metric=cosine, return_distance=False):
        idx = np.where(self.vocab==word)[0]
        neigh = NearestNeighbors(metric=metric)
        neigh.fit(value_space)
        indexes = neigh.kneighbors([key_space[idx].tolist()[0]], n, return_distance=return_distance)[0]
        return self.vocab[indexes]

    # measure a distance between matrices
    def diverge(self, metric, **metric_args):
        self.divergences = metric(self.X0c, self.X1c, axis=1, **metric_args)

    # wordwise divergence
    # best choice is any wordwise_metric from support file
    # [a, b, c] - [d, e, f] = [dist(a-d), dist(b-e), dist(c-f)]
    def word_diverge(self, word, wordwise_metric, **metric_args):
        if word not in self.vocab:
            raise Exception(f"There is no {word} in the vocabulary!")
        idx = np.where(self.vocab==word)[0]
        inp = np.array([self.X0c[idx].tolist()[0], self.X1c[idx].tolist()[0]]).T
        return wordwise_metric(inp, **metric_args)
    
    def to_pandas(self):
        df = DataFrame(columns=['Word', 'Divergence'])
        df['Word'] = self.vocab
        df['Divergence'] = self.divergences
        return df