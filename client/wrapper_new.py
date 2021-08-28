#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket   #for sockets
import sys  #for exit
import getopt, argparse
import time
from naoqi import *
from multim import *
from speech import *
from client import *


import speech

# https://pymotw.com/2/argparse/

tts_speed=85  #default tts speed
gesture = 2

parser = argparse.ArgumentParser(description='Welcome in help for NAO wrapper')

parser.add_argument('-NaoIP', action='store', dest='ip', help='IP address of robot NAO')
parser.add_argument('-HostIP', action='store', dest='host_ip', help='IP address of DM')
parser.add_argument('-PORT', type=int, action="store", dest='port', help='PORT')
parser.add_argument('-LAN', action='store', dest='language', help='Language used for speech recognition and synthetic modul')
parser.add_argument('-TTSspeed',type=int, action='store', dest='tts_speed', help='Speed of TTS from 0 to 100')
parser.add_argument('-Gesture',type=int, action='store', dest='gesture', help='0 - no gestures, 1 - no random, predefined gestures, 2 - random + predefined')
parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
results = parser.parse_args()
print 'IP address =', results.ip
print 'PORT       =', results.port
print 'Host IP    =', results.host_ip
print 'Language    =', results.language
print 'TTS_speed =', results.tts_speed
print 'Gesture = ', results.gesture
prem = results.language

gesture =results.gesture
tts_speed =results.tts_speed

def upperfirst(prem):
    return prem[0].upper() + prem[1:].lower()
nao_lang = upperfirst(prem)

global content
open("readfile.txt","w").close()

with open("init.txt") as f:
	content3 = f.readlines()
content3 = [x.strip() for x in content3]
	
with open("readfile.txt", 'a') as file_handler1:
	# file_handler.write("\n")
	for item in content3:
		file_handler1.write("{}\n".format(item))


		
clientclass = ClientClass('ClientClass')		
		
		
#ROZPOZNAVAC
########################################################

ROBOT_IP = results.ip

# global broker; broker = ALBroker("pythonBroker","0.0.0.0", 0, ROBOT_IP, 9559)
# global pythonSpeechModule;
# pythonSpeechModule = SpeechRecoModule('pythonSpeechModule')

global broker; broker = ALBroker("pythonBroker","0.0.0.0", 0, ROBOT_IP, 9559)
global pythonSpeechModule;
pythonSpeechModule = SpeechRecoModule('pythonSpeechModule')

try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'

port = results.port
BUFFER_SIZE = 4096
host = results.host_ip

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
 
#Connect to remote server
s.connect((remote_ip , port))

IPcka = results.ip
PORTik = 9559
# apx = ALProxy("ALAnimatedSpeech", ROBOT_IP, PORTik)

try:
    tts = ALProxy("ALTextToSpeech", ROBOT_IP, PORTik)
except Exception,e:
    print "Could not create proxy to ALTextToSpeech"
    print "Error was: ",e
    sys.exit()
## set the language of the synthesis engine to English:
tts.setLanguage(nao_lang)

##gain applied to the signal. The default value - 1.0.
tts.setVolume(1.0)

## modifications of the voice’s speed. The default value - 100.
#tts.setParameter("speed", 85)
tts.setParameter("speed", tts_speed)
 
try :
    #Set the whole string
    s.send("Begin")
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()
 
print 'Message send successfully'

############
def mysend(msg):
    totalsent = 0
    MSGLEN = len(msg)
    print MSGLEN
    while totalsent < MSGLEN:
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

############
def myreceive(msg):
    msg = b''
    MSGLEN = len(msg)
    while len(msg) < MSGLEN:
        chunk = s.recv(MSGLEN-len(msg))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        msg = msg + chunk
    return msg

############ PARSE AddGramar
def parse_gramar(msg):
	global premenna
	print "Prijal som AddGramar a odpovedam Ok"
	try:
		s.send("Ok                                     ")
	except:
		print "Send failed"
		sys.exit()
        
	l1 = []
	pokr = True
	while pokr:
		while msg.startswith(" "):
			msg = msg[1:]
		pos = 0
		for c in msg:
			if c == " ":
				# print(msg[:pos])
				l1.append(msg[:pos])
				msg = msg[pos+1:]
				break
			if c == '\t':
				# print(msg[:pos])
				l1.append(msg[:pos])
				msg = msg[pos+1:]
				break
			pos += 1
		else:
			l1.append(msg[:pos])
			# print(msg[:pos])
			pokr = False
			premenna = l1[2]
			print premenna
	
	jedem = True
	pomoc = "";
	while jedem:
		for c in premenna:
			if c != ".":
				pomoc += c
			else:
				print pomoc
				break
			jedem = False
	adresa = pomoc+".nao_grammar"
	
	# otovrim subor
	with open(adresa) as f:
		content2 = f.readlines()
	content2 = [x.strip() for x in content2]
	print content2
	
	with open("readfile.txt", 'a') as file_handler:
		# file_handler.write("\n")
		for item in content2:
			file_handler.write("{}\n".format(item))


