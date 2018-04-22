'''
Created on 3 Apr 2018

@author: ernest
'''

import math
from ernestas_monkevicius_14493758_project.data_structures import *
import os
import traceback
import itertools
from scipy.special.basic import perm

class ItineraryOptimizer:
    '''
    Takes in itineraries and produces best or approximate best route for the itinerary.
    '''

    def __init__(self, files):
        '''
        Constructor
        '''
        self.__inputRoutes = InputRoutes(files['inputFile'])
        self.__airports = Airport(files['airportsFile'])
        self.__aircraft = Aircraft(files['aircraftFile'])
        
    def getOptimizedItinerary(self, number=None):
        '''Returns a desired number of optimized itineraries, if number=None then return all.'''
        if number is None:
            number = self.__inputRoutes.size
            
        optimizedRoutesList = []
        try:
            for i in range(0, number):
                optimizedRoutesList.append(self.__optimize(self.__inputRoutes.next))
                #itinerary = self.__inputRoutes.next
                #optimizedRoutesList.append(self.__optimize(itinerary))
        except IndexError: #when EOF is reached
            return optimizedRoutesList
        return optimizedRoutesList
    
    def __optimize(self, destinationList): #get the optimal route - brute force
        aircraft = self.__aircraft.getAircraft(destinationList[-1])
        print('optimize: ', aircraft)
        print('optimize:',destinationList[0])
        destinationListPermutations = self.__permute(destinationList)
        print('optimize:',destinationListPermutations)
        for list in destinationListPermutations:
            list.extend([destinationList[0], list[0]]) # [A1,A2,A3,A4] -> [A2,A3,A4,A5,A0,A1]
        print('optimize:',destinationListPermutations)
        
        costsList = [self.__cost(perm, aircraft) for perm in destinationListPermutations] #Find the total cost of each permutation
        return min(costsList) #Find the smallest costing permutation and return it with it's cost
    
    def __permute(self, destinationList): #generate permutation for the destinations excluding home start airport
        permutationTuples = itertools.permutations(destinationList[1:5]) #slice the 4 destination airports and permute them
        return list([list(_) for _ in permutationTuples]) #itertools.permutations() returns tuples, need to make them lists to modify later
    
    def __cost(self, destinationPermutation, aircraft): #calculate the cost of a permutation    
        print('cost: ', aircraft)
        airportList = self.__airports.getAirports(destinationPermutation) #get airport information for each of the codes.
        #e.g. 'OLT' -> ['United States', 'OLT', 32.7552, -117.1995]
        costList = []
        print('cost:',airportList)
        try:
            for i in range(0, len(airportList)-1):
                distance = coordDist(airportList[i][2:5], airportList[i+1][2:5])
                costList.append(distance)
                #print(costList)
        except Exception as e:
            traceback.print_exc()
            
        print('cost:',costList)
        return 0
    

def coordDist(latLong1, latLong2):
        """Returns the great circle distance between two sets of coordinates"""
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