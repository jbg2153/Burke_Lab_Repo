# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 17:24:44 2018

@author: justi
"""

def chemEqn(eqn):
    '''
    Formats cantera reaction strings for matplotlib labels 
    with appropriate symbols including subscripts based on db 
    dict. Formatting only appears in matplotlib plots.
    
    FUTURE UPDATES:
        -transfer 'db' to database and upload
    '''

    ##########stub: replace with permanent solution#########
    db = {
        '=>': r'$\rightarrow$',
        '<=': r'$\leftarrow$',
        '<=>': r'$\leftrightharpoons$',
        '+' : '+',
        'c2h2': r'$C_2H_2$',
        'c2h3': r'$C_2H_3$',
        'ch3oh': r'$CH_3OH$',
        'c2h4': r'$C_2H_4$',
        'sc2h4oh': r'$sC_2H_4OH$',
        'c2h5': r'$C_2H_5$',
        'c2h5o': r'$C_2H_5O$',
        'c2h5oh': r'$C_2H_5OH$',
        'c2h6': r'$C_2H_6$',
        'ch2[s]': r'$CH_2(s)$',
        'ch2cho': r'$CH_2CHO$',
        'ch2o': r'$CH_2O$',
        'ch2oh': r'$CH_2OH$',
        'ch2opo2': r'$CH_2OPO_2$',
        'ch3': r'$CH_3$',
        'c3h6': r'$C_3H_6$',
        'c3h8': r'$C_3H_8$',
        'ch3o': r'$CH_3O$',
        'ch3o2': r'$CH_3O_2$',
        'ch3opo': r'$CH_3OPO$',
        'ch3opo2': r'$CH_3OPO_2$',
        'ch3po2': r'$CH_3PO_2$',
        'ch4': r'$CH_4$',
        'co': 'CO',
        'co2': r'$CO_2$',
        'h': 'H',
        'h2': '$H_2$',
        'h2o': r'$H_2O$',
        'h2o2': r'$H_2O_2$',
        'hcco': 'HCCO',
        'hco': 'HCO',
        'ho2': r'$HO_2$',
        'hocho': 'HOCHO',
        'hoch2o': r'$HOCH_2O$',
        'hopo': 'HOPO',
        'hopo2': r'$HOPO_2$',
        'hpo2': r'$HPO_2$',
        'o': 'O',
        'o2': r'$O_2$',
        'oh': 'OH',
        'pc2h4oh': r'$PC_2H_4OH$',
        'po2': r'$PO_2$',
        'po3': r'$PO_3$',
        'p[oh]3': r'$P(OH)_3$',
        'pome[oet]2': r'$POCH_3(OC_2H_5)2$',
        'po[oh]2me': r'$PO(OH)_2CH_3$',
        'p[oh]2[ome]': r'$P(OH)_2(OCH_3)$',
        'po[oh]3': r'$PO(OH)_3$',
        'po[oh]me': r'$PO(OH)CH_3$',
        'po[oh]me[oet]': r'$PO(OH)CH_3(OC_2H_5)$',
        'po[oh][ome]': r'$PO(OH)(OCH_3)$',
        'po[oh]2[ome]': r'$PO(OH)_2(OCH_3)$',
        'po[ome]2': r'$PO(OCH_3)_2$',
        'po[ome]2[och2]': r'$PO(OCH_3)_2(OCH_2)$',
        'po[ome]2o': r'$PO(OCH_3)_3O_2$',
        'po[ome]3': r'$PO(OCH_3)_3$'
    }
    ########################################################
    
    eqnList = eqn.split(' ')
    for i in range(len(eqnList)):
        if eqnList[i][0].isdigit():
            try:
                eqnList[i] = eqnList[i][0] + db[eqnList[i][1:]]
            except:
                pass
        elif eqnList[i][0].isalpha():
            try:
                eqnList[i] = db[eqnList[i]]
            except:
                pass
        else:
            try:
                eqnList[i] = db[eqnList[i]]
            except:
                pass
    return ' '.join(eqnList)