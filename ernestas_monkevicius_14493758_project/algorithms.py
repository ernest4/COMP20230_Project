'''
Created on 3 Apr 2018

@author: ernest
'''

import math
from ernestas_monkevicius_14493758_project.data_structures import *
import os
import traceback
import itertools

class ItineraryOptimizer:
    '''
    Takes in itineraries and supporting files and produces the best route for
    the itinerary, via exhaustive brute force evaluation.
    '''
    
    #Global variable for the class. Contains the cached information for a cost of a leg.
    airportLegCostCacheDict = {}

    def __init__(self, files):
        '''
        Takes in a list of files and creates instances of appropriate classes
        to store and prepare those files.
        '''
        
        self.__inputRoutes = InputRoutes(files['inputFile'])
        self.__airports = Airport(files['airportsFile'])
        self.__aircraft = Aircraft(files['aircraftFile'])
        self.__currency = Currency(files['countryCurrencyFile'],
                                    files['currencyFile'])
        
        
    def getOptimizedItinerary(self, number=None):
        '''
        getOptimizedItinerary(number : integer) 
        -> (optimizedRoutesList : list of lists)
        
        Returns a desired number of optimized itineraries,
        if number=None then return all.
        '''
        
        #If no specific number given, set number of itineraries to be processed
        #to equal all the itineraries in the input file.
        if number is None:
            number = self.__inputRoutes.size
            
        optimizedRoutesList = []
        for _ in range(0, number): #for the number of itineraries required.
            #Get the the itinerary to process
            nextItinerary = self.__inputRoutes.next
            
            #If we successfully got an itinerary, optimize it.
            if nextItinerary is not None:
                optimizedRoutesList.append(self.__optimize(nextItinerary))
            else:
                #If EOF is reached, no more itineraries left to process.
                break
            
        #print('getOptimizedItinerary: Final',optimizedRoutesList) #TESTING
        return optimizedRoutesList #Return all optimized itineraries.
    
    
    def __optimize(self, destinationList): #get the optimal route - brute force
        '''
        __optimize(destinationList : list) -> (cheapestPermutation : list)
        
        Returns a cheapest permuation with it's cost.
        '''
        
        #print("Optimizing itinerary:", destinationList)
        
        aircraft = self.__aircraft.getAircraft(destinationList[-1])
        if aircraft is None: #No valid aircraft found
            return [] #No valid aircraft provided means no flight plan made
            #aircraft = ['A321', 12000.0] #HARDCODED PLANE WITH LONEGEST RANGE, MAKE DYNAMIC !
            
        homeDestination = destinationList[0]
        destinationListPermutations = self.__permute(destinationList)
        
        #Positive infinity to start when comparing the cost of the cheapest permutation.
        lowestCost = float("inf")
        
        cheapestPermutation = []
        for permutation in destinationListPermutations: 
            #Attach home and first destination to the end of each permutation
            #and find the total cost of the permutation.
            # [A1,A2,A3,A4] -> [A1,A2,A3,A4,A0,A1]
            
            permutation.extend([homeDestination, permutation[0]])
            extendedPerm = permutation
            
            cost = self.__cost(extendedPerm, aircraft)
            if cost is None: 
                #Indicates that there's a leg that the aircraft can't complete,
                #this permutation is not possible, discard it.
                continue #try the next permutation...
            elif cost == -1:
                #Indicates that one of the airport codes or currencies is invalid
                #and/or missing, this route list is not possible, abort the search.
                return []
                
            if cost < lowestCost: #If all is good an valid, keep track of the best permutation.
                lowestCost = cost #Keep track of the lowest.
                cheapestPermutation = [homeDestination, permutation[0],
                                        permutation[1], permutation[2],
                                         permutation[3], homeDestination,
                                          lowestCost]
                
        #Lowest costing permutation with it's cost
        return cheapestPermutation
    
    
    def __permute(self, destinationList): #generate permutation for the destinations excluding home start airport
        '''
        __permute(destinationList : list) -> list of lists
        
        Returns list of permutations for a list of destinations excluding home start airport.
        '''
        #slice the 4 destination airports and permute them
        permutationTuples = itertools.permutations(destinationList[1:5])
        #itertools.permutations() returns tuples, need to make them lists to modify later
        return list([list(_) for _ in permutationTuples])
        
    
    def __cost(self, destinationPermutation, aircraft): #calculate the cost of a permutation    
        '''
        __cost(destinationPermutation : list, aircraft : list) -> int
        
        Returns list of permutations for a list of destinations.
        '''
        
        aircraftRange = aircraft[1]
        airportList = self.__airports.getAirports(destinationPermutation) #get airport information for each of the codes.
        #e.g. 'OLT' -> ['United States', 'OLT', 32.7552, -117.1995]
        
        #If one of the airport codes is invalid, return prematurely.
        for airport in airportList:
            if airport is None:
                return -1
        
        total = 0
        for i in range(0, len(airportList)-1):
            fromAirport = airportList[i][0]
            toAirport = airportList[i+1][0]
            
            #If no cached value is found, compute the distance between start
            #airport and destination airport
            distance = coordDist(airportList[i][2:5], airportList[i+1][2:5])
            
            #if any leg is longer than aircraft range, this permutation can't be flown.
            if distance > aircraftRange:
                return None
            
            exchangeRate = self.__currency.getExchangeRate(toAirport)
            if exchangeRate is not None:
                #Update the total cost
                total += distance*exchangeRate
            else:
                #Means one of the currencies was not found and/or invalid
                return -1
            
        return total
    

