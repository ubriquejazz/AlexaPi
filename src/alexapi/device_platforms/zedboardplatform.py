import tempfile
import subprocess
import time
import threading
import logging
from .baseplatform import BasePlatform

logger = logging.getLogger(__name__)

const_setup = '''\
echo 63 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio63/direction
echo 64 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio64/direction
echo 77 >/sys/class/gpio/export
echo in >/sys/class/gpio/gpio77/direction
'''
const_cleanup = '''\
echo 63 >/sys/class/gpio/unexport
echo 64 >/sys/class/gpio/unexport
echo 77 >/sys/class/gpio/unexport
'''

def run_script(script):
    with tempfile.NamedTemporaryFile() as scriptfile:
        scriptfile.write(script)
        scriptfile.flush()
        return subprocess.check_output(['/bin/bash', scriptfile.name])

class ZedboardPlatform(BasePlatform):

	def __init__(self, config, silent):
		super(ZedboardPlatform, self).__init__(config, silent, 'zedboard')
		self.trigger_thread = None
		self.started = 0

	def setup(self):
		logging.debug("setup")
		run_script(const_setup)
		if self._silent:
			run_script('echo 78 >/sys/class/gpio/export')
			run_script('echo in >/sys/class/gpio/gpio78/direction')
	
	def cleanup(self):
		logging.debug("cleanup")
		run_script(const_cleanup)
		if self._silent:
			run_script('echo 78 >/sys/class/gpio/unexport')

	def indicate_failure(self):
		logger.info("setup_failure")
		for _ in range(0, 5):
			time.sleep(.1)
			run_script('echo 0 >/sys/class/gpio/gpio63/value')
			time.sleep(.1)
			run_script('echo 1 >/sys/class/gpio/gpio63/value')

	def indicate_success(self):
		logger.info("setup_complete")
		for _ in range(0, 5):
			time.sleep(.1)
			run_script('echo 0 >/sys/class/gpio/gpio64/value')
			time.sleep(.1)
			run_script('echo 1 >/sys/class/gpio/gpio64/value')

	def indicate_recording(self, state=True):
		logger.info("indicate_recording_on %s", state)
		if state:
			run_script('echo 1 >/sys/class/gpio/gpio63/value')
		else:
			run_script('echo 0 >/sys/class/gpio/gpio63/value')

	def indicate_playback(self, state=True):
		logger.info("indicate_playback %s", state)
		if state:
			run_script('echo 1 >/sys/class/gpio/gpio64/value')
		else:
			run_script('echo 0 >/sys/class/gpio/gpio64/value')

	def indicate_processing(self, state=True):
		logger.info("indicate_processing %s", state)
		if state:
			run_script('echo 1 >/sys/class/gpio/gpio63/value')
			run_script('echo 1 >/sys/class/gpio/gpio64/value')
		else:
			run_script('echo 0 >/sys/class/gpio/gpio63/value')
			run_script('echo 0 >/sys/class/gpio/gpio64/value')

	def after_setup(self, trigger_callback=None): 
		logger.info("after_setup")
		self._trigger_callback = trigger_callback
		if self._trigger_callback:
			# threaded detection of button press
			self.trigger_thread = DesktopPlatformTriggerThread(self, trigger_callback)
			self.trigger_thread.setDaemon(True)
			self.trigger_thread.start()

	def force_recording(self):
		return  time.time() - self.started < self._pconfig['min_seconds_to_record']

class DesktopPlatformTriggerThread(threading.Thread):
	def __init__(self, platform, trigger_callback):
		threading.Thread.__init__(self)
		self.platform = platform
		self._trigger_callback = trigger_callback
		self.should_run = True

	def stop(self):
		self.should_run = False

	def run(self):
		while self.should_run:
			if self.platform._silent:
				pressed = run_script('cat /sys/class/gpio/gpio78/value')
				while pressed[0] == '0':
					pressed = run_script('cat /sys/class/gpio/gpio78/value')	
			else:
				pressed = run_script('cat /sys/class/gpio/gpio77/value')
				while pressed[0] == '0':
					pressed = run_script('cat /sys/class/gpio/gpio77/value')
			# 					
			self.platform.started = time.time()
			if self._trigger_callback:
				self._trigger_callback(self.platform.force_recording)

