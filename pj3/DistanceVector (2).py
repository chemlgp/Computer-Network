# Project 3 for CS 6250: Computer Networks
#


from Node import *
from helpers import *

class DistanceVector(Node):

    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)


        ''' The dictionary is used to hold distance info'''
        self.vector = {name:0}


    def is_outgoing_node(self, node_name):
        for link in self.outgoing_links:
            if node_name == link.name:
                return True
            else:
                return False

    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here.

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''



        vector_copy = self.vector.copy()
        for link in self.incoming_links:
            msg = {"from":self.name , "vector":vector_copy, "to":link}
            self.send_msg(msg,link.name)


    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:

        updated = False
        for msg in self.messages:
            # messages is a list, it contains many msg.

            # start to traverse all msgs, each msg is a dictionary. 'vector' in msg is a dict in a dict.

            out_node_names = msg["vector"].keys()

            # each msg contains three pieces of info: 'from' , 'vector', 'to'
            # 'vector' is a dictionary
            # it contains might be more than one key(nodename)-value(weght) paires, SO we extract all nodenames here. The nodename here is all of the NODEs that the node sent message can reach to. Let's name them 'out_node_names'

            # traverse all nodenames one by one:

            for out_node_name in out_node_names:
                # if an out_node_name is not in the node's vector, which means this node found a new destination(to) it can reach
                # this node need to confirm that this out_node_name is not itself
                if out_node_name not in self.vector and out_node_name != self.name:
                    # this node need to know if this out_node_name can be reach directly, which means if this out_node_name is in its outgoing_links, it can reach it directly, so the weight is just the weight of link.
                    if self.is_outgoing_node(out_node_name):
                        weight = int(self.get_outgoing_neighbor_weight(out_node_name))
                    # if the out_node_name cannot be reach directly, it need to add the weight of itself to previous node  and the weight of the previous node to the out_node_name.
                    else:
                        weight = int(self.get_outgoing_neighbor_weight(msg["from"])) + int(msg["vector"][out_node_name])
                    # Once the weight to out_node_name is updated, the current node need to change.
                    # So it needs to add an new node-weight pair in its vector dictionary
                    self.vector[out_node_name] = weight
                    updated = True




                # if an out_node_name is already in the current node's vector, it need to confirm that whether the distance has any change or not.
                elif out_node_name in self.vector and out_node_name != self.name:
                    to_from_distance = int(self.get_outgoing_neighbor_weight(msg["from"]))
                    out_node_name_from_distance = int(msg["vector"][out_node_name])
                    overall_distance = to_from_distance + out_node_name_from_distance


                    # Here to handle : Infinite LOOP!
                    if to_from_distance <= -99 or out_node_name_from_distance <= -99 or overall_distance <= -99:
                        if self.vector[out_node_name]  != -99:

                            self.vector[out_node_name] = -99
                            updated = True

                    else:
                        if overall_distance < self.vector[out_node_name]:
                            if overall_distance > -99:
                                self.vector[out_node_name] = overall_distance
                                updated = True
                            else:

                                self.vector[out_node_name] = -99
                                updated = True





        # Empty queue
        self.messages = []

        if updated == True:

            for i_link in self.incoming_links:
                up_vec = self.vector.copy()
                up_msg = {"from":self.name , "vector":up_vec, "to":i_link}
                self.send_msg(up_msg,i_link.name)

    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It
        prints distances to the console and the log file in the following format (no whitespace either end):

        A:A0,B1,C2

        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''

       
        coma = ','
        text = []
        key_collection = self.vector.keys()
        key_collection.sort()
        for key in key_collection:
            text.append(key + str(self.vector[key]))
        text.sort()
        add_entry(self.name, coma.join(text))
