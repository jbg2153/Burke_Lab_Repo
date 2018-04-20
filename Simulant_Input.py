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
#    reactorType = 'cv' #default = 'cv',
#    logyaxis = True, #default = False
#)
#output_dict['TMP_air_1'] = run1
#
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
#    observables = ['ch3','h','oh','o','ho2'], #['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','po[ome]3'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#    logyaxis = True, #default = False
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
#    logyaxis = True, #default = False
#)
#output_dict['TMP_argon_air_1'] = run3
#
##########################################################
#run4 = uncert_sens(
#    ctiFile = 'mecph_v2b_3.cti',
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
#    finalTime = 0.00025, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oet]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#    logyaxis = True, #default = False
#)
#output_dict['DEMP_air_1'] = run4
#
#########################################################
#run5 = uncert_sens(
#    ctiFile = 'mecph_v2b_3.cti',
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
#    logyaxis = True, #default = False
#)
#output_dict['DEMP_argon_1'] = run5
#
#########################################################
#run6 = uncert_sens(
#    ctiFile = 'mecph_v2b_3.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['ar'],
#    Fuel = 'DEMP',
#    CaseName = 'Argon-Air Diluent-1',
#    pressure = 15, #atm
#    temperature = 1200, #Kelvin
#    concentrations = {
#            'pome[oet]2':0.01,
#            'ar':0.90,
#            'o2': .018908,
#            'n2': .071092
#            },
#    initialTime = 0,
#    finalTime = 0.01, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oet]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#    logyaxis = True, #default = False
#)
#output_dict['DEMP_argon_air_1'] = run6
#
##########################################################
#run7 = uncert_sens(
#    ctiFile = 'mecph_v2b.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['air'],
#    Fuel = 'DIMP',
#    CaseName = 'Air Diluent-1',
#    pressure = 15, #atm
#    temperature = 1200, #Kelvin
#    concentrations = {
#            'pome[oipr]2':0.01,
#            'o2':0.99*1/4.76,
#            'n2':0.99*3.76/4.76
#            },
#    initialTime = 0,
#    finalTime = 0.00025, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oipr]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#    logyaxis = True, #default = False
#)
#output_dict['DIMP_air_1'] = run7
#
#########################################################
#run8 = uncert_sens(
#    ctiFile = 'mecph_v2b.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['ar'],
#    Fuel = 'DIMP',
#    CaseName = 'Argon Diluent-1',
#    pressure = 15, #atm
#    temperature = 1500, #Kelvin
#    concentrations = {
#            'pome[oipr]2':0.01,
#            'ar':0.99
#            },
#    initialTime = 0,
#    finalTime = 0.01, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oipr]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#    logyaxis = True, #default = False
#)
#output_dict['DIMP_argon_1'] = run8
#
#########################################################
#run9 = uncert_sens(
#    ctiFile = 'mecph_v2b.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['ar'],
#    Fuel = 'DIMP',
#    CaseName = 'Argon-Air Diluent-1',
#    pressure = 15, #atm
#    temperature = 1200, #Kelvin
#    concentrations = {
#            'pome[oipr]2':0.01,
#            'ar':0.90,
#            'o2': .018908,
#            'n2': .071092
#            },
#    initialTime = 0,
#    finalTime = 0.01, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['co','co2','oh','ch4','h2o','c2h4','ch2o','c2h2','pome[oipr]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cv' #default = 'cv'
#    logyaxis = True, #default = False
#)
#output_dict['DIMP_argon_air_1'] = run9
#
#########################################################
#run10 = uncert_sens(
#    ctiFile = 'mecph_v2b_3.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['n2'],
#    Fuel = 'DEMP',
#    CaseName = 'Nitrogen Diluent-1',
#    pressure = 1, #atm
#    temperature = 802, #Kelvin
#    concentrations = {
#            'pome[oet]2':0.0036,
#            'n2':1-0.0036
#            },
#    initialTime = 0,
#    finalTime = 0.075, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['c2h5oh','c2h4','pome[oet]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cp', #default = 'cv'
#    logyaxis = False, #default = False
#    ylimits = (0,.0036) #default = None
#)
#output_dict['DEMP_nitrogen_1'] = run10
#
#########################################################
#run11 = uncert_sens(
#    ctiFile = 'mecph_v2b_3.cti',
#    mech = 'incineration_Glaude',
#    speciesNames = ['n2'],
#    Fuel = 'DIMP',
#    CaseName = 'Nitrogen Diluent-1',
#    pressure = 1, #atm
#    temperature = 753, #Kelvin
#    concentrations = {
#            'pome[oipr]2':0.0115,
#            'n2':1-0.0115
#            },
#    initialTime = 0,
#    finalTime = 0.08, # seconds
#    thermalBoundary = 'adiabatic',
#    observables = ['ic3h7oh','c3h6','pome[oipr]2'],
#    physicalParams = list(),
#    kinetic_sens = 1, #default = 0
#    physical_sens = 0, #default = 0
#    reactorType = 'cp', #default = 'cv'
#    logyaxis = False, #default = False
#    ylimits = (0.00001, .017)
#)
#output_dict['DIMP_nitrogen_1'] = run11