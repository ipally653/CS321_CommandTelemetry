from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
import serial
import keyboard
import sys
import time
sys.path.append('../')

class Radio:
    def __init__(self):
        self.serialPort = "COM3"
        self.device = XBeeDevice(self.serialPort,9600)
        self.remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string("0013A2004068CC5D")) # "0013A20040XXXXXX"
        self.callback = None;

    def __repr__(self):
        return "Xbee Device at Port".format(self.serialPort,self.device.is_open())

    def __str__(self):
        return "Xbee Device at Port".format(self.serialPort,self.device.is_open())

    def openConnection(self):
        if (self.device != None and self.device.is_open() == False):
            self.device.open()

    def closeConnection(self):
        if (self.device != None and self.device.is_open()):
            self.device.close()

    def send(self, data):
        try:
            self.device.send_data_async(self.remote_device,data)
        except(KeyboardInterrupt):
            print("something went wrong when sending data")

    def data_received_callback(xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        f = open("Balloon_Data.txt", "a")
        f.write(data + "\n") #writing data to text file
        print("Received data from %s: %s" % (address, data))

	# opens the XBEE device and sets the receive call back
	# parameters
    def setUP(self):
        self.openConnection()
        self.callback = Radio.data_received_callback
        self.device.add_data_received_callback(self.callback)

    #terminate XBEE connection and delete callback
    def terminate(self):
        self.device.del_data_received_callback(self.callback)
        self.closeConnection()


radio = Radio()
radio.setUP() #essentially sets up and runs receiving data on separate thread

while(True):
    if(keyboard.is_pressed('ctrl+space')): #if Ctrl and space keys are pressed simultaneously, the cut command will be sent
        radio.send("cut")
        print("Cut command sent")
        time.sleep(0.5)
    if(keyboard.press('`')):
        break
radio.terminate()
