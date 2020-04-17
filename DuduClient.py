#These are the comments provided by olliz0r. These may be useful if you need to calibrate for other languages
#Commands:
#make sure to append \r\n to the end of the command string or the switch args parser might not work
#responses end with a \n (only poke has a response atm)

#click A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#press A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#release A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE

#peek <address in hex, prefaced by 0x> <amount of bytes, dec or hex with 0x>
#poke <address in hex, prefaced by 0x> <data, if in hex prefaced with 0x>

#setStick LEFT/RIGHT <xVal from -0x8000 to 0x7FFF> <yVal from -0x8000 to 0x7FFF


import binascii
import struct
import time
import usb.core
import usb.util
from PK8 import *
from NumpadInterpreter import *

global_dev = None
global_out = None
global_in = None

#Sends string commands to the switch
def sendCommand(content):
    global_out.write(struct.pack("<I", (len(content)+2)))
    global_out.write(content)

def readData():
    size = int(struct.unpack("<L", global_in.read(4, timeout=0).tobytes())[0])

    #Converts received data to integer array
    data = [0] * size
    x = global_in.read(size, timeout=0).tobytes()
    for i in range(size):
        data[i] = int(x[i])
    return data

#Using method from Goldleaf
def connect_switch():
    global global_dev
    global global_out
    global global_in
    global_dev = usb.core.find(idVendor=0x057E, idProduct=0x3000)
    if global_dev is not None:
        try:
            global_dev.set_configuration()
            intf = global_dev.get_active_configuration()[(0,0)]
            global_out = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_OUT)
            global_in = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_IN)
            return True
        except:
            return False
            pass
    else:
        return False

#To communicate with the user
def attemptConnection():
    isConnected = False
    while not isConnected:
        if connect_switch():
            print("Connected to Switch Successfully!")
            isConnected = True
        else:
            print("Failed to Connect to Switch!")
            print("Attempting to Reconnect in 5 Seconds...")
            time.sleep(5)

#New interpreter for new packet structure
def bytesToInt(bytedata, length):
        data = list()
        j = 0
        i = 0
        while j < length:
            if bytedata[j] == 0x0A:
                break
            digit = str(chr(bytedata[i])) + str(chr(bytedata[i+1]))
            data.append(int(digit, 16))
            j += 1
            i += 2

        return data

#New interpreter for new packet structure
def convertToString(arr):
    size = len(arr)
    i = 0
    accumulator = ""
    while i < size:
        accumulator = accumulator + '{:02x}'.format(int(arr[i]), 'x')
        i += 1

    return accumulator

#New interpreter for new packet structure
def convertToBytes(arr):
    size = len(arr)
    i = 0
    accumulator = ""
    while i < size:
        if arr[i] == 0xA:
            break
        accumulator = accumulator + str(chr(arr[i]))
        i += 1

    return accumulator

#Cleans out the file relied for communication
def cleanEnvironment():
    fileOut = open("communicate.bin", "wb")
    outData = list()
    outData.append(0)
    outData.append(0)
    outData.append(0)
    fileOut.write(bytes(outData))
    fileOut.close()

#Writes timeout flag to file
def timedOut():
    fileOut = open("communicate.bin", "wb")
    outData = list()
    outData.append(0)
    outData.append(0)
    outData.append(1)
    fileOut.write(bytes(outData))
    fileOut.close()

#Interprets sequence of strings in arraylist
def interpretStringList(arr):
    length = len(arr)
    i = 0
    while i < length:
        sendCommand(arr[i])
        i+=1
        time.sleep(0.2)

#Calibrated for games set to english
#Will exit the trade once the timeout period is reached
def timeOutTradeSearch():
    sendCommand('click Y')
    time.sleep(1)
    sendCommand("click A")
    time.sleep(0.7)
    sendCommand("click A")
    time.sleep(0.55)
    sendCommand("click A")
    time.sleep(0.55)
    sendCommand("click A")
    time.sleep(0.7)
    sendCommand("click A")
    time.sleep(0.9)

    #uncomment if you are using in Japanese
    #sendCommand("click A")
    #time.sleep(0.7)
    sendCommand("click B")
    time.sleep(0.7)
    sendCommand("click B")
    time.sleep(0.55)


