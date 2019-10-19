import pandas as pd
import numpy as np

from datetime import *

data = pd.read_excel('data.xlsx')

date_o = data['Date of Offence']

month_l = []
for _, row in date_o.iteritems():
    a = row.month
    if a == 1:
        month_l.append('January')
    elif a == 2:
        month_l.append('February')
    elif a == 3:
        month_l.append('March')
    elif a == 4:
        month_l.append('April')
    elif a == 5:
        month_l.append('May')
    elif a == 6:
        month_l.append('June')
    elif a == 7:
        month_l.append('July')
    elif a == 8:
        month_l.append('August')
    elif a == 9:
        month_l.append('September')
    elif a == 10:
        month_l.append('October')
    elif a == 11:
        month_l.append('November')
    elif a == 12:
        month_l.append('December')

X = data[['Rural/Urban', 'Maneuver type as per FIR']]

X = X.rename(columns={'Rural/Urban' : 'rural_urban', 'Maneuver type as per FIR':'fir_types'})
fir_types = ['Rough Driving', 'Over Speeding', 'Approaching From Wrong Side', 'Wrong Parking']

 # fir_dict_urban = dict.fromkeys(fir_types, 0)

unique_fir_types = X[~X.duplicated(subset=['rural_urban','fir_types'])]
series = X.groupby(['rural_urban','fir_types'])

final_df = None
for single in range(unique_fir_types.shape[0]):
    group = series.get_group((unique_fir_types.iloc[single]['rural_urban'],unique_fir_types.iloc[single]['fir_types']))
    group['count'] = group.shape[0]
    final_df = pd.concat([group,final_df],axis=0)

f = final_df[~final_df.duplicated(subset=['rural_urban','fir_types'])].reset_index()

f.drop('index', axis=1,   inplace=True)

f.to_csv('bubble.csv', index=False)