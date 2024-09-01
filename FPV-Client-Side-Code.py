#This program runs on the laptop end 
#Authors: B. Yu and A. Martin

import time
import pickle
from pynput.keyboard import *
from threading import Thread
import numpy as np
import socket
import cv2

print("Enter the Pi IP address: ")
ip = input()
port = 5050
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Status list, each index corresponds to control
global status
status = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def press_on(key):
    global status
    print('Press on: {}'.format(key))

    # Key press controls update control status
    if str(key)[1:2] == 'w':
        status[0] = 1
    if str(key)[1:2] == 'a':
        status[1] = 1
    if str(key)[1:2] == 's':
        status[2] = 1
    if str(key)[1:2] == 'd':
        status[3] = 1
    if str(key)[1:2] == 'q':
        status[4] = 1
    if str(key)[1:2] == 'e':
        status[5] = 1
    if str(key)[1:2] == 'k':
        status[6] = 1
    if str(key)[1:2] == ' ':
        status[7] = 1
    if str(key)[1:2] == 'g':
        status[8] = 1
    if str(key)[1:2] == 't':
        status[9] = 1
    if str(key)[1:2] == 'f':
        status[10] = 1
    if str(key)[1:2] == 'r':
        status[11] = 1
    print("press_on: status is %s" % (status))
    time.sleep(.01)

def sendData():
    global status
    while True:
        print("sendData: status is %s" % (status))

        # Converts status list to byte arary for socket
        client.sendto(pickle.dumps(status), (ip, port))
        time.sleep(.01)

def control():
    print("controlling!")

    # Listens to keyboard presses
    with Listener(on_press=press_on) as l:
        l.join()

def press_off(key):
    print('Press off: {}'.format(key))
    global status

    # Resets controls to all off-- allows for short and long press controls
    status = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if key == Key.esc:
        return False

def reset():
    global status
    with Listener(on_release=press_off) as listener:
        listener.join()

def camServer():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    #print(f'Enter your ZeroTier IP address')
    #serverip = '10.61.1.242'
    serverip = input(f' Enter your ZeroTier IP address: ')
    camPort = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((serverip, camPort))

    # Receives camera bytes and opens video stream
    while True:
        data, addr = server.recvfrom(64000)
        print('data received')
        image_bytes = data
        img = np.frombuffer(image_bytes, dtype=np.uint8)
        img2 = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
        cv2.imshow("test", img2)
        k = cv2.waitKey(1)
        time.sleep(0.01)
    cam.release()

t1 = Thread(target=control)
t2 = Thread(target=sendData)
t3 = Thread(target=reset)
t4 = Thread(target=camServer)

t4.start()
print('Sleeping for 20 sec-- type the ip to the pi')
time.sleep(20)
t1.start()
t2.start()
t3.start()
