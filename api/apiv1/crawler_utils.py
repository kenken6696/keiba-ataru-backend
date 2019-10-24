import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from logzero import logger
from datetime import date, timedelta

HOME_URL='https://www.nankankeiba.com/'

def update_uma_csv():
   uma_link_set = set()
   df = pd.DataFrame()
   raceset_link_list = __get_raceset_link_list_from_entries_link()
   logger.info(raceset_link_list)

   for link in raceset_link_list:
      uma_link_list = __get_uma_link_list_from_race_link(link)
      # race_linkから各馬のuma_linkとってくるので、当然レース数が多くなれば重複出てくる。
      uma_link_set |= set(uma_link_list)
   
   for link in uma_link_set:
      df = pd.concat([df, __get_df_from_uma_link(link)]) 
   
   df.to_csv('/code/api/data/uma.csv')

def crawl_df_of_this_week_race():
   uma_link_set = set()
   
   raceset_link_list = __get_raceset_link_list_from_entries_link(filter_by_this_week=True)
   for link in raceset_link_list:
      uma_link_list = __get_uma_link_list_from_race_link(link)
      uma_link_set |= set(uma_link_list)
   # TODO CHECK DATA
   return 

def __url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def __get_raceset_link_list_from_entries_link(entris_link='program/00000000000000.do', filter_by_this_week=False):
    soup = __url_to_soup(HOME_URL + entris_link)
    
    if filter_by_this_week == False:
      raceset_link_list = [ link.attrs['href'] for link in soup.find_all(href=re.compile("/race_info/*"))]
    else:
      raceset_link_list = [soup]# TODO 
    print(raceset_link_list)

    return raceset_link_list

def __get_uma_link_list_from_race_link(race_link):
    soup = __url_to_soup(HOME_URL + race_link)
    uma_link_list = [ link.attrs['href'] for link in soup.find_all(href=re.compile("/uma_info/*"))]
    return uma_link_list

def __get_df_from_uma_link(uma_link):
    # crawl
    soup = __url_to_soup(HOME_URL + uma_link)
    
    uma_nm = soup.find('h2', id='tl-prof').text
    logger.info(uma_nm)
    
    uma_info_list = soup.find_all('table', class_=re.compile('tb01*'))[4].text.replace('\n\n','').splitlines()
    logger.info('label:' + str(uma_info_list[0:]))

    # check data:18カラムなのでデータ量も18の倍数のハズ
    if len(uma_info_list)%18 != 0:
       logger.info('data from' + uma_link + ' is wrong')
       print(len(uma_info_list)%18)
       return

    # df化
    uma_info_num = len(uma_info_list)//18
    
    pd_columns = ['馬名']
    pd_data = [uma_nm]
    
    df = pd.DataFrame(data=[pd_data + uma_info_list[i*18:18+i*18] for i in range(1,uma_info_num)], columns=pd_columns + uma_info_list[0:18])
    return df

__get_raceset_link_list_from_entries_link(filter_by_this_week=True)
