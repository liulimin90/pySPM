# -- coding: utf-8 --

# Copyright 2018 Olivier Scholder <o.scholder@gmail.com>

"""
Dictionary of common elements present for a given nominal mass
"""

elts = {
    12:'C',
    13:'CH',
    14:'CH2',
    15:'CH3',
    16:['O','NH2','^13CH3'],
    17:['OH','NH3'],
    18:'NH4',
    19:['H3O'],
    23:'Na',
    24:['Mg','C2'],
    25:['C2H'],
    26:['C2H2'],
    27:['C2H3','Al','CHN'],
    28:['Si','CH2N','C2H4','^13CCH3'],
    29:['^29Si','SiH','CHO','N2H','C2H5','CH3N'],
    30:['CH4N','C2H6'],
    31:['CF','CH3O','N2H3','CH5N','^13CH4N'],
    32:['S','O2','PH','CHF','CH4O','N2H4','CH6N'],
    33:['HS','O2H','NOH3','CH5O','N2H5','^13CH6N'],
    34:['^34S','H2S','NOH4','N2H6'],
    35:['H3S','N2H7'],
    36:['C3'],
    37:['C3H','NaN','C^25Mg'],
    38:['C3H2'],
    39:['C3H3','K'],
    40:['C2H2N','C3H4','C2O','CN2','Ca'],
    41:['C2H3N','C3H5','CaH','^41K','C2HO'],
    42:['C2H4N','C3H6','CH2N2'],
    43:['C2H5N','C3H7','CH3N2','C2H3O'],
    44:['C3H8','C2H6N','C2H4O','CH4N2','CH2NO','SiO'],
    45:['CHS','CHO2','C2H5O','CH5N2','C2H7N','C3H9'],
    46:['Na2','CH2S','NO2','CH4NO','C2H8N','^29SiHO'],
    47:['CH^34S','CH3S','CH3O2','CH7N2','C^13CH8N','SiF'],
    48:['C4','CH4S','SNH2','CH6NO','CH2^34S','SO'],
    49:['C4H','SOH','O3H','CH5S','SNH3','N2OH5','CH2Cl','CH5O2','^13CH4O2','NO2H3'],
    50:['O3H2','SOH2','^34SNH2','C4H2','C3N','CH6O2'],
    51:['C3HN','C4H3','CHF2'],
    52:['C3H2N','C4H4','C2N2'],
    53:['C4H5','C3H3N','C3HO','H3^34SO','C2HN2','CH2K'],
    54:['C3H4N','C3H2O','C4H6'],
    55:['C3H3O','C4H7','C3H5N','C2H3N2'],
    56:['C3H6N','C3H4O','C4H8','C2H2NO','C2H4N2'],
    57:['C2H3NO','C3H5O','C3H7N','C4H9','C2HS','C2H5N2','CaOH'],
    58:['CSN','C2H2S','N3O','C2H2O2','CH2N2O','N4H2','C3H8N','C2H4NO','C2H6N2','C3H6O'],
    59:['C3H7O','C2H5NO','C2H7N2','C3H9N','C2H3S'],
    60:['CSO','SN2','CH2SN','C2H4S','CH2NO2','C5','CH4N2O','C2H6NO','CH6N3','C3H8O','C2H8N2','C3H10N','C2H4O2'],
    61:['CHSO','SN2H','CHO3','CH3SN', 'N2O2H','C5H','C2H5S','CH3NO2','N3OH3','C2H5O2','CH5N2O','N4H5','C2H7NO','C2H9N2'],
    62:['SNO','CH2SO','NO3','C5H2','C2H6S','CH4NO2','C2H8NO','C3H10O'],
    74:['C3H8NO','CH2N2O2','C2H4NO2','C3H6O2','C3H10N2','C4H12N','C4H10O','C2H8N3','C2H6N2O','C3H6S','C6H2','C2H4SN','C5N','C2H2O3']
   }