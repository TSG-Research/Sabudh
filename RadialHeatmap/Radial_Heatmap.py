import numpy as np
import pandas as pd

data = pd.read_excel('data.xlsx')

#data.head()

X = data[['Type of Collision', 'Police Station', 'Total Fatalities']]

X['Type of Collision'] = [x.lower() for x in X['Type of Collision']]

X = X.rename(columns={'Type of Collision' : 'type_of_collision', 'Total Fatalities':'tot_fatalities', 
                     'Police Station':'police_station'})

X['type_of_collision'] = X['type_of_collision'].str.strip(' ')

pol_stat = ['Kiratpur Sahib', 'Chamkaur Sahib', 'City Ropar', 'Morinda',
       'Nurpur Bedi', 'Sadar Roopnagar', 'Singh Bhagwantpura ',
       'Anandpur Sahib ', 'Nangal']

col_l = ['hit from back', 'hit and run', 
       'head on', 'hit from side','hit pedestrian', 
       'unknown', 'hit cyclist', 'sideswipe',
       'hit fixed object', 'head on tail']

col_l_k = []
col_l_c = []
col_l_cr = []
col_l_m = []
col_l_nb = []
col_l_sr = []
col_l_sb = []
col_l_as = []
col_l_na = []

for _, row in X.iterrows():
    pol = row['police_station']
    col = row['type_of_collision']
    
    
    if pol == 'Kiratpur Sahib':
        col_l_k.append(col)
    elif pol == 'Chamkaur Sahib':
        col_l_c.append(col)
    elif pol == 'City Ropar':
        col_l_cr.append(col)
    elif pol == 'Morinda':
        col_l_m.append(col)
    elif pol == 'Nurpur Bedi':
        col_l_nb.append(col)
    elif pol == 'Sadar Roopnagar':
        col_l_sr.append(col)
    elif pol == 'Singh Bhagwantpura ':
        col_l_sb.append(col)
    elif pol == 'Anandpur Sahib ':
        col_l_as.append(col)
    elif pol == 'Nangal':
        col_l_na.append(col)

col_l_k = list(set(col_l_k))
col_l_c = list(set(col_l_c))
col_l_cr = list(set(col_l_cr))
col_l_m = list(set(col_l_m))
col_l_nb = list(set(col_l_nb))
col_l_sr = list(set(col_l_sr))
col_l_sb = list(set(col_l_sb))
col_l_as = list(set(col_l_as))
col_l_na = list(set(col_l_na))

nt_col_k = [e for e in col_l if e not in col_l_k]
nt_col_c = [e for e in col_l if e not in col_l_c]
nt_col_cr = [e for e in col_l if e not in col_l_cr]
nt_col_m = [e for e in col_l if e not in col_l_m]
nt_col_nb = [e for e in col_l if e not in col_l_nb]
nt_col_sr = [e for e in col_l if e not in col_l_sr]
nt_col_sb = [e for e in col_l if e not in col_l_sb]
nt_col_as = [e for e in col_l if e not in col_l_as]
nt_col_na = [e for e in col_l if e not in col_l_na]

for i in range(0,len(nt_col_k)):
    print(nt_col_k[i])
    X = X.append(pd.DataFrame([[nt_col_k[i], 'Kiratpur Sahib', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_c)):
    X = X.append(pd.DataFrame([[nt_col_c[i], 'Chamkaur Sahib', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_cr)):
    X = X.append(pd.DataFrame([[nt_col_cr[i], 'City Ropar', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_m)):
    X = X.append(pd.DataFrame([[nt_col_m[i], 'Morinda', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_nb)):
    X = X.append(pd.DataFrame([[nt_col_nb[i], 'Nurpur Bedi', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_sr)):
    X = X.append(pd.DataFrame([[nt_col_sr[i], 'Sadar Roopnagar', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_sb)):
    X = X.append(pd.DataFrame([[nt_col_sb[i], 'Singh Bhagwantpura ', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_as)):
    X = X.append(pd.DataFrame([[nt_col_as[i], 'Anandpur Sahib ', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)
for i in range(len(nt_col_na)):
    X = X.append(pd.DataFrame([[nt_col_na[i], 'Nangal', 0]], columns=['type_of_collision', 'police_station', 'tot_fatalities']), ignore_index=True)

x = X.groupby(['type_of_collision', 'police_station']).sum().reset_index()

df = pd.DataFrame()

x['type_of_collision'] = x['type_of_collision'].str.title()

df[['Police_Station', 'type', 'value']] = x[['police_station', 'type_of_collision', 'tot_fatalities']]

df.to_csv('radial_heat.csv', index=False)