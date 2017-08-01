# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

from django.http import HttpResponse
from django.shortcuts import render


import requests
from bs4 import BeautifulSoup
# Create your views here.

def main(request):

    url = "http://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm_8"
    # url = 'http://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in_7'
    # url = 'http://www.imdb.com/search/title?count=100&groups=oscar_best_picture_winners&sort=year,desc&ref_=nv_ch_osc_2'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    # //from_encoding="utf-8"
    content = {'data':[]}
    for link in soup.findAll('tr'):
        context = {'name':'','rating':''}
        for col in link.findAll('td',{'class':"titleColumn"}):
            textt = col.find('a').string
            context['name'] = textt
        for rating in link.findAll('td',{'class':'imdbRating'}):
            rat = rating.find('strong').string if rating.find('strong') else 'NIL'
            context['rating'] = rat.encode('ascii','ignore')
        content['data'].append(context)

    return render(request,'index.html',content)

def popular(request):
    url = 'http://www.imdb.com/genre/?ref_=nv_ch_gr_3'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    # //from_encoding="utf-8"
    content = {'data': []}
    for link in soup.findAll('table',{'class':'genre-table'}):

        for row in link.findAll('tr'):
            for col in row.findAll('td'):
                context = {'genre': 'nil','link':"nil"}
                context['genre']= col.find('h3').find('a').find(text=True)

                context['link']= col.find('h3').find('a')['href']
                content['data'].append(context)



    return render(request,'popular.html',content)


def genre(request,genre_name):
    context = {
        'genre':genre_name,
        'data':[]
    }
    genre = genre_name.lower()
    url = 'http://www.imdb.com/genre/'+genre+'/'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    for link in soup.findAll('table',{'class':'results'}):
        # print(link)
        content = {'movie': 'nil', 'image': 'nil'}
        count = 0;
        for row in link.findAll('td',{'class':['title','image']}):


            # print(row['class'][0])
            if row['class'][0] == 'title':
                content['movie'] = row.find('a').string
                # print('istitle')
            else:
                content['image'] = row.find('img')['src']
                # print(content['image'])

            if count%2 is 1:
                print(content)
                context['data'].append(content)
                content = {'movie': 'nil', 'image': 'nil'}

            count += 1



    return render(request,'genre.html',context)