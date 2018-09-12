#!/usr/bin/python
import os
from pocketsphinx.pocketsphinx import Decoder
import logging

logger = logging.getLogger(__name__)

os.environ["PA_ALSA_PLUGHW"] = "1"
import pyaudio

def get_model_path_keyword():
    return "/usr/local/lib/python2.7/dist-packages/pocketsphinx/model"

class PocketKeyword(object):

    AUDIO_CHUNK_SIZE = 1024
    AUDIO_RATE = 16000

    def __init__(self, phrase, threshold, device_index=0):

        self._decoder = None
        self._pa = None
        self._device_no = device_index
        self._phrase = phrase
        self._threshold = float(threshold)

        # PocketSphinx configuration  
        logging.info('Phrase: ' + phrase + ' Threshold: ' + str(threshold))
        ps_config = Decoder.default_config()
        
        # Set recognition model to US
        ps_config.set_string('-hmm', os.path.join(get_model_path_keyword(), 'en-us'))
        ps_config.set_string('-dict', os.path.join(get_model_path_keyword(), 'cmudict-en-us.dict'))
        # Specify recognition key phrase
        ps_config.set_string('-keyphrase', self._phrase)
        ps_config.set_float('-kws_threshold', self._threshold)
        ps_config.set_string('-logfn', '/dev/null')

        # Process audio chunk by chunk. On keyword detected perform action and restart search
        self._decoder = Decoder(ps_config)
        self._pa = pyaudio.PyAudio()

    def _handle_init(self, rate, chunk_size):       
        self._handle = self._pa.open(
            input=True,
            input_device_index=self._device_no,
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            frames_per_buffer=chunk_size
        )

    def _handle_release(self):
        self._handle.stop_stream()
        self._handle.close()

    def _handle_read(self, chunk_size):
        return self._handle.read(chunk_size, exception_on_overflow=False) 

    def getHypothesys(self):

        # init microphone
        self._handle_init(self.AUDIO_RATE, self.AUDIO_CHUNK_SIZE)
        self._decoder.start_utt()

        triggered = False
        while not triggered:
            # Read from microphone and process
            data = self._handle_read(self.AUDIO_CHUNK_SIZE)
            self._decoder.process_raw(data, False, False)

            # best guess from CMU Sphinx STT
            hypothesis = self._decoder.hyp()
            triggered = hypothesis is not None

        # close microphone
        self._handle_release()
        self._decoder.end_utt()
        if triggered:
            return hypothesis.hypstr

class PocketGrammar(object):

    AUDIO_CHUNK_SIZE = 1024
    AUDIO_RATE = 16000
    HMM = 'cmusphinx-5prealpha-en-us-ptm-2.0/'
    DIC = 'dictionary.dic'
    GRAMMAR = 'grammar.jsgf'

    def __init__(self, device_index=0, model_path=None):

        self._decoder = None
        self._pa = None
        self._device_no = device_index
        self._model_path = model_path

        # PocketSphinx configuration  
        logging.info('Grammar file:' + os.path.join(model_path, self.GRAMMAR))
        ps_config = Decoder.default_config()

        # Set recognition model to ...
        ps_config.set_string('-hmm', os.path.join(model_path, self.HMM))
        ps_config.set_string('-dict', os.path.join(model_path, self.DIC))
        ps_config.set_string('-jsgf', os.path.join(model_path, self.GRAMMAR))
        ps_config.set_string('-logfn', '/dev/null')

        # Process audio chunk by chunk. On keyword detected perform action and restart search
        self._decoder = Decoder(ps_config)
        self._pa = pyaudio.PyAudio()

    def _handle_init(self, rate, chunk_size):       
        self._handle = self._pa.open(
            input=True,
            input_device_index=self._device_no,
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            frames_per_buffer=chunk_size
        )

    def _handle_release(self):
        self._handle.stop_stream()
        self._handle.close()

    def _handle_read(self, chunk_size):
        return self._handle.read(chunk_size, exception_on_overflow=False) 

    def getHypothesys(self):

        # init microphone
        self._handle_init(self.AUDIO_RATE, self.AUDIO_CHUNK_SIZE)
        self._decoder.start_utt()

        #  from speech to silence or from silence to speech?
        utteranceStarted = False
        triggered = False
        while not triggered:
            # Read from microphone and process
            data = self._handle_read(self.AUDIO_CHUNK_SIZE)
            self._decoder.process_raw(data, False, False)
            
            # checks for transition from silence to speech.
            inSpeech = self._decoder.get_in_speech() 
            if inSpeech and not utteranceStarted:
                utteranceStarted = True
                logging.debug("Silence")

            # checks for the transition from speech to silence           
            if not inSpeech and utteranceStarted:   
                hypothesis = self._decoder.hyp()
                triggered = hypothesis is not None

        # close microphone
        self._handle_release()
        self._decoder.end_utt()
        if triggered:
            return hypothesis.hypstr
