# Copyright © 2024 Dmitry Pronin.
import pandas as pd
import re
import itertools
from joblib import Parallel, delayed
from pymystem3 import Mystem


PREPROCESS_PATTERN = r'[а-яА-Я0-9]+'


class Stemmer():
    """
    The class for messages lemmatizing
    """
    def __init__(self):
        self.mystem = Mystem()

    def stem(self, messages: list) -> list:
        """
        The function applies Mystem to a given message

        Parameters:
        -----------
        messages : str
            The list of messages to be processed

        Returns:
        --------
        text_list : list
            The list of stemmed messages
        """
        # Merge the messages to one string for Mystem processing
        merged_text = "<SEP>".join(messages)
        # Applying Mystem to the merged text
        lemmatized_text = ''.join(self.mystem.lemmatize(merged_text))
        # Splitting the lemmatized text into individual messages
        text_list = lemmatized_text.split("<SEP>")
        return text_list


def preprocess(message: str) -> str:
    """
    The function cleans the input message for Mystem processing

    Parameters:
    -----------
    message : str
        The message to be processed

    Returns:
    --------
    preprocessed_message : str
        The preprocessed message ready for Mystem processing
    """
    res = re.findall(PREPROCESS_PATTERN, message)
    if len(res) == 0:
        # Symbol for the nonpattern messages that can be changed to NaN etc.
        preprocessed_message = '-'
    else:
        preprocessed_message = ' '.join(
            re.findall(PREPROCESS_PATTERN, message)
            )
    return preprocessed_message


def lemmatize(messages: list, batch_size=1000) -> pd.Series:
    """
    The function applies Mystem to a given messages
    in the batches for parallel processing

    Parameters:
    -----------
    messages : str
        The list of messages to be processed.
    batch_size : int
        Size of the batch of messages per one stemmer instance

    Returns:
    --------
    lemmas_series : pd.Series
        Series of the lemmatized messages
    """
    stemmer = Stemmer()
    messages = messages.apply(preprocess)
    # Creating of the batches for parallel stemmers processing
    text_batches = [messages[i:i+batch_size]
                    for i in range(0, len(messages), batch_size)]
    # Parallel lemmatization
    lemmatized_texts = Parallel(n_jobs=-1)(delayed(stemmer.stem)(batch)
                                           for batch in text_batches)
    # Merging the lemmatized texts into a series and returning it
    lemmas_series = pd.Series(itertools.chain(*lemmatized_texts))
    return lemmas_series
