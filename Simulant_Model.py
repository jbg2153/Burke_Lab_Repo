# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 16:37:44 2018

@author: justin gomes
"""

def sens_results(obs, specArray, timeSeries):
    '''
    return dataframe with sensitivities for a given species by reaction and time
    
    obs: (str) observable species for sensitivity analysis
    specArray: 3D numpy array with sensitivities by species, reaction, and time
    timeSeries: dataframe with times for each datapoint and index that will merge
        with sensitivities dataframe (df_sens)
    '''
    import pandas as pd
    
    #slice 2D array for given observable from 3D input array and convert to df
    sensArray = specArray.species_slice_ksens(obs)
    df_sens = pd.DataFrame(sensArray)
    df_sens.reset_index(inplace=True)               #stub: Do I need this?
    
    if 'time' not in df_sens:
        df_sens = pd.merge(
            timeSeries,
            df_sens,
            how='left',
            on='index'
        )

    try:
        df_sens.drop('index',inplace=True,axis=1)
    except: 
        pass
    
    return df_sens


def uncert_sens(
        ctiFile,
        mech,
        speciesNames,
        Fuel,
        CaseName,
        pressure,
        temperature,
        concentrations,
        initialTime,
        finalTime,
        thermalBoundary,
        observables,
        uncertFile=None,
        physicalParams = list(),
        kinetic_sens = 1, #default = 0
        physical_sens = 0, #default = 0
        reactorType = 'cv' #default = 'cv'
    ):
    '''
    Creates cantera object based on inputs above. Can be used to run repeated
    models and determine initial sensitivty weighted uncertainties to guide
    further experimental work. Simplified temporary version of a portion of
    Multiscale Informatics Code
    
    Outputs:
        - Plot of concentrations of selected observables vs time
        - Plot of top 10 abs(sensitivity weighted uncertainties) for each
        observable vs time
        - dict with observables species as keys and lists of sensitivity data
        as values [all sens, top 10 weighted uncertainties, weighted 
        uncertainties by time for top 10 reactions]
    '''

    import shockTube_constant_volume as shock
    import uncertainty_merge as um
    from chem_eqn_format import chemEqn
    import matplotlib as mpl
    from matplotlib import pyplot as plt
    from pylab import savefig
    import pandas as pd
    
    #create output object
    output = shock.ShockTube(ctiFile,speciesNames,pressure,temperature,
                             concentrations,initialTime,finalTime,thermalBoundary,
                             observables,physicalParams, kinetic_sens,
                             physical_sens,reactorType)
    
    ### Plot species concentrations ###     
    #stub: future version should call plotting module
    output.solution.set_index('time',inplace=True)
    defaults = mpl.rcParamsDefault['figure.figsize']
    mpl.rcParams['figure.figsize'] = [5*defaults[0],4*defaults[1]]
    output.solution[observables].plot(
            logy=True, 
            ylim=(0.00001, .1),
            linewidth=3
            )
    mpl.pyplot.title('Plot of Mole Fractions for %s Pyrolysis with %s' %(Fuel,CaseName))
    savefig('mole_fraction_plot_%s_fuel_%s' %(Fuel,CaseName), bbox_inches='tight')
    
    
    ### Sensitivity analysis - output is a dict with species keys and
    #   sensitivity dataframes for values ###
    
    #get uncertainties dataframe and save .csv file for reference
    df_uncert = pd.DataFrame(output.Index[1])
    df_uncert.rename(columns={0:'Reaction'}, inplace=True)
    #assign ID numbers to each reaction before proceeding
    df_uncert['Reaction_ID'] = df_uncert.index
    uncert = um.get_uncertainties(df_uncert, uncertFile)
    uncertDict = uncert.to_dict()
    
    #define timeSeries dataframe to add time values to sensitivity data
    timeSeries = pd.DataFrame(output.Index[0])
    timeSeries.reset_index(inplace=True)
    timeSeries.rename(columns={0:'time'}, inplace=True)
    
    symList = ['o-','--','-',':','x-']
    
    #create dict to store sensitivity data for each observable species
    obs_dict = dict()
    
    #list of chemical equations
    eqns = output.Index[1]          #stub: should be able to get rid of this
    
    #iterate through each observable and populate obs_dict
    for o in observables:
        
        # [0] index for each value is the data frame with all reaction sensitivities
        df_sens_uncert = [sens_results(o,output,timeSeries)]
        for c in df_sens_uncert[0]:
            try:
                df_sens_uncert[0].loc[:,c] *= uncertDict[
                        'Uncertainty A (unit)'
                    ][
                        int(c)
                    ]
            except:
                if c == 'time':
                    pass
                else:
                    raise ValueError(
                        'No uncertinty provided for reaction ' + 
                        eqns[int(c)]
                    )
        df_sens_uncert[0].set_index('time',inplace=True)
        obs_dict[o] = df_sens_uncert
    
        # [1] index is a data frame with the 10 reactions with the highest
            #absolute sensitivity values
        abs_sens = obs_dict[o][0].abs().max(axis=0).sort_values(ascending=False)[0:10].reset_index()
        abs_sens.columns = ['reaction','max_abs_value_sensitivity']
        obs_dict[o].append(abs_sens)
    
        # [2] index contains time series reaction sensitivities from [0] but only 
            #for the reactions in [1]
        react_list = list()
        react_list += obs_dict[o][1]['reaction'].tolist()
        temp_df = obs_dict[o][0][react_list]#.set_index('time',inplace=True)
        obs_dict[o].append(temp_df)
    
        # save time series plot for each species
        #stub: future version should call plotting module
        fig = plt.figure(figsize=(8,5))
        ax  = fig.add_subplot(111)
        ax.set_position([0.1,0.1,0.5,0.8])
        i = 0
        for r in obs_dict[o][2].columns:
            ax.plot(
                obs_dict[o][2][r],
                symList[(i+5)%5],
                linewidth=1,
                label=chemEqn(
                    eqns[obs_dict[o][2].columns[i]]
                ),
                markevery=120
            )
            i += 1
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,frameon=False,prop={'size':7})
        current_obs = chemEqn(o)
        plt.title('Sensitivity of (%s) for %s and %s' %(current_obs,Fuel,CaseName))
        plt.xlabel('time (s)')
        ax.tick_params(axis='both',direction='in',labelsize=12)
        ax.set_ylabel(r'$\frac{\partial(abs_7)}{\partial(X_j)} * \sigma_{j}$ ',fontsize=13)
        fig.savefig('Sensitivity_%s_%s_%s' %(o,Fuel,CaseName),bbox_inches='tight',dpi=300)
        plt.close(fig)
    
    return obs_dict