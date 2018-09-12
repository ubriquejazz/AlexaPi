#! /usr/bin/env python
import RPi.GPIO as GPIO
import pyttsx, time
import os, sys
import random
import argparse

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--testsize',
        dest="testsize",
        type=int,
        default=1,
        help="number of repetions")
parser.add_argument('-g', '--grammar',
        dest="grammar",
        action="store_true",
        default=False,
        help="grammar mode (no default)")
parser.add_argument('-s', '--silent',
		dest="silent",
		action="store_true",
		default=False,
		help="start without saying hello")

cmdargs = parser.parse_args()
grammar = cmdargs.grammar
silent = cmdargs.silent
testsize = cmdargs.testsize
engine = pyttsx.init()

command={}
command['weather'] = ["Alexa, how is the weather in Glasgow", 8]
command['siri'] = ["Alexa, who is Siri", 5]
command['joke'] = ["Alexa, tell me a joke", 5]
command['music'] = ["Alexa, play some music", 5]
command['alarm'] = ["Alexa, set an alarm for seven a.m.", 5]
command['time'] = ["Alexa, what time is it?", 5]
command['timer'] = ["Alexa, set a timer for 2 minutes", 5]

action={}
action['on'] = "Turn on"
action['off'] = "Turn off"
household={}
household['kettle'] = "The kettle"
household['lamp'] = "The lamp"

def setup(grammar_mode=True):
	GPIO.setmode(GPIO.BCM)
	if grammar_mode:
		#setup_input() - monitoring relay (lamp)
		GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	else:
		#setup_output() - button simulation (alexapi)
		GPIO.setup(4, GPIO.OUT)
		GPIO.output(4, GPIO.LOW)

def cleanup(grammar_mode=True):
	if grammar_mode:
		GPIO.cleanup()
	else:
		GPIO.output(4, GPIO.LOW)
		GPIO.cleanup()

def push_button(delay):
	print 'Button pressed'
	GPIO.output(4, GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(4, GPIO.LOW)

def check_keyword(delay):
	print 'Playing response for', delay, 's'
	time.sleep(delay)
	raw_input("Press Enter to continue...")
	return True

def check_grammar(onOrOff):
	retVal = GPIO.input(4)
	ideal = 1 if (onOrOff == 'on') else 0
	print 'set', onOrOff, '; read', retVal
	return retVal == ideal

def runMain_grammar():
	count = 0
	for tst in range(0, testsize):
		print '******', tst, '******'
		for key in action:
			time.sleep(1)
			array = [action[key], household['lamp']]
			phrase = " ".join(array)
			engine.say(phrase)
			engine.runAndWait()
			if check_grammar(key):
				count += 1
	# results
	print '******', count,'/', len(action)*testsize, '******'

def runMain_keyword():
	count = 0
	for tst in range(0, testsize):
		print '******', tst, '******'
		key = random.choice(command.keys())
		if silent:
			push_button(0.5)
			#for key in command:
		time.sleep(3)
		print command[key][0]
		engine.say(command[key][0])
		engine.runAndWait()
		#time.sleep(5)
		if check_keyword(command[key][1]):
			count += 1
	# results
	print '******', count,'/', testsize, '******'

if __name__ == '__main__':

	engine.say("Welcome")
	engine.runAndWait()
	setup (grammar)
	if grammar:
		runMain_grammar()
	else:
		runMain_keyword()
	cleanup(grammar)

