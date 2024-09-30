# -*- coding: utf-8 -*-
__author__ = ['Gregory A. Greene, map.n.trowel@gmail.com']

import os
import time
from datetime import datetime
import PySimpleGUI as sg
import bcwft2018
import fiona
import pandas as pd
import numpy as np
import geopandas as gpd
import ProcessFeatures as pf
import multiprocessing as mp
from multiprocessing import current_process, Value, Lock
from typing import Union
import traceback
import logging
import warnings

coastInteriorToolTip = '''A code indicating that the stand is located in the Coast or Interior Region of the Province.
The Coast Region is defined as the mainland west of the Cascade and Coast Mountains, including the off-shore
islands. Forest Inventory Zones (FIZ) A to C are included in the Coast region. The Interior Region is defined
as the mainland east of the Cascade and Coast Mountains. Forest Inventory Zones (FIZ) D to L are
included in the Interior Region.'''
vegetatedToolTip = '''V = Vegetated
    A site is considered Vegetated when the total cover of trees, shrubs, herbs, and bryoids (other than
    crustose lichens) covers at least 5% of the total surface area of the site.
N = Non-Vegetated
    A site is considered Non-Vegetated when the total cover of trees, shrubs, herbs, and bryoids (other
    than crustose lichens) covers less than 5% of the total surface area of the site. Bodies of water are to
    be classified as Non-Vegetated.'''
landCoverToolTip = '''T = Treed
    A site is considered Treed if at least 10% of the site area, by crown cover, consists of tree species
    of any size. A site can only be Treed if it is vegetated.
N = Non-treed
    A site is considered Non-Treed if less than 10% of the site area, by crown cover, consists of tree
    species of any size. A site can only be Non-treed if it is vegetated.
L = Land
    The portion of the landscape not covered by water (as defined below), based on the percentage area
    coverage. A site can only be Land if it is Non-vegetated.
W = Water
    A naturally occurring, static body of water, two or more metres deep in some portion, or a watercourse
    formed when water flows between continuous, definable banks. These flows may be intermittent or
    perennial; but do not include ephemeral flows where a channel with no definable banks is present. Islands
    within streams that have definable banks are not part of the stream; gravel bars are part of the stream.
    Interpretation is based on the percentage area coverage.  A site can only be Water if it is Non-vegetated.'''
standardInventoryCodeToolTip = '''Code indicating under which inventory standard the data was collected.
V = Vegetation Resources Inventory (VRI)
F = Forest Inventory Planning (FIP)
I = Incomplete (when a full set of VRI attributes is not collected)
L = Landscape Vegetation Inventory (LVI)'''
landCoverClassCodeToolTip = '''The Land Cover Class Code describes the first most dominate land cover type by percent 
area occupied within the polygon that contribute to the overall polygon description, but may be too small to be
spatially identified. The sub-division of a polygon by a quantified Land Cover Component, allowing non-
spatial resolution for modeling of wildlife habitat capability.

NON-VEGETATED:\t\tVEGETATED:\t\t\tWATER COVER:
SI = Snow/ice\t\t\tTB = Treed Broadleaf\t\tLA = Lake
GL = Glacier\t\t\tTC = Treed Coniferous\t\tRE = Reservoir
PN = Snow cover\t\t\tTM = Treed Mixed\t\tRI = River/stream
RO = Rock/rubble\t\t\tST = Shrub Tall\t\t\tOC = Ocean
BR = Bedrock\t\t\tSL = Shrub Low
TA = Talus\t\t\tHE = Herb
BL = Blockfiend\t\t\tHF = Herb - Fords
MZ = Rubbly mine spoils\t\tHG = Herb - Graminoids
LB = Lava bed\t\t\tBY = Bryoid
EL = Exposed Land\t\tBM = Bryoid - Moss
RS = River Sediments\t\tBL = Bryoid - Lichens
ES = Exposed soil
LS = Pond or land sediments
RM = Reservoir margin
BE = Beach
LL = Landing
BU = Burned area
RZ = Road surface
MY = Mudflat sediments
CB = Cutbank
MN = Moraine
GP = Gravel pit
TZ = Tailings
RN = Railway
UR = Urban
AP = Airport
MI = Open pit mine
OT = Other'''
nonVegCoverTypeToolTip = '''Non-vegetated cover type is the designation for the predominate observable non-vegetated 
land cover within the site. Non-vegetated cover types provide detailed reporting for non-vegetated land cover.

LAND COVER:\t\t\tWATER COVER:
GL = Glacier\t\t\tOT = Other
PN = Snow cover\t\t\tLA = Lake
BR = Bedrock\t\t\tRE = Reservoir
TA = Talus\t\t\tRI = River/stream
BL = Blockfield\t\t\tDW = Downwood
MZ = Rubbly mine spoils\t\tOC = Ocean
LB = Lava bed
RS = River sediments
ES = Exposed soil
LS = Pond or lake sediments
RM = Reservoir margin
BE = Beach
LL = Landing
BU = Burned
RZ = Road surface
MU = Mudflat sediment
GP = Gravel pit
TZ = Tailings
RN = Railway
UR = Urban
AP = Airport
MI = Open pit mine'''
canopyCoverToolTip = '''Tree canopy cover is the percentage of ground area covered by the vertically projected 
crowns of trees for each tree layer (1-3) within the site and provides an essential estimate of the vertical projection 
of tree crowns upon the ground.'''
spDeOpToolTip = '''DE = Dense
    Tree, shrub, or herb cover is between 61% and 100% for the site.
OP = Open
    Tree, shrub, or herb cover is between 26% and 60% for the site.
SP = Sparse
    Cover is between 10% and 25% for treed sites, or cover is between 20% and 25% for shrub or herb
    sites.'''


