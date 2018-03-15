# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:08:43 2018

@author: justin gomes
"""

import shockTube_constant_volume as shock
import matplotlib as mpl
from pylab import savefig
import pandas as pd

#establish parameters
ctiFile = 'mecph_v2b.cti' 
mech = 'incineration_Glaude'
speciesNames = ['air']
pressure = 15 #atm
temperature = 1200 #Kelvin
concentrations = {
        'po[ome]3':0.01,
        'o2':0.99*1/4.76,
        'n2':0.99*3.76/4.76
        }
initialTime = 0
finalTime = 0.002 # seconds
thermalBoundary = 'adiabatic'
observables = ['co','ch4','h2o','c2h4','ch2o','po[ome]3','co2','oh']
physicalParams = list()
kinetic_sens = 1 #default = 0
physical_sens = 0 #default = 0
reactorType = 'cv' #default = 'cv'        

#create output object
output = shock.ShockTube(ctiFile,speciesNames,pressure,temperature,
                         concentrations,initialTime,finalTime,thermalBoundary,
                         observables,physicalParams, kinetic_sens,
                         physical_sens,reactorType)


### Plot species concentrations ###
output.solution.set_index('time',inplace=True)
defaults = mpl.rcParamsDefault['figure.figsize']
mpl.rcParams['figure.figsize'] = [5*defaults[0],4*defaults[1]]
output.solution[observables].plot(
        logy=True, 
        #ylim=(0.00001, .1), #stub: commented out for 1000K case
        linewidth=3
        )
mpl.pyplot.title('Plot of Mole Fractions for TMP Pyrolysis with Air as Diluent')
savefig('mole_fraction_plot_air_'+mech, bbox_inches='tight')


### Sensitivity analysis - output is a dict with species keys and
    # sensitivity dataframes for values ###
    
# Aside from saved file names, the below code can be standardized as a
# standalone module

def sens_results(obs, specArray, timeSeries):
    '''
    return dataframe with sensitivities for a given species by reaction and time
    
    obs: (str) observable species for sensitivity analysis
    specArray: 3D numpy array with sensitivities by species, reaction, and time
    timeSeries: dataframe with times for each datapoint and index that will merge
        with sensitivities dataframe (df_sens)
    '''
    sensArray = specArray.species_slice_ksens(obs)
    
    df_sens = pd.DataFrame(sensArray)
    df_sens.columns = specArray.Index[1]
    df_sens.reset_index(inplace=True)
    
    if 'time' not in df_sens:
        df_sens = pd.merge(
            timeSeries,
            df_sens,
            how='left',
            on='index'
        )

    try:
        df_sens.drop('index',inplace=True,axis=1)
    except: pass
    
    return df_sens

#create dict to store sensitivity data for each observable species
obs_dict = dict()

#define timeSeries dataframe to add time values to sensitivity data
timeSeries = pd.DataFrame(output.Index[0])
timeSeries.reset_index(inplace=True)
timeSeries.rename(columns={0:'time'}, inplace=True)

#iterate through each observable and populate obs_dict
for o in observables:
    # [0] index for each value is the data frame with all reaction sensitivities
    obs_dict[o] = [sens_results(o,output,timeSeries)]
    # [1] index is a data frame with the 20 reactions with the highest max sensitivities and those reactions max and min sensitivity values
    max_sens = obs_dict[o][0].max(axis=0).sort_values(ascending=False)[0:10].reset_index()
    min_sens = obs_dict[o][0].min(axis=0).reset_index()
    combined_sens = pd.merge(
        max_sens,
        min_sens,
        how='left',
        on='index'
    )
    combined_sens.columns = ['reaction','max_sensitivity','min_sensitivity']
    obs_dict[o].append(combined_sens)
    # [2] index contains time series reaction sensitivities from [0] but only for the reactions in [1]
    react_list = ['time'] #stub: trying to get time back in
    react_list += obs_dict[o][1]['reaction'].tolist()
    temp_df = obs_dict[o][0][react_list]#.set_index('time',inplace=True)
    temp_df.set_index('time',inplace=True)
    obs_dict[o].append(temp_df)
    # save time series plot for each species
    obs_dict[o][2].plot(linewidth=3)
    mpl.pyplot.title('Plot of Reaction Sensitivities to %s for TMP Pyrolysis with Air as Diluent' %(o))
    savefig(o + '_sensitivites_plot_air_'+mech, bbox_inches='tight')