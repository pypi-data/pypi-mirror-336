import numpy as np
import pandas as pd


def load_and_preprocess_data(file_path, drop_column):
    df = pd.read_csv(file_path, delimiter=',')
    df = df.iloc[0:, :]
    df.replace("NA", np.nan, inplace=True)
    y = df[drop_column].astype(int)
    x = df.drop(columns=[drop_column]).values
    return x, y

def load_and_process_data(file_path):
    df = pd.read_csv(file_path, delimiter=',')
    df = df.iloc[0:, :]
    df.replace("NA", np.nan, inplace=True)
    return df
