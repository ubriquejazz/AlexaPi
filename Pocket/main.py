#!/usr/bin/python
import os, sys, traceback
import logging, coloredlogs
import optparse

# Get arguments
parser = optparse.OptionParser()
parser.add_option('-d', '--debug',
        dest="debug",
        action="store_true",
        default=False,
        help="display debug messages")
parser.add_option('-g', '--grammar',
        dest="grammar",
        action="store_true",
        default=False,
        help="grammar mode (no default)")
parser.add_option("-p", "--path", 
        dest="filename",
        help="path where to find the JSGF", 
        metavar="dir")
cmdopts, cmdargs = parser.parse_args()
debug = cmdopts.debug
grammar = cmdopts.grammar
filename = cmdopts.filename

if grammar and not cmdopts.filename:   # if filename is not given
    parser.error('Grammar file not given')

def get_model_path_grammar():
    cwd = os.getcwd()
    return os.path.join(cwd, 'Pocket/model')

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
coloredlogs.DEFAULT_FIELD_STYLES = {
    'hostname': {'color': 'magenta'},
    'levelname': {'color': 'magenta', 'bold': True},
    'asctime': {'color': 'green'}
}
coloredlogs.DEFAULT_LEVEL_STYLES = {
    'info': {'color': 'blue'},
    'critical': {'color': 'red', 'bold': True},
    'error': {'color': 'red'},
    'debug': {'color': 'green'},
    'warning': {'color': 'yellow'}
}
coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

if debug:
    log_level = logging.DEBUG
else:
    log_level = logging.getLevelName('INFO')

pocket_logger = logging.getLogger('pocket')
pocket_logger.setLevel(log_level)
coloredlogs.install(level=log_level)
logger = logging.getLogger(__name__)

from src.pocket import PocketKeyword, PocketGrammar
from src.devices import Roomba, Lamp

os.environ["PA_ALSA_PLUGHW"] = "1"
import pyaudio

def get_model_path():
    return "/usr/local/lib/python2.7/dist-packages/pocketsphinx/model"

class ConfigurationException(Exception):
    pass

class DeviceInfo(object):

    def __init__(self):
        self._pa = pyaudio.PyAudio()

    def get_device_list(self, input_only=False):

        device_list = []
        for i in range(self._pa.get_device_count()):
            if (not input_only) or (input_only and self._pa.get_device_info_by_index(i)['maxInputChannels'] > 0):
                device_list.append(self._pa.get_device_info_by_index(i)['name'])

        return device_list

    def get_device_index(self, name):
        if not name:
            return None

        return self.get_device_list().index(name)

    def __del__(self):
        self._pa.terminate()
 
if __name__ == '__main__':
   
    device_info = DeviceInfo()
    input_devices = device_info.get_device_list(True)
    pulseaudio_index = device_info.get_device_index("pulse")
    lamp = None
    count = 0
    if grammar:
        pocket = PocketGrammar(pulseaudio_index, filename)
        lamp = Lamp()
    else:
        pocket = PocketKeyword("alexa", 1e-50, pulseaudio_index)

    while True:
        try:
            # We can set debug here to see what the decoder thinks
            command = pocket.getHypothesys()
            logging.info('I just heard you say "{}"'.format(command))
            command = command.lower().replace('the', '')
            if command.startswith('turn'):
                onOrOff = command.split()[1]
                deviceName = ''.join(command.split()[2:])
                if deviceName == 'lamp':
                    lamp.turn(onOrOff)
            # number of transactions
            count += 1
        except (KeyboardInterrupt, SystemExit):
            print '******', count, '******'
            sys.exit()

