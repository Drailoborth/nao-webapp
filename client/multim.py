#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from naoqi import ALProxy
from multiadd import *
from addmovement import *
from time import sleep
from pricitanie import *


def multim(ip,port,paths,inputspeech,Speechmode):
    '''
    :param ip: ip robota
    :param port: port number pre komunikaciu s robotom
    :param paths: cesty k zoznamom zo slovami
    :param inputspeech: vstupny text
    :param RandomBehaviour: prepinac k nahodnemu pohybu

    Funkcia vykonava syntezu reci s pohybmi.
    Medzi kazdou vyslovenou vetou je nastavitelna pauza.
    V logu je vypisany vystup funkcie.
    '''
    str(inputspeech)
	
    Rp = ALProxy("ALRobotPosture", ip, port)
    Tts = ALProxy("ALTextToSpeech", ip, port)
    As = ALProxy("ALAnimatedSpeech", ip, port)
    # Spojenie sa s modulmy v robotovi NAO

    for x in paths:
        try:
            f = open(x,'r')
        except IOError:
            print 'cannot open', x
            return None
    # Kontrola ciest k zoznamom
    if inputspeech is '':
        print 'Enter correct arguments of Inputspeech or Speechmode!'
        return None
    # Kontrola vstupnej vety
    if Speechmode not in [0,1,2]:
        print 'Enter correct arguments of Inputspeech or Speechmode!'
        return None

	
    print (inputspeech)

    if inputspeech.find('#move_forward') != -1:
        move_forward(find_number(inputspeech))

    elif inputspeech.find('#move_back') != -1:
        move_back(find_number(inputspeech))

    elif inputspeech.find('#move_left') != -1:
        move_left(find_number(inputspeech))

    elif inputspeech.find('#move_right') != -1:
        move_right(find_number(inputspeech))

    elif inputspeech.find('#move_turnleft') != -1:
        move_turnleft(find_number(inputspeech))

    elif inputspeech.find('#move_turnright') != -1:
        move_turnright(find_number(inputspeech))

    elif inputspeech.find('#move_turnback') != -1:
        move_turnback()


    elif inputspeech.find('#move_sit') != -1:
        move_sit()
    elif inputspeech.find('#move_stand') != -1:
        move_stand()
    elif inputspeech.find('#move_crouch') != -1:
        move_crouch()
    elif inputspeech.find('#move_lyingBack') != -1:
        move_lyingBack()
    elif inputspeech.find('#move_lyingBelly') != -1:
        move_lyingBelly()
    elif inputspeech.find('#move_StandZero') != -1:
        move_standZero()
    elif inputspeech.find('#move_SitRelax') != -1:
        move_sitRelax()
    elif inputspeech.find('#move_StandInit') != -1:
        move_standInit()
    elif inputspeech.find('#move_hello') != -1:
        move_hello()



    #if inputspeech.find("#move_forward_2")!=-1:
	#print 'Nasiel som move_forward'
    #    addmovement(inputspeech)
    #else:
    #    print 'Nenasiel som nic'
		
    sentence = divide(inputspeech)
    # Rozdelenie vstupneho paragrafu na pole s vetami a suvetiami

    if Speechmode == 0:
        output = ''
        for i in sentence:
            if tagin(i) is False:
                Tts.say(i.encode('utf-8'))
                output = output + i
            else:
                i = tagin(i)
                As.say(i.encode('utf-8'))
                output = output + i

        print output
        return None



    numberoflists = len(paths)
    # Pocet zoznamov s klucovymi slovami

    for j in range(len(sentence)):
        if tagin(sentence[j]) is False:
            for i in range(numberoflists):
                if '^start(' not in sentence[j]:
                    sentence[j] = tagset(sentence[j],paths[i])

        else:
            sentence[j] = tagin(sentence[j])

    # Priradenie tagov podla zoznamu klucovych slov a tagu napisaneho pri vete
    # Vyuzitie uz deklarovanych funkcii

    output = str()

    for counter, element in enumerate(sentence):
        if '^start(' in element:
            if counter != len(sentence)-1:
                output = output + element
                As.say(element.encode('utf-8'))
            else:
                element = element.replace('^wait', '^stop')
                output = output + element
                As.say(element.encode('utf-8'))

        else:
            if Speechmode == 2:
                if counter != len(sentence)-1:
                    output = output + randtag(element)
                    As.say(randtag(element.encode('utf-8')))
                else:
                    element = randtag(element)
                    element = element.replace('^wait', '^stop')
                    output = output + element
                    As.say(element.encode('utf-8'))

            else:
                output = output + element
                Tts.say(element.encode('utf-8'))


    # Inicializacia reci s pohybom
    # Priradzovanie nahodneho neutralneho pohybu v pripade RandomBehaviour je True
    # Ak RandoMBehaviour je False vyuzitie modulu Text-to-Speech
    # Cely vysloveny paragraf sa uklada do premennej output

    # Rp.goToPosture("Stand", 0.6)
    # print output
    # Default pozicia tela
    print output
    return None
    # Vypis vysloveneho paragrafu s prikazmi


#multim('169.254.35.27', 9559, ["First.txt", "Second.txt"], 'Ahoj. Heh.', 2)










