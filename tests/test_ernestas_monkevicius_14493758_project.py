'''
Created on 3 Apr 2018

@author: ernest
'''
import unittest
from ernestas_monkevicius_14493758_project import data_structures
from ernestas_monkevicius_14493758_project import utility

class Test(unittest.TestCase):
    
    #Creating a test graph. The structure is just like the example in lecture notes.
    testGraph = utility.Graph()

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
        self.assertTrue(utility.BFS(self.testGraph, 'c') == ['c', 'a', 'd', 'b', 'e', 'j', 'f', 'h', 'i', 'g'])
    
    def test_OptimalPath(self):
        self.assertTrue(utility.optimalPath(self.testGraph, 'c', 'g') == ['c', 'a', 'e', 'f', 'g'])
        
        
    airportList = {
    'DUB' : ['Dublin', 'Ireland', (53.421333, -6.270075)],
    'LHR' : ['Heathrow', 'United Kingdom', (51.4775, -0.461389)],
    'JFK' : ['John F Kennedy Intl', 'United States', (40.639751, -73.778925)],
    'AAL' : ['Aalborg', 'Denmark', (57.092789, 9.849164)],
    'CDG' : ['Charles De Gaulle', 'France', (49.012779, 2.55)],
    'SYD' : ['Sydney Intl', 'Australia', (-33.946111, 151.177222)]
    }    
    
    def test_getDistanceBetweenAirports(self):
        firstAirport = list(self.airportList.keys())[0]
        answerList = []
        for airport in self.airportList:
            answerList.append([airport, utility.getDistanceBetweenAirports(self.airportList, firstAirport, airport)])
        self.assertTrue(answerList == [['DUB', 0], ['LHR', 449], ['JFK', 5103], ['AAL', 1097], ['CDG', 785], ['SYD', 17215]])
    
if __name__ == '__main__':
    unittest.main()
