
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def main():
    f = open('Статистика.csv')  # имя файла выгруженной статистики из модуля 2 (опционально)
    df = pd.read_csv(f, sep=';', encoding='utf8')
    f.close()

    ##print(df.shape)
    ##print(df.columns)
    ##print(df.info())
    ##print(df.describe(include=['object', 'bool']))
    ##print(df['Пол'].value_counts())
    ##print(df['Возраст'].value_counts())
    ##print(df['Город'].value_counts())
    ##print(df['Город'].value_counts(normalize=True))
    ##print(df[(df['Город'] == 'Москва') & (df['Возраст']!='не указано')]['Возраст'].max())
    # print(df.loc[0:5, "Имя":"Пол"])
    # print(df.apply(np.max))
    # d = {'Не указано': 0}                - другие значения будут указываться, как NaN
    # df['Возраст'] = df['Возраст'].map(d)
    # d = {'не указано': 0}
    # df = df.replace({'Возраст': d})
    # df['Возраст'].astype('int64')
    # print(df[df['Город'] == 'Москва']['Возраст'])

    d = {'none': 0}
    df.replace({'Instagram': d}, inplace=True)
    df.replace({'Facebook': d}, inplace=True)
    df.replace({'Twitter': d}, inplace=True)
    df.replace({'Skype': d}, inplace=True)
    df.replace({'Livejournal': d}, inplace=True)

    df.loc[df.Instagram != 0, 'Instagram'] = 1
    df.loc[df.Facebook != 0, 'Facebook'] = 1
    df.loc[df.Twitter != 0, 'Twitter'] = 1
    df.loc[df.Skype != 0, 'Skype'] = 1
    df.loc[df.Livejournal != 0, 'Livejournal'] = 1

    total_calls = df['Instagram'] + df['Facebook'] + \
                  df['Skype'] + df['Twitter'] + df['Livejournal']
    df.insert(loc=len(df.columns), column='Количество аккаунтов', value=total_calls)

    d = {'не указано': 0}
    df.replace({'Возраст': d}, inplace=True)
    df['Возраст'] = pd.to_numeric(df['Возраст'])
    df['Количество аккаунтов'] = pd.to_numeric(df['Количество аккаунтов'])
    # print(pd.crosstab(df[df['Возраст'] < 100], df[df['Количество аккаунтов']>0]))


if __name__ == '__main__':
    main()


