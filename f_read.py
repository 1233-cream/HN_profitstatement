import pandas as pd


def fread(file_in):
    reader=pd.read_csv(file_in)
    f_columns=reader.to_dict(orient='records')
    return f_columns