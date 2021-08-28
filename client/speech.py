#!/usr/bin/env python
from naoqi import *
import time


# ROBOT_IP = 'localhost'

#with open("readfile.txt") as f:
#    content = f.readlines()
#content = [x.strip() for x in content]

class SpeechRecoModule(ALModule):
    """ A module to use speech recognition """
    def __init__(self, name):
        ALModule.__init__(self, name)
        try:
            self.asr = ALProxy("ALSpeechRecognition")
	    self.asr.setLanguage('Czech')
 	    print 'SpeechRecognition nastavena'
        except Exception as e:
            self.asr = None
        self.memory = ALProxy("ALMemory")
	print 'Memory nastavena'
	global posliMiTo
	global treshold


    def onLoad(self):
        from threading import Lock
        self.bIsRunning = False
        self.mutex = Lock()
        self.hasPushed = False
        self.hasSubscribed = False
        self.BIND_PYTHON(self.getName(), "onWordRecognized")
        self.posliMiTo=""
        self.treshold=0


    def onUnload(self):
        from threading import Lock
        self.mutex.acquire()
        try:
            if (self.bIsRunning):
                if (self.hasSubscribed):
                    self.memory.unsubscribeToEvent("WordRecognized", self.getName())
                if (self.hasPushed and self.asr):
                    self.asr.popContexts()
        except RuntimeError, e:
            self.mutex.release()
            raise e
        self.bIsRunning = False;
        self.mutex.release()

    def onInput_onStart(self):
        from threading import Lock
        self.mutex.acquire()
        if(self.bIsRunning):
            self.mutex.release()
            return
        self.bIsRunning = True
        try:
            if self.asr:
                self.asr.setVisualExpression(True)
                self.asr.pushContexts()
            self.hasPushed = True
            if self.asr:
                with open("readfile.txt") as f:
                  content = f.readlines()
                content = [x.strip() for x in content]
                self.asr.setVocabulary(content, False )
            print 'Slovna zasoba nastavena'
            self.memory.subscribeToEvent("WordRecognized", self.getName(), "onWordRecognized")
            self.hasSubscribed = True
        except RuntimeError, e:
            self.mutex.release()
            self.onUnload()
            raise e
        self.mutex.release()



    def onWordRecognized(self, key, value, message):
		print 'word recognized'

		if(len(value) > 1 and value[1] >= 0.1):
			print 'recognized the word :', value[0]
			print 'treshold :', value[1]
		        self.posliMiTo = value[0]
		        self.treshold = value[1]
		else:
			print 'unsifficient threshold'

# global broker; broker = ALBroker("pythonBroker","0.0.0.0", 0, ROBOT_IP, 9559)
# global pythonSpeechModule;
# pythonSpeechModule = SpeechRecoModule('pythonSpeechModule')
# pythonSpeechModule.onLoad()
# pythonSpeechModule.onInput_onStart()
# time.sleep(5)
# pythonSpeechModule.onUnload()