def coordDist(latLong1, latLong2):
        '''
        coordDist(latLong1 : list, latLong2 : list) -> float
        
        Returns the great circle distance between two sets of coordinates.
        '''
        
        lat1 = math.radians(90-latLong1[0])
        long1 = math.radians(latLong1[1])
        lat2 = math.radians(90-latLong2[0])
        long2 = math.radians(latLong2[1])

        product1 = math.sin(lat1)*math.sin(lat2)*math.cos(long1-long2)
        product2 = math.cos(lat1)*math.cos(lat2)

        return round(math.acos(product1+product2)*6371)


def optimalPath(graph, rootNode, targetNode):
    '''Based on algorithm from Wikipedia: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    Finds the most optimal path from rootNode to targetNode.'''
    
    #This function takes us through the graph and finds the costs of reaching vertices in the graph
    def dijkstra(graph, source, destination):
        dist = {}
        prev = {}
        Q = []
        
        for vertex in graph.getVertices():
            dist[vertex] = float('inf')
            prev[vertex] = None
            Q.append(vertex)
            
        dist[source] = 0
        
        while Q:
            u = Q[0] #start with the first element
            for vertex in Q: #compare all vertices in Q and select the one with least distance
                if dist[vertex] < dist[u]:
                    u = vertex
                    if u == destination: #we reached the destination node and can exit prematurely to save time
                        return dist, prev
                    
            Q.remove(u) #remove the visited vertex
            
            for v in graph.getNeighbours(u):
                alt = dist[u] + graph.getEdge(u, v)
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    
        return dist, prev
    
    #This code constructs the path
    prev = dijkstra(graph, rootNode, targetNode)[1]
    S = []
    u = targetNode
    while prev[u]: #backtrace the path from target vertex back to source vertex
        S.append(u)
        u = prev[u]
    S.append(u)
    S.reverse() #reverse the path to point from source to target
    return S


def BFS(graph, rootNode):
    '''Finds all the nodes in the graph, starting from rootNode.'''
    to_visit = []
    to_visit.append(rootNode)
    
    visited = []
    
    while to_visit:
        current = to_visit.pop(0)
        if not current in visited:
            visited.append(current)
        
        for neighbour in graph.getNeighbours(current):
            if not neighbour in visited:
                to_visit.append(neighbour)
        
    return visited