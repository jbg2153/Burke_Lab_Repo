# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 10:39:06 2018

@author: justi

Create and return dataframe with kinetic parameter uncertainties for each 
    reaction.
"""

import pandas as pd
import re

def react_split(reaction):
    '''
    Splits a chem. eqn into products and reactants.
    
    Input: chemical reaction equation (string)
    Output: list of products and reactants
            - list[0] = reactants
            - list[1] = products
    '''
    sList = re.split('=|<|>', reaction)
    sList = list(filter(None, sList))
    return sList

def species_split(species):
    '''
    Removes symbols from string of chemical species
    
    Input: products or reactants string with symbols
    Output: string containing only chemical species
    '''
    sList = re.split(' |\+|\(|\)',species)
    sList = list(filter(None, sList))
    return ' '.join(sorted(sList))  

def get_uncertainties(ct_eqns, uncert_file='uncertainty.csv'):
    
    #create df with all chemical equations from mechanism file and apply all caps
    df_reactions = pd.DataFrame(ct_eqns)
    df_reactions['Reaction'] = df_reactions['Reaction'].apply(lambda x: x.lower())
    
    #apply react_split and species_split to prep reactions for comparison
    #create df columns for reactants and products
    df_reactions = df_reactions.merge(
        df_reactions.Reaction.apply(
            lambda x: pd.Series(
                {
                    'Reactants':react_split(x)[0],
                    'Products':react_split(x)[1]
                }
            )
        ), 
        left_index=True,
        right_index=True
    )
    
    #remove symbols so that reactants and products columns contain only species
    df_reactions['Reactants'] = df_reactions['Reactants'].apply(lambda x: species_split(x))
    df_reactions['Products'] = df_reactions['Products'].apply(lambda x: species_split(x))
    
    try:
        #import uncertainty.csv file and create equivalent reactant and product columns
        df_uncert = pd.read_csv('uncertainty.csv')
        df_uncert['Reaction'] = df_uncert['Reaction'].apply(lambda x: x.lower())
        
        #apply react_split and species_split to prep reactions for comparison
        df_uncert = df_uncert.merge(
            df_uncert.Reaction.apply(
                lambda x: pd.Series(
                    {
                        'Reactants':react_split(x)[0],
                        'Products':react_split(x)[1]
                    }
                )
            ), 
            left_index=True,
            right_index=True
        )
        
        df_uncert['Reactants'] = df_uncert['Reactants'].apply(lambda x: species_split(x))
        df_uncert['Products'] = df_uncert['Products'].apply(lambda x: species_split(x))
        
        #merge uncertainties to mech file reactions progressing in SAME direction
        df_combined  = pd.merge(
            df_reactions[[
                'Reaction_ID',
                'Products',
                'Reactants',
                'Reaction'
            ]],
            df_uncert[[
                'Uncertainty A (unit)',
                'Uncertainty N (unit)',
                'Uncertainty Ea (unit)',
                'Products',
                'Reactants'
            ]],
            how='left',
            left_on=['Products','Reactants'],
            right_on=['Products','Reactants']
        )
        
        #merge uncertainties to mech file reactions progressing in OPPOSITE direction
        df_combined2 = pd.merge(
            df_combined[df_combined.isnull().any(axis=1)][[
                'Reaction_ID',
                'Products',
                'Reactants',
                'Reaction'
            ]],
            df_uncert[[
                'Uncertainty A (unit)',
                'Uncertainty N (unit)',
                'Uncertainty Ea (unit)',
                'Products',
                'Reactants'
            ]],
            how='left',
            left_on=['Reactants','Products'],
            right_on=['Products','Reactants']
        )
        
        df_combined2.drop(['Products_y','Reactants_y'],axis=1, inplace=True)
        df_combined2.rename(columns={'Products_x':'Products','Reactants_x':'Reactants'}, inplace=True)
        
        #merge both combined uncertainties dfs to create final uncertainties df
        df_combined3 = pd.merge(
            df_combined,
            df_combined2[[
                'Reaction_ID',
                'Uncertainty A (unit)',
                'Uncertainty N (unit)',
                'Uncertainty Ea (unit)'
            ]],
            how='left',
            left_on=['Reaction_ID'],
            right_on=['Reaction_ID']
        )
        
        #coalesce uncertainty columns to keep first non-null value per row
        for u in ['A','N','Ea']:    #stub: probably a bettter way to do this
            df_combined3['Uncertainty '+u+' (unit)_x'] = df_combined3[
                'Uncertainty '+u+' (unit)_x'
            ].fillna(df_combined3['Uncertainty '+u+' (unit)_y'])
        
        df_combined3.drop(
            [
                'Uncertainty A (unit)_y',
                'Uncertainty N (unit)_y',
                'Uncertainty Ea (unit)_y'
            ],
            inplace=True,
            axis=1
        )
        
        df_combined3.rename(
            columns={
                'Uncertainty A (unit)_x':'Uncertainty A (unit)',
                'Uncertainty N (unit)_x':'Uncertainty N (unit)',
                'Uncertainty Ea (unit)_x':'Uncertainty Ea (unit)'
            },
            inplace=True
        )
        
        df_combined3.drop_duplicates(inplace=True)
    
    #if no uncertainty reference file exists...
    except:
        for u in ['A','N','Ea']:
            df_combined3 = df_reactions
            df_combined3['Uncertainty '+u+' (unit)'] = ''
    
    #assign default values to null uncertainty fields
    for u in ['A','N','Ea']:
        col = 'Uncertainty '+u+' (unit)'
        if u == 'A':
            df_combined3[col].fillna(5, inplace=True)
        elif u == 'N':
            df_combined3[col].fillna(0, inplace=True)
        elif u == 'Ea':
            df_combined3[col].fillna(0, inplace=True)
    
    df_combined3.set_index('Reaction_ID', inplace=True)
    
    df_combined3.to_csv('uncert_temp.csv')
    
    return df_combined3


##################### TEST TEST TEST ########################
#get_uncertainties(
#    mech_file='mecph_v2b_3.cti',
#    uncert_file='uncertainty_WMD.csv'
#    )





