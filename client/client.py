import socket
import time
import StringIO
import thread
import sys       
import almath   
import time     
import re
import getopt, argparse

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# <-----------------------------------------------> 
PARSE  = 0	# Use parser

HOST = '147.232.158.23'  # API ENTRYPOINT
URL = 'Naocloud-env-4.ekud3empzi.eu-west-2.elasticbeanstalk.com'
TCP_PORT = 65432    # control port num
MSGLEN = 1024       # Standard max lenght of message
# <-----------------------------------------------> 

COMMAND_WAKEUP = 'WAKEUP'
COMMAND_REST = 'REST'
COMMAND_FORWARD = 'FORWARD'
COMMAND_BACK = 'BACK'
COMMAND_LEFT = 'LEFT'
COMMAND_RIGHT = 'RIGHT'
COMMAND_STOP = 'STOP'
COMMAND_TURNLEFT = 'TURNLEFT'
COMMAND_TURNRIGHT = 'TURNRIGHT'
COMMAND_DISCONNECT = 'DISCONNECT'

COMMAND_HEADYAW = 'HEADYAW'     
COMMAND_HEADPITCH = 'HEADPITCH'

COMMAND_SENSOR = 'SENSOR'

COMMAND_ARMREST = 'ARMREST' 
COMMAND_LARMOPEN = 'LARMOPEN'
COMMAND_LARMCLOSE = 'LARMCLOSE'
COMMAND_LARMUP = 'LARMUP'
COMMAND_LARMDOWN = 'LARMDOWN'
COMMAND_RARMOPEN = 'RARMOPEN'
COMMAND_RARMCLOSE = 'RARMCLOSE'
COMMAND_RARMUP = 'RARMUP'
COMMAND_RARMDOWN = 'RARMDOWN'

COMMAND_SAY = 'SAY'

COMMAND_POSTURE_STAND = 'POSTURE_STAND'                    
COMMAND_POSTURE_MOVEINIT = 'POSTURE_STANDINIT'             
COMMAND_POSTURE_STANDZERO = 'POSTURE_STANDZERO'            
COMMAND_POSTURE_CROUCH = 'POSTURE_CROUCH'                
COMMAND_POSTURE_SIT = 'POSTURE_SIT'                            
COMMAND_POSTURE_SITRELAX = 'POSTURE_SITRELAX'            
COMMAND_POSTURE_LYINGBELLY = 'POSTURE_LYINGBELLY'        
COMMAND_POSTURE_LYINGBACK = 'POSTURE_LYINGBACK'            

COMMAND_POSTURE_RECORD = 'POSTURE_RECORD'                
COMMAND_POSTURE_RECORD_STOP = 'POSTURE_RECORD_STOP'        
COMMAND_POSTURE_CUSTOMER = 'POSTURE_CUSTOMER'            
COMMAND_POSTURE_DELETE = 'POSTURE_DELETE'                
                                                 
COMMAND_VIDEO_SWITCH_CAMARA = 'SWITCH_CAMERA'            

# <------------------------------------------------------------->
# flag       
SENSOR_FLAG  = False        
POSTURE_RECORD_FLAG = False    
# <------------------------------------------------------------->
if PARSE == 1:
	parser = argparse.ArgumentParser(description='Welcome in help for NAO client wrapper')
	parser.add_argument('-NaoIP', action='store', dest='ip', help='IP address of Cloud server')
	parser.add_argument('-NaoPort', action='store', dest='port', help='Application port')
	parser.add_argument('-CloudURL', action='store', dest='url', help='URL of Cloud')
	res = parser.parse_args()
	HOST = res.ip
	TCP_PORT = res.port
	URL = url
	
class clientsocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send_str_data(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
            self.sock.send('\n')

    def recieve_str_data(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd,2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            if '\n' in chunk: break
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)
        
    def close(self):
        self.sock.close()    
    pass

class ClientClass():

    def onLoad(self):
        #put initialization code here
        self.POSTURE_CHANGE_SPEED = 0.8
        self.posture_list = {}
        self.posture_value = {}

        self.sock = clientsocket()
        
        self.tts = ALProxy("ALTextToSpeech",'127.0.0.1',9559)
        #self.tts.setLanguage("English")
        self.motion = ALProxy("ALMotion",'127.0.0.1',9559)
        self.posture = ALProxy("ALRobotPosture",'127.0.0.1',9559)
        self.memory = ALProxy("ALMemory",'127.0.0.1',9559)
        self.battery = ALProxy("ALBattery",'127.0.0.1',9559)
        self.sonar = ALProxy("ALSonar",'127.0.0.1',9559)
        self.leds = ALProxy("ALLeds",'127.0.0.1',9559)
        pass

    def onUnload(self):
        #put clean-up code here
        self.sock.close()
        self.sock = None
        self.tts = self.motion = self.memory = self.battery = self.autonomous = self.posture = self.sonar = None
        pass

    def Operation(self, command,arg=''):    
        ok=''
        if command == COMMAND_WAKEUP:                            # wakeup
            ok=self.motion.post.wakeUp()
        elif command == COMMAND_REST:                            # rest
            ok=self.motion.post.rest()
        elif command == COMMAND_FORWARD:                        # forward
            ok=self.mymoveinit()
            ok=self.motion.move(0.1, 0, 0) 
        elif command == COMMAND_BACK:                            # back
            ok=self.mymoveinit()
            ok=self.motion.move(-0.1, 0, 0)
        elif command == COMMAND_LEFT:                            # left
            ok=self.mymoveinit()
            ok=self.motion.move(0, 0.1, 0)
        elif command == COMMAND_RIGHT:                            # right
            ok=self.mymoveinit()
            ok=self.motion.move(0, -0.1, 0)
        elif command == COMMAND_STOP:                            # stop
            ok=self.motion.stopMove()
        elif command == COMMAND_TURNLEFT:                        # turn left
            ok=self.mymoveinit()
            ok=self.motion.move(0, 0, 0.3)
        elif command == COMMAND_TURNRIGHT:                        # turn right
            ok=self.mymoveinit()
            ok=self.motion.move(0, 0, -0.3)
        elif command == COMMAND_DISCONNECT:                        # disconnect
            ok=self.motion.rest()
        elif command == COMMAND_HEADYAW:                        # head yaw
            angles = (int(arg) - 50) * 2
            self.motion.setStiffnesses("Head", 1.0)
            ok=self.motion.setAngles("HeadYaw", angles * almath.TO_RAD, 0.2)
        elif command == COMMAND_HEADPITCH:                        # head pitch

            angles = (int(arg) - 50)
            self.motion.setStiffnesses("Head", 1.0)
            ok=self.motion.setAngles("HeadPitch", angles * almath.TO_RAD, 0.2)
        elif command == COMMAND_SENSOR:                            # sensor
            global SENSOR_FLAG
            if SENSOR_FLAG == False:
                SENSOR_FLAG = True
                thread.start_new_thread(self.sensor, (0.5,)) # 2nd arg must be a tuple
            else:
                SENSOR_FLAG = False  
        elif command == COMMAND_ARMREST:                        # arm rest
            ok=self.LArmMoveInit()
            ok=self.RArmMoveInit()
        elif command == COMMAND_LARMOPEN:                        # left hand open
            ok=self.motion.post.openHand("LHand")
        elif command == COMMAND_LARMCLOSE:                        # left hand close
            ok=self.motion.post.closeHand("LHand")
        elif command == COMMAND_RARMOPEN:                        # Right hand open
            ok=self.motion.post.openHand("RHand")
        elif command == COMMAND_RARMCLOSE:                        # Right hand close
            ok=self.motion.post.closeHand("RHand")
        elif command == COMMAND_LARMUP:                            # left arm up
            self.LArmUp()
        elif command == COMMAND_LARMDOWN:                        # left arm down
            self.LArmMoveInit()
        elif command == COMMAND_RARMUP:                            # right arm up
            ok=self.RArmUp()
        elif command == COMMAND_RARMDOWN:                        # right arm down
            ok=self.RArmMoveInit()
        elif command == COMMAND_SAY:                            # say

            print('say ' + arg)
            self.tts.say(arg)
            #ok=thread.start_new_thread(self.mysay, (messages,))
        elif command == COMMAND_POSTURE_STAND:                    # posture - stand
            ok=self.posture.post.goToPosture("Stand", 1.0)
           
        elif command == COMMAND_POSTURE_STANDZERO:                # posture - stand zero
            ok=self.posture.post.goToPosture("StandZero", self.POSTURE_CHANGE_SPEED)
        elif command == COMMAND_POSTURE_MOVEINIT:                # posture - move init / stand init
            ok=self.posture.post.goToPosture("StandInit", self.POSTURE_CHANGE_SPEED)
        elif command == COMMAND_POSTURE_CROUCH:                    # posture - Crouch
            ok=self.posture.post.goToPosture("Crouch", self.POSTURE_CHANGE_SPEED)
        elif command == COMMAND_POSTURE_SIT:                    # posture - sit
            ok=self.posture.post.goToPosture("Sit", self.POSTURE_CHANGE_SPEED)
        elif command == COMMAND_POSTURE_SITRELAX:                # posture - sit relax
            ok=self.posture.post.goToPosture("SitRelax", self.POSTURE_CHANGE_SPEED)
        elif command == COMMAND_POSTURE_LYINGBELLY:                # posture - lying belly
            ok=self.posture.post.goToPosture("LyingBelly", self.POSTURE_CHANGE_SPEED)
        elif command == COMMAND_POSTURE_LYINGBACK:                # posture - lying back
            ok=self.posture.post.goToPosture("LyingBack", self.POSTURE_CHANGE_SPEED)
        elif command == COMMAND_POSTURE_RECORD:                    # posture - record
            global POSTURE_RECORD_FLAG
            global posture_list
            if POSTURE_RECORD_FLAG == False:    
                POSTURE_RECORD_FLAG = True
                self.record_on()
            else:                                
                POSTURE_RECORD_FLAG = False

                posture_name = arg
                self.record_off()
                print ("Record Over:", posture_name)
                posture_list[posture_name] = posture_value
        elif command == COMMAND_POSTURE_RECORD_STOP:            # posture record stop
            POSTURE_RECORD_FLAG = False
            self.motion.setStiffnesses("Body", 1.0)
            self.tts.post.say('stop record')
            self.motion.wakeUp()
            self.motion.rest()
        elif command == COMMAND_POSTURE_CUSTOMER:                # posture - customer
            posture_name = arg
            print "Posture Customer:", posture_name
            self.reappear(posture_name)
        elif command == COMMAND_POSTURE_DELETE:                    # posture - record
            posture_name = arg
            print "Posture delete:", posture_name
            if posture_name in posture_list:
                del posture_list[posture_name]
                self.tts.post.say('delete customer posture.')
            else:
                self.tts.post.say('wrong posture name.')

        elif command == COMMAND_VIDEO_SWITCH_CAMARA:            # switch camera
            self.video.switchCamera()
            print 'switch Camera'

        else:                                                        # error
            print 'Error Command'
        print ok
        if ok==True:
            return 'Success\n'
        else:
            return 'Error\n'

    def mymoveinit(self):
       
        if self.motion.robotIsWakeUp() == False:
            self.motion.post.wakeUp()
            self.motion.post.moveInit()
        else:
            pass
    def sensor(self,interval):
       
        while SENSOR_FLAG == True:
            self.sock.send_str_data("BATTERY" + "'" + str(self.battery.getBatteryCharge()) + "'" + "\n")
            time.sleep(interval)
        # SENSOR_FLAG == False
        thread.exit_thread()

    def LArmInit(self):    
        self.motion.setAngles('LShoulderPitch', 0, 0.2)
        self.motion.setAngles('LShoulderRoll', 0, 0.2)
        self.motion.setAngles('LElbowYaw', 0, 0.2)
        self.motion.setAngles('LElbowRoll', 0, 0.2)
        self.motion.setAngles('LWristYaw', 0, 0.2)
        self.motion.setAngles('LHand', 0, 0.2)
    def RArmInit(self): 
        self.motion.setAngles('RShoulderPitch', 0, 0.2)
        self.motion.setAngles('RShoulderRoll', 0, 0.2)
        self.motion.setAngles('RElbowYaw', 0, 0.2)
        self.motion.setAngles('RElbowRoll', 0, 0.2)
        self.motion.setAngles('RWristYaw', 0, 0.2)
        self.motion.setAngles('RHand', 0, 0.2)
    def LArmUp(self): 
        self.motion.setAngles('LShoulderPitch', 0.7, 0.2)
        self.motion.setAngles('LShoulderRoll', 0.3, 0.2)
        self.motion.setAngles('LElbowYaw', -1.5, 0.2)
        self.motion.setAngles('LElbowRoll', -0.5, 0.2)
        self.motion.setAngles('LWristYaw', -1.7, 0.2)
    def RArmUp(self): 
        self.motion.setAngles('RShoulderPitch', 0.7, 0.2)
        self.motion.setAngles('RShoulderRoll', -0.3, 0.2)
        self.motion.setAngles('RElbowYaw', 1.5, 0.2)
        self.motion.setAngles('RElbowRoll', 0.5, 0.2)
        self.motion.setAngles('RWristYaw', 1.7, 0.2)
    def ArmUp2(self):
       
        self.motion.rest()
        self.motion.wakeUp()
        self.motion.setAngles('RShoulderPitch', 0.7, 0.2)
        self.motion.setAngles('RWristYaw', 1.5, 0.2)
        self.motion.setAngles('LShoulderPitch', 0.7, 0.2)
        self.motion.setAngles('LWristYaw', -1.5, 0.2)
    def LArmMoveInit(self): 
        self.motion.setAngles('LShoulderPitch', 1, 0.2)
        self.motion.setAngles('LShoulderRoll', 0.3, 0.2)
        self.motion.setAngles('LElbowYaw', -1.3, 0.2)
        self.motion.setAngles('LElbowRoll', -0.5, 0.2)
        self.motion.setAngles('LWristYaw', 0, 0.2)
        self.motion.setAngles('LHand', 0, 0.2)

    def RArmMoveInit(self):
        self.motion.setAngles('RShoulderPitch', 1, 0.2)
        self.motion.setAngles('RShoulderRoll', -0.3, 0.2)
        self.motion.setAngles('RElbowYaw', 1.3, 0.2)
        self.motion.setAngles('RElbowRoll', 0.5, 0.2)
        self.motion.setAngles('RWristYaw', 0, 0.2)
        self.motion.setAngles('RHand', 0, 0.2)

    def mysay(self,messages):

        messages=messages.encode('utf-8')
        print 'mesager is: '+messages
        self.tts.say(messages)

        thread.exit_thread()
            
    def record_on(self):

        global motion, tts
        self.motion.rest()
        
        self.tts.say("rest all joints")
        self.motion.setStiffnesses("Body", 0.0)

    def record_off(self):
        global motion, tts

        self.tts.say("lock all joints")
        self.motion.setStiffnesses("Body", 1.0) 

        self.tts.say('recording')
        namelist = motion.getBodyNames('Body')
        anglelist = motion.getAngles('Body', True)
        global posture_value
        posture_value = {}    
        for i in range(len(namelist)):
            posture_value[namelist[i]] = anglelist[i]

        self.tts.say('ok, recorded.')
        self.motion.rest()

    def reappear(self,posture_name):

        global posture_list
        global motion, tts

        if posture_name in posture_list:
            posture_value = posture_list[posture_name]
            self.motion.rest()
            self.motion.setStiffnesses("Body", 1.0)
            self.tts.post.say("reappear recorded posture")
            for name, angle in posture_value.items():
                self.motion.post.setAngles(name, angle, 0.1)
            time.sleep(3)
        else:
            self.tts.post.say('wrong posture name.')
    
    
    def onInput_onStart(self):
        #self.tts.post.say('Pripajam sa')
        self.sock.connect(HOST,TCP_PORT)
        print(self.sock.recieve_str_data())
        #parser loop
        while True:
		
			msg = self.sock.recieve_str_data()
			print('msg: ' + msg)

			arg = msg.split(" ",1)
			print(arg)
			
			response = self.Operation(arg[0],arg[1])
			#self.sock.send_str_data(response)
			
			if "PING" in msg:
				self.sock.send_str_data("PONG\n")
                
			elif "WHOAMI" in msg:
				self.sock.send_str_data('naorobot123456789\n')                
               
			elif "END" in msg:
				break	
				self.onInput_onStop()
        pass

    def onInput_onStop(self):
        self.onUnload()   #it is recommended to reuse the clean-up as the box is stopped
        #self.onStopped() #activate the output of the box

#######################
####  MAIN PROGRAM ####		
cc = ClientClass()
cc.onLoad()
cc.onInput_onStart()
#######################
		
		