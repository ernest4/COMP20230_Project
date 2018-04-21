'''
Created on 3 Apr 2018

@author: ernest
'''

import pandas as pd
from ernestas_monkevicius_14493758_project.utility import cleanUp

class Graph:
    '''Models the graph data structure.'''
    def __init__(self):
        self.__vertices = {}
        
    def setVertex(self, v):
        if not v in self.getVertices():
            #create a vertex key with empty adjacency dict
            self.__vertices[v] = {}
        else: #Error, vertex v already exists.
            return -1
        
    def setEdge(self, v1, v2, cost=None):
        #adds 1 or more bidirectional connections with corresponding cost.
        if cost is None: #Default cost is 1.
            cost = [1 for _ in range(0, len(v2))]
        for c, v in enumerate(v2):
            if v not in self.__vertices[v1]:
                self.__vertices[v1][v] = int(cost[c])
                self.__vertices[v][v1] = int(cost[c])
                
    def getEdge(self, v1, v2):
        return self.__vertices[v1][v2]
            
    def getNeighbours(self, x):
        return self.__vertices[x]
    
    def getVertices(self):
        return self.__vertices.keys()
            
    def __str__(self):
        returnStr = ""
        for v in self.__vertices.keys():
            returnStr = "\n".join([returnStr,''.join([v,"->",str(self.__vertices[v])])])
        return returnStr

class Aircraft:
    '''
    Stores aircraft codes and ranges.
    '''

    def __init__(self, file):
        '''
        Takes in a file and creates a list of [aircraft, range] lists.
        '''
        try:
            self.__df_aircraft = pd.read_csv(file, skipinitialspace=True)
        except IOError as e:
            print(e)
            
        self.__df_aircraft = self.__df_aircraft[['code', 'units', 'range']]
        self.__df_aircraft.loc[self.__df_aircraft['units'] == 'imperial', 'range'] *= 1.60934 #1.60934 is miles to kilometers
        self.__df_aircraft = self.__df_aircraft.drop('units', 1)
        self.__df_aircraft = cleanUp(self.__df_aircraft)
        self.__df_aircraft = self.__df_aircraft.values.tolist()
    
    @property
    def aircraft(self):
        return self.__df_aircraft

class Airport:
    '''
    Stores airport countries, codes and coordinates.
    '''

    def __init__(self, file):
        '''
        Takes in a file and creates a list of [country, code, latitude, longitude] lists.
        '''
        try:
            self.__df_airport = pd.read_csv(file, skipinitialspace=True, header=None, names=[0,1,2,'country', 'IATA', 'ICAO','N_lat','E_lon',8,9,10,11])
        except IOError as e:
            print(e)
            
        self.__df_airport = self.__df_airport[['country', 'IATA','N_lat','E_lon']]
        self.__df_airport = cleanUp(self.__df_airport)
        
    def getAirports(self, codes):
        codes = [c.upper() for c in codes]
        airports = []
        
        for code in codes:
            try:
                airports.append(self.__df_airport.loc[self.__df_airport['IATA'] == code].values.tolist()[0])
            except Exception as e:
                airports.append(None)
                
        return airports


class Currency:
    '''
    Stores country names, their currency codes and exchange rates.
    '''

    def __init__(self, countryCurrencyFile, currencyRatesFile):
        '''
        Takes in a countryCurrencyFile and creates a list of [currency_alphabetic_code, currency_country_name] lists.
        Takes in a currencyRatesFile and creates a list of [currency_alphabetic_code, toEuro] lists.
        '''
        try:
            self.__df_countrycurrency = pd.read_csv(countryCurrencyFile, skipinitialspace=True)
            self.__df_currencyrates = pd.read_csv(currencyRatesFile, skipinitialspace=True, header=None, names=['name', 'currency_alphabetic_code', 'toEuro', 'fromEuro'])
        except IOError as e:
            print(e)
            
        self.__df_countrycurrency = self.__df_countrycurrency[self.__df_countrycurrency.columns[14:16]]
        self.__df_countrycurrency = cleanUp(self.__df_countrycurrency)
        
        self.__df_currencyrates = self.__df_currencyrates[self.__df_currencyrates.columns[1:3]]
        self.__df_currencyrates = cleanUp(self.__df_currencyrates)
    
    def getExchangeRate(self, countryName):
        countryName = countryName.upper()
        try:
            code = self.__df_countrycurrency.loc[self.__df_countrycurrency['currency_country_name'] == countryName].values.tolist()[0][0]
            return self.__df_currencyrates.loc[self.__df_currencyrates['currency_alphabetic_code'] == code].values.tolist()[0][1]
        except Exception as e:
            return None
        
class InputRoutes:
    '''
    Stores the test routes.
    '''
    dataframeIndex = -1
    
    def __init__(self, file):
        '''
        Takes in a file and creates a list of input route lists.
        '''
        try:
            self.__df_routes = pd.read_csv(file, skipinitialspace=True, header=None,
                          error_bad_lines=False, names=[x for x in range(0,6)])
        except Exception as e:
            print(e)
            
        self.__df_routes = self.__df_routes.dropna(subset=[0,1,2,3,4])
        
    @property
    def next(self):
        self.dataframeIndex += 1
        return [str(_).upper() for _ in self.__df_routes.iloc[self.dataframeIndex].values.tolist()]
        
        
        
    