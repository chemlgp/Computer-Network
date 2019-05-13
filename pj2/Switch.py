# Project 2 for OMS6250

from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        #TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree
        ini = []
        ini.append(self.switchID)
        self.root = ini[0]
        self.distance = 0
        self.pathThrough = ini[0]
        self.activeLinks = []

    def send_initial_messages(self):

        length = len(self.links)

        for i in range(length):
            # Message(root, distance, origin, destination, pathThrough)
            msg = Message(self.switchID, 0, self.switchID, self.links[i], False)
            self.send_message(msg)
        return

    def process_message(self, message):

        if message.pathThrough == False and message.origin != self.pathThrough and message.origin in self.activeLinks:
            self.activeLinks.remove(message.origin)

        elif message.pathThrough == True:
            if message.origin not in self.activeLinks:
                self.activeLinks.append(message.origin)


        # if the message has a new root
        if message.root < self.root:
            ls = []
            ls.append(message.root)
            self.root = message.root
            ls.append(self.root)
            self.distance = message.distance + 1
            ls.append(self.distance)
            self.pathThrough = message.origin
            ls.append(self.pathThrough)
            if ls[3] not in self.activeLinks:
                self.activeLinks.append(ls[3])
            newLength = len(self.links)
            for i in range(newLength):
                message = Message(self.root, self.distance, self.switchID, self.links[i], self.pathThrough == self.links[i])
                self.send_message(message)

        # if the message has the same root but a shorter distance
        if message.root == self.root and message.distance + 1 < self.distance:
            self.distance = message.distance + 1
            newPathThrough = message.origin

            newLength = len(self.links)

            for j in range(newLength):
                message = Message(self.root, self.distance, self.switchID, self.links[j], newPathThrough == self.links[j])
                self.send_message(message)

            self.pathThrough = newPathThrough

            self.activeLinks.remove(self.pathThrough)
            lss = []
            lss.append(newPathThrough)
            if lss[0]  not in self.activeLinks:
                self.activeLinks.append(lss[0])
        # message has the same root and same distance but the sender has a smaller switchID than current path
        if message.root == self.root and message.distance + 1 == self.distance and self.pathThrough > message.origin:
            newPathThrough = message.origin

            newLength = len(self.links)
            i = 0

            while i < newLength:
                message = Message(self.root, self.distance, self.switchID, self.links[i], newPathThrough == self.links[i])
                self.send_message(message)
                i += 1

            self.activeLinks.remove(self.pathThrough)
            lsss = []
            lsss.append(newPathThrough)
            self.pathThrough = lsss[0]
            if lsss[0] not in self.activeLinks:
                self.activeLinks.append(lsss[0])
        return

    def generate_logstring(self):


        self.activeLinks.sort()
        Strings = []
        activelength = len(self.activeLinks)
        j = 0
        for linkID in self.activeLinks:
            temp = []
            temp.append(linkID)
            temp.append(self.switchID)
            Strings.append(str(temp[1]) + ' - ' + str(temp[0]))

        return ', '.join(Strings)
