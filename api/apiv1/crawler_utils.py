import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from logzero import logger

HOME_URL='https://www.nankankeiba.com/'

def get_uma_csv():
   raceset_link_list = ['program/00000000000000.do']# TODO use method with selenium
   uma_link_set = set()
   df = pd.DataFrame()
   for link in raceset_link_list:
      race_link_list = __get_race_link_list_from_raceset_link_list(link)
      logger.info(race_link_list)

   for link in race_link_list:
      uma_link_list = __get_uma_link_list_from_race_link(link)
      uma_link_set |= set(uma_link_list)
   
   unique_uma_link_list = list(uma_link_set) # TODO use set better
   #logger.info(unique_uma_link_list)

   for link in unique_uma_link_list:
      df = pd.concat([df, __get_df_from_uma_link(link)]) 
   
   df.to_csv('/code/api/data/uma.csv')

def pickle_this_week_race():
   return 

def __url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def __get_race_link_list_from_raceset_link_list(raceset_link_list):
    soup = __url_to_soup(HOME_URL + raceset_link_list)
    race_link_list = [ link.attrs['href'] for link in soup.find_all( href=re.compile("/race_info/*"))]
    return race_link_list

def __get_uma_link_list_from_race_link(race_link):
    soup = __url_to_soup(HOME_URL + race_link)
    uma_link_list = [ link.attrs['href'] for link in soup.find_all( href=re.compile("/uma_info/*"))]
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

get_uma_csv()
