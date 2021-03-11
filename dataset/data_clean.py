import pandas as pd

df=pd.read_csv('D:\\Project\\DMpro\\netflix_titles.csv')

df=df['cast'].str.split(', ', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'cast'}).join(df.drop('cast', axis=1))
df.fillna(value='unknow')
df.to_csv('D:\\Project\\DMpro\\netflix_titles_s.csv',index=None)