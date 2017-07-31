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



    return render(request,'popular.html',content)