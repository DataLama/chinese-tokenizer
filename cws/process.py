import os
import re
import monpa
import jiagu
import hanlp
import pandas as pd
from pkuseg import pkuseg
from LAC import LAC
from thulac import thulac
from multiprocessing import Pool

## load chinese word segementations
pku = pkuseg()
lac = LAC(mode='seg')
thu = thulac(seg_only=True)
hnp = hanlp.load('LARGE_ALBERT_BASE')

def cws(sent):
    sent = sent.split('。')[0]
    cws_sent = {
        "sentence" : sent,
        "pkuseg" : " ".join(pku.cut(sent)),
        "lac" : " ".join(lac.run(sent)),
        "thulac" : " ".join(list(list(zip(*thu.cut(sent)))[0])),
        "monpa" : " ".join(monpa.cut(sent)),
        "hanlp" : " ".join(hnp(sent))
    }
    return cws_sent

if __name__ == '__main__':
    df = pd.read_csv('data.csv',usecols=['Id', 'Media Type','Mention Content'])
    df = df.loc[(~df['Mention Content'].duplicated()) & (df['Mention Content'].fillna('').apply(len) > 5)]
    df = df.groupby('Media Type', group_keys=False).apply(lambda x: x.sample(min(len(x), 100)))
    df = pd.concat((df, pd.DataFrame(df['Mention Content'].apply(lambda x: cws(x)).tolist())), axis=1)
    df.to_csv('processed.csv', index=False)
    