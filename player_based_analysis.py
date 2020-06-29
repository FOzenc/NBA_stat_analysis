#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:16:04 2020

@author: ulasugurluoglu
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime

# =============================================================================

# IMPORT AND ADJUST DATA
data=pd.read_csv("player_stats.csv")

data.isna().sum()
(data=="-").sum()
data=data.replace("-", np.nan)
data['DAK']=data['DAK'].str.replace( ":",".")
data.isna().sum()

data = data.apply(pd.to_numeric,errors="ignore")
data['DAK']=data['DAK'].replace( np.nan,"0.00")
data['DAK'] = pd.to_numeric(data['DAK'], errors='coerce')
#data["date"]=pd.to_datetime(data["date"])

# CONVERT STRING DATE INTO DATETIME
data['date'] = [x[:10] for x in data['date']]
#dates=data['DATE']
def convert_time(mytime):


    # Remove on period and after
    try:
        if (mytime[2]!=".") | (mytime[5]!="."):
            raise Exception
        else:
            mytime=datetime.strptime(mytime, "%d.%m.%Y")
            #mytime=mytime.replace(".","")
    except Exception:
        print ("Does NOT fit the format .")

    # Remove Timeframe (E.g. MST)
    #mytime = str(mytime).split(" ")[0] + " " + str(mytime).split(" ")[1]

    return mytime
data['date']=data['date'].apply(convert_time)


# Fİll na values with 0
data=data.fillna(0)
data.isna().sum()

# =============================================================================

# =============================================================================

# Delete special matches like allstar
# Get indexes
indexNames = data[ data['match_type'] == "NBA - All Stars - Final"].index
# Delete these row indexes from dataFrame
#data.shape
data.drop(indexNames , inplace=True)

# =============================================================================

# =============================================================================

#FIND player importance values

_player_importance=data[["SAY","+/-","DAK"]] 
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
_player_importance_scaled = sc.fit_transform(_player_importance)
player_importance=np.mean(_player_importance_scaled,axis=1)

data["player_importance"]=player_importance



# =============================================================================


# =============================================================================

# Find best players
players=data.groupby(["season","Takım","Oyuncu"]).mean().reset_index()
players[players.season=="2018/2019"][["Oyuncu","Takım","player_importance"]].sort_values(by="player_importance" , ascending=False)[:10].to_dict('records')
players[players.season=="2017/2018"][["Oyuncu","Takım","player_importance"]].sort_values(by="player_importance" , ascending=False)[:10]
players[players.season=="2019/2020"][["Oyuncu","Takım","player_importance"]].sort_values(by="player_importance" , ascending=False)[:10]

best_players={}

for s in players.season.unique():
    best_players[s]=players[players.season==s][["Oyuncu","Takım","player_importance"]].sort_values(by="player_importance" , ascending=False)[:10].to_dict('records')
    
import json
with open('best_players.json', 'w',encoding='utf-8') as jsonfile:
    json.dump(best_players, jsonfile,ensure_ascii=False)
# =============================================================================

# =============================================================================
 
#FIND PLAYER ID's

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples


# Fınd duplicated names
_duplicate_names_in_one_match=data[["match_id","Oyuncu","Takım"]].groupby(["match_id","Oyuncu"]).count()
duplicate_names_in_one_match=_duplicate_names_in_one_match[_duplicate_names_in_one_match.Takım>1].reset_index()

duplicate_names=np.unique(duplicate_names_in_one_match.Oyuncu.values)
dublicatedName_stats=players[players["Oyuncu"].isin(duplicate_names)].drop(["saha","match_id"],axis=1)


# Unique Player Names

player_id=[]
ids=0
for p in np.unique(players.Oyuncu):
    if p not in duplicate_names:
        player_id.append([p,ids])
        ids+=1
df_player_id=pd.DataFrame(data=player_id,columns=["Oyuncu","player_id"])
players=players.merge(df_player_id, how="left", on="Oyuncu")