def isNumber(s: str) -> bool:
    """
    Function to determine if a string is a number
    :param s: input string object
    :return: True or False
    """
    try:
        float(f'{s}')
        return True
    except ValueError:
        return False


def valuesValid(inValues: dict,
                treeList: list,
                becZones: list,
                becSubzones: list) -> Union[bool, str]:
    """
    Function to validate input values
    :param inValues: A dictionary of input values to compare
    :param treeList: A list of tree species
    :param becZones: A list of BEC zones
    :param becSubzones: A list of BEC subzones
    :return: False if no errors found. A string containing the errors otherwise.
    """
    try:
        errorList = []

        if not inValues['BEC_ZONE_CODE'] in becZones:
            errorList.append('BEC Zone Invalid')

        if not inValues['BEC_SUBZONE'] in becSubzones:
            errorList.append('BEC Subzone Invalid')

        if not isNumber(inValues['PROJ_AGE_1']):
            errorList.append('Stand Age Invalid')

        if not isNumber(inValues['PROJ_HEIGHT_1']):
            errorList.append('Stand Height Invalid')

        if not isNumber(inValues['VRI_LIVE_STEMS_PER_HA']):
            errorList.append('Live Tree Count Invalid')

        if not isNumber(inValues['VRI_DEAD_STEMS_PER_HA']):
            errorList.append('Dead Tree Count Invalid')

        if not isNumber(inValues['STAND_PERCENTAGE_DEAD']):
            errorList.append('Dead Tree Percentage Invalid')

        if inValues['CROWN_CLOSURE'] != '':
            if float(inValues['CROWN_CLOSURE']) > 100:
                errorList.append('Canopy Cover Exceeds 100%')

        i = 1
        sumPercent = 0
        while i <= 6:
            if inValues[f'SPECIES_CD_{i}'] != '':
                if not inValues[f'SPECIES_CD_{i}'].upper() in treeList:
                    errorList.append(f'Species {i} Code Invalid')
            if inValues[f'SPECIES_PCT_{i}'] != '':
                if not isNumber(inValues[f'SPECIES_PCT_{i}']):
                    errorList.append(f'Species {i} Percent Invalid')
                else:
                    sumPercent += float(inValues[f'SPECIES_PCT_{i}'])
            i += 1

        if (inValues['BCLCS_LEVEL_2'] == 'T') and (inValues['SPECIES_CD_1'] == ''):
            errorList.append('Species 1 Code Must Have A Value')

        if (sumPercent != 100) or (sumPercent > 100):
            errorList.append('Species Percents Not = 100')

        if errorList:
            errorString = ''
            for i in errorList:
                errorString += f'{i}\n'
            return errorString
        else:
            return False
    except:
        return 'ERROR: Unable to assess validity of input data'


