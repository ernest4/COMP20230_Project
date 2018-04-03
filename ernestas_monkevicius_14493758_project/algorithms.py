'''
Created on 3 Apr 2018

@author: ernest
'''

import math

class Dummy:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

def dist(lat1, long1, lat2, long2):
    """Returns distance between two sets of coordinates"""
    lat1 = math.radians(90-lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(90-lat2)
    long2 = math.radians(long2)
    
    product1 = math.sin(lat1)*math.sin(lat2)*math.cos(long1-long2)
    product2 = math.cos(lat1)*math.cos(lat2)
    
    return round(math.acos(product1+product2)*6371)

airportList = {
    'DUB' : ['Dublin', 'Ireland', 53.421333, -6.270075],
    'LHR' : ['Heathrow', 'United Kingdom', 51.4775, -0.461389],
    'JFK' : ['John F Kennedy Intl', 'United States', 40.639751, -73.778925],
    'AAL' : ['Aalborg', 'Denmark', 57.092789, 9.849164],
    'CDG' : ['Charles De Gaulle', 'France', 49.012779, 2.55],
    'SYD' : ['Sydney Intl', 'Australia', -33.946111, 151.177222]
}

def getDistanceBetweenAirports(airportCode1, airportCode2):
    """Returns the distance between two airports"""
    return dist(airportList[airportCode1][2],airportList[airportCode1][3],airportList[airportCode2][2],airportList[airportCode2][3])