# Duplicated Name Cases
ids2=ids
for p in np.unique(players.Oyuncu):
    
    if p in duplicate_names:
        
        kmeans = KMeans(n_clusters=2, random_state=2026649)
        _player=players[players.Oyuncu==p]
        codes, uniques = pd.factorize(_player["Takım"].values)
        _player["team_id"]=codes
        
        _player_clustering_data=_player[["team_id","HR","B3S.1"]]
        cluster_labels=kmeans.fit_predict(_player_clustering_data)

        _player["label"]=cluster_labels
        for index, row in _player.iterrows():
            
            if row["label"]==0:
                players.loc[(players.season==row["season"]) & (players.Takım==row["Takım"]) & (players.Oyuncu==row["Oyuncu"]),["player_id"]]=ids2
                
            else:
                players.loc[(players.season==row["season"]) & (players.Takım==row["Takım"]) & (players.Oyuncu==row["Oyuncu"]),["player_id"]]=ids2+1
                
        ids2+=1
        
# Check labeling
players.isna().sum() 
players[players.Oyuncu=="Curry S."].sort_values("player_id")  
players[players.Oyuncu=="Green D."].sort_values("player_id")   


data=data.merge(players[["season","Takım","Oyuncu","player_id"]], on=["season","Takım","Oyuncu"],how="left")


# =============================================================================


# =============================================================================

# FIND STAR PERFORMANCES OF EACH TEAM

#import time
#start_time = time.time()
_data=data[["match_id","Takım","DAK","SAY","player_importance"]]
df_star=_data.sort_values(by=['DAK','SAY'], ascending=[False,False]).groupby(["match_id","Takım"]).head(3)
df_star=df_star.groupby(["match_id","Takım"]).mean().reset_index()

#print(time.time() - start_time)


# =============================================================================

# =============================================================================

# FIND MATCH RESULTS

df_matchStats=data.groupby(["match_id","Takım","season","date","saha","match_type"]).sum().reset_index()
_home_points=df_matchStats["SAY"][0::2].values
_away_points=df_matchStats["SAY"][1::2].values
result=[]

for x in range(len(_home_points)):
    if ((_home_points[x]-_away_points[x])>0):
        result.append(1)
        result.append(0)
    else:
        result.append(0)
        result.append(1)
df_matchStats["result"]=result
df_star["result"]=result

# add season and month columns
df_star["season"]=df_matchStats["season"]
#df_star["date"]=df_matchStats["date"]
df_star["month"]=df_matchStats["date"].dt.month
# =============================================================================

# =============================================================================

# FIND STANDINGS

# Calculate true number of wins for each season and team
standings=df_matchStats[df_matchStats["match_type"]=="NBA"][["season","Takım","result"]].groupby(["season","Takım"]).sum()
standings=standings.reset_index()
standings=standings.rename(columns={"result": "true_w"})

# =============================================================================


# =============================================================================

# ADJUST DATA

# Arrange X and Y

X=df_star.drop(["result","match_id","month"],axis=1).select_dtypes(include=["float64","int64"]) # result int type'ında olduğu için yok
#X=df_star[["player_importance","SAY_ratio"]] # result int type'ında olduğu için yok
y=df_star.result

#Split data into train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Scale test and train data
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform (X_test)

# MLP model

from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(hidden_layer_sizes=(5,5),activation="tanh",max_iter=300)
clf.fit(X_train_scaled, y_train)
print(clf.score(X_test_scaled, y_test))
predict_proba=clf.predict_proba(X_test_scaled)
y_pred=clf.predict(X_test_scaled)



# =============================================================================

# =============================================================================

# Feature importance
from sklearn.ensemble import RandomForestRegressor
def feature_importance(X,y):
  
    regr = RandomForestRegressor(max_depth=8, random_state=0)
    regr.fit(X, y)
    importance = regr.feature_importances_
    feature_imp={}
    for i,att in enumerate(X.columns):
        feature_imp[att]=importance[i]
    return feature_imp

