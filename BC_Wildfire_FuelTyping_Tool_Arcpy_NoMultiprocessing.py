__author__ = ['Gregory A. Greene, map.n.trowel@gmail.com']

import PySimpleGUI as sg
import bcwft2018
import os
import pandas as pd
import numpy as np


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
landCoverClassCodeToolTip = '''The Land Cover Class Code describes the first most dominate land cover type by percent area
occupied within the polygon that contribute to the overall polygon description, but may be too small to be
spatially identified. The sub-division of a polygon by a quantified Land Cover Component, allowing non-
spatial resolution for modeling of wildlife habitat capability.

NON-VEGETATED:\t\tVEGETATED:\t\t\tWATER COVER:
SI = Snow/ice\t\t\tTB = Treed Broadleaf\t\tLA = Lake
GL = Glacier\t\t\tTC = Treed Coniferous\t\tRE = Reservoir
PN = Snow cover\t\t\tTM = Treed Mixed\t\tRI = River\stream
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
nonVegCoverTypeToolTip = '''Non-vegetated cover type is the designation for the predominate observable non-vegetated land cover
within the site. Non-vegetated cover types provide detailed reporting for non-vegetated land cover.

LAND COVER:\t\t\tWATER COVER:
GL = Glacier\t\t\tOT = Other
PN = Snow cover\t\t\tLA = Lake
BR = Bedrock\t\t\tRE = Reservoir
TA = Talus\t\t\tRI = River\stream
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


def csvToDF(inPath, inCols=None, header=None, asList=None):
    df = pd.read_csv(inPath, usecols=inCols, header=header)
    df = df.reindex(columns=inCols)

    if asList:
        return df.values.tolist()
    else:
        return df


def isNumber(s):
    try:
        float(f'{s}')
        return True
    except ValueError:
        return False


def valuesValid(inValues, treeList, becZones, becSubzones):
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


