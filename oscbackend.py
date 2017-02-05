# -*- coding: UTF-8 -*-
'''
Created on 3 févr. 2017

@author: dassier
'''

import OSC
from Cython.Shadow import address

class TouchPanelOSCBackend(object):
    '''
    OSC backend
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def startClient(self, address='127.0.0.1', port=7700):
        self.client = OSC.OSCClient()
        self.client.connect((address, port))
        
    def startServer(self, address='127.0.0.1', port=9900):
        self.server = OSC.ThreadingOSCServer((address, port))
        
    def closeServer(self):
        self.server.close()

    def closeClient(self):
        self.client.close()
        
    def close(self):
        self.closeClient()
        self.closeServer()

    def addhandler(self, address, callback):
        self.server.addMsgHandler(address, callback)
        
    def send(self, address, data):
        msg = OSC.OSCMessage(address)
        if type(data) is list:
            for d in data:
                msg.append(d)
        else:
            msg.append(data)
        try:
            self.client.send(msg)
        except OSC.OSCClientError as e:
            print (e)
        