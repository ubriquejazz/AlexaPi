import os, tempfile
import subprocess
import logging

logger = logging.getLogger(__name__)

const_setup = '''\
echo 78 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio78/direction
echo 61 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio61/direction
echo 77 >/sys/class/gpio/export
echo in >/sys/class/gpio/gpio77/direction
'''
const_cleanup = '''\
echo 64 >/sys/class/gpio/unexport
echo 78 >/sys/class/gpio/unexport
echo 77 >/sys/class/gpio/unexport
'''

class ArduinoIR():

    def __init__(self):
        pass

    def listSerialPorts(self):
        if os.name == 'posix':
            self.available = []
            try:
                self.s = serial.Serial('/dev/ttyACM0', 9600)
                self.available.append('/dev/ttyACM0')
                self.s.close()
            except serial.SerialException:
                pass
            if len(self.available) == 0:
                raise Exception
            return self.available

    def executeArduinoIRCommand(self, command):
        try:
            self.serialPortsArray = []
            self.serialPortsArray = self.listSerialPorts()
        except:
            print "Is the arduino plugged in?"
        if len(self.serialPortsArray) == 1:
            self.ser = serial.Serial(self.serialPortsArray[0], timeout=5)
            self.ser.write(command)  # write a string
            self.response = self.ser.readline()
            if self.response.endswith("is an unknown command"):
                print "The Arduino didn't understand our command"
                raise Exception
            print(self.response)
            self.ser.close()

class Zedboard():

    def __init__(self):
        logging.debug("Zedboard created")
        self.run_script(const_setup)

    def run_script(self, script):
        with tempfile.NamedTemporaryFile() as scriptfile:
            scriptfile.write(script)
            scriptfile.flush()
            return subprocess.check_output(['/bin/bash', scriptfile.name])

    def __del__(self):
        logging.debug("Zedboard deleted")
        self.run_script(const_cleanup)

class Roomba():

    def __init__(self):
        self.arduinoIR = ArduinoIR()

    def turn(self, onOrOff):
        if onOrOff == 'on':
            self.turnOn()
        if onOrOff == 'off':
            self.turnOff()

    def turnOn(self):
        self.arduinoIR.executeArduinoIRCommand('turn on')

    def turnOff(self):
	   self.arduinoIR.executeArduinoIRCommand('turn off')

class Lamp():

    def __init__(self):
        self.zedboard = Zedboard()

    def turn(self, onOrOff):
        if onOrOff == 'on':
            self.turnOn()
        if onOrOff == 'off':
            self.turnOff()

    def turnOff(self):
        logger.info("Lamp turned off")
        self.zedboard.run_script('echo 1 >/sys/class/gpio/gpio78/value')
        self.zedboard.run_script('echo 0 >/sys/class/gpio/gpio61/value')

    def turnOn(self):
        logger.info("Lamp turned on")
        self.zedboard.run_script('echo 0 >/sys/class/gpio/gpio78/value')
        self.zedboard.run_script('echo 1 >/sys/class/gpio/gpio61/value')

# end file