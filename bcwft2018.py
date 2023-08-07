__author__ = ['Gregory A. Greene, map.n.trowel@gmail.com']

import inspect
import pandas as pd
from datetime import datetime


class BCFuelType:
    def __init__(self):
        ## Instantiate Lists and Variables
        self.fldList = ['BCWFT_rowRef', 'FuelType', 'FT_Modifier', 'COAST_INTERIOR_CD', 'BCLCS_LEVEL_1',
                        'BCLCS_LEVEL_2', 'BCLCS_LEVEL_3', 'BCLCS_LEVEL_4', 'BCLCS_LEVEL_5',
                        'BEC_ZONE_CODE', 'BEC_SUBZONE', 'EARLIEST_NONLOGGING_DIST_TYPE',
                        'EARLIEST_NONLOGGING_DIST_DATE', 'HARVEST_DATE',
                        'CROWN_CLOSURE', 'PROJ_HEIGHT_1', 'PROJ_AGE_1', 'VRI_LIVE_STEMS_PER_HA',
                        'VRI_DEAD_STEMS_PER_HA', 'STAND_PERCENTAGE_DEAD',
                        'INVENTORY_STANDARD_CD', 'NON_PRODUCTIVE_CD', 'LAND_COVER_CLASS_CD_1',
                        'SPECIES_CD_1', 'SPECIES_PCT_1', 'SPECIES_CD_2', 'SPECIES_PCT_2',
                        'SPECIES_CD_3', 'SPECIES_PCT_3', 'SPECIES_CD_4', 'SPECIES_PCT_4',
                        'SPECIES_CD_5', 'SPECIES_PCT_5', 'SPECIES_CD_6', 'SPECIES_PCT_6']

        self.fldDTypes = ['object', 'object', 'object', 'object', 'object',
                          'object', 'object', 'object', 'object',
                          'object', 'object', 'object',
                          'datetime64[ns]', 'datetime64[ns]',
                          'float64', 'float64', 'float64', 'float64',
                          'float64', 'float64',
                          'object', 'object', 'object',
                          'object', 'float64', 'object', 'float64',
                          'object', 'float64', 'object', 'float64',
                          'object', 'float64', 'object', 'float64']

        self.treeList = ['', 'A', 'AC', 'ACB', 'ACT', 'AT', 'AX', 'B', 'BA', 'BB', 'BG', 'BL', 'BN', 'C', 'CW', 'D',
                         'DG', 'DM', 'DR', 'E', 'EA', 'EB', 'EP',
                         'ES', 'EW', 'EX', 'EXP', 'EXW', 'F', 'FD', 'FDC', 'FDI', 'G', 'GP', 'GR', 'H', 'HM', 'HW',
                         'HX', 'HXM', 'J', 'JD', 'JH', 'JR', 'LA',
                         'LS', 'LT', 'LW', 'M', 'MB', 'MR', 'MV', 'P', 'PA', 'PF', 'PJ', 'PL', 'PLC', 'PLI', 'PR', 'PW',
                         'PX', 'PXJ', 'PY', 'Q', 'QG', 'RA',
                         'S', 'SA', 'SB', 'SE', 'SS', 'SW', 'SX', 'SXB', 'SXE', 'SXL', 'SXS', 'SXW', 'SXX', 'T', 'TW',
                         'UP', 'V', 'VB', 'VP', 'VW', 'W', 'WA',
                         'WB', 'WD', 'S', 'WT', 'Y', 'YC']

        self.coniferList = ['C', 'CW',
                            'Y', 'YC',
                            'F', 'FD', 'FDC', 'FDI',
                            'B', 'BA', 'BG', 'BL',
                            'H', 'HM', 'HW', 'HXM',
                            'J', 'JR',
                            'P', 'PJ', 'PF', 'PL', 'PLI', 'PXJ', 'PY', 'PLC', 'PW', 'PA',
                            'S', 'SB', 'SE', 'SS', 'SW', 'SX', 'SXB', 'SXE', 'SXL', 'SXS', 'SXW', 'SXX',
                            'T', 'TW']

        self.becZones = ['BAFA', 'BG', 'BWBS', 'CDF', 'CMA', 'CWH', 'ESSF', 'ICH', 'IDF', 'IMA', 'MH', 'MS', 'PP',
                         'SBPS', 'SBS', 'SWB']

        self.becSubzones = ['dc', 'dcp', 'dcw', 'dh', 'dk', 'dkp', 'dkw', 'dm', 'ds', 'dv', 'dvp', 'dvw', 'dw', 'mc',
                            'mcp', 'mh', 'mk', 'mkp',
                            'mks', 'mm', 'mmp', 'mmw', 'ms', 'mv', 'mvp', 'mw', 'mwp', 'mww', 'un', 'unp', 'uns', 'vc',
                            'vcp', 'vcw', 'vh', 'vk',
                            'vks', 'vm', 'wc', 'wcp', 'wcw', 'wh', 'whp', 'wk', 'wm', 'wmp', 'wmw', 'ws', 'wv', 'wvp',
                            'ww', 'xc', 'xcp', 'xcw',
                            'xh', 'xk', 'xm', 'xv', 'xvp', 'xvw', 'xw', 'xx']

        self.dryBECzones = ['BG', 'PP', 'IDF', 'MS']  # LIST OF DRY BEC ZONES

        self.borealBECzonse = ['BBWS', 'SWB']  # LIST OF BOREAL BEC ZONES

    def isVegetated(self, inData):
        ## Function determines if inData is vegetated
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]
        # print(df) # FOR ERROR CHECKING

        if df.BCLCS_LEVEL_1 == 'V':
            return True
        elif df.BCLCS_LEVEL_1 == 'N':
            return False
        else:
            return None

    def isForested(self, inData):
        # Check if polygon is forested with >=10% crown closure
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]
        # print(df) # FOR ERROR CHECKING

        if df.BCLCS_LEVEL_2 == 'T':
            del df
            return True
        elif df.BCLCS_LEVEL_2 == 'N':
            del df
            return False
        else:
            del df
            return None

    def isLogged(self, inData):
        ## Determine if inData is logged
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]
        if df.HARVEST_DATE is not None:
            return True
        else:
            return False

    def getHarvLag(self, inData):
        ## Determine number of years since harvest
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]
        currentYear = datetime.now().year

        if df.HARVEST_DATE is not None:
            if df.HARVEST_DATE.year > currentYear:
                return 'HARVEST_DATE-ERROR', None
            else:
                harvLag = currentYear - pd.to_datetime(df.HARVEST_DATE, format='%Y-%m-%d').year
        else:
            harvLag = None

        #print(harvLag)
        del df, currentYear
        return harvLag

    def isBurned(self, inData):
        ## Determine if inData is burned
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]
        if df.EARLIEST_NONLOGGING_DIST_TYPE in ['B', 'BE', 'BG', 'BW', 'BR', 'NB']:
            del df
            return True
        else:
            del df
            return False

    def getDistLag(self, inData):
        ## Determine number of years since burn
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]
        currentYear = datetime.now().year

        if df.EARLIEST_NONLOGGING_DIST_DATE is not None:
            if df.EARLIEST_NONLOGGING_DIST_DATE.year > currentYear:
                return 'EARLIEST_NONLOGGING_DIST_DATE-ERROR', None
            else:
                distLag = currentYear - df.EARLIEST_NONLOGGING_DIST_DATE.year
        else:
            distLag = None

        del df, currentYear
        return distLag

    def getPrcntConifer(self, inData):
        # Create pandas DataFrame if inData isn't one
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]
        prcntCnfr = 0
        # If species code is a conifer, add its percentage to sum
        if (df.SPECIES_CD_1 is not None) and (df.SPECIES_PCT_1 is not None) and (df.SPECIES_CD_1 in self.coniferList):
            prcntCnfr += df.SPECIES_PCT_1
        if (df.SPECIES_CD_2 is not None) and (df.SPECIES_PCT_2 is not None) and (df.SPECIES_CD_2 in self.coniferList):
            prcntCnfr += df.SPECIES_PCT_2
        if (df.SPECIES_CD_3 is not None) and (df.SPECIES_PCT_3 is not None) and (df.SPECIES_CD_3 in self.coniferList):
            prcntCnfr += df.SPECIES_PCT_3
        if (df.SPECIES_CD_4 is not None) and (df.SPECIES_PCT_4 is not None) and (df.SPECIES_CD_4 in self.coniferList):
            prcntCnfr += df.SPECIES_PCT_4
        if (df.SPECIES_CD_5 is not None) and (df.SPECIES_PCT_5 is not None) and (df.SPECIES_CD_5 in self.coniferList):
            prcntCnfr += df.SPECIES_PCT_5
        if (df.SPECIES_CD_6 is not None) and (df.SPECIES_PCT_6 is not None) and (df.SPECIES_CD_6 in self.coniferList):
            prcntCnfr += df.SPECIES_PCT_6
        # Change prcntCnfr to 100% if it evaluates to >100%
        if prcntCnfr is not None and prcntCnfr > 100:
            prcntCnfr = 100
        # Remove temporary df
        del df
        # return percent conifer
        return prcntCnfr

    # Function to check if BEC subzone is dry or wet
    def getDryWet(self, inSubZone):
        # Create dry/wet dictionary
        dryWet = {
            'd': 'dry',
            'x': 'dry',
            'm': 'wet',
            'w': 'wet',
            'v': 'wet',
            'u': 'undifferentiated'}

        # Lookup first letter of subzone and return if dry or wet
        return dryWet.get(inSubZone[0], 'Invalid Subzone')

    def getStocking(self, inData):
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]

        liveStems = 0
        if df.VRI_LIVE_STEMS_PER_HA is not None:
            liveStems = df.VRI_LIVE_STEMS_PER_HA.sum()

        deadStems = 0
        if df.VRI_DEAD_STEMS_PER_HA is not None:
            deadStems = df.VRI_DEAD_STEMS_PER_HA.sum()

        return liveStems + deadStems

    #### CHECK IF SPECIES IN CHECKLIST ARE THE DOMINANT CONIFERS ON SITE
    def checkDomConifers(self, inData, checkList):
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]

        sppCdList = [df.SPECIES_CD_1, df.SPECIES_CD_2, df.SPECIES_CD_3,
                     df.SPECIES_CD_4, df.SPECIES_CD_5, df.SPECIES_CD_6]
        sppPrcntList = [df.SPECIES_PCT_1, df.SPECIES_PCT_2, df.SPECIES_PCT_3,
                        df.SPECIES_PCT_4, df.SPECIES_PCT_5, df.SPECIES_PCT_6]
        spDF = pd.DataFrame([sppPrcntList], columns=sppCdList).iloc[0]
        # print(sppCdList) # FOR ERROR CHECKING

        # GET LIST OF CONIFER SPECIES AT SITE IF THEY MATCH SPECIES IN CHECKLIST
        cnfrList = [i for i in sppCdList if i in checkList]
        if not cnfrList:
            cnfrPrcnt = 0  # ASSIGN AS 0 IF NO CONIFER SPECIES IN CHECKLIST FOUND AT SITE
        else:
            cnfrPrcnt = spDF[cnfrList][0]  # GET MAXIMUM PERCENTAGE OF CONIFERS IN CHECKLIST

        # GET LIST OF ALL OTHER CONIFERS AT SITE
        altCnfrList = [i for i in sppCdList if ((not i in checkList) and (i in self.coniferList))]
        if not altCnfrList:
            altCnfrPrcnt = 0  # ASSIGN AS 0 IF NO OTHER CONIFER SPECIES FOUND AT SITE
        else:
            altCnfrPrcnt = spDF[altCnfrList][0]  # GET MAXIMUM PERCENTAGE OF ALL OTHER CONIFERS

        # print(cnfrList) # FOR ERROR CHECKING
        # print(spDF[cnfrList][0]) # FOR ERROR CHECKING
        # print(sppCdList.index(cnfrList[0])) # FOR ERROR CHECKING
        # print(altCnfrList) # FOR ERROR CHECKING
        # print(spDF[altCnfrList][0]) # FOR ERROR CHECKING
        # print(sppPrcntList.index(altCnfrPrcnt)) # FOR ERROR CHECKING

        if cnfrPrcnt != 0 and cnfrPrcnt == altCnfrPrcnt:
            if sppCdList.index(cnfrList[0]) < sppCdList.index(altCnfrList[0]):
                return True
            else:
                return False
        elif cnfrPrcnt > altCnfrPrcnt:
            return True
        else:
            return False

    #### GET FUEL TYPE FOR INPUT DATA
    def getFuelType(self, season, inData):
        if isinstance(inData, pd.DataFrame):
            df = inData.iloc[0]
        else:
            df = pd.DataFrame([inData], columns=self.fldList).iloc[0]

        harvLag = self.getHarvLag(df)
        if isinstance(harvLag, tuple):
            return harvLag
        distLag = self.getDistLag(df)
        if isinstance(distLag, tuple):
            return distLag
        dryWet = self.getDryWet(df.BEC_SUBZONE)
        cnfrPrcnt = self.getPrcntConifer(inData)
        standStocking = self.getStocking(inData)

        #### NON-VEGETATED SITE
        if (not self.isVegetated(df)) or self.isVegetated(df) is None:
            #### SITE LOGGED
            if self.isLogged(df):
                #### SITE HARVESTED WITHIN LAST 6 YEARS
                if harvLag <= 6:
                    if df.COAST_INTERIOR_CD == 'C':
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                    else:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                #### SITE HARVESTED WITHIN LAST 7-24 YEARS
                elif harvLag <= 24:
                    if df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    else:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                #### SITE HARVESTED LONGER THAN 24 YEARS AGO
                else:
                    if df.BEC_ZONE_CODE in ['CMA', 'IMA']:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    elif df.BEC_ZONE_CODE in ['BAFA', 'MH']:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    elif df.BEC_ZONE_CODE in ['CWH', 'CDF', 'ICH'] and dryWet == 'wet':
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                    elif df.BEC_ZONE_CODE in ['BWBS']:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                    elif df.BEC_ZONE_CODE == 'SWB':
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 50
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 50
                    elif (df.BEC_ZONE_CODE == 'SBS') or (df.BEC_ZONE_CODE == 'IDF' and dryWet == 'wet') or (
                            df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry'):
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                    elif df.BEC_ZONE_CODE in ['SBPS', 'MS', 'ESSF'] or (
                            df.BEC_ZONE_CODE in ['IDF', 'CDF'] and dryWet == 'dry'):
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                    elif df.BEC_ZONE_CODE in ['PP', 'BG']:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                    elif df.BEC_ZONE_CODE == 'CWH' and dryWet == 'dry':
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
            #### SITE UNLOGGED
            else:
                #### SITE RECENTLY BURNED
                if self.isBurned(df) and (distLag is not None) and (distLag < 11):
                    if distLag <= 3:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    elif distLag <= 6:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    elif distLag <= 10:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                #### SITE NOT RECENTLY BURNED
                else:
                    if df.BCLCS_LEVEL_2 in ['L', None]:
                        if df.SPECIES_CD_1 is not None:
                            if df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    else:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None

        #### SITE VEGETATED
        elif self.isVegetated(df):
            #### SITE FORESTED
            if self.isForested(df):
                #### SITE RECENTLY BURNED
                if self.isBurned(df) and distLag is not None and distLag <= 10:
                    if cnfrPrcnt is not None and cnfrPrcnt >= 60:
                        if df.CROWN_CLOSURE is not None and df.CROWN_CLOSURE > 40:
                            if distLag <= 3:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            elif distLag <= 6:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:  # if distLag <= 10:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                        else:  # if df.CROWN_CLOSURE is None or df.CROWN_CLOSURE <= 40:
                            if distLag <= 1:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            elif distLag <= 6:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:  # if distLag <= 10:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                    else:
                        if distLag <= 1:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                        else:  # if distLag <= 10:
                            if season == 'Dormant':
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                            else:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                #### SITE NOT RECENTLY BURNED
                else:
                    if (df.SPECIES_CD_1 is None) or (df.SPECIES_PCT_1 is None) or (df.SPECIES_PCT_1 == 0):
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegForestNoBurn_Species-ERROR', None
                    #### PURE/SINGLE SPECIES STANDS
                    elif df.SPECIES_PCT_1 >= 80:
                        if df.SPECIES_CD_1 in self.coniferList:
                            #### PURE LODGEPOLE PINE STANDS
                            if df.SPECIES_CD_1 in ['PL', 'PLI', 'PLC', 'PJ', 'PXJ', 'P']:
                                if harvLag is not None and harvLag <= 7:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:
                                    if df.BCLCS_LEVEL_5 == 'SP':  #### SPARSE STANDS
                                        if (df.BEC_ZONE_CODE in ['CWH', 'CDF', 'MH']) or (
                                                df.BEC_ZONE_CODE in ['ICH'] and dryWet == 'wet'):
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  #### DENSE OR OPEN STANDS
                                        if df.PROJ_HEIGHT_1 < 4:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                        elif df.PROJ_HEIGHT_1 <= 12:
                                            if standStocking > 8000:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-4', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        elif df.PROJ_HEIGHT_1 > 12:
                                            if df.CROWN_CLOSURE < 40:
                                                if df.BEC_ZONE_CODE in ['BG', 'PP', 'IDF', 'MS']:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                                elif df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            else:
                                                if df.EARLIEST_NONLOGGING_DIST_TYPE == 'IBM':  #### MOUNTAIN PINE BEETLE STANDS
                                                    if distLag <= 5:
                                                        if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 50:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-3', 65
                                                        elif df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD >= 25:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                        else:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                    else:
                                                        if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 50:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                        elif df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD >= 25:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                        else:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                else:  #### NON MOUNTAIN PINE BEETLE STANDS
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                            #### PURE PONDEROSA PINE STANDS
                            elif df.SPECIES_CD_1 == 'PY':
                                if df.BCLCS_LEVEL_5 in ['DE', 'OP']:  #### DENSE OR OPEN STANDS
                                    if harvLag is not None and harvLag <= 10:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:
                                        if df.PROJ_HEIGHT_1 < 4:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                        elif df.PROJ_HEIGHT_1 <= 12:
                                            if standStocking > 8000:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-4', None
                                            elif standStocking >= 3000:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        elif df.PROJ_HEIGHT_1 <= 17:
                                            if df.BCLCS_LEVEL_5 == 'DE':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            elif df.BCLCS_LEVEL_5 == 'OP':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif df.BCLCS_LEVEL_5 == 'SP':  #### SPARSE STANDS
                                    if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD >= 40:
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                    else:
                                        if harvLag is not None and harvLag <= 10:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                            #### PURE OTHER PINE STANDS
                            elif df.SPECIES_CD_1 in ['PA', 'PF', 'PW']:
                                if df.BCLCS_LEVEL_5 == 'DE':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif df.BCLCS_LEVEL_5 in ['SP', 'OP']:
                                    if standStocking >= 900:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    elif standStocking >= 600:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE DOUGLAS-FIR STANDS
                            elif df.SPECIES_CD_1 in ['FD', 'FDC', 'FDI', 'F']:
                                #### SITE HARVESTED WITHIN LAST 6 YEARS
                                if harvLag is not None and harvLag <= 6:
                                    if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                            df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                    else:  # if (df.BEC_ZONE_CODE in self.dryBECzones) or (df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry'):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                #### SITE HARVESTED LONGER THAN 6 YEARS AGO
                                else:
                                    if df.PROJ_HEIGHT_1 is not None and df.PROJ_HEIGHT_1 < 4:
                                        if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                        else:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                    elif df.PROJ_HEIGHT_1 is not None and df.PROJ_HEIGHT_1 >= 4:
                                        if df.CROWN_CLOSURE is not None and df.CROWN_CLOSURE > 55:
                                            if df.PROJ_HEIGHT_1 <= 12:
                                                if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                else:  # if (df.BEC_ZONE_CODE in self.dryBECzones) or (df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry'):
                                                    if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 34:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-4', None
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            elif df.PROJ_HEIGHT_1 > 12:
                                                if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                else:  # if (df.BEC_ZONE_CODE in self.dryBECzones) or (df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry'):
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        elif df.CROWN_CLOSURE is None or df.CROWN_CLOSURE >= 26:
                                            if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                    df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                            else:  # if (df.COAST_INTERIOR_CD == 'I'):
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:  # if df.CROWN_CLOSURE < 26:
                                            if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                    df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                            else:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegForestNoBurnPureFd_ProjHeight-ERROR', None
                            #### PURE ENGELMANN SPRUCE STANDS
                            elif df.SPECIES_CD_1 == 'SE':
                                if harvLag is not None and harvLag <= 10:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:
                                    if df.BCLCS_LEVEL_5 == 'SP':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    elif df.BCLCS_LEVEL_5 == 'DE':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                    elif df.BCLCS_LEVEL_5 == 'OP':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                            #### PURE SITKA SPRUCE STANDS
                            elif df.SPECIES_CD_1 == 'SS':
                                if harvLag is not None and harvLag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                else:
                                    if df.BCLCS_LEVEL_5 == 'SP':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    elif df.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE BLACK OR WHITE SPRUCE STANDS
                            elif df.SPECIES_CD_1 in ['SB', 'SW']:
                                if harvLag is not None and harvLag <= 10:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:
                                    if df.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                    elif df.BCLCS_LEVEL_5 == 'SP':
                                        if df.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-1', None
                                        else:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 30
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 30
                            #### PURE SPRUCE (UNKNOWN OR HYBRID) STANDS
                            elif df.SPECIES_CD_1.startswith('S'):  # in ['SX','SXB','SXE','SXL','SXS','SXW','SXX','S']:
                                if harvLag is not None and harvLag <= 7:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:
                                    if df.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                        if df.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                        else:  # if df.BCLCS_LEVEL_5 == 'SP':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-1', None
                                    else:
                                        if df.BCLCS_LEVEL_5 == 'SP':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:  # if df.BCLCS_LEVEL_5 in ['DE','OP']:
                                            if df.BEC_ZONE_CODE in ['CWH', 'CDF']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                            else:  # if df.COAST_INTERIOR_CD == 'I' and df.SPECIES_CD_1 != 'SS':
                                                if df.PROJ_HEIGHT_1 < 4:
                                                    if season == 'Dormant':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                                elif df.PROJ_HEIGHT_1 >= 4:
                                                    if df.BCLCS_LEVEL_5 == 'OP':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                    elif df.BCLCS_LEVEL_5 == 'DE':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegForestPureOtherSpruceInterior_NoBCLCSLv5-ERROR', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegForestPureOtherSpruceInterior_ProjHeight-ERROR', None
                            #### PURE REDCEDAR, YELLOW CEDAR OR HEMLOCK STANDS
                            elif df.SPECIES_CD_1 in ['C', 'CW', 'Y', 'YC', 'H', 'HM', 'HW', 'HXM']:
                                if harvLag is not None and harvLag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                else:
                                    if df.BCLCS_LEVEL_5 == 'DE':
                                        if df.PROJ_HEIGHT_1 < 4:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                        elif df.PROJ_HEIGHT_1 <= 15:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        elif df.PROJ_HEIGHT_1 > 15:
                                            if df.PROJ_AGE_1 < 60:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            elif df.PROJ_AGE_1 <= 99:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 30
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 30
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    elif df.BCLCS_LEVEL_5 == 'OP':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    elif df.BCLCS_LEVEL_5 == 'SP':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            #### PURE TRUE FIR STANDS
                            elif df.SPECIES_CD_1.startswith('B'):
                                # print('Made it to pure true fir') # FOR ERROR CHECKING
                                if df.SPECIES_CD_1 == 'BG':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif df.SPECIES_CD_1 == 'BA':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 30
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 30
                                else:
                                    if df.BCLCS_LEVEL_5 == 'SP':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE YEW STANDS
                            elif df.SPECIES_CD_1 in ['T', 'TW']:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE JUNIPER STANDS
                            elif df.SPECIES_CD_1 in ['J', 'JR']:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            else:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegForestedPureSpeciesStand_Species-ERROR', None
                        else:  #### DECIDUOUS/BROADLEAF OR LARCH STAND
                            if season == 'Dormant':
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                            else:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                #### MIXED-SPECIES STANDS
                    elif df.SPECIES_PCT_1 < 80:
                        #### MIXED-SPECIES DECIDUOUS STANDS
                        if cnfrPrcnt <= 20:
                            if season == 'Dormant':
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                            else:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                        #### MIXED-SPECIES CONIFER OR MIXEDWOOD STANDS
                        elif cnfrPrcnt > 20:
                            #### 21-40% CONIFER = DECIDUOUS DOMINATED MIXEDWOOD STANDS
                            if cnfrPrcnt <= 40:
                                if harvLag is not None and harvLag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:  # harvLag > 6 or df.HARVEST_DATE is None:
                                    #### DOMINANT CONIFER = BLACK, WHITE, ENGELMANN, OR HYBRID SPRUCE
                                    if self.checkDomConifers(df,
                                                             ['SB', 'SW', 'SE', 'SX', 'SXB', 'SXE', 'SXL', 'SXS', 'SXW',
                                                              'SXX']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt
                                    #### DOMINANT CONIFER = UNKNOWN SPRUCE
                                    elif self.checkDomConifers(df, ['S']):
                                        if df.COAST_INTERIOR_CD == 'C':
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.5
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.5
                                        else:  # if df.COAST_INTERIOR_CD == 'I':
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt
                                    #### DOMINANT CONIFER = ANY OTHER CONIFER
                                    else:
                                        if df.BCLCS_LEVEL_5 == 'SP':
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.5
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.5
                                        else:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.7
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.7
                            #### 41-65% CONIFER = CONIFER_DOMINATED MIXEDWOOD STANDS
                            elif cnfrPrcnt <= 65:
                                if harvLag is not None and harvLag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:
                                    #### DOMINANT CONIFER = LODGEPOLE PINE
                                    if self.checkDomConifers(df, ['PL', 'PLI', 'PLC', 'PJ', 'PXJ', 'P']):
                                        if df.BCLCS_LEVEL_5 == 'SP':
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                        elif df.BCLCS_LEVEL_5 == 'OP':
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.7
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.7
                                        elif df.BCLCS_LEVEL_5 == 'DE':
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.8
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.8
                                    #### DOMINANT CONIFER = PONDEROSA PINE
                                    elif self.checkDomConifers(df, ['PY']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                    #### DOMINANT CONIFER = OTHER PINE
                                    elif self.checkDomConifers(df, ['PA', 'PF', 'PW']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.5
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.5
                                    #### DOMINANT CONIFER = DOUGLAS-FIR
                                    elif self.checkDomConifers(df, ['F', 'FD', 'FDC', 'FDI']):
                                        if df.BEC_ZONE_CODE in ['CWH', 'CDF', 'ICH']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.5
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.5
                                        else:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                    #### DOMINANT CONIFER = ENGELMANN SPRUCE
                                    elif self.checkDomConifers(df, ['SE']):
                                        if df.BCLCS_LEVEL_5 == 'SP':
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                        elif df.BCLCS_LEVEL_5 in ['OP', 'DE']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.9
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.9
                                    #### DOMINANT CONIFER = SITKA SPRUCE
                                    elif self.checkDomConifers(df, ['SS']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.4
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.4
                                    #### DOMINANT CONIFER = BLACK OR WHITE SPRUCE
                                    elif self.checkDomConifers(df, ['SB', 'SW']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt
                                    #### DOMINANT CONIFER = UNKNOWN OR HYBRID SPRUCE
                                    elif self.checkDomConifers(df,
                                                               ['SX', 'SXB', 'SXE', 'SXL', 'SXS', 'SXW', 'SXX', 'S']):
                                        if df.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                            if df.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt
                                            elif df.BCLCS_LEVEL_5 in ['SP']:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                        else:
                                            if df.BCLCS_LEVEL_5 in ['SP']:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                            elif df.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                if df.COAST_INTERIOR_CD == 'I':
                                                    if season == 'Dormant':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.8
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.8
                                                elif df.COAST_INTERIOR_CD == 'C':
                                                    if season == 'Dormant':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.5
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.5
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegForestMixedSpeciesCnfrLT65_BCLCSLv5-ERROR', None
                                    #### DOMINANT CONIFER = REDCEDAR, YELLOW CEDAR OR HEMLOCK
                                    elif self.checkDomConifers(df, ['C', 'CW', 'Y', 'YC', 'H', 'HM', 'HW', 'HXM']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.4
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.4
                                    #### DOMINANT CONIFER = FIR
                                    elif self.checkDomConifers(df, ['B', 'BA', 'BG', 'BL']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                    #### DOMINANT CONIFER = YEW
                                    elif self.checkDomConifers(df, ['T', 'TW']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = JUNIPER
                                    elif self.checkDomConifers(df, ['J', 'JR']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            #### 66-80% CONIFER = CONIFER_DOMINATED MIXEDWOOD STANDS
                            elif cnfrPrcnt <= 80:
                                if harvLag is not None and harvLag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:  # harvLag > 6 or df.HARVEST_DATE is None:
                                    #### DOMINANT CONIFER = LODGEPOLE PINE
                                    if self.checkDomConifers(df, ['PL', 'PLI', 'PLC', 'PJ', 'PXJ', 'P']):
                                        if df.BCLCS_LEVEL_5 in ['SP']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.5
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.5
                                        elif df.BCLCS_LEVEL_5 in ['OP']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.7
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.7
                                        elif df.BCLCS_LEVEL_5 in ['DE']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.8
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.8
                                    #### DOMINANT CONIFER = PONDEROSA PINE
                                    elif self.checkDomConifers(df, ['PY']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    #### DOMINANT CONIFER = OTHER PINE
                                    elif self.checkDomConifers(df, ['PA', 'PF', 'PW']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = DOUGLAS-FIR
                                    elif self.checkDomConifers(df, ['F', 'FD', 'FDC', 'FDI']):
                                        if (df.BEC_ZONE_CODE in ['CWH', 'CDF']) or (
                                                df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                        else:
                                            if df.BCLCS_LEVEL_5 in ['DE']:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.7
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.7
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    #### DOMINANT CONIFER = ENGELMANN SPRUCE
                                    elif self.checkDomConifers(df, ['SE']):
                                        if df.BCLCS_LEVEL_5 in ['SP']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                        elif df.BCLCS_LEVEL_5 in ['OP', 'DE']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.7
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.7
                                    #### DOMINANT CONIFER = SITKA SPRUCE
                                    elif self.checkDomConifers(df, ['SS']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = BLACK OR WHITE SPRUCE
                                    elif self.checkDomConifers(df, ['SB', 'SW']):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt
                                    #### DOMINANT CONIFER = UNKNOWN OR HYBRID SPRUCE
                                    elif self.checkDomConifers(df,
                                                               ['SX', 'SXB', 'SXE', 'SXL', 'SXS', 'SXW', 'SXX', 'S']):
                                        if df.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                            if df.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt
                                            if df.BCLCS_LEVEL_5 in ['SP']:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                        else:
                                            if df.BCLCS_LEVEL_5 in ['SP']:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.6
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.6
                                            else:  # df.BCLCS_LEVEL_5 in ['DE','OP']:
                                                if df.COAST_INTERIOR_CD == 'I':
                                                    if season == 'Dormant':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', cnfrPrcnt * 0.8
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', cnfrPrcnt * 0.8
                                                else:  # df.COAST_INTERIOR_CD == 'C':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = REDCEDAR, YELLOW CEDAR OR HEMLOCK
                                    elif self.checkDomConifers(df, ['C', 'CW', 'Y', 'YC', 'H', 'HM', 'HW', 'HXM']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = FIR
                                    elif self.checkDomConifers(df, ['B', 'BA', 'BG', 'BL']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    #### DOMINANT CONIFER = YEW
                                    elif self.checkDomConifers(df, ['T', 'TW']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = JUNIPER
                                    elif self.checkDomConifers(df, ['J', 'JR']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                            #### 81-100% CONIFER = PURE CONIFER, MIXED-SPECIES STANDS
                            elif cnfrPrcnt <= 100:
                                #### DOMINANT CONIFER = LODGEPONE PINE
                                if df.SPECIES_CD_1 in ['P', 'PL', 'PLI', 'PLC', 'PJ', 'PXJ']:
                                    if harvLag is not None and harvLag <= 7:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:
                                        if df.BCLCS_LEVEL_5 in ['SP']:
                                            if (df.BEC_ZONE_CODE in ['CWH', 'CDF', 'MH']) or (
                                                    df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:  # if df.BCLCS_LEVEL_5 in ['DE','OP']:
                                            if df.PROJ_HEIGHT_1 < 4:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                            elif df.PROJ_HEIGHT_1 >= 4:
                                                if df.SPECIES_CD_2.startswith('S') or df.SPECIES_CD_2.startswith('B'):
                                                    if df.PROJ_HEIGHT_1 <= 12:
                                                        if standStocking > 8000:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-4', None
                                                        else:  # standStocking <= 8000 or (df.VRI_LIVE_STEMS_PER_HA is None and df.VRI_DEAD_STEMS_PER_HA is None):
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                    else:  # df.PROJ_HEIGHT_1 > 12:
                                                        if df.CROWN_CLOSURE < 40:
                                                            if df.BEC_ZONE_CODE in ['BG', 'PP', 'IDF', 'MS']:
                                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                                            elif df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                            else:
                                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                        else:  # df.CROWN_CLOSURE >= 40 or df.CROWN_CLOSURE is None:
                                                            if df.EARLIEST_NONLOGGING_DIST_TYPE == 'IBM':
                                                                if distLag <= 5:
                                                                    if df.BCLCS_LEVEL_5 in ['DE']:
                                                                        if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-3', 65
                                                                        elif df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                                        else:  # df.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                                    else:  # df.BCLCS_LEVEL_5 in ['OP']:
                                                                        if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-3', 65
                                                                        elif df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                                        else:  # df.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                                else:  # distLag > 5:
                                                                    if df.BCLCS_LEVEL_5 in ['DE']:
                                                                        if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                                        elif df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                                        else:  # df.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                                    else:  # df.BCLCS_LEVEL_5 in ['OP']:
                                                                        if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                                        elif df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                                        else:  # df.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                            else:
                                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                else:
                                                    if df.CROWN_CLOSURE < 40:
                                                        if df.BEC_ZONE_CODE in ['IDF', 'PP', 'BG', 'SBPS', 'MS']:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                                        elif df.BEC_ZONE_CODE in ['CWH', 'CDF', 'ICH']:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                        else:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                    else:  # df.CROWN_CLOSURE >= 40:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                #### DOMINANT CONIFER = PONDEROSA PINE
                                elif df.SPECIES_CD_1 in ['PY']:
                                    if harvLag is not None and harvLag <= 7:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:  # harvLag > 7:
                                        if df.PROJ_HEIGHT_1 < 4:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                        else:  # df.PROJ_HEIGHT_1 >= 4:
                                            if df.BCLCS_LEVEL_5 in ['DE']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            else:  # df.BCLCS_LEVEL_5 in ['OP','SP']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                #### DOMINANT CONIFER = OTHER PINE
                                elif df.SPECIES_CD_1 in ['PA', 'PF', 'PW']:
                                    if df.BCLCS_LEVEL_5 in ['DE']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    else:  # df.BCLCS_LEVEL_5 in ['OP','SP']:
                                        if standStocking >= 900:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        elif standStocking >= 600:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                #### DOMINANT CONIFER = DOUGLAS-FIR
                                elif df.SPECIES_CD_1.startswith('F'):
                                    if harvLag is not None and harvLag <= 6:
                                        if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                        else:  # if (df.BEC_ZONE_CODE in self.dryBECzones) or (df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:  # harvLag > 6:
                                        if df.PROJ_HEIGHT_1 < 4:
                                            if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                    df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                            else:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                        else:  # df.PROJ_HEIGHT_1 >= 4:
                                            if df.CROWN_CLOSURE > 55:
                                                if df.PROJ_HEIGHT_1 <= 12:
                                                    if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                            df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                    else:  # if (df.BEC_ZONE_CODE in self.dryBECzones) or (df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry'):
                                                        if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 34:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-4', None
                                                        else:
                                                            if df.SPECIES_CD_2 == 'PY':
                                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                                            else:
                                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                elif df.PROJ_HEIGHT_1 > 12:
                                                    if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                            df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                    else:  # (df.BEC_ZONE_CODE in self.dryBECzones) or (df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry'):
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                            elif df.CROWN_CLOSURE >= 26 or df.CROWN_CLOSURE is None:
                                                if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                else:  # df.COAST_INTERIOR_CD = 'I' and ((df.BEC_ZONE_CODE in self.dryBECzones) or (df.BEC_ZONE_CODE == 'ICH' and dryWet == 'dry')):
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                            else:
                                                if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                                    if season == 'Dormant':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                                else:
                                                    if season == 'Dormant':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                #### DOMINANT CONIFER = SPRUCE
                                elif df.SPECIES_CD_1.startswith('S'):
                                    if harvLag is not None and harvLag <= 6:
                                        if (df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                        else:  # (df.COAST_INTERIOR_CD = 'I') or (df.BEC_ZONE_CODE in self.dryBECzones):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                    else:  # (harvLag > 6):
                                        if df.SPECIES_CD_1 == 'SE':
                                            if df.BCLCS_LEVEL_5 in ['SP']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                            else:  # df.BCLCS_LEVEL_5 in ['DE','OP']:
                                                if df.SPECIES_CD_2 in ['BL', 'B', 'PL', 'P', 'PLI']:
                                                    if df.BCLCS_LEVEL_5 in ['DE']:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                    else:  # df.BCLCS_LEVEL_5 in ['OP']:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                elif df.SPECIES_CD_2 in ['HW', 'HM', 'CW', 'YC']:
                                                    if df.BCLCS_LEVEL_5 in ['DE']:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                    else:  # df.BCLCS_LEVEL_5 in ['OP']:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        elif df.SPECIES_CD_1 in ['SS']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                        elif df.SPECIES_CD_1 in ['SB']:
                                            if df.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                            else:  # df.BCLCS_LEVEL_5 in ['SP']:
                                                if df.BEC_ZONE_CODE in ['BWBS']:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-1', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        else:  # if df.SPECIES_CD_1 in ['SX','SXB','SXE','SXL','SXS','SXW','SXX','SW','S']:
                                            if df.BEC_ZONE_CODE in ['BWBS']:
                                                if df.BCLCS_LEVEL_5 in ['DE']:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                elif df.BCLCS_LEVEL_5 in ['OP']:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                else:  # df.BCLCS_LEVEL_5 in ['SP']:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-1', None
                                            else:
                                                if df.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']:
                                                    if (df.SPECIES_CD_2 in ['BL', 'B']) or df.SPECIES_CD_2.startswith('P'):
                                                        if df.BCLCS_LEVEL_5 in ['SP']:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                                        else:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                                else:  # (df.COAST_INTERIOR_CD = 'I') and (not df.BEC_ZONE_CODE in self.borealBECzones):
                                                    if df.BCLCS_LEVEL_5 in ['SP']:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                                    else:
                                                        if df.BCLCS_LEVEL_5 in ['DE']:
                                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                        else:  # df.BCLCS_LEVEL_5 in ['OP']:
                                                            if df.STAND_PERCENTAGE_DEAD is not None and df.STAND_PERCENTAGE_DEAD > 34:
                                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                            else:  # (df.STAND_PERCENTAGE_DEAD <= 34) or (df.STAND_PERCENTAGE_DEAD is None):
                                                                if (df.SPECIES_CD_2 in ['PL', 'PLI', 'P']):
                                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                                                else:
                                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                ##### DOMINANT CONIFER = REDCEDAR, YELLOW CEDAR OR HEMLOCK
                                elif df.SPECIES_CD_1.startswith('C') or df.SPECIES_CD_1.startswith('Y') or df.SPECIES_CD_1.startswith('H'):
                                    if harvLag is not None and harvLag <= 6:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                    else:  # harvLag > 6:
                                        if df.BCLCS_LEVEL_5 == 'DE':
                                            if df.PROJ_HEIGHT_1 < 4:
                                                if season == 'Dormant':
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                            elif df.PROJ_HEIGHT_1 <= 15:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            else:  # (df.PROJ_HEIGHT_1 > 15) and (df.BCLCS_LEVEL_5 in ['DE']):
                                                if df.PROJ_AGE_1 < 60:
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                                elif df.PROJ_AGE_1 <= 99:
                                                    if season == 'Dormant':
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                                    else:
                                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                                else:  # (df.PROJ_AGE_1 > 99) or (df.BCLCS_LEVEL_5 in ['DE']) or (df.BCLCS_LEVEL_5 is None):
                                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                        elif df.BCLCS_LEVEL_5 in ['OP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                        else:  # df.BCLCS_LEVEL_5 in ['SP']:
                                            if season == 'Dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                ##### DOMINANT CONIFER = GRAND FIR
                                elif df.SPECIES_CD_1 in ['BG']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                ##### DOMINANT CONIFER = AMABALIS FIR
                                elif df.SPECIES_CD_1 in ['BA']:
                                    if df.SPECIES_CD_2 in ['SE', 'SW', 'S']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    else:
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                ##### DOMINANT CONIFER = OTHER FIR
                                elif df.SPECIES_CD_1 in ['B', 'BL']:
                                    if df.COAST_INTERIOR_CD == 'C':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # df.COAST_INTERIOR_CD == 'I':
                                        if df.BCLCS_LEVEL_5 in ['SP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        elif df.BCLCS_LEVEL_5 in ['DE']:
                                            if df.SPECIES_CD_2 in ['SE', 'SW', 'S']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        else:  # df.BCLCS_LEVEL_5 in ['OP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                ##### DOMINANT CONIFER = YEW
                                elif df.SPECIES_CD_1 in ['T', 'TW']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                ##### DOMINANT CONIFER = JUNIPER
                                elif df.SPECIES_CD_1 in ['J', 'JR']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None

            #### NON-FORESTED SITE
            else:
                #### SITE RECENTLY BURNED
                if self.isBurned(df) and distLag is not None and distLag < 11:
                    if distLag <= 1:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    elif distLag <= 3:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    else:  # distLag <= 10:
                        if season == 'Dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                #### SITE NOT RECENTLY BURNED
                else:
                    #### SITE LOGGED
                    if self.isLogged(df):
                        if df.SPECIES_CD_1 is not None:
                            if harvLag <= 7:
                                if str(df.SPECIES_CD_1).startswith('P'):
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                elif str(df.SPECIES_CD_1).startswith('S') or str(df.SPECIES_CD_1).startswith('B'):
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                elif (df.SPECIES_CD_1 in ['CW', 'YC']) or str(df.SPECIES_CD_1).startswith('H'):
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                elif str(df.SPECIES_CD_1).startswith('FD'):
                                    if df.BEC_ZONE_CODE in ['CWH', 'ICH']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                            elif harvLag <= 24:
                                if (df.BEC_ZONE_CODE in ['CWH', 'MH']) or (
                                        df.BEC_ZONE_CODE == 'ICH' and dryWet == 'wet'):
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                else:  # (df.BEC_ZONE_CODE in self.dryBECzones) or (dryWet == 'dry'):
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            else:  # if harvLag > 24:
                                if df.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                elif df.BEC_ZONE_CODE == 'BAFA':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif df.BEC_ZONE_CODE == 'CWH':
                                    if dryWet == 'dry':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # dryWet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif df.BEC_ZONE_CODE == 'BWBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                elif df.BEC_ZONE_CODE == 'SWB':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 50
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 50
                                elif df.BEC_ZONE_CODE == 'SBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif df.BEC_ZONE_CODE == 'SBPS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif df.BEC_ZONE_CODE == 'MS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif df.BEC_ZONE_CODE == 'IDF':
                                    if dryWet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # dryWet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif df.BEC_ZONE_CODE == 'PP':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif df.BEC_ZONE_CODE == 'BG':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif df.BEC_ZONE_CODE == 'MH':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif df.BEC_ZONE_CODE == 'ESSF':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif df.BEC_ZONE_CODE == 'CDF':
                                    if dryWet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # dryWet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif df.BEC_ZONE_CODE == 'ICH':
                                    if dryWet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    else:  # dryWet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegNonForestUnburnedLoggedGT24HasSpecies_BEC-ERROR', None
                        else:  # if df.SPECIES_CD_1 is None:
                            if harvLag <= 5:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                            elif harvLag <= 24:
                                if df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                else:  # (df.BEC_ZONE_CODE in self.dryBECzones) or (dryWet == 'dry'):
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            else:  # harvLag > 24:
                                if df.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                elif df.BEC_ZONE_CODE == 'BAFA':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif df.BEC_ZONE_CODE == 'CWH':
                                    if dryWet == 'dry':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # dryWet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif df.BEC_ZONE_CODE == 'BWBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                elif df.BEC_ZONE_CODE == 'SWB':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 25
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 25
                                elif df.BEC_ZONE_CODE == 'SBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif df.BEC_ZONE_CODE == 'SBPS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif df.BEC_ZONE_CODE == 'MS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif df.BEC_ZONE_CODE == 'IDF':
                                    if dryWet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # dryWet == 'wet':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 50
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 50
                                elif df.BEC_ZONE_CODE == 'PP':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif df.BEC_ZONE_CODE == 'BG':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif df.BEC_ZONE_CODE == 'MH':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif df.BEC_ZONE_CODE == 'ESSF':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif df.BEC_ZONE_CODE == 'CDF':
                                    if dryWet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # dryWet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif df.BEC_ZONE_CODE == 'ICH':
                                    if dryWet == 'dry':
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # dryWet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'VegNonForestUnburnedLoggedGT24NoSpecies_BEC-ERROR', None
                    #### SITE NOT LOGGED
                    else:  # not isLogged(df):
                        if df.SPECIES_CD_1 is not None:
                            if df.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            elif df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH', 'BAFA']:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:
                                if season == 'Dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                        else:
                            if df.INVENTORY_STANDARD_CD == 'F':
                                if df.NON_PRODUCTIVE_CD in [11, 12, 13]:
                                    if df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    else:  # (df.BEC_ZONE_CODE in self.dryBECzones) or (dryWet == 'dry'):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif df.NON_PRODUCTIVE_CD == 35:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'W', None
                                elif df.NON_PRODUCTIVE_CD == 42:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                elif df.NON_PRODUCTIVE_CD in [60, 62, 63]:
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif df.NON_PRODUCTIVE_CD is None:
                                    if df.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                    elif df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    else:  # (df.BEC_ZONE_CODE in self.dryBECzones) or (dryWet == 'dry'):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            else:  # df.INVENTORY_STANDARD_CD in ['V','I','L']:
                                if df.LAND_COVER_CLASS_CD_1 in ['LA', 'RE', 'RI', 'OC']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'W', None
                                elif df.LAND_COVER_CLASS_CD_1 == 'HG':
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif df.LAND_COVER_CLASS_CD_1 in ['BY', 'BM', 'BL']:
                                    if season == 'Dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif df.LAND_COVER_CLASS_CD_1 in ['SL', 'ST', 'HE', 'HF', None]:
                                    if df.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                    elif df.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    else:  # (df.BEC_ZONE_CODE in self.dryBECzones) or (dryWet == 'dry'):
                                        if season == 'Dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
