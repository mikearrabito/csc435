# Michael Arrabito
# CSC 435 - Lab 3

import tkinter as tk
import random
import math


def gethammingcode(code):
    n = len(code)
    r = calcnumcheckbits(len(code))

    hammingcode = ""
    for c in code:
        if c == 'P':
            hammingcode += str(0)
        else:
            hammingcode += c
    
    for i in range(r):
        parity = 0
        for j in range(1, n + 1):
            if (j & (2 ** i) == (2 ** i)):
                parity = parity ^ int(hammingcode[-1 * j])
            hammingcode = hammingcode[:n - (2 ** i)] + str(parity) + hammingcode[n - (2 ** i) + 1:]

    return hammingcode


def checkforerror(code):
    n = len(code)
    nr = calcnumcheckbits(len(sentdata))
    res = 0

    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if (j & (2 ** i) == (2 ** i)):
                val = val ^ int(code[-1 * j])

        res += val * (10 ** i)
    return int(str(res), 2)


def send(data):
    global sentdata
    sentdata = str(data)
    receivedlabel.config(text='Data received: ' + sentdata)
    return


def generateerror(code):
    # Choose random bit in code and flips it
    errorcode = ""
    errbit = random.randrange(0, len(code))
    for i in range(len(code)):
        if i == errbit:
            errorcode += str(int(code[i]) ^ 1)  # Convert to int for xor with 1 to flip, then back to str
        else:
            errorcode += code[i]

    return errorcode


def getcodetosend(n):
    result = ""
    for i in range(n):
        result += str(random.getrandbits(1))
    return result


def ispoweroftwo(n):
    return n & (n - 1) == 0


def getcheckcode(code):
    result = ""
    i = 1
    charindex = 0
    while i < len(code) + calcnumcheckbits(len(code)) + 1:
        if ispoweroftwo(i):
            result += 'P'
        else:
            result += code[charindex]
            charindex += 1
        i += 1
    return result


def calcnumcheckbits(m):
    # take m data bits and find out num of check bits
    # 2**r ≥ m+r+1
    r = 0
    while (2**r) < (m+r+1):
        r += 1
    return r


def correctcode(code):
    errorpos = checkforerror(code)
    if errorpos == 0:
        return code
    code = code[::-1]
    errorpos -= 1
    res = ""
    for i in range(len(code)):
        if i == errorpos:
            res += str(int(code[i]) ^ 1)
        else:
            res += code[i]
    return res[::-1]


def getdata(code):
    res = ""
    for i in range(len(code)):
        if not ispoweroftwo(i+1):
            res += code[i]
    return res


def inputbuttonclick(input):
    global numDataBits, numCheckBits, data, sentdata
    if input == 1:
        numDataBits = int(e1.get())
        databitslabel.config(text='Number of data bits: ' + str(numDataBits))
        checkbitslabel.config(text='Number of check bits: ' + str(calcnumcheckbits(int(e1.get()))))

    if input == 2:
        send(generateerror(gethammingcode(getcheckcode(data))))

    if input == 3:
        data = getcodetosend(numDataBits)
        codelabel.config(text='Bits to be sent: ' + str(data))
        checkcodelabel.config(text='Check Bits: ' + getcheckcode(data))
        hammingcodelabel.config(text='Hamming Code: ' + gethammingcode(getcheckcode(data)))

    if input == 4:
        send(gethammingcode(getcheckcode(data)))

    if input == 5:
        error = checkforerror(sentdata)
        if error == 0:
            errorlabel.config(text='No error detected')
            reclabel.config(text='Received data bits: ' + getdata(sentdata))
        else:
            errorlabel.config(text='Error detected at bit: ' + str(error))  # error bit is # from the right
    if input == 6:
        correctlabel.config(text='Corrected code: ' + correctcode(sentdata))
        reclabel.config(text='Received data bits after correction: ' + getdata(correctcode(sentdata)))
    return


root = tk.Tk()
root.title("Hamming Code App")

e1 = tk.Entry(root, width=5)
e1.grid(row=2, column=0)


e1button = tk.Button(root, text="Click to set number of data bits", command=lambda: inputbuttonclick(1))
e2button = tk.Button(root, text="Send with 1-bit error", command=lambda: inputbuttonclick(2))
e3button = tk.Button(root, text="Generate random code to be sent", command=lambda: inputbuttonclick(3))
e4button = tk.Button(root, text="Send without error", command=lambda: inputbuttonclick(4))
e5button = tk.Button(root, text="Check for error", command=lambda: inputbuttonclick(5))
e6button = tk.Button(root, text="Correct error", command=lambda: inputbuttonclick(6))
e1button.grid(row=3, column=0)
e2button.grid(row=9, column=0)
e3button.grid(row=4, column=0)
e4button.grid(row=8, column=0)
e5button.grid(row=6, column=1)
e6button.grid(row=8, column=1)

numDataBits = 7
numCheckBits = 4
data = ""  # Data to encode and send
sentdata = ""  # Data received

databitslabel = tk.Label(root, text='Number of data bits: ' + str(numDataBits))
checkbitslabel = tk.Label(root, text='Number of check bits: ' + str(numCheckBits))
codelabel = tk.Label(root, text='Bits to be sent: ' + str(data))
checkcodelabel = tk.Label(root, text='Check Bits: ')
hammingcodelabel = tk.Label(root, text='Hamming Code: ')
receivedlabel = tk.Label(root, text='Data received: ')
correctlabel = tk.Label(root, text='Corrected code: ')
reclabel = tk.Label(root, text='Received data bits: ')
errorlabel = tk.Label(root)
databitslabel.grid(row=0, column=0)
checkbitslabel.grid(row=0, column=1)
codelabel.grid(row=5, column=0)
checkcodelabel.grid(row=6, column=0)
hammingcodelabel.grid(row=7, column=0)
receivedlabel.grid(row=5, column=1)
errorlabel.grid(row=7, column=1)
correctlabel.grid(row=9, column=1)
reclabel.grid(row=10, column=0)

root.mainloop()
