#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from tpot import TPOTClassifier
import pickle

def classify_dist(dist):
    if dist > 2500:#長距離
        class_ = 4
    elif dist > 1800:#中距離
        class_ = 3
    elif dist > 1200:#マイル
        class_ = 2
    else:#短距離
        class_ = 1
    return class_

def load_keiba_data():
    # load data
    TRAIN_CSV = '/code/data/keiba-ataru/uma.csv'
    df = pd.read_csv(TRAIN_CSV)

    # preprocessing
    ## drop meaningless columns
    df = df.drop(['Unnamed: 0', 'R', 'タイム','差/事故', '上3F', 'コーナー通過順', '獲得賞金（円）'], axis=1)
    ## 処理方法わからないのでとりあえず消す
    df = df.drop(['年月日', '馬名', '騎手', '調教師', 'レース名'], axis=1)

    ## complement missing data
    #print(df.dtypes, df.shape, df.isnull().sum())
    
    ### 前処理
    # 着順は1/15の形なので、順位のみ取る
    df['着順'] = df['着順'].map(lambda x:x.split('/')[0]).astype(int).map(lambda x: 0 if x > 3 else 1)
    # 体重は測れていない場合、直前の値を入れる
    df['体重'] = df['体重'].replace('計不', pd.np.nan).fillna(method='ffill').astype(int)
    # 競馬場 後ろの☆を消す
    df['競馬場'] = df['競馬場'].str.replace('☆', '')
    # 距離 後ろの/芝を消して分類
    df['距離'] = df['距離'].str.replace('/芝', '').astype(int).map(classify_dist)

    # 天候/馬場を分割する
    df_weather_condition = df['天候馬場'].str.split('/', expand=True)
    df_weather_condition.columns = ['天候', '馬場']
    df = pd.concat([df, df_weather_condition], axis=1)
    df = df.drop(['天候馬場'], axis=1)
    weather_mapping = {'晴': 0, '曇': 1, '小雨': 2, '雨': 3, '小雪': 4, '雪': 5}
    df['天候'] = df['天候'].map(weather_mapping)
    condition_mapping = {'良': 0, '稍重': 1, '重': 2, '不良': 3}
    df['馬場'] = df['馬場'].map(condition_mapping)

    ### norminal
    df = pd.get_dummies(df)
    
    # split data between training and testing
    X = df.drop('着順', axis=1).values
    y = df['着順'].values
    
    return train_test_split(X, y, test_size=0.1, random_state=0)

def learn_keiba_by_tpot():
    # make data
    X_train, X_test, y_train, y_test = load_keiba_data()
    # modelling
    tpot = TPOTClassifier(generations=5, population_size=5, verbosity=2, n_jobs=-1)
    tpot.fit(X_train, y_train)
    # save tpot
    tpot.export('tpot_pipeline.py')

def pickle_pipeline(pipe):
    with open('/code/keiba-ataru/tpot_pipeline.pickle', 'wb') as f:
        pickle.dump(pipe, f)

if __name__ == '__main__':
    learn_keiba_by_tpot()