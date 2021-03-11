from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import NetflixAll, NetflixOri
from django.db.models import Q
from django.forms.models import model_to_dict
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from itertools import chain
import random


def se_apriori(df, minsup, mincof):
    te = TransactionEncoder()
    te_ary = te.fit(df).transform(df)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    se = apriori(df, min_support=minsup, use_colnames=True)
    ar = association_rules(se, metric='confidence', min_threshold=mincof)
    ar.sort_values(by='confidence', ascending=False, inplace=True)
    ar = ar[['antecedents', 'consequents']]
    ar['antecedents'] = ar['antecedents'].astype('str')
    ar['consequents'] = ar['consequents'].astype('str')
    ar['antecedents'] = ar['antecedents'].str.replace("frozenset", '').str.lstrip("({'").str.rstrip("'})").str.replace(
        "'", '')  # .str.replace(" ", '')
    ar['consequents'] = ar['consequents'].str.replace('frozenset', '').str.lstrip("({'").str.rstrip("'})").str.replace(
        "'", '')  # .str.replace(" ", '')
    ar = ar['antecedents'].str.cat(ar['consequents'], sep=',').drop_duplicates()
    return ar




def movieforselect(request):
    start=random.randint(1,2000)
    end=start+10
    movie__list = list(NetflixOri.objects.values_list('title')[start:end])
    # movie__list = list(NetflixOri.objects.values_list('title')[1:10])
    movie_list=[]
    for i in range(len(movie__list)):
        movie_list.append(str(movie__list[i])[2:-3])
    return render(request, 'movieselect.html', {'movie_list': movie_list})


def castforselect(request):
    if request.method == 'POST':
        print(request.POST.get('input'))
        st = request.POST.get('input')
        movie_cast = list(NetflixAll.objects.filter(title=st).values_list('cast'))
        other_cast = []
        for j in range(len(movie_cast)):
            other_cast.append(str(movie_cast[j])[2:-3])
        return render(request, 'castselect.html', {'cast_list': other_cast})


def armake(request):
    if request.method == 'POST':
        main_name = request.POST.get('input')
        # all_cast=与选中演员合作过的所有演员

        # all_movie=该演员出演过的所有电影
        all_movie = list(NetflixAll.objects.filter(cast=main_name).values_list('title'))
        all_cast = [[] for i in range(len(all_movie))]
        for i in range(len(all_movie)):
            r_title = str(all_movie[i])[2:-3]
            m_cast = list(NetflixAll.objects.filter(title=r_title).values_list('cast'))
            for j in range(len(m_cast)):
                all_cast[i].append(str(m_cast[j])[2:-3])
        ass_rules = se_apriori(all_cast, 0.2, 0.5)
        # print(ass_rules)
        movie_final = [[] for i in range(ass_rules.shape[0])]
        for i in range(ass_rules.shape[0]):
            # t为ar每行的cast字符串列表
            t = str(ass_rules.iloc[i])
            t = t.split(',', 1)
            if len(t) == 2:
                movie = list(
                    NetflixOri.objects.filter(Q(cast__contains=t[0]) & Q(cast__contains=t[1])).values_list('title'))
                for j in range(len(movie)):
                    # print(str(movie[j]))
                    movie_final[i].append(str(movie[j])[2:-3])
            elif len(t) == 3:
                movie = list(
                    NetflixOri.objects.filter(
                        Q(cast__contains=t[0]) & Q(cast__contains=t[1]) & Q(cast__contains=t[2])).values_list('title'))
                for j in range(len(movie)):
                    print(str(movie[j]))
                    movie_final[i].append(str(movie[j])[2:-3])
            elif len(t) == 4:
                movie = list(
                    NetflixOri.objects.filter(
                        Q(cast__contains=t[0]) & Q(cast__contains=t[1]) & Q(cast__contains=t[2]) & Q(
                            cast__contains=t[3])).values_list('title'))
                for j in range(len(movie)):
                    # print(str(movie[j]))
                    movie_final[i].append(str(movie[j])[2:-3])
            else:
                movie = list(
                    NetflixOri.objects.filter(Q(cast__contains=t[0]) & Q(cast__contains=t[1])).values_list('title'))
                for j in range(len(movie)):
                    # print(str(movie[j]))
                    movie_final[i].append(str(movie[j])[2:-3])
        movie_final = list(chain.from_iterable(movie_final))
        movie_final=list(set(movie_final))
        print(movie_final)
        return render(request, 'apriori.html', {'movie_final': movie_final})


def movieinfo(request):
    if request.method == 'POST':
        moviename = request.POST.get('input')
        info = model_to_dict(NetflixOri.objects.filter(title=moviename).first())
        return render(request, 'movieinfo.html', {'info': info})