def read_and_process_features(process_all: bool,
                              feature_slice: slice,
                              season: str,
                              fields_to_extract: list,
                              gdb_path: str,
                              feature_class: str,
                              counter: Value,
                              lock: Lock) -> gpd.GeoDataFrame:
    """
    Function to read data from the feature class, filter the fields, and run the fuel typing algorithm
    :param process_all: If True, process all features. If false, only process features without "FuelType" values
    :param feature_slice: A slice representing the rows to process in the VRI dataset
    :param season: season for fuel typing assignments. Options: "growing", "dormant"
    :param fields_to_extract: the fields in the VRI dataset that are needed for BCWFT fuel typing
    :param gdb_path: path to the gdb containing the VRI dataset
    :param feature_class: name of the VRI feature class
    :param counter: the shared multiprocessing counter object to track the number of features processed
    :param lock: the shared multiprocessing lock object
    :return: a geopandas GeoDataframe object containing the fuel type data for the current feature slice
    """
    process_id = current_process().name
    print(f'\t[{process_id}] Processing chunk: {feature_slice}')

    # Get a geodataframe object of the current VRI feature slice
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        slice_gdf = gpd.read_file(gdb_path, layer=feature_class, columns=fields_to_extract, rows=feature_slice)

    # Ensure all values in date columns are datetime objects
    slice_gdf['EARLIEST_NONLOGGING_DIST_DATE'] = pd.to_datetime(slice_gdf['EARLIEST_NONLOGGING_DIST_DATE'],
                                                                errors='coerce')
    slice_gdf['HARVEST_DATE'] = pd.to_datetime(slice_gdf['HARVEST_DATE'],
                                               errors='coerce')

    # Reorder the columns
    slice_gdf = slice_gdf[fields_to_extract]

    # Instantiate the bcwft2018 FuelTyping class
    bcwft = bcwft2018.FuelTyping()

    # Run fuel typing
    if process_all:
        # Add the BCWFT fields to the geodataframe
        slice_gdf[['BCWFT_rowRef', 'FuelType', 'FT_Modifier']] = None
        # Get the fuel types
        for index, row in slice_gdf.iterrows():
            try:
                result = bcwft.getFuelType(season, *row[:32])
                if not isinstance(result, type(None)):
                    slice_gdf.at[index, 'BCWFT_rowRef'] = result[0]
                    slice_gdf.at[index, 'FuelType'] = result[1]
                    slice_gdf.at[index, 'FT_Modifier'] = result[2]
                else:
                    slice_gdf.at[index, 'BCWFT_rowRef'] = None
                    slice_gdf.at[index, 'FuelType'] = 'NoneTypeReturn-ERROR'
                    slice_gdf.at[index, 'FT_Modifier'] = None
            except Exception as err:
                # Assign FuelType as error
                slice_gdf.at[index, 'FuelType'] = 'FuelTyping-Error'
                # Print error messages
                print(row, feature_slice)
                print(f'An exception occurred: {err}')
                print(logging.error(traceback.format_exc()))
                # Allow the code to continue
                pass
    else:
        # Get a subset of slice_gdf that contains no data values
        partial_gdf = slice_gdf[slice_gdf['FuelType'].isna()]
        # Get the fuel types
        for index, row in partial_gdf.iterrows():
            (partial_gdf.at[index, 'BCWFT_rowRef'],
             partial_gdf.at[index, 'FuelType'],
             partial_gdf.at[index, 'FT_Modifier']) = bcwft.getFuelType(season, *row[:32])
        # Add the new data to the geodataframe
        slice_gdf.update(partial_gdf)

    # Update the counter in a thread-safe manner
    with lock:
        counter.value += len(slice_gdf)

    return slice_gdf


