import RPi.GPIO as gpio
import numpy as np
import time
import cv2
import os
import imutils
import math
import serial

trig = 16
echo = 18
file = open("IMUData.txt",'a')
#Indentify serial communication
ser = serial.Serial('/dev/ttyUSB0', 9600)

##### INit the pins

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31, gpio.OUT)
    gpio.setup(33, gpio.OUT)
    gpio.setup(35, gpio.OUT)
    gpio.setup(37, gpio.OUT)
    gpio.setup(36, gpio.OUT)
    gpio.output(36, False)
    gpio.setup(7, gpio.IN, pull_up_down = gpio.PUD_UP)
    gpio.setup(12, gpio.IN, pull_up_down = gpio.PUD_UP)
    
def gameover():
    gpio.output(31, False)
    gpio.output(33, False)
    gpio.output(35, False)
    gpio.output(37, False)
    
    gpio.cleanup()


def forward(maxTicks):
    init()
    counterBR = np.uint64(0)
    counterFL = np.uint64(0)

    buttonBR = int(0)
    buttonFL = int(0)

    # Initialize pwm signal to control motor
    pwm1 = gpio.PWM(37, 50) #Right side
    pwm2 = gpio.PWM(31, 50) #Left side
    val = 40
    pwm1.start(val)
    pwm2.start(val)
    time.sleep(0.1)


    while True:
        #print("counterBR = ", counterBR,"counterFL = ", counterFL, "BR state: ", gpio.input(12), "FL state: ", gpio.input(7))
        #file.write(str(counterBR)+","+str(counterFL)+","+str(gpio.input(12))+","+str(gpio.input(7))+'\n')
        
        if int(gpio.input(12)) != int(buttonBR):
            buttonBR = int(gpio.input(12))
            counterBR += 1
            
        if int(gpio.input(7)) != int(buttonFL):
            buttonFL = int(gpio.input(7))
            counterFL += 1
            #print(counter)
            
        if counterBR >= maxTicks:
            pwm1.stop()
            
        if counterFL >= maxTicks:
            pwm2.stop()
            
        if counterFL >= maxTicks and counterBR >= maxTicks:
            pwm1.stop()
            pwm2.stop()
            gameover()
            #Read serial stream
            line = ser.readline() #print(line)
            line = line.rstrip().lstrip()
            line = str(line)
            line = line.strip("'")
            line = line.strip("b'")
            #print(line)
        
            #Return float
            currAngle = float(line)
            #file.write(str(currAngle)+'\n')
            file.write(str(currAngle)+','+str(maxTicks/98)+'\n')
            break


def reverse(maxTicks):
    init()
    counterBR = np.uint64(0)
    counterFL = np.uint64(0)

    buttonBR = int(0)
    buttonFL = int(0)

    # Initialize pwm signal to control motor
    pwm1 = gpio.PWM(33, 50) #Right side
    pwm2 = gpio.PWM(35, 50) #Left side
    val = 40
    pwm1.start(val)
    pwm2.start(val)
    time.sleep(0.1)


    while True:
        #print("counterBR = ", counterBR,"counterFL = ", counterFL, "BR state: ", gpio.input(12), "FL state: ", gpio.input(7))
        #file.write(str(counterBR)+","+str(counterFL)+","+str(gpio.input(12))+","+str(gpio.input(7))+'\n')
        
        if int(gpio.input(12)) != int(buttonBR):
            buttonBR = int(gpio.input(12))
            counterBR += 1
            
        if int(gpio.input(7)) != int(buttonFL):
            buttonFL = int(gpio.input(7))
            counterFL += 1
            #print(counter)
            
        if counterBR >= maxTicks:
            pwm2.stop()
            
        if counterFL >= maxTicks:
            pwm1.stop()
            
        if counterFL >= maxTicks and counterBR >= maxTicks:
            pwm1.stop()
            pwm2.stop()
            gameover()
            #Read serial stream
            line = ser.readline() #print(line)
            line = line.rstrip().lstrip()
            line = str(line)
            line = line.strip("'")
            line = line.strip("b'")
            #print(line)
        
            #Return float
            currAngle = float(line)
            #file.write(str(currAngle)+'\n')
            file.write(str(currAngle)+','+str(maxTicks/98)+'\n')
            break


def pivotright(angle):#maxTicks):
    init()
    offset = 1 #degrees
    counterBR = np.uint64(0)
    counterFL = np.uint64(0)

    buttonBR = int(0)
    buttonFL = int(0)

    # Initialize pwm signal to control motor
    pwm1 = gpio.PWM(31, 50) #Right side
    pwm2 = gpio.PWM(35, 50) #Left side
    val = 35
    pwm1.start(val)
    pwm2.start(val)
    time.sleep(0.1)
    
    if ser.in_waiting > 0:
        line = ser.readline() #print(line)
        line = line.rstrip().lstrip()
        line = str(line)
        line = line.strip("'")
        line = line.strip("b'")
        #print(line)
        
        #Return float
        goalAngle = (float(line) + angle)%360


    while True:
        #print("counterBR = ", counterBR,"counterFL = ", counterFL, "BR state: ", gpio.input(12), "FL state: ", gpio.input(7))
        
        #Read serial stream
        line = ser.readline() #print(line)
        line = line.rstrip().lstrip()
        line = str(line)
        line = line.strip("'")
        line = line.strip("b'")
        #print(line)
        
        #Return float
        currAngle = float(line)
        #file.write(str(currAngle)+'\n')
        
        #file.write(str(counterBR)+","+str(counterFL)+","+str(gpio.input(12))+","+str(gpio.input(7))+'\n')
        if int(gpio.input(12)) != int(buttonBR):
            buttonBR = int(gpio.input(12))
            counterBR += 1
            
        if int(gpio.input(7)) != int(buttonFL):
            buttonFL = int(gpio.input(7))
            counterFL += 1

        if currAngle+offset >= goalAngle and currAngle-offset <= goalAngle:
            pwm1.stop()
            pwm2.stop()
            gameover()
            break




