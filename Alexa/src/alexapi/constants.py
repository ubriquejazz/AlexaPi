MAX_VOLUME = 100
MIN_VOLUME = 30

class TYPES(object):
	OTHER = 0
	VOICE = 1

class EVENT_TYPES(object): # pylint: disable=invalid-name
	ONESHOT_VAD = 1
	CONTINUOUS = 2
	CONTINUOUS_VAD = 3

types_vad = [
	EVENT_TYPES.ONESHOT_VAD,
	EVENT_TYPES.CONTINUOUS_VAD,
]

types_continuous = [
	EVENT_TYPES.CONTINUOUS,
	EVENT_TYPES.CONTINUOUS_VAD,
]

class RequestType(object):
	STARTED = 'STARTED'
	INTERRUPTED = 'INTERRUPTED'
	FINISHED = 'FINISHED'
	ERROR = 'ERROR'

	def __init__(self):
		pass

class PlayerActivity(object):
	PLAYING = 'PLAYING'
	PAUSED = 'PAUSED'
	IDLE = 'IDLE'

	def __init__(self):
		pass
