import sys

class Building:     # node (vertex) class
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id    = building_id       # IE. "ICT-121"
        self.name           = name              # "Information and Comm. Tech"
        self.location       = location          # (lat, lon) or grid coords
        self.rooms          = {}                # room id -> Room

class Campus:       # graph class
    def __init__(self):
        '''
        -   self.buildings is a dict that stores Buildings nodes as keys with assigned value being
            pointer to the nodes associated adjacency list (self.pathways)
        -   self.pathways is an adjacency list formatted as a list of lists, each sublist associated
            to a Building node and containing tuples storing info on the connected Building node and edge weight
            between the two nodes.
        
        NOTES: functions are adapted and adjusted from lab08 ex1 work, hence adjacency list use for convenience of reference and familiarity
        '''
        self.buildings = {}     # dict for buildings, node as key, value is pointer to associated adjacency list in self.pathways
        self.pathways  = [ [] for i in range(len(self.buildings)) ]     # adjacency list of lists, 
                                                                        # sublists contain tuples storing neighbor and edge weight of respective building (node)
    
    def addBuilding(self, id):
        '''
        -   adds new Building node to Campus graph given building_id value

        NOTES: Currently instatiates Building Node using only building_id value
        may need more than just building_id to instantiate building node, 
        or default other values to None if not given
        '''
        for building in self.buildings:
            if building.building_id == id:
                return False

        new_building = Building(id)
        self.pathways.append([])
        self.buildings[new_building] = self.pathways[-1]
        return new_building
    
    def addPathway(self, building1, building2, weight):
        '''
        -   adds new Pathway edge given two building nodes (n1, n2) and edge weight (weight).
        '''
        if building1 not in self.buildings or building2 not in self.buildings:
            return -1
        
        self.buildings[building1].append((building2, weight))     # add n2 node and associated edge weight to current n1 nodes adj list thru self.buildings node key acess
        self.buildings[building2].append((building1, weight))

    def fileImport(self, file):
        '''
        -   imports graph description from file, possibly a GraphViz .dot file formatted:
            (taken from lab 8)
            strict graph G {
	            0 -- 557	[weight=45];
                0 -- 596	[weight=30];
                0 -- 802	[weight=86];
                0 -- 817	[weight=92];
                1 -- 306	[weight=26];
                1 -- 788	[weight=93];
                2 -- 786	[weight=76];

        -   connection identifiers possibly building_id's (0 -- 557 ...)
        -   weights provided
        -   likely undirected weighted graphs
        '''
        self.buildings = {}
        self.pathways = []
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

                if not lines[0].strip() == 'strict graph G {':
                    return None
                
                for line in lines[1:]:
                    line = line.strip()

                    if line == '}':
                        break

                    if '--' not in line:
                        return None
                    
                    parts = line.split('--')
                    id1 = parts[0].strip()
                    id2 = parts[1].split('[')[0].strip()

                    if 'weight' in line:
                        weight = int(line.split('weight=')[1].split(']')[0])
                    else:
                        weight = 1

                    building1 = None
                    building2 = None

                    for building in self.buildings:
                        if building.building_id == id1:
                            building1 = building
                        if building.building_id == id2:
                            building2 = building
                        if building1 and building2:
                            break

                    if building1 is None:
                        building1 = self.addBuilding(id1)

                    if building2 is None:
                        building2 = self.addBuilding(id2)

                    self.addPathway(building1, building2, weight)
        
        except:
            return None


    def dijkstra(self, srcNode):
        '''
        adapted and adjusted from 'advanced graphs 1' lecture
        currDist, pred, and toBeChecked adjusted from lists to dicts to better suit current chosen data style
        NOTES: return format for use in being called by shortestPathNav(), NOT individual call.
        '''
        # referenced from class but using dicts instead of lists for easier interpretations of current dict format into lecture example
        currDist = {}           # dict stores nodes as keys with int values corresponding to distances from srcNode
        pred = {}               # dict stores nodes as keys with values being predecessor nodes of key node
        toBeChecked = {}        # dict stores nodes as keys with bool flag to determine if node has been checked out from queue

        for V in self.buildings:
            currDist[V] = float("inf")           # using current node in self.buildings as key in currDist, set value to infinity method cited from StackOverflow: 1
            pred[V] = None
            toBeChecked[V] = True
        currDist[srcNode] = 0                       # currDist[srcNode] to be checked first in queue since 0 and rest is infinity

        
        for i in range(len(self.buildings)):
            toCheckValues = {}
            for node in toBeChecked:
                if toBeChecked[node] == True:
                    toCheckValues[node] = currDist[node]
            V = min(toCheckValues, key=toCheckValues.get)       # gets key node of min value in toCheckValues dict, method cited from StackOverflow: 2
            toBeChecked[V] = False
            for (U, weight) in self.buildings[V]:               # iterate over each edge tuple in self.buildings[V]
                tempDistance = currDist[V] + weight
                if tempDistance < currDist[U]:
                    currDist[U] = tempDistance
                    pred[U] = V
        
        return currDist, pred           # returns currDist: dict of distances of nodes from srcNode with node keys, and pred: dict of predecessor building_ids of key nodes for shortest path from srcNode
                                        
    def shortestPathNav(self, srcNode, destNode):
        currDist, pred = self.dijkstra(srcNode)

        path = []                       # ordered list of nodes, ordered from shortest path of srcNode (path[0]) to destNode (path[-1])
        current = destNode              # need to iterate backwards, use pred[current] to iterate for appending to path in reverse order
        while current != None:          # until predecessor of srcNode, None determined from pred[current]
            path.append(current)
            current = pred[current]

        path.reverse()                  # reverse path to put in correct sequential order, srcNode -> ... -> destNode, method cited from geeksforgeeks: 3
        
        return path, currDist[destNode] # return shortest path of nodes and total distance of destNode to srcNode from dijkstra().

'''
CITINGS:

1.  https://stackoverflow.com/questions/7781260/how-to-represent-an-infinite-number-in-python
2.  https://stackoverflow.com/questions/3282823/get-the-key-corresponding-to-the-minimum-value-within-a-dictionary
3.  https://www.geeksforgeeks.org/python/python-reversing-list/
'''