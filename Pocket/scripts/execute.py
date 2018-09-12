import tempfile
import subprocess
import time
import threading
import logging

logger = logging.getLogger(__name__)

const_setup = '''\
echo 63 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio63/direction
echo 64 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio64/direction
echo 78 >/sys/class/gpio/export
echo in >/sys/class/gpio/gpio78/direction
echo 77 >/sys/class/gpio/export
echo in >/sys/class/gpio/gpio77/direction
'''
const_cleanup = '''\
echo 63 >/sys/class/gpio/unexport
echo 64 >/sys/class/gpio/unexport
echo 78 >/sys/class/gpio/unexport
echo 77 >/sys/class/gpio/unexport
'''

def run_script(script):
    with tempfile.NamedTemporaryFile() as scriptfile:
        scriptfile.write(script)
        scriptfile.flush()
        return subprocess.check_output(['/bin/bash', scriptfile.name])

if __name__ == '__main__':
	run_script(const_setup)
	pressed = run_script('cat /sys/class/gpio/gpio77/value')
	while pressed[0] == '0':
		pressed = run_script('cat /sys/class/gpio/gpio77/value')
	
	if pressed[0] == '1':
		for _ in range(0, 5):
	        time.sleep(.1)
	        run_script('echo 0 >/sys/class/gpio/gpio64/value')
	        time.sleep(.1)
	        run_script('echo 1 >/sys/class/gpio/gpio64/value')

# end file