# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 16:37:44 2018

@author: justin gomes
"""

import shockTube_constant_volume as shock
import matplotlib as mpl
from pylab import savefig
import pandas as pd

ctiFile = 'mecph_v2b.cti'
speciesNames = ['ar']
pressure = 15 #atm
temperature = 1500 #Kelvin
concentrations = {
        'po[ome]3':0.01,
        'ar':0.99
        }
initialTime = 0
finalTime = 0.01 # seconds
thermalBoundary = 'adiabatic'
observables = ['co','ch4','h2o','c2h4','ch2o','c2h2','po[ome]3']
physicalParams = list()
kinetic_sens = 1 #default = 0
physical_sense = 0 #default = 0
reactorType = 'cv' #default = 'cv'        

output = shock.ShockTube(ctiFile,speciesNames,pressure,temperature,concentrations,
              initialTime,finalTime,thermalBoundary,observables,
              physical_params, kinetic_sens, physical_sens,
              reactorType)


## Plot species concentrations
output.solution.set_index('time',inplace=True)
defaults = mpl.rcParamsDefault['figure.figsize']
mpl.rcParams['figure.figsize'] = [5*defaults[0],4*defaults[1]]
output.solution[observables].plot(
        logy=True, 
        ylim=(0.00001, .1),
        linewidth=3
        )
savefig('concentration_plot_argon', bbox_inches='tight')


## Sensitivity analysis - output is a dict with species keys and
    ## sensitivity dataframes for values

def sens_results(obs, specArray, timeSeries):
    '''
    return dataframe with sensitivities for a given species by reaction and time
    
    obs: observable species for sensitivity analysis
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
    obs_dict[o] = sens_results(o,output,timeSeries)