feature_imp=feature_importance(X,y)

corr_matrix=df_star[X.columns].corr()

# =============================================================================

# =============================================================================

# NUMBER OF MATCHES

num_matches=df_matchStats[(df_matchStats.match_type=="NBA")][["season","Takım","result"]].groupby(["season","Takım"]).count()
num_matches=num_matches.rename(columns={"result":"n_matches"})
num_matches=num_matches.reset_index()

# =============================================================================


# =============================================================================

#  PREDICTION WITH THE PREVIOUS SEASON PERFORMANCES
from sklearn.metrics import mean_squared_error
import math
def preseason_prediction(choose_season):
    previous_season_avg_performances=players[["season","Takım","player_id","player_importance","DAK","SAY"]].groupby(["season","player_id"]).mean().reset_index()
    
   
    _seasons=previous_season_avg_performances.season.unique()
    indexNames = previous_season_avg_performances[ previous_season_avg_performances['season'] == "2019/2020"].index
    previous_season_avg_performances.drop(indexNames , inplace=True)
    
    previous_season_avg_performances.replace(_seasons[:-1],_seasons[1:] ,inplace=True)
    
    _df_star_before_Season=players[["season","Takım","player_id"]]
    indexNames = _df_star_before_Season[ _df_star_before_Season['season'] == "2013/2014"].index
    _df_star_before_Season.drop(indexNames , inplace=True)
    
    df_star_before_Season=_df_star_before_Season.merge(previous_season_avg_performances, on=["season","player_id"], how="left")
    
    df_star_before_Season=df_star_before_Season.sort_values(by=['player_importance','SAY'], ascending=[False,False]).groupby(["season","Takım"]).head(3)
    df_star_before_Season.sort_values(by=["season","Takım"],inplace=True)
    
    X_team=df_star_before_Season.groupby(["season","Takım"]).mean()[X.columns]   
    
    #number of matches
    num_matches=df_matchStats[(df_matchStats.match_type=="NBA")][["season","Takım","result"]].groupby(["season","Takım"]).count()
    num_matches=num_matches.rename(columns={"result":"n_matches"})
    num_matches=num_matches.reset_index()
    
    X_team_scaled=sc.transform(X_team)
    _standings_pred=clf.predict_proba(X_team_scaled)
    standings_pred=pd.DataFrame(_standings_pred)
    standings_pred["season"]=X_team.index.get_level_values(0)
    standings_pred["Takım"]=X_team.index.get_level_values(1)

    standings_pred = pd.merge(standings_pred, num_matches, on=['season', 'Takım'])
    standings_pred["pred_w"]=standings_pred[1]*standings_pred["n_matches"]
    
    standings_pred[standings_pred.season=="2019/2020"].sort_values("pred_w")[["Takım","pred_w"]] #CHECK PREDICTION RESULTS
    
    #Win coeff
    coeff_matrix=[]
    
    for s in df_star_before_Season.season.unique():
        
        pred_wins=standings_pred[standings_pred.season==s]["pred_w"].values
        #print(len(pred_wins))
        true_wins=standings[standings.season==s]["true_w"].values
        #print(len(true_wins))
        true_wins.sort()
        pred_wins.sort()
        win_coeff=true_wins/pred_wins
        coeff_matrix.append(win_coeff)
    coeff_matrix=np.array(coeff_matrix)
    coeff=coeff_matrix.mean(0) 
    
    # Execute winn_coeff on preddicted standings
    standings_adjusted=standings_pred.drop([0,1],axis=1).sort_values(["season","pred_w"])
    standings_adjusted["coeff"]=len(df_star_before_Season.season.unique())*list(coeff)
    standings_adjusted["adjusted_w"]=standings_adjusted.pred_w*standings_adjusted.coeff
    
    # Merge true and predicted standings for comparison
    standings_adjusted=standings_adjusted.merge(standings, on=['season', 'Takım'])
    
    # Comparison
    result_standings=standings_adjusted[standings_adjusted.season==choose_season].drop(["pred_w","coeff"],axis=1).sort_values("adjusted_w")
    RMSE=math.sqrt(mean_squared_error(standings_adjusted["true_w"], standings_adjusted["adjusted_w"])  )
    return result_standings, RMSE