#Exits trade if a disconnection occured
#or if the player refused to input a pokemon
def exitTrade():
    sendCommand("click B")
    time.sleep(0.7)
    sendCommand("click A")
    time.sleep(0.7)

#Calibrated for games set to english
#Starts up trade and inputs code
def initiateTrade():
    global code

    #Gets to the code input menu
    sendCommand('click Y')
    time.sleep(0.8)
    sendCommand('click A')
    time.sleep(0.7)
    sendCommand('click DDOWN')
    time.sleep(0.7)
    sendCommand('click A')
    time.sleep(0.7)
    sendCommand('click A')
    time.sleep(0.9) #Change to 0.7 if you are using in Japanese

    #uncomment if you are using in Japanese
    #sendCommand('click A')
    #time.sleep(0.9)


    #Get passcode button sequence and input them
    #Pass None if you want your code randomly generated
    #Pass in a 4 digit number not containing any zeros for a fixed code
    datalist, code = getButtons(None)
    interpretStringList(datalist)

    #Confirm passcode and exit the menu
    sendCommand('click PLUS')
    time.sleep(0.7)
    sendCommand('click A')
    time.sleep(0.7)
    sendCommand('click A')
    time.sleep(0.7)
    sendCommand('click A')
    time.sleep(0.7)
    sendCommand('click A')
    time.sleep(0.7)

    #Just to be safe since this is a very important part
    sendCommand(f"poke 0x2E32209A 0x00000000")
    sendCommand(f"poke 0x2E322064 0x00000000")

#Start up program and clean up necessary files
attemptConnection()
print("Cleaning environment...")
cleanEnvironment()
print("Environment cleaned!")
print("Awaiting inputs...")



while True:
    fileIn = open("communicate.bin", "rb")
    fileIn.seek(0)
    tradeState = int(fileIn.read()[0])
    
    if tradeState == 1:
        print("Bot initialized!")
        fileIn.close()
        initiateTrade()

        fcode = open("code.txt", "w")
        fcode.write(code)
        fcode.close()
        
        fileOut = open("communicate.bin", "wb")

        outData = list()
        outData.append(0)
        outData.append(1)
        outData.append(0)

        fileOut.write(bytes(outData))
        fileOut.close()

        canTrade = True

        start = time.time()
        while True:
            sendCommand("peek 0x2E322064 4")
            tradeCheck = readData()
            tradeCheck = int(convertToString(tradeCheck), 16)
            end = time.time()
            if tradeCheck != 0:
                print("Trade Started!")
                canTrade = True
                break
            if (end - start) >= 60:
                timeOutTradeSearch()
                timedOut()
                canTrade = False
                print("No Trade Found.")
                break
        if canTrade:
            start = time.time()
            while True:
                sendCommand("peek 0x2E32209A 4")
                memCheck = readData()
                memCheck = int(convertToString(memCheck), 16)
                #print(memCheck)
                end = time.time()
                if memCheck != 0:
                    canTrade = True
                    break
                if (end - start) >= 40:
                    exitTrade()
                    timedOut()
                    canTrade = False
                    break

            
            if canTrade:
                exitTrade()
                sendCommand("peek 0x2E32206A 328")
                time.sleep(0.5)

                ek8 = readData()
                decryptor = PK8(ek8)
                decryptor.decrypt()
                pk8 = decryptor.getData()

                ec = decryptor.getEncryptionConstant()
                pid = decryptor.getPID()

                pk8Out = open("out.pk8", "wb")
                pk8Out.write(bytes(pk8))
                pk8Out.close()

                fileOut = open("communicate.bin", "wb")
                outData = list()
                outData.append(0)
                outData.append(0)
                outData.append(0)
                fileOut.write(bytes(outData))
                fileOut.close()

                print("Encryption Constant: " + str(hex(ec)))
                print("pid: " + str(hex(pid)))
    time.sleep(1)

                
        print("Awaiting inputs...")
