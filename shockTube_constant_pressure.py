# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:02:35 2017

@author: Carly LaGrotta
"""
import itertools
import numpy as np
import cantera as ct
import pandas as pd
import simulations
        

def ShockTube(ctiFile,speciesNames,pressure,temperature,conditions,initialTime,
              finalTime,thermalBoundary,observables=[],physical_params=[], 
              kinetic_sens=0,physical_sens=0,reactorType='cp'):
    #gas = ct.Solution('AramcoMech2.0.cti')
    # 'GRI30-1999.cti'.
#    print('inside stp')
    for s in ['Ar','AR','He','HE','n2','N2']:
        if s in speciesNames:
            addBackin = s
            speciesNames.remove(s)
            break
        
    gas = ct.Solution(ctiFile)
    
    gas.TPX = temperature, pressure*101325, conditions
    
    physicalParamsSpecies = ['X'+ species for species in speciesNames]
    
    physical_params = ['P','T','X']
    
    if thermalBoundary == 'adiabatic': 
        shockTube = ct.IdealGasConstPressureReactor(gas,name = 'R1',energy= 'on')
    elif thermalBoundary == 'isothermal': 
        shockTube = ct.IdealGasConstPressureReactor(gas,name = 'R1', energy= 'off')
    else:
        raise Exception('Please enter adiabatic or isothermal for the thermal boundary layer')
    
    
    sim=ct.ReactorNet([shockTube])
    

 
    if kinetic_sens==1 and bool(observables)==False:
        raise Exception('Please supply a non-empty list of observables for sensitivity analysis or set kinetic_sens=0')
        
        
    if physical_sens==1 and bool(observables)==False:
        raise Exception('Please supply a non-empty list of observables for sensitivity analysis or set physical_sens=0')
    
    
    if kinetic_sens==1 and bool(observables):
        [shockTube.add_sensitivity_reaction(i) for i in range(gas.n_reactions)]
        dfs = [pd.DataFrame() for x in range(len(observables))]
        tempArray = [np.zeros(gas.n_reactions) for x in range(len(observables))]
                
    
    if physical_sens==1 and bool(observables):
        baseConditions = gas.TPX
        originalConditions = conditions 
                      
        
    
    columnNames = [shockTube.component_name(item) for item in range(shockTube.n_vars)]  
    columnNames = ['time']+['pressure'] + columnNames
    timeHistory = pd.DataFrame(columns = columnNames)
    timeHistorytest= pd.DataFrame(columns = columnNames)
    timeHistorytest2= pd.DataFrame(columns = columnNames)
    timeHistorytest4 = [pd.DataFrame(columns = columnNames) for item in range(len(physicalParamsSpecies))]
    
   
    t=initialTime
    counter = 0
    
    #commenting outvb colume 
    
    OHproduction = []
    ratesOfProduction = []
    while t < finalTime:
        t = sim.step() 
        state = np.hstack([t, shockTube.thermo.P, shockTube.mass, 
                    shockTube.T, shockTube.thermo.X])
        timeHistory.loc[counter] = state
        
        OHproduction.append(gas.forward_rates_of_progress)
        ratesOfProduction.append(gas.creation_rates[gas.species_index('OH')])
        if kinetic_sens == 1 and bool(observables):

            newcounter = 0
            for observable,reaction in itertools.product(observables,range(gas.n_reactions)):
                tempArray[observables.index(observable)][reaction] = sim.sensitivity(observable, reaction)
                
                
            
                newcounter +=1
                
                
                if(newcounter%gas.n_reactions == 0):
                    dfs[observables.index(observable)] = dfs[observables.index(observable)].append(((pd.DataFrame(tempArray[observables.index(observable)])).transpose()),ignore_index=True)
                
        counter +=1
    
    if kinetic_sens == 1 and bool(observables):
        ksensIndex = [timeHistory['time'].as_matrix(),gas.reaction_equations(),observables]
       
   
    
        numpyMatrixsksens = [dfs[dataframe].as_matrix() for dataframe in range(len(dfs))]
        
        numpyMatrixsBsens = [numpyMatrixsksens[x]*(np.log(timeHistory['temperature'].as_matrix().flatten()))[:,np.newaxis] for x in range(len(numpyMatrixsksens))]
        
        numpyMatrixsEsens = [numpyMatrixsksens[x]*1/ct.gas_constant*(np.true_divide(-1,timeHistory['temperature'].as_matrix().flatten()))[:,np.newaxis] for x in range(len(numpyMatrixsksens))]
        #numpyMatrixsEsens = [numpyMatrixsksens[x]*1/(np.true_divide(-1,timeHistory['temperature'].as_matrix().flatten()))[:,np.newaxis] for x in range(len(numpyMatrixsksens))]


        S = np.dstack(numpyMatrixsksens)

        
        
        
        
        Sa = numpyMatrixsksens
        Sb = numpyMatrixsBsens
        Se = numpyMatrixsEsens

       
       
    if physical_sens == 1 and bool(observables):
        dk=.01
        originalPsens = (timeHistory[observables]).applymap(np.log)
                        
        for numOfPhyParams in range(len(physical_params)):
            if physical_params[numOfPhyParams] == 'T':
                gas2 = ct.Solution(ctiFile)
                gas2.TPX = baseConditions[0]*np.exp(dk),baseConditions[1],baseConditions[2]
                if thermalBoundary == 'adiabatic': 
                    shockTube2 = ct.IdealGasConstPressureReactor(gas2,name = 'R1',energy= 'on')
                    sim2=ct.ReactorNet([shockTube2])
                if thermalBoundary == 'isothermal':
                    shockTube2 = ct.IdealGasConstPressureReactor(gas2,name = 'R1',energy= 'off')
                    sim2=ct.ReactorNet([shockTube2])
                    

                
                newTime = 0 
                newCounter = 0
                while newTime < finalTime:
                    newTime = sim2.step()
                    state = np.hstack([newTime, shockTube2.thermo.P, shockTube2.mass, 
                                shockTube2.T, shockTube2.thermo.X])
                    timeHistorytest.loc[newCounter] = state
                    newCounter +=1

                newTimeArray = timeHistorytest['time'] 
                #new
                temperatureForMappingPhysicalSensT = timeHistorytest['temperature'].values
                pressureForMappingPhysicalSensT = timeHistorytest['pressure'].values
                
                
                
                tempForInterp = timeHistorytest[observables]
            
                tempForInterplstT = [tempForInterp.ix[:,x].values for x in range(tempForInterp.shape[1])]
                
                interpolatedData = [np.interp(timeHistory['time'].values,newTimeArray.values,tempForInterplstT[x]) for x in range(len(tempForInterplstT))]
                #new
                interpolatedTemperatureForMappingPhysicalSensT = [np.interp(timeHistory['time'].values,newTimeArray.values,temperatureForMappingPhysicalSensT)]
                interpolatedPressureForMappingPhysicalSensT = [np.interp(timeHistory['time'].values,newTimeArray.values,pressureForMappingPhysicalSensT)]
                
                interpolatedData = [pd.DataFrame(interpolatedData[x]) for x in range(len(interpolatedData))]
                interpolatedData = pd.concat(interpolatedData, axis=1,ignore_index=True)
                
                concentrationOfAbsorbanceObservablesForSensT = interpolatedData
                concentrationOfAbsorbanceObservablesForSensT.columns = observables
                concentrationOfAbsorbanceObservablesForSensT = [concentrationOfAbsorbanceObservablesForSensT]
                

                tempT = interpolatedData.applymap(np.log)
                tempT.columns = observables
                #tempT = (originalPsens.subtract(tempT))/np.log(dk)
                tempT = (tempT.subtract(originalPsens)/dk)
                tempTlst = [tempT.ix[:,idx] for idx in range(tempT.shape[1])]
                
                
                
                
                 
                
            if physical_params[numOfPhyParams] == 'P':
                gas3 = ct.Solution(ctiFile)
                gas3.TPX = baseConditions[0],baseConditions[1]*np.exp(dk),baseConditions[2]
                if thermalBoundary == 'adiabatic':
                    shockTube3 = ct.IdealGasConstPressureReactor(gas3,name = 'R1',energy = 'on')
                    sim3 = ct.ReactorNet([shockTube3])
                if thermalBoundary =='isothermal':
                    shockTube3 = ct.IdealGasConstPressureReactor(gas3,name = 'R1', energy = 'off')
                    sim3 = ct.ReactorNet([shockTube3])
                    
                
                newTime2 = 0
                newCounter2 = 0
                while newTime2 < finalTime:
                    newTime2 = sim3.step()
                    state = np.hstack([newTime2, shockTube3.thermo.P, shockTube3.mass, 
                               shockTube3.T, shockTube3.thermo.X])
                    timeHistorytest2.loc[newCounter2] = state
                    newCounter2 +=1
                    
                newTimeArray2 = timeHistorytest2['time']
                temperatureForMappingPhysicalSensP = timeHistorytest2['temperature'].values
                pressureForMappingPhysicalSensP = timeHistorytest2['pressure'].values
                

                tempForInterp = timeHistorytest2[observables]
                tempForInterplstP = [tempForInterp.ix[:,x].values for x in range(tempForInterp.shape[1])]
                                     
                interpolatedData2 = [np.interp(timeHistory['time'].values,newTimeArray2.values,tempForInterplstP[x]) for x in range(len(tempForInterplstP))]
                 #new
                interpolatedTemperatureForMappingPhysicalSensP = [np.interp(timeHistory['time'].values,newTimeArray2.values,temperatureForMappingPhysicalSensP)]
                
                
                interpolatedPressureForMappingPhysicalSensP = [np.interp(timeHistory['time'].values,newTimeArray2.values,pressureForMappingPhysicalSensP)]    
                interpolatedData2 = [pd.DataFrame(interpolatedData2[x]) for x in range(len(interpolatedData2))]
                interpolatedData2 = pd.concat(interpolatedData2,axis=1,ignore_index=True)
                
                
                concentrationOfAbsorbanceObservablesForSensP = interpolatedData2
                concentrationOfAbsorbanceObservablesForSensP.columns = observables
                concentrationOfAbsorbanceObservablesForSensP = [concentrationOfAbsorbanceObservablesForSensP]
                
                
                tempP = interpolatedData2.applymap(np.log)
                tempP.columns = observables
                
                #tempP = (originalPsens.subtract(tempP))/dk
                tempP = tempP.subtract(originalPsens)/dk
                tempPlst = [tempP.ix[:,idx] for idx in range(tempP.shape[1])]
                                     
        
                
                            
            if physical_params[numOfPhyParams] == 'X':
                for simulationNumber ,  speciesName  in enumerate(speciesNames):
                    
                    
                    newConditions = originalConditions
                    gas4 = ct.Solution(ctiFile)
                    originalValue = conditions[speciesName]
                    newValue = originalValue*np.exp(dk)
                    newConditions.update({speciesName:newValue})
                    gas4.TPX = baseConditions[0],baseConditions[1], newConditions
                   
                    if thermalBoundary =='adiabatic':
                        shockTube4 = ct.IdealGasConstPressureReactor(gas4,name = 'R1',energy= 'on')
                        sim4 = ct.ReactorNet([shockTube4])
                    if thermalBoundary == 'isothermal':
                        shockTube4 = ct.IdealGasConstPressureReactor(gas4 ,name = 'R1', energy = 'off')
                        sim4 = ct.ReactorNet([shockTube4]) 
                    
    
                    newTime3 = 0
                    newCounter3 = 0
                    while newTime3 < finalTime:
                        newTime3 = sim4.step()                    
                        state = np.hstack([newTime3, shockTube4.thermo.P, shockTube4.mass, 
                                 shockTube4.T, shockTube4.thermo.X])
                        
                        timeHistorytest4[simulationNumber].loc[newCounter3] = state    
                        newCounter3 +=1
                    
                    newConditions.update({speciesName:originalValue})
                
                
                    
                newTimeArrays3 = [timeHistorytest4[simulationNumber]['time'] for simulationNumber in range(len(timeHistorytest4))]
                temperatureForMappingPhysicalSensX = [timeHistorytest4[simulationNumber]['temperature'] for simulationNumber in range(len(timeHistorytest4))]
                pressureForMappingPhysicalSensX = [timeHistorytest4[simulationNumber]['pressure'] for simulationNumber in range(len(timeHistorytest4))]
                
                tempForInterps = [timeHistorytest4[simulationNumber][observables] for simulationNumber in range(len(timeHistorytest4))]
                
                
                tempForInterplstXs = [[] for x in range(len(timeHistorytest4))]
                for simulationNumber in range(len(timeHistorytest4)):
                    for  x in range(tempForInterps[simulationNumber].shape[1]):
                        tempForInterplstXs[simulationNumber].append(tempForInterps[simulationNumber].ix[:,x].values)
                        

                
                interpolatedData3 = [[] for x in range(len(timeHistorytest4))]
                interpolatedTemperatureForMappingPhysicalSensX = []
                interpolatedPressureForMappingPhysicalSensX = []                     
                for simulationNumber in range(len(timeHistorytest4)):
                    for x in range(tempForInterps[simulationNumber].shape[1]):
                        interpolatedData3[simulationNumber].append(np.interp(timeHistory['time'].values,newTimeArrays3[simulationNumber].values,tempForInterplstXs[simulationNumber][x]))
                        
                for simulationNumber in range(len(timeHistorytest4)):
                    interpolatedTemperatureForMappingPhysicalSensX.append(np.interp(timeHistory['time'].values,newTimeArrays3[simulationNumber].values,temperatureForMappingPhysicalSensX[simulationNumber]))
                
                for simulationNumber in range(len(timeHistorytest4)):
                    interpolatedPressureForMappingPhysicalSensX.append(np.interp(timeHistory['time'].values,newTimeArrays3[simulationNumber].values,pressureForMappingPhysicalSensX[simulationNumber]))
                        
                        
                interpolatedDataFrames = [[] for x in range(len(timeHistorytest4))]

                
                for simulationNumber in range(len(timeHistorytest4)):
                    for x in range(tempForInterps[simulationNumber].shape[1]):
                        interpolatedDataFrames[simulationNumber].append(pd.DataFrame(interpolatedData3[simulationNumber][x]))
                        
                
                interpolatedDataFrames = [pd.concat(interpolatedDataFrames[simulationNumber],axis=1,ignore_index=True) for simulationNumber in range(len(timeHistorytest4))]
                concentrationOfAbsorbanceObservablesForSensX = interpolatedDataFrames
                
                for simulationNumber in range(len(timeHistorytest4)):
                    concentrationOfAbsorbanceObservablesForSensX[simulationNumber].columns = observables
                    
                interpolatedDataFrames = [interpolatedDataFrames[simulationNumber].applymap(np.log) for simulationNumber in range(len(timeHistorytest4))]
                for simulationNumber in range(len(timeHistorytest4)):
                    interpolatedDataFrames[simulationNumber].columns = observables
                #interpolatedDataFrames = [(originalPsens.subtract(interpolatedDataFrames[simulationNumber]))/np.log(dk) for simulationNumber in range(len(timeHistorytest4))]
                interpolatedDataFrames = [(interpolatedDataFrames[simulationNumber].subtract(originalPsens))/dk for simulationNumber in range(len(timeHistorytest4))]
                                          
                tempXlst = [[] for x in range(len(timeHistorytest4))]
                for simulationNumber in range(len(timeHistorytest4)):
                    for x in range(interpolatedDataFrames[simulationNumber].shape[1]):
                        tempXlst[simulationNumber].append(interpolatedDataFrames[simulationNumber].ix[:,x])
                        
              
                tempXlsts = [[] for x in range(len(observables))]
                             
                for lengthOfList in range(len(observables)):
                    for dfInList in range(len(timeHistorytest4)):
                        tempXlsts[lengthOfList].append(tempXlst[dfInList][lengthOfList])
                        
                tempXlsts = [pd.concat(tempXlsts[simulationNumber],axis=1,ignore_index=True) for simulationNumber in range(len(tempXlsts))]
                
                
                
    
                
 



                                

    #if physical_sens == 1 and bool(observables):         
    
    
        if 'T' in physical_params and 'P' in physical_params and 'X' in physical_params:
            t = [tempTlst,tempPlst,tempXlsts]
            psensIndex = [timeHistory['time'].as_matrix(),['T','P'] + physicalParamsSpecies ,observables]
            psensdfs = [pd.concat([t[0][x],t[1][x],t[2][x]],ignore_index = True , axis = 1) for x in range(len(tempXlsts))]
            numpyMatrixspsens = [psensdfs[dataframe].as_matrix() for dataframe in range(len(psensdfs))]
            pS=numpyMatrixspsens
#            pS = np.dstack(numpyMatrixspsens)
            interpolatedTemperatureForMappingPhysicalSens = [interpolatedTemperatureForMappingPhysicalSensT + interpolatedTemperatureForMappingPhysicalSensP + interpolatedTemperatureForMappingPhysicalSensX]
            interpolatedPressureForMappingPhysicalSens = [interpolatedPressureForMappingPhysicalSensT + interpolatedPressureForMappingPhysicalSensP + interpolatedPressureForMappingPhysicalSensX]
            concentrationOfAbsorbanceObservablesForSens = [concentrationOfAbsorbanceObservablesForSensT+concentrationOfAbsorbanceObservablesForSensP+concentrationOfAbsorbanceObservablesForSensX]
        elif 'T' in physical_params and 'P' in physical_params:
            t = [tempTlst,tempPlst]
            psensIndex = [timeHistory['time'].as_matrix(),['T','P'],observables]
            psensdfs = [pd.concat([t[0][x],t[1][x]],ignore_index=True,axis = 1) for x in range(len(tempTlst))]                
            numpyMatrixspsens = [psensdfs[dataframe].as_matrix() for dataframe in range(len(psensdfs))]
            pS=numpyMatrixspsens
#            pS = np.dstack(numpyMatrixspsens)
            interpolatedTemperatureForMappingPhysicalSens = [interpolatedTemperatureForMappingPhysicalSensT + interpolatedTemperatureForMappingPhysicalSensP ]
            interpolatedPressureForMappingPhysicalSens = [interpolatedPressureForMappingPhysicalSensT+ interpolatedPressureForMappingPhysicalSensP]
        elif 'T'in physical_params and 'X' in physical_params:
            t = [tempTlst,tempXlsts]
            psensIndex = [timeHistory['time'].as_matrix(),['T'] + physicalParamsSpecies ,observables]
            psensdfs = [pd.concat([t[0][x],t[1][x]], ignore_index = True, axis = 1) for x in range(len(tempTlst))]
            numpyMatrixspsens = [psensdfs[dataframe].as_matrix() for dataframe in range(len(psensdfs))]
            pS=numpyMatrixspsens
#            pS = np.dstack(numpyMatrixspsens)
            interpolatedTemperatureForMappingPhysicalSens = [interpolatedTemperatureForMappingPhysicalSensT  + interpolatedTemperatureForMappingPhysicalSensX] 
            interpolatedPressureForMappingPhysicalSens = [interpolatedPressureForMappingPhysicalSensT + interpolatedPressureForMappingPhysicalSensX]
        elif 'P'in physical_params and 'X' in physical_params:
            t = [tempPlst,tempXlsts]
            psensIndex = [timeHistory['time'].as_matrix(),['P'] + physicalParamsSpecies ,observables]
            psensdfs = [pd.concat([t[0][x],t[1][x]], ignore_index = True, axis = 1) for x in range(len(tempPlst))]
            numpyMatrixspsens = [psensdfs[dataframe].as_matrix() for dataframe in range(len(psensdfs))]
#            pS = np.dstack(numpyMatrixspsens)
            interpolatedTemperatureForMappingPhysicalSens = [interpolatedTemperatureForMappingPhysicalSensP + interpolatedTemperatureForMappingPhysicalSensX]
            interpolatedPressureForMappingPhysicalSens = [interpolatedPressureForMappingPhysicalSensP + interpolatedPressureForMappingPhysicalSensX]
        elif 'T' in physical_params:
            t = [tempTlst]
            psensIndex = [timeHistory['time'].as_matrix(),['T'],observables]
            numpyMatrixspsens = [tempTlst[dataframe].as_matrix() for dataframe in range(len(tempTlst))]
            pS=numpyMatrixspsens
#            pS = np.dstack(numpyMatrixspsens)
            interpolatedTemperatureForMappingPhysicalSens = [interpolatedTemperatureForMappingPhysicalSensT]
            interpolatedPressureForMappingPhysicalSens = [interpolatedPressureForMappingPhysicalSensT]
        elif 'P' in physical_params:
            t = [tempPlst]
            psensIndex = [timeHistory['time'].as_matrix(),['P'],observables]
            numpyMatrixspsens = [tempPlst[dataframe].as_matrix() for dataframe in range(len(tempPlst))]
            pS=numpyMatrixspsens
#            pS = np.dstack(numpyMatrixspsens)
            interpolatedTemperatureForMappingPhysicalSens = [interpolatedTemperatureForMappingPhysicalSensP]
            interpolatedPressureForMappingPhysicalSens = [interpolatedPressureForMappingPhysicalSensP ]
        elif 'X' in physical_params:
            t = [tempXlsts]
            psensIndex = [timeHistory['time'].as_matrix(),[physicalParamsSpecies],observables]
            numpyMatrixspsens = [tempXlsts[dataframe].as_matrix() for dataframe in range(len(tempXlsts))]
            pS=numpyMatrixspsens
#            pS = np.dstack(numpyMatrixspsens)
            interpolatedTemperatureForMappingPhysicalSens = [interpolatedTemperatureForMappingPhysicalSensX]
            interpolatedPressureForMappingPhysicalSens = [interpolatedPressureForMappingPhysicalSensX]
    
    
    speciesNames.append(addBackin)
    
    
    if kinetic_sens==1 and bool(observables) and physical_sens==0:  
        results = simulations.model_data('Shock-Tube',kinetic_sens = S  ,Solution = timeHistory, Index = ksensIndex)
        results.assign_ksens_mappings(Sa ,Sb, Se)
        return results 
        
    if kinetic_sens==0 and bool(physical_params) and physical_sens==1:
        results = simulations.model_data('Shock-Tube',physical_sens = pS, Solution = timeHistory, pIndex = psensIndex)
        results.add_interpolated_temps_for_physical_sens(interpolatedTemperatureForMappingPhysicalSens)
        results.add_interpolated_pressure_for_physical_sens(interpolatedPressureForMappingPhysicalSens)
        results.add_interpolated_concentration_for_physical_sens(concentrationOfAbsorbanceObservablesForSens)
        return results 

    if physical_sens==1 and bool(observables)and kinetic_sens==1:
        results = simulations.model_data('Shock-Tube',kinetic_sens = S, physical_sens = pS, Solution = timeHistory, Index = ksensIndex, pIndex = psensIndex)
        results.assign_ksens_mappings(Sa ,Sb, Se) 
        results.add_interpolated_temps_for_physical_sens(interpolatedTemperatureForMappingPhysicalSens)
        results.add_interpolated_pressure_for_physical_sens(interpolatedPressureForMappingPhysicalSens)
        results.add_interpolated_concentration_for_physical_sens(concentrationOfAbsorbanceObservablesForSens)
        results.addProduction(OHproduction,ratesOfProduction)
        return results 
#      
    if physical_sens == 0 and kinetic_sens == 0:
        results = simulations.model_data('Shock-Tube',Solution = timeHistory)
        
        return results