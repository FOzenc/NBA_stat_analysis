#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 08:43:52 2020

@author: ulasugurluoglu
"""

import pandas as pd
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options=Options()
chrome_options.add_argument("--headless")

domanin_name="https://www.scoreboard.com/tr/mac/"
#match_stats="/#mac-istatistikleri;0"
#player_stats_home_team="#player-statistics;1"

#SEASON URLs
seasons_url=[]
seasons_url.append("https://www.scoreboard.com/tr/basketbol/abd/nba/sonuclar/")
seasons_url.append("https://www.scoreboard.com/tr/basketbol/abd/nba-2018-2019/sonuclar/")
seasons_url.append("https://www.scoreboard.com/tr/basketbol/abd/nba-2017-2018/sonuclar/")
seasons_url.append("https://www.scoreboard.com/tr/basketbol/abd/nba-2016-2017/sonuclar/")
seasons_url.append("https://www.scoreboard.com/tr/basketbol/abd/nba-2015-2016/sonuclar/")
seasons_url.append("https://www.scoreboard.com/tr/basketbol/abd/nba-2014-2015/sonuclar/")
seasons_url.append("https://www.scoreboard.com/tr/basketbol/abd/nba-2013-2014/sonuclar/")


fixture=[]
match_id=0

for season_url in seasons_url[1:]:
    try:
        driver=webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
        print(1)
        driver.get(season_url)
        driver.maximize_window()
        time.sleep(0.5)
        season = driver.find_element_by_xpath("//div[@class='teamHeader__text']").text
        print(season)
        
        print("Before find all matches")
        while driver.find_elements_by_xpath("//a[@class='event__more event__more--static']")!=[]:

            clck = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='event__more event__more--static']")))
            driver.execute_script("arguments[0].click();", clck)
    
            time.sleep(2)
        
        matches=driver.find_elements_by_xpath("//div[@class='leagues--static event--leagues results']/div/div[@title]")
        val=[]
        for match in matches:
            val.append(match.get_attribute("id")[4:])
        
    
        print("After found all matches")
        driver.close()
    except:
        print("Error in the season",season_url[-19:-10])
        continue
    
    # SCRAPE MATCH STATS
    driver=webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
    for i in val:
        time.sleep(0.1)
        
        try:
            url=domanin_name+i+"#player-statistics;1" # url of each match page
        
            driver.get(url)
            time.sleep(0.3)
            html = driver.page_source
            
            match_player_stats=pd.io.html.read_html(html)
            response = Selector(text=html)
            date=response.xpath("//div[@id='utime']/text()").get()
            match_type=response.xpath("//span[@class='description__country']/a/text()").get()
            
            
            home=match_player_stats[3] #Home team stats
            away=match_player_stats[5] #Away team stats
            
            #Extra attributes            
            home["date"]=home.shape[0]*[date]
            home["match_type"]=home.shape[0]*[match_type]
            home["saha"]=0
            home["match_id"]=match_id
            home["season"]=season
            away["date"]=away.shape[0]*[date]
            away["match_type"]=away.shape[0]*[match_type]
            away["saha"]=1
            away["match_id"]=match_id
            away["season"]=season
            
            
            fixture.append(home)
            fixture.append(away)
            #print(match_id)
            match_id+=1
        except:
            print("Error in match",match_id)
            driver.close()
            driver=webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
            
        
    driver.close()
    
# Join all match stats (dataframes)
stats = pd.concat(fixture)

# Export data as csv
stats.to_csv("player_stats.csv",index=False)


