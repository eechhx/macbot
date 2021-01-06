import isotp
import logging
import time
import threading
import pybinn

from can.interfaces.socketcan import SocketcanBus

class GoLinkNode(object):
    def __init__(self, nodeId):
        self.nodeId = nodeId
        self.bus = SocketcanBus(channel='can0')
        addr = isotp.Address(isotp.AddressingMode.Normal_11bits, rxid=self.nodeId+100, txid=self.nodeId)
        self.stack = isotp.CanStack(self.bus, address=addr, error_handler=self.my_error_handler)
        self.inData = {}
        self.isNewInputData = False
        self.outData = {}
        self.newOutData = False

    def my_error_handler(self, error):
        pass
        #logging.warning('IsoTp error happened : %s - %s' % (error.__class__.__name__, str(error)))

    def app(self):
        while 1:
            self.stack.process()  
            #time.sleep(self.stack.sleep_time())
            if self.stack.available():
                payload = self.stack.recv()
                obj = bytes(payload)
                self.inData = pybinn.loads(obj)
                self.isNewInputData = True
            
            #check output data
            if self.newOutData == True:
                self.newOutData = False
                obj = pybinn.dumps(self.outData)
                self.stack.send(bytes(obj))
            time.sleep(0.001)

class GoLinkManager(object):
    
    def __init__(self, nodes):
        self.nodes = nodes
        self.nodeObjects = []
        self.nodeThreads = []

        
    def startNodes(self):
        for node in self.nodes:
            self.nodeObjects.append(GoLinkNode(node))
        for nodeObject in self.nodeObjects:
            self.nodeThreads.append(threading.Thread(target=nodeObject.app))
        for nodeThread in self.nodeThreads:
            nodeThread.start()
            
    def getData(self, nodeId):
        for idx, node in enumerate(self.nodes):
            if node == nodeId:
                return self.nodeObjects[idx].inData
            
    def setData(self, nodeId, inputData):
        for idx, node in enumerate(self.nodes):
            if node == nodeId:
                self.nodeObjects[idx].outData = inputData
                self.nodeObjects[idx].newOutData = True
    
    def isNewData(self, nodeId):
        for idx, node in enumerate(self.nodes):
            if node == nodeId:
                if self.nodeObjects[idx].isNewInputData:
                    self.nodeObjects[idx].isNewInputData = False
                    return True
        return False
            
if __name__ == "__main__":
    POWER_DIST = 2
    MOTOR_DRIVER_LEFT = 4
    MOTOR_DRIVER_RIGHT = 5
    
    systemNodeIds = [POWER_DIST, MOTOR_DRIVER_LEFT, MOTOR_DRIVER_RIGHT]
    man = GoLinkManager(systemNodeIds)
    man.startNodes()
    index = 1
    while 1:
        
        if man.isNewData(MOTOR_DRIVER_LEFT):
            print(man.getData(MOTOR_DRIVER_LEFT), index)
            man.setData(MOTOR_DRIVER_LEFT, {'spr' : int(5)})
            
        index += 1
        #man.setData(MOTOR_DRIVER_LEFT, {'meow2' : index})
        time.sleep(0.05)
        #if man.isNewData(MOTOR_DRIVER_RIGHT):
        #    print(man.getData(MOTOR_DRIVER_RIGHT))

        
        #time.sleep(1)