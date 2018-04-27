'''
Created on 3 Apr 2018

@author: ernest
'''
import unittest
from ernestas_monkevicius_14493758_project import data_structures
from ernestas_monkevicius_14493758_project import utility
from ernestas_monkevicius_14493758_project import algorithms
import pandas as pd
import numpy as np
from ernestas_monkevicius_14493758_project.data_structures import Aircraft, Airport, Currency, InputRoutes
from ernestas_monkevicius_14493758_project.algorithms import ItineraryOptimizer

class Test(unittest.TestCase):
    
    #Creating a test graph. The structure is just like the example in lecture notes.
    testGraph = data_structures.Graph()

    for i in "abcdefghij":
        testGraph.setVertex(i)
        
    testGraph.setEdge('a', ['b', 'c', 'd', 'e', 'j'], [4,6,7,5,1])
    testGraph.setEdge('b', 'aef', '498')
    testGraph.setEdge('c', 'ad', '62')
    testGraph.setEdge('d', 'acj', '723')
    testGraph.setEdge('e', 'abfh', '5943')
    testGraph.setEdge('f', 'beg', '847')
    testGraph.setEdge('g', 'fi', [7,15])
    testGraph.setEdge('h', 'ei', [3,12])
    testGraph.setEdge('i', 'ghj', [15,12,9])
    testGraph.setEdge('j', 'adi', '139')
        
    def test_Graph(self):
        self.assertTrue(self.testGraph.getNeighbours('a') == {'b': 4, 'c': 6, 'd': 7, 'e': 5, 'j': 1})
        self.assertTrue(list(self.testGraph.getVertices()) == ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
        self.assertTrue(self.testGraph.getEdge('a', 'b') == 4)
        
    def test_BFS(self):
        self.assertTrue(algorithms.BFS(self.testGraph, 'c') == ['c', 'a', 'd', 'b', 'e', 'j', 'f', 'h', 'i', 'g'])
    
    def test_OptimalPath(self):
        self.assertTrue(algorithms.optimalPath(self.testGraph, 'c', 'g') == ['c', 'a', 'e', 'f', 'g'])
        
        
    airportList = {
    'DUB' : ['Dublin', 'Ireland', [53.421333, -6.270075]],
    'LHR' : ['Heathrow', 'United Kingdom', (51.4775, -0.461389)],
    'JFK' : ['John F Kennedy Intl', 'United States', (40.639751, -73.778925)],
    'AAL' : ['Aalborg', 'Denmark', (57.092789, 9.849164)],
    'CDG' : ['Charles De Gaulle', 'France', (49.012779, 2.55)],
    'SYD' : ['Sydney Intl', 'Australia', (-33.946111, 151.177222)]
    }    
    
    def test_coordDist(self):
        firstAirport = self.airportList['DUB'][2]
        answerList = []
        for airport in self.airportList:
            answerList.append([airport, algorithms.coordDist(firstAirport, self.airportList[airport][2])])
        self.assertTrue(answerList == [['DUB', 0], ['LHR', 449], ['JFK', 5103], ['AAL', 1097], ['CDG', 785], ['SYD', 17215]])
    
    def test_cleanUp(self):
        df = pd.DataFrame(data={'col1' : [1,2,3,np.nan,5], 'col2' : [1,np.nan,3,4,5]})
        df = utility.cleanUp(df)
        self.assertTrue(df.shape == (3,2))
        
    def test_aircraft(self):
        af = Aircraft('testdata/aircraft.csv')
        self.assertTrue(af.aircraft == [['A319', 3750.0],['A320', 12000.0],['A321', 12000.0],['A330', 13430.0],['737', 9012.304],
                                             ['747', 15771.532],['757', 11622.65348],['767', 11474.5942],['777', 15610.598],
                                             ['BAE146', 2909.0],['DC8', 7724.832],['F50', 2055.0],['MD11', 20390.3378],['A400M', 3298.0],
                                             ['C212', 1811.0],['V22', 2610.34948],['BB1', 1627.04274],['BA10', 1371.15768],
                                             ['SIS99', 1300.34672],['SAH', 1300.34672]])
        
        self.assertTrue(af.getAircraft('A319') == ['A319', 3750.0])
        self.assertTrue(af.getAircraft('747') == ['747', 15771.532])
        
    def test_airport(self):
        ap = Airport('testdata/airport.csv')
        self.assertTrue(ap.getAirports(['KBL']) == [['Afghanistan', 'KBL', 34.565853000000004, 69.212328]]) #get the third list
        self.assertTrue(ap.getAirports(['hEa']) == [['Afghanistan', 'HEA', 34.210017, 62.2283]]) #get the first list, convert code to upper case
        self.assertTrue(ap.getAirports(['thisCodeDoesntExist']) == [None]) #get None for invalid codes
        self.assertTrue(ap.getAirports(['HEA','JAa', 'thisCodeDoesntExist', 'KdH', 'mmZ']) == [['Afghanistan', 'HEA', 34.210017, 62.2283],
                                                                                 ['Afghanistan', 'JAA', 34.399842, 70.498625],
                                                                                 None,
                                                                                 ['Afghanistan', 'KDH', 31.505755999999998, 65.847822],
                                                                                 ['Afghanistan', 'MMZ', 35.930789000000004, 64.760917]]) #get a list of lists
    
    def test_currency(self):
        c = Currency('testdata/countrycurrency.csv', 'testdata/currencyrates.csv')
        self.assertTrue(c.getExchangeRate('Afghanistan') == 0.016440) #1 Afghani == 0.016440 Euro
        self.assertTrue(c.getExchangeRate('Albania') == 0.007237) #1 Albanian Lek == 0.007237 Euro
        self.assertTrue(c.getExchangeRate('thisCountryDoesNotExist') == None) #get None for invalid countries
        self.assertTrue(c.getExchangeRate('RUSSIAN FEDERATION') == 0.01524) #get Russia's exchange rate using alternative
        self.assertTrue(c.getExchangeRate('Russia') == 0.01524) #get Russia's exchange rate using regular name
        
    def test_inputRoutes(self):
        ir = InputRoutes('testdata/testroutesOld.csv')
        self.assertTrue(ir.next == ['DUB', 'LHR', 'SYD', 'JFK', 'AAL', '777']) #get the first input route
        self.assertTrue(ir.next == ['SNN', 'ORK', 'MAN', 'CDG', 'SIN', 'A330']) #get the second input route
        ir.next
        ir.next
        ir.next
        self.assertTrue(ir.next == ['BOS', 'DFW', 'ORD', 'SFO', 'ATL', 'NAN']) #get the fifth input route
        for _ in range(5, 14): #move down the rows to get to the row of interest...
            ir.next
        self.assertTrue(ir.next == ['DUB', 'LHR', 'SYD', 'JFK', 'SIN', '777']) #this row was originally ['DUB', 'lhr', 'SYD', 'JFK', 'SiN', '777']
        self.assertTrue(ir.size == 17)
    
    
    filesDict = { 'outputFile' : 'testdata/testBestroutes.csv',
                  'inputFile' : 'testdata/testroutesNew.csv',
                  'currencyFile' : 'testdata/currencyrates.csv',
                  'countryCurrencyFile' : 'testdata/countrycurrency.csv',
                  'airportsFile' : 'testdata/airport.csv',
                  'aircraftFile' : 'testdata/aircraft.csv'}
    
    def test_itineraryOptimizer(self):
        io = ItineraryOptimizer(self.filesDict)
        self.assertTrue(io.getOptimizedItinerary(1) == [['LUP','EKI','YPO','MRV','AGM','A321','->','LUP', 'AGM', 'MRV', 'YPO', 'EKI', 'LUP', 15166.05498]])
        self.assertTrue(io.getOptimizedItinerary(1) == [['MAM','BXR','ERS','GDN','NBX','747','->','MAM', 'NBX', 'BXR', 'GDN', 'ERS', 'MAM', 2508.7659795]])
        self.assertTrue(io.getOptimizedItinerary(1) == [['OLA','OLT','ELU','EGR','MNZ','767','->','OLA', 'MNZ', 'OLT', 'ELU', 'EGR', 'OLA', 10087.174878]])
        self.assertTrue(io.getOptimizedItinerary(3) != None)
        self.assertTrue(len(io.getOptimizedItinerary()) == 34) 
        
if __name__ == '__main__':
    unittest.main()