preseason_prediction("2016/2017")


# =============================================================================

# =============================================================================

# MONTHLY PREDICTION
from sklearn.metrics import mean_squared_error
import math
def monthly_prediction(choose_season,choose_month,include_wins_losses_Y_or_N="Y"):
    #choose_month=12
    choose_month=choose_month
    if choose_month<9:
        choose_month+=12
    months=[i%13 if i<13  else (i%13)+1 for i in range(9,choose_month+1)]
    
    _played_matches=df_star.month.isin(months)
    X_team=df_star[_played_matches].groupby(["season","Takım"]).mean()[X.columns]
    
    # Number of matches left
    num_matches_uptodate=df_matchStats[(df_matchStats.match_type=="NBA") & (_played_matches)][["season","Takım","result"]].groupby(["season","Takım"]).count().reset_index()
    num_matches_uptodate=num_matches_uptodate.rename(columns={"result":"n_matches_made"})
    #num_matches_uptodate=df_matchStats[(df_star.month.isin(list(range(9,choose_month+1))))][["season","Takım","result"]].groupby(["season","Takım"]).count()
    num_matches_uptodate["n_matches_left"]=num_matches.n_matches-num_matches_uptodate.n_matches_made
    num_matches_uptodate["n_matches"]=num_matches.n_matches
    
    #Current standings
    standings_current=df_matchStats[(df_matchStats["match_type"]=="NBA") & (_played_matches)][["season","Takım","result"]].groupby(["season","Takım"]).sum()
    standings_current=standings_current.reset_index()
    standings_current=standings_current.rename(columns={"result": "current_w"})
    
    # Predict
    X_team_scaled=sc.transform(X_team)
    _standings_pred=clf.predict_proba(X_team_scaled)
    standings_pred=pd.DataFrame(_standings_pred)
    standings_pred["season"]=X_team.index.get_level_values(0)
    standings_pred["Takım"]=X_team.index.get_level_values(1)
    standings_pred = pd.merge(standings_pred, num_matches_uptodate, on=['season', 'Takım'])
    standings_pred = pd.merge(standings_pred, standings_current, on=['season', 'Takım'])
    
    # Decide if uptodate wins and losses are included
    if include_wins_losses_Y_or_N=="Y":
        standings_pred["pred_w"]=standings_pred[1]*standings_pred["n_matches_left"]+standings_pred.current_w
    else:
        standings_pred["pred_w"]=standings_pred[1]*standings_pred["n_matches"]
    
    #Win coeff
    coeff_matrix=[]
    
    for s in df_matchStats.season.unique():
        
        pred_wins=standings_pred[standings_pred.season==s]["pred_w"].values
        true_wins=standings[standings.season==s]["true_w"].values

        true_wins.sort()
        pred_wins.sort()


        win_coeff=true_wins/pred_wins
        coeff_matrix.append(win_coeff)
    coeff_matrix=np.array(coeff_matrix)
    coeff=coeff_matrix.mean(0) 
    
    # Execute winn_coeff on preddicted standings
    standings_adjusted=standings_pred.drop([0,1],axis=1).sort_values(["season","pred_w"])
    standings_adjusted["coeff"]=len(df_matchStats.season.unique())*list(coeff)
    standings_adjusted["adjusted_w"]=standings_adjusted.pred_w*standings_adjusted.coeff
    
    # Merge true and predicted standings for comparison
    standings_adjusted=standings_adjusted.merge(standings, on=['season', 'Takım'])
    
    # Comparison example
    #standings_adjusted[standings_adjusted.season=="2019/2020"].drop(["pred_w","coeff"],axis=1).sort_values("adjusted_w")
    result_standings=standings_adjusted[standings_adjusted.season==choose_season][["season","Takım","n_matches_made","n_matches_left","adjusted_w","true_w"]].sort_values("adjusted_w")
    result_RMSE=math.sqrt(mean_squared_error(standings_adjusted["true_w"], standings_adjusted["adjusted_w"]) )
    return result_standings,result_RMSE