def main():
    # Remove stale tasks and set initial values for tool functions
    # sg.theme('DarkAmber')   # Add a touch of color if desired (other themes available)
    """
    refList = ['BCWFT_rowRef', 'FuelType','FT_Modifier','COAST_INTERIOR_CD','INVENTORY_STANDARD_CD',
               'BCLCS_LEVEL_1','BCLCS_LEVEL_2','BCLCS_LEVEL_3','BCLCS_LEVEL_4','BCLCS_LEVEL_5',
               'BEC_ZONE_CODE','BEC_SUBZONE',
               'EARLIEST_NONLOGGING_DIST_TYPE','EARLIEST_NONLOGGING_DIST_DATE','HARVEST_DATE',
               'CROWN_CLOSURE','PROJ_HEIGHT_1','PROJ_AGE_1','VRI_LIVE_STEMS_PER_HA','VRI_DEAD_STEMS_PER_HA',
               'STAND_PERCENTAGE_DEAD','NON_VEG_COVER_TYPE_1','NON_PRODUCTIVE_CD','LAND_COVER_CLASS_CD_1',
               'SPECIES_CD_1', 'SPECIES_PCT_1','SPECIES_CD_2', 'SPECIES_PCT_2','SPECIES_CD_3', 'SPECIES_PCT_3',
               'SPECIES_CD_4', 'SPECIES_PCT_4','SPECIES_CD_5', 'SPECIES_PCT_5','SPECIES_CD_6', 'SPECIES_PCT_6']
    """
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
                      sg.Combo(['B', 'IBM'], size=(4, 1), key='EARLIEST_NONLOGGING_DIST_TYPE', background_color='white',
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
         sg.Radio('Process Entire VRI Dataset', "radioProcessData", key='doAllData'),
         sg.Radio('Process Unclassified Data Only', "radioProcessData", key='doNullData', default=True)],
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
                    season = 'Growing'
                else:
                    season = 'Dormant'

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
            import arcpy
            from arcpy import env

            env.workspace = values['inVRI_Source']
            ftList = arcpy.ListFeatureClasses(feature_type='Polygon')

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
                season = 'Growing'
            else:
                season = 'Dormant'

            window['Model Fuel Types'].update(disabled=False)

        if event == 'Model Fuel Types':
            try:
                arcpy.Delete_management('in_memory')
                arcpy.ClearWorkspaceCache_management()

                print('Importing the VRI dataset')
                vri = 'in_memory\\vri'
                arcpy.MakeFeatureLayer_management(
                    os.path.join(values['inVRI_Source'], values['inVRI'][0]),
                    vri
                )
                fldLst = arcpy.ListFields(vri)

                # Add or reset BCWFT_rowRef field
                if 'BCWFT_rowRef' not in fldLst:
                    print('Adding "BCWFT_rowRef" field to VRI dataset')
                    arcpy.AddField_management(vri, 'BCWFT_rowRef', 'TEXT')
                elif values['doAllData']:
                    arcpy.CalculateField_management(vri, 'BCWFT_rowRef', None)

                # Add or reset FuelType field
                if 'FuelType' not in fldLst:
                    print('Adding "FuelType" field to VRI dataset')
                    arcpy.AddField_management(vri, 'FuelType', 'TEXT')
                elif values['doAllData']:
                    arcpy.CalculateField_management(vri, 'FuelType', None)

                # Add or reset FT_Modifier field
                if 'FT_Modifier' not in fldLst:
                    print('Adding "FT_Modifier" field to VRI dataset')
                    arcpy.AddField_management(vri, 'FT_Modifier', 'TEXT')
                elif values['doAllData']:
                    arcpy.CalculateField_management(vri, 'FT_Modifier', None)

                vriTableView = 'in_memory\\vriTableView'

                if arcpy.Exists(vriTableView):
                    print('Deleting old TableView of VRI dataset')
                    arcpy.Delete_management(vriTableView)

                print('Creating TableView of VRI dataset')
                arcpy.MakeTableView_management(vri, vriTableView)
                BAR_MAX = int(arcpy.GetCount_management(vriTableView).getOutput(0))

                if values['doNullData']:
                    print('Selecting features without Fuel Type assignments')
                    where_clause = """FuelType IS NULL"""
                    arcpy.SelectLayerByAttribute_management(vriTableView, 'NEW_SELECTION', where_clause)
                    REMAINING = int(arcpy.GetCount_management(vriTableView).getOutput(0))
                elif values['doAllData']:
                    REMAINING = BAR_MAX

                with arcpy.da.UpdateCursor(vriTableView, fldList) as cursor:
                    print('Assigning Fuel Types')
                    for count, row in enumerate(cursor):
                        fuelData = bcwft.getFuelType(season, row)
                        if fuelData is not None:
                            row[0], row[1], row[2] = fuelData
                        else:
                            row[0], row[1], row[2] = None, 'NoMatchingFuelType_ERROR', None
                        cursor.updateRow(row)
                        PROGRESS = ((BAR_MAX - REMAINING) / BAR_MAX) + (count / REMAINING)
                        window['featCountProg'].update(f'{REMAINING - count} Features Remaining')
                        window['progBar'].update(PROGRESS)
                        window['progPcnt'].update(f'{round(100 * PROGRESS, 1)}%')

                if values['doNullData']:
                    arcpy.SelectLayerByAttribute_management(vri, 'CLEAR_SELECTION')

                # DELETE TEMPORARY DATA
                del BAR_MAX, REMAINING, PROGRESS
                del count, vriTableView
                arcpy.Delete_management('in_memory')
                arcpy.ClearWorkspaceCache_management()
            except arcpy.ExecuteError:
                # Get the tool error messages
                msgs = arcpy.GetMessages(2)
                # Return tool error messages for use with a script tool
                arcpy.AddError(msgs)
            except:
                arcpy.Delete_management('in_memory')
                arcpy.ClearWorkspaceCache_management()

        if (event is None) or (event == 'Close Program'):  # if user closes window or clicks close program
            break

    # Close  the window
    window.close()


if __name__ == "__main__":
    main()