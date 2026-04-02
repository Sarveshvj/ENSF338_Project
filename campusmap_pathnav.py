class Building:     # node (vertex) class
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id    = building_id       # IE. "ICT-121"
        self.name           = name              # "Information and Comm. Tech"
        self.location       = location          # (lat, lon) or grid coords
        self.rooms          = {}                # room id -> Room

class Campus:       # graph class
    def __init__(self):
        self.buildings = {}
        self.pathways  = [ [] for i in range(len(self.buildings)) ]     # list of lists, 
                                                                        # sublists contain tuples storing neighbor and edge weight of respective building (node)