monthly_prediction("2019/2020",4,"N")



 
# =============================================================================

# =============================================================================

# AFTER CORONA PREDICTION
def afterCorona(include_wins_losses_Y_or_N="Y"): 
    prediction_results, pred_RMSE=monthly_prediction("2019/2020",4,include_wins_losses_Y_or_N)
    prediction_results["adjusted_w"]=prediction_results["adjusted_w"]*82/prediction_results["n_matches_made"]
    return prediction_results.drop(["n_matches_made","n_matches_left","true_w"],axis=1)

afterCorona("Y")
# =============================================================================

# =============================================================================

# PRO PREDICTIONS 
pro_predicts_after_corona=[22,26,26,23,23,27,25,28,35,29,33,40,38,37,39,36,38,48,51,48,52,51,50,51,56,53,58,57,63,65]
pro_predicts_preseason=[21,35,33,38,46,39,28,24,27,43,40,51,42,58,40,37,42,37,31,36,47,46,43,50,40,57,51,48,44,54]

# =============================================================================

# =============================================================================

# JSON FILES

# Monthly Predictions
monthly_predictions={}
for s in df_star.season.unique():
    m_p={}
    for m in range(1,13):
        try:
            #print(s,m)
            ss,RMSE=monthly_prediction(s,m,"N")
            m_p[m]=ss.to_dict('records')
            m_p[m].append({"RMSE":RMSE})
        except:
            print(s,m)
            print("Exception occured")
            continue
    monthly_predictions[s]=m_p 
#monthly_predictions["2019/2020"][12]

import json
with open('monthly_predictions.json', 'w',encoding='utf-8') as jsonfile:
    json.dump(monthly_predictions, jsonfile,ensure_ascii=False)

# After Corona
afterCorona_prediction=afterCorona("N")
afterCorona_prediction["pro_pred"]=pro_predicts_after_corona
RMSE=math.sqrt(mean_squared_error(afterCorona_prediction["pro_pred"], afterCorona_prediction["adjusted_w"]) )
afterCorona_prediction_dict=afterCorona_prediction.to_dict('records')
afterCorona_prediction_dict.append({"RMSE":RMSE})

import json
with open('afterCorona_prediction.json', 'w',encoding='utf-8') as jsonfile:
    json.dump(afterCorona_prediction_dict, jsonfile,ensure_ascii=False)

# Predictions Before Season
before_season_prediction_dict={}

before_season_prediction,RMSE=preseason_prediction("2019/2020")
before_season_prediction["pro_pred"]=pro_predicts_preseason
RMSE_pro=math.sqrt(mean_squared_error(before_season_prediction["true_w"], before_season_prediction["pro_pred"]) )
before_season_prediction_dict["2019/2020"]=before_season_prediction.to_dict('records')
before_season_prediction_dict["2019/2020"].append({"RMSE_pro":RMSE_pro,"RMSE":RMSE})

#before_season_prediction_dict["2019/2020"][-1] #See RMSE results

for s in df_star.season.unique()[1:]:
    before_season_prediction,RMSE=preseason_prediction(s)
    before_season_prediction_dict[s]=before_season_prediction.to_dict('records')
    before_season_prediction_dict[s].append({"RMSE":RMSE})
    
import json
with open('before_season_prediction.json', 'w',encoding='utf-8') as jsonfile:
    json.dump(before_season_prediction_dict, jsonfile,ensure_ascii=False)

# =============================================================================





