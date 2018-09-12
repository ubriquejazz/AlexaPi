# AlexaPi and PocketSphinx

This is the client for Amazon's Alexa service, it also includes the solution described in the section 2 of the FAQ of the AlexaPi project:

	https://github.com/alexa-pi/AlexaPi/wiki/Q&A-(FAQ)

### Options

root@localhost:/opt/AlexaPi# ./src/main.py -h
  -h, --help          show this help message and exit
  -s, --silent        automated test mode
  -d, --debug         display debug messages

root@localhost:/opt/AlexaPi# ./Pocket/main.py -h
  -h, --help          show this help message and exit
  -d, --debug         display debug messages
  -g, --grammar       grammar mode (no default)
  -p dir, --path=dir  path where to find the JSGF

root@localhost:/opt/AlexaPi# uname -a
  Linux 4.4.30-xillinux-2.0 #1 SMP PREEMPT Tue Dec 5 11:54:25 IST 2017 armv7l armv7l armv7l GNU/Linux

### Platform

It is intended to run on Xillinux 16.04 (see uname command). These are the paramaters to configure the Zedboard:

cat /etc/opt/AlexaPi/config.yaml 
...
sound:
  input_device: "pulse"
  playback_handler: "vlc"
  output: "pulse"
  output_device: "default"
  ...

triggers:
  platform:
    enabled: true
    voice_confirm: true
    event_type: "oneshot-vad"
    # only for "continuous" event_types
    long_press:
      command: ""
      duration: 10
      audio_file: ""

  pocketsphinx:
    enabled: false
    voice_confirm: true
    phrase: "alexa"
    threshold: 1e-10

event_commands:
  startup: ""
  pre_interaction: ""
  post_interaction: ""
  shutdown: ""

platform:
  # Name of your platform, e.g. raspberrypi, orangepi, desktop
  device: "zedboard"
platforms:
  ...
  desktop:
    min_seconds_to_record: 3
  dummy:
  zedboard:
    min_seconds_to_record: 3
    # GPIO Pin with button connected
    button: 77
    # GPIO Pin for the playback/activity light
    plb_light: 64
    # GPIO Pin for the recording light
    rec_light: 63

More info at

	https://github.com/alexa-pi/AlexaPi/wiki/Configuration-file
