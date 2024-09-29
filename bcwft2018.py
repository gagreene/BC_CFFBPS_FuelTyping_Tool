# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:15:00 2022

@author: Gregory A. Greene
"""
__author__ = ['Gregory A. Greene, map.n.trowel@gmail.com']

import inspect
import pandas as pd
from numpy import nan, datetime64
from datetime import datetime as dt


class FuelTyping:
    """
    Class for the BC Wildfire Fuel Typing Algorithm
    """
    def __init__(self):
        # Instantiate VRI Variables
        self.COAST_INTERIOR_CD = None
        self.BCLCS_LEVEL_1 = None
        self.BCLCS_LEVEL_2 = None
        self.BCLCS_LEVEL_3 = None
        self.BCLCS_LEVEL_4 = None
        self.BCLCS_LEVEL_5 = None
        self.BEC_ZONE_CODE = None
        self.BEC_SUBZONE = None
        self.EARLIEST_NONLOGGING_DIST_TYPE = None
        self.EARLIEST_NONLOGGING_DIST_DATE = None
        self.HARVEST_DATE = None
        self.CROWN_CLOSURE = None
        self.PROJ_HEIGHT_1 = None
        self.PROJ_AGE_1 = None
        self.VRI_LIVE_STEMS_PER_HA = None
        self.VRI_DEAD_STEMS_PER_HA = None
        self.STAND_PERCENTAGE_DEAD = None
        self.INVENTORY_STANDARD_CD = None
        self.NON_PRODUCTIVE_CD = None
        self.LAND_COVER_CLASS_CD_1 = None
        self.SPECIES_CD_1 = None
        self.SPECIES_PCT_1 = None
        self.SPECIES_CD_2 = None
        self.SPECIES_PCT_2 = None
        self.SPECIES_CD_3 = None
        self.SPECIES_PCT_3 = None
        self.SPECIES_CD_4 = None
        self.SPECIES_PCT_4 = None
        self.SPECIES_CD_5 = None
        self.SPECIES_PCT_5 = None
        self.SPECIES_CD_6 = None
        self.SPECIES_PCT_6 = None

        # Instantiate bcwft variables
        self.season = None
        self.is_vegetated = None
        self.is_forested = None
        self.is_logged = None
        self.is_burned = None
        self.harv_lag = None
        self.dist_lag = None
        self.pct_cnfr = None
        self.dry_wet = None
        self.stocking = None

        ## Instantiate Lists
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

    def verifyInputs(self):
        if not isinstance(self.season, str):
            raise TypeError('The "season" parameter must be string data type.')
        elif self.season not in ['growing', 'dormant']:
            raise ValueError('The "season" parameter must be either "growing" or "dormant".')
        if not isinstance(self.COAST_INTERIOR_CD, (str, type(None))):
            raise TypeError('The "COAST_INTERIOR_CD" parameter must be string data type.')
        if not isinstance(self.BCLCS_LEVEL_1, (str, type(None), type(nan))):
            raise TypeError('The "BCLCS_LEVEL_1" parameter must be string data type.')
        if not isinstance(self.BCLCS_LEVEL_2, (str, type(None), type(nan))):
            raise TypeError('The "BCLCS_LEVEL_2" parameter must be string data type.')
        if not isinstance(self.BCLCS_LEVEL_3, (str, type(None), type(nan))):
            raise TypeError('The "BCLCS_LEVEL_3" parameter must be string data type.')
        if not isinstance(self.BCLCS_LEVEL_4, (str, type(None), type(nan))):
            raise TypeError('The "BCLCS_LEVEL_4" parameter must be string data type.')
        if not isinstance(self.BCLCS_LEVEL_5, (str, type(None), type(nan))):
            raise TypeError('The "BCLCS_LEVEL_5" parameter must be string data type.')
        if not isinstance(self.BEC_ZONE_CODE, str):
            raise TypeError('The "BEC_ZONE_CODE" parameter must be string data type.')
        if not isinstance(self.BEC_SUBZONE, str):
            raise TypeError('The "BEC_SUBZONE" parameter must be string data type.')
        if not isinstance(self.EARLIEST_NONLOGGING_DIST_TYPE, (str, type(None))):
            raise TypeError('The "EARLIEST_NONLOGGING_DIST_TYPE" parameter must be string data type.')
        if not isinstance(self.EARLIEST_NONLOGGING_DIST_DATE, (dt, type(None))):
            raise TypeError('The "EARLIEST_NONLOGGING_DIST_DATE" parameter must be datetime data type.')
        if not isinstance(self.HARVEST_DATE, (dt, type(None))):
            raise TypeError('The "HARVEST_DATE" parameter must be datetime data type.')
        if not isinstance(self.CROWN_CLOSURE, (int, float, type(None))):
            raise TypeError('The "CROWN_CLOSURE" parameter must be int or float data type.')
        if not isinstance(self.PROJ_HEIGHT_1, (float, type(None))):
            raise TypeError('The "PROJ_HEIGHT_1" parameter must be float data type.')
        if not isinstance(self.PROJ_AGE_1, (int, float, type(None))):
            raise TypeError('The "PROJ_AGE_1" parameter must be int or float data type.')
        if not isinstance(self.VRI_LIVE_STEMS_PER_HA, (int, float, type(None))):
            raise TypeError('The "VRI_LIVE_STEMS_PER_HA" parameter must be int or float data type.')
        if not isinstance(self.VRI_DEAD_STEMS_PER_HA, (int, float, type(None))):
            raise TypeError('The "VRI_DEAD_STEMS_PER_HA" parameter must be int or float data type.')
        if not isinstance(self.STAND_PERCENTAGE_DEAD, (int, float, type(None))):
            raise TypeError('The "STAND_PERCENTAGE_DEAD" parameter must be int or float data type.')
        if not isinstance(self.INVENTORY_STANDARD_CD, (str, type(None), type(nan))):
            raise TypeError('The "INVENTORY_STANDARD_CD" parameter must be string data type.')
        if not isinstance(self.NON_PRODUCTIVE_CD, (str, type(None), type(nan))):
            raise TypeError('The "NON_PRODUCTIVE_CD" parameter must be string data type.')
        if not isinstance(self.LAND_COVER_CLASS_CD_1, (str, type(None), type(nan))):
            raise TypeError('The "LAND_COVER_CLASS_CD_1" parameter must be string data type.')
        if not isinstance(self.SPECIES_CD_1, (str, type(None))):
            raise TypeError('The "SPECIES_CD_1" parameter must be a string data type.')
        if not isinstance(self.SPECIES_PCT_1, (int, float, type(None))):
            raise TypeError('The "SPECIES_PCT_1" parameter must be int or float data type.')
        if not isinstance(self.SPECIES_CD_2, (str, type(None))):
            raise TypeError('The "SPECIES_CD_2" parameter must be a string data type.')
        if not isinstance(self.SPECIES_PCT_2, (int, float, type(None))):
            raise TypeError('The "SPECIES_PCT_2" parameter must be int or float data type.')
        if not isinstance(self.SPECIES_CD_3, (str, type(None))):
            raise TypeError('The "SPECIES_CD_3" parameter must be string data type.')
        if not isinstance(self.SPECIES_PCT_3, (int, float, type(None))):
            raise TypeError('The "SPECIES_PCT_3" parameter must be int or float data type.')
        if not isinstance(self.SPECIES_CD_4, (str, type(None))):
            raise TypeError('The "SPECIES_CD_4" parameter must be string data type.')
        if not isinstance(self.SPECIES_PCT_4, (int, float, (type(None)))):
            raise TypeError('The "SPECIES_PCT_4" parameter must be int or float data type.')
        if not isinstance(self.SPECIES_CD_5, (str, (type(None)))):
            raise TypeError('The "SPECIES_CD_5" parameter must be string data type.')
        if not isinstance(self.SPECIES_PCT_5, (int, float, type(None))):
            raise TypeError('The "SPECIES_PCT_5" parameter must be int or float data type.')
        if not isinstance(self.SPECIES_CD_6, (str, type(None))):
            raise TypeError('The "SPECIES_CD_6" parameter must be string data type.')
        if not isinstance(self.SPECIES_PCT_6, (int, float, type(None))):
            raise TypeError('The "SPECIES_PCT_6" parameter must be int or float data type.')

        return

    def isVegetated(self) -> None:
        """
        Function to check if the area is vegetated.
        :return: None
        """
        if self.BCLCS_LEVEL_1 == 'V':
            self.is_vegetated = True
        elif self.BCLCS_LEVEL_1 == 'N':
            self.is_vegetated = False
        else:
            self.is_vegetated = None
        return

    def isForested(self) -> None:
        """
        Function to check if area is forested (has >=10% crown closure).
        :return: None
        """
        if self.BCLCS_LEVEL_2 == 'T':
            self.is_forested = True
        elif self.BCLCS_LEVEL_2 == 'N':
            self.is_forested = False
        else:
            self.is_forested = None
        return

    def isLogged(self) -> None:
        """
        Function to check if the area is logged.
        :return: None
        """
        if self.HARVEST_DATE is not None:
            self.is_logged = True
        else:
            self.is_logged = False
        return

    def isBurned(self) -> None:
        """
        Function to check if the area has been burned.
        :return: None
        """
        ## Determine if the polygon is burned
        if self.EARLIEST_NONLOGGING_DIST_TYPE in ['B', 'BE', 'BG', 'BW', 'BR', 'NB']:
            self.is_burned = True
        else:
            self.is_burned = False
        return

    def getHarvLag(self) -> None:
        """
        Function to get the number of years since the area was harvested.
        :return: None
        """
        # Get the current year
        currentYear = dt.now().year
        if self.HARVEST_DATE is not None:
            if self.HARVEST_DATE.year > currentYear:
                self.harv_lag = 'HARVEST_DATE-ERROR', None
            else:
                # Calculate difference between harvest date and current year
                self.harv_lag = currentYear - pd.to_datetime(self.HARVEST_DATE, format='%Y-%m-%d').year
        else:
            self.harv_lag = None
        del currentYear

        return

    def getDistLag(self) -> None:
        """
        Function to get the number of years since the area was last disturbed (non harvest).
        :return: None
        """
        ## Determine number of years since burn
        currentYear = dt.now().year
        if self.EARLIEST_NONLOGGING_DIST_DATE is not None:
            if self.EARLIEST_NONLOGGING_DIST_DATE.year > currentYear:
                self.dist_lag = 'EARLIEST_NONLOGGING_DIST_DATE-ERROR'
            else:
                self.dist_lag = currentYear - self.EARLIEST_NONLOGGING_DIST_DATE.year
        else:
            self.dist_lag = None
        del currentYear

        return

    def getPrcntConifer(self) -> None:
        """
        Function to calculate tbe percentage of conifer trees in forested areas.
        :return: None
        """
        # Create pandas DataFrame if inData isn't one
        pct_cnfr = 0
        # If species code is a conifer, add its percentage to sum
        if (self.SPECIES_CD_1 is not None) and (self.SPECIES_PCT_1 is not None) and (
                self.SPECIES_CD_1 in self.coniferList):
            pct_cnfr += self.SPECIES_PCT_1
        if (self.SPECIES_CD_2 is not None) and (self.SPECIES_PCT_2 is not None) and (
                self.SPECIES_CD_2 in self.coniferList):
            pct_cnfr += self.SPECIES_PCT_2
        if (self.SPECIES_CD_3 is not None) and (self.SPECIES_PCT_3 is not None) and (
                self.SPECIES_CD_3 in self.coniferList):
            pct_cnfr += self.SPECIES_PCT_3
        if (self.SPECIES_CD_4 is not None) and (self.SPECIES_PCT_4 is not None) and (
                self.SPECIES_CD_4 in self.coniferList):
            pct_cnfr += self.SPECIES_PCT_4
        if (self.SPECIES_CD_5 is not None) and (self.SPECIES_PCT_5 is not None) and (
                self.SPECIES_CD_5 in self.coniferList):
            pct_cnfr += self.SPECIES_PCT_5
        if (self.SPECIES_CD_6 is not None) and (self.SPECIES_PCT_6 is not None) and (
                self.SPECIES_CD_6 in self.coniferList):
            pct_cnfr += self.SPECIES_PCT_6

        # Change pct_cnfr to 100% if it evaluates to >100%
        if pct_cnfr is not None and pct_cnfr > 100:
            pct_cnfr = 100

        # Assign final value to self.pct_cnfr
        self.pct_cnfr = pct_cnfr

        del pct_cnfr

        return

    def getDryWet(self) -> None:
        """
        Function to check if BEC subzone is dry or wet
        :return: None
        """
        # Create dry/wet dictionary
        dryWet = {
            'd': 'dry',
            'x': 'dry',
            'm': 'wet',
            'w': 'wet',
            'v': 'wet',
            'u': 'undifferentiated'}

        # Lookup first letter of subzone and return if dry or wet
        self.dry_wet = dryWet.get(self.BEC_SUBZONE[0], 'Invalid Subzone')

        return

    def getStocking(self) -> None:
        """
        Function to get the number of live and dead stems in the stand (i.e., stocking)
        :return: None
        """
        liveStems = 0
        if self.VRI_LIVE_STEMS_PER_HA is not None:
            liveStems = self.VRI_LIVE_STEMS_PER_HA

        deadStems = 0
        if self.VRI_DEAD_STEMS_PER_HA is not None:
            deadStems = self.VRI_DEAD_STEMS_PER_HA

        self.stocking = liveStems + deadStems

        return

    def checkDomConifers(self, checkList: list) -> bool:
        """
        Function to check if the dominant conifers in a stand match species in a list.
        :param checkList:
        :return: true or false
        """
        sppCdList = [self.SPECIES_CD_1, self.SPECIES_CD_2, self.SPECIES_CD_3,
                     self.SPECIES_CD_4, self.SPECIES_CD_5, self.SPECIES_CD_6]
        sppPrcntList = [self.SPECIES_PCT_1, self.SPECIES_PCT_2, self.SPECIES_PCT_3,
                        self.SPECIES_PCT_4, self.SPECIES_PCT_5, self.SPECIES_PCT_6]
        spDF = pd.DataFrame([sppPrcntList], columns=sppCdList).iloc[0]

        # GET LIST OF CONIFER SPECIES AT SITE IF THEY MATCH SPECIES IN CHECKLIST
        cnfrList = [i for i in sppCdList if i in checkList]
        if not cnfrList:
            cnfrPrcnt = 0  # ASSIGN AS 0 IF NO CONIFER SPECIES IN CHECKLIST FOUND AT SITE
        else:
            cnfrPrcnt = spDF[cnfrList].max()  # GET MAXIMUM PERCENTAGE OF CONIFERS IN CHECKLIST

        # GET LIST OF ALL OTHER CONIFERS AT SITE
        altCnfrList = [i for i in sppCdList if ((not i in checkList) and (i in self.coniferList))]
        if not altCnfrList:
            altCnfrPrcnt = 0  # ASSIGN AS 0 IF NO OTHER CONIFER SPECIES FOUND AT SITE
        else:
            altCnfrPrcnt = spDF[altCnfrList].max()  # GET MAXIMUM PERCENTAGE OF ALL OTHER CONIFERS

        # Compare species and return result
        if cnfrPrcnt != 0 and cnfrPrcnt == altCnfrPrcnt:
            if sppCdList.index(cnfrList[0]) < sppCdList.index(altCnfrList[0]):
                return True
            else:
                return False
        elif cnfrPrcnt > altCnfrPrcnt:
            return True
        else:
            return False

    def decisionTree(self):
        """
        The fuel typing decision tree.
        """
        #### NON-VEGETATED SITE
        if (not self.is_vegetated) or (self.is_vegetated is None):
            #### SITE LOGGED
            if self.is_logged:
                #### SITE HARVESTED WITHIN LAST 6 YEARS
                if self.harv_lag <= 6:
                    if self.COAST_INTERIOR_CD == 'C':
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                    else:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                #### SITE HARVESTED WITHIN LAST 7-24 YEARS
                elif self.harv_lag <= 24:
                    if self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    else:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                #### SITE HARVESTED LONGER THAN 24 YEARS AGO
                else:
                    if self.BEC_ZONE_CODE in ['CMA', 'IMA']:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    elif self.BEC_ZONE_CODE in ['BAFA', 'MH']:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    elif self.BEC_ZONE_CODE in ['CWH', 'CDF', 'ICH'] and self.dry_wet == 'wet':
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                    elif self.BEC_ZONE_CODE in ['BWBS']:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                    elif self.BEC_ZONE_CODE == 'SWB':
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 50
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 50
                    elif (self.BEC_ZONE_CODE == 'SBS') or (self.BEC_ZONE_CODE == 'IDF' and self.dry_wet == 'wet') or (
                            self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry'):
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                    elif self.BEC_ZONE_CODE in ['SBPS', 'MS', 'ESSF'] or (
                            self.BEC_ZONE_CODE in ['IDF', 'CDF'] and self.dry_wet == 'dry'):
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                    elif self.BEC_ZONE_CODE in ['PP', 'BG']:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                    elif self.BEC_ZONE_CODE == 'CWH' and self.dry_wet == 'dry':
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
            #### SITE UNLOGGED
            else:
                #### SITE RECENTLY BURNED
                if self.is_burned and (self.dist_lag is not None) and (self.dist_lag < 11):
                    if self.dist_lag <= 3:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    elif self.dist_lag <= 6:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    elif self.dist_lag <= 10:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                #### SITE NOT RECENTLY BURNED
                else:
                    if self.BCLCS_LEVEL_2 in ['L', None]:
                        if self.SPECIES_CD_1 is not None:
                            if self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    else:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None

        #### SITE VEGETATED
        elif self.is_vegetated:
            #### SITE FORESTED
            if self.is_forested:
                #### SITE RECENTLY BURNED
                if self.is_burned and self.dist_lag is not None and self.dist_lag <= 10:
                    if self.pct_cnfr is not None and self.pct_cnfr >= 60:
                        if self.CROWN_CLOSURE is not None and self.CROWN_CLOSURE > 40:
                            if self.dist_lag <= 3:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            elif self.dist_lag <= 6:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:  # if self.dist_lag <= 10:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                        else:  # if self.CROWN_CLOSURE is None or self.CROWN_CLOSURE <= 40:
                            if self.dist_lag <= 1:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            elif self.dist_lag <= 6:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:  # if self.dist_lag <= 10:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                    else:
                        if self.dist_lag <= 1:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                        else:  # if self.dist_lag <= 10:
                            if self.season == 'dormant':
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                            else:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                #### SITE NOT RECENTLY BURNED
                else:
                    if (self.SPECIES_CD_1 is None) or (self.SPECIES_PCT_1 is None) or (self.SPECIES_PCT_1 == 0):
                        return inspect.getframeinfo(
                            inspect.currentframe()).lineno, 'VegForestNoBurn_Species-ERROR', None
                    #### PURE/SINGLE SPECIES STANDS
                    elif self.SPECIES_PCT_1 >= 80:
                        if self.SPECIES_CD_1 in self.coniferList:
                            #### PURE LODGEPOLE PINE STANDS
                            if self.SPECIES_CD_1 in ['PL', 'PLI', 'PLC', 'PJ', 'PXJ', 'P']:
                                if self.harv_lag is not None and self.harv_lag <= 7:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:
                                    if self.BCLCS_LEVEL_5 == 'SP':  #### SPARSE STANDS
                                        if (self.BEC_ZONE_CODE in ['CWH', 'CDF', 'MH']) or (
                                                self.BEC_ZONE_CODE in ['ICH'] and self.dry_wet == 'wet'):
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  #### DENSE OR OPEN STANDS
                                        if self.PROJ_HEIGHT_1 < 4:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                        elif self.PROJ_HEIGHT_1 <= 12:
                                            if self.stocking > 8000:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-4', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        elif self.PROJ_HEIGHT_1 > 12:
                                            if self.CROWN_CLOSURE < 40:
                                                if self.BEC_ZONE_CODE in ['BG', 'PP', 'IDF', 'MS']:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-7', None
                                                elif self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-5', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-3', None
                                            else:
                                                if self.EARLIEST_NONLOGGING_DIST_TYPE == 'IBM':  #### MOUNTAIN PINE BEETLE STANDS
                                                    if self.dist_lag <= 5:
                                                        if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 50:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'M-3', 65
                                                        elif self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD >= 25:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-2', None
                                                        else:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-3', None
                                                    else:
                                                        if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 50:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-2', None
                                                        elif self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD >= 25:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-3', None
                                                        else:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-3', None
                                                else:  #### NON MOUNTAIN PINE BEETLE STANDS
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-3', None
                            #### PURE PONDEROSA PINE STANDS
                            elif self.SPECIES_CD_1 == 'PY':
                                if self.BCLCS_LEVEL_5 in ['DE', 'OP']:  #### DENSE OR OPEN STANDS
                                    if self.harv_lag is not None and self.harv_lag <= 10:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:
                                        if self.PROJ_HEIGHT_1 < 4:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                        elif self.PROJ_HEIGHT_1 <= 12:
                                            if self.stocking > 8000:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-4', None
                                            elif self.stocking >= 3000:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        elif self.PROJ_HEIGHT_1 <= 17:
                                            if self.BCLCS_LEVEL_5 == 'DE':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            elif self.BCLCS_LEVEL_5 == 'OP':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif self.BCLCS_LEVEL_5 == 'SP':  #### SPARSE STANDS
                                    if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD >= 40:
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                    else:
                                        if self.harv_lag is not None and self.harv_lag <= 10:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                            #### PURE OTHER PINE STANDS
                            elif self.SPECIES_CD_1 in ['PA', 'PF', 'PW']:
                                if self.BCLCS_LEVEL_5 == 'DE':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif self.BCLCS_LEVEL_5 in ['SP', 'OP']:
                                    if self.stocking >= 900:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    elif self.stocking >= 600:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE DOUGLAS-FIR STANDS
                            elif self.SPECIES_CD_1 in ['FD', 'FDC', 'FDI', 'F']:
                                #### SITE HARVESTED WITHIN LAST 6 YEARS
                                if self.harv_lag is not None and self.harv_lag <= 6:
                                    if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                            self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                    else:  # if (self.BEC_ZONE_CODE in self.dryBECzones) or (self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry'):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                #### SITE HARVESTED LONGER THAN 6 YEARS AGO
                                else:
                                    if self.PROJ_HEIGHT_1 is not None and self.PROJ_HEIGHT_1 < 4:
                                        if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                        else:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                    elif self.PROJ_HEIGHT_1 is not None and self.PROJ_HEIGHT_1 >= 4:
                                        if self.CROWN_CLOSURE is not None and self.CROWN_CLOSURE > 55:
                                            if self.PROJ_HEIGHT_1 <= 12:
                                                if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-3', None
                                                else:  # if (self.BEC_ZONE_CODE in self.dryBECzones) or (self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry'):
                                                    if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 34:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-4', None
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-3', None
                                            elif self.PROJ_HEIGHT_1 > 12:
                                                if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-5', None
                                                else:  # if (self.BEC_ZONE_CODE in self.dryBECzones) or (self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry'):
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-7', None
                                        elif self.CROWN_CLOSURE is None or self.CROWN_CLOSURE >= 26:
                                            if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                    self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                            else:  # if (self.COAST_INTERIOR_CD == 'I'):
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:  # if self.CROWN_CLOSURE < 26:
                                            if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                    self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-2', None
                                            else:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'O-1a', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'O-1b', None
                                    else:
                                        return inspect.getframeinfo(
                                            inspect.currentframe()).lineno, 'VegForestNoBurnPureFd_ProjHeight-ERROR', None
                            #### PURE ENGELMANN SPRUCE STANDS
                            elif self.SPECIES_CD_1 == 'SE':
                                if self.harv_lag is not None and self.harv_lag <= 10:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:
                                    if self.BCLCS_LEVEL_5 == 'SP':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    elif self.BCLCS_LEVEL_5 == 'DE':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                    elif self.BCLCS_LEVEL_5 == 'OP':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                            #### PURE SITKA SPRUCE STANDS
                            elif self.SPECIES_CD_1 == 'SS':
                                if self.harv_lag is not None and self.harv_lag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                else:
                                    if self.BCLCS_LEVEL_5 == 'SP':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    elif self.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE BLACK OR WHITE SPRUCE STANDS
                            elif self.SPECIES_CD_1 in ['SB', 'SW']:
                                if self.harv_lag is not None and self.harv_lag <= 10:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:
                                    if self.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                    elif self.BCLCS_LEVEL_5 == 'SP':
                                        if self.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-1', None
                                        else:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 30
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 30
                            #### PURE SPRUCE (UNKNOWN OR HYBRID) STANDS
                            elif self.SPECIES_CD_1.startswith(
                                    'S'):  # in ['SX','SXB','SXE','SXL','SXS','SXW','SXX','S']:
                                if self.harv_lag is not None and self.harv_lag <= 7:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:
                                    if self.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                        if self.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                        else:  # if self.BCLCS_LEVEL_5 == 'SP':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-1', None
                                    else:
                                        if self.BCLCS_LEVEL_5 == 'SP':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:  # if self.BCLCS_LEVEL_5 in ['DE','OP']:
                                            if self.BEC_ZONE_CODE in ['CWH', 'CDF']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                            else:  # if self.COAST_INTERIOR_CD == 'I' and self.SPECIES_CD_1 != 'SS':
                                                if self.PROJ_HEIGHT_1 < 4:
                                                    if self.season == 'dormant':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'O-1a', None
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'O-1b', None
                                                elif self.PROJ_HEIGHT_1 >= 4:
                                                    if self.BCLCS_LEVEL_5 == 'OP':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-3', None
                                                    elif self.BCLCS_LEVEL_5 == 'DE':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-2', None
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'VegForestPureOtherSpruceInterior_NoBCLCSLv5-ERROR', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'VegForestPureOtherSpruceInterior_ProjHeight-ERROR', None
                            #### PURE REDCEDAR, YELLOW CEDAR OR HEMLOCK STANDS
                            elif self.SPECIES_CD_1 in ['C', 'CW', 'Y', 'YC', 'H', 'HM', 'HW', 'HXM']:
                                if self.harv_lag is not None and self.harv_lag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                else:
                                    if self.BCLCS_LEVEL_5 == 'DE':
                                        if self.PROJ_HEIGHT_1 < 4:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                        elif self.PROJ_HEIGHT_1 <= 15:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        elif self.PROJ_HEIGHT_1 > 15:
                                            if self.PROJ_AGE_1 < 60:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            elif self.PROJ_AGE_1 <= 99:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', 30
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', 30
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    elif self.BCLCS_LEVEL_5 == 'OP':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    elif self.BCLCS_LEVEL_5 == 'SP':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            #### PURE TRUE FIR STANDS
                            elif self.SPECIES_CD_1.startswith('B'):
                                if self.SPECIES_CD_1 == 'BG':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif self.SPECIES_CD_1 == 'BA':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 30
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 30
                                else:
                                    if self.BCLCS_LEVEL_5 == 'SP':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE YEW STANDS
                            elif self.SPECIES_CD_1 in ['T', 'TW']:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                            #### PURE JUNIPER STANDS
                            elif self.SPECIES_CD_1 in ['J', 'JR']:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            else:
                                return inspect.getframeinfo(
                                    inspect.currentframe()).lineno, 'VegForestedPureSpeciesStand_Species-ERROR', None
                        else:  #### DECIDUOUS/BROADLEAF OR LARCH STAND
                            if self.season == 'dormant':
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                            else:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                #### MIXED-SPECIES STANDS
                    elif self.SPECIES_PCT_1 < 80:
                        #### MIXED-SPECIES DECIDUOUS STANDS
                        if self.pct_cnfr <= 20:
                            if self.season == 'dormant':
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                            else:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                        #### MIXED-SPECIES CONIFER OR MIXEDWOOD STANDS
                        elif self.pct_cnfr > 20:
                            #### 21-40% CONIFER = DECIDUOUS DOMINATED MIXEDWOOD STANDS
                            if self.pct_cnfr <= 40:
                                if self.harv_lag is not None and self.harv_lag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                else:  # self.harv_lag > 6 or self.HARVEST_DATE is None:
                                    #### DOMINANT CONIFER = BLACK, WHITE, ENGELMANN, OR HYBRID SPRUCE
                                    if self.checkDomConifers(['SB', 'SW', 'SE', 'SX', 'SXB',
                                                              'SXE', 'SXL', 'SXS', 'SXW', 'SXX']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr
                                    #### DOMINANT CONIFER = UNKNOWN SPRUCE
                                    elif self.checkDomConifers(['S']):
                                        if self.COAST_INTERIOR_CD == 'C':
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.5
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.5
                                        else:  # if self.COAST_INTERIOR_CD == 'I':
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr
                                    #### DOMINANT CONIFER = ANY OTHER CONIFER
                                    else:
                                        if self.BCLCS_LEVEL_5 == 'SP':
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.5
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.5
                                        else:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.7
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.7
                            #### 41-65% CONIFER = CONIFER_DOMINATED MIXEDWOOD STANDS
                            elif self.pct_cnfr <= 65:
                                if self.harv_lag is not None and self.harv_lag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:
                                    #### DOMINANT CONIFER = LODGEPOLE PINE
                                    if self.checkDomConifers(['PL', 'PLI', 'PLC', 'PJ', 'PXJ', 'P']):
                                        if self.BCLCS_LEVEL_5 == 'SP':
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                        elif self.BCLCS_LEVEL_5 == 'OP':
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.7
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.7
                                        elif self.BCLCS_LEVEL_5 == 'DE':
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.8
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.8
                                    #### DOMINANT CONIFER = PONDEROSA PINE
                                    elif self.checkDomConifers(['PY']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                    #### DOMINANT CONIFER = OTHER PINE
                                    elif self.checkDomConifers(['PA', 'PF', 'PW']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.5
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.5
                                    #### DOMINANT CONIFER = DOUGLAS-FIR
                                    elif self.checkDomConifers(['F', 'FD', 'FDC', 'FDI']):
                                        if self.BEC_ZONE_CODE in ['CWH', 'CDF', 'ICH']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.5
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.5
                                        else:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                    #### DOMINANT CONIFER = ENGELMANN SPRUCE
                                    elif self.checkDomConifers(['SE']):
                                        if self.BCLCS_LEVEL_5 == 'SP':
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                        elif self.BCLCS_LEVEL_5 in ['OP', 'DE']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.9
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.9
                                    #### DOMINANT CONIFER = SITKA SPRUCE
                                    elif self.checkDomConifers(['SS']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.4
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.4
                                    #### DOMINANT CONIFER = BLACK OR WHITE SPRUCE
                                    elif self.checkDomConifers(['SB', 'SW']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr
                                    #### DOMINANT CONIFER = UNKNOWN OR HYBRID SPRUCE
                                    elif self.checkDomConifers(['SX', 'SXB', 'SXE', 'SXL', 'SXS', 'SXW', 'SXX', 'S']):
                                        if self.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                            if self.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', self.pct_cnfr
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', self.pct_cnfr
                                            elif self.BCLCS_LEVEL_5 in ['SP']:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                        else:
                                            if self.BCLCS_LEVEL_5 in ['SP']:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                            elif self.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                if self.COAST_INTERIOR_CD == 'I':
                                                    if self.season == 'dormant':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.8
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.8
                                                elif self.COAST_INTERIOR_CD == 'C':
                                                    if self.season == 'dormant':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.5
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.5
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'VegForestMixedSpeciesCnfrLT65_BCLCSLv5-ERROR', None
                                    #### DOMINANT CONIFER = REDCEDAR, YELLOW CEDAR OR HEMLOCK
                                    elif self.checkDomConifers(['C', 'CW', 'Y', 'YC', 'H', 'HM', 'HW', 'HXM']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.4
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.4
                                    #### DOMINANT CONIFER = FIR
                                    elif self.checkDomConifers(['B', 'BA', 'BG', 'BL']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                    #### DOMINANT CONIFER = YEW
                                    elif self.checkDomConifers(['T', 'TW']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = JUNIPER
                                    elif self.checkDomConifers(['J', 'JR']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            #### 66-80% CONIFER = CONIFER_DOMINATED MIXEDWOOD STANDS
                            elif self.pct_cnfr <= 80:
                                if self.harv_lag is not None and self.harv_lag <= 6:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:  # self.harv_lag > 6 or self.HARVEST_DATE is None:
                                    #### DOMINANT CONIFER = LODGEPOLE PINE
                                    if self.checkDomConifers(['PL', 'PLI', 'PLC', 'PJ', 'PXJ', 'P']):
                                        if self.BCLCS_LEVEL_5 in ['SP']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.5
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.5
                                        elif self.BCLCS_LEVEL_5 in ['OP']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.7
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.7
                                        elif self.BCLCS_LEVEL_5 in ['DE']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.8
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.8
                                    #### DOMINANT CONIFER = PONDEROSA PINE
                                    elif self.checkDomConifers(['PY']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    #### DOMINANT CONIFER = OTHER PINE
                                    elif self.checkDomConifers(['PA', 'PF', 'PW']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = DOUGLAS-FIR
                                    elif self.checkDomConifers(['F', 'FD', 'FDC', 'FDI']):
                                        if (self.BEC_ZONE_CODE in ['CWH', 'CDF']) or (
                                                self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                        else:
                                            if self.BCLCS_LEVEL_5 in ['DE']:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.7
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.7
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    #### DOMINANT CONIFER = ENGELMANN SPRUCE
                                    elif self.checkDomConifers(['SE']):
                                        if self.BCLCS_LEVEL_5 in ['SP']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                        elif self.BCLCS_LEVEL_5 in ['OP', 'DE']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.7
                                            else:
                                                return inspect.getframeinfo(
                                                    inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.7
                                    #### DOMINANT CONIFER = SITKA SPRUCE
                                    elif self.checkDomConifers(['SS']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = BLACK OR WHITE SPRUCE
                                    elif self.checkDomConifers(['SB', 'SW']):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-1', self.pct_cnfr
                                        else:
                                            return inspect.getframeinfo(
                                                inspect.currentframe()).lineno, 'M-2', self.pct_cnfr
                                    #### DOMINANT CONIFER = UNKNOWN OR HYBRID SPRUCE
                                    elif self.checkDomConifers(['SX', 'SXB', 'SXE', 'SXL', 'SXS', 'SXW', 'SXX', 'S']):
                                        if self.BEC_ZONE_CODE in ['BWBS', 'SWB']:
                                            if self.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', self.pct_cnfr
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', self.pct_cnfr
                                            if self.BCLCS_LEVEL_5 in ['SP']:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                        else:
                                            if self.BCLCS_LEVEL_5 in ['SP']:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.6
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.6
                                            else:  # self.BCLCS_LEVEL_5 in ['DE','OP']:
                                                if self.COAST_INTERIOR_CD == 'I':
                                                    if self.season == 'dormant':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-1', self.pct_cnfr * 0.8
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-2', self.pct_cnfr * 0.8
                                                else:  # self.COAST_INTERIOR_CD == 'C':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = REDCEDAR, YELLOW CEDAR OR HEMLOCK
                                    elif self.checkDomConifers(['C', 'CW', 'Y', 'YC', 'H', 'HM', 'HW', 'HXM']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = FIR
                                    elif self.checkDomConifers(['B', 'BA', 'BG', 'BL']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    #### DOMINANT CONIFER = YEW
                                    elif self.checkDomConifers(['T', 'TW']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                    #### DOMINANT CONIFER = JUNIPER
                                    elif self.checkDomConifers(['J', 'JR']):
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                            #### 81-100% CONIFER = PURE CONIFER, MIXED-SPECIES STANDS
                            elif self.pct_cnfr <= 100:
                                #### DOMINANT CONIFER = LODGEPONE PINE
                                if self.SPECIES_CD_1 in ['P', 'PL', 'PLI', 'PLC', 'PJ', 'PXJ']:
                                    if self.harv_lag is not None and self.harv_lag <= 7:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:
                                        if self.BCLCS_LEVEL_5 in ['SP']:
                                            if (self.BEC_ZONE_CODE in ['CWH', 'CDF', 'MH']) or (
                                                    self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-2', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:  # if self.BCLCS_LEVEL_5 in ['DE','OP']:
                                            if self.PROJ_HEIGHT_1 < 4:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'O-1a', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'O-1b', None
                                            elif self.PROJ_HEIGHT_1 >= 4:
                                                if self.SPECIES_CD_2.startswith('S') or self.SPECIES_CD_2.startswith(
                                                        'B'):
                                                    if self.PROJ_HEIGHT_1 <= 12:
                                                        if self.stocking > 8000:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-4', None
                                                        else:  # self.stocking <= 8000 or (self.VRI_LIVE_STEMS_PER_HA is None and self.VRI_DEAD_STEMS_PER_HA is None):
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-3', None
                                                    else:  # self.PROJ_HEIGHT_1 > 12:
                                                        if self.CROWN_CLOSURE < 40:
                                                            if self.BEC_ZONE_CODE in ['BG', 'PP', 'IDF', 'MS']:
                                                                return inspect.getframeinfo(
                                                                    inspect.currentframe()).lineno, 'C-7', None
                                                            elif self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                                                return inspect.getframeinfo(
                                                                    inspect.currentframe()).lineno, 'C-5', None
                                                            else:
                                                                return inspect.getframeinfo(
                                                                    inspect.currentframe()).lineno, 'C-3', None
                                                        else:  # self.CROWN_CLOSURE >= 40 or self.CROWN_CLOSURE is None:
                                                            if self.EARLIEST_NONLOGGING_DIST_TYPE == 'IBM':
                                                                if self.dist_lag <= 5:
                                                                    if self.BCLCS_LEVEL_5 in ['DE']:
                                                                        if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'M-3', 65
                                                                        elif self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-2', None
                                                                        else:  # self.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-2', None
                                                                    else:  # self.BCLCS_LEVEL_5 in ['OP']:
                                                                        if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'M-3', 65
                                                                        elif self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-2', None
                                                                        else:  # self.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-3', None
                                                                else:  # self.dist_lag > 5:
                                                                    if self.BCLCS_LEVEL_5 in ['DE']:
                                                                        if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-2', None
                                                                        elif self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-2', None
                                                                        else:  # self.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-3', None
                                                                    else:  # self.BCLCS_LEVEL_5 in ['OP']:
                                                                        if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 50:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-2', None
                                                                        elif self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD >= 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-3', None
                                                                        else:  # self.STAND_PERCENTAGE_DEAD < 25:
                                                                            return inspect.getframeinfo(
                                                                                inspect.currentframe()).lineno, 'C-3', None
                                                            else:
                                                                return inspect.getframeinfo(
                                                                    inspect.currentframe()).lineno, 'C-3', None
                                                else:
                                                    if self.CROWN_CLOSURE < 40:
                                                        if self.BEC_ZONE_CODE in ['IDF', 'PP', 'BG', 'SBPS', 'MS']:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-7', None
                                                        elif self.BEC_ZONE_CODE in ['CWH', 'CDF', 'ICH']:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-5', None
                                                        else:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-3', None
                                                    else:  # self.CROWN_CLOSURE >= 40:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-3', None
                                #### DOMINANT CONIFER = PONDEROSA PINE
                                elif self.SPECIES_CD_1 in ['PY']:
                                    if self.harv_lag is not None and self.harv_lag <= 7:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:  # self.harv_lag > 7:
                                        if self.PROJ_HEIGHT_1 < 4:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                        else:  # self.PROJ_HEIGHT_1 >= 4:
                                            if self.BCLCS_LEVEL_5 in ['DE']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            else:  # self.BCLCS_LEVEL_5 in ['OP','SP']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                #### DOMINANT CONIFER = OTHER PINE
                                elif self.SPECIES_CD_1 in ['PA', 'PF', 'PW']:
                                    if self.BCLCS_LEVEL_5 in ['DE']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    else:  # self.BCLCS_LEVEL_5 in ['OP','SP']:
                                        if self.stocking >= 900:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        elif self.stocking >= 600:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                #### DOMINANT CONIFER = DOUGLAS-FIR
                                elif self.SPECIES_CD_1.startswith('F'):
                                    if self.harv_lag is not None and self.harv_lag <= 6:
                                        if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                        else:  # if (self.BEC_ZONE_CODE in self.dryBECzones) or (self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                    else:  # self.harv_lag > 6:
                                        if self.PROJ_HEIGHT_1 < 4:
                                            if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                    self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-2', None
                                            else:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'O-1a', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'O-1b', None
                                        else:  # self.PROJ_HEIGHT_1 >= 4:
                                            if self.CROWN_CLOSURE > 55:
                                                if self.PROJ_HEIGHT_1 <= 12:
                                                    if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                            self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-5', None
                                                    else:  # if (self.BEC_ZONE_CODE in self.dryBECzones) or (self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry'):
                                                        if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 34:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-4', None
                                                        else:
                                                            if self.SPECIES_CD_2 == 'PY':
                                                                return inspect.getframeinfo(
                                                                    inspect.currentframe()).lineno, 'C-7', None
                                                            else:
                                                                return inspect.getframeinfo(
                                                                    inspect.currentframe()).lineno, 'C-3', None
                                                elif self.PROJ_HEIGHT_1 > 12:
                                                    if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                            self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-5', None
                                                    else:  # (self.BEC_ZONE_CODE in self.dryBECzones) or (self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry'):
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-7', None
                                            elif self.CROWN_CLOSURE >= 26 or self.CROWN_CLOSURE is None:
                                                if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-5', None
                                                else:  # self.COAST_INTERIOR_CD = 'I' and ((self.BEC_ZONE_CODE in self.dryBECzones) or (self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'dry')):
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-7', None
                                            else:
                                                if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                        self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                                    if self.season == 'dormant':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'D-1', None
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'D-2', None
                                                else:
                                                    if self.season == 'dormant':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'O-1a', None
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'O-1b', None
                                #### DOMINANT CONIFER = SPRUCE
                                elif self.SPECIES_CD_1.startswith('S'):
                                    if self.harv_lag is not None and self.harv_lag <= 6:
                                        if (self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']) or (
                                                self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                        else:  # (self.COAST_INTERIOR_CD = 'I') or (self.BEC_ZONE_CODE in self.dryBECzones):
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                    else:  # (self.harv_lag > 6):
                                        if self.SPECIES_CD_1 == 'SE':
                                            if self.BCLCS_LEVEL_5 in ['SP']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                            else:  # self.BCLCS_LEVEL_5 in ['DE','OP']:
                                                if self.SPECIES_CD_2 in ['BL', 'B', 'PL', 'P', 'PLI']:
                                                    if self.BCLCS_LEVEL_5 in ['DE']:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-2', None
                                                    else:  # self.BCLCS_LEVEL_5 in ['OP']:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-3', None
                                                elif self.SPECIES_CD_2 in ['HW', 'HM', 'CW', 'YC']:
                                                    if self.BCLCS_LEVEL_5 in ['DE']:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-3', None
                                                    else:  # self.BCLCS_LEVEL_5 in ['OP']:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-5', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-3', None
                                        elif self.SPECIES_CD_1 in ['SS']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                        elif self.SPECIES_CD_1 in ['SB']:
                                            if self.BCLCS_LEVEL_5 in ['DE', 'OP']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                            else:  # self.BCLCS_LEVEL_5 in ['SP']:
                                                if self.BEC_ZONE_CODE in ['BWBS']:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-1', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-3', None
                                        else:  # if self.SPECIES_CD_1 in ['SX','SXB','SXE','SXL','SXS','SXW','SXX','SW','S']:
                                            if self.BEC_ZONE_CODE in ['BWBS']:
                                                if self.BCLCS_LEVEL_5 in ['DE']:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-2', None
                                                elif self.BCLCS_LEVEL_5 in ['OP']:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-3', None
                                                else:  # self.BCLCS_LEVEL_5 in ['SP']:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-1', None
                                            else:
                                                if self.BEC_ZONE_CODE in ['CWH', 'MH', 'CDF']:
                                                    if (self.SPECIES_CD_2 in ['BL',
                                                                              'B']) or self.SPECIES_CD_2.startswith(
                                                            'P'):
                                                        if self.BCLCS_LEVEL_5 in ['SP']:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-7', None
                                                        else:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-3', None
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-5', None
                                                else:  # (self.COAST_INTERIOR_CD = 'I') and (not self.BEC_ZONE_CODE in self.borealBECzones):
                                                    if self.BCLCS_LEVEL_5 in ['SP']:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'C-7', None
                                                    else:
                                                        if self.BCLCS_LEVEL_5 in ['DE']:
                                                            return inspect.getframeinfo(
                                                                inspect.currentframe()).lineno, 'C-2', None
                                                        else:  # self.BCLCS_LEVEL_5 in ['OP']:
                                                            if self.STAND_PERCENTAGE_DEAD is not None and self.STAND_PERCENTAGE_DEAD > 34:
                                                                return inspect.getframeinfo(
                                                                    inspect.currentframe()).lineno, 'C-2', None
                                                            else:  # (self.STAND_PERCENTAGE_DEAD <= 34) or (self.STAND_PERCENTAGE_DEAD is None):
                                                                if (self.SPECIES_CD_2 in ['PL', 'PLI', 'P']):
                                                                    return inspect.getframeinfo(
                                                                        inspect.currentframe()).lineno, 'C-2', None
                                                                else:
                                                                    return inspect.getframeinfo(
                                                                        inspect.currentframe()).lineno, 'C-3', None
                                ##### DOMINANT CONIFER = REDCEDAR, YELLOW CEDAR OR HEMLOCK
                                elif self.SPECIES_CD_1.startswith('C') or self.SPECIES_CD_1.startswith(
                                        'Y') or self.SPECIES_CD_1.startswith('H'):
                                    if self.harv_lag is not None and self.harv_lag <= 6:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                    else:  # self.harv_lag > 6:
                                        if self.BCLCS_LEVEL_5 == 'DE':
                                            if self.PROJ_HEIGHT_1 < 4:
                                                if self.season == 'dormant':
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-1', None
                                                else:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'D-2', None
                                            elif self.PROJ_HEIGHT_1 <= 15:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                            else:  # (self.PROJ_HEIGHT_1 > 15) and (self.BCLCS_LEVEL_5 in ['DE']):
                                                if self.PROJ_AGE_1 < 60:
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-3', None
                                                elif self.PROJ_AGE_1 <= 99:
                                                    if self.season == 'dormant':
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-1', 40
                                                    else:
                                                        return inspect.getframeinfo(
                                                            inspect.currentframe()).lineno, 'M-2', 40
                                                else:  # (self.PROJ_AGE_1 > 99) or (self.BCLCS_LEVEL_5 in ['DE']) or (self.BCLCS_LEVEL_5 is None):
                                                    return inspect.getframeinfo(
                                                        inspect.currentframe()).lineno, 'C-5', None
                                        elif self.BCLCS_LEVEL_5 in ['OP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                        else:  # self.BCLCS_LEVEL_5 in ['SP']:
                                            if self.season == 'dormant':
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                ##### DOMINANT CONIFER = GRAND FIR
                                elif self.SPECIES_CD_1 in ['BG']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                ##### DOMINANT CONIFER = AMABALIS FIR
                                elif self.SPECIES_CD_1 in ['BA']:
                                    if self.SPECIES_CD_2 in ['SE', 'SW', 'S']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    else:
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                ##### DOMINANT CONIFER = OTHER FIR
                                elif self.SPECIES_CD_1 in ['B', 'BL']:
                                    if self.COAST_INTERIOR_CD == 'C':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # self.COAST_INTERIOR_CD == 'I':
                                        if self.BCLCS_LEVEL_5 in ['SP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                        elif self.BCLCS_LEVEL_5 in ['DE']:
                                            if self.SPECIES_CD_2 in ['SE', 'SW', 'S']:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                            else:
                                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                        else:  # self.BCLCS_LEVEL_5 in ['OP']:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                ##### DOMINANT CONIFER = YEW
                                elif self.SPECIES_CD_1 in ['T', 'TW']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                ##### DOMINANT CONIFER = JUNIPER
                                elif self.SPECIES_CD_1 in ['J', 'JR']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None

            #### NON-FORESTED SITE
            else:
                #### SITE RECENTLY BURNED
                if self.is_burned and (self.dist_lag is not None) and (self.dist_lag < 11):
                    if self.dist_lag <= 1:
                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                    elif self.dist_lag <= 3:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                    else:  # self.dist_lag <= 10:
                        if self.season == 'dormant':
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                        else:
                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                #### SITE NOT RECENTLY BURNED
                else:
                    #### SITE LOGGED
                    if self.is_logged:
                        if self.SPECIES_CD_1 is not None:
                            if self.harv_lag <= 7:
                                if str(self.SPECIES_CD_1).startswith('P'):
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                elif str(self.SPECIES_CD_1).startswith('S') or str(self.SPECIES_CD_1).startswith('B'):
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-2', None
                                elif (self.SPECIES_CD_1 in ['CW', 'YC']) or str(self.SPECIES_CD_1).startswith('H'):
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                elif str(self.SPECIES_CD_1).startswith('FD'):
                                    if self.BEC_ZONE_CODE in ['CWH', 'ICH']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-3', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                            elif self.harv_lag <= 24:
                                if (self.BEC_ZONE_CODE in ['CWH', 'MH']) or (
                                        self.BEC_ZONE_CODE == 'ICH' and self.dry_wet == 'wet'):
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                else:  # (self.BEC_ZONE_CODE in self.dryBECzones) or (self.dry_wet == 'dry'):
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            else:  # if self.harv_lag > 24:
                                if self.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                elif self.BEC_ZONE_CODE == 'BAFA':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif self.BEC_ZONE_CODE == 'CWH':
                                    if self.dry_wet == 'dry':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # self.dry_wet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif self.BEC_ZONE_CODE == 'BWBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                elif self.BEC_ZONE_CODE == 'SWB':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 50
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 50
                                elif self.BEC_ZONE_CODE == 'SBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif self.BEC_ZONE_CODE == 'SBPS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif self.BEC_ZONE_CODE == 'MS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif self.BEC_ZONE_CODE == 'IDF':
                                    if self.dry_wet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # self.dry_wet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif self.BEC_ZONE_CODE == 'PP':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif self.BEC_ZONE_CODE == 'BG':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif self.BEC_ZONE_CODE == 'MH':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif self.BEC_ZONE_CODE == 'ESSF':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif self.BEC_ZONE_CODE == 'CDF':
                                    if self.dry_wet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # self.dry_wet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif self.BEC_ZONE_CODE == 'ICH':
                                    if self.dry_wet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                    else:  # self.dry_wet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                else:
                                    return (inspect.getframeinfo(inspect.currentframe()).lineno,
                                            'VegNonForestUnburnedLoggedGT24HasSpecies_BEC-ERROR', None)
                        else:  # if self.SPECIES_CD_1 is None:
                            if self.harv_lag <= 5:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'S-1', None
                            elif self.harv_lag <= 24:
                                if self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                else:  # (self.BEC_ZONE_CODE in self.dryBECzones) or (self.dry_wet == 'dry'):
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                            else:  # self.harv_lag > 24:
                                if self.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                elif self.BEC_ZONE_CODE == 'BAFA':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif self.BEC_ZONE_CODE == 'CWH':
                                    if self.dry_wet == 'dry':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # self.dry_wet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif self.BEC_ZONE_CODE == 'BWBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-2', None
                                elif self.BEC_ZONE_CODE == 'SWB':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 25
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 25
                                elif self.BEC_ZONE_CODE == 'SBS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-3', None
                                elif self.BEC_ZONE_CODE == 'SBPS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif self.BEC_ZONE_CODE == 'MS':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif self.BEC_ZONE_CODE == 'IDF':
                                    if self.dry_wet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # self.dry_wet == 'wet':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 50
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 50
                                elif self.BEC_ZONE_CODE == 'PP':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif self.BEC_ZONE_CODE == 'BG':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif self.BEC_ZONE_CODE == 'MH':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif self.BEC_ZONE_CODE == 'ESSF':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                elif self.BEC_ZONE_CODE == 'CDF':
                                    if self.dry_wet == 'dry':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-7', None
                                    else:  # self.dry_wet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                elif self.BEC_ZONE_CODE == 'ICH':
                                    if self.dry_wet == 'dry':
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-1', 40
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'M-2', 40
                                    else:  # self.dry_wet == 'wet':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'C-5', None
                                else:
                                    return inspect.getframeinfo(
                                        inspect.currentframe()).lineno, 'VegNonForestUnburnedLoggedGT24NoSpecies_BEC-ERROR', None
                    #### SITE NOT LOGGED
                    else:  # not isLogged(df):
                        if self.SPECIES_CD_1 is not None:
                            if self.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            elif self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH', 'BAFA']:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                            else:
                                if self.season == 'dormant':
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                        else:
                            if self.INVENTORY_STANDARD_CD == 'F':
                                if self.NON_PRODUCTIVE_CD in [11, 12, 13]:
                                    if self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    else:  # (self.BEC_ZONE_CODE in self.dryBECzones) or (self.dry_wet == 'dry'):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif self.NON_PRODUCTIVE_CD == 35:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'W', None
                                elif self.NON_PRODUCTIVE_CD == 42:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                elif self.NON_PRODUCTIVE_CD in [60, 62, 63]:
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif self.NON_PRODUCTIVE_CD is None:
                                    if self.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                    elif self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    else:  # (self.BEC_ZONE_CODE in self.dryBECzones) or (self.dry_wet == 'dry'):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                            else:  # self.INVENTORY_STANDARD_CD in ['V','I','L']:
                                if self.LAND_COVER_CLASS_CD_1 in ['LA', 'RE', 'RI', 'OC']:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'W', None
                                elif self.LAND_COVER_CLASS_CD_1 == 'HG':
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                elif self.LAND_COVER_CLASS_CD_1 in ['BY', 'BM', 'BL']:
                                    if self.season == 'dormant':
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                    else:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                elif self.LAND_COVER_CLASS_CD_1 in ['SL', 'ST', 'HE', 'HF', None]:
                                    if self.BEC_ZONE_CODE in ['CMA', 'IMA']:
                                        return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None
                                    elif self.BEC_ZONE_CODE in ['CWH', 'MH', 'ICH']:
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-1', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'D-2', None
                                    else:  # (self.BEC_ZONE_CODE in self.dryBECzones) or (self.dry_wet == 'dry'):
                                        if self.season == 'dormant':
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1a', None
                                        else:
                                            return inspect.getframeinfo(inspect.currentframe()).lineno, 'O-1b', None
                                else:
                                    return inspect.getframeinfo(inspect.currentframe()).lineno, 'N', None

    def getFuelType(self,
                    season: str,
                    COAST_INTERIOR_CD: str,
                    BCLCS_LEVEL_1: str,
                    BCLCS_LEVEL_2: str,
                    BCLCS_LEVEL_3: str,
                    BCLCS_LEVEL_4: str,
                    BCLCS_LEVEL_5: str,
                    BEC_ZONE_CODE: str,
                    BEC_SUBZONE: str,
                    EARLIEST_NONLOGGING_DIST_TYPE: str,
                    EARLIEST_NONLOGGING_DIST_DATE: dt,
                    HARVEST_DATE: dt,
                    CROWN_CLOSURE: int,
                    PROJ_HEIGHT_1: float,
                    PROJ_AGE_1: int,
                    VRI_LIVE_STEMS_PER_HA: int,
                    VRI_DEAD_STEMS_PER_HA: int,
                    STAND_PERCENTAGE_DEAD: int,
                    INVENTORY_STANDARD_CD: str,
                    NON_PRODUCTIVE_CD: str,
                    LAND_COVER_CLASS_CD_1: str,
                    SPECIES_CD_1: str,
                    SPECIES_PCT_1: float,
                    SPECIES_CD_2: str,
                    SPECIES_PCT_2: float,
                    SPECIES_CD_3: str,
                    SPECIES_PCT_3: float,
                    SPECIES_CD_4: str,
                    SPECIES_PCT_4: float,
                    SPECIES_CD_5: str,
                    SPECIES_PCT_5: float,
                    SPECIES_CD_6: str,
                    SPECIES_PCT_6: float) -> tuple:
        """
        Function to generate the fuel type with the BC Wildfire Fuel Typing algorithm
        :param season:
        :param COAST_INTERIOR_CD:
        :param BCLCS_LEVEL_1:
        :param BCLCS_LEVEL_2:
        :param BCLCS_LEVEL_3:
        :param BCLCS_LEVEL_4:
        :param BCLCS_LEVEL_5:
        :param BEC_ZONE_CODE:
        :param BEC_SUBZONE:
        :param EARLIEST_NONLOGGING_DIST_TYPE:
        :param EARLIEST_NONLOGGING_DIST_DATE:
        :param HARVEST_DATE:
        :param CROWN_CLOSURE:
        :param PROJ_HEIGHT_1:
        :param PROJ_AGE_1:
        :param VRI_LIVE_STEMS_PER_HA:
        :param VRI_DEAD_STEMS_PER_HA:
        :param STAND_PERCENTAGE_DEAD:
        :param INVENTORY_STANDARD_CD:
        :param NON_PRODUCTIVE_CD:
        :param LAND_COVER_CLASS_CD_1:
        :param SPECIES_CD_1:
        :param SPECIES_PCT_1:
        :param SPECIES_CD_2:
        :param SPECIES_PCT_2:
        :param SPECIES_CD_3:
        :param SPECIES_PCT_3:
        :param SPECIES_CD_4:
        :param SPECIES_PCT_4:
        :param SPECIES_CD_5:
        :param SPECIES_PCT_5:
        :param SPECIES_CD_6:
        :param SPECIES_PCT_6:
        :return: a tuple containing
            1: the line number where the code exited the decision tree,
            2: the fuel type, and
            3: the fuel type modifier
        """
        self.season = season
        self.COAST_INTERIOR_CD = COAST_INTERIOR_CD
        self.BCLCS_LEVEL_1 = BCLCS_LEVEL_1
        self.BCLCS_LEVEL_2 = BCLCS_LEVEL_2
        self.BCLCS_LEVEL_3 = BCLCS_LEVEL_3
        self.BCLCS_LEVEL_4 = BCLCS_LEVEL_4
        self.BCLCS_LEVEL_5 = BCLCS_LEVEL_5
        self.BEC_ZONE_CODE = BEC_ZONE_CODE
        self.BEC_SUBZONE = BEC_SUBZONE
        self.EARLIEST_NONLOGGING_DIST_TYPE = EARLIEST_NONLOGGING_DIST_TYPE
        self.EARLIEST_NONLOGGING_DIST_DATE = EARLIEST_NONLOGGING_DIST_DATE
        self.HARVEST_DATE = HARVEST_DATE
        self.CROWN_CLOSURE = CROWN_CLOSURE
        self.PROJ_HEIGHT_1 = PROJ_HEIGHT_1
        self.PROJ_AGE_1 = PROJ_AGE_1
        self.VRI_LIVE_STEMS_PER_HA = VRI_LIVE_STEMS_PER_HA
        self.VRI_DEAD_STEMS_PER_HA = VRI_DEAD_STEMS_PER_HA
        self.STAND_PERCENTAGE_DEAD = STAND_PERCENTAGE_DEAD
        self.INVENTORY_STANDARD_CD = INVENTORY_STANDARD_CD
        self.NON_PRODUCTIVE_CD = NON_PRODUCTIVE_CD
        self.LAND_COVER_CLASS_CD_1 = LAND_COVER_CLASS_CD_1
        self.SPECIES_CD_1 = SPECIES_CD_1
        self.SPECIES_PCT_1 = SPECIES_PCT_1
        self.SPECIES_CD_2 = SPECIES_CD_2
        self.SPECIES_PCT_2 = SPECIES_PCT_2
        self.SPECIES_CD_3 = SPECIES_CD_3
        self.SPECIES_PCT_3 = SPECIES_PCT_3
        self.SPECIES_CD_4 = SPECIES_CD_4
        self.SPECIES_PCT_4 = SPECIES_PCT_4
        self.SPECIES_CD_5 = SPECIES_CD_5
        self.SPECIES_PCT_5 = SPECIES_PCT_5
        self.SPECIES_CD_6 = SPECIES_CD_6
        self.SPECIES_PCT_6 = SPECIES_PCT_6

        # Verify inputs
        self.verifyInputs()

        # Process the input variables
        self.isVegetated()
        self.isForested()
        self.isLogged()
        self.isBurned()
        self.getHarvLag()
        self.getDistLag()
        self.getPrcntConifer()
        self.getDryWet()
        self.getStocking()

        # Run the fuel typing algorithm via the decision tree
        return self.decisionTree()