def pivotleft(angle):#maxTicks):
    init()
    offset = 1 #degrees
    counterBR = np.uint64(0)
    counterFL = np.uint64(0)

    buttonBR = int(0)
    buttonFL = int(0)

    # Initialize pwm signal to control motor
    pwm1 = gpio.PWM(33, 50) #Right side
    pwm2 = gpio.PWM(37, 50) #Left side
    val = 35
    pwm1.start(val)
    pwm2.start(val)
    time.sleep(0.1)
    
    if ser.in_waiting > 0:
        line = ser.readline() #print(line)
        line = line.rstrip().lstrip()
        line = str(line)
        line = line.strip("'")
        line = line.strip("b'")
        #print(line)
        
        #Return float
        goalAngle = (float(line) - angle)%360

    while True:
        #print("counterBR = ", counterBR,"counterFL = ", counterFL, "BR state: ", gpio.input(12), "FL state: ", gpio.input(7))
         
        #Read serial stream
        line = ser.readline() #print(line)
        line = line.rstrip().lstrip()
        line = str(line)
        line = line.strip("'")
        line = line.strip("b'")
        #print(line)
        
        #Return float
        currAngle = float(line)
        #file.write(str(currAngle)+'\n')
        
        #file.write(str(counterBR)+","+str(counterFL)+","+str(gpio.input(12))+","+str(gpio.input(7))+'\n')
        if int(gpio.input(12)) != int(buttonBR):
            buttonBR = int(gpio.input(12))
            counterBR += 1
            
        if int(gpio.input(7)) != int(buttonFL):
            buttonFL = int(gpio.input(7))
            counterFL += 1

        if currAngle+offset >= goalAngle and currAngle-offset <= goalAngle:
            pwm1.stop()
            pwm2.stop()
            gameover()
            break
            
    
def closeGripper():
    gpio.setmode(gpio.BOARD)
    gpio.setup(36, gpio.OUT)  #Gripper
    
    pwm = gpio.PWM(36, 50)
    pwm.start(5)
    
    rate = 0.15
    duty = float(3.5)
    while True:
        duty += rate
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.2)
        if duty >= 6.5:#6.25:
            break
    pwm.stop()
    #clear the output pins
    #GPIO.cleanup() 

def openGripper():
    gpio.setmode(gpio.BOARD)
    gpio.setup(36, gpio.OUT)  #Gripper
    
    pwm = gpio.PWM(36, 50)
    pwm.start(5)
    
    rate = 0.15
    duty = float(6)
    while True:
        pwm.ChangeDutyCycle(duty)
        duty -= rate        
        time.sleep(0.2)
        if duty <= 3.5:
            break
    pwm.stop()
    #clear the output pins
    #GPIO.cleanup() 
            
def distance():
    gpio.setmode(gpio.BOARD)
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    
    #Ensure outout has no value
    gpio.output(trig, False)
    time.sleep(0.01)

    #Generate Trigger pulse
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    #Generate Echo time signal
    while gpio.input(echo) == 0:
        pulse_start = time.time()

    while gpio.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    #Convert time to distance
    distance = pulse_duration*17150
    distance = round(distance, 2)
        
    #clear the output pins
    gpio.cleanup()        
    return distance

def key_input(event):
    init()
    print("Key: ", event)
    key_press = event
    
    if key_press.lower() == 'w':
        x = input('Enter distance in meters:')
        dist = float(x)
        maxticks = 98 * dist
        forward(maxticks)
    elif key_press.lower() == 's':
        x = input('Enter distance in meters:')
        dist = float(x)
        maxticks = 98 * dist
        reverse(maxticks)
    elif key_press.lower() == 'a':
        x = input('Enter angle in degrees:')
        angle = float(x)
        #maxticks = math.ceil(0.1444 * angle)
        pivotleft(angle)#maxticks)
    elif key_press.lower() == 'd':
        x = input('Enter angle in degrees:')
        angle = float(x)
        #maxticks = math.ceil(0.1444 * angle)
        pivotright(angle)#maxticks)
    elif key_press.lower() == 'x':
        closeGripper()
    elif key_press.lower() == 'c':
        openGripper()
    else:
        print("Invalid key pressed!")
    
    #distance_sum = 0;
    #for i in range(0,10):
    #    distance_sum = distance_sum + distance()
    
    #avg_distance = distance_sum / 10
    #print("Distance for closest object in the front: "+str(avg_distance)+"cm")

if __name__ == '__main__':
    read_trash = ser.readline()
    line = ser.readline() #print(line)
    line = line.rstrip().lstrip()
    line = str(line)
    line = line.strip("'")
    line = line.strip("b'")
    
    currAngle = float(line)
    file.write(str(currAngle)+','+'0.00'+'\n')
    while True:
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            gpio.cleanup()
            file.close()
            break
        key_input(key_press)
    
            

