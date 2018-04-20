'''
Created on 15 Apr 2018

@author: ernest
'''

import math

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

def getDistanceBetweenAirports(airportList, airportCode1, airportCode2):
    """Returns the great circle distance between two airports"""
    
    def coordDist(latLong1, latLong2):
        """Returns the great circle distance between two sets of coordinates"""
        lat1 = math.radians(90-latLong1[0])
        long1 = math.radians(latLong1[1])
        lat2 = math.radians(90-latLong2[0])
        long2 = math.radians(latLong2[1])

        product1 = math.sin(lat1)*math.sin(lat2)*math.cos(long1-long2)
        product2 = math.cos(lat1)*math.cos(lat2)

        return round(math.acos(product1+product2)*6371)
    
    
    airport1Coord = airportList[airportCode1][2]
    airport2Coord = airportList[airportCode2][2]
    
    return coordDist(airport1Coord, airport2Coord)

def cleanUp(df):
    '''Drops duplicate rows and rows with NaN values in argument dataframe'''
    return df.dropna().drop_duplicates()
    