def main():
    # Remove stale tasks and set initial values for tool functions
    # sg.theme('DarkAmber')   # Add a touch of color if desired (other themes available)
    bcwft = bcwft2018.FuelTyping()
    treeList = bcwft.treeList
    fldList = bcwft.fldList
    df = pd.DataFrame([], columns=fldList)
    df = pd.concat([df, pd.Series(name='UserData', dtype='object')], axis=1)
    df.loc['UserData'] = np.nan
    fldDT_List = bcwft.fldDTypes
    fldDT = dict(zip(fldList, fldDT_List))
    fldDTypes = pd.DataFrame(fldDT, index=['i', ])
    becZones = bcwft.becZones
    becSubzones = bcwft.becSubzones

    ftList = []
    BAR_MAX = 1

    standCols = [[sg.T('')],
                 [sg.T('STAND INFO', font=('Helvetica', 10), text_color='black')],
                 [sg.T('Stand Age (yrs):'), sg.In('120', size=(5, 1), key='PROJ_AGE_1', background_color='white',
                                                  disabled_readonly_background_color='gray', enable_events=True),
                  sg.T('Stand Height (m):'), sg.In('45', size=(5, 1), key='PROJ_HEIGHT_1', background_color='white',
                                                   disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Canopy Cover (%):'),
                  sg.In('40', size=(5, 1), key='CROWN_CLOSURE', tooltip=canopyCoverToolTip, background_color='white',
                        disabled_readonly_background_color='gray', enable_events=True),
                  sg.T('(SP)arse, (OP)en, or (DE)nse:'),
                  sg.In('OP', size=(5, 1), key='BCLCS_LEVEL_5', tooltip=spDeOpToolTip, background_color='white',
                        disabled_readonly_background_color='gray', enable_events=True, disabled=True)],
                 [sg.T('Live Stems (per ha):'),
                  sg.In('200', size=(5, 1), key='VRI_LIVE_STEMS_PER_HA', background_color='white',
                        disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Dead Stems (per ha):'),
                  sg.In('100', size=(5, 1), key='VRI_DEAD_STEMS_PER_HA', background_color='white',
                        disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('% Dead (relative BA per ha):'),
                  sg.In('33', size=(5, 1), key='STAND_PERCENTAGE_DEAD', background_color='white',
                        disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Species 1   '),
                  sg.T('Code:'),
                  sg.Combo(treeList, default_value='PY', size=(5, 1), key='SPECIES_CD_1', background_color='white',
                           enable_events=True),
                  sg.T('Percent:'), sg.In('90', size=(4, 1), key='SPECIES_PCT_1', background_color='white',
                                          disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Species 2   '),
                  sg.T('Code:'),
                  sg.Combo(treeList, default_value='FDI', size=(5, 1), key='SPECIES_CD_2', background_color='white',
                           enable_events=True),
                  sg.T('Percent:'), sg.In('10', size=(4, 1), key='SPECIES_PCT_2', background_color='white',
                                          disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Species 3   '),
                  sg.T('Code:'),
                  sg.Combo(treeList, default_value='', size=(5, 1), key='SPECIES_CD_3', background_color='white',
                           enable_events=True),
                  sg.T('Percent:'), sg.In('', size=(4, 1), key='SPECIES_PCT_3', background_color='white',
                                          disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Species 4   '),
                  sg.T('Code:'),
                  sg.Combo(treeList, default_value='', size=(5, 1), key='SPECIES_CD_4', background_color='white',
                           enable_events=True),
                  sg.T('Percent:'), sg.In('', size=(4, 1), key='SPECIES_PCT_4', background_color='white',
                                          disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Species 5   '),
                  sg.T('Code:'),
                  sg.Combo(treeList, default_value='', size=(5, 1), key='SPECIES_CD_5', background_color='white',
                           enable_events=True),
                  sg.T('Percent:'), sg.In('', size=(4, 1), key='SPECIES_PCT_5', background_color='white',
                                          disabled_readonly_background_color='gray', enable_events=True)],
                 [sg.T('Species 6   '),
                  sg.T('Code:'),
                  sg.Combo(treeList, default_value='', size=(5, 1), key='SPECIES_CD_6', background_color='white',
                           enable_events=True),
                  sg.T('Percent:'), sg.In('', size=(4, 1), key='SPECIES_PCT_6', background_color='white',
                                          disabled_readonly_background_color='gray', enable_events=True)]]

    fuelTypeOut = [[sg.T('')],
                   [sg.T('')],
                   [sg.T('FUEL TYPE', size=(10, 1), font=('Helvetica', 20), text_color='black',
                         justification='center')],
                   [sg.T('', size=(10, 1), font=('Helvetica', 46), justification='center', key='ftOut',
                         background_color='black')],
                   [sg.Button('Model Fuel Type')]]

    standFuelType = [[sg.T('')],
                     [sg.Checkbox('Enable Advanced Options', key='advanced', checkbox_color='white', text_color='black',
                                  enable_events=True, default=False)],
                     [sg.T('Inventory Standard Code:', text_color='black'),
                      sg.Combo(['V', 'F', 'I', 'L'], default_value='F', size=(4, 1), key='INVENTORY_STANDARD_CD',
                               tooltip=standardInventoryCodeToolTip, background_color='white', enable_events=True,
                               disabled=True),
                      sg.T('Vegetation Status:', text_color='black'),
                      sg.Combo(['V', 'N'], default_value='V', size=(4, 1), key='BCLCS_LEVEL_1',
                               tooltip=vegetatedToolTip, background_color='white', enable_events=True, disabled=True),
                      sg.T('Land Cover Type:', text_color='black'),
                      sg.Combo(['T', 'L', 'W', 'N'], default_value='T', size=(4, 1), key='BCLCS_LEVEL_2',
                               tooltip=landCoverToolTip, background_color='white', enable_events=True, disabled=True)],

                     [sg.T('Land Cover Class Code:', text_color='black'),
                      sg.Combo(['', 'BL', 'BM', 'BY', 'HE', 'HF', 'HG', 'SL', 'ST', 'TB', 'TC', 'TM',
                                'AP', 'BE', 'BL', 'BR', 'BU', 'CB', 'EL', 'ES', 'GL', 'GP', 'LB', 'LL', 'LS', 'MI',
                                'MN',
                                'MY', 'MZ', 'OT', 'PN', 'RM', 'RN', 'RO', 'RS', 'RZ', 'SI', 'TA', 'TZ', 'UR',
                                'LA', 'OC', 'RE', 'RI'],
                               default_value='', size=(4, 1), key='LAND_COVER_CLASS_CD_1',
                               tooltip=landCoverClassCodeToolTip, background_color='white', enable_events=True,
                               disabled=True),
                      sg.T('Non Veg Cover Type:', text_color='black'), sg.Combo(
                         ['', 'AP', 'BE', 'BL', 'BR', 'BU', 'ES', 'GL', 'GP', 'LB', 'LL', 'LS', 'MI', 'MU', 'MZ', 'PN',
                          'RM',
                          'RN', 'RS', 'RZ', 'TA', 'TZ', 'UR', 'DW', 'LA', 'OC', 'OT', 'RI', 'RE'],
                         default_value='', size=(4, 1), key='NON_VEG_COVER_TYPE_1',
                         tooltip=nonVegCoverTypeToolTip, background_color='white', enable_events=True, disabled=True)],
                     [sg.T('')],
                     [sg.T('SITE INFO', font=('Helvetica', 10), text_color='black')],
                     [sg.T('Site Location - (C)oast or (I)nterior:'),
                      sg.Combo(['C', 'I'], default_value='I', size=(4, 1), key='COAST_INTERIOR_CD',
                               tooltip=coastInteriorToolTip, background_color='white', enable_events=True)],
                     [sg.T('BEC Zone:'),
                      sg.Combo(becZones, default_value='PP', size=(7, 1), key='BEC_ZONE_CODE', background_color='white',
                               enable_events=True),
                      sg.T('Subzone:'),
                      sg.Combo(becSubzones, default_value='xh', size=(7, 1), key='BEC_SUBZONE',
                               background_color='white', enable_events=True)],
                     [sg.T('Growing Season:'),
                      sg.Combo(['Trees Growing -or- Standing Dead Grass', 'Trees Dormant -or- Matted Grass'],
                               default_value='Trees Growing -or- Standing Dead Grass',
                               size=(40, 1), key='standSeason', enable_events=True)],
                     [sg.T('')],
                     [sg.T('DISTURBANCE INFO', font=('Helvetica', 10), text_color='black')],
                     [sg.T('Site Harvested (Clearcut Only):'),
                      sg.Radio('No', "radioHarvest", key='harvNo', enable_events=True, default=True),
                      sg.Radio('Yes', "radioHarvest", key='harvYes', enable_events=True)],
                     [sg.T('\tHarvest Date (YYYY-MM-DD):'),
                      sg.In('', size=(11, 1), key='HARVEST_DATE', background_color='white',
                            disabled_readonly_background_color='gray', enable_events=True, disabled=True),
                      sg.CalendarButton('Choose Date', target='HARVEST_DATE', key='harvCalendar', format='%Y-%m-%d',
                                        disabled=True)],
                     [sg.T('Other Disturbances'),
                      sg.Radio('No', "radioDisturbance", key='distNo', enable_events=True, default=True),
                      sg.Radio('Yes', "radioDisturbance", key='distYes', enable_events=True)],
                     [sg.T(
                         '\tMost Recent Disturbance Type: (B) Wildfire, (IBM) Mountain Pine Beetle - Lodgepole Pine Only'),
                         sg.Combo(['B', 'IBM'], size=(4, 1), key='EARLIEST_NONLOGGING_DIST_TYPE',
                                  background_color='white',
                                  enable_events=True, disabled=True)],
                     [sg.T('\tDisturbance Date (YYYY-MM-DD):'),
                      sg.In('', size=(11, 1), key='EARLIEST_NONLOGGING_DIST_DATE', background_color='white',
                            disabled_readonly_background_color='gray', enable_events=True, disabled=True),
                      sg.CalendarButton('Choose Date', target='EARLIEST_NONLOGGING_DIST_DATE', key='distCalendar',
                                        format='%Y-%m-%d', disabled=True)],
                     [sg.Column(standCols),
                      sg.Column(fuelTypeOut, justification='center', element_justification='center')],
                     [sg.Button('Reset Inputs')]
                     ]

    vriFuelType = [
        [sg.T('')],
        [sg.T('Select Folder or GDB Containing VRI Dataset:')],
        [sg.In('', size=(70, 1), key='inVRI_Source', background_color='white',
               disabled_readonly_background_color='gray', enable_events=True),
         sg.FolderBrowse(key="folderIn")],
        [sg.T('')],
        [sg.T('Select Dataset:')],
        [sg.Listbox(ftList, size=(50, 10), key='inVRI', enable_events=True)],
        [sg.T('')],
        [sg.T('Select Season:')],
        [sg.Combo(['Trees Growing -or- Standing Dead Grass', 'Trees Dormant -or- Matted Grass'], size=(50, 1),
                  key='vriSeason',
                  background_color='white', enable_events=True, disabled=True)],
        [sg.T('')],
        [sg.T('Modelling Options:'),
         sg.Radio('Process Entire VRI Dataset', "radioProcessData", key='doAllData', default=True),
         sg.Radio('Process Unclassified Data Only', "radioProcessData", key='doNullData')],
        [sg.T('Number of Processors for Multiprocessing:'),
         sg.In('1', size=(10, 1), key='num_processors', background_color='white', enable_events=True)],
        [sg.Button('Model Fuel Types', disabled=True)],
        [sg.T('')],
        [sg.T('')],
        [sg.T('MODELLING PROGRESS', font=('Helvetica', 10), text_color='black'),
         sg.T('', key='featCountProg', font=('Helvetica', 10), text_color='black')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(60, 40), key='progBar'), sg.T('', key='progPcnt')]
    ]

    # Create the Window
    layout = [[sg.TabGroup([[sg.Tab('Model Fuel Type with Stand Data', standFuelType),
                             sg.Tab('Model Fuel Types for VRI Dataset', vriFuelType)]])],
              [sg.Button('Close Program')]]
    window = sg.Window('BC Wildfire Fuel Typing Tool', layout)

    # Event Loop to process "events" and get the "values" of the input
    while True:
        event, values = window.read()

        if event == 'advanced':
            if values['advanced']:
                window['BCLCS_LEVEL_1'].update(disabled=False)
                window['BCLCS_LEVEL_2'].update(disabled=False)
                window['INVENTORY_STANDARD_CD'].update(disabled=False)
                window['NON_VEG_COVER_TYPE_1'].update(disabled=False)
                window['LAND_COVER_CLASS_CD_1'].update(disabled=False)
            else:
                window['BCLCS_LEVEL_1'].update(value='V', disabled=True)
                window['BCLCS_LEVEL_2'].update(value='T', disabled=True)
                window['INVENTORY_STANDARD_CD'].update(disabled=True)
                window['NON_VEG_COVER_TYPE_1'].update(disabled=True)
                window['LAND_COVER_CLASS_CD_1'].update(disabled=True)

        if event == 'BCLCS_LEVEL_1':
            if values['BCLCS_LEVEL_1'] == 'V':
                window['BCLCS_LEVEL_2'].update(value='T', values=['T', 'N'])
            else:
                window['BCLCS_LEVEL_2'].update(value='L', values=['L', 'W', 'N'])

        if event == 'harvNo':
            window['HARVEST_DATE'].update('', disabled=True)
            window['harvCalendar'].update(disabled=True)

        if event == 'harvYes':
            window['HARVEST_DATE'].update(disabled=False)
            window['harvCalendar'].update(disabled=False)

        if event == 'distNo':
            window['EARLIEST_NONLOGGING_DIST_TYPE'].update('', disabled=True)
            window['EARLIEST_NONLOGGING_DIST_DATE'].update('', disabled=True)
            window['distCalendar'].update(disabled=True)

        if event == 'distYes':
            window['EARLIEST_NONLOGGING_DIST_TYPE'].update(disabled=False)
            window['EARLIEST_NONLOGGING_DIST_DATE'].update(disabled=False)
            window['distCalendar'].update(disabled=False)

        if event == 'CROWN_CLOSURE':
            if isNumber(values['CROWN_CLOSURE']) and values['CROWN_CLOSURE'] != '':
                if float(values['CROWN_CLOSURE']) <= 25:
                    window['BCLCS_LEVEL_5'].update('SP')
                elif float(values['CROWN_CLOSURE']) <= 60:
                    window['BCLCS_LEVEL_5'].update('OP')
                elif float(values['CROWN_CLOSURE']) <= 100:
                    window['BCLCS_LEVEL_5'].update('DE')
            else:
                window['BCLCS_LEVEL_5'].update('')

        if event == 'Model Fuel Type':
            inputError = valuesValid(values, treeList, becZones, becSubzones)
            if not inputError:
                if 'Growing' in values['standSeason']:
                    season = 'growing'
                else:
                    season = 'dormant'

                for i in fldList:
                    if (i in df.columns) and (i in values):
                        if (values[f'{i}'] != ''):
                            df[f'{i}'] = values[f'{i}']
                        else:
                            df[f'{i}'] = None

                    df[f'{i}'] = df[f'{i}'].astype(fldDTypes[f'{i}'].iloc[0])

                if values['HARVEST_DATE'] == '':
                    df['HARVEST_DATE'] = None

                if values['EARLIEST_NONLOGGING_DIST_DATE'] == '':
                    df['EARLIEST_NONLOGGING_DIST_DATE'] = None

                ftData = bcwft.getFuelType(season, *df.iloc[0][3:-1])

                if ftData is not None:
                    if ftData[2] is None:
                        window['ftOut'].update(ftData[1])
                    else:
                        window['ftOut'].update(f'{ftData[1]} ({ftData[2]}%)')
                else:
                    window['ftOut'].update('Not Found')

            else:
                print(f'INPUT ERROR:\n\n{inputError}')
                sg.popup(f'INPUT ERROR:\n\n{inputError}')

        if event == 'Reset Inputs':
            srchList = [i for i in values if i in fldList]
            for item in srchList:
                window[f'{item}'].update('')
            window['COAST_INTERIOR_CD'].update(value='I')
            window['BCLCS_LEVEL_1'].update(value='V')
            window['BCLCS_LEVEL_2'].update(value='T')
            window['standSeason'].update(value='Trees Growing -or- Standing Dead Grass')
            window['harvNo'].update(True)
            window['HARVEST_DATE'].update(disabled=True)
            window['harvCalendar'].update(disabled=True)
            window['distNo'].update(True)
            window['EARLIEST_NONLOGGING_DIST_TYPE'].update(disabled=True)
            window['EARLIEST_NONLOGGING_DIST_DATE'].update(disabled=True)
            window['distCalendar'].update(disabled=True)
            window['ftOut'].update('')

        if event == 'folderIn' or event == 'inVRI_Source':
            ftList = pf.listLayersInGDB(values['inVRI_Source'])

            if ftList is not None:
                window['inVRI'].update(values=ftList)
            else:
                window['inVRI'].update('')
                window['vriSeason'].update(disabled=True)
                window['Model Fuel Types'].update(disabled=True)

        if event == 'inVRI':
            if values['inVRI'] != '':
                window['vriSeason'].update(disabled=False)
            else:
                window['vriSeason'].update(disabled=True)

        if event == 'vriSeason':
            if 'Growing' in values['vriSeason']:
                season = 'growing'
            else:
                season = 'dormant'

            window['Model Fuel Types'].update(disabled=False)

        if event == 'Model Fuel Types':
            if not values['num_processors'] != '':
                try:
                    int(values['num_processors'])
                except Exception:
                    sg.popup('Number of Processors must be an integer value')
                if int(values['num_processors']) > mp.cpu_count:
                    window['inVRI'].update(f'{mp.cpu_count}')
            else:
                try:
                    # Start timer
                    start = time.time()

                    # Get the necessary input parameters
                    gdb_path = values['inVRI_Source']
                    feature_class = values['inVRI'][0]
                    output_feature_class = os.path.join(gdb_path, feature_class + '_FuelTypes')
                    output_gpkg = os.path.join(os.path.dirname(gdb_path), feature_class + '_FuelTypes.gpkg')
                    num_processors = int(values['num_processors'])

                    # Get the number of features in the VRI dataset
                    with fiona.open(fp=gdb_path, layer=feature_class) as src:
                        total_features = len(src)
                        schema = src.schema
                        columns = list(schema['properties'].keys())

                    if values['doAllData']:
                        process_all = True
                        valid_data = True
                        fields_to_extract = fldList[3:]
                    elif values['doNullData']:
                        if any(column in columns for column in fldList[:3]):
                            process_all = False
                            valid_data = True
                            fields_to_extract = fldList
                        else:
                            valid_data = False

                    if valid_data:
                        # Set up the feature slices for the dataset
                        slice_size = 5000
                        feature_slices = [slice(i, min(i + slice_size, total_features)) for i in
                                          range(0, total_features, slice_size)]

                        # Initialize the counter and lock
                        counter = mp.Manager().Value('i', 0)  # use Manager to create a shared counter
                        lock = mp.Manager().Lock()  # use Manager to create a shared lock

                        # Add input parameters to args
                        args = [(process_all, feature_slice, season, fields_to_extract + ['geometry'],
                                 gdb_path, feature_class, counter, lock)
                                for feature_slice in feature_slices]

                        print('Reading the VRI Dataset and Assigning Fuel Types')
                        with mp.Pool(num_processors) as pool:
                            result_async = pool.starmap_async(read_and_process_features, args)

                            # Periodically print the counter value while workers are running
                            while not result_async.ready():
                                time.sleep(1)  # Wait for 1 second between updates
                                BAR_MAX = total_features
                                REMAINING = total_features
                                # Track progress
                                PROGRESS = ((BAR_MAX - REMAINING) / BAR_MAX) + (counter.value / REMAINING)
                                window['featCountProg'].update(f'{REMAINING - counter.value} Features Remaining')
                                window['progBar'].update(PROGRESS)
                                window['progPcnt'].update(f'{round(100 * PROGRESS, 1)}%')

                            # Wait for all workers to complete
                            geo_dataframes = result_async.get()

                        merged_gdf = gpd.GeoDataFrame(pd.concat(geo_dataframes, ignore_index=True))

                        with fiona.open(gdb_path, layer=feature_class) as src:
                            crs = src.crs
                        merged_gdf.crs = crs

                        try:
                            merged_gdf.to_file(output_feature_class, driver='FileGDB')
                        except Exception:
                            merged_gdf.to_file(output_gpkg, driver='GPKG')

                        # DELETE TEMPORARY DATA
                        del BAR_MAX, REMAINING, PROGRESS

                        # End timer
                        end = time.time()
                        print(f'Fuel typing finished at: {datetime.now().strftime("%H:%M:%S")}')

                        # Print elapsed time
                        total_time = round((end - start) / 60, 3)
                        print(f'Fuel typing completed in: {total_time} minutes')
                        sg.popup(f'Fuel typing complete!\nFinished in: {total_time} minutes')
                    else:
                        sg.popup(f'None of the necessary Fuel Typing fields\n{fldList[:3]}\nare in the dataset.\n'
                                 'You must process the entire dataset.')
                        window['doAllData'].update(True)

                except Exception:
                    print(traceback.format_exc())

        if (event is None) or (event == 'Close Program'):  # if user closes window or clicks close program
            break

    # Close  the window
    window.close()


if __name__ == "__main__":
    main()
