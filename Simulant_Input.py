# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 21:31:53 2018

@author: justi
"""
from Simulant_Model import uncert_sens

output_dict = dict()

##########################################################
#run1 = uncert_sens(
#    ctiFile = 'mecph_v2b.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['air'],
#    Fuel = 'TMP',
#    CaseName = 'Air Diluent-1',
#    pressure = 15, #atm
#    temperature = 1200, #Kelvin
#    concentrations = {
#            'po[ome]3':0.01,
#            'o2':0.99*1/4.76,
#            'n2':0.99*3.76/4.76
#            },
#    initialTime = 0,
#    finalTime = 0.002, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','po[ome]3'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#)
#output_dict['TMP_air_1'] = run1

##########################################################
#run2 = uncert_sens(
#    ctiFile = 'mecph_v2b.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['ar'],
#    Fuel = 'TMP',
#    CaseName = 'Argon Diluent-1',
#    pressure = 15, #atm
#    temperature = 1500, #Kelvin
#    concentrations = {
#            'po[ome]3':0.01,
#            'ar':0.99
#            },
#    initialTime = 0,
#    finalTime = 0.01, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','po[ome]3'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#)
#output_dict['TMP_argon_1'] = run2
#
##########################################################
#run3 = uncert_sens(
#    ctiFile = 'mecph_v2b.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['ar'],
#    Fuel = 'TMP',
#    CaseName = 'Argon-Air Diluent-1',
#    pressure = 15, #atm
#    temperature = 1200, #Kelvin
#    concentrations = {
#            'po[ome]3':0.01,
#            'ar':0.90,
#            'o2': .018908,
#            'n2': .071092
#            },
#    initialTime = 0,
#    finalTime = 0.01, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','po[ome]3'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#)
#output_dict['TMP_argon_air_1'] = run3
#
##########################################################
#run4 = uncert_sens(
#    ctiFile = 'mecph_v2b_2.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['air'],
#    Fuel = 'DEMP',
#    CaseName = 'Air Diluent-1',
#    pressure = 15, #atm
#    temperature = 1200, #Kelvin
#    concentrations = {
#            'pome[oet]2':0.01,
#            'o2':0.99*1/4.76,
#            'n2':0.99*3.76/4.76
#            },
#    initialTime = 0,
#    finalTime = 0.002, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oet]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#)
#output_dict['DEMP_air_1'] = run4
#
#########################################################
#run5 = uncert_sens(
#    ctiFile = 'mecph_v2b_2.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['ar'],
#    Fuel = 'DEMP',
#    CaseName = 'Argon Diluent-1',
#    pressure = 15, #atm
#    temperature = 1500, #Kelvin
#    concentrations = {
#            'pome[oet]2':0.01,
#            'ar':0.99
#            },
#    initialTime = 0,
#    finalTime = 0.01, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oet]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#)
#output_dict['DEMP_argon_1'] = run5
#
#########################################################
run6 = uncert_sens(
    ctiFile = 'mecph_v2b_3.cti',
    mech = 'incineration_Glaude',
    speciesNames = ['ar'],
    Fuel = 'DEMP',
    CaseName = 'Argon-Air Diluent-1',
    pressure = 15, #atm
    temperature = 1200, #Kelvin
    concentrations = {
            'pome[oet]2':0.01,
            'ar':0.90,
            'o2': .018908,
            'n2': .071092
            },
    initialTime = 0,
    finalTime = 0.01, # seconds
    thermalBoundary = 'adiabatic',
    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oet]2'],
    physicalParams = list(),
    kinetic_sens = 1, #default = 0
    physical_sens = 0, #default = 0
    reactorType = 'cv' #default = 'cv'
)
output_dict['DEMP_argon_air_1'] = run6