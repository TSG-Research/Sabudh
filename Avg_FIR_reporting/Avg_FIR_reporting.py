import pandas as pd
import numpy as np

from datetime import *

data = pd.read_excel('data.xlsx')

#  data.head()

X = pd.DataFrame()
X[['police_station', 'date_of_fir', 'date_of_off']] = data[['Police Station', 'Date of FIR' , 'Date of Offence']]

x = pd.DataFrame(X.groupby(['police_station', 'date_of_fir', 'date_of_off']).count().reset_index())

x['police_station'] = x['police_station'].str.strip()

as_l = []
cs_l = []
cr_l = []
ks_l = []
mr_l = []
ng_l = []
nb_l = []
sr_l = []
sb_l = []

for _, row in x.iterrows():
    ps = row['police_station']
    fir = row['date_of_fir'].date()
    off = row['date_of_off'].date()
    
    diff = fir - off
    diff = diff.days
    
    if ps == 'Anandpur Sahib':
        as_l.append(diff)
    if ps == 'Chamkaur Sahib':
        cs_l.append(diff)
    if ps == 'City Ropar':
        cr_l.append(diff)
    if ps == 'Kiratpur Sahib':
        ks_l.append(diff)
    if ps == 'Morinda':
        mr_l.append(diff)
    if ps == 'Nangal':
        ng_l.append(diff)
    if ps == 'Nurpur Bedi':
        nb_l.append(diff)
    if ps == 'Sadar Roopnagar':
        sr_l.append(diff)
    if ps == 'Singh Bhagwantpura':
        sb_l.append(diff)


as_avg_day = sum(as_l)/len(as_l)
cr_avg_day = sum(cr_l)/len(cr_l)
cs_avg_day = sum(cs_l)/len(cs_l)
ks_avg_day = sum(ks_l)/len(ks_l)
mr_avg_day = sum(mr_l)/len(mr_l)
ng_avg_day = sum(ng_l)/len(ng_l)
nb_avg_day = sum(nb_l)/len(nb_l)
sr_avg_day = sum(sr_l)/len(sr_l)
sb_avg_day = sum(sb_l)/len(sb_l)

ps_l = list(x['police_station'].unique())

day_l = [as_avg_day, cs_avg_day, cr_avg_day, ks_avg_day, mr_avg_day, ng_avg_day, nb_avg_day, sr_avg_day, sb_avg_day]

df = pd.DataFrame(list(zip(ps_l, day_l)), columns =['police_station', 'avg_days'])

df.to_csv('bar_chart.csv', index=False)