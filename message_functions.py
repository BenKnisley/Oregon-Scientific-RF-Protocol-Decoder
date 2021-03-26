"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 26 March, 2021
"""

def process_message(data):
    ## Convert manchesterSignal into rawSignal by remove first and then every other
    ## As each bit is sent twice and inverted
    dataSignal = data[1::2]

    ## Split dataSignal into list of 4 chars for each nimble
    dataSignal = [dataSignal[i:i+4] for i in range(0, len(dataSignal), 4)]

    ## Flip each nimble to get real binary value
    dataSignal = [x[::-1] for x in dataSignal]

    ## If signal is not aligned right, fix it
    if dataSignal[1] == '0000':
        tempDataSig = list()
        for nimble in dataSignal:
            #! Fix this, make better code
            nimble = nimble.replace('0', 'x')
            nimble = nimble.replace('1', 'y')
            nimble = nimble.replace('x', '1')
            nimble = nimble.replace('y', '0')
            tempDataSig.append(nimble)
        dataSignal = tempDataSig

    ## Convert each nimble into a hex char
    hexString = ''
    for nimble in dataSignal:
        hexString += str( hex( int(nimble, 2) ) )[2:]
    
    return(hexString)


def hex2data(hexString):
    try:
        ## Process hexString into data
        ID = hexString[5:][:4]
        chan = hexString[9:][:1]
        flag = hexString[12:][:1]

        if hexString[16:][:1] == '0':
            temp = float(hexString[13:][:3][::-1]) * 0.1
        else:
            temp = float(hexString[13:][:3][::-1]) * -0.1

        hum = int(hexString[17:][:2][::-1])

        ## Return success status, and data list
        return True, [ID, chan, flag, temp, hum]

    ## If anything fails, then return fail status, and empty data list
    except:
        return False, []