############ PARSE NewGroup
def parse_newGroup():
	print "Prijal som NewGroup a odovedam Ok"
	open("readfile.txt","w").close()

        try:
		s.send("Ok                                      ")
	except:
		print "Send failed"
		sys.exit()

	with open("init.txt", "w") as z:
		for item in content3:
			z.write("{}\n".format(item))

############ PARSE LoadGroup
def parse_loadGroup():
    print "Prijal som LoadGroup a odovedam Ok"
    try:
        s.send("Ok                                        ")
    except:
        print "Send failed"
        sys.exit()

############ PARSE Synt
def parse_synt(msg):
    try:
        s.send("Ok                                        ") 
    except:
        print "Send failed"
        sys.exit()
        
    print "Ok - prijal som Synt"
    l1 = []
    try:
        start = msg.index( "text " ) + len( "text " )
        end = msg.index( ":bargein", start )
        to_say = msg[start:end]
	# apx.say(multimodal(to_say,ROBOT_IP,PORTik))
	# multimodal(to_say,ROBOT_IP,PORTik)
	multim(ROBOT_IP, PORTik, ["/var/persistent/home/nao/First.txt","/var/persistent/home/nao/Second.txt"], to_say, gesture)
	# tts.say(to_say)
        l1.append(msg[start:end])
    except ValueError:
        return "Error in Value"
    	sys.exit()
            
############ PARSE Inform
def parse_inform(msg):
    try:
        s.send("Ok                                        ") 
    except:
        print "Send failed"
        sys.exit()
        
    print "Ok - prijal som Inform"
    l1 = []
    try:
        start = msg.index( "src " ) + len( "src " )
        end = len(msg)
        to_say = msg[start:end]
      	address = "/home/nao/"
        filetoplay = address + to_say
        print filetoplay
        aup = ALProxy("ALAudioPlayer", "127.0.0.1", 9559)
        fileId = aup.loadFile(filetoplay)
        aup.play(fileId)
        l1.append(msg[start:end])
    except ValueError:
        return "Error in Value"
    	sys.exit()
      
############ PARSE Utterance
def parse_utt():
	pythonSpeechModule.onLoad()
	pythonSpeechModule.onInput_onStart()
	#time.sleep(5)
	
	
        # while(hasattr(speech, 'posliMiTo')==False):
        # print '.'
        counter =1
        while(len(pythonSpeechModule.posliMiTo)==0):
                                      ++counter
                                      if counter > 100:
                                         print '.',
                                         counter=1


        pythonSpeechModule.onUnload()

        print "Prijal som Utterance"
	print pythonSpeechModule.posliMiTo
	# print speech.treshold
	# odpoved = ":utt "+pythonSpeechModule.posliMiTo+"	:conf "+str(pythonSpeechModule.treshold)+ "	:noinput 0	:semantic"
	odpoved = ":utt "+pythonSpeechModule.posliMiTo+"	:conf 0.9	:noinput 0	:semantic"

	try:
		s.send(odpoved)
	except:
		print "Send failed"
		sys.exit()
        
def main(s):
   
   clientclass.onLoad()
   
    try:
      #s.settimeout(0.1)        
      while True:
          #Now receive data
          msg = s.recv(4096)
          print msg
  
          if 'Synt' in msg:
              parse_synt(msg)
  	    # time.sleep(1)
          elif 'NewGroup' in msg:
              parse_newGroup()
          elif 'inform' in msg:
              parse_inform(msg)    
          elif 'AddGram' in msg:
              parse_gramar(msg)
          elif 'LoadGroup' in msg:
              parse_loadGroup()
          elif 'ask' in msg:
              parse_utt()
		  elif 'C' in message: 	  
			  clientclass.Operation(message)
			  
              print "Maj sa"
              s.close()
              sys.exit()
              print 'Koniec dialogu'
    except KeyboardInterrupt:
        print "Bye"
        pythonSpeechModule.onUnload()
        sys.exit()      
            
while True:
    main(s)
