'''
Created on 3 Apr 2018

@author: ernest
'''

import pandas as pd
from ernestas_monkevicius_14493758_project.utility import cleanUp
import traceback
import sys
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

class Graph:
    '''Models the graph data structure.'''
    def __init__(self):
        self.__vertices = {}
        
    def setVertex(self, v):
        if not v in self.getVertices():
            #create a vertex key with empty adjacency dict
            self.__vertices[v] = {}
        else: 
            #Error, vertex v already exists.
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
        except IOError as e: #Cannot read given file, load default
            print('Cannot read file,',file,' loading default...')
            self.__df_aircraft = pd.read_csv('data/aircraft.csv', skipinitialspace=True)
            #traceback.print_exc()
            
        self.__df_aircraft = self.__df_aircraft[['code', 'units', 'range']]
        self.__df_aircraft.loc[self.__df_aircraft['units'] == 'imperial', 'range'] *= 1.60934 #1.60934 is miles to kilometers
        self.__df_aircraft = self.__df_aircraft.drop('units', 1)
        self.__df_aircraft = cleanUp(self.__df_aircraft)
        self.__aircraftDict = self.__df_aircraft.set_index('code').T.to_dict('records')[0]
    
    @property
    def aircraft(self):
        #Return all aircraft in the dataframe
        return self.__df_aircraft.values.tolist()
    
    def getAircraft(self, code):
        code = code.upper()
        #Look for aircraft in the dictionary.
        if code in self.__aircraftDict:
            return [code, self.__aircraftDict[code]]
        else: 
            #Failed to find aircraft.
            return None


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
            print('Cannot read file,',file,' loading default...')
            self.__df_airport = pd.read_csv('data/airport.csv', skipinitialspace=True, header=None, names=[0,1,2,'country', 'IATA', 'ICAO','N_lat','E_lon',8,9,10,11])
            #traceback.print_exc()
            
        #extract the required columns
        self.__df_airport = self.__df_airport[['country', 'IATA','N_lat','E_lon']]
        self.__df_airport = cleanUp(self.__df_airport) #Remove duplicate rows and rows with NaN values
        self.__airportsDict = self.__df_airport.set_index('IATA').T.to_dict('list')
        
    def getAirports(self, codes):
        '''
        getAirports(codes : list) -> list of lists
        
        output format: [['Afghanistan', 'KBL', 34.565853000000004, 69.212328]]
        '''
        
        if type(codes) != type([]) and type(codes) != type(tuple()):
            raise Exception('codes argument must be a list')
        
        codes = [c.upper() for c in codes]
        airports = []
                
        for code in codes:
            if code in self.__airportsDict:
                airports.append([self.__airportsDict[code][0],
                                  code,
                                   self.__airportsDict[code][1],
                                    self.__airportsDict[code][2]])
            else:
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
        except IOError as e:
            print('Cannot read file,',countryCurrencyFile,' loading default...')
            self.__df_countrycurrency = pd.read_csv('data/countrycurrency.csv', skipinitialspace=True)
            #traceback.print_exc()
            
        try:
            self.__df_currencyrates = pd.read_csv(currencyRatesFile, skipinitialspace=True, header=None, names=['name', 'currency_alphabetic_code', 'toEuro', 'fromEuro'])
        except IOError as e:
            print('Cannot read file,',currencyRatesFile,' loading default...')
            self.__df_currencyrates = pd.read_csv('data/currencyrates.csv', skipinitialspace=True, header=None, names=['name', 'currency_alphabetic_code', 'toEuro', 'fromEuro'])
            #traceback.print_exc()
            
        #extract the required columns
        self.__df_countrycurrency = self.__df_countrycurrency[[self.__df_countrycurrency.columns[14],self.__df_countrycurrency.columns[15],self.__df_countrycurrency.columns[0]]]
        self.__df_countrycurrency = cleanUp(self.__df_countrycurrency) #Remove duplicate rows and rows with NaN values
        
        #Create a dictionary of main names e.g. 'Russia'
        self.__countrycurrencyDictMain = self.__df_countrycurrency[['currency_alphabetic_code','name']].set_index('name').T.to_dict('records')[0]
        #Create a dictionary of alternative names e.g. 'RUSSIAN FEDERATION'
        self.__countrycurrencyDictAlt = self.__df_countrycurrency[['currency_alphabetic_code','currency_country_name']].set_index('currency_country_name').T.to_dict('records')[0]

        
        #extract the required columns
        self.__df_currencyrates = self.__df_currencyrates[self.__df_currencyrates.columns[1:3]]
        self.__df_currencyrates = cleanUp(self.__df_currencyrates) #Remove duplicate rows and rows with NaN values
        
        #Create a dictionary of currencies
        self.__currenciesDict = self.__df_currencyrates.set_index('currency_alphabetic_code').T.to_dict('records')[0]
        
    def getExchangeRate(self, countryName):
        countryNameUpper = countryName.upper()
        #Try finding currency code using country main name
        if countryName in self.__countrycurrencyDictMain:
            code = self.__countrycurrencyDictMain[countryName]
        #If above search failed, try finding currency code using country alternative name
        elif countryNameUpper in self.__countrycurrencyDictAlt:
            code = self.__countrycurrencyDictAlt[countryNameUpper]
        else:
            #No currency code found for requested country
            return None
        
        #Return exchange rate for a valid currency code.
        if code in self.__currenciesDict:
            return self.__currenciesDict[code]
        else:
            return None
        
        
class InputRoutes:
    '''
    Stores the input routes.
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
            sys.exit("Cannot read input file: "+file)
            #traceback.print_exc()
            
        #Drop any itineraries which do not have 5 values for airports
        self.__df_routes = self.__df_routes.dropna(subset=[0,1,2,3,4])
        
    @property
    def next(self): #Get one itinerary list from the dataframe at a time.
        self.dataframeIndex += 1
        if self.dataframeIndex < self.size:
            return [str(_).upper() for _ in self.__df_routes.iloc[self.dataframeIndex].values.tolist()]
        else:
            return None
    
    @property
    def size(self): #Get the total number of itineraries in the dataframe
        return self.__df_routes.shape[0]
        
        
        
    