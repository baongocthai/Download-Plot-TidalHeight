# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:27:50 2023

@author: baongoc.thai
"""
# =============================================================================
# This script scraps tidal information from Singapore's website (courtesy of Jackie Leong)
# Clean scrapped data & plot tidal height for each month/year
# =============================================================================

import requests
import pandas as pd
import matplotlib.pyplot as plt

year = [2017]
month = ['January','February','March','April','May','June','July','August','September','October','November','December']

for i in range(len(year)):
    for j in range(len(month)):
        url = "http://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-sun-moon-tide-ajax.php"
        r = requests.post(url, data={"smt_year": year[i], "smt_month": month[j]})
        dfs = pd.read_html(f"<table>{r.text}</table>")[0]
        
        # Change column name
        dfs.columns = ['Date','Sun Rise', 'Sun Set', 'Moon Rise', 'Moon Set', 'Moon Fraction', 'Tide Time', 'Tide Height (m)', 'Tide H_L']
        
        # Create datetime from columns
        dfs['DateTime'] = dfs['Date'].astype(str) + '-' + str(month[j]) + '-' + str(year[i]) + ' ' + dfs['Tide Time']
        dfs['DateTime'] = pd.to_datetime(dfs['DateTime'], format= '%d-%B-%Y %I.%M %p')
        dfs.index = dfs.pop('DateTime')
        
        # Clean data
        dfs['Tide Height (m)'] = [float(i.split(' ')[0]) for i in dfs['Tide Height (m)']]
        
        # Plot
        plt.plot(dfs.index, dfs['Tide Height (m)'])
        plt.rcParams.update({'font.size': 15})
        plt.tight_layout()
        figure = plt.gcf()
        figure.set_size_inches(18, 6)
        plt.title('Tides during ' +str(month[j])+' '+str(year[i]))
        plt.ylabel('Tide height (m)')
        plt.xlim(dfs.index[0].date(), dfs.index[-1].date())
        plt.savefig("Tides\\"+'Tides during ' +str(month[j])+' '+str(year[i])+'.png', bbox_inches='tight',dpi=600)
        print (str(month[j])+' '+str(year[i]))
        plt.close()
